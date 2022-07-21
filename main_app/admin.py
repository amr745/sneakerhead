from django.contrib import admin

# Register your models here.
from .models import Sneaker, Worn

admin.site.register(Sneaker)
admin.site.register(Worn)