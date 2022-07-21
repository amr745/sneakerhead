from django.contrib import admin

# Register your models here.
from .models import Sneaker, Worn, Protector, Photo

admin.site.register(Sneaker)
admin.site.register(Worn)
admin.site.register(Protector)
admin.site.register(Photo)