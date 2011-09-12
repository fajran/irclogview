import datetime
from datetime import timedelta

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def build_calendar_table(year, month):
    # Determine last day of the month
    one_day = timedelta(days=1)

    start = datetime.date(year, month, 1)
    if month == 12:
        last = datetime.date(year, 12, 31)
    else:
        last = datetime.date(year, month+1, 1) - one_day

    # Build calendar table
    date = start
    weekday = 0
    rows = []
    cols = []
    while date <= last:
        while weekday < date.weekday():
            cols.append(None)
            weekday += 1
        cols.append(date)
        date += one_day

        weekday += 1
        if weekday == 7:
            rows.append(cols)
            cols = []
            weekday = 0

    if weekday != 0 and weekday < 7:
        while weekday < 7:
            cols.append(None)
            weekday += 1
        rows.append(cols)

    return rows

@register.simple_tag
def log_calendar(data, today):
    table = build_calendar_table(today.year, today.month)

    def cell_builder(date, row, col):
        classes = ['col-%s' % col]
        if not date in data:
            classes.append('empty')
        elif date == today:
            classes.append('today')

        content = '&nbsp;'
        if date is not None:
            if date in data:
                url = '../%04d%02d%02d/' % (today.year, today.month, date.day)
                content = '<a href="%s">%s</a>' % (url, date.day)
            else:
                content = date.day

        return '<td class="%s">%s</td>' % (' '.join(classes), content)

    # Construct HTML
    title = today.strftime('%B %Y')
    day_names = [datetime.date(2011, 5, day+1).strftime('%A')[0]
                 for day in range(7)]

    html = []
    html.append('<table class="calendar" border="1">')
    html.append('<tr class="title"><th colspan="7">%s</th></tr>' % title)
    html.append('<tr>')
    for day in day_names:
        html.append('<th>%s</th>' % day)
    html.append('</tr>')
    for i, cols in enumerate(table):
        html.append('<tr>')
        for j, date in enumerate(cols):
            html.append(cell_builder(date, i, j))
        html.append('</tr>')
    html.append('</table>')

    return ''.join(html)
    
