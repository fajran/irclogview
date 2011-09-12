from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import Channel, Log
from .utils import update_logs

def _update_logs(f):
    def _func(request, *args, **kwargs):
        update_logs()
        return f(request, *args, **kwargs)
    return _func

@_update_logs
def index(request):
    channels = Channel.objects.all()
    if len(channels) == 1:
        channel = channels[0]
        return HttpResponseRedirect(channel.get_absolute_url())

    context = {'channels': channels}
    return render_to_response('irclogview/index.html', context,
                              context_instance=RequestContext(request))

@_update_logs
def channel_index(request, name):
    channel = get_object_or_404(Channel, name=name)
    logs = Log.objects.filter(channel=channel)

    if len(logs) > 0:
        log = logs[0]
        return HttpResponseRedirect(log.get_absolute_url())

    context = {'channel': channel}
    return render_to_response('irclogview/empty.html', context,
                              context_instance=RequestContext(request))

@_update_logs
def show_log(request, name, year, month, day):
    year, month, day = map(int, [year, month, day])

    channel = get_object_or_404(Channel, name=name)
    date = datetime(year, month, day).date()

    # The day's log
    log = get_object_or_404(Log, channel=channel, date=date)

    # Month summary
    first = datetime(year, month, 1)
    if month == 12:
        last = datetime(year, month, 31)
    else:
        last = datetime(year, month+1, 1) - timedelta(days=1)
    logs = Log.objects.filter(channel=channel,
                              date__gte=first.date(),
                              date__lte=last.date())
    dates = set(logs.values_list('date', flat=True))

    context = {'log': log,
               'date': date,
               'log_dates': dates}
    return render_to_response('irclogview/show_log.html', context,
                              context_instance=RequestContext(request))

