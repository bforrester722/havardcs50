from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = [
    ("auto", "Auto"),
    ("clothing", "Clothing"),
    ("electronics", "Electronics"),
    ("home", "Home"),
    ("jewelry", "Jewelry"),
    ("sportingGoods", "Sporting Goods"),
    ("toys", "Toys"),
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
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_listings",
    )

    def __str__(self):
        return f"{self.id} {self.owner} ({self.title}) {self.startingBid}"


class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids"
    )

    def __str__(self):
        return f"{self.user} {self.bid}"


class Comment(models.Model):
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    date_time = models.DateTimeField()
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=144)

    def formatted_date_time(self):
        return self.date_time.strftime("%m-%d-%Y %H:%M")

    def __str__(self):
        return f"{self.formatted_date_time()} {self.user} says: {self.comment} on {self.listing_id.title}"
