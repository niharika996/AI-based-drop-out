import pandas as pd
import numpy as np

# Load the CSV file
input_file = "updated_file.csv"   # 🔹 replace with your CSV file path
df = pd.read_csv(input_file)

# Update columns with random values in specified ranges
df['attendance'] = np.random.randint(0, 101, size=len(df))       # 0–100
df['marks'] = np.random.randint(10, 101, size=len(df))           # 10–100
df['attempts'] = np.random.randint(0, 21, size=len(df))          # 0–20
df['fees_due'] = np.random.randint(30000, 160001, size=len(df))  # 30k–160k

# Save updated CSV
output_file = "newdataset.csv"   # 🔹 new file name
df.to_csv(output_file, index=False)

print(f"Updated file saved as: {output_file}")