from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentSurvey(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Survey Information
    date_of_survey = models.DateField(auto_now_add=True)
    
    # Liked most about the university (multiple choice)
    liked_students = models.BooleanField(default=False)
    liked_location = models.BooleanField(default=False)
    liked_campus = models.BooleanField(default=False)
    liked_atmosphere = models.BooleanField(default=False)
    liked_dorm_rooms = models.BooleanField(default=False)
    liked_sports = models.BooleanField(default=False)
    
    # Interest source
    INTEREST_CHOICES = [
        ('friends', 'Friends'),
        ('television', 'Television'),
        ('internet', 'Internet'),
        ('other', 'Other'),
    ]
    interest_source = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    
    # Likelihood of recommendation
    recommendation_likelihood = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    # Comments
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.date_of_survey}"