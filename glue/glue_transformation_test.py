from awsglue.utils import getResolvedOptions
args = getResolvedOptions(sys.argv, ["JOB_NAME", "input_loc", "output_loc"])


import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from awsglue.job import Job


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

input_loc = "bucket-name/prefix/sample_data.csv"
output_loc = "bucket-name/prefix/"

inputDyf = glueContext.create_dynamic_frame_from_options(\
    connection_type = "s3", 
    connection_options = { 
        "paths": [input_loc]}, 
    format = "csv",
    format_options={
        "withHeader": True,
        "separator": ","
    })


outputDF = glueContext.write_dynamic_frame.from_options(\
    frame = inputDyf, 
    connection_type = "s3", 
    connection_options = {"path": output_loc 
        }, format = "parquet") 

job.commit()