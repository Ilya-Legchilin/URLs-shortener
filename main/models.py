from django.db import models
from hashids import Hashids


class Couple(models.Model):
    long_url =  models.CharField('Длинный URL', max_length=256)
    short_url = models.CharField('Короткий URL', max_length=256)
    session_key = models.CharField('Идентификатор сессии', max_length=256, default=None)
    
    def __str__(self):
        return short_url
        
    
    
                                                                                                                                                            