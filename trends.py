"""
trends.py
---------
Time-series and seasonal trend analysis for London crime data.
Covers: monthly trends, seasonal decomposition, rolling averages,
month-of-year patterns, and YoY change analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import os

SAVE_DIR = 'reports/figures'
sns.set_theme(style='whitegrid')


def _save(fig, filename: str):
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"[PLOT] Saved: {path}")


def plot_monthly_trend(df: pd.DataFrame):
    """Line chart: total crimes per month across the full dataset."""
    monthly = df.groupby('year_month')['value'].sum().reset_index()
    monthly['year_month_dt'] = monthly['year_month'].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(monthly['year_month_dt'], monthly['value'], color='steelblue', linewidth=1.5)

    # Rolling 12-month average
    monthly['rolling_12'] = monthly['value'].rolling(12, center=True).mean()
    ax.plot(monthly['year_month_dt'], monthly['rolling_12'], color='red',
            linewidth=2, linestyle='--', label='12-month rolling avg')

    ax.set_title('Monthly Crime Trend — London 2013–2024', fontsize=13, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Crimes')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.legend()
    _save(fig, 'monthly_crime_trend.png')


def plot_seasonal_pattern(df: pd.DataFrame):
    """
    Box plot: crime distribution by month of year — reveals seasonality.
    """
    monthly_totals = df.groupby(['year', 'month'])['value'].sum().reset_index()
    month_labels = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec']

    fig, ax = plt.subplots(figsize=(13, 5))
    sns.boxplot(data=monthly_totals, x='month', y='value', ax=ax,
                palette='coolwarm', fliersize=3)
    ax.set_xticklabels(month_labels)
    ax.set_title('Seasonal Crime Pattern by Month (2013–2024)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Crimes')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    _save(fig, 'seasonal_pattern_boxplot.png')


def seasonal_decomposition(df: pd.DataFrame):
    """
    Statsmodels seasonal decomposition into trend, seasonal, residual components.
    """
    monthly = df.groupby('year_month')['value'].sum()
    monthly.index = monthly.index.to_timestamp()
    monthly = monthly.asfreq('MS')  # Monthly start frequency

    # Need at least 2 full cycles — check
    if len(monthly) < 24:
        print("[WARN] Not enough data for seasonal decomposition (need 24+ months).")
        return

    result = seasonal_decompose(monthly, model='additive', period=12)

    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    result.observed.plot(ax=axes[0], color='steelblue')
    axes[0].set_ylabel('Observed')
    result.trend.plot(ax=axes[1], color='orange')
    axes[1].set_ylabel('Trend')
    result.seasonal.plot(ax=axes[2], color='green')
    axes[2].set_ylabel('Seasonal')
    result.resid.plot(ax=axes[3], color='red', alpha=0.6)
    axes[3].set_ylabel('Residual')

    fig.suptitle('Seasonal Decomposition of London Crime (2013–2024)',
                 fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    _save(fig, 'seasonal_decomposition.png')


def plot_yoy_change(df: pd.DataFrame):
    """Bar chart: year-on-year % change in total crime."""
    yearly = df.groupby('year')['value'].sum()
    yoy = yearly.pct_change() * 100

    fig, ax = plt.subplots(figsize=(12, 5))
    colors = ['crimson' if v < 0 else 'seagreen' for v in yoy.values]
    ax.bar(yoy.index, yoy.values, color=colors, edgecolor='white', width=0.6)
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title('Year-on-Year % Change in Total Crime — London', fontsize=13, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('% Change')
    for i, (yr, val) in enumerate(yoy.items()):
        if not np.isnan(val):
            ax.text(yr, val + (0.3 if val >= 0 else -0.8),
                    f'{val:.1f}%', ha='center', fontsize=9)
    _save(fig, 'yoy_crime_change.png')


def run_trend_analysis(df: pd.DataFrame):
    """Run all trend analyses."""
    print("\n[TRENDS] Running trend analysis...")
    plot_monthly_trend(df)
    plot_seasonal_pattern(df)
    seasonal_decomposition(df)
    plot_yoy_change(df)
    print("[TRENDS] ✅ All trend charts saved.")
