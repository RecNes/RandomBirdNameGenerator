from html_tools.mechanize import _urllib2

__all__ = [
    'AbstractBasicAuthHandler',
    'AbstractDigestAuthHandler',
    'BaseHandler',
    'Browser',
    'BrowserStateError',
    'CacheFTPHandler',
    'ContentTooShortError',
    'Cookie',
    'CookieJar',
    'CookiePolicy',
    'DefaultCookiePolicy',
    'DefaultFactory',
    'FTPHandler',
    'Factory',
    'FileCookieJar',
    'FileHandler',
    'FormNotFoundError',
    'FormsFactory',
    'HTTPBasicAuthHandler',
    'HTTPCookieProcessor',
    'HTTPDefaultErrorHandler',
    'HTTPDigestAuthHandler',
    'HTTPEquivProcessor',
    'HTTPError',
    'HTTPErrorProcessor',
    'HTTPHandler',
    'HTTPPasswordMgr',
    'HTTPPasswordMgrWithDefaultRealm',
    'HTTPProxyPasswordMgr',
    'HTTPRedirectDebugProcessor',
    'HTTPRedirectHandler',
    'HTTPRefererProcessor',
    'HTTPRefreshProcessor',
    'HTTPResponseDebugProcessor',
    'HTTPRobotRulesProcessor',
    'HTTPSClientCertMgr',
    'HeadParser',
    'History',
    'LWPCookieJar',
    'Link',
    'LinkNotFoundError',
    'LinksFactory',
    'LoadError',
    'MSIECookieJar',
    'MozillaCookieJar',
    'OpenerDirector',
    'OpenerFactory',
    'ParseError',
    'ProxyBasicAuthHandler',
    'ProxyDigestAuthHandler',
    'ProxyHandler',
    'Request',
    'RobotExclusionError',
    'RobustFactory',
    'RobustFormsFactory',
    'RobustLinksFactory',
    'RobustTitleFactory',
    'SeekableResponseOpener',
    'TitleFactory',
    'URLError',
    'USE_BARE_EXCEPT',
    'UnknownHandler',
    'UserAgent',
    'UserAgentBase',
    'XHTMLCompatibleHeadParser',
    '__version__',
    'build_opener',
    'install_opener',
    'lwp_cookie_str',
    'make_response',
    'request_host',
    'response_seek_wrapper',  # XXX deprecate in public interface?
    'seek_wrapped_response',   # XXX should probably use this internally in place of response_seek_wrapper()
    'str2time',
    'urlopen',
    'urlretrieve',
    'urljoin',

    # ClientForm API
    'AmbiguityError',
    'ControlNotFoundError',
    'FormParser',
    'ItemCountError',
    'ItemNotFoundError',
    'LocateError',
    'Missing',
    'ParseFile',
    'ParseFileEx',
    'ParseResponse',
    'ParseResponseEx',
    'ParseString',
    'XHTMLCompatibleFormParser',
    # deprecated
    'CheckboxControl',
    'Control',
    'FileControl',
    'HTMLForm',
    'HiddenControl',
    'IgnoreControl',
    'ImageControl',
    'IsindexControl',
    'Item',
    'Label',
    'ListControl',
    'PasswordControl',
    'RadioControl',
    'ScalarControl',
    'SelectControl',
    'SubmitButtonControl',
    'SubmitControl',
    'TextControl',
    'TextareaControl',
    ]

import logging
import sys

from _version import __version__









# high-level stateful browser-style interface
from html_tools.mechanize._mechanize import \
     Browser, History, \
     BrowserStateError, LinkNotFoundError, FormNotFoundError

# configurable URL-opener interface
from html_tools.mechanize._useragent import UserAgentBase, UserAgent
from html_tools.mechanize._html import \
     Link, \
     Factory, DefaultFactory, RobustFactory, \
     FormsFactory, LinksFactory, TitleFactory, \
     RobustFormsFactory, RobustLinksFactory, RobustTitleFactory

# urllib2 work-alike interface.  This is a superset of the urllib2 interface.
from html_tools.mechanize._urllib2 import *

if hasattr(_urllib2, "HTTPSHandler"):
    __all__.append("HTTPSHandler")
del _urllib2

# misc
from html_tools.mechanize._http import HeadParser
from html_tools.mechanize._http import XHTMLCompatibleHeadParser
from html_tools.mechanize._opener import ContentTooShortError, OpenerFactory, urlretrieve
from html_tools.mechanize._response import \
     response_seek_wrapper, seek_wrapped_response, make_response
from html_tools.mechanize._rfc3986 import urljoin
from html_tools.mechanize._util import http2time as str2time

# cookies
from html_tools.mechanize._clientcookie import Cookie, CookiePolicy, DefaultCookiePolicy, \
     CookieJar, FileCookieJar, LoadError, request_host_lc as request_host, \
     effective_request_host
from html_tools.mechanize._lwpcookiejar import LWPCookieJar, lwp_cookie_str
# 2.4 raises SyntaxError due to generator / try/finally use
if sys.version_info[:2] > (2,4):
    try:
        import sqlite3
    except ImportError:
        pass
    else:
        from html_tools.mechanize._firefox3cookiejar import Firefox3CookieJar
from html_tools.mechanize._mozillacookiejar import MozillaCookieJar
from html_tools.mechanize._msiecookiejar import MSIECookieJar

# forms
from html_tools.mechanize._form import (
    AmbiguityError,
    ControlNotFoundError,
    FormParser,
    ItemCountError,
    ItemNotFoundError,
    LocateError,
    Missing,
    ParseError,
    ParseFile,
    ParseFileEx,
    ParseResponse,
    ParseResponseEx,
    ParseString,
    XHTMLCompatibleFormParser,
    # deprecated
    CheckboxControl,
    Control,
    FileControl,
    HTMLForm,
    HiddenControl,
    IgnoreControl,
    ImageControl,
    IsindexControl,
    Item,
    Label,
    ListControl,
    PasswordControl,
    RadioControl,
    ScalarControl,
    SelectControl,
    SubmitButtonControl,
    SubmitControl,
    TextControl,
    TextareaControl,
    )

# If you hate the idea of turning bugs into warnings, do:
# import mechanize; mechanize.USE_BARE_EXCEPT = False
USE_BARE_EXCEPT = True

logger = logging.getLogger("mechanize")
if logger.level is logging.NOTSET:
    logger.setLevel(logging.CRITICAL)
del logger
