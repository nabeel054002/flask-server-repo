import requests

# Define the URL of the server and the route
url = "http://localhost:5000/msg"

# Send a GET request to the server
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert the response content to a string
    response_text = response.text
    print("Response from the server:")
    print(response_text)
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
