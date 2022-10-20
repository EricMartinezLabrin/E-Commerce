class Credentials():
    def mercadopago():
        production = 'APP_USR-1816279427628496-082518-c8be8dd4a4811a99d625a132abfe2554-113262566'
        sand = 'TEST-1816279427628496-082518-84255c0be73596985adaf2dccacaeee1-113262566'

        return production
    
    def notification_url():
        notification_url = 'http://descargas.tk:8000/adm/payment/mercadopago'
        # notification_url ='https://webhook.site/27f7ccb4-7a1d-4863-ace3-b13810b5f0b3'
        return notification_url

    def success_url():
        success = "http://descargas.tk:8000/checkout/successfully"
        return success
    
    def failure_url():
        failure = "http://descargas.tk:8000/checkout/failed"
        return failure

    def pending_url():
        pending = "http://descargas.tk:8000/checkout/pending"
        return pending