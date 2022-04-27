from django.apps import AppConfig


class StocksHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'STOCKS_HANDLER'

    def ready(self):
        from .scheduler import scheduler_gather_data
        scheduler_gather_data()