from django.db import models

from main.models.project import Project


class Contract(models.Model):
    STATUS_CHOICES = (
        ("Draft", "Draft"),
        ("Active", "Active"),
        ("Completed", "Completed"),
    )
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    signed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
