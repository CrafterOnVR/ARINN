import os
import sqlite3
import sys

# Ensure correct path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from memory_manager import MemoryManager

def migrate():
    print("Initializing MemoryManager...")
    memory = MemoryManager(root=project_root)
    
    db_path = os.path.join(project_root, "data", "research.db")
    if not os.path.exists(db_path):
        print(f"Error: {db_path} does not exist.")
        return
        
    print("Connecting to SQLite...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # We will migrate documents
    cur.execute("SELECT id, topic_id, url, title, content FROM documents WHERE content IS NOT NULL AND content != ''")
    rows = cur.fetchall()
    
    total = len(rows)
    print(f"Found {total} documents to migrate.")
    
    batch_size = 100
    for i in range(0, total, batch_size):
        batch = rows[i:i+batch_size]
        docs = []
        metas = []
        ids = []
        for row in batch:
            doc_id_db, topic_id, url, title, content = row
            docs.append(content[:20000]) # Prevent massive strings from choking the embedder
            metas.append({"source": "genesis_run", "url": url[:255] if url else "", "topic_id": topic_id, "title": title[:255] if title else ""})
            ids.append(f"doc_{doc_id_db}")
            
        try:
            memory.add_memories(documents=docs, metadatas=metas, ids=ids)
            print(f"Migrated batch {i // batch_size + 1}/{(total + batch_size - 1) // batch_size} ({len(batch)} documents)")
        except Exception as e:
            print(f"Error migrating batch: {e}")
            
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
