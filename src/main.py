# **Bank Name: First National Bank of Omaha**
# Bank Code: 15545

import requests
import pandas as pd
from calculations import apply_calculations  # Import calculations from external file

# FDIC API Endpoint
API_URL = "https://banks.data.fdic.gov/api/financials"

# Fields to be fetched from API
selected_fields = [
    "REPDTE", "CERT", "ASSET", "LNLSGR", "SC", "CHBALI", "DEP", "BRO", "OTHBRF",
    "EQTOT", "LNRECONS", "LNREMULT", "LNCOMRE", "LNRENROT", "LNATRES", "RBCT1J",
    "NIMY", "NETINC", "PTAXNETINC", "IGLSEC", "SCHTMRES", "ELNATR", "NTLNLS",
    "P9ASSET", "NAASSET", "NCLNLSR", "ORE", "INTAN", "RBC1AAJ", "IDT1CER",
    "IDT1RWAJR", "RBCRWAJ", "EQCBHCTR"
]

# API Query Parameters
params = {
    "filters": "CERT:15545",
    "fields": ",".join(selected_fields),
    "sort_by": "REPDTE",
    "sort_order": "DESC",
    "limit": "10000",
    "offset": "0",
    "format": "json"
}

def fetch_fdic_data():
    """Fetches FDIC data from API and returns it as a list of dictionaries."""
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def process_data(data):
    """Processes API data, applies calculations from calculations.py, and returns a DataFrame."""
    records = [entry["data"] for entry in data]

    # Convert JSON response to DataFrame
    df = pd.DataFrame(records)
    
    # Convert REPDTE to datetime and sort by date
    df["REPDTE"] = pd.to_datetime(df["REPDTE"])
    df.sort_values("REPDTE", ascending=False, inplace=True)
    df.set_index("REPDTE", inplace=True)

    # Transpose so reporting dates are columns, and each row is a metric
    df = df.transpose()

    # Apply calculations from external file
    df = apply_calculations(df)

    return df

def save_to_csv(df, filename="fdic_data.csv"):
    """Saves the DataFrame to a CSV file with bank metadata at the top and a spacer row."""
    with open(filename, "w") as f:
        f.write("Bank Name:,First National Bank of Omaha\n")
        f.write("Bank Code:,15545\n")
        f.write("\n")  # Empty line for spacing
        df.to_csv(f)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    data = fetch_fdic_data()
    if data:
        df = process_data(data)
        save_to_csv(df)
