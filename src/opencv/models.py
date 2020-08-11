from django.db import models

# Create your models here.


class Image(models.Model):
    name = models.CharField(max_length=100)
    src = models.FileField(upload_to='image/', blank=True, null=True)

    def __str__(self):
        return self.name