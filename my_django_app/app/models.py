from django.db import models

class File(models.Model):
    subdir = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.subdir}/{self.filename}"