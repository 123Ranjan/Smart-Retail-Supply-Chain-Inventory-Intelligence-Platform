import pandas as pd
from pathlib import Path


def extract_returns():

    project_root = Path(__file__).resolve().parents[3]

    file_path = (
        project_root
        / "data"
        / "raw"
        / "Superstore Dataset.xlsx"
    )

    df = pd.read_excel(
        file_path,
        sheet_name="Returns"
    )

    print(f"Returns extracted: {len(df)} rows")

    return df