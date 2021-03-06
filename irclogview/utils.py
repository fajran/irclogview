import re
import os
import colorsys
import shutil
from glob import glob
from datetime import datetime, timedelta

from django.conf import settings

UPDATE_DELAY = timedelta(seconds=settings.IRCLOGVIEW_UPDATE_DELAY)

class UpdateSemaphore(object):
    def __init__(self, channel):
        self.channel = channel
        self.acquired = False
        self.lock = os.path.join(settings.IRCLOGVIEW_LOCKDIR,
                                 '%s.lock' % channel.name)

    def __enter__(self):
        self.acquired = False

        last_update = self.channel.updated
        if datetime.now() - last_update < UPDATE_DELAY:
            return self

        # Remove uncleaned lock
        if os.path.exists(self.lock):
            stat = os.stat(self.lock)
            mtime = datetime.fromtimestamp(stat.st_mtime)
            if datetime.now() - mtime > UPDATE_DELAY * 5:
                try:
                    shutil.rmtree(self.lock)
                except OSError:
                    pass

        # Try to create lock
        try:
            os.makedirs(self.lock)
            self.acquired = True
        except OSError:
            pass

        return self

    def __exit__(self, type, value, traceback):
        if not self.acquired:
            return

        # Remove lock
        try:
            shutil.rmtree(self.lock)
        except OSError:
            pass

update_semaphore = UpdateSemaphore

def update_logs():
    from .models import Channel

    channels = settings.IRCLOGVIEW_CHANNELS
    if not type(channels) in [list, set, tuple]:
        channels = [channels]

    for name in channels:
        channel, created = Channel.objects.get_or_create(name=name)

        with update_semaphore(channel) as semaphore:
            if semaphore.acquired:
                update_log(channel)

# TODO make the filename pattern configurable
re_fname = re.compile(r'#(?P<name>[\w_.-]+).(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.log')

def update_log(channel):
    logdir = os.path.join(settings.IRCLOGVIEW_LOGDIR, channel.name)
    files = glob(os.path.join(logdir, '*.log'))

    updated = False
    for fname in files:
        m = re_fname.search(fname)
        if not m:
            continue

        info = m.groupdict()

        name = info['name']
        year = int(info['year'])
        month = int(info['month'])
        day = int(info['day'])

        if name != channel.name:
            continue

        updated |= parse_log(channel, year, month, day, fname)

    channel.save()

# TODO make log pattern configurable
re_line = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) ' \
                     r'(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) \|  ' \
                     r'((<(?P<msg_name>[^>]+)> (?P<msg_text>.+))|' \
                      r'(\* (?P<say_name>[^ ]+) (?P<say_text>.+))|' \
                      r'(\*\*\* (?P<act_name>[^ ]+) (?P<act_text>.+)))')
msg_types = ['msg', 'say', 'act']

def parse_log(channel, year, month, day, fname):
    from .models import Log

    date = datetime(year, month, day).date()
    try:
        log = Log.objects.get(channel=channel, date=date)
    except Log.DoesNotExist:
        log = Log(channel=channel, date=date)

    stat = os.stat(fname)
    mtime = datetime.fromtimestamp(stat.st_mtime)
    if log is not None and log.mtime is not None and log.mtime >= mtime:
        return False

    content = []
    for line in open(fname):
        line = line.strip()
        m = re_line.match(line)
        if not m:
            continue

        data = m.groupdict()
        msg_type = [t for t in msg_types
                      if data['%s_name' % t] is not None][0]
        text = data['%s_text' % msg_type]
        name = data['%s_name' % msg_type]

        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
        hour = int(data['hour'])
        minute = int(data['min'])
        sec = int(data['sec'])
        timestamp = datetime(year, month, day, hour, minute, sec)

        content.append((timestamp, msg_type, name, text))

    log.mtime = mtime
    log.content = content
    log.save()

    return True

class RainbowColor(object):
    def __init__(self):
        self.hue = 0.0
        self.colors = {}

    def get_color(self, tag):
        color = self.colors.get(tag, None)
        if color is None:
            r, g, b = colorsys.hsv_to_rgb(self.hue, 1., 1.)
            color = '#%s' % self.to_hex(r, g, b)
            self.colors[tag] = color

            self.hue += 0.641
            while self.hue > 1.0:
                self.hue -= 1.0

        return color

    def to_hex(self, r, g, b):
        r, g, b = map(lambda x: int(x * 255), [r,g,b])
        res = '000000%s' % hex((r<<16)|(g<<8)|b)[2:]
        return res[-6:]

