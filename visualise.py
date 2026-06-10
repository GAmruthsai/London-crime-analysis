"""
visualise.py
------------
Shared reusable plotting utilities used across EDA, trends, and socio-economic modules.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import os

SAVE_DIR = 'reports/figures'


def set_style():
    """Apply consistent visual style across all plots."""
    sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)
    plt.rcParams.update({
        'figure.dpi': 120,
        'axes.titleweight': 'bold',
        'axes.spines.top': False,
        'axes.spines.right': False,
    })


def save_figure(fig: plt.Figure, filename: str):
    """Save a figure to reports/figures/."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"[PLOT] Saved: {path}")


def format_thousands(ax, axis='y'):
    """Format axis tick labels with comma-separated thousands."""
    fmt = mticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
    if axis == 'y':
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)


def plot_value_counts(series: pd.Series, title: str, xlabel: str, filename: str,
                      color: str = 'steelblue', top_n: int = 15):
    """Generic horizontal bar chart for value counts."""
    counts = series.value_counts().head(top_n).sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind='barh', ax=ax, color=color, edgecolor='white')
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel(xlabel)
    format_thousands(ax, axis='x')
    save_figure(fig, filename)
