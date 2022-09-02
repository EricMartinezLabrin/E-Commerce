class Credentials():
    def mercadopago():
        production = ''
        sand = 'TEST-1816279427628496-082518-84255c0be73596985adaf2dccacaeee1-113262566'

        return sand
    
    def notification_url():
        notification_url = 'http://descargas.tk:8000/adm/payment/mercadopago'
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