import os

SCHEDULER_CRON_HOUR = int(os.getenv("SCHEDULER_CRON_HOUR", "10"))
SCHEDULER_CRON_MINUTE = int(os.getenv("SCHEDULER_CRON_MINUTE", "0"))
SCHEDULER_RETRY_COUNT = int(os.getenv("SCHEDULER_RETRY_COUNT", "3"))
STATUS_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "scheduler_status.json")
