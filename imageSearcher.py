#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib
from lxml import html
import json
from PIL import Image
import io

class MyImage:

    DELTA = 50
    MINHEIGHT = 600
    MINWIDTH = 400

    def __init__(self, values):
        self.width = values['width']
        self.url = values['url']
        self.height = values['height']

    def is_confirm(self):
        result = True
        if self.height < self.MINHEIGHT or self.width < self.MINWIDTH:
            result = False
        if self.height > self.MINHEIGHT + 300 and self.width > self.MINWIDTH + 200:
            result = False
        return result and self.is_available()

    def is_available(self):
        try:
            fd = urllib.urlopen(self.url)
            image_file = io.BytesIO(fd.read())
            im = Image.open(image_file)
            return True
        except:
            return False

    def is_square(self):
        if self.height < 200 or self.width < 200:
            return False
        return abs(self.height - self.width) < self.DELTA and self.is_available()


class ImageSearcher:
    @staticmethod
    def get_logo(name):
        url_base = 'https://yandex.ru/images/search?text='
        url = url_base + name.encode('utf-8') + '&isize=small'
        page = html.fromstring(urllib.urlopen(url).read())
        elements = page.find_class('serp-list')
        e = elements[0].getchildren()
        images = [MyImage(json.loads(el.get('data-bem'))['serp-item']['preview'][0]) for el in e]
        for image in images:
            if image.is_square():
                return image.url
        return images[0].url


    @staticmethod
    def get_main_image(name):
        url_base = 'https://yandex.ru/images/search?text='
        url = url_base + name.encode('utf-8')+ ' главный корпус' + '&isize=medium'
        page = html.fromstring(urllib.urlopen(url).read())
        elements = page.find_class('serp-list')
        e = elements[0].getchildren()
        images = [MyImage(json.loads(el.get('data-bem'))['serp-item']['preview'][0]) for el in e]
        for image in images:
            if image.is_confirm():
                return image.url
        return images[0].url
