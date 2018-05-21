import datetime

import requests
from django.db import models
from django.utils import timezone


class Music(models.Model):
    link = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added', db_index=True)
    added_by = models.CharField(max_length=200)
    ip = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100, default='')
    title_cache_time = models.DateTimeField('Cache time of title', default=datetime.datetime(2010, 1, 1))
    position = models.PositiveIntegerField('Position in queue')

    def __str__(self):
        return '{link} {date} by {user} ({ip})'.format(link=self.link, date=self.date_added, user=self.added_by,
                                                       ip=self.ip)

    def cache_expired(self, days_valid):
        valid_period = datetime.timedelta(days=days_valid)
        today = timezone.now()
        return today - self.title_cache_time > valid_period

    def get_title(self):
        info = requests.get('https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v='
                            '{vid}&format=json'.format(vid=self.link)).json()
        return info.get('title', '')

    def update_title(self, force=False):
        if force or self.cache_expired(14):  # 14 days
            self.title = self.get_title()
            self.title_cache_time = timezone.now()
            self.save()
