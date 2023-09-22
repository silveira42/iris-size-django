from django.db import models

# Create your models here.
class iGlobal(models.Model):
    database = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    tablename  = models.CharField(max_length=100, default="")
    allocatedsize = models.FloatField()
    realsize = models.FloatField()

    def __str__(self):
        return self.name

