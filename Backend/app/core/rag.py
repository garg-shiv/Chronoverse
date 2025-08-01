import chromadb
from sentence_transformers import SentenceTransformer
import logging
from typing import List, Dict, Optional
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class HistoricalKnowledgeBase:
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.encoder = None
        self.client = None
        self.collections = {}
        
        logger.info(f"🧠 Initializing Historical Knowledge Base with model: {model_name}")
        self._initialize()
    
    def _initialize(self):
        try:
            self.client = chromadb.PersistentClient(path="./knowledge_db")
            logger.info("✅ ChromaDB client initialized")
            
            logger.info(f"📥 Loading sentence transformer model: {self.model_name}")
            self.encoder = SentenceTransformer(self.model_name)
            logger.info("✅ Sentence transformer model loaded")
            
            self._create_character_collections()
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize knowledge base: {e}")
            raise Exception(f"Could not initialize RAG system: {e}")
    
    def _create_character_collections(self):
        characters = [
            "roman_gladiator",
            "mughal_architect", 
            "egyptian_scribe"
        ]
        
        for character in characters:
            try:
                collection = self.client.get_or_create_collection(
                    name=f"{character}_knowledge",
                    metadata={"character": character, "created": str(datetime.now())}
                )
                self.collections[character] = collection
                logger.info(f"✅ Collection ready for {character}")
            except Exception as e:
                logger.error(f"❌ Failed to create collection for {character}: {e}")
    
    def add_knowledge(self, character_id: str, facts: List[Dict[str, str]]):
        if character_id not in self.collections:
            logger.error(f"❌ Unknown character: {character_id}")
            return False
        
        collection = self.collections[character_id]
        
        try:
            for i, fact in enumerate(facts):
                fact_id = f"{character_id}_{i}_{hash(fact['text']) % 10000}"
                
                embedding = self.encoder.encode(fact['text']).tolist()
                
                collection.add(
                    documents=[fact['text']],
                    embeddings=[embedding],
                    metadatas=[{
                        'character': character_id,
                        'category': fact.get('category', 'general'),
                        'source': fact.get('source', 'historical_records'),
                        'relevance': fact.get('relevance', 'high'),
                        'added_date': str(datetime.now())
                    }],
                    ids=[fact_id]
                )
            
            logger.info(f"✅ Added {len(facts)} facts for {character_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add knowledge for {character_id}: {e}")
            return False
    
    async def retrieve_relevant_facts(
        self, 
        character_id: str, 
        query: str, 
        max_results: int = 3
    ) -> List[Dict[str, str]]:
        
        if character_id not in self.collections:
            logger.warning(f"⚠️ No knowledge base for character: {character_id}")
            return []
        
        try:
            collection = self.collections[character_id]
            
            query_embedding = self.encoder.encode(query).tolist()
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            relevant_facts = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0], 
                    results['distances'][0]
                )):
                    relevance_score = 1 - distance
                    if relevance_score > 0.3:
                        relevant_facts.append({
                            'text': doc,
                            'category': metadata.get('category', 'general'),
                            'source': metadata.get('source', 'unknown'),
                            'relevance_score': relevance_score,
                            'rank': i + 1
                        })
            
            logger.info(f"🔍 Found {len(relevant_facts)} relevant facts for '{query[:50]}...'")
            return relevant_facts
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve facts for {character_id}: {e}")
            return []
    
    def get_collection_stats(self, character_id: str) -> Dict[str, int]:
        if character_id not in self.collections:
            return {"error": "Character not found"}
        
        try:
            collection = self.collections[character_id]
            count = collection.count()
            
            return {
                "character": character_id,
                "total_facts": count,
                "status": "ready" if count > 0 else "empty"
            }
        except Exception as e:
            logger.error(f"❌ Failed to get stats for {character_id}: {e}")
            return {"error": str(e)}

_rag_instance: Optional[HistoricalKnowledgeBase] = None

def get_rag_service() -> HistoricalKnowledgeBase:
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = HistoricalKnowledgeBase()
    return _rag_instance
