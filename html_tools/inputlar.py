#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
eTahsildar Fatura Ödeme Programı
Telif Hakki Bilgisi
 * Surum 0.1.0.0 - 1.5.0.0 Telifhakki (c) 2006-2009 Evren Esat Özkan
 * Surum 1.5.0.0 - Telifhakki (c) 2009 Evren Esat Özkan
        [T.A.F.T. Telekominikasyon Bilișim Hizmetleri Turizim Tekstil İnșaat Ve Sanayi Ticaret Limited Șirketi ]
"""
from sgmllib import SGMLParser


class secimler(SGMLParser):
    """
    adi verilen select kutusunun seceneklerini liste olarak dondurur
    parser=inputlar()
    parser.feed(data,'alanAdi')
    """
    def feed(self, veri, ad):
        self.ad = ad
        SGMLParser.feed(self, veri)
        return self.veriler

    def reset(self):
        SGMLParser.reset(self)
        self.veriler = []

    def start_input(self, attrs):
        if [v for k, v in attrs if k=='name' and v == self.ad]: self.veriler.extend([v for k, v in attrs if k == 'option'])

class inputlar(SGMLParser):
    """
    input alanlarinda verilen addakilerin degerini listede dondurur
    parser=inputlar()
    parser.feed(data,'alanAdi')
    """
    def feed(self, veri, ad):
        self.ad = ad
        SGMLParser.feed(self, veri)
        return self.veriler

    def reset(self):
        SGMLParser.reset(self)
        self.veriler = []

    def start_input(self, attrs):
        if [v for k, v in attrs if k == 'name' and v == self.ad]: self.veriler.extend([v for k, v in attrs if k == 'value'])

class tumInputlar(SGMLParser):
    """
    input alanlarinda verilen addakilerin degerini listede dondurur
    parser=inputlar()
    parser.feed(data)
    """
    def feed(self, veri):
        self.veriler = {}
        SGMLParser.feed(self, veri)
        return self.veriler

    def reset(self):
        SGMLParser.reset(self)
        self.veriler = []

    def start_input(self, attrs):
        ad = deger = None
        try:
            ad = [v for k, v in attrs if k == 'name'][0]
        except:
            pass
        try:
            deger = [v for k, v in attrs if k == 'value'][0]
        except:
            pass
        if ad is not None and deger is not None:
            self.veriler.update({ad: deger})


if __name__ == '__main__':
   from urllib2 import Request, urlopen
   url = 'http://www.google.com.tr'
   r=Request(url)
   h=urlopen(r)
   d=h.read()
   parser=inputlar()
   print parser.feed(d,'btnG')
   print parser.feed(d,'btnI')
