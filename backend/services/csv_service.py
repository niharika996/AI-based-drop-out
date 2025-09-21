import pandas as pd

def merge_csvs(file_paths, output="data/merged_dataset.csv"):
    # Example assumption: CSVs have a common column "rollNo"
    merged_df = None
    for file in file_paths:
        df = pd.read_csv(file)
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="rollNo", how="outer")
    merged_df.to_csv(output, index=False)
    print("✅ Merged dataset created at", output)
    return output
