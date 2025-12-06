import json
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "books.csv"

def main() -> None:
    df = pd.read_csv(DATA_PATH, on_bad_lines="skip")
    summary = []
    for col in df.columns:
        ser = df[col]
        dtype = str(ser.dtype)
        examples = ser.dropna().astype(str).head(3).tolist()
        entry = {
            "column": col,
            "dtype": dtype,
            "examples": examples,
            "non_null_count": int(ser.notna().sum()),
        }
        if dtype == "object":
            entry["max_length"] = int(ser.dropna().astype(str).str.len().max())
        else:
            min_val = ser.min()
            max_val = ser.max()
            if hasattr(min_val, "item"):
                min_val = min_val.item()
            if hasattr(max_val, "item"):
                max_val = max_val.item()
            entry["min"] = min_val
            entry["max"] = max_val
        summary.append(entry)

    print(json.dumps({"rows": len(df), "columns": len(df.columns), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
