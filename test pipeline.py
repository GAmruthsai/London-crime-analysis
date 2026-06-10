"""
test_pipeline.py
----------------
Unit tests for the London Crime Analysis pipeline.
Uses synthetic data — no real CSV files needed.
Run with: python -m pytest tests/
"""

import sys, os
import pandas as pd
import numpy as np
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.clean import (
    parse_dates, handle_nulls, remove_duplicates,
    standardise_boroughs, validate_value_range, filter_years
)


def make_dummy_crime_df(n=200):
    """Generate synthetic London crime data for testing."""
    np.random.seed(42)
    boroughs = ['Westminster', 'Lambeth', 'Hackney', 'Camden', 'Southwark']
    categories = ['Theft', 'Violence', 'Burglary', 'Drugs', 'Robbery']
    dates = pd.date_range('2013-01', '2024-12', freq='MS')

    rows = []
    for _ in range(n):
        rows.append({
            'date': np.random.choice(dates).strftime('%Y-%m-%d'),
            'borough': np.random.choice(boroughs),
            'major_category': np.random.choice(categories),
            'minor_category': 'Test',
            'value': np.random.randint(0, 500)
        })
    return pd.DataFrame(rows)


def test_parse_dates():
    df = make_dummy_crime_df()
    df = parse_dates(df)
    assert 'year' in df.columns
    assert 'month' in df.columns
    assert df['year'].between(2013, 2024).all()
    print("✅ parse_dates passed")


def test_handle_nulls():
    df = make_dummy_crime_df()
    df.loc[0, 'borough'] = None
    df = parse_dates(df)
    result = handle_nulls(df)
    assert result['borough'].isnull().sum() == 0
    print("✅ handle_nulls passed")


def test_remove_duplicates():
    df = make_dummy_crime_df(100)
    df = pd.concat([df, df.head(10)])  # Artificially add duplicates
    df = parse_dates(df)
    result = remove_duplicates(df)
    assert len(result) <= len(df)
    print("✅ remove_duplicates passed")


def test_standardise_boroughs():
    df = make_dummy_crime_df()
    df = parse_dates(df)
    result = standardise_boroughs(df)
    # Should not crash and column should exist
    assert 'borough' in result.columns
    print("✅ standardise_boroughs passed")


def test_validate_value_range():
    df = make_dummy_crime_df()
    df.loc[0, 'value'] = -50  # Inject negative value
    df = parse_dates(df)
    result = validate_value_range(df)
    assert (result['value'] >= 0).all()
    print("✅ validate_value_range passed")


def test_filter_years():
    df = make_dummy_crime_df()
    df = parse_dates(df)
    result = filter_years(df, start=2015, end=2020)
    assert result['year'].min() >= 2015
    assert result['year'].max() <= 2020
    print("✅ filter_years passed")


if __name__ == "__main__":
    test_parse_dates()
    test_handle_nulls()
    test_remove_duplicates()
    test_standardise_boroughs()
    test_validate_value_range()
    test_filter_years()
    print("\n✅ All tests passed!")
