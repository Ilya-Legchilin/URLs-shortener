from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from hashids import Hashids

def index(request):
    print("current request -----------", request)
    new_url = request.POST.get('new_url', 0)
    if 'urls_list' not in request.session:
        request.session['urls_list'] = []
    if new_url != 0:
        h = Hashids(new_url)
        token = h.encode(1, 2, 3)
        request.session['urls_list'].append([new_url, token])
        request.session.modified = True
    print(request.session['urls_list'])
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
