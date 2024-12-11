from datetime import date
import pandas as pd


def monthly_spending(TODAY: date):
    df = pd.read_csv("cleaned_transactions.csv")
    df.drop(["Unnamed: 0", "Description", "Category", "InGrinnell", "IsAmazon"], axis=1, inplace=True)
    
    this_year = TODAY.year
    YTD_df = df[df["Date"].astype("datetime64[ns]").dt.year == this_year]
    
    YTD_df["Date"] = YTD_df["Date"].astype("datetime64[ns]").dt.month
    YTD_df.rename(columns={"Date" : "Month"}, inplace=True)
    YTD_df = YTD_df.groupby("Month").sum()
    YTD_df.reset_index(inplace=True)
    YTD_df.sort_values("Month")
    
    YTD_df['Month'] = pd.to_datetime(YTD_df["Month"], format='%m').dt.strftime('%B')
    
    return YTD_df

def category_spending(TODAY: date):
    df = pd.read_csv("cleaned_transactions.csv")
    
    this_year = TODAY.year
    df = df[df["Date"].astype("datetime64[ns]").dt.year == this_year]
    
    df.drop(["Unnamed: 0", "Description", "Date", "InGrinnell", "IsAmazon"], axis=1, inplace=True)
    
    df = df.groupby("Category").sum()
    df.reset_index(inplace=True)
    
    return df


def category_by_month(TODAY: date):
    df = pd.read_csv("cleaned_transactions.csv")
    
    this_year = TODAY.year
    df = df[df["Date"].astype("datetime64[ns]").dt.year == this_year]
    
    df["Date"] = df["Date"].astype("datetime64[ns]").dt.month
    df.sort_values("Date")
    
    df['Date'] = pd.to_datetime(df["Date"], format='%m').dt.strftime('%B')
    
    # Drop unneccessary cols
    df.drop(columns=["Unnamed: 0", "Description", "InGrinnell", "IsAmazon"], axis=1, inplace=True)
    
    pivot = pd.pivot_table(
        df,
        values='Amount',
        index='Category',
        columns='Date',
        aggfunc='sum'
    )

    return pivot

def monthly_overview(TODAY: date):
    df = pd.read_csv("cleaned_transactions.csv")
    this_year = TODAY.year
    this_month = TODAY.month
    last_month = TODAY.month - 1
    
    df.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    
    df["Date"] = pd.to_datetime(df["Date"])
    
    if this_month == 1:
        # If change in year
        last_month = 12
        df = df[(df["Date"].dt.year == this_year) & (df["Date"].dt.month == this_month)]
        df = df[df["Date"].dt.year == this_year - 1 & df["Date"].dt.month == last_month]
    else:
        # If middle of the year
        df = df[df["Date"].dt.year == this_year]
        df = df[(df["Date"].dt.month == last_month) | (df["Date"].dt.month == this_month)]
    
    # Split the df
    last_month_df = df[df["Date"].dt.month == last_month]
    this_month_df = df[df["Date"].dt.month == this_month]
    
    # Calculating stats
    total_spent_this_month = this_month_df["Amount"].sum()
    total_spent_last_month = last_month_df["Amount"].sum()
    
    vs_last_month = ((total_spent_this_month - total_spent_last_month) / total_spent_last_month) * 100
    
    
    return (total_spent_this_month, total_spent_last_month, vs_last_month)