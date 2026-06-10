"""
main.py
-------
Full pipeline for London Crime Data Analysis (2013–2024).

Stages:
  1. Load raw data
  2. Clean & validate
  3. EDA
  4. Trend analysis
  5. Socio-economic correlation analysis
  6. Export processed data

Run with:
    python main.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.load_data import load_crime_data, load_socioeconomic_data
from src.clean import clean_pipeline, save_processed
from src.eda import run_eda
from src.trends import run_trend_analysis
from src.socioeconomic import run_socioeconomic_analysis

CRIME_DATA_PATH = os.path.join('data', 'raw', 'london_crime.csv')
SOCIO_DATA_PATH = os.path.join('data', 'raw', 'socioeconomic.csv')


def check_data_exists():
    missing = []
    if not os.path.exists(CRIME_DATA_PATH):
        missing.append(CRIME_DATA_PATH)
    if not os.path.exists(SOCIO_DATA_PATH):
        missing.append(SOCIO_DATA_PATH)
    return missing


def main():
    print("=" * 60)
    print("  London Crime Data Analysis (2013–2024)")
    print("  MSc Data Analytics & Technology — Sheffield Hallam")
    print("=" * 60)

    # ── Check data files ───────────────────────────────────────
    missing = check_data_exists()
    if missing:
        print("\n[ERROR] Missing data files:")
        for f in missing:
            print(f"  ✗  {f}")
        print("\n  Please download the datasets and place them in data/raw/")
        print("  See README.md → Data Sources section for download links.")
        sys.exit(1)

    # ── Step 1: Load ───────────────────────────────────────────
    crime_df = load_crime_data(CRIME_DATA_PATH)
    socio_df = load_socioeconomic_data(SOCIO_DATA_PATH)

    # ── Step 2: Clean ──────────────────────────────────────────
    clean_df = clean_pipeline(crime_df)
    save_processed(clean_df, 'cleaned_crime_data.csv')

    # ── Step 3: EDA ────────────────────────────────────────────
    run_eda(clean_df)

    # ── Step 4: Trend Analysis ─────────────────────────────────
    run_trend_analysis(clean_df)

    # ── Step 5: Socio-economic Correlation ─────────────────────
    run_socioeconomic_analysis(clean_df, socio_df)

    print("\n" + "=" * 60)
    print("  ✅  Pipeline complete!")
    print("  📊  All charts saved in: reports/figures/")
    print("  💾  Cleaned data:        data/processed/")
    print("=" * 60)


if __name__ == "__main__":
    main()
