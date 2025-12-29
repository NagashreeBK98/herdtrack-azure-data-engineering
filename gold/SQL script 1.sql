CREATE OR ALTER VIEW dbo.vw_feed
AS
SELECT
    TRY_CAST(Cattle_ID AS VARCHAR(50))      AS Cattle_ID,
    TRY_CAST(FeedType AS VARCHAR(50))       AS FeedType,
    TRY_CAST(FeedQuantityKg AS FLOAT)       AS FeedQuantityKg,
    TRY_CAST(FeedCostUSD AS FLOAT)          AS FeedCostUSD,
    TRY_CAST(FeedingTime AS DATETIME2)      AS FeedingTime
FROM
    OPENROWSET(
        BULK 'feed_type/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT = 'PARQUET'
    ) AS rows;
GO
