import re
import os
import colorsys
from glob import glob
from datetime import datetime

from django.conf import settings

def update_logs():
    from .models import Channel

    channels = settings.IRCLOGVIEW_CHANNELS
    if not type(channels) in [list, set, tuple]:
        channels = [channels]
    for name in channels:
        channel, created = Channel.objects.get_or_create(name=name)
        update_log(channel)

# TODO make the filename pattern configurable
re_fname = re.compile(r'#(?P<name>[\w_.-]+).(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.log')

def update_log(channel):
    logdir = os.path.join(settings.IRCLOGVIEW_LOGDIR, channel.name)
    files = glob(os.path.join(logdir, '*.log'))
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

        parse_log(channel, year, month, day, fname)

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
        return

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

