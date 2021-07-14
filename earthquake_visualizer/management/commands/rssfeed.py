import re
from datetime import datetime
from xml.etree import ElementTree

import requests
from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from earthquake_visualizer.models import EarthQuakeFeed

URI = r'https://www.emsc.eu/service/rss/rss.php?typ=emsc&min_lat=10&min_long=-30&max_long=65'
PRIMARY_KEY_REGEX = re.compile(r'https://www.emsc.eu/Earthquake/earthquake\.php\?id=(\d*)')
MAGNITUDE_REGEX = re.compile(r'.*(\d\.\d)')
COUNTRY = ''
HTTP_OK = 200


def _get_pk(link):
    return int(PRIMARY_KEY_REGEX.findall(link)[0])


def _get_magnitude(magnitude):
    return MAGNITUDE_REGEX.findall(magnitude)[0]


def _get_time(time):
    return make_aware(datetime.strptime(time, "%Y-%m-%d %H:%M:%S %Z"))


def _parse_feed(rss_feed):
    namespace = {
        'geo': 'http://www.w3.org/2003/01/geo/',
        'emsc': 'https://www.emsc.eu'
    }
    root = ElementTree.fromstring(rss_feed.text)
    for item in root.iter('item'):
        yield {
            'id': _get_pk(item.find('link').text),
            'title': item.find('title').text,
            'latitude': item.find('geo:lat', namespace).text,
            'longitude': item.find('geo:long', namespace).text,
            'magnitude': _get_magnitude(item.find('emsc:magnitude', namespace).text),
            'time': _get_time(item.find('emsc:time', namespace).text)
        }


class Command(BaseCommand):
    help = 'Retrieves rss feed data and updates the database.'

    def handle(self, *args, **options):
        rss_feed = requests.get(URI)
        if rss_feed.status_code != HTTP_OK:
            self.stderr('rss feed data unavailable')
            return

        created, updated = 0, 0
        for item in _parse_feed(rss_feed):
            # if COUNTRY not in item['title']:
            #     continue
            try:
                obj = EarthQuakeFeed.objects.get(id=item['id'])
                for key, value in item.items():
                    setattr(obj, key, value)
                    obj.save()
                updated += 1
            except EarthQuakeFeed.DoesNotExist:
                EarthQuakeFeed.objects.create(**item)
                created += 1
        self.stdout(f'Created {created}, updated {updated} records')
