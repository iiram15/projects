import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from login import HotelLoginApp 
from customer import CustomerManagementApp# Import the login page

class HotelRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#D3E8D1")  # Light green background

        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="iram1593",
            database="management"
        )
        self.cursor = self.conn.cursor()

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#D3E8D1")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Registration Box
        self.registration_box = tk.Frame(self.main_frame, bg="#FFFFFF", bd=3, relief=tk.RIDGE)
        self.registration_box.pack(padx=50, pady=50)

        # Hotel Management Heading
        heading_label = tk.Label(self.registration_box, text="Hotel Management", font=("Helvetica", 18, "bold"), bg="#FFFFFF", fg="#4CAF50")
        heading_label.pack(pady=10)

        # Registration Details Labels and Entry Fields
        self.labels = ["Email", "Contact", "First Name", "Last Name", "Password", "Security Answer"]
        self.entries = {}

        for label_text in self.labels:
            entry_frame = tk.Frame(self.registration_box, bg="#FFFFFF", bd=1, relief=tk.SOLID)
            entry_frame.pack(fill=tk.X, padx=20, pady=5)

            label = tk.Label(entry_frame, text=label_text, bg="#FFFFFF", font=("Helvetica", 12))
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(entry_frame, font=("Helvetica", 12), bd=0)
            entry.pack(side=tk.RIGHT, padx=5, pady=3, expand=True, fill=tk.X)
            self.entries[label_text] = entry

        # Security Question Dropdown
        security_q_options = ["First School Name", "Best Friend Name"]
        self.security_q_var = tk.StringVar()
        self.security_q_var.set(security_q_options[0])  # Set default value
        security_q_frame = tk.Frame(self.registration_box, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        security_q_frame.pack(fill=tk.X, padx=20, pady=5)

        security_q_label = tk.Label(security_q_frame, text="Security Question", bg="#FFFFFF", font=("Helvetica", 12))
        security_q_label.pack(side=tk.LEFT, padx=5)

        self.security_q_dropdown = ttk.Combobox(security_q_frame, textvariable=self.security_q_var, values=security_q_options, state="readonly", font=("Helvetica", 12))
        self.security_q_dropdown.pack(side=tk.RIGHT, padx=5, pady=3, expand=True, fill=tk.X)

        # Register Button
        self.register_button = tk.Button(self.registration_box, text="Register", command=self.register, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.register_button.pack(pady=20, padx=20, ipadx=50, ipady=5)

        # Already Registered Label
        login_label = tk.Label(self.registration_box, text="Already registered? Login here", bg="#FFFFFF", fg="#0000FF", cursor="hand2")
        login_label.pack(pady=10)
        login_label.bind("<Button-1>", self.open_login_page)

    def register(self):
        email = self.entries["Email"].get()
        contact = self.entries["Contact"].get()
        fname = self.entries["First Name"].get()
        lname = self.entries["Last Name"].get()
        password = self.entries["Password"].get()
        security_q = self.security_q_var.get()
        security_a = self.entries["Security Answer"].get()
        
        if all([email, contact, fname, lname, security_q, security_a, password]):
            try:
                # Insert registration details into the database
                self.cursor.execute("INSERT INTO register (email, contact, fname, lname, securityQ, securityA, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                    (email, contact, fname, lname, security_q, security_a, password))
                self.conn.commit()
                messagebox.showinfo("Success", "Registration successful")
                
                # Open the login page after registration
                self.open_login_page()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def open_login_page(self, event):
        # Open the login page in a new window
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("400x400")
        app = HotelLoginApp(login_window)    
        
    
# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelRegistrationApp(root)
    root.mainloop()

