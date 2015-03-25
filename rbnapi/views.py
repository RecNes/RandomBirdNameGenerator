# -*- coding: utf-8 -*-
import re
import urllib2
from django.shortcuts import render
# from rbnapi.models import BirdNameDatabase
# from htmlbrowser import HTMLBrowser
from rbnapi.rb_logger import log


# class API():
#     def __init__(self):
#         pass
#
#     @property
#     def get_random_bird_name(self):
#         return BirdNameDatabase.object.order_by('?')[0]
#
#     def serialize_data(self):
#         pass


class ExtractValuesFromRemotePage():
    def __init__(self):
        self.url = "http://tr.wikipedia.org/wiki/T%C3%BCrkiye_ku%C5%9Flar_listesi"
        self.page_list = []
        self.bird_names = []
        self.rgx = None
        self.the_page = None
        self.RECompiled = {}

    def re_machine(self):
        try:
            return re.compile(self.rgx, re.U).findall(self.the_page)
        except Exception as e:
            raise Exception(u'{} regex throws error'.format(self.rgx))

    def make_connection(self):
        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req)
        self.the_page = response.read()
        with open("web_page.txt", "w+") as wp:
            wp.writelines(self.the_page)

    def extract_bird_names(self):
        # self.rgx = '<li><i><a href=\".*?\" title=\"[\w\s]+\" class=\"mw-redirect\">([\w\s]+)</a></i>([\w\s]+)<.*?></li>'
        self.rgx = '<li><a\shref="/wiki/\w+"\stitle="[\w\s]+"\sclass="mw-redirect">([\w\s]+)</.*?\s\(<i>([\w\s]+)</i>\).*?/li>'
        return self.re_machine()

    def format_data(self):
        pass

    def save_to_database(self):
        self.format_data()
        pass

    def write_into_file(self):
        with open("turkish_bird_names.txt", "w+") as bn_file:
            bn_file.writelines(repr(self.bird_names))

    def run(self):
        self.make_connection()
        self.bird_names = self.extract_bird_names()
        self.write_into_file()
        # self.save_to_database()