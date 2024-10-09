import tkinter as tk
from tkinter import ttk, messagebox
import json

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking App")
        self.root.geometry("1000x600")
        
        self.accounts = self.load_accounts()
        self.logged_in_user = None
        
        # Create default admin account if it doesn't exist
        if 'admin' not in self.accounts:
            self.accounts['admin'] = {
                "password": "admin",
                "is_admin": True
            }
            self.save_accounts()
        
        self.create_login_screen()

    def load_accounts(self):
        try:
            with open("accounts.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_accounts(self):
        with open("accounts.json", "w") as file:
            json.dump(self.accounts, file)

    def create_login_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Arial", 18)).pack(pady=10)
        
        tk.Label(frame, text="Username:").pack()
        self.username_entry = tk.Entry(frame)
        self.username_entry.pack()
        
        tk.Label(frame, text="Password:").pack()
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack()

        tk.Button(frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(frame, text="Create Admin Account", command=self.create_admin_screen).pack()

    def create_admin_screen(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Create Admin Account", font=("Arial", 18)).pack(pady=10)
        
        tk.Label(frame, text="Username:").pack()
        self.admin_username_entry = tk.Entry(frame)
        self.admin_username_entry.pack()
        
        tk.Label(frame, text="Password:").pack()
        self.admin_password_entry = tk.Entry(frame, show="*")
        self.admin_password_entry.pack()

        tk.Button(frame, text="Create Admin", command=self.save_admin_account).pack(pady=10)
        tk.Button(frame, text="Back to Login", command=self.create_login_screen).pack()

    def save_admin_account(self):
        username = self.admin_username_entry.get()
        password = self.admin_password_entry.get()

        if username in self.accounts:
            messagebox.showerror("Error", "Username already exists!")
            return

        self.accounts[username] = {
            "password": password,
            "is_admin": True
        }
        self.save_accounts()
        messagebox.showinfo("Success", "Admin account created successfully!")
        self.create_login_screen()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username not in self.accounts:
            messagebox.showerror("Error", "Username not found!")
            return

        if self.accounts[username]["password"] != password:
            messagebox.showerror("Error", "Incorrect password!")
            return

        self.logged_in_user = username
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_screen()

        # Create sidebar
        sidebar = tk.Frame(self.root, bg="#2d3436", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        buttons = [
            ("Create Account", self.show_create_account),
            ("View Accounts", self.show_view_accounts),
            ("Delete Account", self.show_delete_account),
            ("Deposit", self.show_deposit_screen),
            ("Withdraw", self.show_withdraw_screen),
            ("Transaction History", self.show_transaction_history),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            tk.Button(sidebar, text=text, command=command, 
                     bg="#0984e3", fg="white", width=20).pack(pady=5)

        # Create main content area
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Welcome message
        tk.Label(self.content_frame, text=f"Welcome, {self.logged_in_user}!", 
                font=("Arial", 18)).pack(pady=20)

    def show_create_account(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Create Bank Account", font=("Arial", 16)).pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        labels = ["Account Holder's Name:", "Account Number:"]
        self.create_account_entries = {}
        
        for label in labels:
            tk.Label(form_frame, text=label).pack()
            entry = tk.Entry(form_frame)
            entry.pack(pady=5)
            self.create_account_entries[label] = entry
        
        tk.Button(form_frame, text="Create Account", command=self.save_bank_account).pack(pady=10)

    def save_bank_account(self):
        name = self.create_account_entries["Account Holder's Name:"].get()
        account_number = self.create_account_entries["Account Number:"].get()
        
        # Check if account number already exists
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    if account["account_number"] == account_number:
                        messagebox.showerror("Error", "Account number already exists!")
                        return
        
        # Initialize bank_accounts list if it doesn't exist
        if "bank_accounts" not in self.accounts[self.logged_in_user]:
            self.accounts[self.logged_in_user]["bank_accounts"] = []
        
        new_account = {
            "name": name,
            "account_number": account_number,
            "balance": 0,
            "transactions": []
        }
        
        self.accounts[self.logged_in_user]["bank_accounts"].append(new_account)
        self.save_accounts()
        messagebox.showinfo("Success", "Bank account created successfully!")

    def show_view_accounts(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="View Accounts", font=("Arial", 16)).pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(pady=10, fill="x")
        
        # Account Number search
        account_frame = tk.Frame(search_frame)
        account_frame.pack(side="left", padx=10)
        tk.Label(account_frame, text="Account Number:").pack(side="left")
        self.search_account_entry = tk.Entry(account_frame)
        self.search_account_entry.pack(side="left", padx=5)
        
        # Name search
        name_frame = tk.Frame(search_frame)
        name_frame.pack(side="left", padx=10)
        tk.Label(name_frame, text="Name:").pack(side="left")
        self.search_name_entry = tk.Entry(name_frame)
        self.search_name_entry.pack(side="left", padx=5)
        
        # Search button
        tk.Button(search_frame, text="Search", command=self.filter_accounts).pack(side="left", padx=10)
        tk.Button(search_frame, text="Clear Filters", command=self.clear_account_filters).pack(side="left")
        
        # Create table
        self.account_table = ttk.Treeview(self.content_frame, columns=("Name", "Account Number", "Balance"), show="headings")
        self.account_table.heading("Name", text="Name")
        self.account_table.heading("Account Number", text="Account Number")
        self.account_table.heading("Balance", text="Balance")
        self.account_table.pack(pady=10, fill="both", expand=True)
        
        # Display all accounts initially
        self.display_all_accounts()

    def display_all_accounts(self):
        # Clear existing items
        for item in self.account_table.get_children():
            self.account_table.delete(item)
        
        # Display all accounts
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    self.account_table.insert("", "end", values=(
                        account["name"],
                        account["account_number"],
                        f"Rs. {account['balance']}"
                    ))

    def filter_accounts(self):
        account_number = self.search_account_entry.get().strip()
        name = self.search_name_entry.get().strip().lower()
        
        # Clear existing items
        for item in self.account_table.get_children():
            self.account_table.delete(item)
        
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    # Check if account matches either filter
                    if (not account_number or account["account_number"] == account_number) and \
                       (not name or name in account["name"].lower()):
                        self.account_table.insert("", "end", values=(
                            account["name"],
                            account["account_number"],
                            f"Rs. {account['balance']}"
                        ))

    def clear_account_filters(self):
        self.search_account_entry.delete(0, tk.END)
        self.search_name_entry.delete(0, tk.END)
        self.display_all_accounts()

    def show_delete_account(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Delete Account", font=("Arial", 16)).pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Account Number:").pack(side="left")
        self.delete_account_entry = tk.Entry(search_frame)
        self.delete_account_entry.pack(side="left", padx=5)
        
        tk.Label(search_frame, text="Name:").pack(side="left")
        self.delete_name_entry = tk.Entry(search_frame)
        self.delete_name_entry.pack(side="left", padx=5)
        
        tk.Button(search_frame, text="Search", command=self.search_for_delete).pack(side="left")
        
        # Create table
        self.delete_table = ttk.Treeview(self.content_frame, 
                                         columns=("Name", "Account Number", "Balance", "Action"), 
                                         show="headings")
        self.delete_table.heading("Name", text="Name")
        self.delete_table.heading("Account Number", text="Account Number")
        self.delete_table.heading("Balance", text="Balance")
        self.delete_table.heading("Action", text="Action")
        self.delete_table.pack(pady=10, fill="both", expand=True)
        
        # Bind click event to the table
        self.delete_table.bind("<Button-1>", self.handle_delete_click)

    def handle_delete_click(self, event):
        region = self.delete_table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.delete_table.identify_column(event.x)
            if str(column) == "#4":  # Action column
                item = self.delete_table.selection()[0]
                account_number = self.delete_table.item(item)["values"][1]
                self.delete_account(account_number)

    def delete_account(self, account_number):
        response = messagebox.askyesno("Confirm Delete", 
                                       "Are you sure you want to delete this account?")
        if response:
            for username, user in self.accounts.items():
                if isinstance(user, dict) and "bank_accounts" in user:
                    user["bank_accounts"] = [acc for acc in user["bank_accounts"] 
                                            if acc["account_number"] != account_number]
            self.save_accounts()
            messagebox.showinfo("Success", "Account deleted successfully!")
            self.search_for_delete()  # Refresh the table

    def search_for_delete(self):
        account_number = self.delete_account_entry.get()
        name = self.delete_name_entry.get()
        
        # Clear existing items
        for item in self.delete_table.get_children():
            self.delete_table.delete(item)
        
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    if (not account_number or account["account_number"] == account_number) and \
                       (not name or name.lower() in account["name"].lower()):
                        self.delete_table.insert("", "end", values=(
                            account["name"],
                            account["account_number"],
                            f"Rs. {account['balance']}",
                            "Delete"
                        ))

    def show_deposit_screen(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Deposit Money", font=("Arial", 16)).pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Account Number:").pack()
        self.deposit_account_entry = tk.Entry(form_frame)
        self.deposit_account_entry.pack(pady=5)
        
        tk.Label(form_frame, text="Amount:").pack()
        self.deposit_amount_entry = tk.Entry(form_frame)
        self.deposit_amount_entry.pack(pady=5)
        
        tk.Button(form_frame, text="Deposit", command=self.deposit_money).pack(pady=10)

    def deposit_money(self):
        account_number = self.deposit_account_entry.get()
        try:
            amount = float(self.deposit_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
            return
        
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    if account["account_number"] == account_number:
                        account["balance"] += amount
                        account["transactions"].append(f"Deposited Rs. {amount}")
                        self.save_accounts()
                        messagebox.showinfo("Success", f"Deposited Rs. {amount} successfully!")
                        return
        
        messagebox.showerror("Error", "Account not found!")

    def show_withdraw_screen(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Withdraw Money", font=("Arial", 16)).pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Account Number:").pack()
        self.withdraw_account_entry = tk.Entry(form_frame)
        self.withdraw_account_entry.pack(pady=5)
        
        tk.Label(form_frame, text="Amount:").pack()
        self.withdraw_amount_entry = tk.Entry(form_frame)
        self.withdraw_amount_entry.pack(pady=5)
        
        tk.Button(form_frame, text="Withdraw", command=self.withdraw_money).pack(pady=10)

    def withdraw_money(self):
        account_number = self.withdraw_account_entry.get()
        try:
            amount = float(self.withdraw_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
            return
        
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    if account["account_number"] == account_number:
                        if account["balance"] < amount:
                            messagebox.showerror("Error", "Insufficient balance!")
                            return
                        account["balance"] -= amount
                        account["transactions"].append(f"Withdrew Rs. {amount}")
                        self.save_accounts()
                        messagebox.showinfo("Success", f"Withdrew Rs. {amount} successfully!")
                        return
        
        messagebox.showerror("Error", "Account not found!")

    def show_transaction_history(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Transaction History", font=("Arial", 16)).pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Account Number:").pack(side="left")
        self.transaction_account_entry = tk.Entry(search_frame)
        self.transaction_account_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.show_transactions).pack(side="left")
        
        # Create table
        self.transaction_table = ttk.Treeview(self.content_frame, 
                                            columns=("Transaction",), 
                                            show="headings")
        self.transaction_table.heading("Transaction", text="Transaction")
        self.transaction_table.pack(pady=10, fill="both", expand=True)

    def show_transactions(self):
        account_number = self.transaction_account_entry.get()
        
        # Clear existing items
        for item in self.transaction_table.get_children():
            self.transaction_table.delete(item)
        
        found = False
        for user in self.accounts.values():
            if isinstance(user, dict) and "bank_accounts" in user:
                for account in user["bank_accounts"]:
                    if account["account_number"] == account_number:
                        for transaction in account["transactions"]:
                            self.transaction_table.insert("", "end", values=(transaction,))
                        found = True
                        break
        
        if not found:
            messagebox.showinfo("Not Found", "No account found with this account number.")

    def logout(self):
        self.logged_in_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content_frame(self):
        if hasattr(self, 'content_frame'):
            for widget in self.content_frame.winfo_children():
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()