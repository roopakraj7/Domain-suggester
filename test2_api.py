import requests

url = "https://domain-suggester-2.onrender.com/check_domain?domain=test.com"

res = requests.get(url, json)

print(res.json())
