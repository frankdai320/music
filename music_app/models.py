from django.db import models


class Music(models.Model):
    link = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added')
    added_by = models.CharField(max_length=200)

    def __str__(self):
        return self.link + " " + str(self.date_added) + " by " + self.added_by + " id " + str(self.pk)
