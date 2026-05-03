import logging
import numpy as np
import hashlib
from typing import List, Dict, Any, Optional
try:
    from sentence_transformers import SentenceTransformer
    import torch
except ImportError as e:
    print(f"Warning: Could not import sentence_transformers: {e}")
    print("Using mock embedding service for testing...")
    
    class MockSentenceTransformer:
        def __init__(self, model_name):
            self.model_name = model_name
            self.embedding_dim = 384
        
        def encode(self, text, convert_to_numpy=True):
            import numpy as np
            # Mock embedding generation
            if isinstance(text, str):
                text_list = [text]
            else:
                text_list = text
            
            embeddings = []
            for t in text_list:
                # Generate simple hash-based embedding
                import hashlib
                hash_obj = hashlib.md5(t.encode())
                hash_hex = hash_obj.hexdigest()
                
                # Convert to numeric vector
                embedding = np.array([ord(c) for c in hash_hex[:32]], dtype=np.float32)
                if len(embedding) < 384:
                    embedding = np.pad(embedding, (0, 384 - len(embedding)), 'constant')
                embeddings.append(embedding)
            
            if convert_to_numpy:
                return np.array(embeddings)
            return embeddings
        
        def get_sentence_embedding_dimension(self):
            return 384
        
        @property
        def device(self):
            return "cpu"
    
    SentenceTransformer = MockSentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Handles text embedding generation using sentence-transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding service.
        
        Args:
            model_name: Name of the sentence-transformers model to use.
        """
        self.model_name = model_name
        self.model = None
        self.embedding_dim = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the sentence-transformers model."""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded successfully. Embedding dimension: {self.embedding_dim}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed.
            
        Returns:
            Embedding vector as numpy array.
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return np.zeros(self.embedding_dim, dtype=np.float32)
            
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            
            # Ensure float32 type for FAISS compatibility
            embedding = embedding.astype(np.float32)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding for text: {e}")
            return np.zeros(self.embedding_dim, dtype=np.float32)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed.
            
        Returns:
            Matrix of embeddings as numpy array.
        """
        try:
            if not texts:
                logger.warning("Empty text list provided for embedding")
                return np.zeros((0, self.embedding_dim), dtype=np.float32)
            
            # Filter out empty texts
            valid_texts = [text for text in texts if text and text.strip()]
            
            if not valid_texts:
                logger.warning("No valid texts found for embedding")
                return np.zeros((len(texts), self.embedding_dim), dtype=np.float32)
            
            # Generate embeddings in batch
            embeddings = self.model.encode(valid_texts, convert_to_numpy=True)
            
            # Ensure float32 type for FAISS compatibility
            embeddings = embeddings.astype(np.float32)
            
            # Handle cases where some texts were empty
            if len(valid_texts) < len(texts):
                full_embeddings = np.zeros((len(texts), self.embedding_dim), dtype=np.float32)
                valid_idx = 0
                for i, text in enumerate(texts):
                    if text and text.strip():
                        full_embeddings[i] = embeddings[valid_idx]
                        valid_idx += 1
                    else:
                        full_embeddings[i] = np.zeros(self.embedding_dim, dtype=np.float32)
                embeddings = full_embeddings
            
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings for texts: {e}")
            return np.zeros((len(texts), self.embedding_dim), dtype=np.float32)
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> tuple[List[np.ndarray], List[str]]:
        """
        Generate embeddings for text chunks.
        
        Args:
            chunks: List of chunk dictionaries.
            
        Returns:
            Tuple of (embeddings list, chunk_ids list).
        """
        try:
            if not chunks:
                logger.warning("No chunks provided for embedding")
                return [], []
            
            # Extract texts from chunks
            texts = [chunk['text'] for chunk in chunks]
            chunk_ids = [chunk['chunk_id'] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embed_texts(texts)
            
            # Convert to list of arrays
            embedding_list = [emb for emb in embeddings]
            
            logger.info(f"Generated embeddings for {len(chunks)} chunks")
            return embedding_list, chunk_ids
            
        except Exception as e:
            logger.error(f"Error embedding chunks: {e}")
            return [], []
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Embedding dimension.
        """
        return self.embedding_dim
    
    def compute_similarity(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between query and document embeddings.
        
        Args:
            query_embedding: Query embedding vector.
            doc_embeddings: Document embedding matrix.
            
        Returns:
            Similarity scores as numpy array.
        """
        try:
            # Normalize embeddings
            query_norm = query_embedding / np.linalg.norm(query_embedding)
            doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
            
            # Compute cosine similarity
            similarities = np.dot(doc_norms, query_norm)
            
            return similarities
            
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return np.zeros(len(doc_embeddings))
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding model.
        
        Returns:
            Dictionary containing model information.
        """
        return {
            'model_name': self.model_name,
            'embedding_dimension': self.embedding_dim,
            'model_loaded': self.model is not None,
            'device': str(self.model.device) if self.model else None
        }
