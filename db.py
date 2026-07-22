import hashlib
import os
import sqlite3
import json
from typing import List, Optional, Tuple, Dict


def _connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def _hash_text(text: str) -> str:
    normalized = " ".join(text.split())
    return hashlib.sha256(normalized.encode("utf-8", errors="ignore")).hexdigest()


class Database:
    def __init__(self, db_path: str):
        self.remote_url = os.getenv("ARINN_REMOTE_URL")
        if self.remote_url:
            print(f"[RAG] Data Lake Configured. Hoisting DB physical constraints to remote: {self.remote_url}")
            return # Disable OS allocation bounds entirely

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = _connect(db_path)
        self._init_schema()

    def _remote_sync(self, table: str, payload: dict) -> Tuple[bool, Optional[int]]:
        """Unified RPC sync tunnel isolating logic from the remote Data Lake implementation"""
        try:
            import requests # type: ignore
            response = requests.post(
                f"{self.remote_url.rstrip('/')}/api/ingest", 
                json={"table": table, "data": payload}, 
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return True, data.get("inserted_id", 0)
            return False, None
        except Exception as e:
            print(f"[RAG] Remote sync collapsed: {e}")
            return False, None

    def _init_schema(self):
        cur = self.conn.cursor()
        cur.executescript(
            """
            PRAGMA journal_mode=WAL;
            PRAGMA busy_timeout=30000;
            CREATE TABLE IF NOT EXISTS topics (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS documents (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              topic_id INTEGER NOT NULL,
              url TEXT,
              title TEXT,
              content_hash TEXT NOT NULL,
              content TEXT,
              created_at TEXT NOT NULL,
              UNIQUE(topic_id, content_hash),
              FOREIGN KEY(topic_id) REFERENCES topics(id)
            );
            CREATE TABLE IF NOT EXISTS snippets (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              topic_id INTEGER NOT NULL,
              doc_id INTEGER,
              snippet_hash TEXT NOT NULL,
              text TEXT NOT NULL,
              created_at TEXT NOT NULL,
              UNIQUE(topic_id, snippet_hash),
              FOREIGN KEY(topic_id) REFERENCES topics(id),
              FOREIGN KEY(doc_id) REFERENCES documents(id)
            );
            CREATE TABLE IF NOT EXISTS questions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              topic_id INTEGER NOT NULL,
              question TEXT NOT NULL,
              asked_at TEXT NOT NULL,
              status TEXT NOT NULL DEFAULT 'pending',
              FOREIGN KEY(topic_id) REFERENCES topics(id)
            );
            CREATE TABLE IF NOT EXISTS image_ratings (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              image_url TEXT NOT NULL,
              image_title TEXT,
              image_source TEXT,
              category TEXT,
              rating TEXT NOT NULL,  -- 'up' or 'down'
              rated_at TEXT NOT NULL,
              search_query TEXT,  -- what was searched for
              UNIQUE(image_url, search_query)
            );
            CREATE INDEX IF NOT EXISTS idx_documents_topic_id ON documents(topic_id);
            CREATE INDEX IF NOT EXISTS idx_snippets_topic_id ON snippets(topic_id);
            CREATE INDEX IF NOT EXISTS idx_questions_topic_id ON questions(topic_id);
            CREATE INDEX IF NOT EXISTS idx_questions_status ON questions(status);
            """
        )
        self.conn.commit()

    # ----- Topics -----
    def get_or_create_topic(self, name: str) -> int:
        if getattr(self, "remote_url", None):
            success, topic_id = self._remote_sync("topics", {"name": name})
            return topic_id or 1 # Fallback ID logic for remote

        cur = self.conn.cursor()
        cur.execute("SELECT id FROM topics WHERE name = ?", (name,))
        row = cur.fetchone()
        if row:
            return int(row[0])
        cur.execute(
            "INSERT INTO topics(name, created_at) VALUES(?, datetime('now'))",
            (name,),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def list_topics(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, created_at FROM topics ORDER BY created_at DESC")
        return [dict(r) for r in cur.fetchall()]

    def get_total_documents_count(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM documents")
        row = cur.fetchone()
        return int(row[0]) if row else 0

    # ----- Documents & Snippets -----
    def add_document(self, topic_id: int, url: Optional[str], title: str, content: str, created_at: str) -> Tuple[bool, Optional[int]]:
        h = _hash_text(content)
        if getattr(self, "remote_url", None):
            return self._remote_sync("documents", {"topic_id": topic_id, "url": url, "title": title, "content_hash": h, "content": content, "created_at": created_at})

        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT INTO documents(topic_id, url, title, content_hash, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (topic_id, url, title, h, content, created_at),
            )
            self.conn.commit()
            return True, int(cur.lastrowid)
        except sqlite3.IntegrityError:
            return False, None

    def add_snippets_from_text(self, topic_id: int, doc_id: int, text: str, created_at: str, min_len: int = 200):
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        
        if getattr(self, "remote_url", None):
            for p in parts:
                if len(p) >= min_len:
                    self._remote_sync("snippets", {"topic_id": topic_id, "doc_id": doc_id, "snippet_hash": _hash_text(p), "text": p, "created_at": created_at})
            return

        cur = self.conn.cursor()
        for p in parts:
            if len(p) < min_len:
                continue
            h = _hash_text(p)
            try:
                cur.execute(
                    "INSERT INTO snippets(topic_id, doc_id, snippet_hash, text, created_at) VALUES(?,?,?,?,?)",
                    (topic_id, doc_id, h, p, created_at),
                )
            except sqlite3.IntegrityError:
                continue
        self.conn.commit()

    def get_recent_docs(self, topic_id: int, limit: int = 10) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, url, title, content FROM documents WHERE topic_id = ? ORDER BY id DESC LIMIT ?",
            (topic_id, limit),
        )
        return [dict(r) for r in cur.fetchall()]

    # ----- Questions -----
    def add_questions(self, topic_id: int, questions: List[str], asked_at: str):
        cur = self.conn.cursor()
        for q in questions:
            qn = q.strip()
            if not qn:
                continue
            cur.execute(
                "INSERT INTO questions(topic_id, question, asked_at, status) VALUES (?,?,?, 'pending')",
                (topic_id, qn, asked_at),
            )
        self.conn.commit()

    def pop_next_pending_question(self, topic_id: int) -> Optional[Tuple[int, str]]:
        if getattr(self, "remote_url", None):
            try:
                import requests # type: ignore
                r = requests.get(f"{self.remote_url.rstrip('/')}/api/questions/pending", params={"topic_id": topic_id}, timeout=5)
                if r.status_code == 200 and r.json().get("data"):
                    q_data = r.json().get("data")[0]
                    return q_data["id"], q_data["question"]
            except Exception:
                pass
            return None

        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, question FROM questions WHERE topic_id = ? AND status = 'pending' ORDER BY id ASC LIMIT 1",
            (topic_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return int(row[0]), str(row[1])

    def mark_question_done(self, question_id: int):
        cur = self.conn.cursor()
        cur.execute("UPDATE questions SET status = 'done' WHERE id = ?", (question_id,))
        self.conn.commit()

    def count_pending_questions(self, topic_id: int) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM questions WHERE topic_id = ? AND status = 'pending'", (topic_id,))
        row = cur.fetchone()
        return int(row[0]) if row else 0

    # ----- Image Ratings -----
    def save_image_rating(self, image_url: str, image_title: str, image_source: str,
                         category: str, rating: str, search_query: str, rated_at: str) -> bool:
        """Save an image rating to the database."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT OR REPLACE INTO image_ratings
                (image_url, image_title, image_source, category, rating, search_query, rated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (image_url, image_title, image_source, category, rating, search_query, rated_at),
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving image rating: {e}")
            return False

    def get_image_ratings_for_category(self, category: str, limit: int = 100) -> List[Dict]:
        """Get historical ratings for a specific category."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM image_ratings WHERE category = ? ORDER BY rated_at DESC LIMIT ?",
            (category, limit),
        )
        return [dict(r) for r in cur.fetchall()]

    def get_popular_categories(self, limit: int = 10) -> List[Dict]:
        """Get most rated categories with their average ratings."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                category,
                COUNT(*) as total_ratings,
                SUM(CASE WHEN rating = 'up' THEN 1 ELSE 0 END) as positive_ratings,
                ROUND(AVG(CASE WHEN rating = 'up' THEN 1.0 ELSE 0.0 END), 2) as positive_ratio
            FROM image_ratings
            GROUP BY category
            ORDER BY total_ratings DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]

    def get_rating_stats(self) -> Dict[str, int]:
        """Get overall rating statistics."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM image_ratings")
        total_ratings = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM image_ratings WHERE rating = 'up'")
        positive_ratings = cur.fetchone()[0]

        return {
            "total_ratings": total_ratings,
            "positive_ratings": positive_ratings,
            "negative_ratings": total_ratings - positive_ratings
        }

    def get_genesis_start_time(self) -> Optional[str]:
        """Physical anchor to retroactively compute temporal uptime if the script restarts."""
        if self.remote_url:
            return None
        cur = self.conn.cursor()
        cur.execute("SELECT min(asked_at) FROM questions")
        row = cur.fetchone()
        return row[0] if row else None

    # ----- Utils -----
    @staticmethod
    def make_excerpt(text: str, max_len: int = 600) -> str:
        t = " ".join(text.split())
        if len(t) <= max_len:
            return t
        return t[: max_len - 3] + "..."

