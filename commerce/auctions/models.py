from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = [
    ("auto", "Auto"),
    ("clothing", "Clothing"),
    ("sportingGoods", "Sporting Goods"),
]


class User(AbstractUser):
    watching = models.ManyToManyField("Listing", related_name="watching", blank=True)
    pass


class Listing(models.Model):
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    closed = models.BooleanField(default=False)
    description = models.CharField(max_length=144)
    imgUrl = models.CharField(max_length=256, blank=True)
    owner = models.CharField(max_length=64)
    startingBid = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=64)
    watchers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.id} {self.owner} ({self.title}) {self.startingBid}"


class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user} {self.bid}"


class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=144)

    def __str__(self):
        return f"{self.user} says: {self.comment}"
