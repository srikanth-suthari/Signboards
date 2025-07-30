from django.core.management.base import BaseCommand
from contractors.models import Contractor, ContractorCategory

class Command(BaseCommand):
    help = 'Update contractors with new data'

    def handle(self, *args, **options):
        # Clear existing contractors
        self.stdout.write('Clearing existing contractors...')
        Contractor.objects.all().delete()
        
        # Get or create categories
        plumber_category, _ = ContractorCategory.objects.get_or_create(
            name='Plumber',
            defaults={'description': 'Plumbing services and repairs'}
        )
        
        electrician_category, _ = ContractorCategory.objects.get_or_create(
            name='Electrician',
            defaults={'description': 'Electrical services and repairs'}
        )
        
        # Add new contractors
        contractors_data = [
            {
                'name': 'Sharif Khan',
                'email': 'sharif.khan@email.com',
                'phone': '88888555554',
                'address': 'Hyderabad',
                'category': plumber_category,
                'description': 'Experienced plumber with 10+ years in residential and commercial plumbing.',
                'experience_years': 10,
                'hourly_rate': 500.00,
                'is_verified': True,
                'rating': 5
            },
            {
                'name': 'Santhosh Suthari',
                'email': 'santhosh.suthari@email.com',
                'phone': '9550775500',
                'address': 'Hyderabad',
                'category': electrician_category,
                'description': 'Professional electrician specializing in home electrical systems and repairs.',
                'experience_years': 8,
                'hourly_rate': 600.00,
                'is_verified': True,
                'rating': 5
            }
        ]
        
        for contractor_data in contractors_data:
            contractor = Contractor.objects.create(**contractor_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created contractor: {contractor.name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully updated contractors!')
        )
