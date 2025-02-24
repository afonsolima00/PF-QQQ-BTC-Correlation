import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Define the date range for the past 12 months
end_date = datetime(2025, 2, 24)
start_date = end_date - timedelta(days=365)

# Replace with your actual Marketstack API key
MARKETSTACK_API_KEY = "e7c489ef2372fcec0667807ee8ef0061"

# Use Nasdaq Composite symbol without the caret (compatible with Marketstack)
NASDAQ_SYMBOL = "QQQ"

def fetch_nasdaq_data():
    """
    Fetch daily Nasdaq closing prices over the defined period using Marketstack API.
    """
    url = "http://api.marketstack.com/v1/eod"
    params = {
        "access_key": MARKETSTACK_API_KEY,
        "symbols": NASDAQ_SYMBOL,
        "date_from": start_date.strftime("%Y-%m-%d"),
        "date_to": end_date.strftime("%Y-%m-%d"),
        "limit": 500  # Ensures enough records are returned
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching Nasdaq data:", response.status_code)
        return None
    data = response.json().get("data", [])
    if not data:
        print("No Nasdaq data returned")
        return None
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)  # Remove timezone info
    df = df[['date', 'close']].sort_values('date')
    df.rename(columns={'close': 'nasdaq'}, inplace=True)
    return df

def fetch_bitcoin_data():
    """
    Fetch historical Bitcoin price data using the CoinGecko API.
    """
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
    params = {
        "vs_currency": "usd",
        "from": str(int(start_date.timestamp())),
        "to": str(int(end_date.timestamp()))
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching Bitcoin data:", response.status_code)
        return None
    data = response.json().get("prices", [])
    if not data:
        print("No Bitcoin data returned")
        return None
    df = pd.DataFrame(data, columns=['timestamp', 'bitcoin'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize(None)  # Remove timezone info
    # Resample to daily frequency in case of intraday entries
    df = df.set_index('date').resample('D').mean().reset_index()
    return df[['date', 'bitcoin']]

# Fetch datasets from both APIs
nasdaq_df = fetch_nasdaq_data()
bitcoin_df = fetch_bitcoin_data()

if nasdaq_df is None or bitcoin_df is None:
    print("Error fetching one or both datasets.")
else:
    # Merge the Nasdaq and Bitcoin datasets on the date
    merged_df = pd.merge(nasdaq_df, bitcoin_df, on='date', how='inner')
    merged_df.dropna(inplace=True)
    
    # Compute daily percentage returns for each asset
    merged_df['nasdaq_pct'] = merged_df['nasdaq'].pct_change() * 100
    merged_df['btc_pct'] = merged_df['bitcoin'].pct_change() * 100

    # Calculate the Pearson correlation coefficient between daily returns
    correlation = merged_df[['nasdaq_pct', 'btc_pct']].corr().iloc[0, 1]
    print("Correlation between Nasdaq and Bitcoin daily returns: {:.2f}".format(correlation))
    
    # Identify divergence days: significant percentage differences with moves in opposite directions.
    divergence_threshold = 2.0
    divergences = merged_df[
        (abs(merged_df['nasdaq_pct'] - merged_df['btc_pct']) > divergence_threshold) &
        (merged_df['nasdaq_pct'] * merged_df['btc_pct'] < 0)
    ]
    print("Number of divergence days:", len(divergences))
    
    # Visualization: create two plots for comparative analysis
    plt.figure(figsize=(14, 10))
    
    # Plot 1: Normalized Price Comparison
    plt.subplot(2, 1, 1)
    plt.plot(merged_df['date'], merged_df['nasdaq'] / merged_df['nasdaq'].iloc[0],
             label='Nasdaq', color='purple')
    plt.plot(merged_df['date'], merged_df['bitcoin'] / merged_df['bitcoin'].iloc[0],
             label='Bitcoin', color='teal')
    plt.title('Normalized Price Comparison over Last 12 Months')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.legend()
    
    # Plot 2: Daily Percentage Changes with Divergences Highlighted
    plt.subplot(2, 1, 2)
    plt.plot(merged_df['date'], merged_df['nasdaq_pct'], label='Nasdaq % Change', color='green')
    plt.plot(merged_df['date'], merged_df['btc_pct'], label='Bitcoin % Change', color='orange')
    plt.scatter(divergences['date'], divergences['nasdaq_pct'], color='red',
                label='Nasdaq divergence', zorder=5)
    plt.scatter(divergences['date'], divergences['btc_pct'], color='blue',
                label='Bitcoin divergence', zorder=5)
    plt.title('Daily Percentage Changes with Divergences')
    plt.xlabel('Date')
    plt.ylabel('Daily Return (%)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('comparison.png')
    plt.show()
    
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    
    try:
        # Store the merged dataset to a CSV file using absolute path
        csv_path = os.path.join(script_dir, 'nasdaq_bitcoin_data.csv')
        merged_df.to_csv(csv_path, index=False)
        print(f"Successfully saved CSV file to: {csv_path}")
    except Exception as e:
        print(f"Error saving CSV file: {str(e)}")
        print(f"Attempting to write with different encoding...")
        try:
            merged_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"Successfully saved CSV file with utf-8-sig encoding")
        except Exception as e2:
            print(f"Second attempt failed: {str(e2)}")
    
    try:
        # Write analysis results to a text file using absolute path
        txt_path = os.path.join(script_dir, 'analysis_results.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("Correlation between Nasdaq and Bitcoin daily returns: {:.2f}\n".format(correlation))
            f.write("Number of divergence days: {}\n".format(len(divergences)))
            f.write("\nDivergence details (first 5 rows):\n")
            f.write(divergences[['date', 'nasdaq_pct', 'btc_pct']].head().to_string())
        print(f"Successfully saved text file to: {txt_path}")
    except Exception as e:
        print(f"Error saving text file: {str(e)}")
        print(f"File path attempted: {txt_path}")
    
    print("Analysis complete. Data saved to 'nasdaq_bitcoin_data.csv', 'analysis_results.txt', and 'comparison.png'.")
