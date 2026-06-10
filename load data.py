"""
load_data.py
------------
Data ingestion utilities for London crime and socio-economic datasets.
Supports CSV files from data.police.uk, London Datastore, and ONS.
"""

import pandas as pd
import os


EXPECTED_CRIME_COLS = ['date', 'borough', 'major_category', 'minor_category', 'value']
EXPECTED_SOCIO_COLS = ['borough', 'year', 'deprivation_score', 'unemployment_rate']


def load_crime_data(filepath: str) -> pd.DataFrame:
    """
    Load raw London crime CSV.
    Expected columns: date, borough, major_category, minor_category, value
    """
    print(f"[LOAD] Crime data from: {filepath}")
    df = pd.read_csv(filepath)

    # Normalise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    print(f"  Shape      : {df.shape}")
    print(f"  Columns    : {list(df.columns)}")
    print(f"  Date range : {df['date'].min()} → {df['date'].max()}" if 'date' in df.columns else "  [WARN] No date column found")
    print(f"  Boroughs   : {df['borough'].nunique() if 'borough' in df.columns else 'N/A'} unique")
    return df


def load_socioeconomic_data(filepath: str) -> pd.DataFrame:
    """
    Load ONS socio-economic indicators CSV.
    Expected columns: borough, year, deprivation_score, unemployment_rate
    """
    print(f"[LOAD] Socio-economic data from: {filepath}")
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print(f"  Shape   : {df.shape}")
    print(f"  Columns : {list(df.columns)}")
    return df


def validate_columns(df: pd.DataFrame, expected: list, dataset_name: str):
    """Warn about any missing expected columns."""
    missing = [c for c in expected if c not in df.columns]
    if missing:
        print(f"[WARN] {dataset_name} — missing expected columns: {missing}")
        print(f"       Available columns: {list(df.columns)}")
    else:
        print(f"[OK]  {dataset_name} — all expected columns present.")
    return df
