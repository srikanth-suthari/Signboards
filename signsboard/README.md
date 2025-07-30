# Urban Services Website

A comprehensive Django-based urban services platform that provides contractor booking, fresh vegetable delivery, custom signboard services, and vehicle rental solutions.

## Features

### 🔧 Contractor Services
- Browse verified contractors by category (Plumbing, Electrical, Carpentry, Painting, Cleaning, Gardening)
- View contractor profiles with ratings, experience, and hourly rates
- Book contractors for projects with detailed project descriptions
- Track booking status and history

### 🥕 Vegetable Delivery
- Shop fresh vegetables by category
- Organic produce options available
- Shopping cart functionality
- Multiple delivery time slots
- Order tracking and history

### 🪧 ACP Signboard Services
- Custom signboard design and manufacturing
- Multiple materials: ACP, Acrylic, LED, Vinyl, Metal
- Various sizes and finishes available
- Installation services included
- Real-time price calculation
- Gallery of previous work

### 🚗 Vehicle Booking
- Multiple vehicle types: Sedan, SUV, Hatchback, Motorcycle, Mini Truck, Tempo
- Hourly, daily, one-way, round-trip, and airport transfer options
- Professional drivers available
- Real-time fare calculation
- GPS-enabled vehicles

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Forms**: Django Crispy Forms with Bootstrap 4 theme
- **File Handling**: Pillow for image processing

## Quick Start

1. **Clone and Setup**
   ```bash
   cd /Users/mahesh.suthari/Documents/signsboard
   source .venv/bin/activate
   ```

2. **Install Dependencies** (Already installed)
   ```bash
   pip install django pillow django-crispy-forms crispy-bootstrap4 django-widget-tweaks
   ```

3. **Run Migrations** (Already done)
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser** (Already created)
   ```bash
   python manage.py createsuperuser
   # Username: admin
   # Password: admin123
   ```

5. **Populate Sample Data** (Already done)
   ```bash
   python manage.py populate_data
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Website**
   - Main Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
signsboard/
├── urban_services/          # Main project settings
├── contractors/             # Contractor booking app
├── vegetables/              # Vegetable delivery app  
├── signboards/              # Signboard services app
├── vehicles/                # Vehicle booking app
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # User uploaded files
└── manage.py               # Django management script
```

## Key Models

### Contractors
- `ContractorCategory`: Service categories
- `Contractor`: Contractor profiles with ratings and rates
- `ContractorBooking`: Project booking requests
- `ContractorReview`: Customer reviews

### Vegetables
- `VegetableCategory`: Vegetable categories
- `Vegetable`: Product catalog with pricing
- `Cart` & `CartItem`: Shopping cart functionality
- `VegetableOrder` & `OrderItem`: Order management
- `DeliverySlot`: Available delivery windows

### Signboards
- `SignboardType`: Materials and pricing
- `SignboardSize`: Standard and custom sizes
- `SignboardFinish`: Surface treatments
- `SignboardOrder`: Custom orders with design specs
- `SignboardGallery`: Portfolio showcase

### Vehicles
- `VehicleType`: Vehicle categories with rates
- `Vehicle`: Fleet inventory
- `Driver`: Driver profiles and ratings
- `VehicleBooking`: Rental bookings
- `VehicleReview`: Service reviews

## Admin Features

Access the Django admin at `/admin/` to:
- Manage all service providers (contractors, vehicles, etc.)
- Process bookings and orders
- Update inventory and availability
- View customer feedback and reviews
- Generate reports

## User Features

### For Customers:
- Browse services without registration
- Create account to book services
- Track order/booking status
- Leave reviews and ratings
- Manage profile and history

### For Service Providers:
- Managed through admin interface
- Status updates and availability control
- Performance tracking
- Customer communication

## Sample Data

The website comes pre-populated with:
- 10 contractors across 6 categories
- 10 fresh vegetables across 6 categories
- 5 delivery time slots
- 5 signboard types with various sizes and finishes
- 6 vehicle types with 8 sample vehicles
- 5 professional drivers

## Security Features

- CSRF protection on all forms
- User authentication and authorization
- Input validation and sanitization
- Secure file upload handling
- Session management

## Responsive Design

- Mobile-first Bootstrap 5 design
- Responsive navigation and layouts
- Touch-friendly interfaces
- Optimized for all screen sizes

## Future Enhancements

- Payment gateway integration
- Real-time notifications
- GPS tracking for deliveries
- Multi-language support
- API for mobile apps
- Advanced analytics dashboard

## Contact Information

**Akshikha Signs**
- **Phone**: 9000666803
- **Email**: akshikhasignshyd@gmail.com  
- **Address**: Mallapur, Hyderabad

## Support

For questions or issues, contact us using the details above or check the Django documentation at https://docs.djangoproject.com/
