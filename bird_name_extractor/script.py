# -*- coding: utf-8 -*-
import re
import string
import urllib2
from rbnapi.models import BirdNameDatabase, ScientificName
from rbnapi.rb_logger import log

__author__ = 'Sencer Hamarat'


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
            return re.compile(self.rgx, re.UNICODE).findall(self.the_page)
        except Exception:
            raise Exception(u'{} regex throws error'.format(self.rgx))

    def make_connection(self):
        self.the_page = None
        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req)
        self.the_page = response.read()
        with open("temp/{}_html.txt".format(self.file_name), "w+") as wp:
            wp.writelines(self.the_page)

    def save_to_database(self):
        duplicate_items = list()
        self.file_name = "duplicate_items"
        for item in self.bird_names:
            try:
                bird_name = item[1].strip()
                scientific_name = item[0].strip()
                if not len(BirdNameDatabase.objects.filter(bird_name=bird_name)):
                    db_sc = ScientificName(scientific_name=scientific_name)
                    db_sc.save()
                    db = BirdNameDatabase(bird_name=bird_name, scientific_name=db_sc)
                    db.save()
                else:
                    duplicate_items.append(item)
                self.bird_names=duplicate_items
                self.write_into_file()
            except Exception as e:
                print e
                log.exception(e)
                pass

    def write_into_file(self):
        text = str()
        with open("temp/{}.txt".format(self.file_name), "w+") as bn:
            for bnt in self.bird_names:
                text += "{}\r\n".format(repr(bnt))
            bn.writelines(text)

    def run(self):
        self.make_connection()
        # self.bird_names = self.re_machine()
        # self.write_into_file()
        # self.save_to_database()


class WikiTurkiye(ExtractValuesFromRemotePage):
    def __init__(self):
        ExtractValuesFromRemotePage.__init__(self)
        self.url = "http://tr.wikipedia.org/wiki/T%C3%BCrkiye_ku%C5%9Flar_listesi"
        # self.rgx = '<li><a\shref="/wiki/\w+"\stitle="[\w\s]+"\sclass="mw-redirect">([\w\s]+)</.*?\s\(<i>([\w\s]+)</i>\).*?/li>'
        self.rgx = '<li><a\shref="/wiki/[\w_]+"\stitle="[\w\s]+"\sclass="mw-redirect">(.*?)</.*?\s\(<i>([\w\s\'\-]+)</i>\).*?/li>'
        self.file_name = self.class_name()


class WikiLOBOTW(WikiTurkiye):
    def __init__(self):
        WikiTurkiye.__init__(self)
        self.url = "http://en.wikipedia.org/wiki/List_of_birds_of_the_world"
        # self.rgx = '<li><i><a\shref="/wiki/[\w_]+"\stitle="[\w\s]+"\sclass="mw-redirect">([\w\s]+)</.*?/i>([\w\s]+)<.*?li>'
        self.rgx = '<li><i><a\shref="/wiki/[\w_]+"\stitle="[\w\s]+"\sclass="mw-redirect">([\w\s]+)</a></i>\s([\w\s\'\-]+).*?/li>'
        self.file_name = self.class_name()


class SibleyAndMonroe(WikiTurkiye):
    def __init__(self):
        WikiTurkiye.__init__(self)
        self.url = "http://ces.iisc.ernet.in/hpg/envis/sibleydoc63.html"
        # self.rgx = "^\s+?\d{1,3}\s+\d{1,4}([\w\s\'-]+)\s+([\w\s\'-]+)$"
        self.rgx = "\d{1,3}\s{1,4}\d{1,4}\s(\w+\s\w+\s?\w+?)\s+([\w\'-]+\s[\D\w\'-]+\s?[\D\w\'-]+?)"
        self.file_name = self.class_name()

    def read_file(self):
        text = str()
        with open("temp/{}_html.txt".format(self.file_name), "r") as bn:
            return bn.readlines()

    def run(self):
        self.make_connection()

    def run2(self):
        """
        Go find and replace, turn on "regex" and "match case" and apply below step by step
        First: "^\s+\d{1,3}\s+\d{1,4}\s"
        Second: "^\d{1,3}\s+\d{1,4}\s"
        Third; Do replace "\W[\s]+" with "|"

        Than run this method.
        """
        fl = self.read_file()
        for line in fl:
            self.the_page = line
            sline = line.lower().replace("\n", "").split("|")
            print repr(sline)
            self.bird_names.append((sline[0], sline[1]))
        self.save_to_database()


class AllaboutbirdsOrg(ExtractValuesFromRemotePage):
    def __init__(self):
        ExtractValuesFromRemotePage.__init__(self)
        self.base_url = "http://www.allaboutbirds.org/guide/browse.aspx?name="
        self.alphabet = list(string.ascii_lowercase)
        self.rgx = "</span></div><h2><a\shref=\".*?\">(.*?)</a>\s<em>(.*?)</em></h2><div id='browse_links'>"
        self.file_name = self.class_name()
        self.counter = 0

    def save_to_database(self):
        for item in self.bird_names:
            try:
                bird_name = item[0].strip()
                scientific_name = item[1].strip()
                db_sc = ScientificName(scientific_name=scientific_name)
                db_sc.save()
                db = BirdNameDatabase(bird_name=bird_name, scientific_name=db_sc)
                db.save()
            except Exception as e:
                print e
                log.exception(e)
                pass

    def run(self):
        for url_extention in self.alphabet:
            self.url = "{}{}".format(self.base_url, url_extention)
            self.make_connection()
            self.bird_names += self.re_machine()
            self.counter += 1
        self.write_into_file()
        self.save_to_database()