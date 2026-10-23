"""
cleaning_runner.py
"""


import sys
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.paths import PARAMS_FILE_PATH
from lead_scoring.config.entity_config import DataCleaningConfig
from lead_scoring.config.configuration import ConfigurationManager
from lead_scoring.components.data_cleaning import DataCleaning


logger = get_logger(name="data_cleaning")


def main():
    try:
        logger.info("Executing data cleaning runner...")

        logger.info("Initializing configuration manager...")
        config_manager = ConfigurationManager(params_file_path=PARAMS_FILE_PATH)
        logger.info("Configuration manager initialized.")

        logger.info("Invoking data cleaning config...")
        cleaning_config = config_manager.get_data_cleaning_config()
        logger.info("Data cleaning config invoked.")

        logger.info("Confirming validation checks...")
        validation_file_path = cleaning_config.raw_val_status_path
        with open(validation_file_path, "r") as f:
            status = f.read().split(":")[-1]
        logger.info(f"Validation status for raw mode: {status}.")

        if status == "True":
            logger.info("Data cleaning started...")
            data_cleaning = DataCleaning(config=cleaning_config)
            data_cleaning.run_data_cleaning()
            logger.info("Data cleaning completed successfully.")
        else:
            logger.error("Validation checks failed.")
            raise Exception("Data schema is not valid.")

    except Exception as e:
        logger.error("Failed to execute cleaning runner.")
        logger.error(e)
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
