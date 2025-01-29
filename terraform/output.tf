output "s3_bucket_name" {
  value = aws_s3_bucket.spark_streaming_bucket.bucket
}

output "s3_bucket_url" {
  value = "s3://${aws_s3_bucket.spark_streaming_bucket.bucket}/"
}
output "s3_pyspark_url" {
    value = "s3a://${aws_s3_bucket.spark_streaming_bucket.bucket}"
}