"""
✅ Refined Strategy to Prioritize Investments
1. Strong Buy Filter
- Keep only stocks where:
- All 3 timeframes (daily, weekly, monthly) show "Up"
- These represent consistent upward momentum

2. Moderate Buy Opportunities
- Another group you might consider includes:
- Weekly and monthly are "Up" (strong long-term trend)
- daily is "Hold" (short-term pullback or consolidation)


4. Final Ranked List
You can now sort final selections by:
- Sector preference
- Fundamental alignment
- Historical support/resistance
"""

import pandas as pd
import os


folder_name = "data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# Load your CSV
df = pd.read_csv("./data/technical_signals.csv")

# Strong Buy list
strong_buys = df[
    (df['daily'] == 'Up') &
    (df['weekly'] == 'Up') &
    (df['monthly'] == 'Up')
]

# Moderate Buy list (buy the dip)
buy_dips = df[
    (df['weekly'] == 'Up') &
    (df['monthly'] == 'Up') &
    (df['daily'] != 'Down')
]

# Save both to a single Excel file with two sheets
with pd.ExcelWriter("./data/filtered_buys.xlsx", engine='xlsxwriter') as writer:
    strong_buys.to_excel(writer, sheet_name='Strong Buys', index=False)
    buy_dips.to_excel(writer, sheet_name='Buy the Dip', index=False)

print("Filtered signals saved to 'filtered_buys.xlsx'.")
