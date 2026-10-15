import pandas as pd

# ============================================
# 1. LOAD CLEAN DATA
# ============================================

df = pd.read_csv(
    "Data/processed/startup_funding_cleaned.csv"
)

df["Funding_Date"] = pd.to_datetime(
    df["Funding_Date"]
)

print("=" * 70)
print("INDIA STARTUP INVESTMENT INTELLIGENCE - EDA")
print("=" * 70)


# ============================================
# 2. OVERALL BUSINESS KPIs
# ============================================

total_funding = df["Amount_USD"].sum()

total_deals = df["Amount_USD"].notna().sum()

unique_startups = df["Startup_Name"].nunique()

average_deal = df["Amount_USD"].mean()

median_deal = df["Amount_USD"].median()

max_deal = df["Amount_USD"].max()


print("\n1. OVERALL BUSINESS KPIs")
print("-" * 50)

print(f"Total Funding       : ${total_funding:,.0f}")
print(f"Funded Deals        : {total_deals:,}")
print(f"Unique Startups     : {unique_startups:,}")
print(f"Average Deal Size   : ${average_deal:,.0f}")
print(f"Median Deal Size    : ${median_deal:,.0f}")
print(f"Largest Deal        : ${max_deal:,.0f}")


# ============================================
# 3. FUNDING BY YEAR
# ============================================

yearly_funding = (
    df.groupby("Funding_Year")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Deals=("Amount_USD", "count")
      )
      .reset_index()
)

yearly_funding["Average_Deal"] = (
    yearly_funding["Total_Funding"]
    / yearly_funding["Deals"]
)

print("\n2. FUNDING BY YEAR")
print("-" * 50)

print(
    yearly_funding.to_string(index=False)
)


# ============================================
# 4. FUNDING BY INDUSTRY
# ============================================

industry_funding = (
    df.groupby("Industry_Vertical")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Deals=("Amount_USD", "count")
      )
      .reset_index()
      .sort_values(
          "Total_Funding",
          ascending=False
      )
)

industry_funding["Average_Deal"] = (
    industry_funding["Total_Funding"]
    / industry_funding["Deals"]
)

print("\n3. TOP 15 INDUSTRIES BY FUNDING")
print("-" * 50)

print(
    industry_funding
    .head(15)
    .to_string(index=False)
)


# ============================================
# 5. FUNDING BY CITY
# ============================================

city_funding = (
    df.groupby("City_Location")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Deals=("Amount_USD", "count"),
          Startups=("Startup_Name", "nunique")
      )
      .reset_index()
      .sort_values(
          "Total_Funding",
          ascending=False
      )
)

print("\n4. TOP 15 CITIES BY FUNDING")
print("-" * 50)

print(
    city_funding
    .head(15)
    .to_string(index=False)
)


# ============================================
# 6. TOP INVESTORS
# ============================================

investor_funding = (
    df.groupby("Investors_Name")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Deals=("Amount_USD", "count")
      )
      .reset_index()
      .sort_values(
          "Total_Funding",
          ascending=False
      )
)

print("\n5. TOP 15 INVESTORS BY CAPITAL")
print("-" * 50)

print(
    investor_funding
    .head(15)
    .to_string(index=False)
)


# ============================================
# 7. INVESTMENT TYPE
# ============================================

investment_type = (
    df.groupby("Investment_Type")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Deals=("Amount_USD", "count")
      )
      .reset_index()
      .sort_values(
          "Total_Funding",
          ascending=False
      )
)

print("\n6. INVESTMENT TYPE ANALYSIS")
print("-" * 50)

print(
    investment_type.to_string(index=False)
)


# ============================================
# 8. FUNDING SIZE CATEGORY
# ============================================

funding_category = (
    df.groupby(
        "Funding_Size_Category",
        observed=True
    )
    .agg(
        Total_Funding=("Amount_USD", "sum"),
        Deals=("Amount_USD", "count")
    )
    .reset_index()
)

print("\n7. FUNDING SIZE DISTRIBUTION")
print("-" * 50)

print(
    funding_category.to_string(index=False)
)


# ============================================
# 9. TOP 10 STARTUPS
# ============================================

startup_funding = (
    df.groupby("Startup_Name")
      .agg(
          Total_Funding=("Amount_USD", "sum"),
          Deals=("Amount_USD", "count")
      )
      .reset_index()
      .sort_values(
          "Total_Funding",
          ascending=False
      )
)

print("\n8. TOP 10 STARTUPS BY FUNDING")
print("-" * 50)

print(
    startup_funding
    .head(10)
    .to_string(index=False)
)


# ============================================
# 10. FUNDING CONCENTRATION
# ============================================

top_5_startups = (
    startup_funding
    .head(5)["Total_Funding"]
    .sum()
)

top_10_startups = (
    startup_funding
    .head(10)["Total_Funding"]
    .sum()
)

top_5_share = (
    top_5_startups / total_funding
) * 100

top_10_share = (
    top_10_startups / total_funding
) * 100

print("\n9. FUNDING CONCENTRATION")
print("-" * 50)

print(
    f"Top 5 Startups Funding Share  : "
    f"{top_5_share:.2f}%"
)

print(
    f"Top 10 Startups Funding Share : "
    f"{top_10_share:.2f}%"
)


print("\n" + "=" * 70)
print("EDA COMPLETED")
print("=" * 70)