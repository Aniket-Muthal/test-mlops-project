"""
feature_preprocessor.py
"""


import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class FeaturePreprocessor(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            num_features: list | None = None,
            cat_features: list | None = None,
            numerical_imputation_strategy: str = "median",
            categorical_imputation_strategy: str = "most_frequent",
            drop: str | None = "first",
            sparse_output: bool = False,
            handle_unknown: str = "ignore"
        ):

        self.num_features: list | None = num_features
        self.cat_features: list | None = cat_features

        self.numerical_imputation_strategy: str = numerical_imputation_strategy
        self.categorical_imputation_strategy: str = categorical_imputation_strategy

        self.drop: str | None = drop
        self.sparse_output: bool = sparse_output
        self.handle_unknown: str = handle_unknown


    def fit(self, X: pd.DataFrame, y=None) -> "FeaturePreprocessor":
        X = self._validate_input(X, validate_schema=False)

        self._validate_feature_configuration(X)

        num_imputer = SimpleImputer(
            strategy=self.numerical_imputation_strategy,
            keep_empty_features=True
        )

        cat_imputer = SimpleImputer(
            strategy=self.categorical_imputation_strategy,
            keep_empty_features=True
        )

        num_scaler = StandardScaler()

        cat_encoder = OneHotEncoder(
            drop=self.drop,
            sparse_output=self.sparse_output,
            handle_unknown=self.handle_unknown,
        )

        imputation_transformers = []
        if self.num_features_:
            imputation_transformers.append(
                ('num_imputation', num_imputer, self.num_features_)
            )

        if self.cat_features_:
            imputation_transformers.append(
                ('cat_imputation', cat_imputer, self.cat_features_)
            )

        imputation_preprocessor = (
            ColumnTransformer(
                transformers=imputation_transformers,
                remainder='passthrough',
                verbose_feature_names_out=False
            )
            .set_output(transform="pandas")
        )

        feature_transformers = []
        if self.num_features_:
            feature_transformers.append(
                ('num_scaling', num_scaler, self.num_features_)
            )

        if self.cat_features_:
            feature_transformers.append(
                ('cat_encoding', cat_encoder, self.cat_features_)
            )

        feature_preprocessor = (
            ColumnTransformer(
                transformers=feature_transformers,
                remainder="passthrough",
                verbose_feature_names_out=False
            )
            .set_output(transform="pandas")
        )

        X_imputed = imputation_preprocessor.fit_transform(X)

        feature_preprocessor.fit(X_imputed)

        ## Commit fitted states
        self.feature_names_in_ = X.columns.to_numpy(copy=True)

        self.imputation_preprocessor_ = imputation_preprocessor
        self.feature_preprocessor_ = feature_preprocessor

        return self


    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(
            self,
            attributes=[
                "imputation_preprocessor_",
                "feature_preprocessor_"
            ]
        )

        X = self._validate_input(X)

        X_imputed = self.imputation_preprocessor_.transform(X)
        X_transformed = self.feature_preprocessor_.transform(X_imputed)

        return X_transformed


    def impute_only(self, X: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(
            self,
            attributes=[
                "imputation_preprocessor_"
            ]
        )

        X = self._validate_input(X)

        return self.imputation_preprocessor_.transform(X)


    def get_feature_names_out(self, input_features=None):
        check_is_fitted(
            self,
            attributes=[
                "feature_preprocessor_"
            ]
        )

        return self.feature_preprocessor_.get_feature_names_out(
            input_features=input_features
        )


    def _validate_input(self, X: pd.DataFrame, validate_schema: bool = True) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be pandas DataFrame.")
        
        if not X.columns.is_unique:
            raise ValueError("Input DataFrame must have unique column names.")

        if validate_schema and hasattr(self, "feature_names_in_"):
            expected = set(self.feature_names_in_)
            actual = set(X.columns)

            missing = expected - actual
            unexpected = actual - expected

            if missing or unexpected:
                raise ValueError(
                    f"Input schema mismatch: "
                    f"Missing columns: {sorted(missing)}; "
                    f"Unexpected columns: {sorted(unexpected)}"
                )

            X = X.loc[:, self.feature_names_in_]

        return X


    def _validate_feature_configuration(self, X: pd.DataFrame) -> None:
        if self.num_features is None:
            self.num_features_ = (
                X.select_dtypes(
                    include=["number"]
                )
                .columns
                .to_list()
            )
        else:
            self.num_features_ = list(self.num_features)
        
        if self.cat_features is None:
            self.cat_features_ = (
                X.select_dtypes(
                    include=["object", "string", "category", "bool"]
                )
                .columns
                .to_list()
            )
        else:
            self.cat_features_ = list(self.cat_features)
        
        if (not self.cat_features_) and (not self.num_features_):
            raise ValueError("No categorical or numerical columns found.")
        
        if len(set(self.num_features_)) != len(self.num_features_):
            raise ValueError("Duplicate numerical feature names.")
        
        if len(set(self.cat_features_)) != len(self.cat_features_):
            raise ValueError("Duplicate categorical feature names.")
        
        overlap = set(self.cat_features_) & set(self.num_features_)
        
        if overlap:
            raise ValueError(
                f"Features canot be both categorical and numerical: "
                f"{sorted(overlap)}"
            )
        
        selected_features = set(self.num_features_) | set(self.cat_features_)
        missing_features = selected_features - set(X.columns)
        unhandled_features = set(X.columns) - selected_features
        
        if missing_features:
            raise ValueError(
                f"Configured features are missing from X: "
                f"{sorted(missing_features)}"
            )
        
        if unhandled_features:
            raise ValueError(
                f"Features have no preprocessing configuration: "
                f"{sorted(unhandled_features)}"
            )
