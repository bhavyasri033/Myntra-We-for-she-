"""
Taxonomy Manager Module for ml_intelligence
Loads and provides access to fashion taxonomy categories and specializations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List


class TaxonomyManager:
    """Loads and validates fashion taxonomy configuration file."""

    def __init__(self, config_path: str = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            base_dir = Path(__file__).resolve().parent.parent
            self.config_path = base_dir / "configs" / "fashion_taxonomy.json"
        
        self.taxonomy: Dict[str, Any] = self._load_taxonomy()

    def _load_taxonomy(self) -> Dict[str, Any]:
        """Loads taxonomy JSON file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Taxonomy config missing at: {self.config_path}")
        
        with open(self.config_path, encoding="utf-8") as f:
            return json.load(f)

    def get_categories(self) -> List[str]:
        return self.taxonomy.get("categories", [])

    def get_specializations(self) -> List[str]:
        return self.taxonomy.get("specializations", [])
