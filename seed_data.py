"""
Automated Database Seeder for NovaStore
CodeAlpha Web Development Internship Task 1: Simple E-Commerce Store (www.codealpha.tech)
"""

import os
import sys
import django
from decimal import Decimal

# Ensure utf-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, Order, OrderItem, UserProfile


def seed_database():
    print("🚀 Initializing NovaStore database seeding...")

    # 1. Create Superuser (Admin)
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@novastore.example', 'admin123')
        admin_user.first_name = 'Store'
        admin_user.last_name = 'Admin'
        admin_user.save()
        UserProfile.objects.get_or_create(user=admin_user, phone='+91 98765 00000', city='Hyderabad')
        print("✅ Superuser created: admin / admin123")
    else:
        print("ℹ️ Superuser 'admin' already exists.")

    # 2. Create Demo Customer
    if not User.objects.filter(username='customer').exists():
        cust_user = User.objects.create_user('customer', 'customer@example.com', 'customer123')
        cust_user.first_name = 'Harika'
        cust_user.last_name = 'Budamakayala'
        cust_user.save()
        UserProfile.objects.create(
            user=cust_user,
            phone='+91 98765 43210',
            address='Plot No. 42, Silicon Valley Colony',
            city='Hyderabad',
            state='Telangana',
            postal_code='500081'
        )
        print("✅ Demo customer created: customer / customer123")
    else:
        cust_user = User.objects.get(username='customer')
        print("ℹ️ Demo customer 'customer' already exists.")

    # 3. Create Categories
    categories_data = [
        {
            'name': 'Electronics',
            'slug': 'electronics',
            'description': 'Latest premium gadgets, noise-canceling headphones, smart watches, and PC gear.',
            'icon': 'bi-laptop'
        },
        {
            'name': 'Fashion & Apparel',
            'slug': 'fashion',
            'description': 'Modern casual apparel, denim wear, hoodies, and minimalist street footwear.',
            'icon': 'bi-bag'
        },
        {
            'name': 'Home & Lifestyle',
            'slug': 'home-lifestyle',
            'description': 'Ergonomic office accessories, modern drinkware, aroma diffusers, and desk lamps.',
            'icon': 'bi-house-heart'
        },
        {
            'name': 'Accessories & Gear',
            'slug': 'accessories',
            'description': 'Waterproof backpacks, slim RFID wallets, fast wireless chargers, and sunglasses.',
            'icon': 'bi-smartwatch'
        },
    ]

    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'icon': cat_data['icon']
            }
        )
        categories[cat_data['slug']] = cat
        print(f"📦 Category ready: {cat.name}")

    # 4. Products Data (16 realistic high-quality items)
    products_data = [
        # --- Electronics ---
        {
            'category': categories['electronics'],
            'name': 'Wireless Noise-Canceling Headphones Pro',
            'slug': 'wireless-noise-canceling-headphones-pro',
            'price': Decimal('149.99'),
            'discount_price': Decimal('119.99'),
            'stock': 25,
            'rating': Decimal('4.8'),
            'reviews_count': 64,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
            'description': 'Immerse yourself in rich, high-fidelity audio with active noise-cancellation (ANC), 40-hour battery life, and ultra-plush memory foam ear cups.',
            'details': 'Active Noise Cancellation (ANC) with transparency mode\n40 Hours Battery Life on a single charge\nBluetooth 5.3 with dual-device multi-point pairing\nBuilt-in quad microphones with AI voice clarity\nUSB-C Fast Charging (10 mins gives 4 hours playback)'
        },
        {
            'category': categories['electronics'],
            'name': 'Smart Watch Series X AMOLED',
            'slug': 'smart-watch-series-x-amoled',
            'price': Decimal('199.99'),
            'discount_price': Decimal('169.99'),
            'stock': 18,
            'rating': Decimal('4.7'),
            'reviews_count': 42,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
            'description': 'Feature-packed smartwatch with 1.43" Always-On AMOLED screen, comprehensive health metrics, 100+ sports tracking modes, and 5ATM water resistance.',
            'details': '1.43-inch Always-on vibrant AMOLED display\n24/7 Heart rate, SpO2 blood oxygen, and sleep monitoring\n5ATM Water Resistance (up to 50 meters)\nUp to 14 days of typical battery life\nBluetooth Calling & smartphone notifications'
        },
        {
            'category': categories['electronics'],
            'name': 'Ultra HD 4K Action Camera 60FPS',
            'slug': 'ultra-hd-4k-action-camera-60fps',
            'price': Decimal('129.50'),
            'discount_price': None,
            'stock': 12,
            'rating': Decimal('4.6'),
            'reviews_count': 29,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&auto=format&fit=crop&q=80',
            'description': 'Capture thrilling adventures in razor-sharp 4K at 60FPS. Features electronic image stabilization, 170-degree ultra-wide lens, and waterproof housing.',
            'details': 'Native 4K video recording at 60 FPS\nAdvanced 6-Axis Electronic Image Stabilization (EIS)\nWaterproof up to 40m with included case\nDual touchscreen displays (front and rear)\nWiFi connectivity for instant phone transfer'
        },
        {
            'category': categories['electronics'],
            'name': 'RGB Mechanical Gaming Keyboard',
            'slug': 'rgb-mechanical-gaming-keyboard',
            'price': Decimal('89.99'),
            'discount_price': Decimal('69.99'),
            'stock': 20,
            'rating': Decimal('4.9'),
            'reviews_count': 53,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
            'description': 'High-performance hot-swappable mechanical keyboard with custom linear switches, per-key RGB backlighting, and aircraft-grade aluminum top plate.',
            'details': 'Hot-swappable custom linear red switches\nPer-key dynamic RGB backlighting with 18 lighting modes\nPBT double-shot keycaps with zero fading\nDetachable braided Type-C cable\nDedicated volume roller and multimedia keys'
        },

        # --- Fashion & Apparel ---
        {
            'category': categories['fashion'],
            'name': 'Classic Vintage Washed Denim Jacket',
            'slug': 'classic-vintage-washed-denim-jacket',
            'price': Decimal('79.99'),
            'discount_price': Decimal('59.99'),
            'stock': 15,
            'rating': Decimal('4.7'),
            'reviews_count': 38,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800&auto=format&fit=crop&q=80',
            'description': 'Timeless premium denim jacket tailored from 100% heavyweight cotton. Vintage wash finish, button-flap chest pockets, and relaxed comfortable fit.',
            'details': '100% Rigid Heavyweight Cotton Denim\nClassic fit designed for versatile layering\nBrass shank buttons and reinforced double stitching\nDual side slant welt pockets and button flap chest pockets\nMachine washable and preshrunk'
        },
        {
            'category': categories['fashion'],
            'name': 'Premium Heavyweight Cotton Hoodie',
            'slug': 'premium-heavyweight-cotton-hoodie',
            'price': Decimal('64.00'),
            'discount_price': Decimal('49.00'),
            'stock': 30,
            'rating': Decimal('4.8'),
            'reviews_count': 72,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80',
            'description': 'Cozy 400 GSM brushed fleece hoodie crafted for ultimate warmth and comfort. Double-layered hood, kangaroo pocket, and ribbed cuffs.',
            'details': '400 GSM Ultra-Soft Brushed Fleece\n80% Combed Cotton, 20% Polyester blend\nDouble-layered generous hood with matching drawstrings\nReinforced kangaroo pocket\nPre-washed to minimize shrinkage'
        },
        {
            'category': categories['fashion'],
            'name': 'Minimalist White Leather Sneakers',
            'slug': 'minimalist-white-leather-sneakers',
            'price': Decimal('95.00'),
            'discount_price': Decimal('79.00'),
            'stock': 14,
            'rating': Decimal('4.6'),
            'reviews_count': 41,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80',
            'description': 'Handcrafted low-top sneakers in clean white full-grain leather. Cushioned memory foam insoles and durable vulcanized rubber soles.',
            'details': 'Full-grain Italian calf leather upper\nErgonomic memory foam footbed with arch support\nAnti-slip durable rubber cupsole\nBreathable microfiber interior lining\nIncludes spare waxed cotton laces'
        },
        {
            'category': categories['fashion'],
            'name': 'Classic Polarized Aviator Sunglasses',
            'slug': 'classic-polarized-aviator-sunglasses',
            'price': Decimal('45.00'),
            'discount_price': None,
            'stock': 22,
            'rating': Decimal('4.5'),
            'reviews_count': 19,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=80',
            'description': 'Iconic aviator teardrop design with lightweight alloy frame, silicone nose pads, and 100% UV400 polarized scratch-resistant lenses.',
            'details': '100% UV400 Protection (Blocks UVA/UVB rays)\nTAC 9-layer Polarized Anti-Glare lenses\nLightweight stainless steel frame\nAdjustable soft medical-grade silicone nose pads\nIncludes hard clamshell travel case and microfiber cloth'
        },

        # --- Home & Lifestyle ---
        {
            'category': categories['home-lifestyle'],
            'name': 'Ultrasonic Aroma Essential Oil Diffuser',
            'slug': 'ultrasonic-aroma-essential-oil-diffuser',
            'price': Decimal('38.99'),
            'discount_price': Decimal('29.99'),
            'stock': 20,
            'rating': Decimal('4.8'),
            'reviews_count': 45,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&auto=format&fit=crop&q=80',
            'description': 'Elevate your living space with silent ultrasonic mist diffusion. 500ml capacity, 7 ambient LED colors, and automatic waterless shutoff.',
            'details': '500ml large water capacity (runs up to 12 hours)\nWhisper-quiet ultrasonic technology (<23dB)\n7 soothing ambient LED mood light modes\n4 Timer settings: 1H / 3H / 6H / Continuous\nAutomatic waterless shut-off safety protection'
        },
        {
            'category': categories['home-lifestyle'],
            'name': 'Stainless Steel Thermal Tumbler 750ml',
            'slug': 'stainless-steel-thermal-tumbler-750ml',
            'price': Decimal('28.50'),
            'discount_price': None,
            'stock': 35,
            'rating': Decimal('4.9'),
            'reviews_count': 88,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80',
            'description': 'Vacuum insulated double-wall tumbler keeping drinks icy cold for 24 hours or steaming hot for 12 hours. Sweat-proof powder coating.',
            'details': 'Double-wall vacuum insulation technology\n18/8 Pro-Grade food-grade stainless steel\nKeeps cold for 24 hours, hot for 12 hours\n100% Leak-proof sip lid with silicone gasket\nBPA-free and dishwasher safe'
        },
        {
            'category': categories['home-lifestyle'],
            'name': 'Ergonomic Dimmable LED Desk Lamp',
            'slug': 'ergonomic-dimmable-led-desk-lamp',
            'price': Decimal('49.99'),
            'discount_price': Decimal('39.99'),
            'stock': 16,
            'rating': Decimal('4.6'),
            'reviews_count': 33,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1534349762230-e0cadf78f5da?w=800&auto=format&fit=crop&q=80',
            'description': 'Modern eye-caring task light with touch slider controls, 5 color temperature modes, 10 brightness steps, and built-in USB charging port.',
            'details': 'Flicker-free eye-protection diffuse LED panel\n5 Color Temperatures (2700K to 6500K)\n10 Smooth touch brightness levels\nIntegrated USB-A charging port (5V/1A)\nMulti-angle flexible folding arm and swivel head'
        },
        {
            'category': categories['home-lifestyle'],
            'name': 'Artisan Matte Ceramic Coffee Mug Set',
            'slug': 'artisan-matte-ceramic-coffee-mug-set',
            'price': Decimal('32.00'),
            'discount_price': Decimal('24.00'),
            'stock': 24,
            'rating': Decimal('4.7'),
            'reviews_count': 27,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80',
            'description': 'Set of 4 handcrafted stoneware ceramic coffee mugs with comfortable ergonomic handles and tactile organic matte glaze.',
            'details': 'Set of 4 mugs (350ml / 12oz each)\nHigh-fire durable stoneware ceramic\nMicrowave and dishwasher safe\nLead-free and food-safe matte mineral glaze\nGift-ready protective recycled packaging'
        },

        # --- Accessories & Gear ---
        {
            'category': categories['accessories'],
            'name': 'Waterproof Travel Laptop Backpack 25L',
            'slug': 'waterproof-travel-laptop-backpack-25l',
            'price': Decimal('85.00'),
            'discount_price': Decimal('64.99'),
            'stock': 19,
            'rating': Decimal('4.9'),
            'reviews_count': 91,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=80',
            'description': 'Sleek commuting and travel backpack engineered with waterproof Oxford fabric, padded 16" laptop sleeve, and hidden anti-theft pocket.',
            'details': 'Padded shockproof compartment for up to 16-inch laptops\nWaterproof high-density 900D Oxford fabric\nExternal USB charging pass-through port\nHidden anti-theft passport pocket on rear back panel\nBreathable honeycomb padded mesh shoulder straps'
        },
        {
            'category': categories['accessories'],
            'name': 'Minimalist RFID Slim Leather Wallet',
            'slug': 'minimalist-rfid-slim-leather-wallet',
            'price': Decimal('34.99'),
            'discount_price': Decimal('24.99'),
            'stock': 40,
            'rating': Decimal('4.7'),
            'reviews_count': 58,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&auto=format&fit=crop&q=80',
            'description': 'Ultra-compact front-pocket wallet made with genuine top-grain leather. Quick-access card ejection slot and RFID skimming protection.',
            'details': 'Top-grain vegetable-tanned genuine leather\nRigorously tested RFID-blocking inner lining (13.56 MHz)\nHolds 8-10 cards plus folded cash bill clip\nQuick thumb slider notch for rapid card access\nUltra-slim 0.3-inch profile'
        },
        {
            'category': categories['accessories'],
            'name': 'Fast Wireless Charging Pad 15W',
            'slug': 'fast-wireless-charging-pad-15w',
            'price': Decimal('29.99'),
            'discount_price': Decimal('19.99'),
            'stock': 28,
            'rating': Decimal('4.6'),
            'reviews_count': 36,
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1586816879360-004f5b0c51e3?w=800&auto=format&fit=crop&q=80',
            'description': 'Qi-certified fast wireless charging base with aircraft aluminum heat dissipation body, anti-slip silicone ring, and LED charging status.',
            'details': 'Up to 15W Qi-certified high-speed wireless output\nCompatible with iPhone, Samsung Galaxy, and AirPods\nAircraft aluminum base for optimal heat dissipation\nIntelligent temperature control and over-voltage safety\nIncludes 1.2m premium nylon braided Type-C cable'
        },
        {
            'category': categories['accessories'],
            'name': 'Compact Power Bank 20000mAh PD 30W',
            'slug': 'compact-power-bank-20000mah-pd-30w',
            'price': Decimal('49.99'),
            'discount_price': None,
            'stock': 25,
            'rating': Decimal('4.8'),
            'reviews_count': 63,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&auto=format&fit=crop&q=80',
            'description': 'High-density lithium polymer external battery with 30W USB-C Power Delivery. Charges modern phones up to 5 times on a single charge.',
            'details': '20,000mAh high-density airline-safe capacity\n30W USB-C Power Delivery 3.0 & Quick Charge 4.0\nCharges iPhone 15 from 0 to 60% in 30 minutes\nDigital LED battery percentage display\nTriple output ports to charge 3 devices at once'
        },
    ]

    for pdata in products_data:
        p, created = Product.objects.get_or_create(
            slug=pdata['slug'],
            defaults=pdata
        )
        if created:
            print(f"✨ Created product: {p.name} (${p.get_effective_price()})")
        else:
            print(f"ℹ️ Product already exists: {p.name}")

    # 5. Create a Sample Past Order for Demo Customer
    if not Order.objects.filter(user=cust_user).exists():
        sample_prod1 = Product.objects.get(slug='wireless-noise-canceling-headphones-pro')
        sample_prod2 = Product.objects.get(slug='classic-vintage-washed-denim-jacket')

        order = Order.objects.create(
            user=cust_user,
            order_number='ORD-ALPHA778',
            first_name='Harika',
            last_name='Budamakayala',
            email='customer@example.com',
            phone='+91 98765 43210',
            address_line1='Plot No. 42, Silicon Valley Colony',
            address_line2='Near Tech Hub',
            city='Hyderabad',
            state='Telangana',
            postal_code='500081',
            country='India',
            payment_method='card',
            payment_status='Paid',
            status='Confirmed',
            subtotal=sample_prod1.get_effective_price() + sample_prod2.get_effective_price(),
            tax=Decimal('9.00'),
            shipping_cost=Decimal('0.00'),
            total_amount=sample_prod1.get_effective_price() + sample_prod2.get_effective_price() + Decimal('9.00'),
            order_notes='CodeAlpha Project 1 demonstration order.'
        )

        OrderItem.objects.create(
            order=order,
            product=sample_prod1,
            product_name=sample_prod1.name,
            price=sample_prod1.get_effective_price(),
            quantity=1
        )
        OrderItem.objects.create(
            order=order,
            product=sample_prod2,
            product_name=sample_prod2.name,
            price=sample_prod2.get_effective_price(),
            quantity=1
        )
        print("🎉 Created sample demo order: #ORD-ALPHA778 for customer 'customer'")

    print("✅ NovaStore database seeding completed successfully!")


if __name__ == '__main__':
    seed_database()
