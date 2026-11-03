"""
core/templatetags/i18n_extra.py  (yangi fayl; papkada bo'sh __init__.py bo'lishi shart)

{% load i18n_extra %}
{% translate_url request.path "uz" %}  ->  /products/jetour-t1/
{% translate_url request.path "ru" %}  ->  /ru/products/jetour-t1/
"""
from django import template
from django.urls import translate_url as _translate_url

register = template.Library()


@register.simple_tag
def translate_url(path, lang_code):
    return _translate_url(path, lang_code)
