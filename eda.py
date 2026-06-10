"""
eda.py
------
Exploratory Data Analysis for London Crime Data.
Covers: crime type distributions, borough comparisons,
year-on-year totals, top categories.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

SAVE_DIR = 'reports/figures'
sns.set_theme(style='whitegrid', palette='muted')


def _save(fig, filename: str):
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"[PLOT] Saved: {path}")


def summary_stats(df: pd.DataFrame):
    """Print key summary statistics."""
    print("\n" + "="*55)
    print("  EDA Summary Statistics")
    print("="*55)
    print(f"  Total crime records  : {len(df):,}")
    print(f"  Years covered        : {df['year'].min()} – {df['year'].max()}")
    print(f"  Boroughs             : {df['borough'].nunique()}")
    print(f"  Crime categories     : {df['major_category'].nunique()}")
    print(f"\n  Top 5 Crime Types:\n{df.groupby('major_category')['value'].sum().sort_values(ascending=False).head()}")
    print(f"\n  Top 5 Boroughs by Crime:\n{df.groupby('borough')['value'].sum().sort_values(ascending=False).head()}")


def plot_crime_by_year(df: pd.DataFrame):
    """Bar chart: total crimes per year."""
    yearly = df.groupby('year')['value'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(yearly['year'], yearly['value'], color='steelblue', edgecolor='white', width=0.7)
    ax.bar_label(bars, fmt='%,.0f', fontsize=8, padding=3)
    ax.set_title('Total Reported Crimes in London (2013–2024)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Crimes')
    ax.set_xticks(yearly['year'])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    _save(fig, 'crimes_by_year.png')


def plot_crime_by_category(df: pd.DataFrame, top_n: int = 10):
    """Horizontal bar chart: top N crime categories."""
    cat_totals = df.groupby('major_category')['value'].sum().sort_values(ascending=True).tail(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_totals.plot(kind='barh', ax=ax, color='coral', edgecolor='white')
    ax.set_title(f'Top {top_n} Crime Categories — London 2013–2024', fontsize=13, fontweight='bold')
    ax.set_xlabel('Total Incidents')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    _save(fig, 'crimes_by_category.png')


def plot_borough_heatmap(df: pd.DataFrame):
    """Heatmap: crime count by borough × year."""
    pivot = df.pivot_table(index='borough', columns='year', values='value', aggfunc='sum')
    # Normalise each borough by its own mean for easier comparison
    pivot_norm = pivot.div(pivot.mean(axis=1), axis=0)

    fig, ax = plt.subplots(figsize=(16, 12))
    sns.heatmap(pivot_norm, ax=ax, cmap='YlOrRd', linewidths=0.3,
                cbar_kws={'label': 'Normalised Crime Index'})
    ax.set_title('Crime Intensity by Borough & Year (Normalised)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Borough')
    _save(fig, 'borough_year_heatmap.png')


def plot_top_boroughs(df: pd.DataFrame, top_n: int = 10):
    """Bar chart: top N boroughs by total crime."""
    borough_totals = df.groupby('borough')['value'].sum().sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(11, 5))
    borough_totals.plot(kind='bar', ax=ax, color='teal', edgecolor='white')
    ax.set_title(f'Top {top_n} Boroughs by Total Crime (2013–2024)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Total Crimes')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    _save(fig, 'top_boroughs.png')


def run_eda(df: pd.DataFrame):
    """Run full EDA suite."""
    summary_stats(df)
    plot_crime_by_year(df)
    plot_crime_by_category(df)
    plot_borough_heatmap(df)
    plot_top_boroughs(df)
    print("\n[EDA] ✅ All EDA charts saved to reports/figures/")
