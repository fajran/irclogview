from django.http import HttpResponse

def index(request):
    return HttpResponse('index')

def channel(request, name):
    return HttpResponse('channel: %s' % name)

def show(request, name, year, month, day):
    return HttpResponse('show: %s - %s/%s/%s' % (name, year, month, day))

