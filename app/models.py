from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    length_months = Column(Integer, nullable=False)
    monthly_payment = Column(Float, nullable=False)
