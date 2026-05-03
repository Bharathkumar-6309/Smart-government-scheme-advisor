import re
import logging
from typing import List, Dict, Any, Optional
from .data_loader import DataLoader

logger = logging.getLogger(__name__)


class TextProcessor:
    """Handles text cleaning and preprocessing for scheme data."""
    
    def __init__(self):
        """Initialize text processor."""
        self.data_loader = DataLoader()
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text to clean.
            
        Returns:
            Cleaned text.
        """
        if not isinstance(text, str):
            return str(text) if text is not None else ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove bullet points and numbering (but keep the content)
        text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[•\-\*]\s*', '', text, flags=re.MULTILINE)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\:\;\!\?\(\)]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Convert to lowercase for consistency (optional - keep case for proper nouns)
        # text = text.lower()
        
        return text.strip()
    
    def process_scheme_text(self, scheme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and clean all text fields in a scheme.
        
        Args:
            scheme: Scheme dictionary with raw text fields.
            
        Returns:
            Scheme dictionary with cleaned text fields.
        """
        processed_scheme = scheme.copy()
        
        # Fields to clean
        text_fields = [
            'name', 'description', 'benefits', 'application_process'
        ]
        
        for field in text_fields:
            if field in processed_scheme:
                processed_scheme[f'{field}_cleaned'] = self.clean_text(processed_scheme[field])
        
        # Process list fields
        list_fields = ['eligibility', 'documents_required']
        
        for field in list_fields:
            if field in processed_scheme and isinstance(processed_scheme[field], list):
                processed_scheme[f'{field}_cleaned'] = [
                    self.clean_text(item) for item in processed_scheme[field]
                ]
        
        return processed_scheme
    
    def process_all_schemes(self) -> List[Dict[str, Any]]:
        """
        Process and clean all schemes data.
        
        Returns:
            List of processed scheme dictionaries.
        """
        logger.info("Starting text processing for all schemes")
        
        try:
            # Load raw schemes data
            schemes = self.data_loader.load_schemes()
            
            # Process each scheme
            processed_schemes = []
            for i, scheme in enumerate(schemes):
                try:
                    processed_scheme = self.process_scheme_text(scheme)
                    processed_schemes.append(processed_scheme)
                    logger.debug(f"Processed scheme {i+1}/{len(schemes)}: {scheme['name']}")
                except Exception as e:
                    logger.error(f"Error processing scheme {scheme.get('id', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Successfully processed {len(processed_schemes)} schemes")
            return processed_schemes
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            raise
    
    def create_searchable_text(self, scheme: Dict[str, Any]) -> str:
        """
        Create a comprehensive searchable text field for a scheme.
        
        Args:
            scheme: Scheme dictionary.
            
        Returns:
            Combined searchable text string.
        """
        # Use cleaned fields if available, otherwise use original fields
        name = scheme.get('name_cleaned', scheme.get('name', ''))
        description = scheme.get('description_cleaned', scheme.get('description', ''))
        benefits = scheme.get('benefits_cleaned', scheme.get('benefits', ''))
        application_process = scheme.get('application_process_cleaned', scheme.get('application_process', ''))
        
        # Handle list fields
        eligibility_items = scheme.get('eligibility_cleaned', scheme.get('eligibility', []))
        if isinstance(eligibility_items, list):
            eligibility = ' '.join(eligibility_items)
        else:
            eligibility = str(eligibility_items)
        
        documents_items = scheme.get('documents_required_cleaned', scheme.get('documents_required', []))
        if isinstance(documents_items, list):
            documents = ' '.join(documents_items)
        else:
            documents = str(documents_items)
        
        # Combine all text fields
        searchable_text = f"""
        Scheme Name: {name}
        Description: {description}
        Eligibility Criteria: {eligibility}
        Benefits: {benefits}
        Required Documents: {documents}
        Application Process: {application_process}
        Category: {scheme.get('category', '')}
        State: {scheme.get('state', '')}
        """.strip()
        
        return self.clean_text(searchable_text)
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text for better searchability.
        
        Args:
            text: Text to extract keywords from.
            
        Returns:
            List of keywords.
        """
        # Clean the text first
        clean_text = self.clean_text(text)
        
        # Common Indian government scheme keywords
        scheme_keywords = [
            'pradhan mantri', 'pm', 'yojana', 'scheme', 'government', 'central', 'state',
            'scholarship', 'education', 'housing', 'agriculture', 'healthcare', 'skill',
            'development', 'empowerment', 'financial', 'inclusion', 'benefit', 'subsidy',
            'loan', 'grant', 'assistance', 'support', 'bpl', 'ews', 'lig', 'mig',
            'aadhaar', 'ration', 'card', 'certificate', 'application', 'registration'
        ]
        
        # Split text into words
        words = clean_text.lower().split()
        
        # Filter keywords that appear in text
        keywords = []
        for keyword in scheme_keywords:
            if keyword in clean_text.lower():
                keywords.append(keyword)
        
        # Add important words from the text (words longer than 3 characters)
        important_words = [word for word in words if len(word) > 3 and word.isalpha()]
        keywords.extend(important_words[:10])  # Limit to top 10 important words
        
        # Remove duplicates and return
        return list(set(keywords))
    
    def get_text_statistics(self, schemes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about the processed text data.
        
        Args:
            schemes: List of processed scheme dictionaries.
            
        Returns:
            Dictionary containing text statistics.
        """
        total_chars = 0
        total_words = 0
        field_stats = {}
        
        for scheme in schemes:
            searchable_text = self.create_searchable_text(scheme)
            total_chars += len(searchable_text)
            total_words += len(searchable_text.split())
            
            # Track field-specific stats
            for field in ['name', 'description', 'benefits', 'application_process']:
                cleaned_field = f'{field}_cleaned'
                if cleaned_field in scheme:
                    if field not in field_stats:
                        field_stats[field] = {'char_count': 0, 'word_count': 0}
                    
                    field_stats[field]['char_count'] += len(scheme[cleaned_field])
                    field_stats[field]['word_count'] += len(scheme[cleaned_field].split())
        
        return {
            'total_schemes': len(schemes),
            'total_characters': total_chars,
            'total_words': total_words,
            'avg_chars_per_scheme': total_chars / len(schemes) if schemes else 0,
            'avg_words_per_scheme': total_words / len(schemes) if schemes else 0,
            'field_statistics': field_stats
        }
