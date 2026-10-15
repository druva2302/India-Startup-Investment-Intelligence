USE startup_funding_db;

SELECT COUNT(*) AS total_rows
FROM startup_funding;

SELECT
    SUM(Amount_USD) AS total_disclosed_funding
FROM startup_funding;

SELECT
    AVG(Amount_USD) AS average_deal_size
FROM startup_funding
WHERE Amount_USD IS NOT NULL;

SELECT
    Funding_Year,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    AVG(Amount_USD) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Funding_Year
ORDER BY Funding_Year;

SELECT
    Industry_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    AVG(Amount_USD) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Industry_Standardized
ORDER BY total_funding DESC
LIMIT 10;

SELECT
    City_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    AVG(Amount_USD) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY City_Standardized
ORDER BY total_funding DESC
LIMIT 10;

SELECT
    Startup_Name,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Startup_Name
ORDER BY total_funding DESC
LIMIT 10;



