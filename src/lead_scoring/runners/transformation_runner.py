"""
transformation_runner.py
"""


import sys
import pandas as pd
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.paths import PARAMS_FILE_PATH
from lead_scoring.config.configuration import ConfigurationManager
from lead_scoring.components.data_transformation import DataTransformation


logger = get_logger(name="data_transformation")


def main():
    try:
        logger.info("Executing data transformation runner...")

        logger.info("Initializing configuration manager...")
        config_manager = ConfigurationManager(params_file_path=PARAMS_FILE_PATH)
        logger.info("Configuration manager initialized.")

        logger.info("Invoking data transformation config...")
        transformation_config = config_manager.get_data_transformation_config()
        logger.info("Data transformation config invoked.")

        logger.info("Confirming validation checks...")
        validation_file_path = transformation_config.cleaned_val_status_path
        with open(validation_file_path, "r") as f:
            status = f.read().split(":")[-1]
        logger.info(f"Validation status for cleaned mode: {status}.")

        if status == "True":
            logger.info("Data transformation started...")
            data_transformation = DataTransformation(config=transformation_config)
            data_transformation.run_data_transformation()
            logger.info("Data transformation completed successfully.")
        else:
            logger.error("Validation checks failed.")
            raise Exception("Data schema is not valid.")

    except Exception as e:
        logger.error("Failed to execute transformation runner.")
        logger.error(e)
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
