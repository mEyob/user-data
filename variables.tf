variable "firehose_bucket_name" {
  description = "S3 bucket name for Firehose Delivery Stream"
  type        = string
}

variable "firehose_raw_bucket_name" {
  description = "S3 bucket name for Firehose raw data backup"
  type        = string
}

variable "athena_bucket_name" {
  description = "S3 bucket name for Athena query results"
  type        = string
}