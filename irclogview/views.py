from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from .models import Channel, Log

def index(request):
    return HttpResponse('index')

def channel_index(request, name):
    channel = get_object_or_404(Channel, name=name)
    return HttpResponse('channel: %s' % name)

def show_log(request, name, year, month, day):
    channel = get_object_or_404(Channel, name=name)
    date = datetime(int(year), int(month), int(day)).date()

    log = get_object_or_404(Log, channel=channel, date=date)

    context = {'log': log}
    return render_to_response('irclogview/show_log.html', context)

