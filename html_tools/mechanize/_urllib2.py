# urllib2 work-alike interface
# ...from urllib2...
# ...and from mechanize
# crap ATM
## from _gzip import \
##      HTTPGzipProcessor
import httplib
if hasattr(httplib, 'HTTPS'):
    del httplib
