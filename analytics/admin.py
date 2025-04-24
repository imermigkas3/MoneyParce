from django.contrib import admin
from .models import GraphGenerationLog

@admin.register(GraphGenerationLog)
class GraphGenerationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'graph_type', 'timestamp')
    list_filter = ('graph_type', 'timestamp')
    search_fields = ('user__username', 'graph_type')
