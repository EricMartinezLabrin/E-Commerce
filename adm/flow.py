import requests
import mercadopago
import json
from adm.models import Order,Status
# from adm.models import Order, Status
    
url = "https://api.mercadopago.com/v1/payments/1307988079"

payload={}
headers = {
  'Authorization': 'Bearer TEST-1816279427628496-082518-84255c0be73596985adaf2dccacaeee1-113262566'
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
order_id = response['external_reference']
status = response['status']
print('id= '+order_id)
print('status= '+status)
print('-----------------')

status_instance = Status.objects.get(pk=status_id)
order = Order.objects.get(pk=order_id)
print('El primer status es '+order.status.name)
order.status = status_instance
print('orden numero '+str(order.id))
print('El segundo status es '+order.status.name)
