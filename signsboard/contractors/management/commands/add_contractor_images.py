from django.core.management.base import BaseCommand
from contractors.models import Contractor
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Add profile images to contractors'

    def handle(self, *args, **options):
        contractors = Contractor.objects.all()
        
        # Sample professional images for contractors
        contractor_images = {
            'Sharif Khan': 'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'Santhosh Suthari': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        }
        
        for contractor in contractors:
            if contractor.name in contractor_images and not contractor.profile_image:
                try:
                    image_url = contractor_images[contractor.name]
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_content = ContentFile(response.content)
                        contractor.profile_image.save(
                            f'{contractor.name.lower().replace(" ", "_")}.jpg',
                            image_content,
                            save=True
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'Added image for {contractor.name}')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to add image for {contractor.name}: {str(e)}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Finished adding contractor images!')
        )
