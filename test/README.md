A small test case for testing the following:

- Requests with an empty body
- Requests with malformed JSON
- Requests with proper JSON formatting but missing one of the *'first_name'*, *'middle_name'*, *'last_name'* or *'zip_code'* keys
- Requests with different JSON formats

BEFORE RUNNING THE TEST CASES UPDATE THE URL WITH THE ONE RETURNED BY RUNNING 
```
Terraform apply
```
IN THE TERMINAL
