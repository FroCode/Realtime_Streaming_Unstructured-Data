from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
from pyspark.sql import functions as F
from pyspark.sql.functions import udf
from config import configuration
import os

# Your custom UDF imports
from udf_utils import *

def streamWriter(input: DataFrame, checkpointFolder, output):
    return (input.writeStream.
            format('parquet')
            .option('checkpointLocation', checkpointFolder)
            .option('path', output)
            .outputMode('append')
            .trigger(processingTime='5 seconds')
            .start()
            )
def define_udfs():
    return {
        'extract_file_name_udf': udf(extract_file_name, StringType()),
        'extract_class_code_udf': udf(extract_class_code, StringType()),
        'extract_salary_end_udf': udf(extract_salary_end, DoubleType()),
        'extract_end_date_udf': udf(extract_end_date, DateType()),
        'extract_salary_start_udf': udf(extract_salary_start, DateType()),
        'extract_req_udf': udf(extract_req, StringType()),
        'extract_notes_udf': udf(extract_notes, StringType()),
        'extract_duties_udf': udf(extract_duties, StringType()),
        'extract_experience_length_udf': udf(extract_experience_length, StringType()),
        'extract_job_type_udf': udf(extract_job_type, StringType()),
        'extract_education_udf': udf(extract_education, StringType()),
        'extract_school_type_udf': udf(extract_school_type, StringType()),
        'extract_application_location_udf': udf(extract_application_location, StringType())
    }

if __name__ == "__main__":
    # Spark session configuration for S3
    spark = (
        SparkSession.builder.appName('aws_unstructured')
        .config('spark.jars.packages', 
                'org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.469')
        .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
        .config('spark.hadoop.fs.s3a.access.key', configuration.get('AWS_ACCESS_KEY'))
        .config('spark.hadoop.fs.s3a.secret.key', configuration.get('AWS_SECRET_KEY'))
        .config('spark.hadoop.fs.s3a.endpoint', 's3.amazonaws.com')
        .config('spark.hadoop.fs.s3a.aws.credentials.provider', 
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
        .getOrCreate()
    )

    # Input directories
    text_input_dir = 'file:///home/frocode/githubRepos/Realtime_Streaming_Unstructured-Data/input/text'
    json_input_dir = 'file:///home/frocode/githubRepos/Realtime_Streaming_Unstructured-Data/input/json'

    # Define schema
    data_schema = StructType([
        StructField('file_name', StringType(), True),
        StructField('classcode', StringType(), True),
        StructField('salary_end', DoubleType(), True),
        StructField('end_date', DateType(), True),
        StructField('salary_start', DateType(), True),
        StructField('req', StringType(), True),
        StructField('notes', StringType(), True),
        StructField('duties', StringType(), True),
        StructField('experience_length', StringType(), True),
        StructField('job_type', StringType(), True),
        StructField('education', StringType(), True),
        StructField('school_type', StringType(), True),
        StructField('application_location', StringType(), True),
    ])

    udfs = define_udfs()
    json_df = spark.readStream.json(json_input_dir, schema=data_schema, multiLine=True)
    
    # Stream data from text directory
    job_bulletins_df = (
        spark.readStream
        .format('text')
        .option('wholetext', 'true')
        .load(json_input_dir)
    )

    # Clean and process the data
    job_bulletins_df = job_bulletins_df.withColumn('file_name', F.regexp_replace(udfs['extract_file_name_udf'](job_bulletins_df['value']), '\r', ''))
    job_bulletins_df = job_bulletins_df.withColumn('value', F.regexp_replace(job_bulletins_df['value'], '\r\n', ''))

    # Apply UDFs for each column
    job_bulletins_df = job_bulletins_df.withColumn('class_code', udfs['extract_class_code_udf'](job_bulletins_df['value'])) \
                                       .withColumn('salary_end', udfs['extract_salary_end_udf'](job_bulletins_df['value'])) \
                                       .withColumn('end_date', udfs['extract_end_date_udf'](job_bulletins_df['value'])) \
                                       .withColumn('salary_start', udfs['extract_salary_start_udf'](job_bulletins_df['value'])) \
                                       .withColumn('req', udfs['extract_req_udf'](job_bulletins_df['value'])) \
                                       .withColumn('notes', udfs['extract_notes_udf'](job_bulletins_df['value'])) \
                                       .withColumn('duties', udfs['extract_duties_udf'](job_bulletins_df['value'])) \
                                       .withColumn('experience_length', udfs['extract_experience_length_udf'](job_bulletins_df['value'])) \
                                       .withColumn('job_type', udfs['extract_job_type_udf'](job_bulletins_df['value'])) \
                                       .withColumn('education', udfs['extract_education_udf'](job_bulletins_df['value'])) \
                                       .withColumn('school_type', udfs['extract_school_type_udf'](job_bulletins_df['value'])) \
                                       .withColumn('application_location', udfs['extract_application_location_udf'](job_bulletins_df['value']))

    # Create a temporary view for SQL queries
    job_bulletins_df.createOrReplaceTempView("job_bulletins_table")

    # Write output using streamWriter
    output_dir = f"{configuration.get('s3_pyspark_url')}/streaming-output/"
    checkpoint_dir = f"{configuration.get('s3_pyspark_url')}/checkpoints/"
    simple_query = (
        job_bulletins_df.writeStream
        .outputMode("append")  # Output mode (append for continuous streaming)
        .format("json")  # Can be 'csv', 'json', 'parquet' depending on your need
        .option("checkpointLocation", checkpoint_dir)  # Ensure the checkpoint location is specified
        .option("path", output_dir)  # Specify the output S3 directory
        .start()
     )
    # query = streamWriter(job_bulletins_df, 's3a://spark-unstructured-streaming-1891/checkpoints/',
    #                      's3a://spark-unstructured-streaming-1891/data/spark_unstructured')


    simple_query.awaitTermination()
    spark.stop()


























