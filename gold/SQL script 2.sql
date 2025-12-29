CREATE EXTERNAL FILE FORMAT ParquetFormat
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
GO



CREATE EXTERNAL TABLE gold.feed
WITH (
    LOCATION = 'feed/',
    DATA_SOURCE = source_gold,
    FILE_FORMAT = ParquetFormat
)
AS
SELECT
    Cattle_ID,
    FeedType,
    FeedQuantityKg,
    FeedCostUSD,
    FeedingTime
FROM dbo.vw_feed;
GO

