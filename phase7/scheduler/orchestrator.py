import logging
from datetime import datetime
import traceback
import asyncio

from phase1.scraper.fund_scraper import run_scraper
from phase1.scraper.fund_scraper import run_scraper
from phase2.run_processor import run_full_pipeline

from .status_tracker import update_status, read_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_pipeline():
    logger.info("Starting orchestrated pipeline...")
    new_status = {
        "last_run": datetime.now().isoformat(),
        "status": "running",
        "phases": {}
    }
    update_status(new_status)
    
    try:
        # Phase 1
        logger.info("Phase 1: Scraping...")
        await run_scraper()
        new_status["phases"]["phase1"] = {"status": "success"}
        update_status(new_status)
        
        # Phase 2
        logger.info("Phase 2: Processing...")
        run_full_pipeline()
        new_status["phases"]["phase2"] = {"status": "success"}
        update_status(new_status)
        
        # Phase 3
        logger.info("Phase 3: Vector Store Population...")
        from phase3.run_vectorstore import build_store
        build_store(force_rebuild=True)
        new_status["phases"]["phase3"] = {"status": "success"}
        
        new_status["status"] = "success"
        logger.info("Pipeline completed successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        logger.error(traceback.format_exc())
        new_status["status"] = "failed"
        new_status["error"] = str(e)
    finally:
        update_status(new_status)
