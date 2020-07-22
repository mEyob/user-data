import base64
import boto3
import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Change bucket name as needed
DESTINATION_BUCKET_NAME = "processed-user-data-bucket-1822"


def parse(keys, data_dict, new_dict):
    """
    Exhuastively search a possibly nested 'data_dict' and 
    retrieve values associated with a key in 'keys'. Store 
    these key-value pairs in new_dict.
    :param keys: a list of keys to search for
    :param data_dict: a dictionary to be searched
    :param new_dict: a dictionary for storing matching key, values
    """
    for key, value in data_dict.items():
        if key in keys:
            new_dict[key] = value
        if isinstance(value, dict):
            parse(keys, value, new_dict)
    return new_dict


def make_output(recordId, result, data):
    return {'recordId': recordId, 'result': result, 'data': data}


def lambda_handler(event, context):
    keys = ["first_name", "middle_name", "last_name", "zip_code"]
    output = []
    payload = []

    for record in event["records"]:
        clean_data = {}
        data = base64.b64decode(record["data"])
        data = json.loads(data)
        if isinstance(data, str):
            data = json.loads(data)
        try:
            clean_data = parse(keys, data, {})
        except Exception as ex:
            logging.error(str(ex))
        if clean_data:
            payload.append(clean_data)
        output_record = make_output(record['recordId'], 'Dropped',
                                    record["data"])
        output.append(output_record)

    total = "Total number of records = {}".format(len(event["records"]))
    success = "Successfully processed records = {}.".format(len(payload))
    logger.info(total)
    logger.info(success)

    if len(payload) > 0:
        payload = '\n'.join(json.dumps(item) for item in payload)

        now = datetime.utcnow().strftime("%Y/%m/%d/%H/%M")
        s3 = boto3.resource("s3")
        obj = s3.Object(DESTINATION_BUCKET_NAME, now + ".json")
        obj.put(Body=payload)

    return {'records': output}
