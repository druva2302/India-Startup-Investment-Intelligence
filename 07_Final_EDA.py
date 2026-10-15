import pandas as pd
import os

print("=" * 70)
print("FINAL STARTUP FUNDING EDA")
print("=" * 70)

# --------------------------------------------------
# 1. LOAD STANDARDIZED DATA
# --------------------------------------------------

input_file = "Data/processed/startup_funding_analytics.csv"

df = pd.read_csv(input_file)

print(f"\nDataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# --------------------------------------------------
# 2. BASIC DATASET OVERVIEW
# --------------------------------------------------

print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)

print(f"Total Records: {len(df):,}")
print(f"Total Columns: {len(df.columns):,}")
print(f"Unique Startups: {df['Startup_Name'].nunique():,}")

known_amount = df["Amount_USD"].notna().sum()
missing_amount = df["Amount_USD"].isna().sum()

print(f"Known Funding Records: {known_amount:,}")
print(f"Missing/Undisclosed Funding Records: {missing_amount:,}")

disclosure_rate = (known_amount / len(df)) * 100

print(f"Funding Disclosure Rate: {disclosure_rate:.2f}%")


# --------------------------------------------------
# 3. OVERALL FUNDING KPIs
# --------------------------------------------------

print("\n" + "=" * 70)
print("2. OVERALL FUNDING KPIs")
print("=" * 70)

total_funding = df["Amount_USD"].sum()
average_deal = df["Amount_USD"].mean()
median_deal = df["Amount_USD"].median()
largest_deal = df["Amount_USD"].max()

print(f"Total Funding: ${total_funding:,.0f}")
print(f"Average Deal Size: ${average_deal:,.0f}")
print(f"Median Deal Size: ${median_deal:,.0f}")
print(f"Largest Deal: ${largest_deal:,.0f}")


# --------------------------------------------------
# 4. FUNDING BY YEAR
# --------------------------------------------------

print("\n" + "=" * 70)
print("3. FUNDING BY YEAR")
print("=" * 70)

yearly = (
    df.dropna(subset=["Amount_USD"])
      .groupby("Funding_Year")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Funding_Deals=("Amount_USD", "count"),
          Average_Deal=("Amount_USD", "mean"),
          Median_Deal=("Amount_USD", "median"),
          Unique_Startups=("Startup_Name", "nunique")
      )
      .reset_index()
      .sort_values("Funding_Year")
)

print(yearly.to_string(index=False))


# --------------------------------------------------
# 5. INDUSTRY ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 70)
print("4. INDUSTRY ANALYSIS")
print("=" * 70)

industry = (
    df.dropna(subset=["Amount_USD"])
      .groupby("Industry_Standardized")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Funding_Deals=("Amount_USD", "count"),
          Average_Deal=("Amount_USD", "mean"),
          Unique_Startups=("Startup_Name", "nunique")
      )
      .reset_index()
      .sort_values("Total_Funding", ascending=False)
)

industry["Funding_Share_%"] = (
    industry["Total_Funding"] / total_funding * 100
)

print(industry.head(15).to_string(index=False))


# --------------------------------------------------
# 6. CITY / GEOGRAPHIC ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 70)
print("5. GEOGRAPHIC ANALYSIS")
print("=" * 70)

city = (
    df.dropna(subset=["Amount_USD"])
      .groupby("City_Standardized")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Funding_Deals=("Amount_USD", "count"),
          Unique_Startups=("Startup_Name", "nunique"),
          Average_Deal=("Amount_USD", "mean")
      )
      .reset_index()
      .sort_values("Total_Funding", ascending=False)
)

city["Funding_Share_%"] = (
    city["Total_Funding"] / total_funding * 100
)

print(city.head(15).to_string(index=False))


# --------------------------------------------------
# 7. INVESTMENT TYPE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 70)
print("6. INVESTMENT TYPE ANALYSIS")
print("=" * 70)

investment = (
    df.dropna(subset=["Amount_USD"])
      .groupby("Investment_Type_Standardized")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Funding_Deals=("Amount_USD", "count"),
          Average_Deal=("Amount_USD", "mean")
      )
      .reset_index()
      .sort_values("Total_Funding", ascending=False)
)

investment["Funding_Share_%"] = (
    investment["Total_Funding"] / total_funding * 100
)

print(investment.to_string(index=False))


# --------------------------------------------------
# 8. FUNDING SIZE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 70)
print("7. FUNDING SIZE ANALYSIS")
print("=" * 70)

size_analysis = (
    df.dropna(subset=["Amount_USD"])
      .groupby("Funding_Size_Category")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Funding_Deals=("Amount_USD", "count"),
          Average_Deal=("Amount_USD", "mean")
      )
      .reset_index()
)

size_analysis["Funding_Share_%"] = (
    size_analysis["Total_Funding"] / total_funding * 100
)

print(size_analysis.to_string(index=False))


# --------------------------------------------------
# 9. TOP STARTUPS
# --------------------------------------------------

print("\n" + "=" * 70)
print("8. TOP STARTUPS BY FUNDING")
print("=" * 70)

startup = (
    df.dropna(subset=["Amount_USD"])
      .groupby("Startup_Name")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Funding_Deals=("Amount_USD", "count")
      )
      .reset_index()
      .sort_values("Total_Funding", ascending=False)
)

startup["Funding_Share_%"] = (
    startup["Total_Funding"] / total_funding * 100
)

print(startup.head(20).to_string(index=False))


# --------------------------------------------------
# 10. FUNDING CONCENTRATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("9. FUNDING CONCENTRATION")
print("=" * 70)

top_5_funding = startup.head(5)["Total_Funding"].sum()
top_10_funding = startup.head(10)["Total_Funding"].sum()

top_5_share = top_5_funding / total_funding * 100
top_10_share = top_10_funding / total_funding * 100

print(f"Top 5 Startups Funding Share: {top_5_share:.2f}%")
print(f"Top 10 Startups Funding Share: {top_10_share:.2f}%")


# --------------------------------------------------
# 11. DATA QUALITY SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("10. DATA QUALITY SUMMARY")
print("=" * 70)

quality = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Duplicate Records",
        "Known Funding Records",
        "Missing Funding Records",
        "Funding Disclosure Rate",
        "Unique Startups",
        "Unique Industries",
        "Unique Cities",
        "Unique Investors"
    ],
    "Value": [
        len(df),
        df.duplicated().sum(),
        known_amount,
        missing_amount,
        f"{disclosure_rate:.2f}%",
        df["Startup_Name"].nunique(),
        df["Industry_Standardized"].nunique(),
        df["City_Standardized"].nunique(),
        df["Investors_Name"].nunique()
    ]
})

print(quality.to_string(index=False))


# --------------------------------------------------
# 12. EXPORT ANALYSIS TABLES
# --------------------------------------------------

output_folder = "Data/processed/final_analysis"

os.makedirs(output_folder, exist_ok=True)

yearly.to_csv(
    f"{output_folder}/funding_by_year.csv",
    index=False
)

industry.to_csv(
    f"{output_folder}/funding_by_industry.csv",
    index=False
)

city.to_csv(
    f"{output_folder}/funding_by_city.csv",
    index=False
)

investment.to_csv(
    f"{output_folder}/funding_by_investment_type.csv",
    index=False
)

size_analysis.to_csv(
    f"{output_folder}/funding_by_size.csv",
    index=False
)

startup.head(100).to_csv(
    f"{output_folder}/top_startups.csv",
    index=False
)

quality.to_csv(
    f"{output_folder}/data_quality_summary.csv",
    index=False
)


# --------------------------------------------------
# 13. COMPLETION
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL EDA COMPLETED")
print("=" * 70)

print("\nAnalysis files saved to:")
print("Data/processed/final_analysis/")