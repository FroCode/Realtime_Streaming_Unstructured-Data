provider "aws" {
  region = "eu-central-1" # Replace with your AWS region
}

# Glue Database
resource "aws_glue_catalog_database" "spark_streaming_db" {
  name = "spark_streaming_db"
}

# Glue Crawler
resource "aws_glue_crawler" "spark_streaming" {
  name          = "spark_streaming_crawler"
  role          = aws_iam_role.glue_crawler_role.arn # IAM role ARN
  database_name = aws_glue_catalog_database.spark_streaming_db.name

  s3_target {
    path = "s3://sparkbucketfrocode/streaming/streaming-output/"
    exclusions = [
      "_spark_metadata/"
    ]
  }

  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }

  tags = {
    Environment = "Production"
    Project     = "SparkStreaming"
  }
}

# IAM role for Glue Crawler
resource "aws_iam_role" "glue_crawler_role" {
  name = "glue_crawler_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AWS managed policies to the Glue crawler role

# Attach AmazonS3FullAccess
resource "aws_iam_role_policy_attachment" "glue_crawler_s3_full_policy" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Attach AWSGlueConsoleFullAccess
resource "aws_iam_role_policy_attachment" "glue_crawler_console_full_policy" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

# Attach AmazonRedshiftFullAccess
resource "aws_iam_role_policy_attachment" "glue_crawler_redshift_full_policy" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRedshiftFullAccess"
}

# Attach AmazonRedshiftDataFullAccess
resource "aws_iam_role_policy_attachment" "glue_crawler_redshift_data_full_policy" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRedshiftDataFullAccess"
}

resource "aws_s3_bucket" "spark_streaming_bucket" {
  bucket = "my-spark-streaming-fr01" # Change as needed
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "spark_streaming_bucket" {
  bucket = aws_s3_bucket.spark_streaming_bucket.id

  block_public_acls   = false   # Allow public ACLs
  block_public_policy = false   # Allow public policies
  ignore_public_acls  = false   # Do not ignore public ACLs
  restrict_public_buckets = false  # Do not restrict public buckets
}

resource "aws_s3_bucket_policy" "spark_streaming_policy" {
  bucket = aws_s3_bucket.spark_streaming_bucket.id
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:PutBucketPolicy",
          "s3:PutBucketPublicAccessBlock"
        ],
        "Principal": {
          "AWS": [var.aws_arn]  # Update with your IAM user or role ARN
        },
        "Resource": "arn:aws:s3:::my-spark-streaming-fr01"
      }
    ]
  })
}
