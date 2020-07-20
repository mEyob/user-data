 resource "aws_iam_role" "lambda_exec_ts" {
   name = "transformer-lambda-role"

   assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-ts.json

 }

data "aws_iam_policy_document" "lambda-assume-role-ts" {
  statement {
    actions = ["sts:AssumeRole"]
 
    principals {
      type = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "lambda-cloudwatch-log-group-ts" {
  name = "lambda-cloudwatch-log-group-ts"
  role = aws_iam_role.lambda_exec_ts.name
  policy = data.aws_iam_policy_document.cloudwatch-log-group-ts-lambda.json
}
 
data "aws_iam_policy_document" "cloudwatch-log-group-ts-lambda" {
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

data "archive_file" "transformerLambdaFile" { 
  type = "zip"
  source_file = "src/transformer-lambda.py"
  output_path = "package/transformer-lambda.zip"
}

resource "aws_lambda_function" "transformerLambda" {
  filename = data.archive_file.transformerLambdaFile.output_path
  function_name = "transformer-lambda-function"
  role = aws_iam_role.lambda_exec_ts.arn
  handler = "transformer-lambda.lambda_handler"
  runtime = "python3.6"
  timeout = 180
  source_code_hash = base64sha256(filebase64(data.archive_file.transformerLambdaFile.output_path))
}

