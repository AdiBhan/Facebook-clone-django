from django.db import models
import csv
from datetime import datetime
# Create your models here.

class Result(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''
    # identification
    bib = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    ctz = models.TextField()
    city = models.TextField()
    state = models.TextField()
    # gender/division
    gender = models.CharField(max_length=6)
    division = models.CharField(max_length=6)
    # result place
    place_overall = models.IntegerField()
    place_gender = models.IntegerField()
    place_division = models.IntegerField()
    # timing-related
    start_time_of_day = models.TimeField()
    finish_time_of_day = models.TimeField()
    time_finish = models.TimeField()
    time_half1 = models.TimeField()
    time_half2 = models.TimeField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.city}, {self.state}), {self.time_finish}'
    
    
    def get_runners_passed(self):
        started_first = Result.objects.filter(start_time_of_day__lt=self.start_time_of_day)
        passed = started_first.filter(finish_time_of_day__gt=self.finish_time_of_day)
        print(f"Started first: {started_first.count()}, Passed: {len(passed)}")  # Debugging output
        return len(passed)

    def get_runners_passed_by(self):
        started_later = Result.objects.filter(start_time_of_day__gt=self.start_time_of_day)
        passed_by = started_later.filter(finish_time_of_day__lt=self.finish_time_of_day)
        print(f"Started later: {started_later.count()}, Passed by: {len(passed_by)}")  # Debugging output
        return len(passed_by)

def load_data():
    """Function to load data records from CSV file into Django model instances."""
    filename = "C:/Users/adity/Downloads/Fall2024/Django/2023_chicago_results.csv"

    def is_valid_time(value):
        """Helper function to check if a time string is in a valid format."""
        try:
            datetime.strptime(value, "%H:%M:%S")  # Check with seconds
            return True
        except ValueError:
            try:
                datetime.strptime(value, "%H:%M")  # Check without seconds
                return True
            except ValueError:
                return False  # Invalid format

    try:
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            
            for row in reader:
                if len(row) < 16:
                    print("Skipping row due to insufficient data:", row)
                    continue  # Skip rows with insufficient data

                # Skip row if any time fields are invalid
                if not (is_valid_time(row[13]) and is_valid_time(row[14]) and is_valid_time(row[15])):
                    print("Skipping row due to invalid time format:", row)
                    continue
                
                # Map row data to fields in the Result model
                result = Result(
                    bib=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    ctz=row[3],
                    city=row[4],
                    state=row[5],
                    gender=row[6],
                    division=row[7],
                    place_overall=row[8],
                    place_gender=row[9],
                    place_division=row[10],
                    start_time_of_day=row[11],
                    finish_time_of_day=row[12],
                    time_finish=row[13],
                    time_half1=row[14],
                    time_half2=row[15],
                )
                result.save()
                print(f"Created result for: {result.first_name} {result.last_name}")

    except Exception as e:
        print(f"Error loading data: {e}")