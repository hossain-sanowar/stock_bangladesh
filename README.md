# stock_bangladesh
✅ Step-by-Step: How to Get the API Request Info
🔧 1. Open Chrome and Go to:
📍 https://stocknow.com.bd/data-matrix

🔧 2. Press F12 to open Developer Tools
(Or right-click → Inspect)

🔧 3. Click the Network tab
🔧 4. Refresh the page (F5)
🔧 5. In the filter bar, click “XHR”
(This shows all AJAX/JSON data requests)
🔧 6. Look for a request that:
Returns a list of stocks

Has .json or /matrix, /data, etc. in the URL

🔧 7. Click on that request and go to:
📄 Headers tab → Copy the full Request URL

Copy the entire cURL (right-click the request → Copy → cURL) and send that
Example: [https://stocknow.com.bd/api/v1/data-matrix](https://stocknow.com.bd/api/v1/data-matrix)


# Heikin Ashi:
![image](https://github.com/user-attachments/assets/7abd4544-35b2-4237-bc06-3800deb0431b)
![image](https://github.com/user-attachments/assets/dc9e71bb-e52d-40cb-a435-7bb3f2f7d3c8)
![image](https://github.com/user-attachments/assets/80086f23-7f04-4a5d-9949-84c322f356ec)
![image](https://github.com/user-attachments/assets/f1075ced-f7d1-463a-a1db-8c3fb88d7cd9)

Absolutely! To automate the identification of buy/sell signals for all listed companies on the Dhaka Stock Exchange (DSE) using Heikin Ashi technical analysis, we can develop a Python-based solution that integrates data from your provided Excel file and the StockNow API.

🧠 Objective
Goal: Analyze all DSE-listed companies to determine:

Buy Signals: When both Weekly and Monthly Heikin Ashi candles indicate an uptrend.

Sell Signals: When Daily Heikin Ashi candles indicate a downtrend.

🔗 Data Sources
Company List: stocknow_data_matrix.xlsx (local Excel file).

Price Data: StockNow API – provides Heikin Ashi data for specified symbols and timeframes.

⚙️ Implementation Steps
Extract Company Symbols:

Read the Excel file to obtain a list of company symbols.

Fetch Heikin Ashi Data:

For each symbol, retrieve Daily, Weekly, and Monthly Heikin Ashi data from the API.

Analyze Trends:

Buy Signal: If both Weekly and Monthly candles are green with no lower shadows.

Sell Signal: If Daily candles are red with no upper shadows.

Compile Results:

Generate a report listing symbols with corresponding buy or sell signals.




