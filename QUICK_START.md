# Quick Start Guide

## Live Demo

🌐 **Deployed API**: https://api-interview.onrender.com/

Try it now:
- **API Docs**: https://api-interview.onrender.com/docs
- **Health Check**: https://api-interview.onrender.com/

*Note: Free tier spins down after 15 minutes - first request may take 30 seconds to wake up.*

---

## Setup & Run locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python run.py
```
Server runs at `http://localhost:8000`

### 3. Test the API

**Option A: Use the Python Client**
```bash
python client/loan_client.py
```

**Option B: Use curl**
```bash
# Create a loan
curl -X POST http://localhost:8000/loans \
  -H "Content-Type: application/json" \
  -d '{"amount": 100000, "interest_rate": 3.5, "length_months": 360, "monthly_payment": 449.04}'

# Get a loan
curl http://localhost:8000/loans/1

# Update a loan
curl -X PUT http://localhost:8000/loans/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": 150000}'

# List all loans
curl http://localhost:8000/loans
```

## API Documentation
Once running, visit `http://localhost:8000/docs` for interactive Swagger UI.

## Project Structure
- `app/main.py` - FastAPI application with all endpoints
- `app/models.py` - SQLAlchemy database models
- `app/schemas.py` - Pydantic validation schemas
- `app/database.py` - Database configuration
- `client/loan_client.py` - Programmatic Python client
- `run.py` - Server startup script
