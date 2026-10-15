import pandas as pd
import mysql.connector
from mysql.connector import Error

print("=" * 70)
print("IMPORTING STARTUP FUNDING DATA INTO MYSQL")
print("=" * 70)

# --------------------------------------------------
# 1. LOAD CLEANED DATA
# --------------------------------------------------

csv_file = "Data/processed/startup_funding_analytics.csv"

df = pd.read_csv(csv_file)

print(f"\nCSV loaded successfully")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# --------------------------------------------------
# 2. CONNECT TO MYSQL
# --------------------------------------------------

try:

    password = input("\nEnter MySQL root password: ")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="startup_funding_db"
    )

    if not connection.is_connected():
        print("Could not connect to MySQL.")
        exit()

    print("\nMySQL connection successful!")


    # --------------------------------------------------
    # 3. CREATE CURSOR
    # --------------------------------------------------

    cursor = connection.cursor()


    # --------------------------------------------------
    # 4. CLEAR EXISTING TABLE DATA
    # --------------------------------------------------

    cursor.execute("DELETE FROM startup_funding")

    connection.commit()

    print("Existing table data cleared.")


    # --------------------------------------------------
    # 5. INSERT QUERY
    # --------------------------------------------------

    insert_query = """
    INSERT INTO startup_funding (
        Sr_No,
        Funding_Date,
        Startup_Name,
        Industry_Vertical,
        SubVertical,
        City_Location,
        Investors_Name,
        Investment_Type,
        Amount_USD,
        Remarks,
        Funding_Year,
        Funding_Month,
        Funding_Quarter,
        Funding_Size_Category,
        City_Standardized,
        Industry_Standardized,
        Investment_Type_Standardized
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s
    )
    """


    # --------------------------------------------------
    # 6. PREPARE DATA
    # --------------------------------------------------

    df["Funding_Date"] = pd.to_datetime(
        df["Funding_Date"],
        errors="coerce"
    ).dt.date


    # Convert pandas missing values to MySQL NULL
    data = []

    for row in df.itertuples(index=False, name=None):

        cleaned_row = tuple(
            None if pd.isna(value) else value
            for value in row
        )

        data.append(cleaned_row)


    # --------------------------------------------------
    # 7. INSERT DATA IN BATCHES
    # --------------------------------------------------

    batch_size = 500

    total_inserted = 0

    for i in range(0, len(data), batch_size):

        batch = data[i:i + batch_size]

        cursor.executemany(
            insert_query,
            batch
        )

        connection.commit()

        total_inserted += len(batch)

        print(
            f"Inserted: {total_inserted:,}/{len(data):,}"
        )


    # --------------------------------------------------
    # 8. VERIFY DATA
    # --------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM startup_funding"
    )

    result = cursor.fetchone()

    mysql_rows = result[0]


    print("\n" + "=" * 70)
    print("IMPORT COMPLETED")
    print("=" * 70)

    print(f"\nCSV rows:   {len(df):,}")
    print(f"MySQL rows: {mysql_rows:,}")


    if mysql_rows == len(df):

        print("\nSUCCESS: All 3,044 records imported successfully!")

    else:

        print("\nWARNING: CSV and MySQL row counts do not match.")


    # --------------------------------------------------
    # 9. CLOSE CONNECTION
    # --------------------------------------------------

    cursor.close()
    connection.close()

    print("\nMySQL connection closed.")


except Error as e:

    print("\n" + "=" * 70)
    print("MYSQL ERROR")
    print("=" * 70)

    print(e)


except Exception as e:

    print("\n" + "=" * 70)
    print("GENERAL ERROR")
    print("=" * 70)

    print(e)