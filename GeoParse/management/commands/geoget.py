# -*- coding: utf-8 -*-
__author__ = 'booka'

from django.core.management.base import BaseCommand, CommandError
from GeoParse.models import *
from grab import Grab, response
import json
import re
import logging

def get_addresses(xx, po):
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
        houses = re.findall(r'(\d+\w*-?\d+\w*)', x, re.UNICODE) #r'(\d+\w*-{0,1}\d+\w*)'
        tmp_h = []
        for h in houses:
            h2 = re.split(r'-', h, re.UNICODE)
            digit_h = re.findall(r'\d+', h)
            tmp_h.extend(h2)
            if len(h2) == 2:
                tmp_h.extend([u'%d' % d for d in range(int(digit_h[0])+1, int(digit_h[1]))])
        pos = []
        AddressEnum.get_or_create(street=u'%s, %s, %s' % (po.district.area, po.district,  adr))
        for ih in tmp_h:
            adr_full = u'%s, %s, %s%s' % (po.district.area, po.district,  adr, ih)
            adr_match = AddressOnMap.objects.filter(address__exact=adr_full).first()
            if adr_match:
                pos_res = (adr_match.latitude, adr_match.longitude)
            else:
                pos_res = api.geocode(settings.YANDEX_MAPS_API, adr_full)
                mymap = AddressOnMap()
                mymap.longitude = pos_res[0]
                mymap.latitude = pos_res[1]
                mymap.address = adr_full
                mymap.save()
            pos.append(pos_res)
            poi.add(pos_res)
        list_adr.append({adr: pos})

    return list_adr, poi


class Command(BaseCommand):
    help = 'Get, parse and update database'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('area_id', nargs='+', type=int)


    @staticmethod
    def page_parse(data):
        '''
        response: input response page
        :return: prepeared data for models
        '''
        objs = []
        response = data['response']
        trs = response.xpath_list('//table[@class="mytable"]//tr')

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

                    po = PowerOutage()
                    po.outage_type = 'plan'
                    po.address_representation = list_adr
                    po.date_from = header[1].text
                    po.date_to = header[2].text
                    pobj = PowerObject.objects.get_or_create(header[0].text)
                    po.power_object = pobj
                    outreas = OutageReason.objects.get_or_creare(header[3].text)
                    po.outage_reason = outreas
                    po.district = data['district']
                    po.description = header[4].text
                    po.save()
                    logger.info("'Power outage' object created: %s" % po)


        points = set()
        for obj in objs:
            points.update(obj['poi'])

        return {
            'objs': objs,
            'points': json.dumps(points),
        }

    @staticmethod
    def district_update(district):
        g = Grab()
        response = g.go(district.url, charset='utf-8')
        data = Command.page_parse({
            'response': response,
            'district': district,
            }
        )
        return data


    def handle(self, *args, **options):
        if 'area_id' in options:
            iter_by = options['area_id']
        else:
            iter_by = [i.id for i in Area.objects.all()]
        for area_id in iter_by:
            try:
                area = Area.objects.get(pk=area_id)
            except Area.DoesNotExist:
                raise CommandError('Area "%s" does not exist' % area_id)

            districts = list(District.objects.filter(area=area.id))
            for district in district:
                if self.district_update(district):
                    logger.info('Successfully update "%s"' % area)

logger = logging.getLogger()
