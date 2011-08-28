from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response

from .models import Channel, Log

def index(request):
    channels = Channel.objects.all()
    if len(channels) == 1:
        channel = channels[0]
        return HttpResponseRedirect(channel.get_absolute_url())

    context = {'channels': channels}
    return render_to_response('irclogview/index.html', context)

def channel_index(request, name):
    channel = get_object_or_404(Channel, name=name)
    logs = Log.objects.filter(channel=channel)

    if len(logs) > 0:
        log = logs[0]
        return HttpResponseRedirect(log.get_absolute_url())

    context = {'channel': channel}
    return render_to_response('irclogview/empty.html', context)

def show_log(request, name, year, month, day):
    channel = get_object_or_404(Channel, name=name)
    date = datetime(int(year), int(month), int(day)).date()

    log = get_object_or_404(Log, channel=channel, date=date)

    context = {'log': log}
    return render_to_response('irclogview/show_log.html', context)

