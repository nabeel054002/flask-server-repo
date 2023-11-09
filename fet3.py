import requests

# Define the URL of the server and the route you want to access
url = "http://localhost:5000/update_entry"

# Data to send in the POST request
data = {
    "surname": "Khan",  # The surname to identify the entry to update
}

# Send a POST request to the server
response = requests.post(url, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response content, which should indicate if the entry was updated successfully
    print("Response from the server:")
    print(response.json())
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
