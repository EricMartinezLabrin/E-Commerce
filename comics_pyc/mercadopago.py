
#  SDK de Mercado Pago
import mercadopago

class MercadoPagoPayment():
    def __init__(self):
        pass
    def payment(title,quantity,unit_price):
        # Agrega credenciales
        sdk = mercadopago.SDK("TEST-1816279427628496-082518-84255c0be73596985adaf2dccacaeee1-113262566")


        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": title,
                    "quantity": quantity,
                    "unit_price": unit_price
                }
            ]
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return preference

