from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from .views import display_news


def scheduler_display_news():
    
    scheduler = BackgroundScheduler()
    print("News Scheduler being called")
    scheduler.add_job(display_news,  'interval', minutes=1)
    
    scheduler.start()

    # Shutdown your cron thread if the web process is stopped
    atexit.register(lambda: scheduler.shutdown(wait=False))
    print("Scheduler ends")
