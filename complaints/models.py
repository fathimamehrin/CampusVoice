
from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ('Technical', 'Technical Issue'),
        ('Academic', 'Academic Issue'),
        ('Facilities', 'Facilities'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='complaints'
    )

    name = models.CharField(max_length=100)

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
