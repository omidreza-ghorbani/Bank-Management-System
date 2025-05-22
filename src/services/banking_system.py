import json
import os
import re
from typing import List, Optional
from src.core.data_structures import HashMap, LinkedQueue, MaxHeap, BalanceBST
from src.core.models import Customer, BankAccount
from src.core.constants import *

class BankingSystem:
    def __init__(self):
        self.customers = HashMap()
        self.accounts = HashMap()
        self.current_customer: Optional[Customer] = None
        self.data_file = DATA_FILE_PATH
        self.transaction_queue = LinkedQueue()
        self.priority_heap = MaxHeap()
        self.balance_bst = BalanceBST()
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for customer_data in data.get(DATA_CUSTOMERS_KEY, []):
                    customer = Customer(
                        customer_data[DATA_CUSTOMER_ID_KEY],
                        customer_data[DATA_NAME_KEY],
                        customer_data[DATA_PASSWORD_HASH_KEY],
                        is_hashed=True
                    )
                    self.customers.add(customer.customer_id, customer)
                
                for account_data in data.get(DATA_ACCOUNTS_KEY, []):
                    account = BankAccount(
                        account_data[DATA_ACCOUNT_NUMBER_KEY],
                        account_data[DATA_CUSTOMER_ID_KEY]
                    )
                    account.balance = account_data[DATA_BALANCE_KEY]
                    self.accounts.add(account.account_number, account)
                    customer = self.customers.get(account.customer_id)
                    if customer:
                        customer.accounts.add(account.account_number, account)
                    self.balance_bst.insert(account)
    
    def save_data(self):
        customers_data = []
        for bucket in self.customers.table:
            for item in bucket:
                if item:
                    customer = item[1]
                    customers_data.append({
                        DATA_CUSTOMER_ID_KEY: customer.customer_id,
                        DATA_NAME_KEY: customer.name,
                        DATA_PASSWORD_HASH_KEY: customer.password_hash
                    })
        
        accounts_data = []
        for bucket in self.accounts.table:
            for item in bucket:
                if item:
                    account = item[1]
                    transaction_list = []
                    temp_queue = LinkedQueue()
                    while not account.transaction_history.is_empty():
                        trans = account.transaction_history.dequeue()
                        transaction_list.append(trans)
                        temp_queue.enqueue(trans)
                    account.transaction_history = temp_queue
                    
                    accounts_data.append({
                        DATA_ACCOUNT_NUMBER_KEY: account.account_number,
                        DATA_CUSTOMER_ID_KEY: account.customer_id,
                        DATA_BALANCE_KEY: account.balance,
                        DATA_TRANSACTION_HISTORY_KEY: transaction_list
                    })
        
        data = {
            DATA_CUSTOMERS_KEY: customers_data,
            DATA_ACCOUNTS_KEY: accounts_data
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_customer(self, name: str, password: str) -> str:
        if not self._validate_password(password):
            return INVALID_PASSWORD
        
        customer_count = 0
        for bucket in self.customers.table:
            customer_count += len(bucket)
        
        customer_id = CUSTOMER_ID_FORMAT.format(customer_count + 1)
        customer = Customer(customer_id, name, password)
        self.customers.add(customer_id, customer)
        self.save_data()
        return REGISTER_SUCCESS.format(customer_id)
    
    def _validate_password(self, password: str) -> bool:
        return len(password) >= MIN_PASSWORD_LENGTH and \
               bool(re.search(r'[A-Za-z]', password)) and \
               bool(re.search(r'\d', password))
    
    def login(self, customer_id: str, password: str) -> bool:
        customer = self.customers.get(customer_id)
        if customer and customer.verify_password(password):
            self.current_customer = customer
            return True
        return False
    
    def create_account(self) -> str:
        if not self.current_customer:
            return LOGIN_REQUIRED
        
        account_count = 0
        for bucket in self.accounts.table:
            account_count += len(bucket)
        
        account_number = ACCOUNT_NUMBER_FORMAT.format(account_count + 1)
        account = BankAccount(account_number, self.current_customer.customer_id)
        self.accounts.add(account_number, account)
        self.current_customer.accounts.add(account_number, account)
        self.balance_bst.insert(account)
        self.save_data()
        return ACCOUNT_CREATED.format(account_number)
    
    def process_transaction(self, transaction):
        if transaction.get('priority', False):
            self.priority_heap.insert(transaction)
        else:
            self.transaction_queue.enqueue(transaction)
    
    def execute_transactions(self):
        while True:
            max_transaction = self.priority_heap.extract_max()
            if not max_transaction:
                break
            self._apply_transaction(max_transaction)
        
        while not self.transaction_queue.is_empty():
            transaction = self.transaction_queue.dequeue()
            self._apply_transaction(transaction)
    
    def _apply_transaction(self, transaction):
        from_acc = self.accounts.get(transaction['from_account'])
        to_acc = self.accounts.get(transaction['to_account'])
        if from_acc and to_acc:
            if from_acc.balance >= transaction['amount']:
                from_acc.balance -= transaction['amount']
                to_acc.balance += transaction['amount']
                from_acc.add_transaction(
                    TRANSACTION_TYPES['TRANSFER_OUT'],
                    -transaction['amount'],
                    TRANSFER_TO_FORMAT.format(to_acc.account_number)
                )
                to_acc.add_transaction(
                    TRANSACTION_TYPES['TRANSFER_IN'],
                    transaction['amount'],
                    TRANSFER_FROM_FORMAT.format(from_acc.account_number)
                )
                self.save_data()
    
    def deposit(self, account_number: str, amount: float) -> str:
        if not self.current_customer:
            return LOGIN_REQUIRED
        
        account = self.accounts.get(account_number)
        if not account:
            return ACCOUNT_NOT_FOUND
        
        if account.customer_id != self.current_customer.customer_id:
            return UNAUTHORIZED_ACCESS
        
        if amount <= 0:
            return INVALID_AMOUNT
        
        account.balance += amount
        account.add_transaction(TRANSACTION_TYPES['DEPOSIT'], amount, CASH_DEPOSIT)
        self.save_data()
        return DEPOSIT_SUCCESS.format(account.balance)
    
    def withdraw(self, account_number: str, amount: float) -> str:
        if not self.current_customer:
            return LOGIN_REQUIRED
        
        account = self.accounts.get(account_number)
        if not account:
            return ACCOUNT_NOT_FOUND
        
        if account.customer_id != self.current_customer.customer_id:
            return UNAUTHORIZED_ACCESS
        
        if amount <= 0:
            return INVALID_AMOUNT
        
        if account.balance < amount:
            return INSUFFICIENT_BALANCE
        
        account.balance -= amount
        account.add_transaction(TRANSACTION_TYPES['WITHDRAW'], -amount, CASH_WITHDRAWAL)
        self.save_data()
        return WITHDRAW_SUCCESS.format(account.balance)
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> str:
        transaction = {
            'from_account': from_account,
            'to_account': to_account,
            'amount': amount,
            'priority': amount > PRIORITY_TRANSFER_AMOUNT
        }
        self.process_transaction(transaction)
        self.execute_transactions()
        return TRANSFER_SUCCESS.format(amount)
    
    def get_account_balance(self, account_number: str) -> str:
        if not self.current_customer:
            return LOGIN_REQUIRED
        
        account = self.accounts.get(account_number)
        if not account:
            return ACCOUNT_NOT_FOUND
        
        if account.customer_id != self.current_customer.customer_id:
            return UNAUTHORIZED_ACCESS
        
        return BALANCE_FORMAT.format(account.balance)
    
    def get_transaction_history(self, account_number: str) -> str:
        if not self.current_customer:
            return LOGIN_REQUIRED
        
        account = self.accounts.get(account_number)
        if not account:
            return ACCOUNT_NOT_FOUND
        
        if account.customer_id != self.current_customer.customer_id:
            return UNAUTHORIZED_ACCESS
        
        history = TRANSACTION_HISTORY_TITLE + "\n"
        temp_queue = LinkedQueue()
        while not account.transaction_history.is_empty():
            trans = account.transaction_history.dequeue()
            history += TRANSACTION_FORMAT.format(
                trans['timestamp'],
                trans['type'],
                trans['amount'],
                trans['description']
            ) + "\n"
            temp_queue.enqueue(trans)
        account.transaction_history = temp_queue
        return history
    
    def search_accounts_by_balance(self, low: float, high: float) -> List[BankAccount]:
        return self.balance_bst.search_range(low, high) 