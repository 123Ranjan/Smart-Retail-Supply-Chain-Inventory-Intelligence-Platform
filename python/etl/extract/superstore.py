import pandas as pd
from pathlib import Path


def extract_superstore():

    project_root = Path(__file__).resolve().parents[3]

    file_path = (
        project_root
        / "data"
        / "raw"
        / "superstore.csv"
    )

    df = pd.read_csv(file_path)

    print(f"Superstore extracted: {len(df)} rows")

    return df