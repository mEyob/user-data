import requests
import random

names = [
    "Boyd", "Jayde", "Brinley", "Boyd", "Blake", "Michael", 
    "Boykin", "Alona", "Mackenzie", "Boyle", "Mitchell", 
    "Carson", "Boyle", "Tyler", "Owen", "Brant", "Wayne", 
    "Logan", "Brantwein", "Brooke", "Chelsea", "Brashear", 
    "Erin", "Isabella", "Braun", "Louise", "Sienna",
    "Bravo", "Anthony", "Richard", "Breeden", "Noel", 
    "Alahya"
]

zip_codes = [
    "01234", "01269", "04592", "02131", "03421", 
    "01234", "92341", "02192", "91021", "34210",
    "04321"
]

nested_user_info = [
    {
        "name" : {
            "first_name": "John",
            "middle_name": "M.",
            "last_name": "Doe"
        },
        "address" : {
            "city": "Boston",
            "zip_code": "02169",
            "phone": "6171234567"
        }
    },
    {
        "name" : {
            "first_name": "Alice",
            "middle_name": "M.",
            "last_name": "Bob"
        },
        "address" : {
            "city": "New York",
            "zip_code": "04321",
            "phone": "987654321"
        }
    }

]

def green(s):
    return '\033[1;32m%s\033[m\n' % s

def red(s):
    return '\033[1;31m%s\033[m\n' % s

def send_request(URL, user_info, verbose=False):
    if verbose:
        print("\n-----------------------------------------------------------------")
        print("Sending request with the following URL\n")
        print(URL)
        print("\nIn case of Errors, Make sure you are using the base URL returned")
        print("by Terraform deployment")
        print("-----------------------------------------------------------------\n")
    return requests.post(
        URL,
        json=user_info
        )

def simple_request(URL, num_of_requests):
    responses = []
    for _ in range(num_of_requests):
        first_name, middle_name, last_name = [
            random.choice(names) for _ in range(3)
        ]
        zip_code = random.choice(zip_codes)
        user_info = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "zip_code": zip_code
        }
        req = send_request(URL, user_info)
        responses.append(req.status_code)
    success = sum([1 for response in responses if int(response) == 200 ])
    return success / len(responses)

def nested_request(URL):
    responses = []
    for user_info in nested_user_info:
        req = send_request(URL, user_info)
        responses.append(req.status_code)
    success = sum([1 for response in responses if int(response) == 200 ])
    return success / len(responses)

def check(obj1, obj2):
    if obj1 == obj2:
        print(green("PASS"))
    else:
        print(red("FAIL"))


def main(num_of_requests=10):
    URL = input("Enter API Gateway URL:\n")
    print("\nTESTING WITH AN EMPTY REQUEST...")
    response = send_request(URL, user_info=None, verbose=True)
    expected = "Empty request"
    actual = response.content.decode('utf-8')
    print("Expected output: {}".format(expected))
    print("Actual output  : {}".format(actual))
    check(expected, actual)

    print("TESTING A REQUEST WITH MALFORMED JSON...")
    response = send_request(URL, user_info='{"first_name": "Test, "last_name": "Test"}')
    expected = "Malformed JSON"
    actual = response.content.decode('utf-8')
    print("Expected output: {}".format(expected))
    print("Actual output  : {}".format(actual))
    check(expected, actual)

    print("TESTING A REQUEST WITH MISSING NAME OR ZIPCODE JSON KEYS...")
    response = send_request(URL, user_info={"first_name": "Test", "last_name": "Test"})
    expected = "JSON missing required keys"
    actual = response.content.decode('utf-8')
    print("Expected output: {}".format(expected))
    print("Actual output  : {}".format(actual))
    check(expected, actual)

    print("TESTING WITH USER INFO IN FLAT JSON FORMAT...")
    print("Number of requests {}".format(num_of_requests))
    success_rate = int(simple_request(URL, num_of_requests) * 100)
    print("{}% requests returned with status code 200\n".format(success_rate))

    print("TESTING WITH USER INFO IN NESTED JSON FORMAT...")
    print("Number of requests {}".format(len(nested_user_info)))
    success_rate = int(nested_request(URL) * 100)
    print("{}% requests returned with status code 200\n".format(success_rate))
    print("Check S3 bucket after a time period equal to")
    print("Firehose's buffer interval has passed to validate created rows")

if __name__ == "__main__":
    main()
