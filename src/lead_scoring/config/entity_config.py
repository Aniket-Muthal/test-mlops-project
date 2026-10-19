from pathlib import Path
from dataclasses import dataclass


## ---------------------------------------------------------------------- ##
@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration for the data ingestion stage.

    Defines parameters required to load raw data from source
    and save/export it to desired directory.
    """
    source_data_url: str
    raw_data_path: Path