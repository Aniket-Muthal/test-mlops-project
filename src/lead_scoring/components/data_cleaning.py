"""
data_cleaning.py
"""


import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.entity_config import DataCleaningConfig
from lead_scoring.transformers.feature_cleaner import clean_data


logger = get_logger(name='data_cleaning')


class DataCleaning:
    def __init__(self, config: DataCleaningConfig):
        self.config = config


    def _load_raw_data(self) -> pd.DataFrame:
        try:
            logger.info("Loading raw data...")
            raw_data_path = self.config.raw_data_path

            if not raw_data_path:
                raise ValueError("No data path configured.")
            
            df = pd.read_csv(raw_data_path)

            if df.empty:
                logger.info("Loaded dataset contains no rows.")
                raise ValueError("Loaded dataset contains no rows.")
            
            logger.info("Raw dataset loaded.")
            logger.info(f"Raw data shape: {df.shape}")

            return df

        except Exception as e:
            logger.error("Failed to load data.")
            logger.error(e)
            raise CustomException(e, sys)


    def _split_clean_data(self, clean_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        try:
            logger.info("Splitting data into train and test sets...")

            train_df, test_df = train_test_split(
                clean_data,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
                stratify=clean_data[self.config.stratify_column]
            )

            logger.info("Clean data split into train and test sets.")
            logger.info(f"Train set Shape: {train_df.shape}.")
            logger.info(f"Test set Shape: {test_df.shape}.")

            return train_df, test_df

        except Exception as e:
            logger.error("Failed to split data into train and test sets.")
            logger.error(e)
            raise CustomException(e, sys)

        
    def _save_clean_data(self, train_data: pd.DataFrame, test_data: pd.DataFrame):
        try:
            logger.info("Saving clean train and test data...")

            clean_train_path = self.config.cleaned_train_path
            clean_test_path = self.config.cleaned_test_path

            if (not clean_train_path) or (not clean_test_path):
                raise ValueError("Target paths are not configured.")

            train_data.to_csv(clean_train_path, index=False)
            test_data.to_csv(clean_test_path, index=False)

            logger.info("Clean train and test data saved.")

        except Exception as e:
            logger.info("Failed to save clean data.")
            logger.error(e)
            raise CustomException(e, sys)   


    def run_data_cleaning(self):
        try:
            df = self._load_raw_data()

            logger.info("Loading feature cleaner...")
            logger.info("Feature cleaner loaded and cleaning operation started...")

            clean_df = clean_data(data=df)

            logger.info("Data cleaning completed.")

            train_df, test_df = self._split_clean_data(clean_data=clean_df)
            self._save_clean_data(train_data=train_df, test_data=test_df)

        except Exception as e:
            logger.info("Data cleaning failed.")
            logger.error(e)
            raise CustomException(e, sys)
        