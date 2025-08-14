from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .database import SessionLocal
from . import models

scheduler = BackgroundScheduler()

def add_daily_credits():
    """Add +5 credits to all users daily at 00:00 UTC."""
    db: Session = SessionLocal()
    try:
        rows = db.query(models.Credit).all()
        for row in rows:
            row.credits += 5
            # set a timezone-aware UTC timestamp
            row.last_updated = datetime.now(timezone.utc)
        db.commit()
        print(f"[scheduler] Added +5 credits to {len(rows)} users.")
    finally:
        db.close()

def start_scheduler():
    # Run at midnight UTC every day
    scheduler.add_job(add_daily_credits, 'cron', hour=0, minute=0)
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown(wait=False)
