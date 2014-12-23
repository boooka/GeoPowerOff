# -*- coding: utf-8 -*-
import re
from annoying.decorators import render_to
from grab import Grab
from django.utils.translation import gettext as _
from yandex_maps import api
from django.conf import settings
from yandex_maps.models import MapAndAddress
from utils import js_val_converter


@render_to('home.html')
def home(request):

    points =
    return {
        'points': points,
    }
