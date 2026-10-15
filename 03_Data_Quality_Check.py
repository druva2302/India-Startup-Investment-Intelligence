import pandas as pd

# Load the original raw dataset
df = pd.read_csv("Data/raw/startup_funding.csv")

print("=" * 70)
print("DATA QUALITY INVESTIGATION")
print("=" * 70)


# --------------------------------------------------
# 1. INVESTIGATE INVALID DATES
# --------------------------------------------------

df["Parsed_Date"] = pd.to_datetime(
    df["Date dd/mm/yyyy"],
    format="%d/%m/%Y",
    errors="coerce"
)

invalid_dates = df[df["Parsed_Date"].isna()]

print("\n1. INVALID DATE RECORDS")
print(f"Number of invalid dates: {len(invalid_dates)}")

print("\nInvalid date records:")
print(
    invalid_dates[
        ["Sr No", "Date dd/mm/yyyy", "Startup Name"]
    ].to_string(index=False)
)


# --------------------------------------------------
# 2. INVESTIGATE FUNDING AMOUNTS
# --------------------------------------------------

amount_clean = (
    df["Amount in USD"]
    .astype("string")
    .str.replace(",", "", regex=False)
    .str.strip()
)

parsed_amount = pd.to_numeric(
    amount_clean,
    errors="coerce"
)

invalid_amounts = df[
    parsed_amount.isna() &
    df["Amount in USD"].notna()
]

print("\n" + "=" * 70)
print("2. NON-NUMERIC FUNDING AMOUNTS")
print("=" * 70)

print(f"Number of non-numeric amounts: {len(invalid_amounts)}")

print("\nProblematic amount records:")

print(
    invalid_amounts[
        ["Sr No", "Startup Name", "Amount in USD"]
    ].to_string(index=False)
)


# --------------------------------------------------
# 3. VALID FUNDING AMOUNTS
# --------------------------------------------------

valid_amounts = parsed_amount.notna()

print("\n" + "=" * 70)
print("3. FUNDING AMOUNT SUMMARY")
print("=" * 70)

print(f"Valid funding amounts: {valid_amounts.sum()}")
print(f"Missing/invalid amounts: {(~valid_amounts).sum()}")


# --------------------------------------------------
# 4. SAVE INVESTIGATION RESULTS
# --------------------------------------------------

invalid_dates[
    ["Sr No", "Date dd/mm/yyyy", "Startup Name"]
].to_csv(
    "Data/processed/invalid_date_records.csv",
    index=False
)

invalid_amounts[
    ["Sr No", "Startup Name", "Amount in USD"]
].to_csv(
    "Data/processed/invalid_amount_records.csv",
    index=False
)

print("\nInvestigation files created:")
print("- Data/processed/invalid_date_records.csv")
print("- Data/processed/invalid_amount_records.csv")