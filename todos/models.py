# todos/models.py
from django.db import models
from django.conf import settings
import uuid


class Todo(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        # Add any other status options we may need
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id"
    )
    title = models.CharField(max_length=200)
    target_date = models.DateField(null=True, blank=True)
    is_priority = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "todos"  # This ensures the table name in the database matches your specification
