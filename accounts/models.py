from django.db import models
import json

class DynamicForm(models.Model):
    name = models.CharField(max_length=100)  # Name of the form
    configuration = models.TextField()  # Store JSON as a string

    def save(self, *args, **kwargs):
        if isinstance(self.configuration, dict):
            self.configuration = json.dumps(self.configuration)  # Convert dict to JSON string
        super().save(*args, **kwargs)

    def get_configuration(self):
        return json.loads(self.configuration)  # Convert JSON string back to dict

    def __str__(self):
        return self.name
