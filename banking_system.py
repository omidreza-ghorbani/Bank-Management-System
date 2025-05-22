import json
import os
import re
from typing import List, Optional
from data_structures import HashMap, LinkedQueue, MaxHeap, BalanceBST
from models import Customer, BankAccount

class BankingSystem:
    def __init__(self):
        self.customers = HashMap()
        self.accounts = HashMap()
        self.current_customer: Optional[Customer] = None
        self.data_file = 'bank_data.json'
        self.transaction_queue = LinkedQueue()
        self.priority_heap = MaxHeap()
        self.balance_bst = BalanceBST()
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for customer_data in data.get('customers', []):
                    customer = Customer(
                        customer_data['customer_id'],
                        customer_data['name'],
                        customer_data['password_hash'],
                        is_hashed=True
                    )
                    self.customers.add(customer.customer_id, customer)
                
                for account_data in data.get('accounts', []):
                    account = BankAccount(
                        account_data['account_number'],
                        account_data['customer_id']
                    )
                    account.balance = account_data['balance']
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
                        'customer_id': customer.customer_id,
                        'name': customer.name,
                        'password_hash': customer.password_hash
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
                        'account_number': account.account_number,
                        'customer_id': account.customer_id,
                        'balance': account.balance,
                        'transaction_history': transaction_list
                    })
        
        data = {
            'customers': customers_data,
            'accounts': accounts_data
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_customer(self, name: str, password: str) -> str:
        if not self._validate_password(password):
            return "رمز عبور باید حداقل 8 کاراکتر و شامل حروف و اعداد باشد"
        
        customer_count = 0
        for bucket in self.customers.table:
            customer_count += len(bucket)
        
        customer_id = f"CUST{customer_count + 1:04d}"
        customer = Customer(customer_id, name, password)
        self.customers.add(customer_id, customer)
        self.save_data()
        return f"ثبت نام با موفقیت انجام شد. شناسه مشتری شما: {customer_id}"
    
    def _validate_password(self, password: str) -> bool:
        return len(password) >= 8 and bool(re.search(r'[A-Za-z]', password)) and bool(re.search(r'\d', password))
    
    def login(self, customer_id: str, password: str) -> bool:
        customer = self.customers.get(customer_id)
        if customer and customer.verify_password(password):
            self.current_customer = customer
            return True
        return False
    
    def create_account(self) -> str:
        if not self.current_customer:
            return "لطفا ابتدا وارد شوید"
        
        account_count = 0
        for bucket in self.accounts.table:
            account_count += len(bucket)
        
        account_number = f"ACC{account_count + 1:06d}"
        account = BankAccount(account_number, self.current_customer.customer_id)
        self.accounts.add(account_number, account)
        self.current_customer.accounts.add(account_number, account)
        self.balance_bst.insert(account)
        self.save_data()
        return f"حساب با موفقیت ایجاد شد. شماره حساب: {account_number}"
    
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
                from_acc.add_transaction('انتقال خروج', -transaction['amount'], f"انتقال به {to_acc.account_number}")
                to_acc.add_transaction('انتقال ورود', transaction['amount'], f"انتقال از {from_acc.account_number}")
                self.save_data()
    
    def deposit(self, account_number: str, amount: float) -> str:
        if not self.current_customer:
            return "لطفا ابتدا وارد شوید"
        
        account = self.accounts.get(account_number)
        if not account:
            return "حساب مورد نظر یافت نشد"
        
        if account.customer_id != self.current_customer.customer_id:
            return "دسترسی غیرمجاز"
        
        if amount <= 0:
            return "مبلغ باید مثبت باشد"
        
        account.balance += amount
        account.add_transaction('واریز', amount, "واریز نقدی")
        self.save_data()
        return f"واریز با موفقیت انجام شد. موجودی جدید: {account.balance}"
    
    def withdraw(self, account_number: str, amount: float) -> str:
        if not self.current_customer:
            return "لطفا ابتدا وارد شوید"
        
        account = self.accounts.get(account_number)
        if not account:
            return "حساب مورد نظر یافت نشد"
        
        if account.customer_id != self.current_customer.customer_id:
            return "دسترسی غیرمجاز"
        
        if amount <= 0:
            return "مبلغ باید مثبت باشد"
        
        if account.balance < amount:
            return "موجودی کافی نیست"
        
        account.balance -= amount
        account.add_transaction('برداشت', -amount, "برداشت نقدی")
        self.save_data()
        return f"برداشت با موفقیت انجام شد. موجودی جدید: {account.balance}"
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> str:
        transaction = {
            'from_account': from_account,
            'to_account': to_account,
            'amount': amount,
            'priority': amount > 1000000
        }
        self.process_transaction(transaction)
        self.execute_transactions()
        return f"انتقال با موفقیت انجام شد. مبلغ {amount} منتقل شد"
    
    def get_account_balance(self, account_number: str) -> str:
        if not self.current_customer:
            return "لطفا ابتدا وارد شوید"
        
        account = self.accounts.get(account_number)
        if not account:
            return "حساب مورد نظر یافت نشد"
        
        if account.customer_id != self.current_customer.customer_id:
            return "دسترسی غیرمجاز"
        
        return f"موجودی حساب: {account.balance}"
    
    def get_transaction_history(self, account_number: str) -> str:
        if not self.current_customer:
            return "لطفا ابتدا وارد شوید"
        
        account = self.accounts.get(account_number)
        if not account:
            return "حساب مورد نظر یافت نشد"
        
        if account.customer_id != self.current_customer.customer_id:
            return "دسترسی غیرمجاز"
        
        history = "تاریخچه تراکنش‌ها:\n"
        temp_queue = LinkedQueue()
        while not account.transaction_history.is_empty():
            trans = account.transaction_history.dequeue()
            history += f"{trans['timestamp']} - {trans['type']}: {trans['amount']} - {trans['description']}\n"
            temp_queue.enqueue(trans)
        account.transaction_history = temp_queue
        return history
    
    def search_accounts_by_balance(self, low: float, high: float) -> List[BankAccount]:
        return self.balance_bst.search_range(low, high) 