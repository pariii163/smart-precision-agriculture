import pandas as pd


def basic_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic preprocessing:
    - handles missing values
    - removes duplicate rows
    """

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Handle missing values (simple strategy for now)
    df = df.dropna()

    return df


if __name__ == "__main__":
    print("Preprocessing module ready")
