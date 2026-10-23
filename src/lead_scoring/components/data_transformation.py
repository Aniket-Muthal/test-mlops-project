"""
data_transformation.py
"""


import sys
import joblib
import pandas as pd
from typing import Any
from pathlib import Path
from dataclasses import dataclass
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.entity_config import DataTransformationConfig
from lead_scoring.transformers.feature_preprocessor import FeaturePreprocessor


logger = get_logger(name="data_transformation")


@dataclass
class TrainTestSplit:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.DataFrame
    y_test: pd.DataFrame


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config: DataTransformationConfig = config
        self.ohe: dict[str | Any] = self.config.one_hot_encoder

        drop: str | None = self.ohe.get("drop", "first")
        sparse_output: bool = self.ohe.get("sparse_output", False)
        handle_unknown: str = self.ohe.get("handle_unknown", "ignore")

        self.preprocessor = FeaturePreprocessor(
            num_features=self.config.numerical_features,
            cat_features=self.config.categorical_features,
            numerical_imputation_strategy=self.config.numerical_imputation_strategy,
            categorical_imputation_strategy=self.config.categorical_imputation_strategy,
            drop=drop,
            sparse_output=sparse_output,
            handle_unknown=handle_unknown
        )

    def _load_train_test_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        try:
            logger.info("Loading cleaned train and test data...")
            self.cleaned_train_path: Path = self.config.cleaned_train_path
            self.cleaned_test_path: Path = self.config.cleaned_test_path

            if (not self.cleaned_train_path) or (not self.cleaned_test_path):
                raise ValueError("Train and test data paths not configured.")

            train_df = pd.read_csv(self.cleaned_train_path)
            test_df = pd.read_csv(self.cleaned_test_path)

            if train_df.empty:
                logger.info("Loaded train dataset contains no rows.")
                raise ValueError("Loaded train dataset contains no rows.")

            if test_df.empty:
                logger.info("Loaded train dataset contains no rows.")
                raise ValueError("Loaded train dataset contains no rows.")

            logger.info("Cleaned train and test data loaded.")
            logger.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}.")

            return train_df, test_df
        
        except Exception as e:
            logger.error("Failed to load train and test data.")
            logger.error(e)
            raise CustomException(e, sys)


    def _split_data(self, train_data: pd.DataFrame, test_data: pd.DataFrame) -> TrainTestSplit:
        try:
            logger.info("Separating independent and dependent variables...")
            if train_data.empty or test_data.empty:
                logger.warning("Loaded empty dataframe(s).")
                raise ValueError("Empty dataframe(s).")

            target: str = self.config.target_column

            logger.info("Train data: separating independent and dependent variables...")
            X_train = train_data.drop(columns=[target])
            y_train = train_data[[target]]

            logger.info("Test data: separating independent and dependent variables...")
            X_test = test_data.drop(columns=[target])
            y_test = test_data[[target]]

            logger.info(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}.")
            logger.info(f"X_test shape: {X_test.shape}, y_train shape: {y_test.shape}.")
            logger.info("Independent and dependent variables separated for both train and test data.")

            return X_train, X_test, y_train, y_test

        except Exception as e:
            logger.error("Failed to split data into X_train, X_test, y_train, y_test")
            logger.error(e)
            raise CustomException(e, sys)


    def _impute_and_save_data(self, data: TrainTestSplit):
        try:
            X_train, X_test = data.X_train, data.X_test
            y_train, y_test = data.y_train, data.y_test

            logger.info("Preserving lead IDs for train and test data...")
            train_ids = X_train[[self.config.columns_to_drop]]
            test_ids = X_test[[self.config.columns_to_drop]]
            logger.info("Lead IDs for train and test data separated.")

            logger.info("Imputing train and test data...")
            X_train = X_train.drop(columns=[self.config.columns_to_drop])
            X_test = X_test.drop(columns=[self.config.columns_to_drop])

            logger.info("Fitting imputation transformer...")
            self.preprocessor.fit(X_train)
            logger.info("Imputation transformer fitted.")

            logger.info("Transforming imputation on input train and test data...")
            X_train_imputed = self.preprocessor.impute_only(X_train)
            X_test_imputed = self.preprocessor.impute_only(X_test)
            logger.info("Train and test data imputation completed.")

            logger.info("Combining independent & dependent variables of train and test data...")
            logger.info("Lead IDs preserved for analytics.")
            imputed_train_df = pd.concat([train_ids, X_train_imputed, y_train], axis=1)
            imputed_test_df = pd.concat([test_ids, X_test_imputed, y_test], axis=1)
            logger.info("Unified train and test dataset (along with lead IDs) constructed.")

            logger.info("Saving imputed train and test data...")

            if not imputed_train_df.empty:
                imputed_train_df.to_csv(self.config.processed_train_path, index=False)

            if not imputed_test_df.empty:
                imputed_test_df.to_csv(self.config.processed_test_path, index=False)

            logger.info("Imputed train and test data saved successfully.")

        except Exception as e:
            logger.error("Failed to impute and save data.")
            logger.error(e)
            raise CustomException(e, sys)


    def _transform_and_save_data(self, data: TrainTestSplit) -> FeaturePreprocessor:
        try:
            X_train, X_test = data.X_train, data.X_test
            y_train, y_test = data.y_train, data.y_test

            logger.info("Preserving lead IDs for train and test data...")
            train_ids = X_train[[self.config.columns_to_drop]]
            test_ids = X_test[[self.config.columns_to_drop]]
            logger.info("Lead IDs for train and test data separated.")

            logger.info("Transforming train and test data...")
            X_train = X_train.drop(columns=[self.config.columns_to_drop])
            X_test = X_test.drop(columns=[self.config.columns_to_drop])
            
            logger.info("Fitting feature transformer...")
            self.preprocessor.fit(X_train)
            logger.info("Feature transformer fitted.")

            logger.info("Transforming features of input train and test data...")
            X_train_transformed = self.preprocessor.transform(X_train)
            X_test_transformed = self.preprocessor.transform(X_test)
            logger.info("Train and test data transformation completed.")
            logger.info(f"X_train shape: {X_train_transformed.shape}.")
            logger.info(f"X_test shape: {X_test_transformed.shape}.")

            logger.info("Combining independent & dependent variables of train and test data...")
            logger.info("Lead IDs preserved for analytics.")
            transformed_train_df = pd.concat([train_ids, X_train_transformed, y_train], axis=1)
            transformed_test_df = pd.concat([test_ids, X_test_transformed, y_test], axis=1)
            logger.info("Unified train and test dataset (along with lead IDs) constructed.")

            logger.info("Saving transformed train and test data...")

            if not transformed_train_df.empty:
                transformed_train_df.to_csv(self.config.transformed_train_path, index=False)

            if not transformed_test_df.empty:
                transformed_test_df.to_csv(self.config.transformed_test_path, index=False)

            logger.info("Transformed train and test data saved successfully.")

            return self.preprocessor    

        except Exception as e:
            logger.error("Failed to transform and save data.")
            logger.error(e)
            raise CustomException(e, sys)


    def _save_preprocessor_object(self, preprocessor_object: FeaturePreprocessor):
        try:
            logger.info("Saving serialized feature preprocessor object...")

            if not self.config.preprocessor_path:
                raise ValueError("Path to save preprocessor object not configured.")
            
            joblib.dump(
                value=preprocessor_object,
                filename=self.config.preprocessor_path
            )

            logger.info("Serialized feature preprocessor object saved.")

        except Exception as e:
            logger.error("Failed to save serialized feature preprocessor object.")
            logger.error(e)
            raise CustomException(e, sys)


    def run_data_transformation(self):
        try:
            train_df, test_df = self._load_train_test_data()

            X_train, X_test, y_train, y_test = self._split_data(
                train_data=train_df,
                test_data=test_df
            )

            self._impute_and_save_data(
                data=TrainTestSplit(
                    X_train=X_train, X_test=X_test,
                    y_train=y_train, y_test=y_test
                )
            )

            preprocessor_obj = self._transform_and_save_data(
                data=TrainTestSplit(
                    X_train=X_train, X_test=X_test,
                    y_train=y_train, y_test=y_test
                )
            )

            self._save_preprocessor_object(
                preprocessor_object = preprocessor_obj
            )

        except Exception as e:
            logger.error("Data transformation failed.")
            logger.error(e)
            raise CustomException(e, sys)
