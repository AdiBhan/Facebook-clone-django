from django.core.management.base import BaseCommand
from django.core.files import File
from project.models import Pet, Shelter  # Replace 'your_app' with your actual app name
import random
import os

class Command(BaseCommand):
    help = 'Creates 30 sample pets'

    def handle(self, *args, **kwargs):
        # Sample data for pet generation
        dog_breeds = [
            "Labrador Retriever", "German Shepherd", "Golden Retriever", 
            "French Bulldog", "Bulldog", "Poodle", "Beagle", 
            "Rottweiler", "Dachshund", "Yorkshire Terrier",
            "Siberian Husky", "Great Dane", "Doberman", "Shih Tzu"
        ]

        cat_breeds = [
            "Persian", "Maine Coon", "Siamese", "British Shorthair",
            "Ragdoll", "Bengal", "American Shorthair", "Sphynx",
            "Scottish Fold", "Russian Blue", "Norwegian Forest Cat"
        ]

        other_breeds = [
            "Rabbit - Dutch", "Hamster - Syrian", "Guinea Pig - American",
            "Ferret - Sable", "Rabbit - Lionhead", "Guinea Pig - Peruvian",
            "Hamster - Dwarf", "Rabbit - Mini Lop", "Ferret - Albino"
        ]

        pet_names = [
            "Luna", "Bella", "Charlie", "Lucy", "Max", "Bailey", "Cooper",
            "Daisy", "Sadie", "Molly", "Buddy", "Rocky", "Bear", "Leo",
            "Duke", "Zeus", "Bentley", "Milo", "Jack", "Lola", "Ruby",
            "Winston", "Oliver", "Pepper", "Shadow", "Sophie", "Tucker",
            "Murphy", "Oscar", "Sam"
        ]

        addresses = [
            "123 Maple Street", "456 Oak Avenue", "789 Pine Road",
            "321 Cedar Lane", "654 Elm Boulevard", "987 Birch Drive",
            "147 Willow Way", "258 Sycamore Street", "369 Chestnut Avenue",
            "159 Magnolia Road"
        ]

        # Get all shelters (assuming you have some created)
        shelters = list(Shelter.objects.all())
        if not shelters:
            self.stdout.write(self.style.ERROR('No shelters found. Please create shelters first.'))
            return

        # Create 30 pets
        for i in range(30):
            # Randomly choose pet type and associated breeds
            pet_type = random.choice(['DOG', 'CAT', 'OTHER'])
            if pet_type == 'DOG':
                breed = random.choice(dog_breeds)
                description = f"A lovable {breed} looking for a forever home. "
            elif pet_type == 'CAT':
                breed = random.choice(cat_breeds)
                description = f"A charming {breed} cat with a wonderful personality. "
            else:
                breed = random.choice(other_breeds)
                description = f"An adorable {breed} that will make a great pet. "

            # Add more details to description
            description += random.choice([
                "Great with kids and other pets!",
                "Perfect for a quiet home.",
                "Loves to play and exercise.",
                "Very well-behaved and trained.",
                "Friendly and sociable with everyone.",
                "Would make a perfect companion.",
                "Loves attention and cuddles!",
                "Has a gentle and calm demeanor.",
                "Energetic and full of personality.",
                "Smart and easily trainable."
            ])

            # Create the pet
            pet = Pet.objects.create(
                name=random.choice(pet_names),
                age=random.randint(1, 12),  # Age between 1-12 years
                address=random.choice(addresses),
                breed=breed,
                shelter=random.choice(shelters),
                pet_type=pet_type,
                description=description,
                # Note: Image field will need to be handled separately
                # For now, we'll leave it empty or you can add default images
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created pet: {pet.name} ({pet.breed})'))

        self.stdout.write(self.style.SUCCESS('Successfully created 30 sample pets'))

        # Note about images
        self.stdout.write(self.style.WARNING(
            'Note: Pet images were not generated. You will need to manually add images '
            'or modify the script to include default images from a specified directory.'
        ))