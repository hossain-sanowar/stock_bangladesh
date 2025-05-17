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
