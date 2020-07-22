resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream" {
  name        = "kinesis-firehose-extended-s3-stream"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.kinesis_firehose_stream_bucket.arn
    s3_backup_mode = "Enabled"
    buffer_size        = 5
    buffer_interval    = 60

    s3_backup_configuration {
      role_arn   = aws_iam_role.firehose_role.arn
      bucket_arn = aws_s3_bucket.kinesis_firehose_stream_bucket_backup.arn

      cloudwatch_logging_options {
        enabled         = true
        log_group_name  = aws_cloudwatch_log_group.kinesis_firehose_stream_logging_group.name
        log_stream_name = aws_cloudwatch_log_stream.kinesis_firehose_stream_logging_stream.name
      }
    }

    processing_configuration {
      enabled = "true"

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.transformerLambda.arn}:$LATEST"
        }
      }
    }

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.kinesis_firehose_stream_logging_group.name
      log_stream_name = aws_cloudwatch_log_stream.kinesis_firehose_stream_logging_stream.name
    }
  }
}

resource "aws_cloudwatch_log_group" "kinesis_firehose_stream_logging_group" {
  name = "/aws/kinesisfirehose/kinesis_firehose_stream_name"
}

resource "aws_cloudwatch_log_stream" "kinesis_firehose_stream_logging_stream" {
  log_group_name = aws_cloudwatch_log_group.kinesis_firehose_stream_logging_group.name
  name           = "S3Delivery"
}

resource "aws_s3_bucket" "kinesis_firehose_stream_bucket" {
  bucket = var.firehose_bucket_name
  acl    = "private"
}

resource "aws_s3_bucket" "kinesis_firehose_stream_bucket_backup" {
  bucket = var.firehose_raw_bucket_name
  acl    = "private"
}

data "aws_iam_policy_document" "firehose-assume-role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["firehose.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "firehose_access" {
  statement {
    effect = "Allow"

    actions = [
      "s3:AbortMultipartUpload",
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject",
    ]

    resources = [
      aws_s3_bucket.kinesis_firehose_stream_bucket.arn,
      "${aws_s3_bucket.kinesis_firehose_stream_bucket.arn}/*",
      aws_s3_bucket.kinesis_firehose_stream_bucket_backup.arn,
      "${aws_s3_bucket.kinesis_firehose_stream_bucket_backup.arn}/*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction",
      "lambda:GetFunctionConfiguration",
    ]

    resources = [
      aws_lambda_function.transformerLambda.arn,
      "${aws_lambda_function.transformerLambda.arn}:*",
    ]
  }
}

resource "aws_iam_role" "firehose_role" {
  name = "firehose_stream_role"
  assume_role_policy = data.aws_iam_policy_document.firehose-assume-role.json
}

resource "aws_iam_role_policy" "kinesis_firehose_access_bucket_policy" {
  name   = "kinesis_firehose_access_bucket_policy"
  role   = aws_iam_role.firehose_role.name
  policy = data.aws_iam_policy_document.firehose_access.json
}