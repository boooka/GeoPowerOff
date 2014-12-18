# coding: utf-8
import re
from annoying.decorators import render_to
from grab import Grab
from django.utils.translation import gettext as _
from yandex_maps import api
from django.conf import settings
from yandex_maps.models import MapAndAddress
from utils import js_val_converter

def clear_address(s):
    address = re.findall(r'([\w\.]+), ', s, re.UNICODE)

    return s

def get_addresses(xx):
    '''

    :param xx: address list
    :return: list of dict with street key and houses as value
    '''
    list_adr = []
    poi = set()
    for x in xx:
        match_adr = re.match(r'([\w\.\s]+, [\w|\.|\s]+), ', x, re.UNICODE)
        if not match_adr:
            print x
            continue
        adr = u''.join(match_adr.group())
        houses = re.findall(r'(\d+\w*-{0,1}\d+\w*)', x, re.UNICODE)
        tmp_h = []
        for h in houses:
            h2 = re.split(r'-', h, re.UNICODE)
            digit_h = re.findall(r'\d+', h)
            tmp_h.extend(h2)
            if len(h2) == 2:
                tmp_h.extend([u'%d' % d for d in range(int(digit_h[0])+1, int(digit_h[1]))])
        pos = []

        for ih in tmp_h:
            adr_full = u'Кировоградская обл., ' + adr + ih
            adr_match = MapAndAddress.objects.filter(address__exact=adr_full).first()
            if adr_match:
                pos_res = (adr_match.latitude, adr_match.longitude)
            else:
                pos_res = api.geocode(settings.YANDEX_MAPS_API, adr_full)
                mymap = MapAndAddress()
                mymap.longitude = pos_res[0]
                mymap.latitude = pos_res[1]
                mymap.address = adr_full
                mymap.save()
            pos.append(pos_res)
            poi.add(pos_res)
        list_adr.append({adr: pos})

    return list_adr, poi

@render_to('home.html')
def home(request):

    objs = []

    g = Grab()
    g.go('http://kiroe.com.ua/poweroutage/plan/8', charset='utf-8')
    trs = g.xpath_list('//table[@class="mytable"]//tr')

    for r in trs:
        print 'prepare %s of %s' % (trs.index(r), len(trs))
        if r.values() == 'header_last':
            continue

        if 'koe-tr-emergency-active' in r.values():
            header = r.getchildren()
            if trs.index(r)+1 != len(trs) and 'class' not in trs[trs.index(r)+1].attrib:
                list_adr = trs[trs.index(r)+1].xpath('td/text()')
                addresses, pois = get_addresses([u''.join(x) for x in list_adr])

                obj = {
                    'obj': header[0].text,
                    'date_from': header[1].text,
                    'date_to': header[2].text,
                    'reason': header[3].text,
                    'reason_detail': header[4].text,
                    'list_adr': u'| '.join(list_adr),
                    'addresses': addresses,
                    'poi': pois,
                }
                objs.append(obj)
    points = set()
    for obj in objs:
        points.update(obj['poi'])

    #print r'\n'.join([i.text_content() for i in trs])
    return {
        'objs': js_val_converter(objs),
        'points': points,
    }
