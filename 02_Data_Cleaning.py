import pandas as pd
import numpy as np
import re

# ============================================
# 1. LOAD RAW DATA
# ============================================

df = pd.read_csv("Data/raw/startup_funding.csv")

print("RAW DATA LOADED")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ============================================
# 2. CLEAN COLUMN NAMES
# ============================================

df.columns = [
    "Sr_No",
    "Funding_Date",
    "Startup_Name",
    "Industry_Vertical",
    "SubVertical",
    "City_Location",
    "Investors_Name",
    "Investment_Type",
    "Amount_USD",
    "Remarks"
]


# ============================================
# 3. CLEAN TEXT / ENCODING
# ============================================

def clean_text(value):

    if pd.isna(value):
        return value

    value = str(value)

    # Remove encoded non-breaking spaces
    value = re.sub(
        r"\\xC2\\xA0",
        " ",
        value,
        flags=re.IGNORECASE
    )

    # Remove actual non-breaking spaces
    value = value.replace("\xa0", " ")

    # Remove extra whitespace
    value = re.sub(r"\s+", " ", value)

    return value.strip()


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
    df[column] = df[column].apply(clean_text)


# ============================================
# 4. STANDARDIZE MISSING TEXT VALUES
# ============================================

missing_columns = [
    "Industry_Vertical",
    "SubVertical",
    "City_Location",
    "Investors_Name",
    "Investment_Type"
]

for column in missing_columns:
    df[column] = df[column].fillna("Unknown")


# ============================================
# 5. CLEAN DATE VALUES
# ============================================

df["Funding_Date"] = (
    df["Funding_Date"]
    .astype("string")
    .str.strip()
)

# Remove encoded special characters
df["Funding_Date"] = df["Funding_Date"].str.replace(
    r"\\+xC2\\+xA0",
    "",
    regex=True,
    flags=re.IGNORECASE
)

# Remove actual non-breaking spaces
df["Funding_Date"] = df["Funding_Date"].str.replace(
    "\xa0",
    "",
    regex=False
)

df["Funding_Date"] = df["Funding_Date"].str.strip()

# Replace dots with slashes
df["Funding_Date"] = df["Funding_Date"].str.replace(
    ".",
    "/",
    regex=False
)

# Fix double slashes
df["Funding_Date"] = df["Funding_Date"].str.replace(
    "//",
    "/",
    regex=False
)

# 05/072018 → 05/07/2018
df["Funding_Date"] = df["Funding_Date"].str.replace(
    r"^(\d{2})/(\d{2})(\d{4})$",
    r"\1/\2/\3",
    regex=True
)

# 01/07/015 → 01/07/2015
df["Funding_Date"] = df["Funding_Date"].str.replace(
    r"^(\d{2})/(\d{2})/(\d{3})$",
    r"\1/\2/2\3",
    regex=True
)

# 10/7/2015 → 10/07/2015
df["Funding_Date"] = df["Funding_Date"].str.replace(
    r"^(\d{1,2})/(\d{1,2})/(\d{4})$",
    lambda x: (
        f"{int(x.group(1)):02d}/"
        f"{int(x.group(2)):02d}/"
        f"{x.group(3)}"
    ),
    regex=True
)

# Convert to datetime
df["Funding_Date"] = pd.to_datetime(
    df["Funding_Date"],
    format="%d/%m/%Y",
    errors="coerce"
)


# ============================================
# 6. CLEAN FUNDING AMOUNT
# ============================================

df["Amount_USD"] = (
    df["Amount_USD"]
    .astype("string")
    .str.strip()
)

# Remove encoded characters
df["Amount_USD"] = df["Amount_USD"].str.replace(
    r"\\xC2\\xA0",
    "",
    regex=True,
    flags=re.IGNORECASE
)

# Convert undisclosed / unknown / N/A to missing
unknown_amounts = [
    "undisclosed",
    "unknown",
    "n/a",
    "N/A",
    "Undisclosed",
    "Unknown"
]

df["Amount_USD"] = df["Amount_USD"].replace(
    unknown_amounts,
    pd.NA
)

# Remove + and commas
df["Amount_USD"] = (
    df["Amount_USD"]
    .str.replace("+", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

# Convert to numeric
df["Amount_USD"] = pd.to_numeric(
    df["Amount_USD"],
    errors="coerce"
)


# ============================================
# 7. CREATE DATE FEATURES
# ============================================

df["Funding_Year"] = df["Funding_Date"].dt.year

df["Funding_Month"] = df["Funding_Date"].dt.month

df["Funding_Quarter"] = (
    "Q"
    + df["Funding_Date"]
    .dt.quarter
    .astype("Int64")
    .astype("string")
)


# ============================================
# 8. CREATE FUNDING SIZE CATEGORY
# ============================================

df["Funding_Size_Category"] = pd.cut(
    df["Amount_USD"],
    bins=[
        -np.inf,
        1_000_000,
        10_000_000,
        50_000_000,
        np.inf
    ],
    labels=[
        "Below $1M",
        "$1M - $10M",
        "$10M - $50M",
        "$50M+"
    ]
)


# ============================================
# 9. VALIDATE CLEANED DATA
# ============================================

print("\n" + "=" * 70)
print("CLEANED DATA VALIDATION")
print("=" * 70)

print("\nRows and Columns:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nInvalid Dates:")
print(df["Funding_Date"].isna().sum())

print("\nValid Funding Amounts:")
print(df["Amount_USD"].notna().sum())

print("\nMissing Funding Amounts:")
print(df["Amount_USD"].isna().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================
# 10. SAVE CLEAN DATASET
# ============================================

output_path = "Data/processed/startup_funding_cleaned.csv"

df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 70)
print("CLEANING COMPLETED")
print("=" * 70)

print(f"Clean dataset saved to: {output_path}")