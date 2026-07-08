# ORBIT — Mobile Shop (Django)

A mobile phone e-commerce site with a dark "device glow" aesthetic: a tilting
3D phone hero, magnetic hover cards, scroll reveals, animated cart badge,
floating-label forms, and more — all built with vanilla CSS/JS (no frontend
framework or build step required) on top of Django.

## Features

- Home page with animated hero (cursor-tracked 3D tilt on a CSS phone mockup),
  animated stat counters, category grid, featured products, new arrivals rail.
- Full shop listing with category/brand/price filters, search, and sorting.
- Product detail page with quantity stepper, specs grid, related products.
- Session-based cart (add/update/remove) with a bouncing badge indicator.
- Checkout flow that creates a real `Order`/`OrderItem` in the database.
- Contact form that saves messages to the database.
- Django admin wired up for Category, Product, Order, ContactMessage.
- Scroll-reveal animations, magnetic tilt cards, toast notifications, page
  loader, and reduced-motion support — all in `shop/static/shop/css/style.css`
  and `shop/static/shop/js/main.js`.

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed sample products (12 phones/accessories across 4 categories)
python manage.py seed_data

# 5. (Optional) Create an admin user
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Then visit **http://127.0.0.1:8000/** for the storefront and
**http://127.0.0.1:8000/admin/** to manage products.

## Project structure

```
mobileshop/
├── manage.py
├── requirements.txt
├── config/                  # Django project settings/urls
└── shop/                    # Main app
    ├── models.py             # Category, Product, Order, OrderItem, ContactMessage
    ├── views.py               # Home, shop list/filter, detail, cart, checkout, contact
    ├── cart.py                 # Session-based cart helper class
    ├── admin.py
    ├── templatetags/shop_extras.py   # `inr` currency filter
    ├── management/commands/seed_data.py
    ├── templates/shop/*.html
    └── static/shop/css/style.css, static/shop/js/main.js
```

## Customizing

- **Add real product photos**: `Product.photo` is an `ImageField`. Upload a
  photo per product from the Django admin (`/admin/` → Products → open a
  product → Photo field). Once a product has a photo, it automatically shows
  that image everywhere instead of the CSS phone mockup — home hero, product
  cards, product detail, cart, and related items all check `{% if product.photo %}`
  and fall back gracefully if it's empty. Recommended: a clean product shot on
  a transparent or dark background, roughly 3:5 aspect ratio (e.g. 600×1000px),
  saved as PNG or JPG.
- **Colors/fonts**: everything is driven by CSS custom properties at the top
  of `style.css` (`:root { --bg, --accent, --accent-2, ... }`).
- **More products**: edit the `PRODUCTS` list in
  `shop/management/commands/seed_data.py` and re-run `python manage.py seed_data`
  (it's safe to run repeatedly — it upserts by slug).

## Notes

This was built and syntax-checked in a sandbox without Django installed or
network access, so while every Python file compiles cleanly and every template
tag is balanced, you should run it locally end-to-end (`python manage.py runserver`)
before deploying, in case any small issue surfaces that only Django's own
template/URL resolution would catch.
