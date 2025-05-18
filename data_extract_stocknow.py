""" Data extracted from https://stocknow.com.bd/ for fundamental analysis
- using fundamental tool
"""

import requests
import pandas as pd
import os


folder_name = "data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

url = "https://stocknow.com.bd/api/v1/data-matrix"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://stocknow.com.bd/data-matrix"
}

response = requests.get(url, headers=headers)
response.raise_for_status()
df = pd.DataFrame(response.json())
df.to_excel("./data/stocknow_data_matrix.xlsx", index=False)

print("Saved to 'stocknow_data_matrix.xlsx'")
