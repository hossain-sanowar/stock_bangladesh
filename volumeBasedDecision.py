"""
3. Use Volume or Value (Optional Enhancements)
- If your original day_end_data.csv also has VOLUME or VALUE (mn), you can add:
- Sort by highest average volume or value traded
- Ensures you're choosing liquid stocks that are easier to enter/exit
"""
import pandas as pd
import os


folder_name = "data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# Load data with comprehensive cleaning
def clean_number(x):
    try:
        return float(str(x).replace(',', ''))
    except:
        return None
# Reload day_end_data to calculate average volume or value per symbol
raw_df = pd.read_csv(
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
)

# Calculate average volume and value per stock
liquidity_stats = raw_df.groupby('TRADING CODE',observed=False)[['VOLUME', 'VALUE (mn)']].mean().rename(columns={
    'VOLUME': 'avg_volume',
    'VALUE (mn)': 'avg_value'
}).reset_index()

# Load technical signals
signals_df = pd.read_csv("./data/technical_signals.csv")

# Merge signals with average liquidity stats
merged_df = signals_df.merge(
    liquidity_stats,
    how='left',
    left_on='symbol',
    right_on='TRADING CODE'
).drop(columns='TRADING CODE')

# Filter out entries with 0 or missing volume/value
merged_df = merged_df[(merged_df['avg_volume'] > 0) & (merged_df['avg_value'] > 0)]

# Only consider 'Buy' signals
buy_signals = merged_df[merged_df['signal'] == 'Buy']

# Sort by volume or value, take top 100
top_buys_by_volume = buy_signals.sort_values(by='avg_volume', ascending=False).head(100)
top_buys_by_value = buy_signals.sort_values(by='avg_value', ascending=False).head(100)

# Save both to a single Excel file with two sheets
with pd.ExcelWriter("./data/top_buys_liquidity.xlsx", engine='xlsxwriter') as writer:
    top_buys_by_volume.to_excel(writer, sheet_name='Top Volume Buys', index=False)
    top_buys_by_value.to_excel(writer, sheet_name='Top Value Buys', index=False)

print("Top Buy signals (non-zero volume/value) saved to 'top_buys_liquidity.xlsx'.")
