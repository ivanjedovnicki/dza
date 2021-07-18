from datetime import datetime

from django.test import TestCase
from django.utils.timezone import make_aware

from earthquake_visualizer.models import EarthQuakeFeed


class EarthQuakeFeedTest(TestCase):

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

    def setUp(self):
        self.earthquake_feed = EarthQuakeFeed.objects.get(id=1009093)

    def test_create_feed(self):
        self.assertEqual(str(self.earthquake_feed), 'ID = 1009093, TITLE = ML 1.8  SPAIN')
