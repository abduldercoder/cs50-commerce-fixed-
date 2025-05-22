from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
# ---------- auction core ----------
class Listing(models.Model):

    CATEGORY_CHOICES = (
    ("Vintage", "Vintage"),
    ("Modern", "Modern"),
    ("Streetwear", "Streetwear"),
    ("Formal", "Formal"),
    ("Casual", "Casual"),
    ("Designer", "Designer"),
    ("Sustainable", "Sustainable"),
    ("Accessories", "Accessories"),
    ("Shoes", "Shoes"),
    ("Other", "Other"),
    )



    title          = models.CharField(max_length=64)
    description    = models.TextField()
    starting_bid   = models.DecimalField(max_digits=10, decimal_places=2)
    image_url      = models.URLField(blank=True, null=True)
    category       = models.CharField(max_length=64,choices=CATEGORY_CHOICES, blank=True, null=True)
    creator        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active         = models.BooleanField(default=True)
    watchers       = models.ManyToManyField(User, blank=True, related_name="watchlist")
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount   = models.DecimalField(max_digits=10, decimal_places=2)
    time     = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"${self.amount} by {self.bidder.username} on {self.listing.title}"

class Comment(models.Model):
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content  = models.TextField()
    time     = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
