from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from hashids import Hashids
from .models import Couple
import redis
from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)


"""
function that makes long url short usind hashids library
"""
def shorten(url):
    hashids = Hashids(url)
    short = hashids.encode(1, 2, 3)
    return short



"""
get url via post request. If url not given that means that 
session map is empty. We initialize list of urls.
If url is given we make an object Couple and check whether
such url is already stored. If not then we store it with subpart.
If such a subpart is already used we return and get http response.
Else we save couple in mysql and in session.
"""
def index(request):
    new_url = request.POST.get('new_url', 0)
    subpart = request.POST.get('subpart', 0)
    if 'urls_list' not in request.session:
        request.session['urls_list'] = []
    if new_url != 0:
        couple = Couple()
        couple.long_url = new_url
        couple.session_key = request.session._session_key
        already_used = False
        all_couples = Couple.objects.all()
        if subpart == '':
            couple.short_url = shorten(new_url)
        else:
            for c in all_couples:
                if c.short_url == subpart:
                    msg = 'subpart ' + subpart + ' is already used'
                    logger.debug(msg)
                    return HttpResponse('Такой subpart уже используется')
            couple.short_url = subpart
        for c in all_couples:
            if c.long_url == new_url:
                already_used = True
        if not already_used:
            msg = 'new url for ' + couple.long_url + ' is ' + couple.short_url
            logger.debug(msg)
            couple.save()
            request.session['urls_list'].append([couple.long_url, couple.short_url])
            request.session.modified = True
        
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
                    
    return render(request, 'main.html', context=context)
    


"""
slug is a short url. If slug is in cache, take it out
and go to the long url.
Else check if it is in database. If not, we get http response
Else go to long_url.
Data in cache is holding 1 hour
"""
def redir(request, slug):
    if cache.get(slug):
        print("DATA FROM CACHE")
        msg = 'redirect from ' + slug + ' to ' + cache.get(slug) + ' from cache'
        logger.debug(msg)
        return redirect(cache.get(slug))
    else:
        try:
            url = Couple.objects.get(short_url=slug)
            cache.set(slug, url.long_url, timeout=3600)
        except Couple.DoesNotExist:
            msg = 'url for ' + slug + ' does not exist'
            logger.debug(msg)
            return HttpResponse('Нет такой ссылки!')
        else:
            print("DATA FROM MYSQL")
            msg = 'redirect from ' + slug + ' to ' + url.long_url + ' from MySQL'
            logger.debug(msg)
            return redirect(url.long_url)