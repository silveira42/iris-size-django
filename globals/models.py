from django.db import models

# Create your models here.
class iGlobal(models.Model):
    database = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    allocatedsize = models.DecimalField()
    realsize = models.DecimalField()

    def __str__(self):
        return self.name

