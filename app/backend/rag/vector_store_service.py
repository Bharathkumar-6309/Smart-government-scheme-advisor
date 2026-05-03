import logging
import numpy as np
import pickle
from typing import List, Dict, Any, Optional, Tuple
import faiss
from pathlib import Path

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Handles FAISS vector database operations."""
    
    def __init__(self, embedding_dimension: int = 384, index_type: str = "flat"):
        """
        Initialize vector store service.
        
        Args:
            embedding_dimension: Dimension of embedding vectors.
            index_type: Type of FAISS index to use ("flat", "ivf", "hnsw").
        """
        self.embedding_dimension = embedding_dimension
        self.index_type = index_type
        self.index = None
        self.chunk_metadata = {}  # chunk_id -> metadata mapping
        self.id_to_index = {}     # chunk_id -> faiss index mapping
        self.index_to_id = {}     # faiss index -> chunk_id mapping
        self._create_index()
    
    def _create_index(self) -> None:
        """Create FAISS index based on specified type."""
        try:
            if self.index_type == "flat":
                # Simple flat index (exact search)
                self.index = faiss.IndexFlatL2(self.embedding_dimension)
                logger.info("Created Flat L2 index")
            
            elif self.index_type == "ivf":
                # IVF (Inverted File) index for faster search
                nlist = 100  # Number of clusters
                quantizer = faiss.IndexFlatL2(self.embedding_dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.embedding_dimension, nlist)
                logger.info(f"Created IVF index with {nlist} clusters")
            
            elif self.index_type == "hnsw":
                # HNSW (Hierarchical Navigable Small World) index
                M = 16  # Number of connections
                ef_construction = 200  # Construction parameter
                self.index = faiss.IndexHNSWFlat(self.embedding_dimension, M)
                self.index.hnsw.efConstruction = ef_construction
                logger.info(f"Created HNSW index with M={M}, ef_construction={ef_construction}")
            
            else:
                raise ValueError(f"Unsupported index type: {self.index_type}")
            
            logger.info(f"FAISS index created successfully. Type: {self.index_type}")
            
        except Exception as e:
            logger.error(f"Failed to create FAISS index: {e}")
            raise
    
    def add_embeddings(self, embeddings: List[np.ndarray], chunk_ids: List[str], 
                      chunk_metadata: List[Dict[str, Any]]) -> None:
        """
        Add embeddings to the vector store.
        
        Args:
            embeddings: List of embedding vectors.
            chunk_ids: List of chunk IDs.
            chunk_metadata: List of chunk metadata.
        """
        try:
            if not embeddings or not chunk_ids:
                logger.warning("No embeddings or chunk IDs provided")
                return
            
            if len(embeddings) != len(chunk_ids) or len(chunk_ids) != len(chunk_metadata):
                raise ValueError("Lengths of embeddings, chunk_ids, and chunk_metadata must match")
            
            # Convert embeddings to numpy array
            embedding_matrix = np.array(embeddings, dtype=np.float32)
            
            # Get current index size
            start_idx = self.index.ntotal
            
            # Add embeddings to index
            self.index.add(embedding_matrix)
            
            # Update mappings
            for i, (chunk_id, metadata) in enumerate(zip(chunk_ids, chunk_metadata)):
                faiss_idx = start_idx + i
                self.id_to_index[chunk_id] = faiss_idx
                self.index_to_id[faiss_idx] = chunk_id
                self.chunk_metadata[chunk_id] = metadata
            
            logger.info(f"Added {len(embeddings)} embeddings to vector store")
            
            # Train index if it's IVF type and this is the first addition
            if self.index_type == "ivf" and self.index.ntotal == len(embeddings):
                logger.info("Training IVF index...")
                self.index.train(embedding_matrix)
                self.index.reset()
                self.index.add(embedding_matrix)
                logger.info("IVF index training completed")
            
        except Exception as e:
            logger.error(f"Error adding embeddings to vector store: {e}")
            raise
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Search for similar embeddings.
        
        Args:
            query_embedding: Query embedding vector.
            top_k: Number of top results to return.
            
        Returns:
            List of tuples (chunk_id, distance, metadata).
        """
        try:
            if self.index.ntotal == 0:
                logger.warning("Vector store is empty")
                return []
            
            # Ensure query embedding is in correct format
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            query_embedding = query_embedding.astype(np.float32)
            
            # Adjust top_k if necessary
            top_k = min(top_k, self.index.ntotal)
            
            # Search
            distances, indices = self.index.search(query_embedding, top_k)
            
            # Convert results to list of tuples
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx != -1:  # Valid result
                    chunk_id = self.index_to_id.get(idx)
                    if chunk_id:
                        metadata = self.chunk_metadata.get(chunk_id, {})
                        # Convert L2 distance to similarity score (lower distance = higher similarity)
                        similarity = 1 / (1 + distance)
                        results.append((chunk_id, similarity, metadata))
            
            logger.info(f"Search completed. Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def get_chunk_metadata(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific chunk.
        
        Args:
            chunk_id: ID of the chunk.
            
        Returns:
            Chunk metadata or None if not found.
        """
        return self.chunk_metadata.get(chunk_id)
    
    def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a chunk from the vector store.
        
        Args:
            chunk_id: ID of the chunk to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if chunk_id not in self.id_to_index:
                logger.warning(f"Chunk {chunk_id} not found in vector store")
                return False
            
            # FAISS doesn't support deletion directly, so we need to rebuild
            # This is a simplified implementation - in production, you'd want a more efficient approach
            logger.warning("FAISS deletion requires rebuilding index - not implemented in this demo")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting chunk {chunk_id}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary containing vector store statistics.
        """
        return {
            'total_vectors': self.index.ntotal,
            'embedding_dimension': self.embedding_dimension,
            'index_type': self.index_type,
            'total_chunks': len(self.chunk_metadata),
            'memory_usage': self.get_memory_usage()
        }
    
    def get_memory_usage(self) -> str:
        """
        Get memory usage of the vector store.
        
        Returns:
            Memory usage as human-readable string.
        """
        try:
            # Estimate memory usage (rough approximation)
            vectors_memory = self.index.ntotal * self.embedding_dimension * 4  # 4 bytes per float32
            metadata_memory = len(pickle.dumps(self.chunk_metadata))
            total_memory = vectors_memory + metadata_memory
            
            # Convert to human-readable format
            for unit in ['B', 'KB', 'MB', 'GB']:
                if total_memory < 1024:
                    return f"{total_memory:.2f} {unit}"
                total_memory /= 1024
            
            return f"{total_memory:.2f} TB"
            
        except Exception as e:
            logger.error(f"Error calculating memory usage: {e}")
            return "Unknown"
    
    def save_index(self, file_path: str) -> None:
        """
        Save the vector store to disk.
        
        Args:
            file_path: Path to save the index.
        """
        try:
            save_path = Path(file_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            index_path = save_path.with_suffix('.faiss')
            faiss.write_index(self.index, str(index_path))
            
            # Save metadata
            metadata_path = save_path.with_suffix('.pkl')
            metadata = {
                'chunk_metadata': self.chunk_metadata,
                'id_to_index': self.id_to_index,
                'index_to_id': self.index_to_id,
                'embedding_dimension': self.embedding_dimension,
                'index_type': self.index_type
            }
            
            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)
            
            logger.info(f"Vector store saved to {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            raise
    
    def load_index(self, file_path: str) -> None:
        """
        Load the vector store from disk.
        
        Args:
            file_path: Path to load the index from.
        """
        try:
            load_path = Path(file_path)
            
            # Load FAISS index
            index_path = load_path.with_suffix('.faiss')
            if not index_path.exists():
                raise FileNotFoundError(f"Index file not found: {index_path}")
            
            self.index = faiss.read_index(str(index_path))
            
            # Load metadata
            metadata_path = load_path.with_suffix('.pkl')
            if not metadata_path.exists():
                raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
            
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            
            self.chunk_metadata = metadata['chunk_metadata']
            self.id_to_index = metadata['id_to_index']
            self.index_to_id = metadata['index_to_id']
            self.embedding_dimension = metadata['embedding_dimension']
            self.index_type = metadata['index_type']
            
            logger.info(f"Vector store loaded from {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise
