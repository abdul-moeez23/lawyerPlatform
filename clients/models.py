from django.db import models
from django.utils import timezone
from users.models import User, City, Court, SubCategory, FeeBand, Category
# from lawyers.models import LawyerProfile # Avoid circular import if possible, or use string reference

class Case(models.Model):
    """
    Represents a legal case or matter posted by a client.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('matched', 'Matched'),
        ('hired', 'Hired'),
        ('closed', 'Closed'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_cases')
    title = models.CharField(max_length=200, default="Untitled Case")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    court_level = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    fee_band = models.ForeignKey(FeeBand, on_delete=models.SET_NULL, null=True)
    
    urgency = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class CaseDocument(models.Model):
    """
    Documents uploaded by the client related to a specific case.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=150, blank=True)
    file = models.FileField(upload_to='case_docs/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or self.file.name


class Interaction(models.Model):
    """
    Tracks the relationship between a Case and a Lawyer (Matching/Hiring).
    """
    STATUS_CHOICES = (
        ('invited', 'Invited'),
        ('accepted', 'Accepted'), # Lawyer expressed interest
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='interactions')
    lawyer = models.ForeignKey('lawyers.LawyerProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='invited')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.lawyer} - {self.case.title} ({self.status})"


class Message(models.Model):
    """
    Secure communication between Client and Lawyer regarding a specific Case.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg from {self.sender} on {self.case.id}"


class Rating(models.Model):
    """
    Feedback provided by the client after a case is closed.
    """
    interaction = models.OneToOneField(Interaction, on_delete=models.CASCADE, related_name='rating')
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars} Stars for {self.interaction.lawyer}"