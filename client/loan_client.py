"""
LoanStreet Loan Management API Client

A programmatic client for interacting with the LoanStreet Loan Management API.
Similar to PyGithub, this client provides a simple interface for CRUD operations.

Example usage:
    from loan_client import LoanClient
    
    client = LoanClient("http://localhost:8000")
    
    # Create a loan
    loan = client.create_loan(
        amount=100000.0,
        interest_rate=3.5,
        length_months=360,
        monthly_payment=449.04
    )
    print(f"Created loan with ID: {loan['id']}")
    
    # Get a loan
    loan = client.get_loan(1)
    print(f"Loan amount: ${loan['amount']}")
    
    # Update a loan
    updated_loan = client.update_loan(1, interest_rate=3.25)
    print(f"Updated interest rate: {updated_loan['interest_rate']}%")
    
    # List all loans
    loans = client.list_loans()
    print(f"Total loans: {len(loans)}")
"""

import requests
from typing import Optional


class LoanClientError(Exception):
    """Custom exception for LoanClient errors"""
    pass


class LoanClient:
    """
    A client for interacting with the LoanStreet Loan Management API.
    
    Attributes:
        base_url (str): The base URL of the API server
        timeout (int): Request timeout in seconds
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize the LoanClient.
        
        Args:
            base_url: The base URL of the API server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response and raise errors if needed"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_detail = response.json().get('detail', str(e)) if response.content else str(e)
            raise LoanClientError(f"API error: {error_detail}") from e
        except requests.exceptions.RequestException as e:
            raise LoanClientError(f"Request failed: {str(e)}") from e
    
    def create_loan(
        self,
        amount: float,
        interest_rate: float,
        length_months: int,
        monthly_payment: float
    ) -> dict:
        """
        Create a new loan.
        
        Args:
            amount: The loan amount (must be positive)
            interest_rate: The interest rate percentage (must be non-negative)
            length_months: The length of the loan in months (must be positive)
            monthly_payment: The monthly payment amount (must be positive)
        
        Returns:
            dict: The created loan object with its assigned ID
        
        Raises:
            LoanClientError: If the request fails or validation errors occur
        """
        payload = {
            "amount": amount,
            "interest_rate": interest_rate,
            "length_months": length_months,
            "monthly_payment": monthly_payment
        }
        response = self.session.post(
            f"{self.base_url}/loans",
            json=payload,
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def get_loan(self, loan_id: int) -> dict:
        """
        Get a loan by its ID.
        
        Args:
            loan_id: The unique identifier of the loan
        
        Returns:
            dict: The loan object
        
        Raises:
            LoanClientError: If the loan is not found or request fails
        """
        response = self.session.get(
            f"{self.base_url}/loans/{loan_id}",
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def update_loan(
        self,
        loan_id: int,
        amount: Optional[float] = None,
        interest_rate: Optional[float] = None,
        length_months: Optional[int] = None,
        monthly_payment: Optional[float] = None
    ) -> dict:
        """
        Update an existing loan. Only provided fields will be updated.
        
        Args:
            loan_id: The unique identifier of the loan
            amount: The new loan amount (optional)
            interest_rate: The new interest rate (optional)
            length_months: The new loan length in months (optional)
            monthly_payment: The new monthly payment amount (optional)
        
        Returns:
            dict: The updated loan object
        
        Raises:
            LoanClientError: If the loan is not found or request fails
        """
        payload = {}
        if amount is not None:
            payload["amount"] = amount
        if interest_rate is not None:
            payload["interest_rate"] = interest_rate
        if length_months is not None:
            payload["length_months"] = length_months
        if monthly_payment is not None:
            payload["monthly_payment"] = monthly_payment
        
        response = self.session.put(
            f"{self.base_url}/loans/{loan_id}",
            json=payload,
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def list_loans(self, skip: int = 0, limit: int = 100) -> list[dict]:
        """
        List all loans with pagination.
        
        Args:
            skip: Number of loans to skip (for pagination)
            limit: Maximum number of loans to return
        
        Returns:
            list[dict]: List of loan objects
        
        Raises:
            LoanClientError: If the request fails
        """
        response = self.session.get(
            f"{self.base_url}/loans",
            params={"skip": skip, "limit": limit},
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def health_check(self) -> dict:
        """
        Check if the API server is running.
        
        Returns:
            dict: Health check response
        
        Raises:
            LoanClientError: If the server is not reachable
        """
        response = self.session.get(
            f"{self.base_url}/",
            timeout=self.timeout
        )
        return self._handle_response(response)


def main():
    """Example usage of the LoanClient"""
    # Initialize the client
    client = LoanClient("http://localhost:8000")
    
    print("=== LoanStreet Loan Management API Client Demo ===\n")
    
    # Health check
    try:
        health = client.health_check()
        print(f"✓ Server status: {health['message']}\n")
    except LoanClientError as e:
        print(f"✗ Server is not running: {e}")
        print("Please start the server with: uvicorn app.main:app --reload")
        return
    
    # Create a loan
    print("Creating a new loan...")
    loan = client.create_loan(
        amount=250000.0,
        interest_rate=4.5,
        length_months=360,
        monthly_payment=1266.71
    )
    print(f"✓ Created loan with ID: {loan['id']}")
    print(f"  Amount: ${loan['amount']:,.2f}")
    print(f"  Interest Rate: {loan['interest_rate']}%")
    print(f"  Length: {loan['length_months']} months")
    print(f"  Monthly Payment: ${loan['monthly_payment']:,.2f}\n")
    
    loan_id = loan['id']
    
    # Get the loan
    print(f"Retrieving loan {loan_id}...")
    retrieved_loan = client.get_loan(loan_id)
    print(f"✓ Retrieved loan: ${retrieved_loan['amount']:,.2f} at {retrieved_loan['interest_rate']}%\n")
    
    # Update the loan
    print(f"Updating loan {loan_id} with new interest rate...")
    updated_loan = client.update_loan(loan_id, interest_rate=4.25)
    print(f"✓ Updated interest rate: {updated_loan['interest_rate']}%\n")
    
    # List all loans
    print("Listing all loans...")
    loans = client.list_loans()
    print(f"✓ Total loans in system: {len(loans)}")
    for l in loans:
        print(f"  - Loan #{l['id']}: ${l['amount']:,.2f} at {l['interest_rate']}%")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
