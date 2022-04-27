from django.apps import AppConfig
import requests


class NewsHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NEWS_HANDLER'

    def ready(self):
        from .scheduler import scheduler_display_news
        scheduler_display_news(requests.request)