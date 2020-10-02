import pytest
import boto3
import backend_lambda


def mock_firehose(name):
    class MockFireHoseClient():
        def put_record(self, DeliveryStreamName, Record):
            self.DeliveryStreamName = DeliveryStreamName,
            self.Record = Record
            return {
                "statusCode": 200,
                "message": "Data recorded in delivery stream"
            }

    return MockFireHoseClient()


def test_is_valid_json(nested_user_info):
    response = backend_lambda.is_valid_json(nested_user_info)
    assert response == True


def test_lambda_handler(nested_user_info):
    response = backend_lambda.lambda_handler({}, {})
    assert response.get("statusCode") == 400


def test_lambda_handler2(nested_user_info, monkeypatch):
    input_json = {"body": nested_user_info}
    monkeypatch.setattr(boto3, "client", mock_firehose)
    response = backend_lambda.lambda_handler(input_json, {})
    assert response.get("statusCode") == 200
