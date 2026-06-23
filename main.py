import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
from random import randint
from datetime import datetime
import csv


# --- 1. Database Initialization ---
def init_database():
    conn = sqlite3.connect('KSUpay.db')

    conn.execute("""CREATE TABLE IF NOT EXISTS users(
         SID TEXT PRIMARY KEY,
         firstname TEXT,
         lastname TEXT,
         password TEXT,
         email TEXT,
         phone TEXT,
         role TEXT)""")

    conn.execute("""CREATE TABLE IF NOT EXISTS wallets (
         WID TEXT PRIMARY KEY,
         SID TEXT,
         walletType TEXT,
         createdAt TEXT,
         balance REAL)""")
    conn.commit()
    conn.close()


# --- 2. Sign Up Window ---
class SignUpWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KSUPay - Sign Up")
        self.root.geometry("500x750")
        self.root.configure(bg="light gray")

        main_frame = tk.Frame(self.root, bg="white", padx=30, pady=30)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=420)

        tk.Label(main_frame, text="Sign Up", font=("Helvetica", 22, "bold"), fg="dark blue", bg="white").pack(
            pady=(0, 20))

        self.first_name = self.add_styled_input(main_frame, "First Name")
        self.last_name = self.add_styled_input(main_frame, "Last Name")
        self.student_id = self.add_styled_input(main_frame, "Student ID (10 digits)")
        self.password = self.add_styled_input(main_frame, "Password", show="*")
        self.email = self.add_styled_input(main_frame, "Email (XXXXXXXX@student.ksu.edu.sa)")
        self.phone = self.add_styled_input(main_frame, "Phone Number (05XXXXXXXX)")

        tk.Button(main_frame, text="Submit", command=self.submit, bg="forest green", fg="white",
                  font=("Arial", 11, "bold"), relief="flat", cursor="hand2", pady=10).pack(fill="x", pady=(20, 10))

        tk.Button(main_frame, text="Login", command=self.open_login, bg="white", fg="dark blue", bd=0).pack()

    def add_styled_input(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 0))
        entry = tk.Entry(parent, font=("Arial", 11), bd=1, relief="solid", show=show)
        entry.pack(fill="x", ipady=6, pady=5)
        return entry

    def submit(self):
        first = self.first_name.get().strip()
        last = self.last_name.get().strip()

        if not first:
            messagebox.showerror("Error", "Please enter your first name")
            return
        if not last:
            messagebox.showerror("Error", "Please enter your last name")
            return
        if not re.match(r'^[0-9]{10}$', self.student_id.get()):
            messagebox.showerror("Error", "Student ID must be 10 digits")
            return
        if len(self.password.get()) < 6:
            messagebox.showerror("Error", "Password must be at least 6 letters or digits")
            return
        if not re.match(r'^[a-zA-Z0-9._%+-]{8}+@student\.ksu\.edu\.sa$', self.email.get()):
            messagebox.showerror("Error", "Email must be in format: xxxxxxxx@student.ksu.edu.sa")
            return
        if not re.match(r'^05[0-9]{8}$', self.phone.get()):
            messagebox.showerror("Error", "Phone must be 05XXXXXXXX")
            return

        conn = sqlite3.connect('KSUpay.db')
        c = conn.cursor()
        sid = self.student_id.get()
        success = False

        try:
            wid = str(randint(1000000000, 9999999999))
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            initial_balance = 1000.0

            c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)",
                      (sid, first, last,
                       self.password.get(), self.email.get(), self.phone.get(), "student"))

            c.execute("INSERT INTO wallets VALUES (?,?,?,?,?)",
                      (wid, sid, "student", now, initial_balance))

            conn.commit()
            success = True

            messagebox.showinfo("Success",
                                f"Account created successfully!\n"
                                f"Wallet Number: {wid}\n"
                                f"Initial Balance: {initial_balance} SR\n"
                                f"Date & Time: {now}")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "The student has been already registered")
        finally:
            conn.close()

        # Moved outside the Try-Finally block to prevent locking the database
        if success:
            self.open_login()

    def open_login(self):
        self.root.destroy()
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()


# --- 3. Login Window ---
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("KSUPay - Login")
        self.root.geometry("450x550")
        self.root.configure(bg="white")

        main_frame = tk.Frame(root, bg="white", padx=40, pady=40)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="KSUPay", font=("Helvetica", 26, "bold"), fg="navy", bg="white").pack(pady=(0, 10))

        tk.Label(main_frame, text="ID Number", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
        self.login_id_entry = tk.Entry(main_frame, font=("Arial", 12), bd=1, relief="solid")
        self.login_id_entry.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(main_frame, text="Password", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
        self.login_pw_entry = tk.Entry(main_frame, font=("Arial", 12), show="*", bd=1, relief="solid")
        self.login_pw_entry.pack(fill="x", ipady=7, pady=(5, 25))

        tk.Button(main_frame, text="Login", command=self.handle_login, bg="navy", fg="white",
                  font=("Arial", 11, "bold"), relief="flat", cursor="hand2", pady=10).pack(fill="x")

       

    def handle_login(self):
        user_id = self.login_id_entry.get()
        user_pw = self.login_pw_entry.get()

        if not user_id.isdigit() or len(user_id) != 10:
            messagebox.showerror("Error", "ID must be 10 digits")
            return

        conn = sqlite3.connect('KSUpay.db')
        user = conn.execute("SELECT password FROM users WHERE SID=?", (user_id,)).fetchone()
        conn.close()

        if user and user_pw == user[0]:
            self.root.destroy()
            if user_id == "1111111111":
                AdminWindow()
            else:
                WalletGUI(user_id)
        else:
            messagebox.showerror("Error", "Invalid credentials")




# --- 4. Student Wallet Window ---
class WalletGUI:
    def __init__(self, sid):
        self.sid = sid
        self.main_window = tk.Tk()
        self.main_window.title("KSUPay - My Wallet")
        self.main_window.geometry("550x650")
        self.main_window.configure(bg="light gray")

        conn = sqlite3.connect('KSUpay.db')
        wallet_info = conn.execute("SELECT WID FROM wallets WHERE SID = ?", (self.sid,)).fetchone()
        self.wid = wallet_info[0] if wallet_info else "N/A"
        conn.close()

        header = tk.Frame(self.main_window, bg="navy", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Student Wallet", font=("Helvetica", 18, "bold"), fg="white", bg="navy").pack()

        content = tk.Frame(self.main_window, bg="white", padx=30, pady=30)
        content.pack(pady=30, padx=40, fill="both", expand=True)

        card = tk.Frame(content, bg="alice blue", padx=20, pady=20)
        card.pack(fill="x", pady=(0, 20))
        tk.Label(card, text=f"Wallet Number: {self.wid}", bg="alice blue", font=("Arial", 10, "bold")).pack()
        tk.Label(card, text="Current Balance", bg="alice blue", font=("Arial", 10)).pack(pady=(10, 0))
        self.balance_display = tk.Label(card, text="0.00", bg="alice blue", font=("Arial", 24, "bold"), fg="navy")
        self.balance_display.pack()

        tk.Label(content, text="Target Wallet Number:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
        self.target_wid_entry = tk.Entry(content, font=("Arial", 11), bd=1, relief="solid")
        self.target_wid_entry.pack(fill="x", ipady=6, pady=(5, 15))

        tk.Label(content, text="Amount to Pay:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
        self.amount_entry = tk.Entry(content, font=("Arial", 11), bd=1, relief="solid")
        self.amount_entry.pack(fill="x", ipady=6, pady=(5, 15))

        tk.Button(content, text="Pay", command=self.pay, bg="navy", fg="white",
                  font=("Arial", 12, "bold"), relief="flat", cursor="hand2", pady=10).pack(fill="x", pady=10)

        tk.Button(content, text="Back", command=self.go_back, bg="white", fg="red", bd=0).pack()

        self.update_balance_view()
        self.main_window.mainloop()

    def update_balance_view(self):
        conn = sqlite3.connect('KSUpay.db')
        data = conn.execute("SELECT balance FROM wallets WHERE SID = ?", (self.sid,)).fetchone()
        conn.close()
        balance = float(data[0]) if data else 0.0
        self.balance_display.config(text=f"SR {balance:,.2f}")

    def pay(self):
        target_wid = self.target_wid_entry.get().strip()
        amount_val = self.amount_entry.get().strip()

        if not amount_val.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Invalid amount")
            return

        if target_wid == self.wid:
            messagebox.showerror("Error", "You cannot pay to your own wallet")
            return

        result = self.process_payment(self.sid, target_wid, float(amount_val))
        self.update_balance_view()
        if result == "Success":
            messagebox.showinfo("Status", "Transaction successful")
        else:
            messagebox.showerror("Error", result)

    def process_payment(self, sender_sid, target_wid, amount):
        conn = sqlite3.connect('KSUpay.db')
        try:
            sender_data = conn.execute("SELECT balance FROM wallets WHERE SID = ?", (sender_sid,)).fetchone()
            target_data = conn.execute("SELECT balance FROM wallets WHERE WID = ?", (target_wid,)).fetchone()

            if not target_data:
                return "Wallet number does not exist"

            s_balance = float(sender_data[0])
            if amount > s_balance:
                return "There is not enough money"

            conn.execute("UPDATE wallets SET balance = balance - ? WHERE SID = ?", (amount, sender_sid))
            conn.execute("UPDATE wallets SET balance = balance + ? WHERE WID = ?", (amount, target_wid))
            conn.commit()
            return "Success"
        except Exception:
            return "Error occurred"
        finally:
            conn.close()

    def go_back(self):
        self.main_window.destroy()
        app = SignUpWindow()
        app.root.mainloop()


# --- 5. Admin Window ---
class AdminWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KSUPay - Admin")
        self.root.geometry("500x600")
        self.root.configure(bg="light gray")

        frame = tk.Frame(self.root, bg="white", padx=30, pady=30)
        frame.pack(padx=40, pady=40, fill="both", expand=True)

        tk.Label(frame, text="Admin Panel", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        self.total_label = tk.Label(frame, text="", bg="white", font=("Arial", 11))
        self.total_label.pack(pady=10)

        tk.Label(frame, text="Entity Name", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
        self.entity_entry = tk.Entry(frame, font=("Arial", 11), bd=1, relief="solid")
        self.entity_entry.pack(fill="x", ipady=6, pady=5)

        tk.Button(frame, text="submit", command=self.submit,
                  bg="navy", fg="white", font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill="x", pady=5)
        tk.Button(frame, text="Pay Stipends", command=self.pay_stipends,
                  bg="forest green", fg="white", font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill="x",
                                                                                                         pady=5)
        tk.Button(frame, text="Cash Out", command=self.cash_out,
                  bg="dark red", fg="white", font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill="x", pady=5)
        tk.Button(frame, text="Backup", command=self.backup,
                  bg="gray", fg="white", font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill="x", pady=5)
        tk.Button(frame, text="Back", command=self.go_back, bg="white", fg="red", bd=0).pack(pady=10)

        self.update_total()
        self.root.mainloop()

    def update_total(self):
        conn = sqlite3.connect('KSUpay.db')
        result = conn.execute("SELECT SUM(balance) FROM wallets WHERE walletType !='student' ").fetchone()
        conn.close()
        total = float(result[0]) if result[0] else 0.0
        self.total_label.config(text=f"Total KSU Wallets Balance: {total:,.2f} SR")

    def submit(self):
        name = self.entity_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter entity name")
            return

        conn = sqlite3.connect('KSUpay.db')
        wid = str(randint(1000000000, 9999999999))
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute("INSERT INTO wallets VALUES (?,?,?,?,?)",
                     (wid, None, name, now, 0.0))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Wallet created successfully!\nWallet ID: {wid}\nDate & Time: {now}")
        self.entity_entry.delete(0, tk.END)
        self.update_total()

    def pay_stipends(self):
        conn = sqlite3.connect('KSUpay.db')
        conn.execute("UPDATE wallets SET balance = balance + 1000 WHERE walletType='student'")
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "1000 SR added to all student wallets")

    def cash_out(self):
        conn = sqlite3.connect('KSUpay.db')
        conn.execute("UPDATE wallets SET balance = 0 WHERE walletType !='student'")
        conn.commit()
        conn.close()
        messagebox.showinfo("Done", "All KSU wallets have been cleared")
        self.update_total()

    def backup(self):
        conn = sqlite3.connect('KSUpay.db')
        users_data = conn.execute("SELECT * FROM users").fetchall()
        wallets_data = conn.execute("SELECT * FROM wallets").fetchall()
        conn.close()

        with open("backup.csv", "w", newline="") as f:
            writer = csv.writer(f)

            # Users table
            writer.writerow(["--- USERS ---"])
            writer.writerow(["SID", "First Name", "Last Name", "Password", "Email", "Phone", "Role"])
            writer.writerows(users_data)

            writer.writerow([])  # blank row as separator

            # Wallets table
            writer.writerow(["--- WALLETS ---"])
            writer.writerow(["WID", "SID", "Type", "Date", "Balance"])
            writer.writerows(wallets_data)

        messagebox.showinfo("Success", "Backup saved to backup.csv")

    def go_back(self):
        self.root.destroy()
        app = SignUpWindow()
        app.root.mainloop()


# --- 6. Run ---
if __name__ == "__main__":
    init_database()

    conn = sqlite3.connect('KSUpay.db')
    conn.execute(
        "INSERT OR IGNORE INTO users VALUES ('1111111111','Admin','User','123456','admin@student.ksu.edu.sa','0500000000','admin')")
    conn.commit()
    conn.close()

    app = SignUpWindow()
    app.root.mainloop()