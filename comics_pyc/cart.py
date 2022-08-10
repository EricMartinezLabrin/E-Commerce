class CartProcessor:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('cart_number')
        if not carrito:
            self.session['cart_number'] = {}
            self.carrito = self.session['cart_number']
        else:
            self.carrito = carrito

    def add(self,product):
        id = str(product.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                'product_id': product.id,
                'name': product.name,
                'quantity': 1,
                'price': str(product.price),
                'image':product.image.url,
                'description': product.description
            }
        else:
            for key, value in self.carrito.items():
                if key == str(product.id):
                    value['quantity'] = value['quantity']+1
                    value['price'] = str(int(value['price'])+product.price)
                    self.save()
                    break
        self.save()

    def save(self):
        self.session['cart_number'] = self.carrito
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.carrito:
            del self.carrito[product_id]
            self.save()

    def decrement(self,product):
        for key, value in self.carrito.items():
            if key == str(product.id):
                value['quantity'] = value['quantity']-1
                value['price'] = str(int(value['price'])-product.price)
                if value['quantity']<1:
                    self.remove(product)
                else:
                    self.save()
                break
            else:
                print("El producto no existe en el carrito")

    def clear(self):
        self.session['cart_number']={}
        self.session.modified=True