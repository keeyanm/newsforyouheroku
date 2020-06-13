from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class feed(models.Model):
    feed = models.CharField(max_length=128)
    area = models.CharField(max_length=64, default='None')
    def __str__(self):
        return self.feed

class sector(models.Model):
    sector = models.CharField(max_length=64)
    def __str__(self):
        return self.sector
        
class preference(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, null=True)
    sectors = models.ManyToManyField(sector)
    def __str__(self):
        x = str(self.sectors.all())
        return f"{self.user} - {x.replace('<QuerySet','').replace('[','').replace(']','').replace('>','').replace('<','').replace('sector:','')}"

