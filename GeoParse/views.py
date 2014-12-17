# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from grab import Grab
from yandex_maps import api


def context_callback(context, *args, **kwargs):
    return


@render_to('home.html')
def home(request):
    g = Grab()
    g.go('http://kiroe.com.ua/poweroutage/plan/8')
    trs = g.xpath_list('//tr')
    objs = []
    lst = []
    for r in trs:
        if not 'class' in r.attrib:
            lst.append(' '.join([t.text_content().encode('utf-8') for t in r.getchildren()]))
            continue
        if r.attrib['class'] == 'header_last':
            continue
        if r.attrib['class'] == 'koe-tr-emergency-active':
            if lst:
                objs.append(lst)
            lst = [' '.join([t.text_content().encode('utf-8') for t in r.getchildren()]),]


    objs.append(lst)
    return {
        'objs': objs,
    }
