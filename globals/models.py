from django.db import models

# Create your models here.
class Global(models.Model):
    database = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    allocatedsize = models.DecimalField()
    size = models.DecimalField()

    def __str__(self):
        return name

