import json
from django import template
from django.utils.timesince import timesince
import pytz
from datetime import datetime, date
from django import template

register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price):
    return round(float(qty) * float(unit_price), 3)


@register.filter(name="filter_queryset")
def filter_queryset(query_set, filter):
    return [query[filter] for query in query_set]

@register.filter(name='total_price')
def total_price(query_set):
    return round(sum([item.price for item in query_set]), 3)

@register.filter(name='append')
def append(query_set, eleemnt):
    query_set = list(query_set).append(eleemnt)
    return query_set

@register.filter(name='eth_to_usd')
def eth_to_usd(value):
    return round(value * 1789, 2);

@register.filter(name='facebook_time')
def facebook_time(value):
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')    
    now = datetime.now(vietnam_timezone)

    if not value:
        return ""

    time_difference = now.microsecond / 1000 - value.microsecond / 1000

    if time_difference < 60:
        return 'now'
    elif time_difference < 3600:
        minutes_ago = int(time_difference / 60)
        return f'{minutes_ago} min{"s" if minutes_ago != 1 else ""}'
    elif time_difference < 86400:
        hours_ago = int(time_difference / 3600)
        return f'{hours_ago} hour{"s" if hours_ago != 1 else ""}'
    else:
        days_ago = int(time_difference / 86400)
        return f'{days_ago} day{"s" if days_ago != 1 else ""}'
    
@register.filter(name='limit_length_id')
def limit_length_id(value, arg):
    value = str(value)
    parts = str(arg).split(':')
    if len(parts) == 2:
        first, second = int(parts[0]), int(parts[1])
        return value[:first] + "..." + value[len(value) - second:]

@register.filter(name='limit_length_name')
def limit_length_name(id, length):
    return str(id)[:length] + "..." 

@register.filter(name='templatevar_to_js')
def templatevar_to_js(var):
    return json.dumps(list(var))