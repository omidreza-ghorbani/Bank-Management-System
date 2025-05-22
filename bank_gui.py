import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
import hashlib
import re

# ساختارهای داده جدید
class HashMap:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def add(self, key, value):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return
        self.table[index].append([key, value])
    
    def get(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

class LinkedQueue:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def enqueue(self, data):
        new_node = {'data': data, 'next': None}
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear['next'] = new_node
            self.rear = new_node
    
    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = temp['next']
        if self.front is None:
            self.rear = None
        return temp['data']
    
    def is_empty(self):
        return self.front is None

class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def insert(self, transaction):
        self.heap.append(transaction)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_max(self):
        if not self.heap:
            return None
        max_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify_down(0)
        return max_val
    
    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if parent >= 0 and self.heap[index]['amount'] > self.heap[parent]['amount']:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)
    
    def _heapify_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left]['amount'] > self.heap[largest]['amount']:
            largest = left
        if right < len(self.heap) and self.heap[right]['amount'] > self.heap[largest]['amount']:
            largest = right
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

class BalanceBST:
    def __init__(self):
        self.root = None
    
    def insert(self, account):
        self.root = self._insert(self.root, account)
    
    def _insert(self, node, account):
        if node is None:
            return {'account': account, 'left': None, 'right': None}
        if account.balance < node['account'].balance:
            node['left'] = self._insert(node['left'], account)
        else:
            node['right'] = self._insert(node['right'], account)
        return node
    
    def search_range(self, low, high):
        result = []
        self._search_range(self.root, low, high, result)
        return result
    
    def _search_range(self, node, low, high, result):
        if node is None:
            return
        if low <= node['account'].balance <= high:
            result.append(node['account'])
        if node['account'].balance >= low:
            self._search_range(node['left'], low, high, result)
        if node['account'].balance <= high:
            self._search_range(node['right'], low, high, result)

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
                if item:  # اگر آیتم خالی نباشد
                    customer = item[1]  # مقدار (value) در HashMap
                    customers_data.append({
                        'customer_id': customer.customer_id,
                        'name': customer.name,
                        'password_hash': customer.password_hash
                    })
        
        accounts_data = []
        for bucket in self.accounts.table:
            for item in bucket:
                if item:  # اگر آیتم خالی نباشد
                    account = item[1]  # مقدار (value) در HashMap
                    # تبدیل تاریخچه تراکنش‌ها به لیست
                    transaction_list = []
                    temp_queue = LinkedQueue()
                    while not account.transaction_history.is_empty():
                        trans = account.transaction_history.dequeue()
                        transaction_list.append(trans)
                        temp_queue.enqueue(trans)
                    # بازگرداندن تراکنش‌ها به صف اصلی
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
        
        # شمارش تعداد مشتریان موجود
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
        
        # شمارش تعداد حساب‌های موجود
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
            'priority': amount > 1000000  # تراکنش‌های بالای 1 میلیون اولویت دارند
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
        # ایجاد یک صف موقت برای حفظ تراکنش‌ها
        temp_queue = LinkedQueue()
        while not account.transaction_history.is_empty():
            trans = account.transaction_history.dequeue()
            history += f"{trans['timestamp']} - {trans['type']}: {trans['amount']} - {trans['description']}\n"
            temp_queue.enqueue(trans)
        # بازگرداندن تراکنش‌ها به صف اصلی
        account.transaction_history = temp_queue
        return history
    
    def search_accounts_by_balance(self, low: float, high: float) -> List[BankAccount]:
        return self.balance_bst.search_range(low, high)

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم بانکداری مدرن")
        self.root.geometry("800x600")
        self.bank = BankingSystem()
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        style.configure("TLabel", padding=6, font=('Helvetica', 10))
        style.configure("TEntry", padding=6)
        
        self.setup_welcome_screen()
    
    def setup_welcome_screen(self):
        self.clear_window()
        
        # Welcome Frame
        welcome_frame = ttk.Frame(self.root, padding="20")
        welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(welcome_frame, text="به سیستم بانکداری مدرن خوش آمدید", 
                 font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        # Buttons
        ttk.Button(welcome_frame, text="ورود", 
                  command=self.show_login).pack(fill="x", pady=5)
        ttk.Button(welcome_frame, text="ثبت نام", 
                  command=self.show_register).pack(fill="x", pady=5)
    
    def show_login(self):
        self.clear_window()
        
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(login_frame, text="ورود به سیستم", 
                 font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        ttk.Label(login_frame, text="شناسه مشتری:").pack()
        customer_id_entry = ttk.Entry(login_frame)
        customer_id_entry.pack(pady=5)
        
        ttk.Label(login_frame, text="رمز عبور:").pack()
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.pack(pady=5)
        
        def do_login():
            customer_id = customer_id_entry.get()
            password = password_entry.get()
            if self.bank.login(customer_id, password):
                self.show_dashboard()
            else:
                messagebox.showerror("خطا", "شناسه کاربری یا رمز عبور اشتباه است")
        
        ttk.Button(login_frame, text="ورود", 
                  command=do_login).pack(fill="x", pady=10)
        ttk.Button(login_frame, text="بازگشت", 
                  command=self.setup_welcome_screen).pack(fill="x")
    
    def show_register(self):
        self.clear_window()
        
        register_frame = ttk.Frame(self.root, padding="20")
        register_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(register_frame, text="ثبت نام", 
                 font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        ttk.Label(register_frame, text="نام:").pack()
        name_entry = ttk.Entry(register_frame)
        name_entry.pack(pady=5)
        
        ttk.Label(register_frame, text="رمز عبور:").pack()
        password_entry = ttk.Entry(register_frame, show="*")
        password_entry.pack(pady=5)
        
        def do_register():
            name = name_entry.get()
            password = password_entry.get()
            result = self.bank.register_customer(name, password)
            messagebox.showinfo("موفقیت", result)
            self.show_login()
        
        ttk.Button(register_frame, text="ثبت نام", 
                  command=do_register).pack(fill="x", pady=10)
        ttk.Button(register_frame, text="بازگشت", 
                  command=self.setup_welcome_screen).pack(fill="x")
    
    def show_dashboard(self):
        self.clear_window()
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header_frame, 
                 text=f"خوش آمدید، {self.bank.current_customer.name}!",
                 font=('Helvetica', 16, 'bold')).pack(side="left")
        
        ttk.Button(header_frame, text="خروج", 
                  command=self.logout).pack(side="right")
        
        # Main content
        content_frame = ttk.Frame(self.root, padding="20")
        content_frame.pack(fill="both", expand=True)
        
        # Account list
        accounts_frame = ttk.LabelFrame(content_frame, text="حساب‌های شما", padding="10")
        accounts_frame.pack(fill="x", pady=10)
        
        account_numbers = []
        for bucket in self.bank.current_customer.accounts.table:
            for item in bucket:
                if item:
                    account_numbers.append(item[0])
        
        for account_number in account_numbers:
            account_frame = ttk.Frame(accounts_frame)
            account_frame.pack(fill="x", pady=5)
            
            ttk.Label(account_frame, 
                     text=f"حساب: {account_number}").pack(side="left")
            ttk.Label(account_frame, 
                     text=f"موجودی: {self.bank.accounts.get(account_number).balance:.2f} ریال").pack(side="right")
        
        # Action buttons
        actions_frame = ttk.Frame(content_frame)
        actions_frame.pack(fill="x", pady=20)
        
        ttk.Button(actions_frame, text="ایجاد حساب جدید", 
                  command=self.create_account).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text="واریز", 
                  command=self.show_deposit).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text="برداشت", 
                  command=self.show_withdraw).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text="انتقال", 
                  command=self.show_transfer).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text="مشاهده تاریخچه تراکنش‌ها", 
                  command=self.show_transaction_history).pack(fill="x", pady=5)
    
    def create_account(self):
        result = self.bank.create_account()
        messagebox.showinfo("موفقیت", result)
        self.show_dashboard()
    
    def show_deposit(self):
        self.show_transaction_dialog("واریز", self.do_deposit)
    
    def show_withdraw(self):
        self.show_transaction_dialog("برداشت", self.do_withdraw)
    
    def show_transfer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("انتقال وجه")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="حساب مبدا:").pack(pady=5)
        from_account = ttk.Combobox(dialog, values=account_numbers)
        from_account.pack(pady=5)
        
        ttk.Label(dialog, text="حساب مقصد:").pack(pady=5)
        to_account = ttk.Entry(dialog)
        to_account.pack(pady=5)
        
        ttk.Label(dialog, text="مبلغ:").pack(pady=5)
        amount = ttk.Entry(dialog)
        amount.pack(pady=5)
        
        def do_transfer():
            result = self.bank.transfer(from_account.get(), to_account.get(), 
                                      float(amount.get()))
            messagebox.showinfo("انتقال", result)
            dialog.destroy()
            self.show_dashboard()
        
        ttk.Button(dialog, text="انتقال", 
                  command=do_transfer).pack(pady=10)
    
    def show_transaction_dialog(self, title, callback):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="حساب:").pack(pady=5)
        account_numbers = []
        for bucket in self.bank.current_customer.accounts.table:
            for item in bucket:
                if item:
                    account_numbers.append(item[0])
        account = ttk.Combobox(dialog, values=account_numbers)
        account.pack(pady=5)
        
        ttk.Label(dialog, text="مبلغ:").pack(pady=5)
        amount = ttk.Entry(dialog)
        amount.pack(pady=5)
        
        def do_action():
            result = callback(account.get(), float(amount.get()))
            messagebox.showinfo(title, result)
            dialog.destroy()
            self.show_dashboard()
        
        ttk.Button(dialog, text=title, 
                  command=do_action).pack(pady=10)
    
    def do_deposit(self, account, amount):
        return self.bank.deposit(account, amount)
    
    def do_withdraw(self, account, amount):
        return self.bank.withdraw(account, amount)
    
    def show_transaction_history(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("تاریخچه تراکنش‌ها")
        dialog.geometry("600x400")
        
        ttk.Label(dialog, text="انتخاب حساب:").pack(pady=5)
        account_numbers = []
        for bucket in self.bank.current_customer.accounts.table:
            for item in bucket:
                if item:
                    account_numbers.append(item[0])
        account = ttk.Combobox(dialog, values=account_numbers)
        account.pack(pady=5)
        
        history_text = tk.Text(dialog, height=15, width=60)
        history_text.pack(pady=10, padx=10)
        
        def show_history():
            history = self.bank.get_transaction_history(account.get())
            history_text.delete(1.0, tk.END)
            history_text.insert(tk.END, history)
        
        ttk.Button(dialog, text="نمایش تاریخچه", 
                  command=show_history).pack(pady=5)
    
    def logout(self):
        self.bank.current_customer = None
        self.setup_welcome_screen()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop() 