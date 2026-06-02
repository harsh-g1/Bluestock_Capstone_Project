import glob
import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
RAW_DIR = os.path.abspath(RAW_DIR)

csv_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))

for csv_file in csv_files:
    print("-" * 100)
    print(f"File: {os.path.basename(csv_file)}")
    try:
        df = pd.read_csv(csv_file)
        print(f"Shape: {df.shape}")
        print(f"Data types: \n {df.dtypes}")
        print(df.head(5).to_string(index=False))
    except Exception as exc:
        print(f"Failed to read {os.path.basename(csv_file)}: {exc}")

