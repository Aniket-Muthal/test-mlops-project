"""
data_validation.py
"""


import sys
import json
import pandas as pd
from lead_scoring.core.logging_setup import get_logger
from lead_scoring.core.exception import CustomException
from lead_scoring.config.entity_config import DataValidationConfig


logger = get_logger(name='data_validation', mode='a')

class DataValidation:
    def __init__(self, config: DataValidationConfig, mode: str = "raw"):
        self.config = config
        self.mode = mode

        if self.mode == "raw":
            self.df_path = self.config.raw_data_path
            self.schema = self.config.raw_schema
            self.valid_values = self.config.valid_values
            self.report_file_path = self.config.raw_val_report_path
            self.status_file_path = self.config.raw_val_status_path

        elif self.mode == "cleaned":
            self.df_path = self.config.cleaned_train_path
            self.schema = self.config.cleaned_schema
            self.valid_values = self.config.cleaned_valid_values
            self.report_file_path = self.config.cleaned_val_report_path
            self.status_file_path = self.config.cleaned_val_status_path

        elif self.mode == "processed":
            raise NotImplementedError("Processed data validation not yet implemented.")
        
        else:
            raise ValueError(f"Invalid mode={self.mode}. Expected 'raw', 'cleaned' or 'processed'.")

        if not self.df_path:
            raise ValueError(f"No dataframe path configured for mode-{self.mode}")
        
        self.df = pd.read_csv(self.df_path)
        self.report = {}


    def _general_stats(self):
        try:
            logger.info(f"Generating stats for mode - {self.mode}...")

            count_rows, count_columns = int(self.df.shape[0]), int(self.df.shape[1])
            self.report["mode"] = self.mode
            self.report["count_rows"] = count_rows
            self.report["count_columns"] = count_columns

            logger.info(f"Mode: {self.mode}, Shape: {self.df.shape}")
            logger.info(f"General stats for mode = {self.mode} noted.")
            
        except Exception as e:
            logger.error('Failed to generate stats.')
            raise CustomException(e, sys) from e


    def _validate_target(self):
        try:
            logger.info("Validating target feature...")

            target_issues = {}
            dtype_issues = {}

            logger.info("Checking existence of target feature...")

            if 'target_feature' not in self.schema:
                raise ValueError("'target_feature' missing from schema.")

            target_dict_items_list = list(self.schema.get('target_feature').items())[0]
            expected_target_col,  = list(target_dict_items_list)[0], 
            expected_target_dtype = list(target_dict_items_list)[1]

            if expected_target_col not in self.df.columns:
                target_issues["target_missing"] = True
                self.report["target_missing"] = True

                logger.info("Target feature missing.")

            else:
                logger.info("Target feature exists.")
                logger.info("Validating allowed target values...")

                allowed_target_values = {0, 1}
                invalid_target_values = list(set(self.df[expected_target_col].dropna().unique()) - allowed_target_values)
                target_issues["invalid_target_values"] = invalid_target_values

                logger.info("Allowed target values validated.")
                logger.info("Validating datatype of target feature...")

                if expected_target_dtype != str(self.df[expected_target_col].dtype):
                    dtype_issues["expected_dtype"] = expected_target_dtype
                    dtype_issues["actual_dtype"] = str(self.df[expected_target_col].dtype)

                logger.info("Datatype of target feature validated.")

            logger.info("Target feature validation completed.")

            target_issues["dtype_issues"] = dtype_issues
            self.report['target_issues'] = target_issues

        except Exception as e:
            logger.error('Failed to validate target feature.')
            raise CustomException(e, sys) from e


    def _validate_features(self):
        try:
            logger.info("Validating features...")

            dtype_issues = {}

            expected_columns = (
                list(self.schema.get('features').keys()) + 
                list(self.schema.get('target_feature').keys())
            )
            actual_columns = list(self.df.columns)

            logger.info("Checking for missing or extra features...")

            missing_columns = [col for col in expected_columns if col not in actual_columns]
            extra_columns = [col for col in actual_columns if col not in expected_columns]

            logger.info("Missing or extra feature validation completed.")

            self.report["missing_features"] = missing_columns
            self.report["extra_features"] = extra_columns

            logger.info("Validating datatypes of features...")

            for col, expected_dtype in self.schema.get('features').items():
                if col in self.df.columns:
                    actual_dtype = str(self.df[col].dtype)
                    expected_dtype = str(expected_dtype)

                text_dtypes = ["object", "string", "str"]

                is_text_match = (
                    expected_dtype in text_dtypes
                    and actual_dtype in text_dtypes
                )

                if not is_text_match and actual_dtype != expected_dtype:
                    dtype_issues[col] = {
                        "expected_dtype": expected_dtype,
                        "actual_dtype": actual_dtype
                    }

            logger.info("Datatypes of features validated.")

            self.report["dtype_issues"] = dtype_issues

            logger.info("Feature validation completed.")

        except Exception as e:
            logger.error('Failed to validate features.')
            raise CustomException(e, sys) from e


    def _validate_data_quality(self):
        try:
            logger.info("Checking for duplicate entries count...")
            logger.info("Checking for missing values count...")

            duplicate_count = int(self.df.duplicated().sum())
            missing_count = int(self.df.isna().sum().sum())

            logger.info("Count of duplicate entries and missing entries noted.")

            if missing_count > 0:
                logger.info("Checking for feature-wise missing values count (if any)...")

                missing_values = {col: int(self.df[col].isna().sum()) for col in self.df.columns}
                self.report["missing_values"] = missing_values

                logger.info("Feature-wise missing values noted.")

            self.report["duplicate_count"] = duplicate_count
            self.report["missing_count"] = missing_count

        except Exception as e:
            logger.error("Failed to validate data quality.")
            raise CustomException(e, sys) from e


    def _validate_valid_values(self):
        try:
            logger.info("Checking for accurate and valid values...")

            categorical_issues = {}
            numerical_issues = {}

            logger.info("Categorical values validation started...")

            for col, allowed_values in self.valid_values.items():
                if col in self.df.columns:
                    normalized = self.df[col].dropna().astype(str).str.strip().str.lower()
                    allowed_set = set(v.lower() for v in allowed_values)
                    invalid_values = list(set(normalized.dropna().unique()) - allowed_set)

                    if invalid_values:
                        categorical_issues[col] = invalid_values

            logger.info("Categorical values validated.")
            logger.info("Numerical values validation started...")

            if self.mode == "raw":
                numeric_checks = {
                    'age': (0, None),
                    'website_visits': (0, None),
                    'time_spent_on_website': (0, None),
                    'page_views_per_visit': (0, None)
                }

            if self.mode == "cleaned":
                numeric_checks = {
                    'age': (0, None),
                    'website_visits': (0, None),
                    'web_time': (0, None),
                    'page_views_per_visit': (0, None)
                }

            for num_col, (min_value, max_value) in numeric_checks.items():
                if num_col in self.df.columns:
                    if min_value is not None:
                        below_min = int((self.df[num_col] < min_value).sum())
                        if below_min > 0:
                            numerical_issues[f"{num_col}_below_min"] = below_min
                    if max_value is not None:
                        above_max = int((self.df[num_col] > max_value).sum())
                        if above_max > 0:
                            numerical_issues[f"{num_col}_above_max"] = above_max
            
            logger.info("Numerical values validated.")
            logger.info("Data accuracy and allowed values validated.")

            self.report["categorical_issues"] = categorical_issues
            self.report["numerical_issues"] = numerical_issues
            
        except Exception as e:
            logger.error("Failed to validate valid values.")
            raise CustomException(e, sys) from e


    def _export_val_report(self):
        try:
            logger.info("Evaluating hard fail boolean...")
            target_has_issues = (
                bool(self.report["target_issues"].get("invalid_target_values"))
                or bool(self.report["target_issues"].get("dtype_issues"))
                or self.report["target_issues"].get("target_missing", False)

            )

            hard_fail = (
                len(self.report["missing_features"]) > 0 or
                len(self.report["extra_features"]) > 0 or
                len(self.report["dtype_issues"]) > 0 or
                target_has_issues
            )
            logger.info("Hard fail evaluated.")

            if self.mode == "cleaned":
                logger.info("Evaluating 'soft fail - stage 1' boolean...")
                soft_fail_stage1 = (
                    any(v > 0 for v in self.report["numerical_issues"].values()) or  
                    any(len(v) > 0 for v in self.report["categorical_issues"].values()) or
                    self.report["duplicate_count"] > 0 or
                    target_has_issues
                )
                logger.info("Soft fail I evaluated.")

            logger.info("Deciding validation gates based on mode...")
            if self.mode == "raw":
                hard_fail = hard_fail
            
            if self.mode == "cleaned":
                hard_fail = hard_fail or soft_fail_stage1

            validation_status = not hard_fail

            self.report["validation_status"] = validation_status

            logger.info("Validation gate pass decided.")

            logger.info("Exporting validation status text file...")
            with open(self.status_file_path, "w") as status_file:
                status_file.write(f"Validation status:{validation_status}")

            logger.info("Validation status text file exported.")


            logger.info("Exporting validation report json file...")
            with open(self.report_file_path, "w") as report_file:
                json.dump(self.report, report_file, indent=4)

            logger.info("Validation report json file exported.")

        except Exception as e:
            logger.error("Failed to export validation report.")
            raise CustomException(e, sys) from e


    def run_validation(self):
        try:
            logger.info("Executing validation in order...")

            self._general_stats()
            self._validate_target()
            self._validate_features()
            self._validate_data_quality()
            self._validate_valid_values()
            self._export_val_report()

            logger.info("Validation executed successfully.")

        except Exception as e:
            logger.error("Validation execution failed.")
            logger.error(e)
            raise CustomException(e, sys)
