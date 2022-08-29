# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("TEST-1816279427628496-082518-84255c0be73596985adaf2dccacaeee1-113262566")


# Crea un ítem en la preferencia
preference_data = {
    "items": [
        {
            "title": "Mi producto",
            "quantity": 1,
            "unit_price": 75
        }
    ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]

