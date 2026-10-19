"""
ingestion_runner.py
"""


import sys
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.paths import PARAMS_FILE_PATH
from lead_scoring.config.configuration import ConfigurationManager
from lead_scoring.components.data_ingestion import DataIngestion


def main():
    logger = get_logger(name='data_ingestion', mode='w')

    try:
        logger.info("Executing data ingestion runner...")

        logger.info("Initializing configuration manager...")
        config_manager = ConfigurationManager(params_file_path=PARAMS_FILE_PATH)
        logger.info("Configuration manager initialized.")

        logger.info('Invoking data ingestion config...')
        ingestion_config = config_manager.get_data_ingestion_config()
        logger.info('Data ingestion config invoked.')

        logger.info("Data ingestion started...")
        data_ingestion = DataIngestion(config=ingestion_config)
        data_ingestion.fetch_data()
        logger.info("Data ingestion completed succesfully.")

    except Exception as e:
        logger.error("Data ingestion runner failed.")
        logger.error(e)
        raise CustomException(e, sys)


if __name__ == '__main__':
    main()