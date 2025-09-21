import requests

url = "https://domain-suggester-2.onrender.com/check_domain"

# JSON data to send
data = {
    "domain": "test.com"
}

# Make POST request
response = requests.post(url, json=data)

# Get the response as JSON
result = response.json()

print(result)