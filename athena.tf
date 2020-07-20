resource "aws_s3_bucket" "hoge" {
  bucket = "athena-query-result-1822"
}

# uncomment the following lines to create 
# a database. It will throw an error if 
# the database is already created in AWS Glue 
# resource "aws_athena_database" "hoge" {
#   name   = "database_name"
#   bucket = "${aws_s3_bucket.hoge.bucket}"
# }

resource "aws_athena_workgroup" "workgroup" {
  name = "athena_db_workgroup"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.hoge.bucket}"
    }
  }
}