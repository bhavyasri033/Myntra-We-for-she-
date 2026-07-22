"""
Aspect Extractor Module for ml_intelligence
Extracts structured business aspects and text snippets from unstructured why_found text.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List
from ml_intelligence.api.schemas import (
    EvidenceAspectFlags, 
    EvidenceSnippet, 
    EvidenceExtractionInput, 
    EvidenceExtractionOutput
)
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.evidence")


class AspectExtractor:
    """Extracts structured business aspects and evidence snippets from why_found text."""

    def __init__(self, config_path: str = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            base_dir = Path(__file__).resolve().parent.parent
            self.config_path = base_dir / "configs" / "description_rules.json"

        self.rules: Dict[str, Any] = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """Loads aspect rules JSON configuration."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Description rules config missing at: {self.config_path}")
        with open(self.config_path, encoding="utf-8") as f:
            return json.load(f).get("aspect_rules", {})

    def extract(self, input_dto: EvidenceExtractionInput) -> EvidenceExtractionOutput:
        """Parses why_found text into EvidenceExtractionOutput DTO."""
        text = input_dto.why_found.lower()
        snippets: List[EvidenceSnippet] = []

        is_legacy = self._check_aspect(text, "is_legacy", "Legacy", snippets)
        is_authentic = self._check_aspect(text, "is_authentic", "Authentic", snippets)
        is_handloom = self._check_aspect(text, "is_handloom", "Handloom", snippets)
        is_bridal = self._check_aspect(text, "is_bridal", "Bridal", snippets)
        is_government = self._check_aspect(text, "is_government", "Government", snippets)
        is_family_shopping = self._check_aspect(text, "is_family_shopping", "Family Shopping", snippets)

        price_segment = self._determine_price_segment(text)

        aspects = EvidenceAspectFlags(
            is_legacy=is_legacy,
            is_authentic=is_authentic,
            is_handloom=is_handloom,
            is_bridal=is_bridal,
            is_government=is_government,
            is_family_shopping=is_family_shopping,
            price_segment=price_segment
        )

        return EvidenceExtractionOutput(
            store_id=input_dto.store_id,
            aspects=aspects,
            evidence_snippets=snippets
        )

    def _check_aspect(self, text: str, aspect_key: str, display_name: str, snippets: List[EvidenceSnippet]) -> bool:
        """Checks keywords for a specific aspect and appends matching snippet."""
        keywords = self.rules.get(aspect_key, [])
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                snippets.append(EvidenceSnippet(aspect=display_name, snippet=kw))
                return True
        return False

    def _determine_price_segment(self, text: str) -> str:
        """Infers price segment based on rule definitions."""
        price_rules = self.rules.get("price_segment_rules", {})
        for segment, keywords in price_rules.items():
            if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords):
                return segment
        return "Mid-Premium"
