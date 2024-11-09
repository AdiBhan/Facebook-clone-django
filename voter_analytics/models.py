from django.db import models
from datetime import datetime
import csv
import os

class Voter(models.Model):
    #  Identity information
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    
    # Location fields
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    
    # General Information fields
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.IntegerField()
    
    # Voting history
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    # Voting score
    voter_score = models.IntegerField()

    def __str__(self):
        return (
            f"Voter ID: {self.id}, "
            f"Name: {self.first_name} {self.last_name}, "
            f"Address: {self.street_number} {self.street_name}, Apt {self.apartment_number or 'N/A'}, "
            f"Zip Code: {self.zip_code}, "
            f"DOB: {self.date_of_birth}, "
            f"Registration Date: {self.date_of_registration}, "
            f"Party: {self.party_affiliation}, "
            f"Precinct: {self.precinct_number}, "
            f"Voting History: [v20state: {self.v20state}, v21town: {self.v21town}, "
            f"v21primary: {self.v21primary}, v22general: {self.v22general}, v23town: {self.v23town}], "
            f"Score: {self.voter_score}"
        )

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "newton_voters.csv") 

    records_processed = 0
    records_skipped = 0

    with open(data_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                # Create a new Voter instance from the row data
                voter = Voter(
                    last_name=row.get('Last Name', '').strip(),
                    first_name=row.get('First Name', '').strip(),
                    street_number=row.get('Residential Address - Street Number', '').strip() or '',
                    street_name=row.get('Residential Address - Street Name', '').strip() or '',
                    apartment_number=row.get('Residential Address - Apartment Number', '').strip() if row.get('Residential Address - Apartment Number') else None,
                    zip_code=row.get('Residential Address - Zip Code', '').strip(),
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row.get('Party Affiliation', '').strip(),
                    precinct_number=int(row['Precinct Number']),
                    v20state=str(row.get('v20state', 'FALSE')).upper() == 'TRUE',
                    v21town=str(row.get('v21town', 'FALSE')).upper() == 'TRUE',
                    v21primary=str(row.get('v21primary', 'FALSE')).upper() == 'TRUE',
                    v22general=str(row.get('v22general', 'FALSE')).upper() == 'TRUE',
                    v23town=str(row.get('v23town', 'FALSE')).upper() == 'TRUE',
                    voter_score=int(row.get('voter_score', 0))
                )
                
                # Save the voter record to the database
                voter.save()
                records_processed += 1
                
                # Update every 1k records processed
                if records_processed % 1000 == 0:
                    print(f"Processed {records_processed} records...")
                    
            except Exception as e:
                records_skipped += 1
                print(f"\nError on record {records_skipped}:")
                print(f"Last Name: {row.get('Last Name', 'N/A')}")
                print(f"Error: {str(e)}")
                continue
                
    print(f"\nLoad completed:")
    print(f"Successfully processed: {records_processed} records")
    print(f"Skipped records: {records_skipped}")
    
    
