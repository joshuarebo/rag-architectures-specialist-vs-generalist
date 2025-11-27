import pandas as pd

# Check both files
sac = pd.read_csv('sac_rag_golden_detailed.csv')
print("SAC-RAG columns:", sac.columns.tolist())
print("\nSample row:")
for col in sac.columns:
    print(f"  {col}: {sac.iloc[0][col]}")
