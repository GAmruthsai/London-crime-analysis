"""
socioeconomic.py
----------------
Correlates socio-economic indicators (deprivation, unemployment)
against borough crime rates.
Includes: Pearson correlation, scatter plots with regression lines,
ranked borough comparison, and OLS regression summary.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

SAVE_DIR = 'reports/figures'
sns.set_theme(style='whitegrid')


def _save(fig, filename: str):
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"[PLOT] Saved: {path}")


def merge_datasets(crime_df: pd.DataFrame, socio_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge annual crime totals with socio-economic indicators on borough + year.
    """
    annual_crime = crime_df.groupby(['borough', 'year'])['value'].sum().reset_index()
    annual_crime.rename(columns={'value': 'total_crimes'}, inplace=True)

    merged = pd.merge(annual_crime, socio_df, on=['borough', 'year'], how='inner')
    print(f"[MERGE] Merged dataset: {merged.shape[0]:,} rows across {merged['borough'].nunique()} boroughs")
    return merged


def correlation_analysis(merged_df: pd.DataFrame):
    """
    Compute and print Pearson correlations between crime and socio-economic variables.
    """
    print("\n" + "="*55)
    print("  Socio-Economic Correlation Analysis")
    print("="*55)

    indicators = [col for col in merged_df.columns
                  if col not in ['borough', 'year', 'total_crimes']]

    for col in indicators:
        valid = merged_df[['total_crimes', col]].dropna()
        r, p = stats.pearsonr(valid['total_crimes'], valid[col])
        sig = "✅ Significant" if p < 0.05 else "⚠️  Not significant"
        print(f"  {col:30s} r = {r:+.4f}  p = {p:.4f}  [{sig}]")


def plot_deprivation_vs_crime(merged_df: pd.DataFrame):
    """Scatter plot: deprivation score vs crime rate, coloured by borough."""
    if 'deprivation_score' not in merged_df.columns:
        print("[SKIP] deprivation_score column not found.")
        return

    annual = merged_df.groupby('borough').agg(
        total_crimes=('total_crimes', 'mean'),
        deprivation_score=('deprivation_score', 'mean')
    ).reset_index()

    r, p = stats.pearsonr(annual['deprivation_score'], annual['total_crimes'])

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(annual['deprivation_score'], annual['total_crimes'],
               s=60, alpha=0.7, color='steelblue', edgecolors='white')

    # Regression line
    m, b, _, _, _ = stats.linregress(annual['deprivation_score'], annual['total_crimes'])
    x_line = np.linspace(annual['deprivation_score'].min(), annual['deprivation_score'].max(), 100)
    ax.plot(x_line, m * x_line + b, color='crimson', linewidth=2,
            label=f'OLS fit (r = {r:.2f}, p = {p:.4f})')

    # Label notable boroughs
    for _, row in annual.iterrows():
        if row['total_crimes'] > annual['total_crimes'].quantile(0.85) or \
           row['deprivation_score'] > annual['deprivation_score'].quantile(0.85):
            ax.annotate(row['borough'], (row['deprivation_score'], row['total_crimes']),
                        fontsize=7, alpha=0.8,
                        xytext=(4, 4), textcoords='offset points')

    ax.set_title('Deprivation Score vs Average Annual Crime by Borough',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('IMD Deprivation Score (higher = more deprived)')
    ax.set_ylabel('Average Annual Crimes')
    ax.legend()
    _save(fig, 'deprivation_vs_crime.png')


def plot_unemployment_vs_crime(merged_df: pd.DataFrame):
    """Scatter plot: unemployment rate vs crime rate."""
    if 'unemployment_rate' not in merged_df.columns:
        print("[SKIP] unemployment_rate column not found.")
        return

    annual = merged_df.groupby('borough').agg(
        total_crimes=('total_crimes', 'mean'),
        unemployment_rate=('unemployment_rate', 'mean')
    ).reset_index()

    r, p = stats.pearsonr(annual['unemployment_rate'], annual['total_crimes'])

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(annual['unemployment_rate'], annual['total_crimes'],
               s=60, alpha=0.7, color='darkorange', edgecolors='white')

    m, b, _, _, _ = stats.linregress(annual['unemployment_rate'], annual['total_crimes'])
    x_line = np.linspace(annual['unemployment_rate'].min(), annual['unemployment_rate'].max(), 100)
    ax.plot(x_line, m * x_line + b, color='darkblue', linewidth=2,
            label=f'OLS fit (r = {r:.2f}, p = {p:.4f})')

    ax.set_title('Unemployment Rate vs Average Annual Crime by Borough',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Unemployment Rate (%)')
    ax.set_ylabel('Average Annual Crimes')
    ax.legend()
    _save(fig, 'unemployment_vs_crime.png')


def plot_crime_deprivation_ranked(merged_df: pd.DataFrame):
    """
    Side-by-side ranked bar chart comparing crime rank vs deprivation rank.
    """
    if 'deprivation_score' not in merged_df.columns:
        return

    annual = merged_df.groupby('borough').agg(
        total_crimes=('total_crimes', 'mean'),
        deprivation_score=('deprivation_score', 'mean')
    ).reset_index()

    annual['crime_rank']      = annual['total_crimes'].rank(ascending=False).astype(int)
    annual['deprivation_rank'] = annual['deprivation_score'].rank(ascending=False).astype(int)
    annual = annual.sort_values('crime_rank')

    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(annual))
    w = 0.35
    ax.bar(x - w/2, annual['crime_rank'],      width=w, label='Crime Rank',      color='steelblue', alpha=0.85)
    ax.bar(x + w/2, annual['deprivation_rank'], width=w, label='Deprivation Rank', color='coral',    alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(annual['borough'], rotation=45, ha='right', fontsize=8)
    ax.set_title('Borough Crime Rank vs Deprivation Rank', fontsize=13, fontweight='bold')
    ax.set_ylabel('Rank (1 = Highest)')
    ax.legend()
    plt.tight_layout()
    _save(fig, 'crime_vs_deprivation_ranked.png')


def run_socioeconomic_analysis(crime_df: pd.DataFrame, socio_df: pd.DataFrame):
    """Run full socio-economic analysis suite."""
    print("\n[SOCIO] Running socio-economic correlation analysis...")
    merged = merge_datasets(crime_df, socio_df)
    correlation_analysis(merged)
    plot_deprivation_vs_crime(merged)
    plot_unemployment_vs_crime(merged)
    plot_crime_deprivation_ranked(merged)
    print("[SOCIO] ✅ All socio-economic charts saved.")
    return merged
