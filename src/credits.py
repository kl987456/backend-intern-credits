import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv

from .database import get_db, engine
from .models import User, Credit
from .schemas import (
    CreditBalanceOut, CreditDelta, MessageOut, SchemaUpdateIn,
    DevCreateUserIn, DevUserWithCreditsOut
)

# Load env so ADMIN_TOKEN is available
load_dotenv()
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
if not ADMIN_TOKEN:
    raise RuntimeError("ADMIN_TOKEN is not set in .env or environment.")

router = APIRouter(prefix="/api/credits", tags=["Credits"])
schema_router = APIRouter(prefix="/api", tags=["Admin"])

# ---------- Helpers ----------
def _get_or_404_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def _get_or_create_credits(db: Session, user_id: int) -> Credit:
    credits = db.get(Credit, user_id)
    if not credits:
        credits = Credit(user_id=user_id, credits=0, last_updated=datetime.utcnow())
        db.add(credits)
        db.commit()
        db.refresh(credits)
    return credits

# ---------- Public Endpoints ----------
@router.get("/{user_id}", response_model=CreditBalanceOut)
def get_balance(user_id: int, db: Session = Depends(get_db)):
    _get_or_404_user(db, user_id)
    credits = _get_or_create_credits(db, user_id)
    return credits

@router.post("/{user_id}/add", response_model=CreditBalanceOut, status_code=200)
def add_credits(user_id: int, payload: CreditDelta, db: Session = Depends(get_db)):
    _get_or_404_user(db, user_id)
    credits = _get_or_create_credits(db, user_id)
    credits.credits += payload.amount
    credits.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(credits)
    return credits

@router.post("/{user_id}/deduct", response_model=CreditBalanceOut, status_code=200)
def deduct_credits(user_id: int, payload: CreditDelta, db: Session = Depends(get_db)):
    _get_or_404_user(db, user_id)
    credits = _get_or_create_credits(db, user_id)
    if credits.credits - payload.amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient credits")
    credits.credits -= payload.amount
    credits.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(credits)
    return credits

@router.patch("/{user_id}/reset", response_model=CreditBalanceOut)
def reset_credits(user_id: int, db: Session = Depends(get_db)):
    _get_or_404_user(db, user_id)
    credits = _get_or_create_credits(db, user_id)
    credits.credits = 0
    credits.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(credits)
    return credits

# ---------- Admin: External schema update ----------
@schema_router.patch("/schema/update", response_model=MessageOut)
def update_schema(body: SchemaUpdateIn, x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    sql_text = body.sql.strip()
    if not sql_text:
        raise HTTPException(status_code=400, detail="Empty SQL body")

    try:
        with engine.begin() as conn:
            for stmt in [s.strip() for s in sql_text.split(";") if s.strip()]:
                conn.execute(text(stmt))
        return MessageOut(message="Schema updated successfully")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Schema update failed: {e}")

# ---------- Dev-only helpers ----------
@router.post("/dev/create-user", response_model=DevUserWithCreditsOut, status_code=201)
def dev_create_user(payload: DevCreateUserIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        credits = _get_or_create_credits(db, existing.user_id)
        return DevUserWithCreditsOut(
            user_id=existing.user_id,
            email=existing.email,
            name=existing.name,
            credits=credits.credits
        )

    user = User(email=payload.email, name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)

    credits = _get_or_create_credits(db, user.user_id)
    return DevUserWithCreditsOut(
        user_id=user.user_id,
        email=user.email,
        name=user.name,
        credits=credits.credits
    )
