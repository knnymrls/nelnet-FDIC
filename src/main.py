import requests
import pandas as pd

# FDIC API Endpoint
API_URL = "https://banks.data.fdic.gov/api/financials"

# Fields to be fetched from API
selected_fields = [
    "REPDTE", "ASSET", "LNLSGR", "SC", "CHBALI", "DEP", "BRO", "OTHBRF", "EQTOT",
    "NIMY", "NETINC", "PTAXNETINC", "IDT1CER", "RBCRWAJ"
]

# Parameters for fetching data (Modify CERT number as needed)
params = {
    "filters": "CERT:15545",
    "fields": ",".join(selected_fields),
    "sort_by": "REPDTE",
    "sort_order": "DESC",
    "limit": "10000",
    "offset": "0",
    "format": "json"
}

# Mapping of API field names to desired y-axis labels
y_axis_mapping = {
    "ASSET": "Assets",
    "LNLSGR": "Loans",
    "SC": "Investment securities",
    "CHBALI": "Unrealized gains(losses) on securities",
    "DEP": "Deposits",
    "BRO": "Brokered deposits",
    "OTHBRF": "Borrowings",
    "EQTOT": "GAAP capital",
    "NIMY": "Margin",
    "NETINC": "Net Income",
    "PTAXNETINC": "Annualized earnings - pre tax",
    "IDT1CER": "Common equity Tier 1",
    "RBCRWAJ": "Total risk based ratio"
}

# Define the desired row order for the y-axis
desired_order = [
    "Assets", "Loans", "Investment securities", "Unrealized gains(losses) on securities",
    "Deposits", "Brokered deposits", "Borrowings", "GAAP capital", "Margin",
    "Net Income", "Annualized earnings - pre tax", "Common equity Tier 1", "Total risk based ratio"
]

def fetch_fdic_data():
    """Fetches data from FDIC API."""
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print("Error fetching data:", response.status_code)
        return []

def process_data(data):
    """Processes FDIC API data into a structured DataFrame."""
    records = []
    for entry in data:
        row = entry["data"]
        records.append(row)
    
    df = pd.DataFrame(records)
    df["REPDTE"] = pd.to_datetime(df["REPDTE"])
    df.sort_values("REPDTE", ascending=False, inplace=True)  # Recent years first
    df.set_index("REPDTE", inplace=True)
    df = df.transpose()  # Flipping so years are on the x-axis
    
    # Rename index values based on mapping
    df = df.rename(index=y_axis_mapping)
    
    # Reorder rows based on desired order
    df = df.loc[df.index.intersection(desired_order)]
    df = df.reindex(desired_order)
    
    # Define percentage columns
    percentage_columns = ["Margin", "Total risk based ratio", "Common equity Tier 1"]
    
    # Format percentages to 2 decimal places
    for row in percentage_columns:
        if row in df.index:  # Ensuring we format the correct index values
            df.loc[row] = df.loc[row].astype(float).map("{:.2f}%".format)
    
    # Format other numeric columns as whole dollar amounts
    for row in df.index:
        if row not in percentage_columns:
            df.loc[row] = df.loc[row].astype(float).map("${:,.0f}".format)
    
    return df

def save_to_csv(df, filename="fdic_data.csv"):
    """Saves the DataFrame to a CSV file."""
    df.to_csv(filename)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    data = fetch_fdic_data()
    if data:
        df = process_data(data)
        save_to_csv(df)
