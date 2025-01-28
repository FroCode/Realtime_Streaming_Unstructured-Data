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
  role          = aws_iam_role.glue_crawler_role.arn # Replace with your IAM role ARN
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
# IAM policy for Glue catalog access
resource "aws_iam_policy" "glue_crawler_catalog_policy" {
  name        = "glue_crawler_catalog_policy"
  description = "Policy for Glue crawler to access Glue catalog database"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:GetTableVersion",
          "glue:GetTables"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:glue:eu-central-1:905418126921:catalog"
      }
    ]
  })
}

# Attach the Glue catalog policy to the Glue crawler role
resource "aws_iam_role_policy_attachment" "glue_crawler_catalog_policy_attachment" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = aws_iam_policy.glue_crawler_catalog_policy.arn
}


# IAM policy for S3 access
resource "aws_iam_policy" "glue_crawler_s3_policy" {
  name        = "glue_crawler_s3_policy"
  description = "Policy for Glue crawler to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Effect   = "Allow",
        Resource = [
          "arn:aws:s3:::sparkbucketfrocode/streaming/streaming-output/*",
          "arn:aws:s3:::sparkbucketfrocode"
        ]
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "glue_crawler_role_policy_attachment" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = aws_iam_policy.glue_crawler_s3_policy.arn
}
