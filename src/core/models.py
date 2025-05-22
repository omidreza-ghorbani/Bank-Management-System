import hashlib
from datetime import datetime
from src.core.data_structures import HashMap, LinkedQueue

class Customer:
    def __init__(self, customer_id: str, name: str, password: str, is_hashed=False):
        self.customer_id = customer_id
        self.name = name
        if is_hashed:
            self.password_hash = password
        else:
            self.password_hash = self._hash_password(password)
        self.accounts = HashMap()
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        return self._hash_password(password) == self.password_hash

class BankAccount:
    def __init__(self, account_number: str, customer_id: str):
        self.account_number = account_number
        self.customer_id = customer_id
        self.balance = 0.0
        self.transaction_history = LinkedQueue()
    
    def add_transaction(self, transaction_type: str, amount: float, description: str):
        self.transaction_history.enqueue({
            'type': transaction_type,
            'amount': amount,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }) 