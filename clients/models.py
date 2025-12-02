from django.db import models

# Create your models here.
from users.models import User

class CaseDetails(models.Model):
    URGENCY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    case_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    case_category = models.CharField(max_length=100)
    court_level = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Medium')
    language = models.CharField(max_length=50, null=True, blank=True)
    case_description = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_category} by {self.client.full_name}"