import time
import logging
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from phase7.scheduler.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    scheduler = start_scheduler()
    print("Scheduler is running. Press CTRL+C to stop.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.shutdown()
