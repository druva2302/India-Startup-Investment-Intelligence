import pandas as pd

# Load raw dataset
df = pd.read_csv("Data/raw/startup_funding.csv")

print("=" * 70)
print("RAW DATA INVESTIGATION")
print("=" * 70)


# --------------------------------------------------
# 1. INVESTIGATE THE 8 DATE RECORDS
# --------------------------------------------------

print("\n1. RAW DATE VALUES")
print("-" * 70)

date_test = pd.to_datetime(
    df["Date dd/mm/yyyy"],
    format="%d/%m/%Y",
    errors="coerce"
)

invalid_dates = df[date_test.isna()]

for _, row in invalid_dates.iterrows():
    print(
        f"Sr No: {row['Sr No']} | "
        f"Raw Date: {repr(row['Date dd/mm/yyyy'])} | "
        f"Startup: {repr(row['Startup Name'])}"
    )


# --------------------------------------------------
# 2. INVESTIGATE PROBLEMATIC AMOUNTS
# --------------------------------------------------

print("\n2. RAW FUNDING AMOUNTS")
print("-" * 70)

amount_text = (
    df["Amount in USD"]
    .astype("string")
    .str.strip()
)

amount_numeric = pd.to_numeric(
    amount_text.str.replace(",", "", regex=False),
    errors="coerce"
)

invalid_amounts = df[
    amount_numeric.isna() &
    df["Amount in USD"].notna()
]

for _, row in invalid_amounts.iterrows():
    print(
        f"Sr No: {row['Sr No']} | "
        f"Startup: {repr(row['Startup Name'])} | "
        f"Amount: {repr(row['Amount in USD'])}"
    )


# --------------------------------------------------
# 3. INVESTIGATE ROWS 2600+
# --------------------------------------------------

print("\n3. RECORDS AROUND ROW 2600")
print("-" * 70)

rows_2600 = df[
    (df["Sr No"] >= 2600) &
    (df["Sr No"] <= 2615)
]

for _, row in rows_2600.iterrows():
    print("\n----------------------------------------")

    for column in df.columns:
        print(
            f"{column}: {repr(row[column])}"
        )