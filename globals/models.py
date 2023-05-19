from django.db import models

# Create your models here.
class iGlobal(models.Model):
    database = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    allocatedsize = models.FloatField()
    realsize = models.FloatField()

    def __str__(self):
        return self.name

