import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from hashids import Hashids
import redis

from .models import Mapping


logger = logging.getLogger(__name__)


def shorten_url(long_url):
    """Return short url

    function that makes long url short usind hashids library

    """
    hashids = Hashids(long_url)
    short_url = hashids.encode(1, 2, 3)
    return short_url


def get_pagination_context(request):
    """Return context for pagination"""

    paginator = Paginator(request.session['urls_list'], 6)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
        }

    return context


def handle_new_url_and_subpart(request, new_url, subpart):
    if 'urls_list' not in request.session:
        request.session['urls_list'] = []
    if new_url != None:
        all_mappings = Mapping.objects.all()
        if this_url_is_already_stored(new_url, all_mappings):
            return
        mapping = Mapping()
        mapping.long_url = new_url
        mapping.session_key = request.session._session_key
        all_mappings = Mapping.objects.all()
        if subpart == '':
            mapping.short_url = shorten_url(new_url)
        else:
            if this_subpart_is_already_used(subpart):
                return HttpResponse('Такой subpart уже используется')
            else:
                mapping.short_url = subpart
        store_new_mapping(request, mapping)


def store_new_mapping(request, mapping):
    """Return None
        
        Stores mapping into mysql and session
        Puts a message into debug log
        
    """
    msg = 'new url for ' + mapping.long_url + ' is ' + mapping.short_url
    logger.debug(msg)
    mapping.save()
    request.session['urls_list'].append([mapping.long_url, mapping.short_url])
    request.session.modified = True
    
    
def this_subpart_is_already_used(subpart, all_mappings):
    """ Returns True if such a subpart was already used

        Return False if it was not
    """
    for elem in all_mappings:
        if elem.short_url == subpart:
            msg = 'subpart ' + subpart + ' is already used'
            logger.debug(msg)
            return True
    return False


def this_url_is_already_stored(url, all_mappings):
    """ Returns True if such an url was already stored

        Return False if it was not
    """
    for elem in all_mappings:
        if elem.long_url == url:
            return True
    return False
     
     
def redirect_from_cache(slug):
    if cache.get(slug):
        print("FROM CACHE")
        msg = 'redirect from ' + slug + ' to ' + cache.get(slug) + ' from cache'
        logger.debug(msg)
        return cache.get(slug)
    else:
        return None


def redirect_from_database(slug):
    try:
        url = Mapping.objects.get(short_url=slug)
        cache.set(slug, url.long_url, timeout=3600)
    except Mapping.DoesNotExist:
        msg = 'url for ' + slug + ' does not exist'
        logger.debug(msg)
        return None
    else:
        msg = 'redirected from ' + slug + ' to ' + url.long_url + ' from MySQL'
        logger.debug(msg)
        return url.long_url