# from celery import Celery
# from celery.schedules import crontab

# app = Celery('tasks', broker='redis://127.0.0.1:6379')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortener.settings')

# @app.task
# def show(arg):
    # print(arg)

# app.conf.beat_schedule = {
    # 'task-name': {
        # 'task': 'tasks.show',  # instead 'show'
        # 'schedule': 5.0,
        # 'args': (42,),
    # },
# }
# app.conf.timezone = 'UTC'