import boto3
import json
import pytest
import base64
from moto import mock_s3

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from src import transformer_lambda

keys = ["first_name", "middle_name", "last_name", "zip_code"]


@pytest.fixture
def kinesis_user_data(nested_user_info):
    user_data = {"records": []}
    id_increment = 0
    for record in nested_user_info:
        data = {
            "recordId": id_increment,
            "data": base64.b64encode(json.dumps(record).encode("utf-8"))
        }
        user_data["records"].append(data)
        id_increment += 1
    return user_data


def test_parse(nested_user_info):
    for record in nested_user_info:
        parsed = transformer_lambda.parse(keys, record, {})
        user_info = record["name"]
        user_info["zip_code"] = record["address"]["zip_code"]
        assert user_info == parsed


@mock_s3
def test_lambda_handler(kinesis_user_data):
    s3_client = boto3.client('s3')
    test_bucket_name = transformer_lambda.DESTINATION_BUCKET_NAME

    s3_client.create_bucket(Bucket=test_bucket_name)
    response = transformer_lambda.lambda_handler(kinesis_user_data, {})

    for record in response['records']:
        assert record["recordId"] in range(len(kinesis_user_data["records"]))
