import json
import boto3


def lambda_handler(event, context):
    request = event.get('body') or {}
    valid = [
        "first_name" in request, 
        "middle_name" in request, 
        "last_name" in request, 
        "zip_code" in request
    ]

    if all(valid):
        firehose_client = boto3.client('firehose')
        response = firehose_client.put_record(
            DeliveryStreamName="kinesis-firehose-extended-s3-stream",
            Record={'Data': json.dumps(request)})
        return {
            'statusCode': 200, 
            'body': json.dumps(response)
            }

    else:
        return {
            'statusCode': 400, 
            'body': "BAD REQUEST"
            }
