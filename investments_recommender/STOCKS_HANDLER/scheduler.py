from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from .views import gather_stocks_data

def scheduler_gather_data():
    scheduler = BackgroundScheduler()
    print("Scheduler being called")
    scheduler.add_job(gather_stocks_data, 'interval', minutes=60)
    
    scheduler.start()

    # # Shutdown your cron thread if the web process is stopped
    # atexit.register(lambda: scheduler.shutdown(wait=False))
    # print("Scheduler ends")
