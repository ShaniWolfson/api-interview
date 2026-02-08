from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LoanStreet Loan Management API",
    description="API for managing loan records with create, read, and update operations",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "LoanStreet Loan Management API is running"}


@app.post("/loans", response_model=schemas.LoanResponse, status_code=201)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """
    Create a new loan with the following properties:
    - Amount
    - Interest rate
    - Length of loan in months
    - Monthly payment amount
    """
    logger.info(f"Creating loan: amount={loan.amount}, rate={loan.interest_rate}, months={loan.length_months}")
    
    # Step 1: Pydantic validates & creates object (see schemas.py)
    # loan = LoanCreate(...)  # Pydantic object

    # Step 2: Convert to dict
    loan_dict = loan.model_dump()

    # Step 3: Create SQLAlchemy object (in memory only!)
    db_loan = models.Loan(**loan_dict)  # SQLAlchemy object, not in db yet!

    # Step 4: Put it in the database
    db.add(db_loan)      # stage for insertion in memory
    db.commit()          # now it's in the database!
    db.refresh(db_loan)  # get the auto-generated ID back
    
    logger.info(f"Loan created successfully with ID: {db_loan.id}")
    return db_loan       # Return the SQLAlchemy object, FastAPI will convert to JSON using Pydantic schema


@app.get("/loans/{loan_id}", response_model=schemas.LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """Get a loan by its unique identifier"""
    logger.info(f"Retrieving loan with ID: {loan_id}")
    
    # Query the database for the loan with the given ID using SQLAlchemy
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    
    # If no loan is found, raise a 404 error
    if db_loan is None:
        logger.warning(f"Loan not found: ID {loan_id}")
        raise HTTPException(status_code=404, detail="Loan not found")
    
    logger.info(f"Loan retrieved successfully: ID {loan_id}")
    # If found, return the loan object (FastAPI will convert it to JSON using the response_model schema)
    return db_loan


@app.put("/loans/{loan_id}", response_model=schemas.LoanResponse)
def update_loan(loan_id: int, loan: schemas.LoanUpdate, db: Session = Depends(get_db)):
    """Update an existing loan by its unique identifier"""
    logger.info(f"Updating loan with ID: {loan_id}")
    
    # Query the database for the loan with the given ID using SQLAlchemy
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    
    # if no loan is found, raise a 404 error
    if db_loan is None:
        logger.warning(f"Loan not found for update: ID {loan_id}")
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # if a loan is found, update only provided fields
    update_data = loan.model_dump(exclude_unset=True) # Get only fields that were provided in the request (exclude unset fields)
    logger.info(f"Updating fields: {list(update_data.keys())}")
    
    # Set the provided fields on the db_loan object
    for key, value in update_data.items():
        setattr(db_loan, key, value)
    
    db.commit()
    db.refresh(db_loan)
    
    logger.info(f"Loan updated successfully: ID {loan_id}")
    return db_loan


@app.get("/loans", response_model=list[schemas.LoanResponse])
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all loans"""
    logger.info(f"Listing loans: skip={skip}, limit={limit}")
    
    # Query the database for all loans using SQLAlchemy
    loans = db.query(models.Loan).offset(skip).limit(limit).all()
    
    logger.info(f"Retrieved {len(loans)} loans")
    # Return the list of loans (FastAPI will convert to JSON using the response_model schema)
    return loans

@app.delete("/loans/{loan_id}", status_code=204)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """Delete a loan by its unique identifier"""
    logger.info(f"Deleting loan with ID: {loan_id}")
    
    # Query the database for the loan with the given ID using SQLAlchemy
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    
    # If no loan is found, raise a 404 error
    if db_loan is None:
        logger.warning(f"Loan not found for deletion: ID {loan_id}")
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # If found, delete the loan
    db.delete(db_loan)
    db.commit()
    
    logger.info(f"Loan deleted successfully: ID {loan_id}")
    return None