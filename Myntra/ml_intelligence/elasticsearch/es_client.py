"""
Elasticsearch Client Handler Module for ml_intelligence
Manages cluster connections and index initialization.
"""

import os
from typing import Optional
from elasticsearch import Elasticsearch
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.elasticsearch")


class ESClientHandler:
    """Manages Elasticsearch client connection and index mapping initialization."""

    def __init__(self, hosts: Optional[str] = None):
        self.hosts = hosts or os.getenv("ELASTICSEARCH_HOSTS", "http://localhost:9200")
        self.client: Optional[Elasticsearch] = None

    def connect(self) -> Optional[Elasticsearch]:
        """Establishes connection to Elasticsearch cluster."""
        try:
            self.client = Elasticsearch(self.hosts, request_timeout=5)
            if self.client.ping():
                logger.info(f"Connected to Elasticsearch cluster at: {self.hosts}")
                return self.client
            else:
                logger.warning(f"Elasticsearch ping failed at: {self.hosts}. Operating in fallback mode.")
                return None
        except Exception as e:
            logger.warning(f"Could not connect to Elasticsearch cluster ({e}). Operating in fallback search mode.")
            self.client = None
            return None
