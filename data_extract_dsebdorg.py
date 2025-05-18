"""
Data extract from Dsebd.org
- Always works with the current date.
- Automatically goes 3 months + 10 days back.
- Requires no manual date editing
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import os

folder_name = "data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# Step 1: Calculate Dates
end_date = datetime.today()
start_date = end_date - timedelta(days=100)  # approx. 3 months + 10 days

# Format dates for the URL (YYYY-MM-DD)
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# Step 2: Construct the URL
url = f"https://www.dsebd.org/day_end_archive.php?startDate={start_str}&endDate={end_str}&inst=All%20Instrument&archive=data"

# Step 3: Fetch HTML content
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # Ensure correct encoding

# Step 4: Parse with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Step 5: Locate the correct table and extract rows
table = soup.find("table", class_="shares-table")
thead = table.find("thead")
tbody = table.find("tbody")

if not table:
    raise ValueError("Could not find the data table on the page. Check the URL or structure.")

# Extract headers
columns = [th.get_text(strip=True) for th in thead.find_all("th")]

# Extract row data
rows = []
for tr in tbody.find_all("tr"):
    row = [td.get_text(strip=True) for td in tr.find_all("td")]
    if row:
        rows.append(row)

# Step 6: Create DataFrame
df = pd.DataFrame(rows, columns=columns)

# Step 7: Save to CSV and Excel
df.to_csv("./data/day_end_data.csv", index=False)
# df.to_excel("day_end_data.xlsx", index=False)

print(f"Data saved to 'day_end_data.csv' and 'day_end_data.xlsx' for range {start_str} to {end_str}")
