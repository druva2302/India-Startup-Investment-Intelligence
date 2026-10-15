USE startup_funding_db;

WITH industry_funding AS (
    SELECT
        Industry_Standardized,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY Industry_Standardized
)

SELECT
    Industry_Standardized,
    total_funding,
    ROUND(
        total_funding * 100.0 /
        SUM(total_funding) OVER (),
        2
    ) AS funding_share_percent
FROM industry_funding
ORDER BY total_funding DESC;


SELECT
    CASE
        WHEN Amount_USD < 1000000 THEN 'Below $1M'
        WHEN Amount_USD < 10000000 THEN '$1M - $10M'
        WHEN Amount_USD < 50000000 THEN '$10M - $50M'
        ELSE '$50M+'
    END AS funding_size_category,

    COUNT(*) AS funding_deals,

    SUM(Amount_USD) AS total_funding,

    ROUND(AVG(Amount_USD), 2) AS average_deal

FROM startup_funding

WHERE Amount_USD IS NOT NULL

GROUP BY
    CASE
        WHEN Amount_USD < 1000000 THEN 'Below $1M'
        WHEN Amount_USD < 10000000 THEN '$1M - $10M'
        WHEN Amount_USD < 50000000 THEN '$10M - $50M'
        ELSE '$50M+'
    END

ORDER BY total_funding DESC;

WITH industry_summary AS (
    SELECT
        Industry_Standardized,
        COUNT(Amount_USD) AS funding_deals,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY Industry_Standardized
)

SELECT
    Industry_Standardized,
    funding_deals,
    total_funding,
    RANK() OVER (
        ORDER BY total_funding DESC
    ) AS funding_rank
FROM industry_summary
ORDER BY funding_rank;

WITH yearly_funding AS (
    SELECT
        Funding_Year,
        SUM(Amount_USD) AS total_funding
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY Funding_Year
)

SELECT
    Funding_Year,
    total_funding,

    LAG(total_funding) OVER (
        ORDER BY Funding_Year
    ) AS previous_year_funding,

    ROUND(
        (
            total_funding
            - LAG(total_funding) OVER (
                ORDER BY Funding_Year
            )
        )
        * 100.0
        /
        NULLIF(
            LAG(total_funding) OVER (
                ORDER BY Funding_Year
            ),
            0
        ),
        2
    ) AS yoy_growth_percent

FROM yearly_funding

ORDER BY Funding_Year;



WITH city_summary AS (
    SELECT
        City_Standardized,
        COUNT(Amount_USD) AS funding_deals,
        SUM(Amount_USD) AS total_funding,
        AVG(Amount_USD) AS average_deal
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY City_Standardized
)

SELECT
    City_Standardized,
    funding_deals,
    total_funding,
    ROUND(average_deal, 2) AS average_deal,

    RANK() OVER (
        ORDER BY total_funding DESC
    ) AS funding_rank

FROM city_summary

ORDER BY funding_rank;




WITH city_summary AS (
    SELECT
        City_Standardized,
        COUNT(Amount_USD) AS funding_deals,
        SUM(Amount_USD) AS total_funding,
        AVG(Amount_USD) AS average_deal
    FROM startup_funding
    WHERE Amount_USD IS NOT NULL
    GROUP BY City_Standardized
)

SELECT
    City_Standardized,
    funding_deals,
    total_funding,
    ROUND(average_deal, 2) AS average_deal,

    RANK() OVER (
        ORDER BY total_funding DESC
    ) AS funding_rank

FROM city_summary

ORDER BY funding_rank;



SELECT
    Investment_Type_Standardized,
    COUNT(Amount_USD) AS funding_deals,
    SUM(Amount_USD) AS total_funding,
    ROUND(AVG(Amount_USD), 2) AS average_deal,

    ROUND(
        SUM(Amount_USD) * 100.0 /
        SUM(SUM(Amount_USD)) OVER (),
        2
    ) AS funding_share_percent

FROM startup_funding

WHERE Amount_USD IS NOT NULL

GROUP BY Investment_Type_Standardized

ORDER BY total_funding DESC;