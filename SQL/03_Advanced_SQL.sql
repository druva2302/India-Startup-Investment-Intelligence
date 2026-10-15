USE startup_funding_db;

WITH ordered_deals AS (
    SELECT
        Amount_USD,
        ROW_NUMBER() OVER (
            ORDER BY Amount_USD
        ) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
)
SELECT
    ROUND(AVG(Amount_USD), 2) AS median_deal_size
FROM ordered_deals
WHERE rn IN (
    FLOOR((total_rows + 1) / 2),
    FLOOR((total_rows + 2) / 2)
);


WITH startup_industry AS (
    SELECT
        Industry_Standardized,
        Startup_Name,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY
        Industry_Standardized,
        Startup_Name
),
ranked_startups AS (
    SELECT
        Industry_Standardized,
        Startup_Name,
        total_funding,
        ROW_NUMBER() OVER (
            PARTITION BY Industry_Standardized
            ORDER BY total_funding DESC
        ) AS industry_rank
    FROM startup_industry
)
SELECT
    Industry_Standardized,
    Startup_Name,
    total_funding
FROM ranked_startups
WHERE industry_rank = 1
ORDER BY total_funding DESC;


SELECT
    COUNT(*) AS total_records,

    SUM(
        CASE
            WHEN Amount_USD IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_funding_amounts,

    SUM(
        CASE
            WHEN Startup_Name IS NULL
                 OR TRIM(Startup_Name) = ''
            THEN 1
            ELSE 0
        END
    ) AS missing_startup_names,

    SUM(
        CASE
            WHEN Industry_Standardized IS NULL
                 OR TRIM(Industry_Standardized) = ''
            THEN 1
            ELSE 0
        END
    ) AS missing_industries,

    SUM(
        CASE
            WHEN City_Standardized IS NULL
                 OR TRIM(City_Standardized) = ''
            THEN 1
            ELSE 0
        END
    ) AS missing_cities

FROM startup_funding;

SELECT
    Funding_Year,
    Funding_Quarter,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY
    Funding_Year,
    Funding_Quarter
ORDER BY
    Funding_Year,
    Funding_Quarter;
    
    SELECT
    Funding_Month,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Funding_Month
ORDER BY total_funding DESC;


SELECT
    Funding_Year,

    COUNT(*) AS total_records,

    COUNT(Amount_USD) AS disclosed_funding_records,

    COUNT(*) - COUNT(Amount_USD) AS missing_funding_records,

    ROUND(
        COUNT(Amount_USD) * 100.0 / COUNT(*),
        2
    ) AS disclosure_rate_percent

FROM startup_funding

GROUP BY Funding_Year
ORDER BY Funding_Year;

WITH city_funding AS (
    SELECT
        City_Standardized,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY City_Standardized
)
SELECT
    City_Standardized,
    total_funding,
    ROUND(
        total_funding * 100.0 /
        SUM(total_funding) OVER (),
        2
    ) AS funding_share_percent
FROM city_funding
ORDER BY total_funding DESC;


SELECT
    Investment_Type_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Investment_Type_Standardized
HAVING COUNT(Amount_USD) >= 5
ORDER BY average_deal DESC;


WITH startup_summary AS (
    SELECT
        Startup_Name,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY Startup_Name
),
total_market AS (
    SELECT
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
)
SELECT
    s.Startup_Name,
    s.total_funding,
    ROUND(
        s.total_funding * 100.0 /
        t.total_funding,
        2
    ) AS funding_share_percent
FROM startup_summary s
CROSS JOIN total_market t
ORDER BY s.total_funding DESC
LIMIT 10;

WITH yearly_funding AS (
    SELECT
        Funding_Year,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY Funding_Year
),
yearly_comparison AS (
    SELECT
        Funding_Year,
        total_funding,
        LAG(total_funding) OVER (
            ORDER BY Funding_Year
        ) AS previous_year_funding
    FROM yearly_funding
)
SELECT
    Funding_Year,
    total_funding,
    previous_year_funding,
    ROUND(
        (total_funding - previous_year_funding)
        * 100.0
        / NULLIF(previous_year_funding, 0),
        2
    ) AS yoy_growth_percent
FROM yearly_comparison
ORDER BY Funding_Year;

-- View 1: Funding by Year
CREATE OR REPLACE VIEW vw_funding_by_year AS
SELECT
    Funding_Year,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Funding_Year;


-- View 2: Industry Summary
CREATE OR REPLACE VIEW vw_industry_summary AS
SELECT
    Industry_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Industry_Standardized;


-- View 3: City Summary
CREATE OR REPLACE VIEW vw_city_summary AS
SELECT
    City_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY City_Standardized;


-- View 4: Investment Type Summary
CREATE OR REPLACE VIEW vw_investment_type_summary AS
SELECT
    Investment_Type_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal
FROM startup_funding
WHERE Amount_USD IS NOT NULL
GROUP BY Investment_Type_Standardized;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';
