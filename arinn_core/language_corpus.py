
import chromadb
import uuid
import logging
import random

class LanguageCorpus:
    """
    Vector Database for Language Acquisition.
    Stores high-quality text fragments to use as style/content references (RAG).
    """
    def __init__(self, db_path="arinn_language.db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="english_mastery")
        
    def ingest_text(self, text, source="unknown", tags=None):
        """
        'Reads' a text implementation -> Embeds into Vector DB.
        """
        # Chunking
        sentences = text.split('.')
        chunks = ['.'.join(sentences[i:i+3]).strip() for i in range(0, len(sentences), 3) if len(sentences[i:i+3]) > 0]
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": source, "tag": t} for t in (tags or []) for _ in chunks]
        # Allow single metadata dict per item if tags is list, simplified for now:
        metadatas = [{"source": source} for _ in chunks]
        
        if chunks:
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            return len(chunks)
        return 0

    def recall_relevant(self, query, n_results=1):
        """
        Retrieves relevant text fragments to use as context/style guides.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            if results['documents']:
                return results['documents'][0] # List of results for first query
            return []
        except Exception as e:
            logging.error(f"RAG Error: {e}")
            return []

    def get_random_sample(self):
        """For practice."""
        count = self.collection.count()
        if count == 0: return None
        # Chroma doesn't support random fetch easily, we just query a generic word
        return self.recall_relevant("the", n_results=1)[0]
