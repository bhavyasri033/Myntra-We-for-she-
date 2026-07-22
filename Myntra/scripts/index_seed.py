"""
Dataset Indexing Script for Myntra Regional Fashion ML Intelligence Service
Triggers seed dataset loading, entity resolution, trust evaluation, and search indexing.
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from ml_intelligence.api.dependencies import get_service_container
from ml_intelligence.utils.logger import get_logger

logger = get_logger("scripts.index_seed")


def main():
    print("=== Myntra ML Intelligence - Seed Dataset Indexer ===")
    container = get_service_container()
    
    seed_file = sys.argv[1] if len(sys.argv) > 1 else "Master Candidate Dataset v1.xlsx"
    print(f"[INIT] Loading raw seed dataset from: {seed_file}")

    try:
        count = container.index_seed_dataset(raw_path=seed_file)
        regions = sorted(list(set(str(s.get("city", "")).title() for s in container.indexer.in_memory_index.values())))
        print(f"[SUCCESS] Successfully indexed {count} store records across {len(regions)} regions ({', '.join(regions)}).")
    except Exception as e:
        print(f"[ERROR] Indexing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
