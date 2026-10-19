"""
configuration.py

Central configuration manager for the lead scoring MLOps pipeline.
"""


from pathlib import Path
from lead_scoring.utils.data_io import load_yaml, create_directories
from lead_scoring.config.entity_config import (
    DataIngestionConfig
)


class ConfigurationManager:
    def __init__(self, params_file_path: Path):
        self.params_file_path = params_file_path
        self.params = load_yaml(path_to_yaml=self.params_file_path)

        create_directories(
            [
                Path(self.params.data_ingestion.raw_data_path).parent
            ]
        )


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.params.data_ingestion

        data_ingestion_config = DataIngestionConfig(
            source_data_url=config.source_data_url,
            raw_data_path=Path(config.raw_data_path)
        )

        return data_ingestion_config