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
