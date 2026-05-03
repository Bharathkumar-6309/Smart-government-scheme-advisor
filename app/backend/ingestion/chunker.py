import logging
from typing import List, Dict, Any, Tuple
from .data_loader import DataLoader
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)


class TextChunker:
    """Handles text chunking for embedding preparation."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters.
            chunk_overlap: Number of characters to overlap between chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.data_loader = DataLoader()
        self.text_processor = TextProcessor()
    
    def create_chunks(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk.
            
        Returns:
            List of text chunks.
        """
        if not text or len(text) <= self.chunk_size:
            return [text] if text else []
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position for this chunk
            end = start + self.chunk_size
            
            # If this is the last chunk, take everything remaining
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Try to break at a sentence boundary
            chunk_text = text[start:end]
            
            # Look for sentence endings in the last part of the chunk
            sentence_endings = ['.', '!', '?']
            best_break = -1
            
            # Search backwards for sentence ending
            for i in range(len(chunk_text) - 1, max(0, len(chunk_text) - 100), -1):
                if chunk_text[i] in sentence_endings:
                    best_break = i + 1
                    break
            
            # If no sentence ending found, try to break at word boundary
            if best_break == -1:
                for i in range(len(chunk_text) - 1, max(0, len(chunk_text) - 50), -1):
                    if chunk_text[i] == ' ':
                        best_break = i
                        break
            
            # Use the best break point or the full chunk
            if best_break > 0:
                actual_end = start + best_break
                chunks.append(text[start:actual_end].strip())
                start = actual_end
            else:
                chunks.append(chunk_text.strip())
                start = end
            
            # Apply overlap for next chunk
            if start < len(text):
                start = max(start - self.chunk_overlap, 0)
        
        # Filter out empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]
        
        return chunks
    
    def chunk_scheme(self, scheme: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create chunks for a single scheme with metadata.
        
        Args:
            scheme: Scheme dictionary.
            
        Returns:
            List of chunk dictionaries with metadata.
        """
        # Create searchable text
        searchable_text = self.text_processor.create_searchable_text(scheme)
        
        # Create text chunks
        text_chunks = self.create_chunks(searchable_text)
        
        # Create chunk objects with metadata
        scheme_chunks = []
        
        for i, chunk in enumerate(text_chunks):
            chunk_data = {
                'chunk_id': f"{scheme['id']}_chunk_{i+1}",
                'scheme_id': scheme['id'],
                'chunk_index': i,
                'total_chunks': len(text_chunks),
                'text': chunk,
                'metadata': {
                    'scheme_name': scheme['name'],
                    'category': scheme['category'],
                    'state': scheme['state'],
                    'income_limit': scheme['income_limit'],
                    'chunk_type': 'general'
                }
            }
            scheme_chunks.append(chunk_data)
        
        return scheme_chunks
    
    def create_field_specific_chunks(self, scheme: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create chunks for specific fields of a scheme.
        
        Args:
            scheme: Scheme dictionary.
            
        Returns:
            List of field-specific chunk dictionaries.
        """
        field_chunks = []
        
        # Define important fields to chunk separately
        important_fields = {
            'name': 'scheme_name',
            'description': 'description',
            'benefits': 'benefits',
            'application_process': 'application_process'
        }
        
        for field, chunk_type in important_fields.items():
            # Use cleaned field if available
            field_text = scheme.get(f'{field}_cleaned', scheme.get(field, ''))
            
            if field_text:
                chunks = self.create_chunks(field_text)
                
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        'chunk_id': f"{scheme['id']}_{field}_chunk_{i+1}",
                        'scheme_id': scheme['id'],
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'text': chunk,
                        'metadata': {
                            'scheme_name': scheme['name'],
                            'category': scheme['category'],
                            'state': scheme['state'],
                            'income_limit': scheme['income_limit'],
                            'chunk_type': chunk_type,
                            'field_name': field
                        }
                    }
                    field_chunks.append(chunk_data)
        
        # Handle list fields (eligibility and documents)
        list_fields = {
            'eligibility': 'eligibility_criteria',
            'documents_required': 'required_documents'
        }
        
        for field, chunk_type in list_fields.items():
            items = scheme.get(f'{field}_cleaned', scheme.get(field, []))
            
            if isinstance(items, list) and items:
                # Join items into a single text for chunking
                combined_text = ' | '.join(items)
                chunks = self.create_chunks(combined_text)
                
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        'chunk_id': f"{scheme['id']}_{field}_chunk_{i+1}",
                        'scheme_id': scheme['id'],
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'text': chunk,
                        'metadata': {
                            'scheme_name': scheme['name'],
                            'category': scheme['category'],
                            'state': scheme['state'],
                            'income_limit': scheme['income_limit'],
                            'chunk_type': chunk_type,
                            'field_name': field
                        }
                    }
                    field_chunks.append(chunk_data)
        
        return field_chunks
    
    def chunk_all_schemes(self, include_field_chunks: bool = True) -> List[Dict[str, Any]]:
        """
        Create chunks for all schemes.
        
        Args:
            include_field_chunks: Whether to include field-specific chunks.
            
        Returns:
            List of all chunk dictionaries.
        """
        logger.info("Starting chunking process for all schemes")
        
        try:
            # Load and process schemes
            schemes = self.text_processor.process_all_schemes()
            
            all_chunks = []
            
            for i, scheme in enumerate(schemes):
                try:
                    # Create general chunks
                    scheme_chunks = self.chunk_scheme(scheme)
                    all_chunks.extend(scheme_chunks)
                    
                    # Create field-specific chunks if requested
                    if include_field_chunks:
                        field_chunks = self.create_field_specific_chunks(scheme)
                        all_chunks.extend(field_chunks)
                    
                    logger.debug(f"Chunked scheme {i+1}/{len(schemes)}: {scheme['name']}")
                    
                except Exception as e:
                    logger.error(f"Error chunking scheme {scheme.get('id', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Successfully created {len(all_chunks)} chunks from {len(schemes)} schemes")
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error in batch chunking: {e}")
            raise
    
    def create_embedding_ready_chunks(self) -> List[Dict[str, Any]]:
        """
        Create chunks ready for embedding generation.
        
        Returns:
            List of embedding-ready chunk dictionaries.
        """
        chunks = self.chunk_all_schemes(include_field_chunks=True)
        
        # Add embedding-specific fields
        embedding_chunks = []
        
        for chunk in chunks:
            embedding_chunk = chunk.copy()
            
            # Add text length for embedding considerations
            embedding_chunk['text_length'] = len(chunk['text'])
            
            # Add keywords for better searchability
            keywords = self.text_processor.extract_keywords(chunk['text'])
            embedding_chunk['keywords'] = keywords
            
            # Add embedding metadata
            embedding_chunk['embedding_metadata'] = {
                'created_at': '2024-01-01T00:00:00Z',  # Would use actual timestamp
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap,
                'text_type': chunk['metadata']['chunk_type'],
                'word_count': len(chunk['text'].split())
            }
            
            embedding_chunks.append(embedding_chunk)
        
        return embedding_chunks
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about the generated chunks.
        
        Args:
            chunks: List of chunk dictionaries.
            
        Returns:
            Dictionary containing chunk statistics.
        """
        if not chunks:
            return {}
        
        # Basic statistics
        total_chunks = len(chunks)
        total_chars = sum(len(chunk['text']) for chunk in chunks)
        total_words = sum(len(chunk['text'].split()) for chunk in chunks)
        
        # Chunk type distribution
        chunk_types = {}
        for chunk in chunks:
            chunk_type = chunk['metadata']['chunk_type']
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        
        # Scheme distribution
        scheme_distribution = {}
        for chunk in chunks:
            scheme_id = chunk['scheme_id']
            scheme_distribution[scheme_id] = scheme_distribution.get(scheme_id, 0) + 1
        
        # Text length distribution
        text_lengths = [len(chunk['text']) for chunk in chunks]
        avg_text_length = sum(text_lengths) / len(text_lengths)
        min_text_length = min(text_lengths)
        max_text_length = max(text_lengths)
        
        return {
            'total_chunks': total_chunks,
            'total_characters': total_chars,
            'total_words': total_words,
            'avg_chars_per_chunk': avg_text_length,
            'min_chars_per_chunk': min_text_length,
            'max_chars_per_chunk': max_text_length,
            'avg_words_per_chunk': total_words / total_chunks,
            'chunk_type_distribution': chunk_types,
            'scheme_distribution': scheme_distribution,
            'unique_schemes': len(scheme_distribution)
        }
    
    def save_chunks_to_file(self, chunks: List[Dict[str, Any]], output_path: str = "../data/chunks.json") -> None:
        """
        Save chunks to a JSON file.
        
        Args:
            chunks: List of chunk dictionaries.
            output_path: Path to save the chunks file.
        """
        import json
        
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(chunks, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(chunks)} chunks to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving chunks to file: {e}")
            raise
