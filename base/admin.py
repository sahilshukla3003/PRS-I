from django.contrib import admin
from .models import UserReviews, GeneralReviews

# Register your models here.
admin.site.register(UserReviews)
admin.site.register(GeneralReviews)