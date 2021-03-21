#from celery import Celery
#from celery.schedules import crontab


#app = Celery('celery_example')

#@app.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
#    sender.add_periodic_task(2, clear.s(), name='clear storage')


#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortener.settings')
#app.config_from_object('django.conf:settings', namespace='CELERY')
#app.autodiscover_tasks()


#@app.task
#def clear():
#    pass
    
#app.conf.beat_schedule = {
#    'add-every-30-seconds': {
#        'task': 'tasks.clear_task',
#        'schedule': 1.0,
#    },
#}
#app.conf.timezone = 'UTC'
    

#@app.task(bind=True)
#def debug_task(self):
#        print('Request: {0!r}'.formt(self.request))
