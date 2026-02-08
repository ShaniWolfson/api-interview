"""
Seed the database with sample loan data for testing and demonstration.

Run this script to populate the database with realistic loan examples.
"""

from app.database import SessionLocal, engine
from app.models import Base, Loan


def seed_database():
    """Add sample loan data to the database"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Loan).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} loan(s). Skipping seed.")
            return
        
        # Sample loan data
        sample_loans = [
            {
                "amount": 250000.0,
                "interest_rate": 4.5,
                "length_months": 360,
                "monthly_payment": 1266.71,
            },
            {
                "amount": 500000.0,
                "interest_rate": 3.75,
                "length_months": 360,
                "monthly_payment": 2315.10,
            },
            {
                "amount": 150000.0,
                "interest_rate": 5.0,
                "length_months": 180,
                "monthly_payment": 1186.19,
            },
            {
                "amount": 75000.0,
                "interest_rate": 4.25,
                "length_months": 240,
                "monthly_payment": 459.88,
            },
            {
                "amount": 1000000.0,
                "interest_rate": 3.5,
                "length_months": 360,
                "monthly_payment": 4490.44,
            },
        ]
        
        # Add loans to database
        for loan_data in sample_loans:
            loan = Loan(**loan_data)
            db.add(loan)
        
        db.commit()
        print(f"✓ Successfully seeded database with {len(sample_loans)} sample loans!")
        
        # Display the created loans
        print("\nSample loans created:")
        loans = db.query(Loan).all()
        for loan in loans:
            print(f"  Loan #{loan.id}: ${loan.amount:,.2f} @ {loan.interest_rate}% "
                  f"for {loan.length_months} months (${loan.monthly_payment:,.2f}/month)")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("=== Seeding Database with Sample Loans ===\n")
    seed_database()
    print("\n=== Done ===")
