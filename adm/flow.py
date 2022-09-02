
from models import Order,Status
import requests
import mercadopago
import json
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

if status == 'approved':
    status_id = 2
elif status == 'pending':
    status_id = 1
elif status == 'authorized':
    status_id = 1
elif status == 'in_process':
    status_id = 7
elif status == 'in_mediation':
    status_id = 8
elif status == 'rejected':
    status_id = 5
elif status == 'cancelled':
    status_id = 9
elif status == 'refunded':
    status_id = 6
elif status == 'charged_back':
    status_id = 10

status_instance = Status.objects.get(pk=status)
order = Order.objects.get(pk=order_id)
print('El primer status es '+order.status.name)
order.status = status_instance
print('orden numero '+str(order.id))
print('El segundo status es '+order.status.name)
