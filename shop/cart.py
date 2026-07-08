from decimal import Decimal
from .models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def set_quantity(self, product, quantity):
        product_id = str(product.id)
        if quantity <= 0:
            self.remove(product)
            return
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}
        for product_id, item in self.cart.items():
            product = products_map.get(product_id)
            if not product:
                continue
            yield {
                'product': product,
                'quantity': item['quantity'],
                'subtotal': product.current_price * item['quantity'],
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total(self):
        total = Decimal('0')
        for item in self:
            total += item['subtotal']
        return total
