import pytest


@pytest.fixture
def nested_user_info():
    return [{
        "name": {
            "first_name": "John",
            "middle_name": "M.",
            "last_name": "Doe"
        },
        "address": {
            "city": "Boston",
            "zip_code": "02169",
            "phone": "6171234567"
        }
    }, {
        "name": {
            "first_name": "Alice",
            "middle_name": "M.",
            "last_name": "Bob"
        },
        "address": {
            "city": "New York",
            "zip_code": "04321",
            "phone": "987654321"
        }
    }]
