import json
import boto3


def make_response(code, message):
    """
    Create a simple HTTP response.
    """
    return  {
        'statusCode': code, 
        'body': message
        }

def is_valid_json(json_data):
    """Take a JSON data as an input and return true only
    if it is correctly formed and of 'str' or 'dict' type.
    """
    if isinstance(json_data, str):
        try: 
            data = json.loads(json_data)
            if isinstance(data, str):
                json.loads(data)
        except:
            return False
    elif isinstance(json_data, dict):
        try: 
            json.dumps(json_data)
        except:
            return False
    else:
        return False
    return True
    
def lambda_handler(event, context):
    request = event.get('body') or {}

    if not request:
        return make_response(400, "Empty request")
    if not is_valid_json(request):
        return make_response(400, "Malformed JSON")

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
        return make_response(200, json.dumps(response))
    else:
        return make_response(400, "JSON missing required keys")
