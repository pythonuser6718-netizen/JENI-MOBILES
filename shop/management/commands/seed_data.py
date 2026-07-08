from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product


CATEGORIES = [
    ('Flagship', 'flagship', 'bolt'),
    ('Foldables', 'foldables', 'layers'),
    ('Budget', 'budget', 'wallet'),
    ('Accessories', 'accessories', 'headphones'),
]

PRODUCTS = [
    dict(category='flagship', brand='Nova', name='Nova X12 Pro', price=74999, discount_price=68999,
         ram='12GB', storage='256GB', display='6.7" LTPO AMOLED, 120Hz', battery='5000mAh, 65W fast charge',
         camera='50MP triple camera w/ periscope zoom', color='Obsidian Black', hue=200, rating=4.8,
         is_featured=True, is_new=True,
         tagline='Precision engineered. Impossibly fast.',
         description='The Nova X12 Pro pairs a titanium frame with our fastest imaging chip yet, built for people who never miss the shot.'),
    dict(category='flagship', brand='Zenith', name='Zenith S9 Ultra', price=82999, discount_price=None,
         ram='16GB', storage='512GB', display='6.8" QHD+ Dynamic AMOLED, 144Hz', battery='5500mAh, 80W fast charge',
         camera='108MP quad camera w/ 10x optical zoom', color='Cosmic Violet', hue=265, rating=4.9,
         is_featured=True, is_new=True,
         tagline='Ultra display. Ultra everything.',
         description='A cinema-grade display and a camera system tuned for low light make the S9 Ultra the flagship for creators.'),
    dict(category='foldables', brand='Zenith', name='Zenith Fold 4', price=124999, discount_price=114999,
         ram='16GB', storage='512GB', display='7.6" foldable AMOLED + 6.2" cover', battery='4800mAh',
         camera='50MP triple camera', color='Sage Green', hue=150, rating=4.6,
         is_featured=True, is_new=False,
         tagline='One phone. Two worlds.',
         description='Unfold a full tablet-sized canvas for multitasking, then fold it back to a pocket-ready flagship.'),
    dict(category='foldables', brand='Nova', name='Nova Flip Air', price=64999, discount_price=None,
         ram='8GB', storage='256GB', display='6.7" foldable AMOLED + 3.4" cover', battery='4000mAh',
         camera='12MP dual flash camera', color='Coral Pink', hue=15, rating=4.4,
         is_featured=False, is_new=True,
         tagline='Compact by design.',
         description='A featherweight flip phone with a cover screen big enough to run your whole day without opening it.'),
    dict(category='budget', brand='Pulse', name='Pulse Lite 5G', price=16999, discount_price=13999,
         ram='6GB', storage='128GB', display='6.5" IPS LCD, 90Hz', battery='5000mAh, 33W charge',
         camera='48MP dual camera', color='Ocean Blue', hue=210, rating=4.2,
         is_featured=True, is_new=False,
         tagline='All the essentials. None of the excess.',
         description='5G speed, all-day battery and a clean interface — the Pulse Lite is built for real everyday use.'),
    dict(category='budget', brand='Aria', name='Aria Go 4', price=11999, discount_price=None,
         ram='4GB', storage='64GB', display='6.4" HD+ LCD, 60Hz', battery='4500mAh',
         camera='13MP single camera', color='Slate Grey', hue=220, rating=3.9,
         is_featured=False, is_new=False,
         tagline='Reliable. Affordable. Ready.',
         description='A dependable first smartphone or backup device, without cutting corners on battery life.'),
    dict(category='budget', brand='Pulse', name='Pulse Nano', price=9999, discount_price=8499,
         ram='4GB', storage='64GB', display='6.1" HD+ LCD', battery='4200mAh',
         camera='16MP dual camera', color='Mint', hue=160, rating=4.0,
         is_featured=False, is_new=True,
         tagline='Small phone. Big value.',
         description='Compact, light, and priced for everyone — the Pulse Nano keeps you connected without compromise.'),
    dict(category='flagship', brand='Aria', name='Aria Prime 8', price=54999, discount_price=49999,
         ram='12GB', storage='256GB', display='6.5" AMOLED, 120Hz', battery='4600mAh, 45W charge',
         camera='64MP triple camera', color='Midnight Blue', hue=230, rating=4.5,
         is_featured=True, is_new=False,
         tagline='Flagship feel, honest price.',
         description='Aria Prime brings flagship-grade cameras and displays down to a price that still makes sense.'),
    dict(category='accessories', brand='Nova', name='Nova Buds Pro', price=8999, discount_price=6999,
         ram='-', storage='-', display='-', battery='30hrs with case',
         camera='-', color='Pearl White', hue=190, rating=4.6,
         is_featured=False, is_new=True,
         tagline='Silence, on demand.',
         description='Active noise cancellation and spatial audio in a case that fits in your smallest pocket.'),
    dict(category='accessories', brand='Zenith', name='Zenith Watch S', price=15999, discount_price=None,
         ram='-', storage='-', display='1.5" AMOLED', battery='5 days',
         camera='-', color='Graphite', hue=205, rating=4.4,
         is_featured=False, is_new=True,
         tagline='Time, tracked beautifully.',
         description='Round-the-clock health tracking wrapped in a display sharp enough for daylight readability.'),
    dict(category='accessories', brand='Pulse', name='Pulse Fast Charger 65W', price=1999, discount_price=1499,
         ram='-', storage='-', display='-', battery='65W GaN output',
         camera='-', color='White', hue=40, rating=4.3,
         is_featured=False, is_new=False,
         tagline='Full charge, short coffee break.',
         description='A pocket-sized GaN charger that brings any of our phones from empty to full in under an hour.'),
    dict(category='flagship', brand='Pulse', name='Pulse Edge 7', price=45999, discount_price=None,
         ram='8GB', storage='128GB', display='6.4" AMOLED, 90Hz', battery='4500mAh',
         camera='50MP dual camera', color='Steel Grey', hue=195, rating=4.3,
         is_featured=False, is_new=True,
         tagline='Sharp edges. Sharper price.',
         description='A balanced flagship-lite with a curved display and a camera tuned for portraits.'),
]


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **options):
        cat_map = {}
        for name, slug, icon in CATEGORIES:
            cat, _ = Category.objects.update_or_create(
                slug=slug, defaults={'name': name, 'icon': icon}
            )
            cat_map[slug] = cat
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(cat_map)} categories'))

        count = 0
        for p in PRODUCTS:
            slug = slugify(f"{p['brand']}-{p['name']}")
            Product.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    category=cat_map[p['category']],
                    brand=p['brand'],
                    name=p['name'],
                    tagline=p['tagline'],
                    description=p['description'],
                    price=p['price'],
                    discount_price=p['discount_price'],
                    ram=p['ram'], storage=p['storage'], display=p['display'],
                    battery=p['battery'], camera=p['camera'], color=p['color'],
                    hue=p['hue'], rating=p['rating'],
                    is_featured=p['is_featured'], is_new=p['is_new'],
                    stock=30,
                )
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {count} products'))
