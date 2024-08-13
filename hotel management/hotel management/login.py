import tkinter as tk
from tkinter import messagebox
import mysql.connector
from home import HotelManagementApp  # Import the home page

class HotelLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management - Login")
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

        # Login Box
        self.login_box = tk.Frame(self.main_frame, bg="#FFFFFF", bd=3, relief=tk.RIDGE)
        self.login_box.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the login box

        # Hotel Management Heading
        heading_label = tk.Label(self.login_box, text="Hotel Management - Login", font=("Helvetica", 18, "bold"), bg="#FFFFFF", fg="#4CAF50")
        heading_label.pack(pady=10)

        # Login Details Labels and Entry Fields
        self.labels = ["Email", "Password"]
        self.entries = {}

        for label_text in self.labels:
            entry_frame = tk.Frame(self.login_box, bg="#FFFFFF", bd=1, relief=tk.SOLID)
            entry_frame.pack(fill=tk.X, padx=20, pady=5)

            label = tk.Label(entry_frame, text=label_text, bg="#FFFFFF", font=("Helvetica", 12))
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(entry_frame, font=("Helvetica", 12), bd=0)
            entry.pack(side=tk.RIGHT, padx=5, pady=3, expand=True, fill=tk.X)
            entry.config(width=20)  # Adjust width of entry field
            self.entries[label_text] = entry

        # Forgot Password Link
        self.forgot_password_link = tk.Label(self.login_box, text="Forgot Password?", fg="blue", cursor="hand2")
        self.forgot_password_link.pack(pady=10)
        self.forgot_password_link.bind("<Button-1>", self.open_security_question_dialog)

        # Login Button
        self.login_button = tk.Button(self.login_box, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.login_button.pack(pady=10, ipadx=50, ipady=5)

    def login(self):
        email = self.entries["Email"].get()
        password = self.entries["Password"].get()

        if all([email, password]):
            try:
                # Check if the credentials are correct
                self.cursor.execute("SELECT * FROM register WHERE email = %s AND password = %s", (email, password))
                result = self.cursor.fetchone()

                if result:
                    # Credentials are correct, open the home page
                    self.go_to_home()
                else:
                    messagebox.showerror("Error", "Invalid email or password")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def open_security_question_dialog(self, event):
        # Open security question dialog
        security_question_window = tk.Toplevel(self.root)
        security_question_window.title("Security Question")
        security_question_window.geometry("300x200")

        email = self.entries["Email"].get()

        if email:
            try:
                # Fetch security question from database
                self.cursor.execute("SELECT securityQ FROM register WHERE email = %s", (email,))
                result = self.cursor.fetchone()

                if result:
                    security_question = result[0]

                    # Display security question
                    security_question_label = tk.Label(security_question_window, text=security_question, font=("Helvetica", 12))
                    security_question_label.pack(pady=10)

                    # Entry field for security answer
                    security_answer_label = tk.Label(security_question_window, text="Security Answer", font=("Helvetica", 12))
                    security_answer_label.pack(pady=5)

                    security_answer_entry = tk.Entry(security_question_window, font=("Helvetica", 12), bd=1, show="*")
                    security_answer_entry.pack(pady=5)

                    # Entry field for new password
                    new_password_label = tk.Label(security_question_window, text="New Password", font=("Helvetica", 12))
                    new_password_label.pack(pady=5)

                    new_password_entry = tk.Entry(security_question_window, font=("Helvetica", 12), bd=1, show="*")
                    new_password_entry.pack(pady=5)

                    # Submit button
                    submit_button = tk.Button(security_question_window, text="Submit", command=lambda: self.check_security_answer(security_question_window, security_answer_entry.get(), new_password_entry.get()), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
                    submit_button.pack(pady=10)
                else:
                    messagebox.showerror("Error", "No security question found for the provided email")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please enter your email address")

    def check_security_answer(self, window, security_answer, new_password):
        email = self.entries["Email"].get()

        if email and security_answer and new_password:
            try:
                # Fetch security answer from database
                self.cursor.execute("SELECT securityA FROM register WHERE email = %s", (email,))
                result = self.cursor.fetchone()

                if result:
                    if result[0] == security_answer:
                        # Update password in the database
                        self.cursor.execute("UPDATE register SET password = %s WHERE email = %s", (new_password, email))
                        self.conn.commit()
                        messagebox.showinfo("Success", "Password reset successful.")
                        window.destroy()  # Close security question dialog
                    else:
                        messagebox.showerror("Error", "Incorrect security answer")
                else:
                    messagebox.showerror("Error", "No security answer found for the provided email")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")


    def go_to_home(self):
    # Destroy the login window
        

    # Create a Toplevel window for the home page
        home_window = tk.Toplevel()
        app = HotelManagementApp(home_window)

# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelLoginApp(root)
    root.mainloop()

