from django.http import HttpResponse

from html_tools.slimmer import slimmer


class CompressHtmlMiddleware(object):

    def process_response(self, request, response):
        if isinstance(response, HttpResponse) and \
            response.get('Content-Type',None).find('text/html;')==0:
            response.content = slimmer.xhtml_slimmer(response.content)
        return response
