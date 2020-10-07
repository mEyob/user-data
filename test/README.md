Scripts for unit and integration tests

Two unit test scripts are included for testing the backend and 
transformer lambda functions

A simple integration test is also included for testing the following:

- Requests with an empty body
- Requests with malformed JSON
- Requests with proper JSON formatting but missing one of the *'first_name'*, *'middle_name'*, *'last_name'* or *'zip_code'* keys
- Requests with different JSON formats