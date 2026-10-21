"""
feature_cleaner.py

Feature-level data cleaning reusable utility for the ML pipeline.

Defines stateless `clean_data` function responsible for
deterministic cleaning operations on the input dataset.
"""


import pandas as pd
from pandas.api.types import is_string_dtype


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the input pandas dataframe and returns cleaned version.

    Operations performed:
    - Standardizes text columns
    - Renames some of the features
    - Standardizes feature names
    - Removes duplicate entries

    Parameters
    ----------
    data: pd.DataFrame
          input dataset to be cleaned.
    
    Returns
    -------
    pd.DataFrame
          Cleaned dataset.
    """
    clean_df = (
        data
        .apply(
            lambda col: col.str.strip().str.lower()
            if is_string_dtype(col.dtype)
            else col
        )
        .rename(columns={
            'current_occupation': 'occupation',
            'profile_completed': 'profile_completion_level',
            'time_spent_on_website': 'web_time',
            'last_activity': 'last_interaction',
            'print_media_type1': 'newspaper_ad_exposure',
            'print_media_type2': 'magazine_ad_exposure',
            'digital_media': 'digital_ad_exposure',
            'educational_channels': 'educational_forum_exposure',
            'referral': 'via_referral'
        })
        .rename(columns=str.lower)
        .drop_duplicates(keep='first', ignore_index=True)
    )
    return clean_df
