from django.urls import path

from .views import EarthQuakeListView

app_name = 'earthquake_visualizer'

urlpatterns = [
    path('', EarthQuakeListView.as_view(), name='earthquake-list')
]
