from django.contrib import admin
from .models import Budget

class BudgetAdmin(admin.ModelAdmin):
    ordering = ['amount']
    search_fields = ['title']

# Register your models here.
admin.site.register(Budget, BudgetAdmin)