from django.db import models
from django.contrib.auth.models import User
class UserReviews(models.Model):
    product_name = models.CharField(max_length=100)
    rating = models.FloatField()
    summary = models.TextField()
    neg = models.FloatField(null=True, blank=True)
    neu = models.FloatField(null=True, blank=True)
    pos = models.FloatField(null=True, blank=True)
    flipkart = models.BooleanField(default=False)
    img = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name[:50]

class GeneralReviews(models.Model):
    product_name = models.CharField(max_length=100)
    rating = models.FloatField()
    summary = models.TextField()
    neg = models.FloatField(null=True, blank=True)
    neu = models.FloatField(null=True, blank=True)
    pos = models.FloatField(null=True, blank=True)
    flipkart = models.BooleanField(default=False)
    img = models.TextField(null=True, blank=True)
    sc_1 = models.IntegerField(null=True, blank=True)
    sc_2 = models.IntegerField(null=True, blank=True)
    sc_3 = models.IntegerField(null=True, blank=True)
    sc_4 = models.IntegerField(null=True, blank=True)
    sc_5 = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_name[:50]

class Review(models.Model):
    text = models.TextField()