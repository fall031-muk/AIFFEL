from django.contrib import admin
from .models import User

# @admin.register(models.User)
# class UserAdmin(admin.ModelAdmin):
#     pass

admin.site.register(User)