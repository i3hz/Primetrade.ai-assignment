import requests
import pandas as pd
import time
from datetime import datetime
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class CryptoDataHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Get the latest data from the shared data store
        data = self.server.crypto_data
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

class CryptoTracker:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.latest_data = None
        self.server = None
        self.server_thread = None
        self.update_count = 0
        
    def fetch_crypto_data(self):
        """Fetch top 50 cryptocurrencies data from CoinGecko API"""
        endpoint = f"{self.base_url}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 50,
            'page': 1,
            'sparkline': False
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            processed_data = []
            for coin in data:
                processed_data.append({
                    'Cryptocurrency Name': coin['name'],
                    'Symbol': coin['symbol'].upper(),
                    'Current Price (USD)': coin['current_price'],
                    'Market Capitalization': coin['market_cap'],
                    '24h Trading Volume': coin['total_volume'],
                    'Price Change 24h (%)': round(coin['price_change_percentage_24h'], 2)
                })
            
            return processed_data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def start_server(self, port=8000):
        """Start the HTTP server"""
        server_address = ('', port)
        self.server = HTTPServer(server_address, CryptoDataHandler)
        self.server.crypto_data = {'data': [], 'timestamp': '', 'update_count': 0}
        
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"\nServer started at http://localhost:{port}")
        print("You can now open the HTML file in your browser to see live updates")

    def create_excel_template(self):
        """Create Excel template with web query"""
        excel_content = '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=windows-1252">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .update-info { 
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .price-up { color: green; }
        .price-down { color: red; }
    </style>
</head>
<body>
    <div class="update-info">
        <h2>Cryptocurrency Live Data</h2>
        <p>Last Updated: <span id="timestamp">Loading...</span></p>
        <p>Updates Completed: <span id="updateCount">0</span></p>
    </div>
    <table id="cryptoTable">
        <thead>
            <tr>
                <th>Cryptocurrency Name</th>
                <th>Symbol</th>
                <th>Current Price (USD)</th>
                <th>Market Capitalization</th>
                <th>24h Trading Volume</th>
                <th>Price Change 24h (%)</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
    let previousPrices = {};

    function formatNumber(num) {
        return num.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    function updateData() {
        fetch('http://localhost:8000')
            .then(response => response.json())
            .then(data => {
                document.getElementById('timestamp').textContent = data.timestamp;
                document.getElementById('updateCount').textContent = data.update_count;
                
                const tbody = document.querySelector('#cryptoTable tbody');
                tbody.innerHTML = '';
                
                data.data.forEach(coin => {
                    const row = document.createElement('tr');
                    
                    // Add cells for each property
                    const nameCell = document.createElement('td');
                    nameCell.textContent = coin['Cryptocurrency Name'];
                    row.appendChild(nameCell);
                    
                    const symbolCell = document.createElement('td');
                    symbolCell.textContent = coin['Symbol'];
                    row.appendChild(symbolCell);
                    
                    const priceCell = document.createElement('td');
                    const currentPrice = coin['Current Price (USD)'];
                    const previousPrice = previousPrices[coin['Symbol']];
                    priceCell.textContent = '$' + formatNumber(currentPrice);
                    
                    if (previousPrice) {
                        if (currentPrice > previousPrice) {
                            priceCell.className = 'price-up';
                        } else if (currentPrice < previousPrice) {
                            priceCell.className = 'price-down';
                        }
                    }
                    row.appendChild(priceCell);
                    
                    const marketCapCell = document.createElement('td');
                    marketCapCell.textContent = '$' + formatNumber(coin['Market Capitalization']);
                    row.appendChild(marketCapCell);
                    
                    const volumeCell = document.createElement('td');
                    volumeCell.textContent = '$' + formatNumber(coin['24h Trading Volume']);
                    row.appendChild(volumeCell);
                    
                    const changeCell = document.createElement('td');
                    const change = coin['Price Change 24h (%)'];
                    changeCell.textContent = formatNumber(change) + '%';
                    changeCell.className = change >= 0 ? 'price-up' : 'price-down';
                    row.appendChild(changeCell);
                    
                    tbody.appendChild(row);
                    
                    // Store current price for next update comparison
                    previousPrices[coin['Symbol']] = currentPrice;
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById('timestamp').textContent = 'Error updating data';
            });
    }

    // Update immediately and then every 5 seconds
    updateData();
    setInterval(updateData, 5000);
    </script>
</body>
</html>
'''
        # Save the HTML template
        with open('crypto_live_data.html', 'w') as f:
            f.write(excel_content)
        
        print("\nSetup Instructions:")
        print("1. The script has created 'crypto_live_data.html'")
        print("2. Open this file in your web browser to see live updates")
        print("3. For Excel integration:")
        print("   - Open Excel")
        print("   - Go to Data -> Get Data -> From Web")
        print("   - Enter URL: http://localhost:8000")
        print("   - Set refresh rate in Data -> Properties")

    def run(self):
        """Run the live crypto tracker"""
        self.start_server()
        self.create_excel_template()
        
        print("\nStarting live updates...")
        print("Press Ctrl+C to stop the server")
        
        while True:
            try:
                data = self.fetch_crypto_data()
                if data:
                    self.update_count += 1
                    self.server.crypto_data = {
                        'data': data,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'update_count': self.update_count
                    }
                    print(f"\rUpdate #{self.update_count} completed at {self.server.crypto_data['timestamp']}", end='', flush=True)
                
                # Wait before next update (30 seconds)
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n\nStopping server...")
                self.server.shutdown()
                break
            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(30)

if __name__ == "__main__":
    tracker = CryptoTracker()
    tracker.run()