from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, StringType, IntegerType, TimestampType

INPUT_PATH = "data/input/netflow/attack_2.json"
OUTPUT_PATH = "data/input/netflow/attack_2"

spark = (
    SparkSession.builder
    .master("local[4]")
    .config("spark.driver.memory", "8g")
    .config("spark.executor.memory", "8g")
    .config("spark.driver.extraJavaOptions", "-XX:MaxPermSize=512M -XX:MaxHeapFreeRatio=70")
    .config("spark.executor.extraJavaOptions", "-XX:MaxPermSize=512M -XX:MaxHeapFreeRatio=70")
    .getOrCreate()
)

schema = StructType([
    StructField("t_first", TimestampType()),
    StructField("t_last", StringType()),

    StructField("src4_addr", StringType()),
    StructField("src6_addr", StringType()),
    StructField("src_port", IntegerType()),
    StructField("src_tos", IntegerType()),

    StructField("dst4_addr", StringType()),
    StructField("dst6_addr", StringType()),
    StructField("dst_port", IntegerType()),

    StructField("icmp_code", IntegerType()),
    StructField("icmp_status", IntegerType()),

    StructField("in_bytes", IntegerType()),
    StructField("in_packets", IntegerType()),

    StructField("tcp_flags", StringType()),
    StructField("label", StringType()),
    StructField("proto", IntegerType()),
    StructField("sampled", IntegerType()),
    StructField("export_sysid", IntegerType()),
    StructField("fwd_status", IntegerType()),

    StructField("app_latency", FloatType()),
    StructField("cli_latency", FloatType()),
    StructField("srv_latency", FloatType()),

])

df = spark.read.option("multiline", "true").json(INPUT_PATH, schema=schema)
df = df.repartition(50)

df.write.parquet(OUTPUT_PATH)
