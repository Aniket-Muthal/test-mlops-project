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


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Configuration for data validation across different pipeline modes.

    Holds schema definitions, valid value constraints, and validation
    artifact directories for raw, cleaned, and processed datasets.
    """
    raw_data_path: Path
    raw_val_report_path: Path
    raw_val_status_path: Path
    raw_schema: dict
    valid_values: dict
    cleaned_train_path: Path
    cleaned_val_report_path: Path
    cleaned_val_status_path: Path
    cleaned_schema: dict
    cleaned_valid_values: dict
    # processed_val_report_path: Path
    # processed_val_status_path: Path


@dataclass(frozen=True)
class DataCleaningConfig:
    """
    Configuration for data cleaning and split stage.

    Defines paths to load data from and to save it
    to desired directory. Also holds parameters
    necessary for data splitting.
    """
    raw_data_path: Path
    raw_val_status_path: Path
    cleaned_train_path: Path
    cleaned_test_path: Path
    random_state: int
    test_size: float
    stratify_column: str
