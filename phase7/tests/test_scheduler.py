import pytest
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from phase7.scheduler.config import SCHEDULER_CRON_HOUR
from phase7.scheduler.status_tracker import init_status_tracker, STATUS_FILE_PATH, read_status
from phase7.scheduler.scheduler import start_scheduler
from apscheduler.schedulers.background import BackgroundScheduler

def test_config_loads():
    assert isinstance(SCHEDULER_CRON_HOUR, int)

def test_status_tracker_initialization():
    if os.path.exists(STATUS_FILE_PATH):
        os.remove(STATUS_FILE_PATH)
    init_status_tracker()
    assert os.path.exists(STATUS_FILE_PATH)
    status = read_status()
    assert status.get("status") == "initialized"

def test_scheduler_engine_starts():
    scheduler = start_scheduler()
    assert isinstance(scheduler, BackgroundScheduler)
    assert scheduler.running
    jobs = scheduler.get_jobs()
    assert len(jobs) == 1
    scheduler.shutdown()
