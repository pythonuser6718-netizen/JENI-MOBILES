from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=40, default='phone', help_text="Keyword for inline SVG icon")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=60)
    tagline = models.CharField(max_length=140, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    ram = models.CharField(max_length=20, blank=True)
    storage = models.CharField(max_length=20, blank=True)
    display = models.CharField(max_length=60, blank=True)
    battery = models.CharField(max_length=40, blank=True)
    camera = models.CharField(max_length=60, blank=True)
    color = models.CharField(max_length=40, default='Graphite')

    hue = models.PositiveSmallIntegerField(default=200, help_text="0-360, drives the CSS phone glow color")
    photo = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Optional. If left empty, the animated CSS phone mockup is shown instead.")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    stock = models.PositiveIntegerField(default=25)

    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.name}"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price > 0:
            return round((1 - (self.discount_price / self.price)) * 100)
        return 0

    @property
    def specs(self):
        return [
            ('RAM', self.ram), ('Storage', self.storage), ('Display', self.display),
            ('Battery', self.battery), ('Camera', self.camera), ('Color', self.color),
        ]


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    pincode = models.CharField(max_length=12)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity
