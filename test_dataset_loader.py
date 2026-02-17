from src.data_ingestion.dataset_loader import load_csv_dataset
from src.data_ingestion.preprocessor import basic_preprocess

# Load raw dataset
df_raw = load_csv_dataset("data/soil_datasets/sample_soil_data.csv")
print("Raw data:")
print(df_raw)

# Preprocess dataset
df_clean = basic_preprocess(df_raw)
print("\nPreprocessed data:")
print(df_clean)
