import pandas as pd

# List of popular stocks and their tickers
stocks = [
    ("Microsoft", "MSFT"),
    ("Apple", "AAPL"),
    ("NVIDIA", "NVDA"),
    ("Alphabet (Class C)", "GOOG"),
    ("Alphabet (Class A)", "GOOGL"),
    ("Amazon", "AMZN"),
    ("Meta Platforms", "META"),
    ("Berkshire Hathaway (Class A)", "BRK/A"),
    ("Berkshire Hathaway (Class B)", "BRK/B"),
    ("Broadcom", "AVGO"),
    ("Taiwan Semiconductor", "TSM"),
    ("Tesla", "TSLA"),
    ("Walmart", "WMT"),
    ("Eli Lilly", "LLY"),
    ("JPMorgan Chase", "JPM"),
    ("Visa", "V"),
    ("Mastercard", "MA"),
    ("Netflix", "NFLX"),
    ("Costco", "COST"),
    ("ExxonMobil", "XOM"),
    ("Oracle", "ORCL"),
    ("Johnson & Johnson", "JNJ"),
    ("Procter & Gamble", "PG"),
    ("SAP", "SAP"),
    ("UnitedHealth", "UNH"),
    ("Home Depot", "HD"),
    ("AbbVie", "ABBV"),
    ("Bank of America", "BAC"),
    ("Novo Nordisk", "NVO"),
    ("Coca-Cola", "KO"),
    ("Alibaba", "BABA"),
    ("Palantir", "PLTR"),
    ("T-Mobile US", "TMUS"),
    ("Sumitomo Mitsui", "SMFG"),
    ("Philip Morris", "PM"),
    ("ASML Holding", "ASML"),
    ("Salesforce", "CRM"),
    ("Toyota", "TM"),
    ("Wells Fargo", "WFC"),
    ("Chevron", "CVX"),
    ("Cisco", "CSCO"),
    ("Comcast Holdings ZONES", "CCZ"),
    ("IBM", "IBM"),
    ("Abbott", "ABT"),
    ("McDonald’s", "MCD"),
    ("AstraZeneca", "AZN"),
    ("Novartis", "NVS"),
    ("GE Aerospace", "GE"),
    ("Linde", "LIN"),
    ("Merck & Co.", "MRK")
]

# Create DataFrame
df = pd.DataFrame(stocks, columns=["Company", "Ticker"])

# Save to CSV
csv_path = "popular_nasdaq_stocks.csv"
df.to_csv(csv_path, index=False)

csv_path
