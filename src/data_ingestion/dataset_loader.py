import pandas as pd
from pathlib import Path


def load_csv_dataset(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV dataset from the given path and performs basic validation.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {file_path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Loaded dataset is empty")

    return df


if __name__ == "__main__":
    print("Dataset loader module ready")
