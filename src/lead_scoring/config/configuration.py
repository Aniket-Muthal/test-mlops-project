"""
configuration.py

Central configuration manager for the lead scoring MLOps pipeline.
"""


from pathlib import Path
from lead_scoring.utils.data_io import load_yaml, create_directories
from lead_scoring.config.entity_config import (
    DataIngestionConfig, DataValidationConfig
)


class ConfigurationManager:
    def __init__(self, params_file_path: Path):
        self.params_file_path = params_file_path
        self.params = load_yaml(path_to_yaml=self.params_file_path)

        create_directories(
            [
                Path(self.params.data_ingestion.raw_data_path).parent,
                Path(self.params.data_validation.raw_val_report_path).parent
            ]
        )


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.params.data_ingestion

        data_ingestion_config = DataIngestionConfig(
            source_data_url=config.source_data_url,
            raw_data_path=Path(config.raw_data_path)
        )

        return data_ingestion_config


    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.params.data_validation
        schema = self.params.raw_data_validation.schema
        valid_values = self.params.raw_data_validation.valid_values

        data_validation_config = DataValidationConfig(
            raw_data_path=Path(config.raw_data_path),
            raw_val_report_path=Path(config.raw_val_report_path),
            raw_val_status_path=Path(config.raw_val_status_path),
            raw_schema=dict(schema),
            valid_values=dict(valid_values)
        )

        return data_validation_config