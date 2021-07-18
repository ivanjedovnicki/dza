from datetime import timedelta
from collections import defaultdict

from django.utils import timezone
from django.views.generic import ListView

from .models import EarthQuakeFeed


def magnitude_to_color(magnitude):
    if 0 <= magnitude < 1:
        return '#21e11e'
    if 1 <= magnitude < 2:
        return '#2f922e'
    if 2 <= magnitude < 3:
        return '#3b763a'
    if 3 <= magnitude < 4:
        return '#ae6a16'
    if 4 <= magnitude < 5:
        return '#88571d'
    if 5 <= magnitude < 6:
        return '#664a28'
    if 6 <= magnitude < 7:
        return '#eb0c0c'
    if 7 <= magnitude < 8:
        return '#951f1f'
    if 8 <= magnitude:
        return '#6d2626'


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
                return EarthQuakeFeed.objects.filter(
                    time__gte=filter_func).order_by('time')
            return EarthQuakeFeed.objects.all().order_by('time')

    def get_context_data(self, *, object_list=None, **kwargs):
        earthquake_data = defaultdict(list)
        context = super().get_context_data(**kwargs)
        earthquake_objects = context['object_list']
        for earthquake_object in earthquake_objects:
            earthquake_data['latitude'].append(earthquake_object.latitude)
            earthquake_data['longitude'].append(earthquake_object.longitude)
            earthquake_data['color'].append(
                magnitude_to_color(earthquake_object.magnitude))
        context['earthquake_data'] = earthquake_data
        print(context)
        return context
