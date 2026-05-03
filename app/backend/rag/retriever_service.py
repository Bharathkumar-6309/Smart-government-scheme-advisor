import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from .embedding_service import EmbeddingService
from .vector_store_service import VectorStoreService
from .llm_service import LLMService
from ingestion.data_loader import DataLoader
from ingestion.text_processor import TextProcessor
from ingestion.chunker import TextChunker

logger = logging.getLogger(__name__)


class RetrieverService:
    """Handles RAG retrieval operations."""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", index_type: str = "flat"):
        """
        Initialize retriever service.
        
        Args:
            embedding_model: Name of sentence-transformers model.
            index_type: Type of FAISS index to use.
        """
        self.embedding_service = EmbeddingService(embedding_model)
        self.vector_store = VectorStoreService(
            embedding_dimension=self.embedding_service.get_embedding_dimension(),
            index_type=index_type
        )
        self.data_loader = DataLoader()
        self.text_processor = TextProcessor()
        self.chunker = TextChunker()
        self.llm_service = LLMService()
        self.is_initialized = False
    
    def initialize(self, force_rebuild: bool = False) -> None:
        """
        Initialize the RAG system with scheme data.
        
        Args:
            force_rebuild: Whether to force rebuilding the index.
        """
        try:
            logger.info("Initializing RAG system...")
            
            # Try to load existing index if not forcing rebuild
            if not force_rebuild:
                try:
                    self.vector_store.load_index("../data/vector_store")
                    logger.info("Loaded existing vector store")
                    self.is_initialized = True
                    return
                except FileNotFoundError:
                    logger.info("No existing vector store found, building new one...")
            
            # Load and process scheme data
            logger.info("Loading scheme data...")
            chunks = self.chunker.create_embedding_ready_chunks()
            
            if not chunks:
                raise ValueError("No chunks found for processing")
            
            # Generate embeddings
            logger.info("Generating embeddings...")
            embeddings, chunk_ids = self.embedding_service.embed_chunks(chunks)
            
            # Extract metadata
            chunk_metadata = []
            for chunk in chunks:
                metadata = {
                    'scheme_id': chunk['scheme_id'],
                    'scheme_name': chunk['metadata']['scheme_name'],
                    'category': chunk['metadata']['category'],
                    'state': chunk['metadata']['state'],
                    'income_limit': chunk['metadata']['income_limit'],
                    'chunk_type': chunk['metadata']['chunk_type'],
                    'field_name': chunk['metadata'].get('field_name'),
                    'text': chunk['text']
                }
                chunk_metadata.append(metadata)
            
            # Add to vector store
            logger.info("Adding embeddings to vector store...")
            self.vector_store.add_embeddings(embeddings, chunk_ids, chunk_metadata)
            
            # Save index
            self.vector_store.save_index("../data/vector_store")
            
            self.is_initialized = True
            logger.info("RAG system initialization completed")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG system: {e}")
            raise
    
    def search(self, query: str, top_k: int = 3, user_profile: Optional[Dict[str, Any]] = None,
                filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for relevant schemes using RAG with LLM response generation and filtering.
        
        Args:
            query: Search query.
            top_k: Number of top results to return.
            user_profile: Optional user profile information.
            filters: Optional filtering criteria (state, category, income_limit).
            
        Returns:
            Structured response with LLM-generated recommendations.
        """
        try:
            if not self.is_initialized:
                logger.info("RAG system not initialized, initializing now...")
                self.initialize()
            
            if not query or not query.strip():
                logger.warning("Empty query provided")
                return {"error": "Empty query provided"}
            
            logger.info(f"Searching for query: '{query}' with filters: {filters}")
            
            # Apply filters to search
            filtered_schemes = self._apply_filters(filters)
            
            # Generate query embedding
            query_embedding = self.embedding_service.embed_text(query)
            
            # Search vector store
            search_results = self.vector_store.search(query_embedding, top_k * 2)  # Get more results for deduplication
            
            # Group results by scheme and deduplicate
            scheme_results = self._group_results_by_scheme(search_results)
            
            # Apply additional filtering to grouped results
            if filtered_schemes:
                scheme_results = self._filter_grouped_results(scheme_results, filtered_schemes)
            
            # Get top_k unique schemes
            context_schemes = list(scheme_results.values())[:top_k]
            
            # Generate LLM response
            llm_response = self.llm_service.generate_structured_response(
                query=query,
                context_schemes=context_schemes,
                user_profile=user_profile
            )
            
            logger.info(f"Generated LLM response for {len(context_schemes)} retrieved schemes")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error during RAG+LLM search: {e}")
            return {"error": str(e)}
    
    def _apply_filters(self, filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply filters to all schemes before search.
        
        Args:
            filters: Dictionary of filter criteria.
            
        Returns:
            List of filtered scheme dictionaries.
        """
        if not filters:
            return []
        
        try:
            # Load all schemes
            all_schemes = self.data_loader.load_schemes()
            filtered_schemes = []
            
            for scheme in all_schemes:
                include_scheme = True
                
                # State filter
                if filters.get('state'):
                    if scheme['state'] != filters['state'] and scheme['state'] != 'All India':
                        include_scheme = False
                
                # Category filter
                if filters.get('category'):
                    if scheme['category'] != filters['category']:
                        include_scheme = False
                
                # Income limit filter
                if filters.get('income_limit') is not None:
                    if scheme['income_limit'] is None:
                        include_scheme = False
                    elif scheme['income_limit'] > filters['income_limit']:
                        include_scheme = False
                
                if include_scheme:
                    filtered_schemes.append(scheme)
            
            logger.info(f"Applied filters: {len(filtered_schemes)} schemes out of {len(all_schemes)}")
            return filtered_schemes
            
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            return []
    
    def _filter_grouped_results(self, scheme_results: Dict[str, Dict[str, Any]], 
                          filtered_schemes: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Apply additional filtering to grouped results.
        
        Args:
            scheme_results: Original grouped results.
            filtered_schemes: List of schemes to filter by.
            
        Returns:
            Filtered grouped results.
        """
        try:
            for scheme_id, result in scheme_results.items():
                if scheme_id in [scheme['id'] for scheme in filtered_schemes]:
                    # Keep the result (scheme passes filters)
                    continue
                else:
                    # Remove the result (scheme doesn't pass filters)
                    del scheme_results[scheme_id]
            
            return scheme_results
            
        except Exception as e:
            logger.error(f"Error filtering grouped results: {e}")
            return scheme_results
    
    def _group_results_by_scheme(self, search_results: List[Tuple[str, float, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
        """
        Group search results by scheme and combine scores.
        
        Args:
            search_results: Raw search results from vector store.
            
        Returns:
            Dictionary grouped by scheme_id.
        """
        scheme_results = {}
        
        for chunk_id, similarity_score, metadata in search_results:
            scheme_id = metadata['scheme_id']
            
            if scheme_id not in scheme_results:
                # Initialize scheme result
                scheme_results[scheme_id] = {
                    'scheme_id': scheme_id,
                    'scheme_name': metadata['scheme_name'],
                    'category': metadata['category'],
                    'state': metadata['state'],
                    'income_limit': metadata['income_limit'],
                    'similarity_score': 0.0,
                    'matching_chunks': [],
                    'chunk_types': set()
                }
            
            # Update scheme result
            scheme_result = scheme_results[scheme_id]
            scheme_result['similarity_score'] = max(scheme_result['similarity_score'], similarity_score)
            scheme_result['chunk_types'].add(metadata['chunk_type'])
            
            # Add matching chunk
            chunk_info = {
                'chunk_id': chunk_id,
                'similarity_score': similarity_score,
                'chunk_type': metadata['chunk_type'],
                'field_name': metadata.get('field_name'),
                'text': metadata['text']
            }
            scheme_result['matching_chunks'].append(chunk_info)
        
        # Convert sets to lists for JSON serialization
        for result in scheme_results.values():
            result['chunk_types'] = list(result['chunk_types'])
            # Sort chunks by similarity score
            result['matching_chunks'].sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return scheme_results
    
    def get_scheme_details(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific scheme.
        
        Args:
            scheme_id: ID of the scheme.
            
        Returns:
            Scheme details or None if not found.
        """
        try:
            return self.data_loader.get_scheme_by_id(scheme_id)
        except Exception as e:
            logger.error(f"Error getting scheme details for {scheme_id}: {e}")
            return None
    
    def get_similar_schemes(self, scheme_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Find schemes similar to a given scheme.
        
        Args:
            scheme_id: ID of the reference scheme.
            top_k: Number of similar schemes to return.
            
        Returns:
            List of similar schemes.
        """
        try:
            # Get scheme details
            scheme = self.get_scheme_details(scheme_id)
            if not scheme:
                logger.warning(f"Scheme {scheme_id} not found")
                return []
            
            # Create search query from scheme name and description
            query = f"{scheme['name']} {scheme['description']}"
            
            # Search
            results = self.search(query, top_k + 1)  # +1 to exclude the original scheme
            
            # Filter out the original scheme
            similar_schemes = [r for r in results if r['scheme_id'] != scheme_id]
            
            return similar_schemes[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar schemes for {scheme_id}: {e}")
            return []
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system.
        
        Returns:
            Dictionary containing system statistics.
        """
        try:
            vector_stats = self.vector_store.get_stats()
            embedding_info = self.embedding_service.get_model_info()
            
            return {
                'is_initialized': self.is_initialized,
                'vector_store': vector_stats,
                'embedding_model': embedding_info
            }
            
        except Exception as e:
            logger.error(f"Error getting search statistics: {e}")
            return {'error': str(e)}
    
    def rebuild_index(self) -> None:
        """
        Rebuild the entire vector index.
        """
        logger.info("Rebuilding vector index...")
        self.initialize(force_rebuild=True)
        logger.info("Vector index rebuilt successfully")
