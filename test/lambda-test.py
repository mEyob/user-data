# import boto3
# import json
# from datetime import datetime

# data = {
#     "Hello World": []
# }
# now = datetime.now().strftime("%Y-%m-%d")

# s3 = boto3.resource('s3')
# # s3.create_bucket(Bucket='my-test-bucket1822')
# obj = s3.Object('my-bucket', now + '/hello.json')
# obj.put(Body=json.dumps(data))


def parse(keys, data_dict, new_dict):
    for key, value in data_dict.items():
        if key in keys:
            new_dict[key] = value
        if isinstance(value, dict):
            parse(keys, value, new_dict)
    return new_dict


keys = ['first_name', 'last_name', 'zip_code']
s = {
    'first_name': 'Misikir',
    'middle_name': 'ME',
    'last_name': 'Eyob',
    'address': {
        'zip_code': '02169',
        'city': 'Boston'
    }
}
print(parse(keys, s, {}))
