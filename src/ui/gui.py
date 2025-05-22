import tkinter as tk
from tkinter import ttk, messagebox
from src.services.banking_system import BankingSystem
from src.core.constants import *

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
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
        
        welcome_frame = ttk.Frame(self.root, padding="20")
        welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(welcome_frame, text=WELCOME_MESSAGE, 
                 font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        ttk.Button(welcome_frame, text=LOGIN_BUTTON, 
                  command=self.show_login).pack(fill="x", pady=5)
        ttk.Button(welcome_frame, text=REGISTER_BUTTON, 
                  command=self.show_register).pack(fill="x", pady=5)
    
    def show_login(self):
        self.clear_window()
        
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(login_frame, text=LOGIN_TITLE, 
                 font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        ttk.Label(login_frame, text=CUSTOMER_ID_LABEL).pack()
        customer_id_entry = ttk.Entry(login_frame)
        customer_id_entry.pack(pady=5)
        
        ttk.Label(login_frame, text=PASSWORD_LABEL).pack()
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.pack(pady=5)
        
        def do_login():
            customer_id = customer_id_entry.get()
            password = password_entry.get()
            if self.bank.login(customer_id, password):
                self.show_dashboard()
            else:
                messagebox.showerror(ERROR_TITLE, LOGIN_ERROR)
        
        ttk.Button(login_frame, text=LOGIN_BUTTON, 
                  command=do_login).pack(fill="x", pady=10)
        ttk.Button(login_frame, text=BACK_BUTTON, 
                  command=self.setup_welcome_screen).pack(fill="x")
    
    def show_register(self):
        self.clear_window()
        
        register_frame = ttk.Frame(self.root, padding="20")
        register_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(register_frame, text=REGISTER_TITLE, 
                 font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        ttk.Label(register_frame, text=NAME_LABEL).pack()
        name_entry = ttk.Entry(register_frame)
        name_entry.pack(pady=5)
        
        ttk.Label(register_frame, text=PASSWORD_LABEL).pack()
        password_entry = ttk.Entry(register_frame, show="*")
        password_entry.pack(pady=5)
        
        def do_register():
            name = name_entry.get()
            password = password_entry.get()
            result = self.bank.register_customer(name, password)
            messagebox.showinfo(SUCCESS_TITLE, result)
            self.show_login()
        
        ttk.Button(register_frame, text=REGISTER_BUTTON, 
                  command=do_register).pack(fill="x", pady=10)
        ttk.Button(register_frame, text=BACK_BUTTON, 
                  command=self.setup_welcome_screen).pack(fill="x")
    
    def show_dashboard(self):
        self.clear_window()
        
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header_frame, 
                 text=WELCOME_USER_FORMAT.format(self.bank.current_customer.name),
                 font=('Helvetica', 16, 'bold')).pack(side="left")
        
        ttk.Button(header_frame, text=LOGOUT_BUTTON, 
                  command=self.logout).pack(side="right")
        
        content_frame = ttk.Frame(self.root, padding="20")
        content_frame.pack(fill="both", expand=True)
        
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
                     text=ACCOUNT_INFO_FORMAT.format(account_number)).pack(side="left")
            ttk.Label(account_frame, 
                     text=BALANCE_INFO_FORMAT.format(
                         self.bank.accounts.get(account_number).balance
                     )).pack(side="right")
        
        actions_frame = ttk.Frame(content_frame)
        actions_frame.pack(fill="x", pady=20)
        
        ttk.Button(actions_frame, text=CREATE_ACCOUNT_BUTTON, 
                  command=self.create_account).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text=DEPOSIT_BUTTON, 
                  command=self.show_deposit).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text=WITHDRAW_BUTTON, 
                  command=self.show_withdraw).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text=TRANSFER_BUTTON, 
                  command=self.show_transfer).pack(fill="x", pady=5)
        ttk.Button(actions_frame, text=TRANSACTION_HISTORY_BUTTON, 
                  command=self.show_transaction_history).pack(fill="x", pady=5)
    
    def create_account(self):
        result = self.bank.create_account()
        messagebox.showinfo(SUCCESS_TITLE, result)
        self.show_dashboard()
    
    def show_deposit(self):
        self.show_transaction_dialog(DEPOSIT_BUTTON, self.do_deposit)
    
    def show_withdraw(self):
        self.show_transaction_dialog(WITHDRAW_BUTTON, self.do_withdraw)
    
    def show_transfer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(TRANSFER_TITLE)
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text=FROM_ACCOUNT_LABEL).pack(pady=5)
        account_numbers = []
        for bucket in self.bank.current_customer.accounts.table:
            for item in bucket:
                if item:
                    account_numbers.append(item[0])
        from_account = ttk.Combobox(dialog, values=account_numbers)
        from_account.pack(pady=5)
        
        ttk.Label(dialog, text=TO_ACCOUNT_LABEL).pack(pady=5)
        to_account = ttk.Entry(dialog)
        to_account.pack(pady=5)
        
        ttk.Label(dialog, text=AMOUNT_LABEL).pack(pady=5)
        amount = ttk.Entry(dialog)
        amount.pack(pady=5)
        
        def do_transfer():
            result = self.bank.transfer(from_account.get(), to_account.get(), 
                                      float(amount.get()))
            messagebox.showinfo(SUCCESS_TITLE, result)
            dialog.destroy()
            self.show_dashboard()
        
        ttk.Button(dialog, text=TRANSFER_BUTTON, 
                  command=do_transfer).pack(pady=10)
    
    def show_transaction_dialog(self, title, callback):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text=ACCOUNT_LABEL).pack(pady=5)
        account_numbers = []
        for bucket in self.bank.current_customer.accounts.table:
            for item in bucket:
                if item:
                    account_numbers.append(item[0])
        account = ttk.Combobox(dialog, values=account_numbers)
        account.pack(pady=5)
        
        ttk.Label(dialog, text=AMOUNT_LABEL).pack(pady=5)
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
        dialog.title(TRANSACTION_HISTORY_TITLE)
        dialog.geometry("600x400")
        
        ttk.Label(dialog, text=SELECT_ACCOUNT_LABEL).pack(pady=5)
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
        
        ttk.Button(dialog, text=SHOW_HISTORY_BUTTON, 
                  command=show_history).pack(pady=5)
    
    def logout(self):
        self.bank.current_customer = None
        self.setup_welcome_screen()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy() 