from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TransactionCreate(BaseModel):
    user_id: int
    type: str
    amount: float
    description: str
    category: str = "Other"