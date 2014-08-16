from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('question',)}

admin.site.register(Question, QuestionAdmin)
