# -*- coding: utf-8 -*-

karakter_tablosu = {
    u'0': '00',
    u'1': '01',
    u'2': '02',
    u'3': '03',
    u'4': '04',
    u'5': '05',
    u'6': '06',
    u'7': '07',
    u'8': '08',
    u'9': '09',
    u'A': '10',
    u'B': '11',
    u'C': '12',
    u'Ç': '13',
    u'D': '14',
    u'E': '15',
    u'F': '16',
    u'G': '17',
    u'Ğ': '18',
    u'H': '19',
    u'I': '20',
    u'İ': '21',
    u'J': '22',
    u'K': '23',
    u'L': '24',
    u'M': '25',
    u'N': '26',
    u'O': '27',
    u'Ö': '28',
    u'P': '29',
    u'Q': '30',
    u'R': '31',
    u'S': '32',
    u'Ş': '33',
    u'T': '34',
    u'U': '35',
    u'Ü': '36',
    u'V': '37',
    u'W': '38',
    u'X': '39',
    u'Y': '40',
    u'Z': '41',
    u'a': '42',
    u'b': '43',
    u'c': '44',
    u'ç': '45',
    u'd': '46',
    u'e': '47',
    u'f': '48',
    u'g': '49',
    u'ğ': '50',
    u'h': '51',
    u'ı': '52',
    u'i': '53',
    u'j': '54',
    u'k': '55',
    u'l': '56',
    u'm': '57',
    u'n': '58',
    u'o': '59',
    u'ö': '60',
    u'p': '61',
    u'q': '62',
    u'r': '63',
    u's': '64',
    u'ş': '65',
    u't': '66',
    u'u': '67',
    u'ü': '68',
    u'v': '69',
    u'w': '70',
    u'x': '71',
    u'y': '72',
    u'z': '73',
    u'.': '74',
    u',': '75',
    u':': '76',
    u'"': '77',
    u'é': '78',
    u'+': '79',
    u'%': '80',
    u'&': '81',
    u'/': '82',
    u'(': '83',
    u')': '84',
    u'=': '85',
    u'?': '86',
    u'*': '87',
    u'\\': '88',
    u'-': '89',
    u'_': '90',
    u'}': '91',
    u']': '92',
    u'[': '93',
    u'{': '94',
    u'$': '95',
    u'#': '96',
    u'<': '97',
    u'>': '98',
}

class BasicEncoder:
    def __init__(self, char_map, varsayilan_deger):
        self.karater_tablosu = char_map
        self.varsayilan_deger = varsayilan_deger

    def encode(self, metin):
        _sonuc = ''
        for _k in metin:
            _sonuc += self.karater_tablosu.get(_k, self.varsayilan_deger)
        return _sonuc


def rsa_encrypt(plain_text, karater_tablosu='', varsayilan_deger='99'):
    public_exponent = int('10001', 16)
    public_modulus = int('9F2EEA4AA03D55B33172E9A86CFF6156AC1628C67983193A337B98995151F9B0F41562290DB9869728'
                         '0E805803E4B18914519CEB55CEA5D03A927C28C36A4BC7', 16)
    _karakter_tablosu = karakter_tablosu
    plain_text = BasicEncoder(_karakter_tablosu, varsayilan_deger).encode(plain_text)
    plaintext = int(plain_text.encode('hex'), 16)
    ciphertext = pow(plaintext, public_exponent, public_modulus)
    sonuc= '%X' % ciphertext
    return ((128 - len(sonuc)) * '0') + sonuc