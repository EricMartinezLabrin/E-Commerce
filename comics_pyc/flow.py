import hmac
import hashlib
import requests

#SIGN FLOW APP

apikey = '7F47221F-5168-4221-BD0B-23LB681C7D66'
currency = 'CLP'
amount = '5000'
secret_key = '1834669a8ec20935942fc3ff0ccc71930cc93da6'

params = {'apikey':apikey,'amount':amount,'currency':currency}

to_sign = ""
for key,value in params.items():
    to_sign = to_sign+str(key+value)
h = hmac.new(to_sign,hashlib.sha256)
signature = h.secret_key #hmac('sha256',to_sign,secret_key)
    

#POST METHOD
url = 'https://httpbin.org/post'#https://sandbox.flow.cl/api'
#Add url of service to use
url = url+'/payment/create'
#add signature to the paramenters
params['s'] = signature

response = requests.post(url,data=params)
response_text = response.text

print(response_text)