import requests

url = "https://apis-dev.pgf.cl/trxs"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers)

print(response.text)