from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StorageLocation,Category,Item

admin.site.register(StorageLocation)
admin.site.register(Category)
admin.site.register(Item)

# Register your models here.
