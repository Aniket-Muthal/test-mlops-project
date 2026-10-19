"""
data_ingestion.py
"""


import sys
import pandas as pd
from pathlib import Path
from lead_scoring.utils.data_io import create_directories
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.entity_config import DataIngestionConfig


logger = get_logger(name='data_ingestion', mode='w')


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

        self.raw_data_path = Path(self.config.raw_data_path)
        raw_data_dir = self.raw_data_path.parent

        if raw_data_dir.exists():
            logger.info('Raw data directory exists.')
        else:
            create_directories([raw_data_dir])
            logger.info('Raw data directory created.')


    def fetch_data(self):

        try:
            source_data_url = self.config.source_data_url

            logger.info("Fetching data from source url...")

            df = pd.read_csv(source_data_url)

            if df.empty:
                raise ValueError("The downloaded dataset contains no rows.")
            
            df.to_csv(self.raw_data_path, index=False)

            if (
                not self.raw_data_path.is_file()
                or self.raw_data_path.stat().st_size==0
            ):
                raise RuntimeError("Data fetching failed or produced an empty file.")

            logger.info("Data fetched successfully.")
            logger.info(f"Shape: {df.shape}")

        except Exception as e:
            logger.error("Data fetching failed.")
            raise CustomException(e, sys) from e
