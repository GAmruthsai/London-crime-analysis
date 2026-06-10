"""
clean.py
--------
Data cleaning and validation for London crime dataset.
Handles nulls, duplicates, date parsing, borough name standardisation,
outlier detection, and export of cleaned data.
"""

import pandas as pd
import numpy as np
import os


# Canonical borough names (32 London boroughs + City of London)
LONDON_BOROUGHS = [
    'Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley',
    'Camden', 'City of London', 'Croydon', 'Ealing', 'Enfield',
    'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Haringey', 'Harrow',
    'Havering', 'Hillingdon', 'Hounslow', 'Islington', 'Kensington and Chelsea',
    'Kingston upon Thames', 'Lambeth', 'Lewisham', 'Merton', 'Newham',
    'Redbridge', 'Richmond upon Thames', 'Southwark', 'Sutton', 'Tower Hamlets',
    'Waltham Forest', 'Wandsworth', 'Westminster'
]


def parse_dates(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
    """Parse date column and extract year, month, quarter."""
    print("[CLEAN] Parsing dates...")
    df[date_col] = pd.to_datetime(df[date_col], infer_datetime_format=True)
    df['year']    = df[date_col].dt.year
    df['month']   = df[date_col].dt.month
    df['quarter'] = df[date_col].dt.quarter
    df['year_month'] = df[date_col].dt.to_period('M')
    print(f"  Date range after parse: {df[date_col].min().date()} → {df[date_col].max().date()}")
    return df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Report and drop or impute nulls."""
    print("\n[CLEAN] Null value check:")
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if null_counts.empty:
        print("  ✅ No null values found.")
    else:
        print(null_counts)
        before = len(df)
        df = df.dropna(subset=['borough', 'major_category', 'value'])
        print(f"  Dropped {before - len(df)} rows with critical nulls.")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        print(f"[CLEAN] Removed {removed} duplicate rows.")
    else:
        print("[CLEAN] ✅ No duplicates found.")
    return df


def standardise_boroughs(df: pd.DataFrame, borough_col: str = 'borough') -> pd.DataFrame:
    """
    Standardise borough names — strip whitespace, fix known variants.
    Flags any boroughs not in the canonical London list.
    """
    print("\n[CLEAN] Standardising borough names...")
    df[borough_col] = df[borough_col].str.strip().str.title()

    # Fix common variants
    replacements = {
        'Hammersmith': 'Hammersmith and Fulham',
        'Kensington': 'Kensington and Chelsea',
        'Kingston': 'Kingston upon Thames',
        'Richmond': 'Richmond upon Thames',
    }
    df[borough_col] = df[borough_col].replace(replacements)

    unknown = set(df[borough_col].unique()) - set(LONDON_BOROUGHS)
    if unknown:
        print(f"  [WARN] Unrecognised boroughs: {unknown}")
    else:
        print("  ✅ All boroughs recognised.")
    return df


def validate_value_range(df: pd.DataFrame, value_col: str = 'value') -> pd.DataFrame:
    """Flag and remove negative or implausibly large crime counts."""
    print("\n[CLEAN] Validating crime count values...")
    negatives = (df[value_col] < 0).sum()
    if negatives:
        print(f"  [WARN] {negatives} negative values found — removing.")
        df = df[df[value_col] >= 0]
    outlier_threshold = df[value_col].quantile(0.999)
    outliers = (df[value_col] > outlier_threshold).sum()
    print(f"  99.9th percentile: {outlier_threshold:.0f} | Extreme outliers: {outliers}")
    print(f"  ✅ Value range: {df[value_col].min()} – {df[value_col].max()}")
    return df


def filter_years(df: pd.DataFrame, start: int = 2013, end: int = 2024) -> pd.DataFrame:
    """Filter dataset to 2013–2024 scope."""
    df = df[(df['year'] >= start) & (df['year'] <= end)]
    print(f"\n[CLEAN] Filtered to {start}–{end}: {len(df):,} rows remaining.")
    return df


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Run full cleaning pipeline."""
    print("=" * 55)
    print("  Running Data Cleaning Pipeline")
    print("=" * 55)
    df = parse_dates(df)
    df = handle_nulls(df)
    df = remove_duplicates(df)
    df = standardise_boroughs(df)
    df = validate_value_range(df)
    df = filter_years(df)
    print(f"\n[CLEAN] ✅ Clean dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def save_processed(df: pd.DataFrame, filename: str = 'cleaned_crime_data.csv',
                   out_dir: str = 'data/processed'):
    """Save cleaned DataFrame to processed folder."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    df.to_csv(path, index=False)
    print(f"[SAVE] Cleaned data saved to: {path}")
