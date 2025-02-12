import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from establecimiento.models import Establecimiento, ImagenEstablecimiento
from PIL import Image
from io import BytesIO

class Command(BaseCommand):
    help = 'Assign random images to establishments from available images'

    def handle(self, *args, **kwargs):
        # Path where images are stored locally
        images_folder = 'establecimiento/imagenes_prueba/'

        # Get a list of image filenames
        image_filenames = [f for f in os.listdir(images_folder) if f.endswith('.png')]

        # Select establishments to assign images
        establecimientos = Establecimiento.objects.all()

        # Loop through each establishment and assign 1-5 random images
        for establecimiento in establecimientos:
            # Pick 1 to 5 random images from the available images
            selected_images = random.sample(image_filenames, random.randint(1, 5))
            
            for image_filename in selected_images:
                # Read image and prepare for upload to S3
                image_path = os.path.join(images_folder, image_filename)
                with open(image_path, 'rb') as image_file:
                    image = Image.open(image_file)
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    buffer.seek(0)

                    # Create an ImagenEstablecimiento object and upload to S3
                    img_instance = ImagenEstablecimiento(establecimiento=establecimiento)
                    img_instance.imagen.save(image_filename, buffer, save=False)
                    img_instance.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully assigned images to {establecimiento.nombre}'))

