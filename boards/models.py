from django.db import models
from django.contrib.auth.models import User
from accounts.models import Regions

class Board(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='boards')
    seats = models.IntegerField(null=True, blank=True)
    from_region = models.CharField(max_length=2, choices=Regions, null=True, blank=True)
    from_city = models.CharField(max_length=50, null=True, blank=True)
    to_region = models.CharField(max_length=2, choices=Regions, null=True, blank=True)
    to_city = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.driver}"