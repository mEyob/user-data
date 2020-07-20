resource "aws_glue_catalog_database" "glue_catalog_database" {
  name = "user_database"
}

resource "aws_glue_crawler" "user_data_crawler" {
  database_name = "${aws_glue_catalog_database.glue_catalog_database.name}"
  name          = "user_data_crawler"
  role          = "${aws_iam_role.glue.arn}"
  classifiers   = ["split-array-into-records"]

  s3_target {
    path = "s3://${aws_s3_bucket.kinesis_firehose_stream_bucket.bucket}"
  }
}

resource "aws_iam_role" "glue" {
  name = "AWSGlueServiceRoleTF"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "glue_service" {
    role = aws_iam_role.glue.id
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "s3_access_policy" {
  name = "s3_access_policy"
  role = "${aws_iam_role.glue.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "arn:aws:s3:::processed-user-data-bucket-1822",
        "arn:aws:s3:::processed-user-data-bucket-1822/*"
      ]
    }
  ]
}
EOF
}
