import pandas as pd

# Change filename if needed
df = pd.read_csv("data/soil_datasets/crop_recommendation.csv")

print("\nCrop Distribution:\n")
print(df['label'].value_counts())

print("\nPercentage Distribution:\n")
print(df['label'].value_counts(normalize=True) * 100)
