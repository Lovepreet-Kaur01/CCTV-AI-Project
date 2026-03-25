from django.db import models

class Detection(models.Model):
    object_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.object_name