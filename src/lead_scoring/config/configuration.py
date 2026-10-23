"""
configuration.py

Central configuration manager for the lead scoring MLOps pipeline.
"""


from pathlib import Path
from lead_scoring.utils.data_io import load_yaml, create_directories
from lead_scoring.config.entity_config import (
    DataIngestionConfig, DataValidationConfig,
    DataCleaningConfig, DataTransformationConfig
)


class ConfigurationManager:
    def __init__(self, params_file_path: Path):
        self.params_file_path = params_file_path
        self.params = load_yaml(path_to_yaml=self.params_file_path)

        create_directories(
            [
                Path(self.params.data_ingestion.raw_data_path).parent,
                Path(self.params.data_validation.raw_val_report_path).parent,
                Path(self.params.data_cleaning_split.cleaned_train_path).parent,
                Path(self.params.data_validation.cleaned_val_report_path).parent,
                Path(self.params.data_transformation.processed_train_path).parent,
                Path(self.params.data_transformation.transformed_train_path).parent,
                Path(self.params.data_transformation.preprocessor_path).parent
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
        cleaned_schema = self.params.cleaned_data_validation.schema
        cleaned_valid_values = self.params.cleaned_data_validation.valid_values

        data_validation_config = DataValidationConfig(
            raw_data_path=Path(config.raw_data_path),
            raw_val_report_path=Path(config.raw_val_report_path),
            raw_val_status_path=Path(config.raw_val_status_path),
            raw_schema=dict(schema),
            valid_values=dict(valid_values),
            cleaned_train_path=Path(config.cleaned_train_path),
            cleaned_val_report_path=Path(config.cleaned_val_report_path),
            cleaned_val_status_path=Path(config.cleaned_val_status_path),
            cleaned_schema=dict(cleaned_schema),
            cleaned_valid_values=dict(cleaned_valid_values)
        )

        return data_validation_config


    def get_data_cleaning_config(self) -> DataCleaningConfig:
        config = self.params.data_cleaning_split

        data_cleaning_config = DataCleaningConfig(
            raw_data_path=Path(config.raw_data_path),
            raw_val_status_path=Path(config.raw_val_status_path),
            cleaned_train_path=Path(config.cleaned_train_path),
            cleaned_test_path=Path(config.cleaned_test_path),
            random_state=int(config.random_state),
            test_size=float(config.test_size),
            stratify_column=str(config.stratify_column)
        )

        return data_cleaning_config


    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.params.data_transformation

        data_transformation_config = DataTransformationConfig(
            cleaned_val_status_path=Path(config.cleaned_val_status_path),
            cleaned_train_path=Path(config.cleaned_train_path),
            cleaned_test_path=Path(config.cleaned_test_path),
            processed_train_path=Path(config.processed_train_path),
            processed_test_path=Path(config.processed_test_path),
            transformed_train_path=Path(config.transformed_train_path),
            transformed_test_path=Path(config.transformed_test_path),
            preprocessor_path=Path(config.preprocessor_path),
            target_column=str(config.target_column),
            columns_to_drop=str(config.columns_to_drop),
            numerical_imputation_strategy=str(config.numerical_imputation_strategy),
            categorical_imputation_strategy=str(config.categorical_imputation_strategy),
            one_hot_encoder=dict(config.one_hot_encoder),
            numerical_features=list(config.numerical_features),
            categorical_features=list(config.categorical_features)
        )

        return data_transformation_config
