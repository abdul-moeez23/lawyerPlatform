
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField
# from django.core.validators import MinValueValidator, MaxValueValidator
# from users.models import User, City, Court, SubCategory, FeeBand, Language

# class Case(models.Model):
#     STATUS_CHOICES = (
#         ('draft', 'Draft'),
#         ('submitted', 'Submitted'),
#         ('matched', 'Matched'),
#         ('shortlisted', 'Shortlisted'),
#         ('hired', 'Hired'),
#         ('closed', 'Closed'),
#     )

#     client = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
#     court_level = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True)
#     city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
#     fee_band = models.ForeignKey(FeeBand, on_delete=models.SET_NULL, null=True)
    
#     urgency = models.CharField(max_length=50)
#     language_preference = models.CharField(max_length=50)
#     description = models.TextField()

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
#     created_at = models.DateTimeField(default=timezone.now)

#     embedding = ArrayField(models.FloatField(), blank=True, null=True)

#     def __str__(self):
#         return f"Case {self.id} - {self.client.username}"


# class CaseDocument(models.Model):
#     case = models.ForeignKey(Case, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='case_docs/')
#     uploaded_at = models.DateTimeField(default=timezone.now)


# # =========================
# # MATCHING RESULTS (Fit Score + Reasons)
# # =========================


# class Interaction(models.Model):
#     STATUS_CHOICES = (
#         ('invited', 'Invited'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#         ('hired', 'Hired'),
#     )

#     case = models.ForeignKey(Case, on_delete=models.CASCADE)
#     lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     created_at = models.DateTimeField(default=timezone.now)


# # =========================
# # OPTIONAL FEEDBACK
# # =========================

# class Rating(models.Model):
#     interaction = models.OneToOneField(Interaction, on_delete=models.CASCADE)
#     stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comments = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(default=timezone.now)