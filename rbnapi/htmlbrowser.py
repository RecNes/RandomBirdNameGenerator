# -*- coding: utf-8 -*-
import gzip
import inspect
from json import loads
import re
import shelve
from time import time, sleep
from urllib import urlencode, quote_plus
from urllib2 import AbstractHTTPHandler
import sys
from html_tools import mechanize
from html_tools.inputlar import inputlar
from rbnapi.rb_logger import log


__author__ = 'Remind Bird'


class HtmlCleaner():
    def __init__(self):
        self.re_js = re.compile(
            '(<javascript.*?/javascript>|<head.*?/head>|<style.*?/style>|<script.*?/script>|<.*?>|</.*?>|&nbsp;)',
            (re.I | re.DOTALL))
        self.re_br = re.compile('(<BR.*?>|<P.*?>|<tr.*?>)', (re.I | re.DOTALL))

    def cleanup(self, content):
        result = self.re_js.sub(' ', self.re_br.sub('\n', content)).split('\n')
        result = [s for s in result if s.strip()]
        return '\n'.join(result)


class BrowserHTTPHandler(AbstractHTTPHandler):
    """
    host, Content-val_type ve content-length gibi Browser.addheaders yada default_headers ile guncellenemeyen
    headerlar için Handler sınıfı...
    """
    def __init__(self, headers=None):
        AbstractHTTPHandler.__init__(self)
        if not headers:
            headers = {}
        self.headers_to_override = headers

    def http_request(self, request):
        if self.headers_to_override:
            for key, value in self.headers_to_override.items():
                request.add_unredirected_header(key.capitalize(), value)
        return request

    https_request = http_request


class HTMLBrowser():
    """
    Yeniden revize edilmiş Tarayici sınıfı
    """
    def __init__(self):
        HTMLBrowser.__init__(self)

        self.urls = {}
        self.default_headers = {
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,'
                      'image/png,*/*;q=0.5',
            'Accept-Charset': 'utf-8;q=0.7,*;q=0.7',
            'Accept-Language': 'tr,en-us;q=0.7,en;q=0.3',
            'Connection': 'keep-alive',
            'Keep-Alive': '300',
            'Accept-Encoding': 'gzip,deflate',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        }
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        # self.browser.set_handle_redirect(Mechanize.HTTPRedirectHandler)
        self.__make_cj()
        self.last_url = ''
        self.html_cleaner = HtmlCleaner()
        self._stringUrlEncode = urlencode
        self.output_stack = []
        self.output_stack_raw = []
        self.err_reason = ''
        self.generic_err = ''
        self.result_dict = {}
        self.err_dict = {}
        self.logged_in = False
        self.last_content = ''
        self.response_headers = ''
        self._set_proxy()
        self.info_required = {}
        self.received_info = {}
        self.response_headers_info = None
        self.referer = ''
        self.user = None
        self.time_stamp = 0
        self.codeGen = None  # odeyen modelinin metodu bunun uzerine atanmali
        self.sessionGen = None  # odeyen modelinin metodu bunun uzerine atanmali
                                 # #PTT gibi tek oturumda cok islem yapilabilen sistemlerde kullanilabilir.
        self.sess_hash = ''
        self.instance = False
        self.smsGen = None
        self.billToControl = None

        # Başla: banka.__init__ de override edilecek değişkenler
        self.safestr = '±'  # self.UnicodeUrlEncode fonksiyonunda quote_plus'ın encode edemediği karakterler için
                            # değişim karaterini belirtir
        self.defaultReferer = ''
        self.login = True
        self.info = True
        self.time_out = 0
        self.generic_err_texts = []
        self.relogin_texts = []
        self.generic_err_texts = []
        self.oid = 0
        self.login_cred_number = 3
        self.logname = 'htmlbrowser'
        self.marker = "Oid: {}".format(self.oid)
        self._make_loger()
        # Bitti: banka.__init__ de override edilecek değişkenler

    def _make_loger(self, logname=''):
        """
        logname  : Log dosya adı. Verilmemesi durumunda self.logname kullanılır.

        Loglayıcıya dışarıdan direkt erişim olmamalı. Dolayısıyla da self.__log olarak isimlendiriyoruz. Böylece
        loglayıcıya erişim sadece self.logit üzerinden olacak
        """
        self.logname = logname or self.logname or 'ttfo'
        self.__log = log

    def logit(self, prompt, val_type='info'):
        """
        Merkezi loglama methodu
        prompt: loglanacak prompt
        val_type: loglama seviyesi. Mevcut seviyeler: critical, debug, error, exception, fatal, info, warn, warning
        """
        try:
            _stack = inspect.stack()[1]
            _stack_data = '{} betiği {} methodu satir {} :'.format(_stack[1], _stack[3], _stack[2])
        except Exception as e:
            self.__log.exception(e)
            _stack_data = ''
        try:
            getattr(self.__log, val_type, self.__log.info)("{} Oid:{} Log:{}".format(repr(_stack_data),
                                                                                     repr(self.marker), repr(prompt)))
        except Exception as e:
            self.__log.exception("Hareket loglanamadı: {}".format(repr(e)))

    def _clean_output_stack(self):
        """
        Döngü içerisnde çalışan bankalar için, bankanın yeni işleme başlamadan, önceki işleme ait çıktı ve iletilerin
        sıfırlanmasını sağlar
        """
        self.output_stack = []
        self.output_stack_raw = []
        self.err_reason = ''
        self.generic_err = ''
        self.result_dict.clear()

    # def uzakcodeGen (self):
    #     return uzak_smsGen(self.sinif_tanimi, self.log)

    def ___timed_out(self):
        """
        self.time_out tanimlandıyse, yeni işleme başlamadan önce oturumun time aşımına uğrayıp uğramadığı bilgisini
        döndürür.
        """
        if self.time_out:
            _time_diff = time() - self.time_stamp
            _time_off = self.time_out <= _time_diff
            self.logit('Last Porc: {} Sys Time: {}, Diff: {} Session Timed Out?: {}'.format(
                       self.time_stamp, time(), _time_diff, _time_off))
            return _time_off

    def _make_permanent_session(self):
        if hasattr(self, 'db'):
            if self.logged_in:
                self.db['session'] = self._get_session()
                self.db['time'] = time()
            else:
                del self.db['session']
            self.db.close()

    def _get_permanent_session(self, period):
        self.db = shelve.open('{}_session.db'.format(self.logname), writeback=True)
        if self.db.get('time') and time() - self.db.get('time') <= period:
            self._make_session(self.db['session'])
            print 'session yukleniyor'
            return True
        else:
            print 'session yok yada eski, login yapilmali'

    def __session_generator2(self):
        if self.sessionGen:
            _ohash, _session, _time = self.sessionGen()
            self.logit('sessionGen available...')
            _time_diff = time() - _time
            if _session and self.sess_hash != _ohash and _time_diff <= self.time_out:
                self.logit('session refreshed with sessionGen')
                self._make_session(_session)
                self.sess_hash = _ohash
                self.logged_in = True
                self.time_stamp = _time
            elif (_time_diff > self.time_out) and _ohash:
                self.sessionGen(erase=True)
                self.logit('Session timed out; time diff: {}, self.hash: {} ohash: {}'.format(_time_diff,
                           self.sess_hash, _ohash))
            else:
                self.logit('Session is invalid; time diff: {},  ohash: {}'.format(_time_diff, _ohash))

    def _daily_session(self, infos=None, user=None):
        """
        infos    : Oturum gerektiren sistemler için giriş bilgilerini barındırır. Oturum açıldıktan sonra oturumla
                        ilgili datas (cookie, session kaydı vs) bu sözlükle aktarılır.
        user        : Bazı sistemlerde kullanızı bazlı bazı işlevler olduğu için ilgili kullanıcı bilgisinin
                        aktarılmasında kullanılır.
        Oturum durumunu ve session süre aşımını kontrol eden ve gerekli durumlarda isteği _sign_in methoduna yönlendiren
        methoddur.
        """
        if infos is None:
            infos = {}
        try:
            if user:
                self.user = user
            self.__session_generator2()

            if infos and 'session' in infos:
                self._make_session(infos['session'])
                self.logit('Session refreshed with infos')

            if self.__info_required() and 'data' in infos:
                self.__login_credentials()

            if self.logged_in and self.___timed_out():
                self.logit('Session timed out')
                self.logged_in = False

            if not self.logged_in:
                if self._sign_in():
                    if self.sessionGen:
                        self.sessionGen(self._get_session())
                self.logit('Login result: {}'.format(self.logged_in))

            return self.logged_in
        except Exception as e:
            self.logit(e, val_type='exception')
            self.logit('Unexpected error on Signing in! Credentilas: {}'.format(infos), val_type='exception')

    @property
    def _info_check(self):
        """
        methodun döndürdüğü value herhangi bir işe yaramıyor gibi...
        Yeniden revize edildi, test edilmesi lazım...
        """
        return True
        # response = None
        # if self.info_required:
        #     _bellek = onbellek('info_required', self.user.id)
        #     bg = _bellek.al({})
        #     try:
        #         bg.update(self.info_required)
        #         _bellek.ata(bg)
        #         self.logit('Gerekli infos istendi: {}'.format(self.info_required))
        #         say = 0
        #         for b, d in self.info_required.items():
        #             _bellek_alt = onbellek(b, self.user.id)
        #             try:
        #                 self.received_info[b] = _bellek_alt.al()
        #                 while not self.received_info[b]:
        #                     say += 1
        #                     sleep(2)
        #                     self.received_info[b] = _bellek_alt.al()
        #                     self.logit('Deneme {}, alinan info ( {} ) henuz alinamadi'.format(say,
        #                                                                                 self.received_info[b]))
        #                     if not self.received_info[b]:
        #                         self.logit('Deneme {}, istenen info ( {} ) henuz alinamadi'.format(say, b))
        #                         if say >= 50:
        #                             self.logit('Istenen info ( {} ) alınamadı. Vazgeçiyoruz.'.format(b))
        #                             break
        #                         else:
        #                             continue
        #                     else:
        #                         pass
        #             except Exception as e:
        #                 self.logit('Bilgileri almaya çalışırken bir hata oluştu: {}'.format(repr(e)))
        #             finally:
        #                 self.logit('Deneme {}, istenen info ( {} ) {}'.format(say, b,
        #                            ('alindi' if self.received_info[b] else 'alınamadı')))
        #                 _bellek_alt.erase()
        #                 self.info_required.pop(b, None)
        #                 if self.received_info[b]:
        #                     self.logit('Alinan info:: {} >> {}'.format(b, self.received_info[b]))
        #                     if len(d) >= 3:
        #                         if d[2]:
        #                             getattr(self, d[2])(self.received_info[b])
        #                         elif d[2] is None:
        #                             response = self.received_info[b]
        #                     break
        #                 else:
        #                     pass
        #     except Exception as e:
        #         self.logit('Bilgileri almaya çalışırken bir hata oluştu: {}'.format(repr(e)))
        #     finally:
        #         for k in self.received_info:
        #             bg.pop(k, {})
        #         _bellek.ata(bg)
        # else:
        #     self.logit('Bu modul icin su anda fazladan info gerekmiyor: {}'.format(self.logname))
        # response = response or bool(self.received_info or not self.info_required)
        # self.logit('BilgiKontrolu sonucu: {}'.format(response))
        # return response

    def __login_credentials(self):
        self.logged_in = True

    @staticmethod
    def _process_login_cred(infos):
        return infos if (type(infos) in (tuple, list)) else map(lambda x: x.strip(), loads(str(infos)))

    def _set_proxy(self):
        """
        Tarayiciya proxy tanımlanmasını sağlar. İlgili class içerisinde self.proxies değişkeniyle proxy verisi girilmeli
        ve ardından bu method çağırılmalıdır
        """
        if hasattr(self, 'proxies') and getattr(self, 'proxies'):
            self.browser.set_proxies(self.proxies)
            self.logit('Proxy setted: {}'.format(repr(self.proxies)))

    def __make_cj(self):
        self.cj = mechanize.CookieJar()

    def _search_in_clean_content(self, m):
        try:
            return filter(lambda x: x in m, self.output_stack)
        except Exception as e:
            self.logit(e, val_type='exception')
            self.logit('Error on searching in stack', val_type='exception')

    def _search_content(self, m, content=None):
        """
        Verilen içerikte belirtilen tümcenin bulunma durumunu döndürür. content belirtilmezse last_content içerisinde
        arama yapar
        """
        if content is None:
            content = self.last_content
        return m in content

    def _search_in_all_content(self, m):
        try:
            return filter(lambda _x: m in _x, repr(self.output_stack_raw))
        except Exception as e:
            self.logit(e, val_type='exception')
            self.logit('Error on searching in all content', val_type='exception')

    def __login_required(self):
        if not self.login:
            self.logged_in = True
        return self.login

    def _sign_in(self):
        """
        Banka tarafından override edilmediyse giriş yapmaya da gerek yok demektir.
        """
        self.logged_in = True
        return self.logged_in

    def _get_session(self):
        return self.cj

    def _make_session(self, cj):
        self.cj = cj

    @staticmethod
    def balance():
        """
        Dummy method. Banka tarafından override edilmediği durumda hata oluşmasını engellemek için
        boş sözlük döndürelim
        """
        return {}

    def _return_response(self, response):
        self.logit('Response returning: {}'.format(repr(response)))
        if self.err_reason or self.generic_err:
            self.logit('Browser errors: {}'.format(self.err_reason or self.generic_err))
        response = {
            'response': response, 'raw_response': self.output_stack_raw,
            'hata': self.err_dict.get(self.err_reason) or self.generic_err,
            'err_reason': self.err_reason, 'cikti': self.output_stack
        }
        response.update(self.result_dict)
        self.logit('Common error: {}, Error reason:{} '.format(self.generic_err, self.err_reason))
        self._clean_output_stack()
        if self.sessionGen and not self.err_reason:
            self.sessionGen(self._get_session())
        return response

    def __info_required(self):
        return self.info

    def form_to_dict(self, set_multi_select=False):
        """
        Formu inputlara girilen verilrle birlikte sözlüğe dönüştürür.
        set_multi_select: eger formda çoktan seçmeli alan varsa (combobox/radio vs) ve bu alanda tek bir
        seçenek mevcutsa o seçeneği alır. Birden fazla seçenek varsa hali hazırda seçilen değeri alır

        """
        fields = {}
        for k in self.browser.form.controls:
            if set_multi_select and type(k.value) is list and len(k.value) == 1:
                fields[k.name] = k.value[0]
            else:
                fields[k.name] = k.value
        return fields

    def fcontrol(self, name, value=None, values_dict=None):

        """
        secili formda adı verilen anahtarı bularak belirtilen değeri atar, belirtilen anahtar yoksa yeni bir tane
        form alanı oluşturur.
        name          : Form alanı adı. Belirtilen isimde bir alan yoksa yeni bir form alanı oluşturur
        value       : Belirtilen alana verilen değeri atar.
        values_dict  : İlgili alana doğrudan bu değer sözlüğünü atar. value parametresine göre daha yüksek önceliklidir
        """
        if not value and not values_dict:
            self.logit("value or values_dict parameters required", val_type='exception')
            raise Exception("Value required")
        try:
            _alan = self.browser.form.find_control(name=name)
            _alan.readonly = False
            _alan.disabled = False
            _alan.value = values_dict['value'] if values_dict else value
        except mechanize.AmbiguityError:
            self.logit("{} = {} Many form fields found in same name".format(name, (values_dict or value)),
                       val_type='debug')
            self.browser.form.new_control('Text', name, (values_dict or {'value': value}))
        except mechanize.ControlNotFoundError:
            self.logit("{} = {} No form field, new one appending".format(name, (values_dict or value)),
                       val_type='debug')
            self.browser.form.new_control('Text', name, values_dict or {'value': value})
        except Exception as e:
            self.logit(e, val_type='exception')
            try:
                self.browser.form.new_control('Text', name, values_dict or {'value': value})
            except Exception as e:
                self.logit(e, val_type='exception')
                self.logit("{} = {} Unable to append new form field".format(name, (values_dict or value)),
                           val_type='exception')

    def flist(self, name, value, status=True):
        """
        Formda adı verilen alanda belirtilen seçeeği bularak seçili/seçili değil hale getirir
        name      : Form alanının adı
        value   : Seçili/seçili değil hale getirilecek seçenek
        status   : belirtilen seçenek seçili mi yoksa seçili değil mi haline getirilecek?
        """
        try:
            self.browser.find_control(str(name)).get(str(value)).selected = status
        except Exception as e:
            _options = self.browser.find_control(str(name)).items
            self.logit(e, val_type='exception')
            self.logit("Expected option not availabe in form field. available options: {}".format(_options),
                       val_type='exception')
        raise Exception("Expected option not availabe in form field")

    def flistin(self, name, value, status=True):
        """
        Formda adı verilen alanda belirtilen seçeeği bularak seçili/seçili değil hale getirir
        flist'ten farkı, value'in tamamını aramaz, içerisinde value parametresindeki değer geçen ilk seçeneği seçer
        name      : Form alanının adı
        value   : Seçili/seçili değil hale getirilecek seçenek
        status   : belirtilen seçenek seçili mi yoksa seçili değil mi haline getirilecek?
        """
        _select = None
        for i in self.browser.find_control(str(name)).items:
            if value in i.name:
                _select = i
                break
        try:
            _select.selected = status
        except:
            _options = self.browser.find_control(str(name)).items
            self.logit("Expected option not availabe in form field. available options: {}".format(_options),
                       val_type='exception')
            raise Exception("Expected option not availabe in form field")

    @property
    def _cli_login_cred(self):
        """
        Komut satırından banka test edilirken banka giriş bilgilerinin verilmesini sağlar.
        Ör:

        python <betik_adi>.py credentials=1234,1234,1234
        """
        for a in sys.argv:
            if 'credentials' in a:
                return a.replace('credentials=', '').split(',')
        print("Write credentials seperated with commas without spaces: " +
              "{} credentials=324324,23423,34234".format(sys.argv[0]))
        sys.exit()

    def __login_needed(self):
        """

        """
        for c in self.relogin_texts:  # + self.generic_err_texts:
            if self._search_content(c, self.last_content):
                self.err_reason = c
                self.logit("Relogin needed: {}".format(c))
                self.logged_in = False
                return True
        self.logit("Relogin not needed...")

    def __temp_err_available(self):
        """

        """
        for k, v in self.err_dict.items():
            if self._search_in_all_content(k):
                self.logit("Error: {}: {}".format(k, v))
                self.err_reason = v
                return True

    def __login_check(self):
        self.logit("Login check")
        if not self.__login_required() or not self.__login_needed():
            return True
        else:
            self.logit("Relogin...")
            sleep(3)
            self.__make_cj()
            # self.sess = ''
            self._daily_session()
            if self.__login_needed():
                self.logit("Relogin unsuccessful...")
            else:
                self.logit("Reloged in...")
                # self.tekrar_sorgula = True
                return True

    def __check_out(self, val_type='t'):
        """
        Hata durumunu ve oturumu kontrol eder. Gerekiyorsa yeniden giriş yapar
        val_type     :
            't'   : tum kontroller,
            'g'   : sadece login kontrolu,
            'h'   : sadece hata kontrolleri,
            ''    : kontrol yapilmaz.
        """
        self.logit("Session and error check" if val_type else "Check unnecessary...")
        if val_type in ['t', 'g']:
            if not self.__login_check():
                self.logit("Sign in check failed")
                self.generic_err = u'Signing in failed'
                return
        if val_type in ['t', 'h']:
            if self.__temp_err_available():
                self.generic_err = u"Can not login. Try again later."
                return
        return True

    def __un_gzip(self, response):
        """
        Yapılan isteğe gelen yanıt gzip ise, paketi açarak browser nesnesinin yaniti olarak atar.
        response   : gzip olarak gelen response
        """

        _gz = gzip.GzipFile(fileobj=response, mode='rb')
        _content = _gz.read()
        _gz.close()
        response.set_data(_content)
        self.browser.set_response(response)

    def __process_content(self, raw_response, rsp_enc='iso-8859-9', ursp_enc=None):
        """
        raw_response       : işlenecke içerik metni
        rsp_enc     : self.rsp değişkenine atanacak içeriğin enciding tipi
        ursp_enc    : self.ursp değişkenine atanacak içeriğin enciding tipi

        gelen yanıtı işleyerek üç değişkene değer ataması yapar:
            self.last_content  : gelen yanıtı işlemeden bu değişkene yazar
            self.rsp         : gelen yanıttaki \r ve \n karakterleri çıkartılır, belirtilen encodinge göre decode edilir
            self.ursp        : gelen yanıttaki \r ve \n karakterleri çıkartılır, belirtilen encodinge göre decode edilir
        """
        self.last_content = raw_response
        _content = raw_response.replace('\n', '').replace('\r', '')
        # self.rsp değerini işleyerek atayalım...
        try:
            if rsp_enc is not None:
                _rsp = _content.decode(rsp_enc, 'replace')
            else:
                _rsp = _content
        except Exception as e:
            self.logit("Error occured during creation of self.rsp: {}".format(repr(e)))
            _rsp = ''
        self.rsp = _rsp
        # self.ursp değerini işleyerek atayalım...
        try:
            if ursp_enc is not None:
                _ursp = _content.decode(ursp_enc, 'replace')
            else:
                _ursp = _content
        except Exception as e:
            self.logit("Error occured during creation of self.ursp: {}".format(repr(e)))
            _ursp = ''
        self.ursp = _ursp

    def submit_form(self, sel_form=0, name=None, nr=None, headers=None, control='t'):
        """
        Formu işleyerek mechanize.submit methoduyla gönderir.
        sel_form    :
                      0: Seçme
                      1: Submitten sonra seç
                      2: Form seç, submit et ve sonraki sayfada tekrar seç
        name        : Seçilecek formun ismi
        nr          : Seççilecek formun tüm formlar listesindeki index'i
        headers     : Eklenecek/güncellenecek istek başlıkları bir sözlük olarka verilmelidir
        control       : __check_out methoduna verilecek kontrol tipi
        """
        if control and not self.__check_out(control):
            raise Exception("Session and Error control: {}".format(self.generic_err))
        if sel_form == 2:
            if name is not None:
                self.browser.select_form(name=name)
            else:
                if nr is None:
                    nr = 0
                self.browser.select_form(nr=nr)
        self.logit("Mechanize action: {}".format(self.browser.form.action))
        if headers:
            dh = self.default_headers
            self.browser.set_handle_referer(False)
            dh.update(headers)
            self.browser.addheaders = dh.items()
        else:
            self.browser.set_handle_referer(True)
        self.logit("Req Headers: \n\n{}".format("\n".join(map(lambda x: repr(x).replace(', ', ': '),
                                                              self.browser.request.header_items()))))
        try:
            self.browser.submit()
        except Exception as e:
            self.logit("Server not responding: {}".format(repr(e)))
            raise Exception("Server not responding")
        self.time_stamp = time()
        self.logit("Mechanize data:  \n\n{}".format(self.browser.request.data.replace('&', '\n').replace("=", ': ')))
        if self.browser.response().info().get("Content-Encoding"):
            if self.browser.response().info()['Content-Encoding'] == 'gzip':
                self.__un_gzip(self.browser.response())
        self.__process_content(self.browser.response().read())
        self.output_stack.append(self.html_cleaner.cleanup(self.last_content))
        self.output_stack_raw.append(self.last_content)
        self.logit("Resp Headers: \n\n{}".format(self.browser.response().info()))
        self.logit("HTML Response: \n\n{}".format(self.last_content), val_type='debug')
        self.logit("Response: \n\n{}".format(self.html_cleaner.cleanup(self.last_content).strip()))
        if sel_form in [1, 2]:
            try:
                if name is not None:
                    self.browser.select_form(name=name)
                else:
                    if nr is None:
                        nr = 0
                    self.browser.select_form(nr=nr)
                if self.browser.form:
                    self.logit("Form sent and new form selected.")
            except Exception as e:
                self.logit("Form unable to select: {}".format(repr(e)))
        self.last_url = self.browser.response().geturl()

    def _unicode_url_enc(self, data):
        """
        urllib.urlencode'un aksine, veriyi quote etme işleminden önce str'ye çevirmeye çalışmaz.
        str türkçe karkaterleri ascii'ye çevirirken hata veriyor
        """
        _data = []
        for v in data.keys():
            if type(v) != unicode:
                v = str(v)
            if type(data[v]) != unicode:
                data[v] = str(data[v])
            try:
                _data.append("{}={}".format(quote_plus(v.encode('iso-8859-9'), self.safestr),
                                            quote_plus(data[v].encode('iso-8859-9'), self.safestr)))
            except Exception as e:
                self.logit(e, val_type="exception")
                _data.append("{}={}".format(quote_plus(v, self.safestr), quote_plus(data[v], self.safestr)))
        return '&'.join(_data)

    def url_link(self, url, datas=None, head=None, control='t', url_enc_seq=None):  # TODO
        """
        url         : İstek yapılacak URL
        datas     : Veri POST methodu ile yollanacaksa, gönderilecek datas bu sözlük içerisinde verilmelidir
        approve        : Gidilen sayfada verilen approve tümcesi aranır. Kullanımı durumunda bağ methodunun döndüreceği
                    değere bakılmalıdır
        head        : İstek header'larına eklenecek yada güncellenecek datas
        urlSoneki   : Mevcut sayfa ve gidilecek sayfa için URL'ye ve referer'a eklenecek sonEk.
        control       : __check_out methoduna verilecek kontrol tipi
        """
        if not url_enc_seq:
            url_enc_seq = [self._unicode_url_enc, self._stringUrlEncode]
        if type(url) in [list, tuple] and len(url) == 2:  # url'nin 2.kısmı referer bilgisi
            _referer = url[1]
        elif self.last_url:  # son tarayici hareketi self.last_url'yi atamışsa referer olarak onu kullanıyoruz
            _referer = self.last_url
        elif self.defaultReferer:  # defaultReferer tanımlanmışsa onu kullanalım
            _referer = self.defaultReferer
        else:  # referer yok...
            _referer = ''
        if not _referer.startswith('http'):
            _referer = "{}{}".format(self.urls['domain'], _referer)
        self.default_headers['Referer'] = _referer
        # Referer ayarlandıktan sonra self.last_url'yi sonraki gidilecek url olarak ayarlıyoruz...
        if type(url) in [list, tuple]:
            url = url[0]
        self.last_url = url
        if 'http' not in self.last_url:
            self.last_url = self.urls['domain'] + self.last_url
        self.logit(u'\n\r\n\rReferrer: {rfr}\n\rTarget: {tgt}'.format(rfr=_referer, tgt=self.last_url),
                   val_type='debug')
        # Verileri encode edelim...
        if not (datas is None or type(datas) in [str, unicode]):
            for _encode_method in url_enc_seq:
                try:
                    datas = _encode_method(datas)
                except Exception as e:
                    self.logit(e, val_type="exception")
                    pass
                else:
                    self.logit("Encoded datas for POST method: {}".format(datas))
        else:
            pass  # encode edilecek POST verisi yok...
        self.browser.set_cookiejar(self.cj)
        headers = self.default_headers
        if head:
            # # Content-val_type normal yollarla guncellenemeyen header.. Onun için farklı bir handler kulalnacağız..
            # if 'Content-val_type' in head.keys():
            #     self.browser.add_handler(TarayiciHTTPHandler({'Content-val_type':head['Content-val_type']}))
            #     head.pop('Content-val_type')
            # TODO: gorunuse gore yeni mechanizede bu işler daha farklı bir şekilde oluyor...
            headers.update(head)
        self.browser.addheaders = headers.items()
        try:
            http_response = self.browser.open(self.last_url, datas)
            self.response_headers = http_response.info()
            self.response_headers_info = http_response.info().headers
            self.logit(self.response_headers_info, val_type='debug')
            if http_response.info().get('Content-Encoding'):
                if http_response.info()['Content-Encoding'] == 'gzip':
                    self.logit("Extract G-Zip")
                    self.__un_gzip(http_response)
                else:
                    self.logit("Encoding is not g-zip...")
            self.time_stamp = time()
            if self.browser.request.data:
                self.logit("Request data: {}".format(self.browser.request.data.replace('&', '\n').replace("=", ': ')))
            self.logit("Response headers: {}".format(self.browser.response().info()), val_type='debug')

            content = http_response.read()
        except Exception as e:
            self.logit("Cannot connect to URL: {}".format(repr(e)), val_type='exception')
            self.logit("URL: {} \r\nRequest Datas: {}".format(
                repr(self.last_url), repr(datas), val_type='exception'
            ))
            content = ''
        self.__process_content(content)
        self.output_stack.append(self.html_cleaner.cleanup(self.last_content))
        self.output_stack_raw.append(self.last_content)
        if control and not self.__check_out(control):
            raise Exception("Session and Error check: {}".format(self.generic_err))

    def _get_tokens(self, key):
        try:
            parser = inputlar()
            token = parser.feed(self.last_content, key)[0]
            parser.reset()
        except Exception as e:
            self.logit(e, val_type='exception')
            self.logit('{} object not parsed'.format(key), val_type='exception')
            token = ''
        return token
