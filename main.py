import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from schemas import UserCreate, LoginRequest, TransactionCreate


# --------------------------------
# CREATE DATABASE TABLES
# --------------------------------

models.Base.metadata.create_all(bind=engine)


# --------------------------------
# FASTAPI APPLICATION
# --------------------------------

app = FastAPI(
    title="BuildSecure API",
    description="Financial Transaction Management API",
    version="1.0.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# HOME
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "BuildSecure API is running"
    }


# --------------------------------
# SERVE FRONTEND APPLICATION
# --------------------------------

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.get("/app")
def serve_app():
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend not found"}


# --------------------------------
# CREATE USER
# --------------------------------

@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "message": "User created successfully",

        "user": {

            "id": new_user.id,

            "name": new_user.name,

            "email": new_user.email

        }

    }


# --------------------------------
# GET USERS
# --------------------------------

@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(models.User).all()

    return {

        "users": [

            {

                "id": user.id,

                "name": user.name,

                "email": user.email

            }

            for user in users

        ]

    }


# --------------------------------
# LOGIN
# --------------------------------

@app.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.email == login_data.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if user.password != login_data.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {

        "message": "Login successful",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email

        }

    }


# --------------------------------
# CREATE TRANSACTION
# --------------------------------

@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == transaction.user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_transaction = models.Transaction(

        user_id=transaction.user_id,

        type=transaction.type,

        amount=transaction.amount,

        description=transaction.description,

        category=transaction.category

    )

    db.add(new_transaction)

    db.commit()

    db.refresh(new_transaction)

    return {

        "message": "Transaction created successfully",

        "transaction": {

            "id": new_transaction.id,

            "user_id": new_transaction.user_id,

            "type": new_transaction.type,

            "amount": new_transaction.amount,

            "description": new_transaction.description,

            "category": new_transaction.category

        }

    }


# --------------------------------
# GET ALL TRANSACTIONS
# --------------------------------

@app.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db)
):

    transactions = db.query(
        models.Transaction
    ).all()

    return {

        "transactions": [

            {

                "id": transaction.id,

                "user_id": transaction.user_id,

                "type": transaction.type,

                "amount": transaction.amount,

                "description": transaction.description,

                "category": transaction.category

            }

            for transaction in transactions

        ]

    }


# --------------------------------
# GET USER TRANSACTIONS
# --------------------------------

@app.get("/transactions/{user_id}")
def get_user_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):

    transactions = db.query(
        models.Transaction
    ).filter(
        models.Transaction.user_id == user_id
    ).all()

    return {

        "user_id": user_id,

        "transactions": [

            {

                "id": transaction.id,

                "type": transaction.type,

                "amount": transaction.amount,

                "description": transaction.description,

                "category": transaction.category

            }

            for transaction in transactions

        ]

    }