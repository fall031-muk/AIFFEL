from django.contrib import admin
from .models import Question

# @admin.register(models.Post)
# class QuestionAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Question)