import tkinter as tk
from tkinter import ttk, messagebox
from banking_system import BankingSystem

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
        
        welcome_frame = ttk.Frame(self.root, padding="20")
        welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(welcome_frame, text="به سیستم بانکداری مدرن خوش آمدید", 
                 font=('Helvetica', 20, 'bold')).pack(pady=20)
        
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
        
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header_frame, 
                 text=f"خوش آمدید، {self.bank.current_customer.name}!",
                 font=('Helvetica', 16, 'bold')).pack(side="left")
        
        ttk.Button(header_frame, text="خروج", 
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
                     text=f"حساب: {account_number}").pack(side="left")
            ttk.Label(account_frame, 
                     text=f"موجودی: {self.bank.accounts.get(account_number).balance:.2f} ریال").pack(side="right")
        
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
        account_numbers = []
        for bucket in self.bank.current_customer.accounts.table:
            for item in bucket:
                if item:
                    account_numbers.append(item[0])
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