"""
Dossier package initialization.
"""
from ml_intelligence.dossier.prompt_templates import DOSSIER_MARKDOWN_TEMPLATE
from ml_intelligence.dossier.dossier_generator import DossierGenerator

__all__ = ["DOSSIER_MARKDOWN_TEMPLATE", "DossierGenerator"]
