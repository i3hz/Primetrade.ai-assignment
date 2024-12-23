import requests
import pandas as pd
import time
from datetime import datetime
import openpyxl
from openpyxl.styles import PatternFill, Font
import os

class CryptoAnalyzer:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.excel_file = "crypto_live_data.xlsx"
        
    def fetch_top_50_crypto(self):
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
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def process_data(self, data):
        """Process the raw API data into a pandas DataFrame"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
        df = df[[
            'name', 'symbol', 'current_price', 'market_cap',
            'total_volume', 'price_change_percentage_24h'
        ]]
        df.columns = [
            'Cryptocurrency Name', 'Symbol', 'Current Price (USD)',
            'Market Capitalization', '24h Trading Volume',
            'Price Change 24h (%)'
        ]
        return df

    def analyze_data(self, df):
        """Perform analysis on the cryptocurrency data"""
        if df is None or df.empty:
            return None
        
        analysis = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'top_5_by_market_cap': df.head(5)[['Cryptocurrency Name', 'Market Capitalization']].to_dict('records'),
            'average_price': df['Current Price (USD)'].mean(),
            'highest_24h_change': df.nlargest(1, 'Price Change 24h (%)')[['Cryptocurrency Name', 'Price Change 24h (%)']].to_dict('records')[0],
            'lowest_24h_change': df.nsmallest(1, 'Price Change 24h (%)')[['Cryptocurrency Name', 'Price Change 24h (%)']].to_dict('records')[0]
        }
        return analysis

    def update_excel(self, df, analysis):
        """Update Excel file with live data and analysis"""
        if df is None or analysis is None:
            return
        
        # Create Excel writer object
        with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='w') as writer:
            # Write main data
            df.to_excel(writer, sheet_name='Live Data', index=False)
            
            # Create analysis sheet
            analysis_df = pd.DataFrame([
                ['Analysis Timestamp', analysis['timestamp']],
                ['Average Price (USD)', f"${analysis['average_price']:.2f}"],
                ['Highest 24h Change', f"{analysis['highest_24h_change']['Cryptocurrency Name']}: {analysis['highest_24h_change']['Price Change 24h (%)']:.2f}%"],
                ['Lowest 24h Change', f"{analysis['lowest_24h_change']['Cryptocurrency Name']}: {analysis['lowest_24h_change']['Price Change 24h (%)']:.2f}%"]
            ])
            analysis_df.to_excel(writer, sheet_name='Analysis', index=False, header=False)
            
            # Create top 5 sheet
            top_5_df = pd.DataFrame(analysis['top_5_by_market_cap'])
            top_5_df.to_excel(writer, sheet_name='Top 5 by Market Cap', index=False)

    def run_live_update(self, update_interval=300):
        """Run continuous updates at specified interval (default 5 minutes)"""
        while True:
            print(f"\nFetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Fetch and process data
            raw_data = self.fetch_top_50_crypto()
            df = self.process_data(raw_data)
            
            if df is not None:
                # Perform analysis
                analysis = self.analyze_data(df)
                
                # Update Excel file
                self.update_excel(df, analysis)
                
                print("Data updated successfully!")
                print(f"Next update in {update_interval} seconds...")
                
                # Print some key statistics
                print("\nQuick Stats:")
                print(f"Top Cryptocurrency: {df.iloc[0]['Cryptocurrency Name']}")
                print(f"Average Price: ${analysis['average_price']:.2f}")
                print(f"Highest 24h Change: {analysis['highest_24h_change']['Cryptocurrency Name']} ({analysis['highest_24h_change']['Price Change 24h (%)']:.2f}%)")
            
            # Wait for next update
            time.sleep(update_interval)

if __name__ == "__main__":
    analyzer = CryptoAnalyzer()
    analyzer.run_live_update()