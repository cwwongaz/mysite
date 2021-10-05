from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

class client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_profile")
    delivery_address = models.TextField(blank=True, max_length=500)
    birthday = models.DateTimeField()
    # consider implementing bought history

class comment(models.Model):
    comment_content = models.TextField(max_length=2000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_comment")

class rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

class item(models.Model):
    # item basic information
    item_name = models.CharField(max_length=100)
    item_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    item_Description = models.TextField(max_length=1000)
    item_footnote = models.TextField(max_length=100, blank=True)
    number_in_store = models.PositiveIntegerField(default=0)
    # handling the rating
    rating = models.ManyToManyField(rating, blank=True, related_name="item")
    rating_average = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    number_of_rating = models.PositiveIntegerField(default=0)

    picture = models.ImageField(upload_to='images/', blank=True)
    comments = models.ManyToManyField(comment, blank=True, related_name="item")

