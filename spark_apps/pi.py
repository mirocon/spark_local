import random
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Spark Pi").getOrCreate()
sc = spark.sparkContext

n = 100000

def inside(_):
    x = random.random()
    y = random.random()
    return 1 if x * x + y * y <= 1 else 0

count = sc.parallelize(range(n), 8).map(inside).reduce(lambda a, b: a + b)
print(f"Pi is roughly {4.0 * count / n}")

spark.stop()
