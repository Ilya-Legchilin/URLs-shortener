from django.db import models

from hashids import Hashids


class Mapping(models.Model):
    """

    long_url is a normal url to be shorten. 
    long_url means the real addres of web-site.
    short_url is a result of shortening via hashids.
    session_key is like an id of user taken from session.

    """
    long_url =  models.CharField('Длинный URL', max_length=256)
    short_url = models.CharField('Короткий URL', max_length=256)
    session_key = models.CharField('Идентификатор сессии',
                                   max_length=256,
                                   default=None)