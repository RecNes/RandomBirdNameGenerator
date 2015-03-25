# -*- coding: utf-8 -*-
import re
import string
import urllib2

__author__ = 'Remind Bird'


class ExtractValuesFromRemotePage(object):
    def __init__(self):
        self.url = ""
        self.page_list = []
        self.bird_names = []
        self.rgx = None
        self.the_page = None
        self.file_name = "rbng_temp"

    @classmethod
    def class_name(cls):
        return cls.__name__

    def re_machine(self):
        try:
            return re.compile(self.rgx, re.U).findall(self.the_page)
        except Exception:
            raise Exception(u'{} regex throws error'.format(self.rgx))

    def make_connection(self):
        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req)
        self.the_page = response.read()
        with open("{}_html.txt".format(self.file_name), "w+") as wp:
            wp.writelines(self.the_page)

    def format_data(self):
        pass

    def save_to_database(self):
        self.format_data()
        pass

    def write_into_file(self):
        with open("{}.txt".format(self.file_name)) as bn:
            bn.writelines(repr(self.bird_names))

    def run(self):
        self.make_connection()
        self.bird_names = self.re_machine()
        self.write_into_file()
        # self.save_to_database()


class WikiTurkiye(ExtractValuesFromRemotePage):
    def __init__(self):
        ExtractValuesFromRemotePage.__init__(self)
        self.url = "http://tr.wikipedia.org/wiki/T%C3%BCrkiye_ku%C5%9Flar_listesi"
        self.rgx = '<li><a\shref="/wiki/\w+"\stitle="[\w\s]+"\sclass="mw-redirect">([\w\s]+)</.*?\s\(<i>([\w\s]+)</i>\).*?/li>'
        self.file_name = self.class_name()


class WikiLOBOTW(WikiTurkiye):
    def __init__(self):
        WikiTurkiye.__init__(self)
        self.url = "http://en.wikipedia.org/wiki/List_of_birds_of_the_world"
        self.rgx = '<li><a\shref="/wiki/\w+"\stitle="[\w\s]+"\sclass="mw-redirect">([\w\s]+)</.*?\s\(<i>([\w\s]+)</i>\).*?/li>'
        self.file_name = self.class_name()


class AllaboutbirdsOrg(ExtractValuesFromRemotePage):
    def __init__(self):
        ExtractValuesFromRemotePage.__init__(self)
        self.base_url = "http://www.allaboutbirds.org/guide/browse.aspx?name="
        self.alphabet = list(string.ascii_lowercase)
        self.rgx = "</span></div><h2><a\shref=\".*?\">(.*?)</a>\s<em>(.*?)</em></h2><div id='browse_links'>"
        self.file_name = self.class_name()
        self.counter = 0

    def run(self):
        for url_extention in self.alphabet:
            self.url = "{}{}".format(self.base_url, url_extention)
            self.make_connection()
            self.bird_names += self.extract_bird_names()
            self.counter += 1
        self.write_into_file()
        # self.save_to_database()