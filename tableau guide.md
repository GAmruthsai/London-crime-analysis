# 📊 Tableau Dashboard Setup Guide

## London Crime Data Analysis (2013–2024)

-----

## Overview

This guide walks you through building the 4-dashboard Tableau workbook for this project.
The processed CSV output from the Python pipeline (`data/processed/cleaned_crime_data.csv`) is the primary data source.

-----

## Step 1 — Connect Your Data

1. Open **Tableau Desktop** or **Tableau Public** (free)
1. Click **Connect → Text File** → select `data/processed/cleaned_crime_data.csv`
1. Also connect `data/raw/socioeconomic.csv` as a second data source
1. In Data Source tab — verify data types:
- `date` → Date
- `year`, `month`, `value` → Number (Integer)
- `borough`, `major_category`, `minor_category` → String

-----

## Dashboard 1 — KPI Overview

**What it shows:** High-level crime summary with year filter

**Sheets to create:**

1. **Total Crimes (Big Number)** — SUM(Value) as a KPI card
1. **YoY Change %** — Table calc: (SUM(Value) - LOOKUP(SUM(Value),-1)) / LOOKUP(SUM(Value),-1)
1. **Top 3 Crime Types** — Bar chart: Major Category vs SUM(Value), top 3 filter
1. **Top 3 Boroughs** — Bar chart: Borough vs SUM(Value), top 3 filter

**Layout:** Horizontal container with 4 tiles across the top, trend line below

-----

## Dashboard 2 — Crime Hotspot Map

**What it shows:** Borough-level choropleth of crime intensity

**Steps:**

1. Create new sheet → drag `Borough` to Detail
1. Click **Show Me → Filled Map** (Tableau will auto-geocode London boroughs)
1. Drag `SUM(Value)` to **Colour**
1. Colour palette: Orange-Red (sequential, high = red)
1. Add **Year** as a filter (show as slider)
1. Add **Major Category** as a filter (dropdown)
1. Add tooltip: Borough name, Total crimes, YoY change

**Tip:** If boroughs don’t geocode correctly, manually assign geographic roles or use a custom shapefile from the London Datastore.

-----

## Dashboard 3 — Trend Analysis

**What it shows:** Time-series of monthly crime with seasonal overlays

**Sheets to create:**

1. **Monthly Trend Line** — DATETRUNC(‘month’, Date) on Columns, SUM(Value) on Rows
- Add reference line: 12-month moving average using Table Calc → Moving Average, 12
1. **Seasonal Box Plot** — MONTH(Date) on Columns, SUM(Value) on Rows → change to Box Plot
1. **Crime Type Stacked Area** — MONTH(Date) + YEAR(Date) on Columns, SUM(Value) on Rows, Major Category on Colour → Area mark

**Filters:** Year range slider, Borough multiselect

-----

## Dashboard 4 — Socio-Economic Analysis

**What it shows:** Correlation between deprivation/unemployment and crime rates

**Blend the two data sources:**

1. Go to Data → Edit Relationships → link on `Borough` + `Year`

**Sheets to create:**

1. **Deprivation vs Crime Scatter** — Deprivation Score on Columns, AVG(Total Crimes) on Rows, Borough on Detail
- Add trend line: Linear, show R²
1. **Unemployment vs Crime Scatter** — same structure with Unemployment Rate
1. **Borough Comparison Table** — Borough, Avg Crime, Deprivation Score, Unemployment Rate as a highlight table

-----

## Publishing to Tableau Public

1. File → **Save to Tableau Public**
1. Sign in / create free account at public.tableau.com
1. Your dashboard will get a public URL — paste this into your README and LinkedIn!

-----

## Tips

- Always use **Extract** (not Live connection) when working with CSVs for better performance
- Use **Device Layouts** (Dashboard → Device Layouts) to make it mobile-friendly
- Add **Dashboard Actions** (filter actions between sheets) for interactivity