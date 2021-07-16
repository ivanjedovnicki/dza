from django.urls import path

from .views import EarthQuakeListView

urlpatterns = [
    path('', EarthQuakeListView.as_view())
]
