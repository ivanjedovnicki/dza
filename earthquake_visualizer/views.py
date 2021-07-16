from datetime import timedelta

from django.utils import timezone
from django.views.generic import ListView

from .models import EarthQuakeFeed


class EarthQuakeListView(ListView):
    template_name = 'visualizer.html'

    def get_queryset(self):
        filter_dict = {
            'last_24_hours': timezone.now() - timedelta(days=1),
            'last_3_days': timezone.now() - timedelta(days=3),
            'last_month': timezone.now() - timedelta(days=30),
        }
        if self.request.method == 'GET':
            time_filter = self.request.GET.get('time', None)
            filter_func = filter_dict.get(time_filter, None)
            if filter_func is not None:
                return EarthQuakeFeed.objects.filter(time__gte=filter_func).order_by('time')
            return EarthQuakeFeed.objects.all().order_by('time')
