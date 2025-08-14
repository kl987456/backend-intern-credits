from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# ----- Public credit API -----

class CreditDelta(BaseModel):
    amount: int = Field(ge=1)  # must be >= 1

class CreditBalanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    credits: int
    last_updated: datetime | None = None

class MessageOut(BaseModel):
    message: str

# ----- Schema Update API -----

class SchemaUpdateIn(BaseModel):
    sql: str = Field(min_length=1)

# ----- Dev helpers for testing -----

class DevCreateUserIn(BaseModel):
    email: str
    name: str

class DevUserOut(BaseModel):
    user_id: int
    email: str
    name: str

class DevUserWithCreditsOut(DevUserOut):
    credits: int
