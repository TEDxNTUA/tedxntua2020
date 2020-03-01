from urllib.parse import urlparse

from django.utils.http import is_same_domain


def is_url_same_domain(request, url):
    if url is None:
        return False

    url = urlparse(url)
    return is_same_domain(url.netloc, request.META['HTTP_HOST'])
