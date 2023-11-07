from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, FloatType, StringType, IntegerType, TimestampType

INPUT_PATH = "data/input/netflow/background.json"
OUTPUT_PATH = "data/output/netflow/background/parquet/"

spark = (
    SparkSession.builder
    .master("local[4]")
    .config("spark.executor.memory", "8g")
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

joined = (
    df.alias("df1")
    .join(
        df.alias("df2"),
        on=[
            col("df1.src4_addr") == col("df2.dst4_addr"),
            col("df1.dst4_addr") == col("df2.src4_addr"),
            col("df1.src_port") == col("df2.dst_port"),
            col("df1.dst_port") == col("df2.src_port"),
            col("df1.t_first") == col("df2.t_first")
        ]
    )
    .select(
        "df1.*",
        col("df2.in_bytes").alias("out_bytes"),
        col("df2.in_packets").alias("out_packets")
    )
)

joined.show()
joined.write.parquet(OUTPUT_PATH)

