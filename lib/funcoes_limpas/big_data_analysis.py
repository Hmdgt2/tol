
try:
    from pyspark import SparkContext, SparkConf
    from pyspark.sql import SparkSession
    SPARK_AVAILABLE = True
except ImportError:
    SPARK_AVAILABLE = False
from typing import List, Dict

