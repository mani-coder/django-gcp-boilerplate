# Standard Library Imports
import json

# Third Party Library Imports
# Django Imports
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class NonHtmlDebugToolbarMiddleware(MiddlewareMixin):
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug)
    Special handling for json (pretty printing) and
    binary data (only show data length)
    """

    def process_response(self, request, response):
        if request.GET.get("debug") is not None:
            if response["Content-Type"] == "application/octet-stream":
                new_content = "<html><body>Binary Data, " "Length: {}</body></html>".format(len(response.content))
                response = HttpResponse(new_content)
            elif response["Content-Type"] != "text/html":
                content = response.content
                try:
                    json_ = json.loads(content)
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse("<html><body><pre>{}" "</pre></body></html>".format(content))

        return response
