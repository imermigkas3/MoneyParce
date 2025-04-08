from django.contrib import admin
from .models import Budget

class BudgetAdmin(admin.ModelAdmin):
    ordering = ['cost']
    search_fields = ['name']

# Register your models here.
admin.site.register(Budget, BudgetAdmin)