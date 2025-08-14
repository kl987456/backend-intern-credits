from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)

    # one-to-one style relation (uselist=False) with credits
    credits = relationship("Credit", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Credit(Base):
    __tablename__ = "credits"

    # PK also FK to users.user_id (1-1 link)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    credits = Column(Integer, default=0, nullable=False)
    # server_default/ onupdate keep last_updated current
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="credits")
