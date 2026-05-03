import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading and validation of scheme data from JSON files."""
    
    def __init__(self, data_path: str = "../data/schemes.json"):
        """
        Initialize data loader.
        
        Args:
            data_path: Path to the JSON data file.
        """
        self.data_path = Path(data_path)
        self.schemes_data: List[Dict[str, Any]] = []
    
    def load_schemes(self) -> List[Dict[str, Any]]:
        """
        Load schemes from JSON file.
        
        Returns:
            List of scheme dictionaries.
            
        Raises:
            FileNotFoundError: If data file doesn't exist.
            json.JSONDecodeError: If JSON is invalid.
        """
        try:
            if not self.data_path.exists():
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            with open(self.data_path, 'r', encoding='utf-8') as file:
                self.schemes_data = json.load(file)
            
            logger.info(f"Loaded {len(self.schemes_data)} schemes from {self.data_path}")
            
            # Validate data structure
            self._validate_schemes()
            
            return self.schemes_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading schemes: {e}")
            raise
    
    def _validate_schemes(self) -> None:
        """
        Validate the structure of loaded schemes data.
        
        Raises:
            ValueError: If required fields are missing.
        """
        required_fields = [
            'id', 'name', 'description', 'eligibility', 
            'benefits', 'documents_required', 'application_process',
            'state', 'category', 'income_limit'
        ]
        
        for i, scheme in enumerate(self.schemes_data):
            # Check if all required fields are present
            missing_fields = [field for field in required_fields if field not in scheme]
            if missing_fields:
                raise ValueError(f"Scheme {i} missing required fields: {missing_fields}")
            
            # Validate field types
            if not isinstance(scheme['id'], str):
                raise ValueError(f"Scheme {i}: 'id' must be string")
            
            if not isinstance(scheme['name'], str):
                raise ValueError(f"Scheme {i}: 'name' must be string")
            
            if not isinstance(scheme['description'], str):
                raise ValueError(f"Scheme {i}: 'description' must be string")
            
            if not isinstance(scheme['eligibility'], list):
                raise ValueError(f"Scheme {i}: 'eligibility' must be list")
            
            if not isinstance(scheme['benefits'], str):
                raise ValueError(f"Scheme {i}: 'benefits' must be string")
            
            if not isinstance(scheme['documents_required'], list):
                raise ValueError(f"Scheme {i}: 'documents_required' must be list")
            
            if not isinstance(scheme['application_process'], str):
                raise ValueError(f"Scheme {i}: 'application_process' must be string")
        
        logger.info("All schemes data validation passed")
    
    def get_scheme_by_id(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific scheme by its ID.
        
        Args:
            scheme_id: The ID of the scheme to retrieve.
            
        Returns:
            Scheme dictionary if found, None otherwise.
        """
        if not self.schemes_data:
            self.load_schemes()
        
        for scheme in self.schemes_data:
            if scheme['id'] == scheme_id:
                return scheme
        
        return None
    
    def get_schemes_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get schemes filtered by category.
        
        Args:
            category: Category to filter by.
            
        Returns:
            List of schemes in the specified category.
        """
        if not self.schemes_data:
            self.load_schemes()
        
        return [scheme for scheme in self.schemes_data if scheme['category'] == category]
    
    def get_schemes_by_state(self, state: str) -> List[Dict[str, Any]]:
        """
        Get schemes filtered by state.
        
        Args:
            state: State to filter by.
            
        Returns:
            List of schemes available in the specified state.
        """
        if not self.schemes_data:
            self.load_schemes()
        
        return [scheme for scheme in self.schemes_data 
                if scheme['state'] == state or scheme['state'] == "All India"]
    
    def get_all_categories(self) -> List[str]:
        """
        Get all unique categories from the schemes data.
        
        Returns:
            List of unique categories.
        """
        if not self.schemes_data:
            self.load_schemes()
        
        categories = set()
        for scheme in self.schemes_data:
            categories.add(scheme['category'])
        
        return sorted(list(categories))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the loaded schemes data.
        
        Returns:
            Dictionary containing statistics.
        """
        if not self.schemes_data:
            self.load_schemes()
        
        stats = {
            'total_schemes': len(self.schemes_data),
            'categories': self.get_all_categories(),
            'states': set(),
            'schemes_with_income_limit': 0,
            'schemes_without_income_limit': 0
        }
        
        for scheme in self.schemes_data:
            stats['states'].add(scheme['state'])
            if scheme['income_limit'] is not None:
                stats['schemes_with_income_limit'] += 1
            else:
                stats['schemes_without_income_limit'] += 1
        
        stats['states'] = sorted(list(stats['states']))
        
        return stats
