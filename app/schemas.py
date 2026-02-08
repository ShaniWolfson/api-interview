"""
Pydantic schemas for loan data validation and conversion to object.

These schemas define the shape of data for different operations:
- LoanBase: Common fields shared across operations
- LoanCreate: For creating new loans (all fields required)
- LoanUpdate: For updating loans (all fields optional for partial updates)
- LoanResponse: For API responses (includes auto-generated ID)
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class LoanBase(BaseModel):
    """
    Base schema with common loan fields and validation rules
    Field(...) - Ellipsis makes fields required (must be in JSON)
    "gt=0" means the value must be greater than 0, 
    "ge=0" means it must be greater than or equal to 0
    """
    amount: float = Field(..., gt=0, description="Loan amount must be positive")
    interest_rate: float = Field(..., ge=0, description="Interest rate must be non-negative")
    length_months: int = Field(..., gt=0, description="Loan length must be positive")
    monthly_payment: float = Field(..., gt=0, description="Monthly payment must be positive")


class LoanCreate(LoanBase):
    """Schema for creating a new loan. Inherits all required fields from LoanBase."""
    pass


class LoanUpdate(BaseModel):
    """
    Schema for updating an existing loan.
    All fields are optional to support partial updates.
    """
    amount: float | None = Field(None, gt=0, description="Loan amount must be positive")
    interest_rate: float | None = Field(None, ge=0, description="Interest rate must be non-negative")
    length_months: int | None = Field(None, gt=0, description="Loan length must be positive")
    monthly_payment: float | None = Field(None, gt=0, description="Monthly payment must be positive")


class LoanResponse(LoanBase):
    """
    Schema for loan API responses.
    Includes the database-generated ID and enables reading from ORM objects.
        
    """
    id: int  # ← Adds the 'id' field to the inherited fields

    class Config:
        from_attributes = True  # Read from SQLAlchemy objects (what you have)
