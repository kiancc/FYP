# Generated and editing using Gemini 3.1, with the following prompt and passing it the master_prompts.csv:
# 'How can I take this and create a small test prompt batch that takes one prompt for each task for each genre?'
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
in_csv = base_dir / "master_prompts.csv"
out_csv = base_dir / "test_prompts_small.csv"

df = pd.read_csv(in_csv, dtype=str)

test_batch = (
    df.groupby(["genre", "task"], group_keys=False)
      .sample(n=1, random_state=42)
      .sort_values(["genre", "task"])
      .reset_index(drop=True)
)

for col in ["id", "file_id"]:
    if col in test_batch.columns:
        test_batch[col] = "TEST_" + test_batch[col].astype(str)

test_batch.to_csv(out_csv, index=False)

print("rows:", len(test_batch))
print("columns:", test_batch.columns.tolist())
print(test_batch[["genre", "task", "file_id"]].head(20))