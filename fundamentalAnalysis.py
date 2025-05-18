# # Current App for Stock Selection (Fundamental)

# """The dataset contains detailed financial and structural information about various stocks, including identifiers, 
# company names, ownership breakdown, and key financial metrics like reserves, loans, and price circuit limits.

# 1. To identify potentially good investment opportunities, I'll apply common investment criteria such as:
# 2. Positive financial health: Healthy reserves, low debt.
# 3. Ownership structure: High institutional or director ownership often indicates confidence.
# 4. Active trading status: Only consider active stocks.
# 5. Circuit data: Stocks not stuck at their circuit limits may indicate healthy volatility."""

# """How to Use:
# 1. Save this script as app.py.
# 2. Install Streamlit if you haven't: pip install streamlit
# 3. Run it: streamlit run app.py
# 4. Upload your Excel file through the web interface.
# streamlit run fundamentalAnalysis.py

# """


# # app.py
# import streamlit as st
# import pandas as pd

# st.title("Stock Investment Advisor")

# uploaded_file = st.file_uploader("Upload your stock Excel file", type=["xlsx"])

# if uploaded_file:
#     # Load the Excel file
#     excel_data = pd.ExcelFile(uploaded_file)
#     sheet = excel_data.sheet_names[0]
#     df = excel_data.parse(sheet)

#     # Filter active stocks
#     df = df[df['active'] == 1].copy()

#     # Prepare numeric columns
#     df["net_reserve"] = pd.to_numeric(df["reserve_and_surp"], errors='coerce')
#     df["total_loans"] = pd.to_numeric(df["short_term_loan"], errors='coerce') + \
#                         pd.to_numeric(df["long_term_loan"], errors='coerce')
#     df["ownership_strength"] = df["institute"] + df["director"]

#     # Drop incomplete rows
#     df = df.dropna(subset=["net_reserve", "total_loans", "ownership_strength"])

#     # Calculate investment score
#     df["score"] = (
#         df["net_reserve"].rank(ascending=False) +
#         df["total_loans"].rank(ascending=True) +
#         df["ownership_strength"].rank(ascending=False)
#     )

#     # Select top stocks
#     top_stocks = df.sort_values("score").head(10)[
#         ["code", "name", "net_reserve", "total_loans", "ownership_strength", "score"]
#     ]

#     st.success("Top recommended stocks for investment:")
#     st.dataframe(top_stocks)
# else:
#     st.info("Please upload an Excel file to continue.")

import pandas as pd
import os

folder_name = "data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# === Configuration ===
input_file = "./data/stocknow_data_matrix.xlsx"  # Replace with your actual file
output_folder = "data"
output_file = os.path.join(output_folder, "top_fundamental_stocks.xlsx")

# === Ensure Output Folder Exists ===
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# === Load Excel File ===
excel_data = pd.ExcelFile(input_file)
sheet = excel_data.sheet_names[0]
df = excel_data.parse(sheet)

# === Filter: Active stocks only ===
df = df[df['active'] == 1].copy()

# === Prepare Numeric Columns ===
df["net_reserve"] = pd.to_numeric(df["reserve_and_surp"], errors='coerce')
df["total_loans"] = pd.to_numeric(df["short_term_loan"], errors='coerce') + \
                    pd.to_numeric(df["long_term_loan"], errors='coerce')
df["ownership_strength"] = df["institute"] + df["director"]

# === Drop Incomplete Rows ===
df = df.dropna(subset=["net_reserve", "total_loans", "ownership_strength"])

# === Calculate Score ===
df["score"] = (
    df["net_reserve"].rank(ascending=False) +
    df["total_loans"].rank(ascending=True) +
    df["ownership_strength"].rank(ascending=False)
)

# === Select Top Stocks ===
top_stocks = df.sort_values("score").head(10)[
    ["code", "name", "net_reserve", "total_loans", "ownership_strength", "score"]
]

# === Save to Excel ===
top_stocks.to_excel(output_file, index=False)
# print(f"✅ Top recommended stocks saved to: {output_file}")
print(f"Top recommended stocks saved to: {output_file}")

