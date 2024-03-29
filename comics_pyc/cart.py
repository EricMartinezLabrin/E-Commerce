class CartProcessor:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('cart_number')
        carrito_total = self.session.get('cart_total')
        carrito_cantidad = self.session.get('cart_quantity')
        if not carrito:
            self.session['cart_number'] = {}
            self.carrito = self.session['cart_number']
            self.session['cart_total']=0
            self.carrito_total = self.session['cart_total']
            self.session['cart_quantity']=0
            self.carrito_cantidad = self.session['cart_quantity']
        else:
            self.carrito = carrito
            self.carrito_total = carrito_total
            self.carrito_cantidad = carrito_cantidad

    def add(self,product):
        id = str(product.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                'product_id': int(product.id),
                'name': product.name,
                'quantity': 1,
                'price': int(product.price),
                'image':product.image.url,
                'description': product.description
            }
            self.carrito_total= int(self.carrito_total) + int(product.price)
            self.carrito_cantidad=int(self.carrito_cantidad)+1
        else:
            for key, value in self.carrito.items():
                if key == str(product.id):
                    value['quantity'] = value['quantity']+1
                    value['price'] = value['price']+product.price
                    self.carrito_total=int(self.carrito_total) + int(product.price)
                    self.carrito_cantidad=int(self.carrito_cantidad)+1
                    self.save()
                    break
        self.save()

    def save(self):
        self.session['cart_number'] = self.carrito
        self.session['cart_total'] = self.carrito_total
        self.session['cart_quantity'] = self.carrito_cantidad
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.id)
        for key, value in self.carrito.items():
            if key == str(product.id):
                subtotal = value['price']
                quantity = value['quantity']
                break
        if product_id in self.carrito:
            self.carrito_total = self.carrito_total-subtotal
            self.carrito_cantidad = self.carrito_cantidad-quantity
            del self.carrito[product_id]
            self.save()

    def decrement(self,product):
        for key, value in self.carrito.items():
            if key == str(product.id):
                value['quantity'] = value['quantity']-1
                value['price'] = int(value['price'])-product.price
                self.carrito_total = self.carrito_total - product.price
                self.carrito_cantidad = self.carrito_cantidad -1
                if value['quantity']<1:
                    self.remove(product)
                else:
                    self.save()
                break
            else:
                print("El producto no existe en el carrito")

    def clear(self):
        self.session['cart_number']={}
        self.session['cart_total'] = 0
        self.session['cart_quantity'] = 0
        self.session.modified=True
