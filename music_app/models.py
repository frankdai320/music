from django.db import models


class Music(models.Model):
    link = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added')
    added_by = models.CharField(max_length=200)
    ip = models.CharField(max_length=100, default='')

    def __str__(self):
        return '{link} {date} by {user} ({ip})'.format(link=self.link, date=self.date_added, user=self.added_by,
                                                       ip=self.ip)
