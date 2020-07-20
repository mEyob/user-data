provider "aws" {
   region = "us-east-1"
 }

 resource "aws_iam_role" "lambda_exec" {
   name = "backend-lambda-role"

   assume_role_policy = data.aws_iam_policy_document.lambda-assume-role.json

 }

data "aws_iam_policy_document" "lambda-assume-role" {
  statement {
    actions = ["sts:AssumeRole"]
 
    principals {
      type = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "lambda-cloudwatch-log-group" {
  name = "lambda-cloudwatch-log-group"
  role = aws_iam_role.lambda_exec.name
  policy = data.aws_iam_policy_document.cloudwatch-log-group-lambda.json
}
 
data "aws_iam_policy_document" "cloudwatch-log-group-lambda" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
 
    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "lambda_to_kinesis_policy" {
  name   = "backend_lambda_to_kinesis_policy"
  role   = aws_iam_role.lambda_exec.name
  policy = data.aws_iam_policy_document.lambda_firehose_access.json
}

data "aws_iam_policy_document" "lambda_firehose_access" {
  statement {
    actions = [
      "firehose:PutRecordBatch",
      "firehose:PutRecord"
    ]
 
    resources = [
      aws_kinesis_firehose_delivery_stream.extended_s3_stream.arn,
    ]
  }
}

data "archive_file" "lambda" { 
  type = "zip"
  source_file = "src/backend-lambda.py"
  output_path = "package/backend-lambda.zip"
}

resource "aws_lambda_function" "userDetailLambda" {
  filename = data.archive_file.lambda.output_path
  function_name = "backend-lambda-function"
  role = aws_iam_role.lambda_exec.arn
  handler = "backend-lambda.lambda_handler"
  runtime = "python3.6"
  timeout = 60
  source_code_hash = base64sha256(filebase64(data.archive_file.lambda.output_path))
}

