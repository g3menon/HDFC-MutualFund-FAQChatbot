import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from .orchestrator import run_pipeline
from .config import SCHEDULER_CRON_HOUR, SCHEDULER_CRON_MINUTE

import logging
logger = logging.getLogger(__name__)

def sync_run_pipeline():
    asyncio.run(run_pipeline())

def start_scheduler():
    logger.info(f"Starting APScheduler... scheduling daily at {SCHEDULER_CRON_HOUR:02d}:{SCHEDULER_CRON_MINUTE:02d}")
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        sync_run_pipeline, 
        'cron', 
        hour=SCHEDULER_CRON_HOUR, 
        minute=SCHEDULER_CRON_MINUTE,
        id="daily_pipeline_job",
        replace_existing=True
    )
    scheduler.start()
    return scheduler
