"""
ES Bulk Indexer Module for ml_intelligence
Encodes 384-dim dense vectors using sentence-transformers (with fast fallback) and indexes store payloads into ES 8.x.
"""

import json
import os
import math
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from ml_intelligence.elasticsearch.es_client import ESClientHandler
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.elasticsearch.indexer")


class ESBulkIndexer:
    """Encodes store descriptions into 384-dim vectors and indexes documents into Elasticsearch."""

    def __init__(self, index_name: str = "myntra_bharat_stores_v1"):
        self.index_name = index_name
        self.es_handler = ESClientHandler()
        self.client = self.es_handler.connect()
        self._model = None
        self.in_memory_index: Dict[str, Dict[str, Any]] = {}

    @property
    def model(self):
        """Lazy loads SentenceTransformer model with fallback."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                # Load lightweight model
                self._model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Using fast vector encoder fallback.")
                self._model = "FALLBACK"
        return self._model

    def encode_text(self, texts: List[str]) -> List[List[float]]:
        """Encodes texts into 384-dim vectors using model or fast hashing fallback."""
        m = self.model
        if m != "FALLBACK" and hasattr(m, "encode"):
            try:
                return m.encode(texts).tolist()
            except Exception as e:
                logger.warning(f"Model encoding failed ({e}). Using fallback vector encoder.")

        # Fast deterministic 384-dim embedding fallback
        embeddings = []
        for text in texts:
            vec = [0.0] * 384
            words = text.lower().split()
            for idx, word in enumerate(words):
                h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
                pos = h % 384
                val = ((h >> 8) % 100) / 100.0
                vec[pos] += val
            # Normalize vector
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [round(x / norm, 5) for x in vec]
            embeddings.append(vec)
        return embeddings

    def create_index_mapping(self) -> bool:
        """Creates index mapping if connected to Elasticsearch."""
        if not self.client:
            return False

        config_path = Path(__file__).resolve().parent.parent / "configs" / "elasticsearch_mappings.json"
        if not os.path.exists(config_path):
            logger.error(f"Mapping file not found at: {config_path}")
            return False

        with open(config_path, encoding="utf-8") as f:
            mapping = json.load(f)

        try:
            if not self.client.indices.exists(index=self.index_name):
                self.client.indices.create(index=self.index_name, body=mapping)
                logger.info(f"Created Elasticsearch index mapping for '{self.index_name}'.")
            return True
        except Exception as e:
            logger.warning(f"Error creating ES index mapping: {e}")
            return False

    def index_store_payloads(self, store_payloads: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        """Encodes dense vectors and indexes store payloads."""
        logger.info(f"Indexing {len(store_payloads)} store payloads into search engine...")
        indexed_ids = []

        texts_to_embed = []
        for store in store_payloads:
            doc_text = f"{store.get('canonical_name', '')} {store.get('city', '')}. {store.get('why_found', '')} Categories: {', '.join(store.get('categories', []))}"
            texts_to_embed.append(doc_text)

        # Generate 384-dim dense vectors
        embeddings = self.encode_text(texts_to_embed)

        for idx, store in enumerate(store_payloads):
            sid = str(store.get("store_id"))
            vec = embeddings[idx]

            doc = dict(store)
            doc["store_embedding"] = vec
            doc["doc_text"] = texts_to_embed[idx]

            self.in_memory_index[sid] = doc
            indexed_ids.append(sid)

            if self.client:
                try:
                    self.client.index(index=self.index_name, id=sid, document=doc)
                except Exception as e:
                    logger.warning(f"ES index error for store {sid}: {e}")

        logger.info(f"Successfully indexed {len(indexed_ids)} store records.")
        return len(indexed_ids), indexed_ids
