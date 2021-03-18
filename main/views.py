from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator


def index(request):
    session_list = [['my1/first.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/second.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/third.com', 'http://htmlbook.ru/html/table'],
                    ['my1/fourth.com', 'https://music.yandex.ru/home'],
                    ['my1/fifth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/sixth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/seventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/eighth.com', 'https://music.yandex.ru/home'],
                    ['my1/ninth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/tenth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/eleventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/twelvth.com', 'https://music.yandex.ru/home'],
                    ['my1/first.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/second.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/third.com', 'http://htmlbook.ru/html/table'],
                    ['my1/fourth.com', 'https://music.yandex.ru/home'],
                    ['my1/fifth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/sixth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/seventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/eighth.com', 'https://music.yandex.ru/home'],
                    ['my1/ninth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/tenth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/eleventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/twelvth.com', 'https://music.yandex.ru/home'],
                    ['my1/first.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/second.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/third.com', 'http://htmlbook.ru/html/table'],
                    ['my1/fourth.com', 'https://music.yandex.ru/home'],
                    ['my1/fifth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/sixth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/seventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/eighth.com', 'https://music.yandex.ru/home'],
                    ['my1/ninth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/tenth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/eleventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/twelvth.com', 'https://music.yandex.ru/home'],
                    ['my1/first.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/second.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/third.com', 'http://htmlbook.ru/html/table'],
                    ['my1/fourth.com', 'https://music.yandex.ru/home'],
                    ['my1/fifth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/sixth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/seventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/eighth.com', 'https://music.yandex.ru/home'],
                    ['my1/ninth.com', 'https://developer.mozilla.org/ru/docs'],
                    ['my1/tenth.com', 'https://github.com/Ilya-Legchilin/URLs-shortener'],
                    ['my1/eleventh.com', 'http://htmlbook.ru/html/table'],
                    ['my1/twelvth.com', 'https://music.yandex.ru/home'],
                    ]
    paginator = Paginator(session_list, 6)
    
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
