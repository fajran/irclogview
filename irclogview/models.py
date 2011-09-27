from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse

from picklefield.fields import PickledObjectField

from . import utils

class Channel(models.Model):
    name = models.SlugField(max_length=50, unique=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'#%s' % self.name

    def get_absolute_url(self):
        return reverse('irclogview_channel', args=[self.name])

class Log(models.Model):
    channel = models.ForeignKey(Channel, db_index=True)
    date = models.DateField(db_index=True)
    mtime = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    content = PickledObjectField()

    class Meta:
        ordering = ['-date']
        unique_together = ('channel', 'date')

    def __unicode__(self):
        return u'#%s - %s' % (self.channel.name,
                              self.date.strftime('%Y-%m-%d'))

    def get_absolute_url(self):
        date = self.date
        return reverse('irclogview_show',
                       args=[self.channel.name,
                             '%04d' % date.year,
                             '%02d' % date.month,
                             '%02d' % date.day])

    def content_dict(self):
        colors = utils.RainbowColor()
        for data in self.content:
            item = dict(zip(['time', 'type', 'name', 'text'], data))
            item['name_color'] = item['type'] == 'act' \
                                 and 'inherit' \
                                 or colors.get_color(item['name'])
            yield item

class Bookmark(models.Model):
    log = models.ForeignKey(Log)
    path = models.SlugField(max_length=100)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, default=None, blank=True)

    created = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return u'#%s - %s' % (self.log.channel.name, self.title)

    def get_absolute_url(self):
        return reverse('irclogview_bookmark_show',
                       args=[self.log.channel.name, self.path])

