# KSUPay 💳🏫

[cite_start]KSUPay is a newly developed payment system designed for King Saud University administration to manage and streamline financial transactions within the campus[cite: 14]. [cite_start]The system facilitates various payments, such as purchasing from the bookstore, paying for accommodation, and depositing monthly student stipends[cite: 15]. 

## 🛠️ Tech Stack
* **Language:** Python
* [cite_start]**GUI Framework:** Tkinter [cite: 16]
* [cite_start]**Database:** SQLite [cite: 16]

## ✨ Features

### Student Features
* [cite_start]**Sign Up & Wallet Creation:** Users can register new accounts, which securely saves their data to the SQLite database and automatically generates a wallet with an initial balance of 1000 SR[cite: 44].
* [cite_start]**Student Wallet:** Allows students to process payments to other wallets[cite: 46]. 
* [cite_start]**Safe Transactions:** The system includes a validation step to verify that a target wallet actually exists in the database; if it does not exist, the system safely stops the transaction and alerts the user without deducting any money[cite: 21, 22].

### Admin Features
* [cite_start]**Role-Based Routing:** Authenticates users via the database and directs them to either the Admin Window (using a specific Admin ID) or the Student Wallet[cite: 45].
* [cite_start]**Entity Management:** Enables administrators to create and manage KSU entity wallets (e.g., the bookstore)[cite: 47].
* [cite_start]**Stipend Distribution:** Admins can easily pay monthly stipends (1000 SR) to all registered student wallets[cite: 47].
* [cite_start]**Data Backup:** Includes functionality to export all system records (users and wallets) to a `backup.csv` file[cite: 47].

## 🚀 How to Run the Project

1. **Prerequisites:** Make sure you have Python installed on your system. SQLite and Tkinter are included in the standard Python library, so no external `pip` installations are required.
2. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/KSUPay.git](https://github.com/your-username/KSUPay.git)
   cd KSUPay
