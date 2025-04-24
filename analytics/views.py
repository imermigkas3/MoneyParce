from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import GraphGenerationLog
from django.db.models import Count
from django.utils.timezone import now, timedelta

@staff_member_required
def graph_report(request):
    last_30_days = now() - timedelta(days=30)
    data = (
        GraphGenerationLog.objects
        .filter(timestamp__gte=last_30_days)
        .values('graph_type')
        .annotate(total=Count('id'))
    )
    return render(request, 'analytics/graph_report.html', {'report': data})
