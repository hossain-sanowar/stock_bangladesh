"""
Heikin Ashi Analysis for Daily, Weekly and Monthly
Buying, Selling and Holding decision

"""

import pandas as pd
from time import sleep
import os


folder_name = "data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# --- Helper to clean number fields ---
def clean_number(x):
    try:
        return float(str(x).replace(',', ''))
    except:
        return None

# --- Heikin Ashi Calculation ---
def calculate_heikin_ashi(df):
    if df.empty or df.isnull().all().any():
        return pd.DataFrame(columns=['ha_open', 'ha_close', 'ha_high', 'ha_low'])

    ha_close = (df['OPENP*'] + df['HIGH'] + df['LOW'] + df['CLOSEP*']) / 4
    ha_open = [(df['OPENP*'].iloc[0] + df['CLOSEP*'].iloc[0]) / 2]
    for i in range(1, len(df)):
        ha_open.append((ha_open[i-1] + ha_close.iloc[i-1]) / 2)

    ha_high = pd.concat([df['HIGH'], pd.Series(ha_open, index=df.index), ha_close], axis=1).max(axis=1)
    ha_low = pd.concat([df['LOW'], pd.Series(ha_open, index=df.index), ha_close], axis=1).min(axis=1)

    return pd.DataFrame({
        'ha_open': ha_open,
        'ha_close': ha_close,
        'ha_high': ha_high,
        'ha_low': ha_low
    }, index=df.index)

# --- Detect trend based on last 3 Heikin Ashi candles ---
def detect_trend(ha_df):
    if ha_df.empty or len(ha_df) < 3:
        return "Hold"
    df = ha_df.tail(3)
    up = all(df['ha_close'].iloc[i] > df['ha_open'].iloc[i] for i in range(len(df)))
    down = all(df['ha_close'].iloc[i] < df['ha_open'].iloc[i] for i in range(len(df)))
    if up:
        return "Up"
    elif down:
        return "Down"
    return "Hold"

# --- Load local dataset ---
df = pd.read_csv(
    "./data/day_end_data.csv",
    parse_dates=['DATE'],
    dtype={'TRADING CODE': 'category'},
    converters={
        'OPENP*': clean_number,
        'CLOSEP*': clean_number,
        'HIGH': clean_number,
        'LOW': clean_number,
        'VALUE (mn)': clean_number,
        'VOLUME': lambda x: int(str(x).replace(',', '')) if x else 0
    }
).dropna().sort_values('DATE')

df.set_index('DATE', inplace=True)

results = []

# --- Loop through each symbol ---
for code, group in df.groupby('TRADING CODE', observed=False):
    print(f"Analyzing {code}...")

    group = group.sort_index()
    if group.empty or group[['OPENP*', 'CLOSEP*']].isnull().any().any():
        continue

    # Daily
    daily = group.copy()
    ha_daily = calculate_heikin_ashi(daily)

    # Weekly
    weekly = group.resample('W').agg({
        'OPENP*': 'first', 'HIGH': 'max', 'LOW': 'min', 'CLOSEP*': 'last'
    }).dropna()
    ha_weekly = calculate_heikin_ashi(weekly)

    # Monthly
    monthly = group.resample('ME').agg({
        'OPENP*': 'first', 'HIGH': 'max', 'LOW': 'min', 'CLOSEP*': 'last'
    }).dropna()
    ha_monthly = calculate_heikin_ashi(monthly)

    # Detect trends
    trend_d = detect_trend(ha_daily)
    trend_w = detect_trend(ha_weekly)
    trend_m = detect_trend(ha_monthly)

    # Combined signal logic
    if (trend_w == "Up" and trend_m == "Up") or (trend_d == "Up"):
        signal = "Buy"
    elif trend_d == "Down":
        signal = "Sell"
    else:
        signal = "Hold"

    results.append({
        "symbol": code,
        "daily": trend_d,
        "weekly": trend_w,
        "monthly": trend_m,
        "signal": signal
    })

    sleep(0.1)

# --- Save results ---
results_df = pd.DataFrame(results)
results_df.to_csv("./data/technical_signals.csv", index=False)
print("Analysis complete. Results saved to technical_signals.csv")
