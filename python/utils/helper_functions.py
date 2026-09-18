import pandas as pd


def load_csv(path):
    """Load CSV file"""
    return pd.read_csv(path)


def load_excel(path, sheet_name):
    """Load Excel sheet"""
    return pd.read_excel(path, sheet_name=sheet_name)