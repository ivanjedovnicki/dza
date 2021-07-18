from datetime import datetime

from django.test import TestCase
from django.utils.timezone import make_aware
from django.shortcuts import reverse

from earthquake_visualizer.models import EarthQuakeFeed


class EarthQuakeListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        EarthQuakeFeed.objects.create(
            id=1009093,
            title='ML 1.8  SPAIN',
            latitude=38.10,
            longitude=-2.35,
            magnitude=1.8,
            time=make_aware(datetime(2021, 7, 13, 23, 22, 37))
        )

    def test_get_earthquake_list(self):
        response = self.client.get(reverse('earthquake:earthquake-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ML 1.8  SPAIN')
        self.assertContains(response, '38.10')
        self.assertContains(response, '-2.35')
        self.assertContains(response, '1.8')
