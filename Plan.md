### Step-by-Step Plan to Investigate and Compare Nasdaq and Bitcoin Price Movements Over the Last 12 Months

#### **1. Define the Task Scope**
- Compare Nasdaq and Bitcoin price movements over the past 12 months (Feb 2024–Feb 2025).
- Use a free API for both datasets to ensure accessibility and cost-effectiveness.
- Calculate correlations and identify divergences in price movements.

---

#### **2. Select APIs for Data Retrieval**
- **Nasdaq Data**: Use Marketstack API (free plan) to access historical stock market data, including Nasdaq prices[1][4].
- **Bitcoin Data**: Use CoinGecko API for historical Bitcoin price data, as it is free and requires no API key[2].

---

#### **3. Fetch Historical Data**
- Register for API keys or credentials where required (e.g., Marketstack).
- Retrieve daily closing prices for:
  - Nasdaq index.
  - Bitcoin (BTC-USD pair).
- Ensure data covers the same date range (last 12 months).

---

#### **4. Preprocess the Data**
- Convert both datasets into a standardized format (e.g., pandas DataFrame in Python).
- Ensure:
  - Dates are aligned.
  - Missing data points are handled (e.g., interpolate or drop missing values).

---

#### **5. Perform Analysis**
1. **Correlation Analysis**:
   - Calculate the Pearson correlation coefficient between Nasdaq and Bitcoin daily closing prices.
   - This will quantify the linear relationship between the two assets.

2. **Price Movements**:
   - Compute daily percentage changes for both assets to analyze volatility.
   - Identify significant divergences where one asset moves sharply while the other remains stable.

3. **Visualizations**:
   - Plot time series of both assets to observe trends.
   - Overlay percentage changes to highlight divergences.

---

#### **6. Summarize Findings**
- Write a concise report summarizing:
  - Correlation results.
  - Key divergences or patterns observed.
  - Implications for diversification strategies.

---

#### **7. Store Results for Future Reference**
- Save:
  - Cleaned datasets (e.g., CSV files).
  - Analysis results (e.g., correlation values, divergence points).
  - Visualizations (e.g., PNG or PDF format).
- Archive the summary report for easy access during trading decisions.
