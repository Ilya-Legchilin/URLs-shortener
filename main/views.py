import logging

from django.shortcuts import render, redirect
from main.services import *


def index(request):
    """Return render to html page with context

        Get url via post request. If url not given that means that
        session map is empty. We initialize list of urls.

        If url is given we make an object Mapping and check whether
        such url is already stored. If not then we store it with subpart.

        If such a subpart is already used we return and get http response.
        Else we save mapping in mysql and in session.
        
    """
    new_url = request.POST.get('new_url', None)
    subpart = request.POST.get('subpart', None)
    handle_new_url_and_subpart(request, new_url, subpart)
    context = get_pagination_context(request)
    return render(request, 'main.html', context=context)


def redirect_to_website(request, slug):
    """Return web-site with long url which corresponds to slug

    """
    url_from_cache = redirect_from_cache(slug)
    url_from_database = redirect_from_database(slug)
    if url_from_cache != None:
        return redirect(url_from_cache)
    elif url_from_database != None:
        return redirect(url_from_database)
    else:
        return HttpResponse("Нет такого адреса!")