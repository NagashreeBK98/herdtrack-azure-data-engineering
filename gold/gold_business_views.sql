/* ================================
   1️⃣ HEALTH VIEW
================================ */
CREATE OR ALTER VIEW vw_health AS
SELECT
    Cattle_ID,
    CASTh_HealthScore_AS_INT AS HealthScore,
    CASTh_LiveFeedIntake_AS_DOUBLE AS LiveFeedIntake,
    CASTh_LiveMilkYield_AS_DOUBLE AS LiveMilkYield,
    CASTh_LiveTemperature_AS_DOUBLE AS LiveTemperature,
    Region AS HealthRegion,
    Severity AS HealthSeverity
FROM OPENROWSET(
        BULK 'health/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT = 'PARQUET'
    ) AS rows;
GO


/* ================================
   2️⃣ ENVIRONMENT VIEW
================================ */
CREATE OR ALTER VIEW vw_env AS
SELECT *
FROM OPENROWSET(
        BULK 'env/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT='PARQUET'
    ) AS rows;
GO


/* ================================
   3️⃣ ALERTS VIEW
================================ */
CREATE OR ALTER VIEW vw_alerts AS
SELECT
    Cattle_ID,
    Message AS AlertMessage,
    Region AS AlertRegion,
    Severity AS AlertSeverity,
    TriggerTime
FROM OPENROWSET(
        BULK 'alerts/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT='PARQUET'
    ) AS rows;
GO


/* ================================
   4️⃣ PREGNANCY VIEW
================================ */
CREATE OR ALTER VIEW vw_pregnancy AS
SELECT
    Cattle_ID,
    PregStatus,
    DaysPregnant,
    DueDate,
    LastCheckupDate,
    VetName
FROM OPENROWSET(
        BULK 'pregnancy/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT='PARQUET'
    ) AS rows;
GO


/* ================================
   5️⃣ FEED VIEW
================================ */
CREATE OR ALTER VIEW vw_feed AS
SELECT
    Cattle_ID,
    FeedType,
    FeedQuantityKg,
    FeedingTime AS FeedTime,
    FeedCostUSD
FROM OPENROWSET(
        BULK 'feed_type/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT='PARQUET'
    ) AS rows;
GO


/* ================================
   6️⃣ SENSOR VIEW
================================ */
CREATE OR ALTER VIEW vw_sensor AS
SELECT
    SensorID,
    Cattle_ID,
    SensorType,
    InstallDate,
    BatteryLevel,
    FirmwareVersion
FROM OPENROWSET(
        BULK 'sensor_metadata/*.parquet',
        DATA_SOURCE = 'silver_data',
        FORMAT='PARQUET'
    ) AS rows;
GO


/* ================================
   7️⃣ UNIFIED GOLD VIEW
================================ */
CREATE OR ALTER VIEW vw_unified AS
SELECT
    h.Cattle_ID,

    -- Health
    h.HealthScore,
    h.LiveFeedIntake,
    h.LiveMilkYield,
    h.LiveTemperature,
    h.HealthRegion,
    h.HealthSeverity,

    -- Pregnancy
    p.PregStatus,
    p.DaysPregnant,
    p.DueDate,
    p.LastCheckupDate,
    p.VetName,

    -- Feed
    f.FeedType,
    f.FeedQuantityKg,
    f.FeedTime,
    f.FeedCostUSD,

    -- Alerts
    a.AlertMessage,
    a.AlertRegion,
    a.AlertSeverity,
    a.TriggerTime,

    -- Sensor
    s.SensorID,
    s.SensorType,
    s.InstallDate,
    s.BatteryLevel,
    s.FirmwareVersion

FROM vw_health h
LEFT JOIN vw_pregnancy p ON h.Cattle_ID = p.Cattle_ID
LEFT JOIN vw_feed f ON h.Cattle_ID = f.Cattle_ID
LEFT JOIN vw_alerts a ON h.Cattle_ID = a.Cattle_ID
LEFT JOIN vw_sensor s ON h.Cattle_ID = s.Cattle_ID;
GO
