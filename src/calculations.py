import pandas as pd

def apply_calculations(df):
    df = df.apply(pd.to_numeric, errors='coerce')

    try: df.loc["Assets"] = df.loc["ASSET"]
    except: df.loc["Assets"] = None

    try: df.loc["Loans"] = df.loc["LNLSGR"]
    except: df.loc["Loans"] = None

    try: df.loc["Investment Securities"] = df.loc["SC"] + df.loc["CHBALI"]
    except: df.loc["Investment Securities"] = None

    try: df.loc["Investments/Assets"] = round((df.loc["SC"] + df.loc["CHBALI"]) / df.loc["ASSET"] * 100, 2)
    except: df.loc["Investments/Assets"] = None

    try: df.loc["Deposits"] = df.loc["DEP"]
    except: df.loc["Deposits"] = None

    try: df.loc["Loan-to-Deposit Ratio"] = round(df.loc["LNLSGR"] / df.loc["DEP"] * 100, 2)
    except: df.loc["Loan-to-Deposit Ratio"] = None

    try: df.loc["Brokered Deposits"] = df.loc["BRO"]
    except: df.loc["Brokered Deposits"] = None

    try: df.loc["Brokered Deposits/Total Deposits"] = round(df.loc["BRO"] / df.loc["DEP"] * 100, 2)
    except: df.loc["Brokered Deposits/Total Deposits"] = None

    try: df.loc["Borrowings"] = df.loc["OTHBRF"]
    except: df.loc["Borrowings"] = None

    try: df.loc["Borrowings/Assets"] = round(df.loc["OTHBRF"] / df.loc["ASSET"] * 100, 2)
    except: df.loc["Borrowings/Assets"] = None

    try: df.loc["GAAP Capital"] = df.loc["EQTOT"]
    except: df.loc["GAAP Capital"] = None

    try: df.loc["GAAP Capital/Assets"] = round(df.loc["EQTOT"] / df.loc["ASSET"] * 100, 2)
    except: df.loc["GAAP Capital/Assets"] = None

    try:
        df.loc["Non-Owner Occupied Commercial Real Estate/Total Capital"] = round(
            (df.loc["LNRECONS"] + df.loc["LNREMULT"] + df.loc["LNCOMRE"] + df.loc["LNRENROT"]) /
            (df.loc["LNATRES"] + df.loc["RBCT1J"]) * 100, 2)
    except: df.loc["Non-Owner Occupied Commercial Real Estate/Total Capital"] = None

    try: df.loc["Net Interest Margin"] = round(df.loc["NIMY"], 2)
    except: df.loc["Net Interest Margin"] = None

    try: df.loc["Net Income"] = df.loc["NETINC"]
    except: df.loc["Net Income"] = None

    try: df.loc["Efficiency Ratio"] = round(df.loc["EEFFR"], 2)
    except: df.loc["Efficiency Ratio"] = None

    try:
        months_up_to_quarter = df.columns.to_series().dt.quarter.map({1: 3, 2: 6, 3: 9, 4: 12})
        df.loc["Annualized Earnings (Pre-Tax)"] = ((df.loc["PTAXNETINC"] - df.loc["IGLSEC"]) / months_up_to_quarter) * 12
        df.loc["Annualized Earnings (Tax Adjusted)"] = (df.loc["NETINC"] / months_up_to_quarter) * 12
    except:
        df.loc["Annualized Earnings (Pre-Tax)"] = None
        df.loc["Annualized Earnings (Tax Adjusted)"] = None

    try: df.loc["Return on Assets"] = round(df.loc["ROA"], 2)
    except: df.loc["Return on Assets"] = None

    try: df.loc["Return on Equity"] = round(df.loc["ROE"], 2)
    except: df.loc["Return on Equity"] = None

    try: df.loc["Allowance for Loan Losses"] = df.loc["LNATRES"]
    except: df.loc["Allowance for Loan Losses"] = None

    try: df.loc["CECL Adoption"] = df.loc["SCHTMRES"]
    except: df.loc["CECL Adoption"] = None

    try: df.loc["Allowance/Loans"] = round(df.loc["LNATRES"] / df.loc["LNLSGR"] * 100, 2)
    except: df.loc["Allowance/Loans"] = None

    try: df.loc["YTD Provision for Loan Losses"] = df.loc["ELNATR"]
    except: df.loc["YTD Provision for Loan Losses"] = None

    try: df.loc["YTD Net Charge-Offs (Recoveries)"] = df.loc["NTLNLS"]
    except: df.loc["YTD Net Charge-Offs (Recoveries)"] = None

    try:
        months_up_to_quarter = df.columns.to_series().dt.quarter.map({1: 3, 2: 6, 3: 9, 4: 12})
        df.loc["Annualized Losses/Loans"] = round(((df.loc["NTLNLS"] / months_up_to_quarter) * 12) / df.loc["LNLSGR"] * 100, 2)
    except: df.loc["Annualized Losses/Loans"] = None

    try: df.loc["90 Days Past Due & Nonaccrual Loans"] = df.loc["P9ASSET"] + df.loc["NAASSET"]
    except: df.loc["90 Days Past Due & Nonaccrual Loans"] = None

    try: df.loc["Non-Performing Loans Ratio"] = round(df.loc["NCLNLSR"], 2)
    except: df.loc["Non-Performing Loans Ratio"] = None

    try: df.loc["Other Real Estate Owned"] = df.loc["ORE"]
    except: df.loc["Other Real Estate Owned"] = None

    try:
        df.loc["(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)"] = round(
            (df.loc["P9ASSET"] + df.loc["NAASSET"] + df.loc["ORE"]) /
            (df.loc["LNATRES"] + df.loc["EQTOT"] - df.loc["INTAN"]) * 100, 2)
    except: df.loc["(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)"] = None

    try: df.loc["Tier 1 Leverage Ratio"] = round(df.loc["RBC1AAJ"], 2)
    except: df.loc["Tier 1 Leverage Ratio"] = None

    try: df.loc["Common Equity Tier 1 Ratio"] = round(df.loc["IDT1CER"], 2)
    except: df.loc["Common Equity Tier 1 Ratio"] = None

    try: df.loc["Tier 1 Risk Based Ratio"] = round(df.loc["IDT1RWAJR"], 2)
    except: df.loc["Tier 1 Risk Based Ratio"] = None

    try: df.loc["Total Risk Based Ratio"] = round(df.loc["RBCRWAJ"], 2)
    except: df.loc["Total Risk Based Ratio"] = None

    try: df.loc["Capital Contribution"] = df.loc["EQCBHCTR"]
    except: df.loc["Capital Contribution"] = None

    try: df.loc["Ineligible Intangibles"] = df.loc["INTAN"]
    except: df.loc["Ineligible Intangibles"] = None

    try: df.loc["YTD Taxes Paid"] = df.loc["ITAX"]
    except: df.loc["YTD Taxes Paid"] = None

    try: df.loc["YTD Taxes Paid as a Percentage of Income"] = round(df.loc["ITAXR"], 2)
    except: df.loc["YTD Taxes Paid as a Percentage of Income"] = None

    # ✅ FORMATTING SECTION — numbers and percentages
    dollar_rows = [
        "Allowance for Loan Losses", "Annualized Earnings (Pre-Tax)", "Annualized Earnings (Tax Adjusted)",
        "Assets", "Borrowings", "Brokered Deposits", "Capital Contribution", "CECL Adoption",
        "Deposits", "GAAP Capital", "Ineligible Intangibles", "Investment Securities", "Loans",
        "Net Income", "Other Real Estate Owned", "YTD Net Charge-Offs (Recoveries)",
        "YTD Provision for Loan Losses", "YTD Taxes Paid", "90 Days Past Due & Nonaccrual Loans"
    ]

    percent_rows = [
        "(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)", "Allowance/Loans",
        "Borrowings/Assets", "Brokered Deposits/Total Deposits", "Common Equity Tier 1 Ratio",
        "Efficiency Ratio", "GAAP Capital/Assets", "Investments/Assets", "Loan-to-Deposit Ratio",
        "Net Interest Margin", "Non-Owner Occupied Commercial Real Estate/Total Capital",
        "Non-Performing Loans Ratio", "Return on Assets", "Return on Equity",
        "Tier 1 Leverage Ratio", "Tier 1 Risk Based Ratio", "Total Risk Based Ratio",
        "YTD Taxes Paid as a Percentage of Income", "Annualized Losses/Loans"
    ]

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
            gap_row = pd.DataFrame([["" for _ in df.columns]], index=[""], columns=df.columns)
            df = pd.concat([top, gap_row, bottom])

    for row in dollar_rows:
        if row in df.index:
            df.loc[row] = df.loc[row].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "")

    for row in percent_rows:
        if row in df.index:
            df.loc[row] = df.loc[row].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "")

    return df