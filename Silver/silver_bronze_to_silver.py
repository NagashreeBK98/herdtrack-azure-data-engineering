# Databricks notebook source
# ============================================================
# 1️⃣ STORAGE CONFIGURATION
# ============================================================
storage_account = "storage_Account_name"
storage_key = "storage_key"

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.blob.core.windows.net",
    storage_key
)
print("✔ Storage Connected")


# ============================================================
# 2️⃣ LOAD BRONZE JSON STREAM FILES
# ============================================================
from pyspark.sql.functions import explode, col

bronze_path = f"wasbs://bronze@{storage_account}.blob.core.windows.net/api_streams/"

raw_df = spark.read.json(bronze_path, multiLine=True)
print("📥 Bronze Loaded")
raw_df.printSchema()


# ============================================================
# 3️⃣ CLEAN COLUMN NAME FUNCTION
# ============================================================
def clean_cols(df):
    for c in df.columns:
        new = (
            c.strip()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace("-", "_")
            .replace(".", "_")
        )
        df = df.withColumnRenamed(c, new)
    return df


# ============================================================
# 4️⃣ SILVER — ENVIRONMENT TABLE
# ============================================================
df_env = (
    raw_df
        .select(explode("env_records").alias("env"))
        .select("env.*")
)

df_env = clean_cols(df_env).dropDuplicates()

df_env.write.mode("overwrite").parquet(
    f"wasbs://silver@{storage_account}.blob.core.windows.net/env/"
)

print("🌿 ENV → Silver Completed")


# ============================================================
# 5️⃣ SILVER — HEALTH TABLE (FINAL FIX)
# ============================================================

df_health = (
    raw_df
        .select(explode("health_stream").alias("h"))
        .select(
            col("h.Cattle_ID").alias("Cattle_ID"),   # STRING ID like CATTLE_1234
            col("h.HealthScore").cast("int"),
            col("h.LiveFeedIntake").cast("double"),
            col("h.LiveMilkYield").cast("double"),
            col("h.LiveTemperature").cast("double"),
            col("h.Region"),
            col("h.Severity")
        )
)

df_health = clean_cols(df_health).dropDuplicates()

df_health.write.mode("overwrite").parquet(
    f"wasbs://silver@{storage_account}.blob.core.windows.net/health/"
)

print("❤️ HEALTH → Silver Completed (Cattle_ID as STRING)")


# ============================================================
# 6️⃣ SILVER — ALERTS TABLE
# ============================================================
df_alerts = (
    raw_df
        .select(explode("alerts").alias("a"))
        .select("a.*")
)

df_alerts = clean_cols(df_alerts).dropDuplicates()

df_alerts.write.mode("overwrite").parquet(
    f"wasbs://silver@{storage_account}.blob.core.windows.net/alerts/"
)

print("🚨 ALERTS → Silver Completed")


# ============================================================
# 7️⃣ VERIFY SILVER OUTPUT
# ============================================================
print("📂 SILVER FOLDERS:")
display(dbutils.fs.ls(f"wasbs://silver@{storage_account}.blob.core.windows.net/"))


# COMMAND ----------

# ============================================================
# 0️⃣ HELPER: CLEAN COLUMN NAMES
# ============================================================
def clean_cols(df):
    for c in df.columns:
        new = (
            c.strip()
             .replace(" ", "_")
             .replace("(", "")
             .replace(")", "")
             .replace(",", "")
             .replace("-", "_")
             .replace(".", "_")
        )
        df = df.withColumnRenamed(c, new)
    return df


# ============================================================
# 1️⃣ PREGNANCY → SILVER
# ============================================================
pregnancy_path = (
    "wasbs://bronze@herdtrackstorage1.blob.core.windows.net/static/pregnancy_record.csv"
)

df_preg = (
    spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(pregnancy_path)
)

print("📥 Pregnancy CSV Loaded")
df_preg.printSchema()

df_preg = clean_cols(df_preg)

df_preg.write.mode("overwrite").parquet(
    "wasbs://silver@herdtrackstorage1.blob.core.windows.net/pregnancy/"
)

print("🤱 PREGNANCY → Silver Completed")


# ============================================================
# 2️⃣ FEED TYPE → SILVER  (optional but good for analytics)
# ============================================================
feed_path = (
    "wasbs://bronze@herdtrackstorage1.blob.core.windows.net/static/feed_type.csv"
)

df_feed = (
    spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(feed_path)
)

print("📥 Feed CSV Loaded")
df_feed.printSchema()

df_feed = clean_cols(df_feed)

df_feed.write.mode("overwrite").parquet(
    "wasbs://silver@herdtrackstorage1.blob.core.windows.net/feed_type/"
)

print("🌾 FEED TYPE → Silver Completed")


# ============================================================
# 3️⃣ SENSOR METADATA → SILVER  (optional)
# ============================================================
sensor_path = (
    "wasbs://bronze@herdtrackstorage1.blob.core.windows.net/static/sensor_metadata.csv"
)

df_sensor = (
    spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(sensor_path)
)

print("📥 Sensor CSV Loaded")
df_sensor.printSchema()

df_sensor = clean_cols(df_sensor)

df_sensor.write.mode("overwrite").parquet(
    "wasbs://silver@herdtrackstorage1.blob.core.windows.net/sensor_metadata/"
)

print("📟 SENSOR METADATA → Silver Completed")


# ============================================================
# 4️⃣ CHECK ALL SILVER STATIC TABLES
# ============================================================
display(dbutils.fs.ls("wasbs://silver@herdtrackstorage1.blob.core.windows.net/"))


# ============================================================
# LOAD SENSOR METADATA STATIC CSV FROM BRONZE → SILVER
# ============================================================

sensor_path = f"wasbs://bronze@{storage_account}.blob.core.windows.net/static/sensor_metadata.csv"

df_sensor = spark.read.csv(sensor_path, header=True, inferSchema=True)

df_sensor = df_sensor.dropDuplicates()

df_sensor.write.mode("overwrite").parquet(
    f"wasbs://silver@{storage_account}.blob.core.windows.net/sensor/"
)

print("🔧 SENSOR → Silver Completed")




# ============================================================
# SILVER SENSOR (from Bronze/static/sensor_metadata.csv)
# ============================================================

sensor_path = f"wasbs://bronze@{storage_account}.blob.core.windows.net/static/sensor_metadata.csv"

df_sensor = spark.read.csv(sensor_path, header=True, inferSchema=True)

df_sensor = df_sensor.dropDuplicates()

df_sensor.write.mode("overwrite").parquet(
    f"wasbs://silver@{storage_account}.blob.core.windows.net/sensor/"
)

print("🔧 SENSOR → Silver Completed")




display(dbutils.fs.ls(f"wasbs://silver@{storage_account}.blob.core.windows.net/sensor/"))


storage_account = "storage_account_name"
storage_key = "storage_key"

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.blob.core.windows.net",
    storage_key
)
print("✔ Storage Connected")