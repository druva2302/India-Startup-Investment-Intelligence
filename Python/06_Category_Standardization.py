import pandas as pd
import re

# ============================================
# 1. LOAD CLEAN DATA
# ============================================

df = pd.read_csv(
    "Data/processed/startup_funding_cleaned.csv"
)

print("=" * 70)
print("CATEGORY STANDARDIZATION")
print("=" * 70)


# ============================================
# 2. STANDARDIZE GENERAL TEXT
# ============================================

text_columns = [
    "Startup_Name",
    "Industry_Vertical",
    "SubVertical",
    "City_Location",
    "Investors_Name",
    "Investment_Type",
    "Remarks"
]

for column in text_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


# ============================================
# 3. STANDARDIZE CITY NAMES
# ============================================

city_mapping = {
    "Bangalore": "Bengaluru",
    "Bengaluru": "Bengaluru",

    "Gurgaon": "Gurugram",
    "Gurugram": "Gurugram",

    "New Delhi": "Delhi NCR",
    "Delhi": "Delhi NCR",

    "Noida": "Delhi NCR",

    "Kormangala": "Bengaluru"
}

df["City_Standardized"] = (
    df["City_Location"].replace(city_mapping)
)


# ============================================
# 4. STANDARDIZE INDUSTRY NAMES
# ============================================

def standardize_industry(value):

    if pd.isna(value):
        return "Unknown"

    value = str(value).strip()
    value_lower = value.lower()

    # E-Commerce
    if (
        "ecommerce" in value_lower
        or "e-commerce" in value_lower
        or "e commerce" in value_lower
    ):
        return "E-Commerce"

    # Food & Beverage
    if (
        "food & beverage" in value_lower
        or "food and beverage" in value_lower
    ):
        return "Food & Beverage"

    # FinTech
    if "fintech" in value_lower:
        return "FinTech"

    # Healthcare
    if (
        "healthcare" in value_lower
        or "health care" in value_lower
    ):
        return "Healthcare"

    # EdTech
    if (
        "ed-tech" in value_lower
        or "edtech" in value_lower
    ):
        return "Ed-Tech"

    # Education
    if "education" in value_lower:
        return "Education"

    # Logistics
    if "logistics" in value_lower:
        return "Logistics"

    # Technology
    if "technology" in value_lower:
        return "Technology"

    # Finance
    if (
        value_lower == "finance"
        or value_lower == "financial services"
    ):
        return "Finance"

    # Consumer Internet
    if "consumer internet" in value_lower:
        return "Consumer Internet"

    return value


df["Industry_Standardized"] = (
    df["Industry_Vertical"]
    .apply(standardize_industry)
)


# ============================================
# 5. STANDARDIZE INVESTMENT TYPES
# ============================================

def standardize_investment_type(value):

    if pd.isna(value):
        return "Unknown"

    value = str(value)

    # Remove escaped newline
    value = value.replace("\\n", " ")

    # Normalize whitespace
    value = re.sub(r"\s+", " ", value).strip()

    value_lower = value.lower()

    # Private Equity
    if (
        "private equity" in value_lower
        or value_lower == "privateequity"
    ):
        return "Private Equity"

    # Seed + Angel
    if (
        "seed" in value_lower
        and "angel" in value_lower
    ):
        return "Seed / Angel"

    # Seed
    if "seed" in value_lower:
        return "Seed"

    # Angel
    if "angel" in value_lower:
        return "Angel"

    # Series
    if "series a" in value_lower:
        return "Series A"

    if "series b" in value_lower:
        return "Series B"

    if "series c" in value_lower:
        return "Series C"

    if "series d" in value_lower:
        return "Series D"

    if "series e" in value_lower:
        return "Series E"

    if "series f" in value_lower:
        return "Series F"

    if "series g" in value_lower:
        return "Series G"

    if "series h" in value_lower:
        return "Series H"

    if "series j" in value_lower:
        return "Series J"

    # Debt
    if "debt" in value_lower:
        return "Debt"

    # Equity
    if "equity" in value_lower:
        return "Equity"

    # Venture
    if "venture" in value_lower:
        return "Venture"

    # Corporate
    if "corporate" in value_lower:
        return "Corporate"

    # Funding Round
    if "funding round" in value_lower:
        return "Funding Round"

    return value


df["Investment_Type_Standardized"] = (
    df["Investment_Type"]
    .apply(standardize_investment_type)
)


# ============================================
# 6. VALIDATION
# ============================================

print("\nCITY STANDARDIZATION")
print("-" * 50)

print(
    df["City_Standardized"]
    .value_counts()
    .head(15)
)


print("\nINDUSTRY STANDARDIZATION")
print("-" * 50)

print(
    df["Industry_Standardized"]
    .value_counts()
    .head(15)
)


print("\nINVESTMENT TYPE STANDARDIZATION")
print("-" * 50)

print(
    df["Investment_Type_Standardized"]
    .value_counts()
)


# ============================================
# 7. SAVE ANALYTICAL DATASET
# ============================================

output_path = (
    "Data/processed/"
    "startup_funding_analytics.csv"
)

df.to_csv(
    output_path,
    index=False
)


# ============================================
# 8. FINAL MESSAGE
# ============================================

print("\n" + "=" * 70)
print("STANDARDIZATION COMPLETED")
print("=" * 70)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nSaved to:")
print(output_path)
