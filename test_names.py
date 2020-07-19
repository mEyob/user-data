import requests
import random

names = [
    "Boyd", "Jayde", "Brinley", "Boyd", "Blake", "Michael", "Boykin", "Alona",
    "Mackenzie", "Boyle", "Mitchell", "Carson"
    "Boyle", "Tyler", "Owen", "Brant", "Wayne", "Logan", "Brantwein", "Brooke",
    "Chelsea", "Brashear", "Erin", "Isabella", "Braun", "Louise", "Sienna",
    "Bravo", "Anthony", "Richard", "Breeden", "Noel", "Alahya"
]

zip_codes = [
    "01234", "01269"
    "04592", "02131", "03421", "01234", "92341", "02192", "91021", "34210",
    "04321"
]


def main(num_of_requests=10):
    for _ in range(num_of_requests):
        first_name, middle_name, last_name = [
            random.choice(names) for _ in range(3)
        ]
        zip_code = random.choice(zip_codes)
        data = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "zip_code": zip_code
        }
        r = requests.post(
            'https://w16a2rrwma.execute-api.us-east-1.amazonaws.com/production/messages',
            json=data)
        print(r.status_code)


main(100)
