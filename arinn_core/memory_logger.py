
import os
import json
import time

try:
    import chromadb  # type: ignore
except ImportError:
    chromadb = None

class MemoryLogger:
    """
    Phase 79: Mnemosyne Protocol.
    Logs 'Golden' interactions for offline training AND
    stores them in ChromaDB for Online In-Context Learning (RAG).
    """
    def __init__(self, data_dir="training_data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            
        self.log_file = os.path.join(self.data_dir, "golden_memories.jsonl")
        
        # Initialize Vector Store
        self.vector_db = None
        self.collection = None
        
        if chromadb:
            try:
                # Persistent Client
                db_path = os.path.join(self.data_dir, "chroma_db")
                self.vector_db = chromadb.PersistentClient(path=db_path)
                
                # Get/Create Collection
                self.collection = self.vector_db.get_or_create_collection(  # type: ignore
                    name="arinn_golden_memories",
                    metadata={"hnsw:space": "cosine"}
                )
                print(f"[LOGGER] ChromaDB Connected ({self.collection.count()} memories).")  # type: ignore
            except Exception as e:
                print(f"[LOGGER] ChromaDB Init Error: {e}")
        else:
            print("[LOGGER] ChromaDB not installed. RAG disabled.")
        
    def log_golden_memory(self, prompt, code, metadata=None):
        """
        Appends a verified example to the training log AND Vector Store.
        """
        timestamp = time.time()
        
        # 1. JSONL (Offline Training)
        entry = {
            "conversations": [
                {"from": "human", "value": prompt},
                {"from": "gpt", "value": code}
            ],
            "timestamp": timestamp,
            "metadata": metadata or {}
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            # print(f"[LOGGER] Saved to JSONL.")
        except Exception as e:
            print(f"[LOGGER] JSONL Save Error: {e}")
            return False
            
        # 2. Vector Store (Online RAG)
        if self.collection:
            try:
                # We embed the PROMPT (The Task)
                # Metadata contains the CODE (The Solution)
                # ID is timestamp
                
                # Truncate content for metadata limit safety if needed, though Chroma handles decent size.
                self.collection.add(  # type: ignore
                    documents=[prompt],
                    metadatas=[{"solution": code[:4000], "timestamp": timestamp}], # Chroma metadata has limits? Usually OK.
                    ids=[str(timestamp)]
                )
                print(f"[LOGGER] Embedded in ChromaDB.")
            except Exception as e:
                print(f"[LOGGER] Vector Save Error: {e}")
                
        return True

    def retrieve_relevant_memory(self, query, n_results=1):
        """
        Finds the most similar past solved task to the current query.
        Returns: matching_code (str) or None
        """
        if not self.collection:
            return None
            
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results and results['ids'][0]:
                # Found a match
                # Check distance/score if desired (lower is better for cosine distance in some libs, but Chroma returns distance)
                # Chroma default is L2 or Cosine. If Cosine Distance, 0 is identical, 1 is orthogonal.
                # Let's assume valid.
                
                # Return the solution from metadata
                solution = results['metadatas'][0][0]['solution']
                original_task = results['documents'][0][0]
                
                return {"task": original_task, "solution": solution}
                
        except Exception as e:
            # print(f"[LOGGER] Retrieval Failed: {e}")
            pass
            
        return None
