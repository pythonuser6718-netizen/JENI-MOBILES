from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Category, Product, ContactMessage, Order, OrderItem
from .cart import Cart


def home(request):
    featured = Product.objects.filter(is_featured=True)[:4]
    new_arrivals = Product.objects.filter(is_new=True)[:8]
    categories = Category.objects.all()
    hero_product = featured.first() or Product.objects.first()
    context = {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'hero_product': hero_product,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    products = Product.objects.select_related('category')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    brand = request.GET.get('brand')
    max_price = request.GET.get('max_price')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand:
        products = products.filter(brand=brand)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__icontains=query) | Q(description__icontains=query)
        )
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    brands = Product.objects.values_list('brand', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'active_category': category_slug,
        'active_brand': brand,
        'active_sort': sort,
        'query': query or '',
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    context = {'product': product, 'related': related}
    return render(request, 'shop/product_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(product, quantity)
    messages.success(request, f'{product.name} added to cart.')
    next_url = request.POST.get('next') or 'shop:cart_detail'
    return redirect(next_url)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.set_quantity(product, quantity)
    return redirect('shop:cart_detail')


@require_POST
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.info(request, f'{product.name} removed from cart.')
    return redirect('shop:cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop:product_list')

    if request.method == 'POST':
        order = Order.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            pincode=request.POST.get('pincode'),
            total=cart.get_total(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                quantity=item['quantity'],
                price=item['product'].current_price,
            )
        cart.clear()
        return redirect('shop:order_success', order_id=order.id)

    return render(request, 'shop/checkout.html', {'cart': cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, "Message sent! We'll get back to you soon.")
        return redirect('shop:contact')
    return render(request, 'shop/contact.html')
