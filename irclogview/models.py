from django.db import models

from picklefield.fields import PickledObjectField

from . import utils

class Channel(models.Model):
    name = models.SlugField(max_length=50, unique=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'#%s' % self.name

class Log(models.Model):
    channel = models.ForeignKey(Channel)
    date = models.DateField()
    mtime = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    content = PickledObjectField()

    class Meta:
        unique_together = ('channel', 'date')

    def content_dict(self):
        colors = utils.RainbowColor()
        for data in self.content:
            item = dict(zip(['time', 'type', 'name', 'text'], data))
            item['name_color'] = colors.get_color(item['name'])
            yield item

