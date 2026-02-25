from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from uuid import uuid4

class Roles(models.TextChoices):
    PASSENGER = 'P', 'Passanger'
    DRIVER = 'D', 'Driver'
    ADMIN = 'A', 'Admin'

class Regions(models.TextChoices):
    ANDIJON = "AN", "Andijon"
    BUXORO = "BU", "Buxoro"
    JIZZAX = "JI", "Jizzax"
    QASHQADARYO = "QA", "Qashqadaryo"
    NAVOIY = "NA", "Navoiy"
    NAMANGAN = "NM", "Namangan"
    SAMARQAND = "SA", "Samarqand"
    SURXONDARYO = "SU", "Surxondaryo"
    SIRDARYO = "SI", "Sirdaryo"
    TOSHKENT = "TO", "Toshkent"
    FARGONA = "FE", "Farg'ona"
    XORAZM = "XO", "Xorazm"
    QORAQALPOGISTON = "QR", "Qoraqalpog'iston"

class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_profile')
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=10, null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)
    role = models.CharField(max_length=1, choices=Roles, default=Roles.PASSENGER)
    phone = models.CharField(max_length=15, null=True, blank=True)
    region = models.CharField(max_length=2, choices=Regions, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.username or self.telegram_id}"
    
class Car(models.Model):
    class Types(models.TextChoices):
        SEDAN = 'SN', 'Sedan'
        CROSSOVER = 'CS', 'Crossover'
        MINIVAN = 'MV', 'Minivan'
        MICROBUS = 'MB', 'Micro bus / Gazel'
        BUS = 'BS', 'Avtobus'

    driver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='car')
    model = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    seats = models.IntegerField(null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    photo_url = models.ImageField(upload_to='cars/', null=True, blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])
    car_type = models.CharField(max_length=2, choices=Types, null=True, blank=True)

    def __str__(self):
        try:
            profile = self.driver.telegram_profile
        except Exception:
            profile = self.driver
        return f"{profile} {self.model}"