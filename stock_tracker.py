import requests
import pandas as pd
from plyer import notification  


print('Environment is ready! Libraries are working.')

# Your Alpha Vantage API key
API_KEY = "CS4AFRBGDD8Q39C1"

# URL for fetching stock data
BASE_URL = "https://www.alphavantage.co/query"

sector_etfs = {
    "Technology": "XLK",
    "Energy": "XLE",
    "Financials": "XLF",
    "Healthcare": "XLV",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Materials": "XLB",
    "Industrials": "XLI"
}

def fetch_etf_performance(etfs):
    etf_performance = {}
    for sector, etf in etfs.items():
        print(f"Fetching data for ETF: {etf}")
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": etf,
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            # Extract percentage change from the API response
            global_quote = data.get("Global Quote", {})
            percent_change = global_quote.get("10. change percent", None)
            if percent_change:
                etf_performance[sector] = float(percent_change.strip('%'))
            else:
                print(f"No percent change data for {etf}")
        else:
            print(f"Error fetching data for {etf}: {response.status_code}")
    return etf_performance

if __name__ == "__main__":
    sector_etfs = {
    "Technology": "XLK",
    "Energy": "XLE",
    "Financials": "XLF",
    "Healthcare": "XLV",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Materials": "XLB",
    "Industrials": "XLI"
    }

    sector_performance = fetch_etf_performance(sector_etfs)
    print("Sectoral Performance (Percent Change):")
    for sector, performance in sorted(sector_performance.items(), key=lambda x: x[1], reverse=True):
        print(f"{sector}: {performance:.2f}%")


def fetch_historical_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "full"  # 'compact' for last 100 days; 'full' for all available data
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("Time Series (Daily)", {})
    else:
        print(f"Error fetching historical data for {symbol}: {response.status_code}")
        return {}
    

def show_notification(data):
    # Format the top-performing sectors
    message = "\n".join([f"{sector}: {performance:.2f}%" for sector, performance in data[:5]])  # Top 5 sectors
    
    # Display the notification
    notification.notify(
        title="Daily Sector Performance Report",
        message=message,
        app_name="Sector Tracker",
        timeout=10  # Duration in seconds
    )

if __name__ == "__main__":
    # Fetch sector performance
    sector_performance = fetch_etf_performance(sector_etfs)

    # Sort the performance data
    sorted_performance = sorted(sector_performance.items(), key=lambda x: x[1], reverse=True)

    # Show the notification with the top 5 sectors
    show_notification(sorted_performance)

    # (Optional) Print all sector performances
    print("Sectoral Performance (Percent Change):")
for sector, performance in sorted_performance:
        print(f"{sector}: {performance:.2f}%")


