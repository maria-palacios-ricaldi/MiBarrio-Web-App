from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
import json

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    userID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


class SearchProfiles(models.Model):
    search_profileID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sp_name = models.TextField()
    age = models.TextField()

    #factor tags
    social_cultural_tags = models.TextField()
    health_wellness_tags = models.TextField()
    leisure_recreation_tags = models.TextField()
    community_services_tags = models.TextField()

    #factor levels
    social_cultural_levels = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    health_wellness_levels = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    leisure_recreation_levels = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    community_services_levels = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    transportation_active = models.BooleanField()
    transportation_public = models.BooleanField()
    backup_power_supply = models.BooleanField()
    backup_water_supply = models.BooleanField()

    class Meta:
        unique_together = ('user', 'sp_name',)


class Searches(models.Model):
    searchID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    search_profileID = models.ForeignKey(SearchProfiles, on_delete=models.CASCADE)
    search_parameters = models.TextField()
    search_timestamp = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    feedbackID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    category = models.CharField(max_length=255)
    message = models.TextField()


class Cities(models.Model):
    cityID = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=255)


class Suburbs(models.Model):
    suburbID = models.AutoField(primary_key=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    coordinates = models.TextField()


class Properties(models.Model):
    propertyID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    suburb = models.ForeignKey(Suburbs, on_delete=models.CASCADE)
    property_search_parameters = models.TextField()
    num_of_bedrooms = models.FloatField()
    num_of_bathrooms = models.FloatField()
    has_power_solutions = models.BooleanField()
    has_water_solutions = models.BooleanField()
    property_type = models.CharField(max_length=255)
    search_timestamp = models.DateTimeField(auto_now_add=True)


class PropertiesToBuy(Properties):
    properties_buy_ID = models.AutoField(primary_key=True)
    sale_price = models.PositiveIntegerField()

class PropertiesToRent(Properties):
    properties_rent_ID = models.AutoField(primary_key=True)
    rental_price = models.PositiveIntegerField()

class SearchResults(models.Model):
    search_resultID = models.AutoField(primary_key=True)
    search = models.ForeignKey(Searches, on_delete=models.CASCADE)
    suburb = models.ForeignKey(Suburbs, on_delete=models.CASCADE)

class SuburbStatistics(models.Model):
    suburb_statsID = models.AutoField(primary_key=True)
    suburb = models.ForeignKey(Suburbs, on_delete=models.CASCADE)
    crime_rate = models.PositiveIntegerField()
    year = models.DateTimeField()
