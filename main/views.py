from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from hashids import Hashids
from .models import Couple
import redis
from django.core.cache import cache


def shorten(url):
    hashids = Hashids(url)
    short = hashids.encode(1, 2, 3)
    return short


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
                    return HttpResponse('Такой subpart уже используется')
            couple.short_url = subpart
        for c in all_couples:
            if c.long_url == new_url:
                already_used = True
        if not already_used:
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
    

def redir(request, slug):
    if cache.get(slug):
        print("DATA FROM CACHE")
        return redirect(cache.get(slug))
    else:
        try:
            url = Couple.objects.get(short_url=slug)
            cache.set(slug, url.long_url, timeout=10)
        except Couple.DoesNotExist:
            return HttpResponse('Нет такой ссылки!')
        else:
            print("DATA FROM MYSQL")
            return redirect(url.long_url)