from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contractors.models import ContractorCategory, Contractor
from vegetables.models import VegetableCategory, Vegetable, DeliverySlot
from signboards.models import SignboardType, SignboardSize, SignboardFinish
from vehicles.models import VehicleType, Vehicle, Driver
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create contractor categories
        contractor_categories = [
            ('Plumbing', 'Water supply, drainage, and pipe repairs'),
            ('Electrical', 'Electrical installations and repairs'),
            ('Carpentry', 'Furniture making and wood work'),
            ('Painting', 'Interior and exterior painting'),
            ('Cleaning', 'House and office cleaning services'),
            ('Gardening', 'Landscaping and garden maintenance'),
        ]
        
        for name, desc in contractor_categories:
            ContractorCategory.objects.get_or_create(name=name, defaults={'description': desc})
        
        # Create sample contractors
        categories = ContractorCategory.objects.all()
        contractor_names = [
            'Rajesh Kumar', 'Amit Singh', 'Priya Sharma', 'Suresh Patel', 'Meera Joshi',
            'Deepak Gupta', 'Kavita Reddy', 'Vinod Yadav', 'Sunita Verma', 'Ravi Tiwari'
        ]
        
        for i, name in enumerate(contractor_names):
            if not Contractor.objects.filter(name=name).exists():
                Contractor.objects.create(
                    name=name,
                    email=f'{name.lower().replace(" ", ".")}@example.com',
                    phone=f'98765{43210 + i}',
                    address=f'{i+1}23 Main Street, Mumbai',
                    category=random.choice(categories),
                    description=f'Experienced {random.choice(categories).name.lower()} contractor with quality workmanship.',
                    experience_years=random.randint(2, 15),
                    hourly_rate=Decimal(str(random.randint(200, 800))),
                    is_verified=random.choice([True, False]),
                    rating=random.randint(3, 5),
                    total_projects=random.randint(5, 50)
                )
        
        # Create vegetable categories
        veg_categories = [
            ('Leafy Greens', 'Spinach, lettuce, kale, etc.'),
            ('Root Vegetables', 'Carrots, radish, beetroot, etc.'),
            ('Fruits', 'Tomatoes, cucumbers, bell peppers, etc.'),
            ('Onions & Garlic', 'Different varieties of onions and garlic'),
            ('Beans & Peas', 'Green beans, peas, etc.'),
            ('Herbs', 'Coriander, mint, curry leaves, etc.'),
        ]
        
        for name, desc in veg_categories:
            VegetableCategory.objects.get_or_create(name=name, defaults={'description': desc})
        
        # Create vegetables
        veg_data = [
            ('Spinach', 'Leafy Greens', 30, 'kg'), ('Carrots', 'Root Vegetables', 40, 'kg'),
            ('Tomatoes', 'Fruits', 25, 'kg'), ('Onions', 'Onions & Garlic', 35, 'kg'),
            ('Green Beans', 'Beans & Peas', 60, 'kg'), ('Coriander', 'Herbs', 15, 'bunch'),
            ('Lettuce', 'Leafy Greens', 50, 'piece'), ('Beetroot', 'Root Vegetables', 45, 'kg'),
            ('Bell Peppers', 'Fruits', 80, 'kg'), ('Garlic', 'Onions & Garlic', 120, 'kg'),
        ]
        
        veg_categories_dict = {cat.name: cat for cat in VegetableCategory.objects.all()}
        
        for name, cat_name, price, unit in veg_data:
            if not Vegetable.objects.filter(name=name).exists():
                Vegetable.objects.create(
                    name=name,
                    category=veg_categories_dict[cat_name],
                    price_per_unit=Decimal(str(price)),
                    unit=unit,
                    is_organic=random.choice([True, False]),
                    stock_quantity=random.randint(10, 100),
                    description=f'Fresh {name.lower()} delivered from local farms.'
                )
        
        # Create delivery slots
        slots = ['6:00 AM - 9:00 AM', '9:00 AM - 12:00 PM', '12:00 PM - 3:00 PM', 
                '3:00 PM - 6:00 PM', '6:00 PM - 9:00 PM']
        
        for slot in slots:
            DeliverySlot.objects.get_or_create(slot_time=slot, defaults={'max_orders': 50})
        
        # Create signboard types
        signboard_types = [
            ('ACP Signboard', 'Aluminum Composite Panel', 150),
            ('Acrylic Signboard', 'Acrylic', 200),
            ('LED Signboard', 'LED Display', 500),
            ('Vinyl Banner', 'Vinyl', 50),
            ('Metal Signboard', 'Stainless Steel', 300),
        ]
        
        for name, material, price in signboard_types:
            SignboardType.objects.get_or_create(
                name=name, 
                defaults={
                    'material': material, 
                    'price_per_sqft': Decimal(str(price)),
                    'description': f'High quality {material.lower()} signboard'
                }
            )
        
        # Create signboard sizes
        sizes = [
            ('2x3 feet', 2, 3), ('3x4 feet', 3, 4), ('4x6 feet', 4, 6),
            ('6x8 feet', 6, 8), ('8x10 feet', 8, 10), ('Custom Size', 0, 0)
        ]
        
        for name, width, height in sizes:
            SignboardSize.objects.get_or_create(
                name=name,
                defaults={'width_feet': Decimal(str(width)), 'height_feet': Decimal(str(height))}
            )
        
        # Create signboard finishes
        finishes = [
            ('Matte Finish', 'Non-reflective matte coating', 10),
            ('Glossy Finish', 'High-gloss reflective coating', 15),
            ('UV Protection', 'UV resistant coating', 20),
            ('Anti-scratch', 'Scratch resistant surface', 25),
        ]
        
        for name, desc, cost in finishes:
            SignboardFinish.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'additional_cost_percentage': Decimal(str(cost))}
            )
        
        # Create vehicle types
        vehicle_types = [
            ('Sedan', '4-5 passengers', 12, 8),
            ('SUV', '6-7 passengers', 15, 10),
            ('Hatchback', '4 passengers', 10, 6),
            ('Motorcycle', '2 passengers', 5, 3),
            ('Mini Truck', '2 tons cargo', 20, 15),
            ('Tempo', '1 ton cargo', 18, 12),
        ]
        
        for name, capacity, rate_hour, rate_km in vehicle_types:
            VehicleType.objects.get_or_create(
                name=name,
                defaults={
                    'capacity': capacity,
                    'base_rate_per_hour': Decimal(str(rate_hour)),
                    'base_rate_per_km': Decimal(str(rate_km)),
                    'description': f'{name} for {capacity}'
                }
            )
        
        # Create vehicles
        vehicle_models = [
            'Maruti Suzuki Swift', 'Hyundai i20', 'Honda City', 'Toyota Innova',
            'Mahindra Scorpio', 'Tata Ace', 'Bajaj Pulsar', 'Honda Activa'
        ]
        
        vehicle_types_obj = VehicleType.objects.all()
        fuel_choices = ['petrol', 'diesel', 'cng']
        
        for i, model in enumerate(vehicle_models):
            if not Vehicle.objects.filter(make_model=model).exists():
                Vehicle.objects.create(
                    vehicle_type=random.choice(vehicle_types_obj),
                    make_model=model,
                    year=random.randint(2018, 2024),
                    license_plate=f'MH01AB{1000 + i}',
                    fuel_type=random.choice(fuel_choices),
                    seating_capacity=random.randint(2, 7),
                    insurance_valid_until='2025-12-31',
                    pollution_certificate_valid_until='2025-06-30',
                    current_location=f'Zone {i+1}, Mumbai'
                )
        
        # Create drivers
        driver_names = [
            'Sunil Kumar', 'Ramesh Singh', 'Mahesh Patel', 'Vijay Sharma', 'Raju Yadav'
        ]
        
        for i, name in enumerate(driver_names):
            if not Driver.objects.filter(name=name).exists():
                Driver.objects.create(
                    name=name,
                    phone=f'98765{54321 + i}',
                    license_number=f'MH{2020 + i}0{100 + i}',
                    license_expiry='2027-12-31',
                    experience_years=random.randint(3, 20),
                    rating=Decimal(str(random.uniform(4.0, 5.0))).quantize(Decimal('0.01')),
                    languages_spoken='Hindi, English, Marathi'
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
