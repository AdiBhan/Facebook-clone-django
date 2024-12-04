from django.core.management.base import BaseCommand
from project.models import Pet  # Replace 'yourapp' with your actual app name

class Command(BaseCommand):
    help = 'Updates pet image URLs based on pet type'

    def handle(self, *args, **kwargs):
        # Dictionary of pet type to list of possible image URLs - expanded for more unique images
        pet_images = {
            'DOG': [
                "https://images.pexels.com/photos/1805164/pexels-photo-1805164.jpeg",
                "https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg",
                "https://images.pexels.com/photos/1490908/pexels-photo-1490908.jpeg",
                "https://images.pexels.com/photos/3361739/pexels-photo-3361739.jpeg",
                "https://images.pexels.com/photos/2607544/pexels-photo-2607544.jpeg",
                "https://images.pexels.com/photos/58997/pexels-photo-58997.jpeg",
                "https://images.pexels.com/photos/825947/pexels-photo-825947.jpeg",
                "https://images.pexels.com/photos/1870301/pexels-photo-1870301.jpeg",
                "https://images.pexels.com/photos/2023384/pexels-photo-2023384.jpeg",
                "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg",
                "https://images.pexels.com/photos/1254140/pexels-photo-1254140.jpeg",
                "https://images.pexels.com/photos/2679612/pexels-photo-2679612.jpeg",
                "https://images.pexels.com/photos/3196887/pexels-photo-3196887.jpeg",
                "https://images.pexels.com/photos/4587998/pexels-photo-4587998.jpeg",
                "https://images.pexels.com/photos/4587971/pexels-photo-4587971.jpeg",
                "https://images.pexels.com/photos/4587993/pexels-photo-4587993.jpeg",
                "https://images.pexels.com/photos/3715583/pexels-photo-3715583.jpeg",
                "https://images.pexels.com/photos/4668425/pexels-photo-4668425.jpeg",
                "https://images.pexels.com/photos/4588435/pexels-photo-4588435.jpeg"
            ],
            'CAT': [
                "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg",
                "https://images.pexels.com/photos/1056251/pexels-photo-1056251.jpeg",
                "https://images.pexels.com/photos/320014/pexels-photo-320014.jpeg",
                "https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg",
                "https://images.pexels.com/photos/96938/pexels-photo-96938.jpeg",
                "https://images.pexels.com/photos/127028/pexels-photo-127028.jpeg",
                "https://images.pexels.com/photos/774731/pexels-photo-774731.jpeg",
                "https://images.pexels.com/photos/1543793/pexels-photo-1543793.jpeg"
            ],
            'OTHER': [
                "https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg"  # rabbit
            ]
        }

        # Update dogs (19 images)
        dogs = Pet.objects.filter(pet_type='DOG')
        for index, dog in enumerate(dogs):
            if index < len(pet_images['DOG']):
                dog.image_url = pet_images['DOG'][index]
                dog.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated image for dog {dog.name} with image {index + 1}'
                    )
                )

        # Update cats (8 images)
        cats = Pet.objects.filter(pet_type='CAT')
        for index, cat in enumerate(cats):
            if index < len(pet_images['CAT']):
                cat.image_url = pet_images['CAT'][index]
                cat.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated image for cat {cat.name} with image {index + 1}'
                    )
                )

        # Update other pets (1 image)
        other_pets = Pet.objects.filter(pet_type='OTHER')
        for pet in other_pets:
            pet.image_url = pet_images['OTHER'][0]
            pet.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated image for other pet {pet.name} with image'
                )
            )

        total_updated = dogs.count() + cats.count() + other_pets.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {total_updated} pets with new image URLs'
            )
        )