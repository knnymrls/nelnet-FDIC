import pandas as pd

def apply_calculations(df):
    """Applies all custom calculations directly on the DataFrame."""

    # Convert values to numeric to avoid errors
    df = df.apply(pd.to_numeric, errors='coerce')

    # Perform calculations
    try:
        df.loc["Investment securities"] = df.loc["SC"] + df.loc["CHBALI"]
    except Exception as e:
        print(f"Error calculating Investment securities: {e}")
        df.loc["Investment securities"] = None

    try:
        df.loc["Investments/Assets"] = round(((df.loc["SC"] + df.loc["CHBALI"]) / df.loc["ASSET"]) * 100)
    except Exception as e:
        print(f"Error calculating Investments/Assets: {e}")
        df.loc["Investments/Assets"] = None

    try:
        df.loc["Loan-to-Deposit Ratio"] = round((df.loc["LNLSGR"] / df.loc["DEP"]) * 100)
    except Exception as e:
        print(f"Error calculating Loan-to-Deposit Ratio: {e}")
        df.loc["Loan-to-Deposit Ratio"] = None

    try:
        df.loc["Brokered Deposits/Total Deposits"] = round((df.loc["BRO"] / df.loc["DEP"]) * 100, 1)
    except Exception as e:
        print(f"Error calculating Brokered Deposits/Total Deposits: {e}")
        df.loc["Brokered Deposits/Total Deposits"] = None
        
    try:
        df.loc["Borrowings/Assets"] = round((df.loc["OTHBRF"] / df.loc["ASSET"]) * 100, 1)
    except Exception as e:
        print(f"Error calculating Borrowings/Assets: {e}")
        df.loc["Borrowings/Assets"] = None
        
    try:
        df.loc["Non-Owner Occupied Commercial Real Estate/Total Capital"] = round(((df.loc["LNRECONS"] + df.loc["LNREMULT"] + df.loc["LNCOMRE"] + df.loc["LNRENROT"]) / (df.loc["LNATRES"] + df.loc["RBCT1J"])) * 100)
    except Exception as e:
        print(f"Error calculating Non-Owner Occupied Commercial Real Estate/Total Capital: {e}")
        df.loc["Non-Owner Occupied Commercial Real Estate/Total Capital"] = None

    try:
        # Extract quarter from REPDTE (date index)
        months_up_to_quarter = df.columns.to_series().dt.quarter.map({1: 3, 2: 6, 3: 9, 4: 12})

        #BUG: Find the other thing you should be subtracting from this!
        df.loc["Annualized Earnings (Pre-Tax)"] = ((df.loc["PTAXNETINC"] + df.loc["IGLSEC"]) / months_up_to_quarter) * 12
    except Exception as e:
        print(f"Error calculating Annualized Earnings (Pre-Tax): {e}")
        df.loc["Annualized Earnings (Pre-Tax)"] = None
        
    try:
        # Extract quarter from REPDTE (date index)
        months_up_to_quarter = df.columns.to_series().dt.quarter.map({1: 3, 2: 6, 3: 9, 4: 12})

        #BUG: This isn't matching goal!
        df.loc["Annualized Earnings (Tax-Adjusted)"] = (df.loc["NETINC"] / months_up_to_quarter) * 12
    except Exception as e:
        print(f"Error calculating Annualized Earnings (Tax-Adjusted): {e}")
        df.loc["Annualized Earnings (Tax-Adjusted)"] = None
        
    try:
        #BUG: This isn't matching goal!
        df.loc["Allowance/Loans"] = round((df.loc["NETINC"] / (df.loc["LNLSGR"]) * 100), 2)
    except Exception as e:
        print(f"Error calculating Allowance/Loans: {e}")
        df.loc["Allowance/Loans"] = None
        
    try:
        #BUG: This isn't matching goal!
        months_up_to_quarter = df.columns.to_series().dt.quarter.map({1: 3, 2: 6, 3: 9, 4: 12})
        df.loc["Annualized Losses/Loans"] = round((((df.loc["NTLNLS"] / months_up_to_quarter)*12)/df.loc["LNLSGR"]) * 100, 2)
    except Exception as e:
        print(f"Error calculating Annualized Losses/Loans: {e}")
        df.loc["Annualized Losses/Loans"] = None
    
    try:
        df.loc["90 Days Past Due & Nonaccrual Loans"] = df.loc["P9ASSET"] + df.loc["NAASSET"]
    except Exception as e:
        print(f"Error calculating 90 Days Past Due & Nonaccrual Loans: {e}")
        df.loc["90 Days Past Due & Nonaccrual Loans"] = None
        
    try:
        df.loc["(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)"] = round((df.loc["P9ASSET"] + df.loc["NAASSET"] + df.loc["ORE"]) / (df.loc["LNATRES"] + df.loc["EQTOT"] - df.loc["INTAN"])* 100, 1)
    except Exception as e:
        print(f"Error calculating (90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance): {e}")
        df.loc["(90 Days Past Due + Nonaccrual + REO) / (Capital + Allowance)"] = None
        
        
        
    
        
    

    


    return df
