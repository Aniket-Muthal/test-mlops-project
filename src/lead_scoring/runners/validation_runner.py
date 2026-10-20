"""
validation_runner.py
"""


import sys
import argparse
from lead_scoring.config.paths import PARAMS_FILE_PATH
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.configuration import ConfigurationManager
from lead_scoring.components.data_validation import DataValidation


def main():
    logger = get_logger('data_validation')

    try:
        logger.info("Executing data validation runner...")

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--mode",
            type=str,
            required=True,
            choices=["raw", "cleaned", "processed"]
        )

        args = parser.parse_args()
        
        mode = args.mode

        logger.info("Initializing configuration manager...")
        configuration_manager = ConfigurationManager(params_file_path=PARAMS_FILE_PATH)
        logger.info("Configuration manager initialized.")

        logger.info('Invoking data validation config...')
        validation_config = configuration_manager.get_data_validation_config()
        logger.info('Data validation config invoked.')

        logger.info(f"Data validation started for mode={mode}...")
        data_validation = DataValidation(config=validation_config, mode=mode)
        data_validation.run_validation()
        logger.info(f"Data validation for mode={mode} completed succesfully.")

    except Exception as e:
        logger.error("Data validation runner failed.")
        raise CustomException(e, sys) from e


if __name__ == "__main__":
    main()
