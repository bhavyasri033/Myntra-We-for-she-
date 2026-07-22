"""
Dataset Loader Module for ml_intelligence
Ingests raw merchant dataset files and validates records against StoreRawRecord Pydantic DTOs.
"""

import os
import pandas as pd
from pathlib import Path
from typing import List, Union
from ml_intelligence.api.schemas import StoreRawRecord, StoreDiscoveryInput, StoreDiscoveryOutput
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.discovery")


class DatasetLoader:
    """Ingests raw seller dataset files and returns validated StoreDiscoveryOutput DTOs."""

    def __init__(self, raw_source_path: Union[str, Path] = "Master Candidate Dataset v1.xlsx"):
        self.raw_source_path = str(raw_source_path)

    def load(self, source_tag: str = "MANUAL_CURATED_SEED") -> StoreDiscoveryOutput:
        """Loads and parses raw dataset into StoreDiscoveryOutput DTO."""
        disc_input = StoreDiscoveryInput(
            raw_source_path=self.raw_source_path,
            source_tag=source_tag
        )

        if not os.path.exists(disc_input.raw_source_path):
            fallback_path = os.path.basename(disc_input.raw_source_path)
            if os.path.exists(fallback_path):
                file_to_open = fallback_path
            else:
                logger.error(f"File not found at: {disc_input.raw_source_path}")
                raise FileNotFoundError(f"Raw dataset file not found at: {disc_input.raw_source_path}")
        else:
            file_to_open = disc_input.raw_source_path

        logger.info(f"Loading raw dataset from: {file_to_open}")
        if file_to_open.endswith(".xlsx") or file_to_open.endswith(".xls"):
            df = pd.read_excel(file_to_open)
        else:
            df = pd.read_csv(file_to_open)

        col_map = {
            "Region": "region",
            "Store": "raw_store_name",
            "Source Found": "source_found",
            "Why Found": "why_found",
            "region": "region",
            "store": "raw_store_name",
            "source found": "source_found",
            "why found": "why_found",
            "store_name": "raw_store_name"
        }
        df = df.rename(columns=col_map)

        for col in ["region", "raw_store_name", "source_found", "why_found"]:
            if col not in df.columns:
                df[col] = ""
            df[col] = df[col].fillna("").astype(str).str.strip()

        raw_records: List[StoreRawRecord] = []
        regions_set = set()

        for _, row in df.iterrows():
            reg = row["region"] if row["region"] else "Pan-India"
            regions_set.add(reg)

            record = StoreRawRecord(
                raw_store_name=row["raw_store_name"],
                region=reg,
                source_found=row["source_found"],
                why_found=row["why_found"]
            )
            raw_records.append(record)

        logger.info(f"Successfully validated {len(raw_records)} raw store records across {len(regions_set)} regions.")

        return StoreDiscoveryOutput(
            records_ingested=len(raw_records),
            regions_found=sorted(list(regions_set)),
            raw_stores=raw_records
        )
