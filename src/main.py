import requests
import pandas as pd
from calculations import apply_calculations

API_URL = "https://banks.data.fdic.gov/api/financials"
SUMMARY_URL = "https://banks.data.fdic.gov/api/institutions"

bank_codes = [
    1105, 3832, 3973, 4239, 4832, 7230, 9087, 10248, 11971, 17266, 19772, 20504, 22858, 23091,
    24045, 26906, 28489, 29961, 30776, 30788, 32541, 35456, 35521, 35541, 57083, 57614, 57665,
    57833, 58228, 58291, 58458, 90196
]

selected_fields = [
    "REPDTE", "CERT", "ASSET", "LNLSGR", "SC", "CHBALI", "DEP", "BRO", "OTHBRF",
    "EQTOT", "LNRECONS", "LNREMULT", "LNCOMRE", "LNRENROT", "LNATRES", "RBCT1J",
    "NIMY", "NETINC", "PTAXNETINC", "IGLSEC", "SCHTMRES", "ELNATR", "NTLNLS",
    "P9ASSET", "NAASSET", "NCLNLSR", "ORE", "INTAN", "RBC1AAJ", "IDT1CER",
    "IDT1RWAJR", "RBCRWAJ", "EQCBHCTR", "ROA", "ROE", "EEFFR", "ITAX", "ITAXR"
]

def fetch_fdic_data(cert):
    params = {
        "filters": f"CERT:{cert}",
        "fields": ",".join(selected_fields),
        "sort_by": "REPDTE",
        "sort_order": "DESC",
        "limit": "10000",
        "offset": "0",
        "format": "json"
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching data for CERT {cert}: {response.status_code}")
        return []

def fetch_bank_name(cert):
    params = {
        "filters": f"CERT:{cert}",
        "fields": "NAME,CERT",
        "limit": "1",
        "format": "json"
    }
    response = requests.get(SUMMARY_URL, params=params)
    if response.status_code == 200:
        results = response.json().get("data", [])
        if results:
            return results[0]["data"]["NAME"]
    return f"Bank_{cert}"

def process_data(data):
    records = [entry["data"] for entry in data]
    df = pd.DataFrame(records)
    
    # Convert REPDTE to datetime and sort correctly
    df["REPDTE"] = pd.to_datetime(df["REPDTE"])
    df.sort_values("REPDTE", ascending=False, inplace=True)
    # Create a new column with formatted dates (e.g., "Dec 2024")
    df["REPDTE_formatted"] = df["REPDTE"].dt.strftime("%b %Y")
    df.drop("REPDTE", axis=1, inplace=True)
    df.rename(columns={"REPDTE_formatted": "REPDTE"}, inplace=True)
    
    df.set_index("REPDTE", inplace=True)
    df = df.transpose()
    df = apply_calculations(df)
    
    # Ensure earnings rows exist even if blank
    if "Annualized Earnings (Pre-Tax)" not in df.index:
        df.loc["Annualized Earnings (Pre-Tax)"] = ""
    if "Annualized Earnings (Tax Adjusted)" not in df.index:
        df.loc["Annualized Earnings (Tax Adjusted)"] = ""
    
    ordered_rows = [
        "Assets", "Loans", "Investment Securities", "Investments/Assets", "Deposits",
        "Loan-to-Deposit Ratio", "Brokered Deposits", "Brokered Deposits/Total Deposits",
        "Borrowings", "Borrowings/Assets", "GAAP Capital", "GAAP Capital/Assets",
        "Non-Owner Occupied Commercial Real Estate/Total Capital", "Net Interest Margin",
        "Net Income", "Efficiency Ratio", "Annualized Earnings (Pre-Tax)",
        "Annualized Earnings (Tax Adjusted)", "Return on Assets", "Return on Equity",
        "Allowance for Loan Losses", "CECL Adoption", "Allowance/Loans",
        "YTD Provision for Loan Losses", "YTD Net Charge-Offs (Recoveries)",
        "Annualized Losses/Loans", "90 Days Past Due & Nonaccrual Loans",
        "Non-Performing Loans Ratio", "Other Real Estate Owned",
        "(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)",
        "Tier 1 Leverage Ratio", "Common Equity Tier 1 Ratio",
        "Tier 1 Risk Based Ratio", "Total Risk Based Ratio",
        "Capital Contribution", "Ineligible Intangibles",
        "YTD Taxes Paid", "YTD Taxes Paid as a Percentage of Income"
    ]
    
    df = df[~df.index.duplicated(keep="first")]
    df = df.reindex([row for row in ordered_rows if row in df.index])
    
    # Insert gap rows after specified sections
    gap_after = [
        "Assets", "Borrowings/Assets", "Return on Equity",
        "(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)",
        "Total Risk Based Ratio", "Ineligible Intangibles"
    ]
    for row in reversed(gap_after):
        if row in df.index:
            idx = df.index.get_loc(row)
            top = df.iloc[:idx + 1]
            bottom = df.iloc[idx + 1:]
            gap = pd.DataFrame([["" for _ in df.columns]], index=[""], columns=df.columns)
            df = pd.concat([top, gap, bottom])
    
    return df

def run_all_to_excel(filename="fdic_combined.xlsx"):
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        for cert in bank_codes:
            print(f"Processing CERT {cert}...")
            data = fetch_fdic_data(cert)
            if data:
                bank_name = fetch_bank_name(cert)
                df = process_data(data)
                
                # Reset index so that the metrics become a column
                df_reset = df.reset_index()
                df_reset.columns.values[0] = "Metric"
                
                # Write data starting at row 5
                df_reset.to_excel(writer, sheet_name=bank_name[:31], startrow=4, index=False)
                
                # Get workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets[bank_name[:31]]
                
                # Write header rows
                worksheet.write("A1", bank_name)
                worksheet.write("A2", "(overview, amounts in $1000s)")
                worksheet.write("A3", f"FDIC CERT: {cert}")
                
    print(f"\n✅ Excel file saved to {filename}")

if __name__ == "__main__":
    run_all_to_excel()