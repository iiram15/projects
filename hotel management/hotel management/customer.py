import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import room  # Import room.py for the Book Room functionality

class CustomerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management System")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#0B2044")  # Dark blue background
        
        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="iram1593",
            database="management"
        )
        self.cursor = self.conn.cursor()

        # Define colors
        self.primary_color = "#0B2044"  # Dark blue
        self.secondary_color = "#6FB0C5"  # Light blue
        self.text_color = "#FFFFFF"  # White
        self.button_color = "#C26D5C"  # Salmon

        # Main frame
        self.main_frame = tk.Frame(root, bg=self.primary_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Customer Details Frame
        self.customer_frame = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE, bg=self.secondary_color)
        self.customer_frame.pack(pady=20, padx=20, side=tk.LEFT)

        # Customer Details Labels and Entry Fields
        self.labels = ["Ref:", "Name:", "Gender:", "Mobile:", "Email:", "Nationality:", "ID Proof:", "ID Number:", "Address:"]
        self.entries = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self.customer_frame, text=label_text, bg=self.secondary_color, fg=self.text_color)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            entry = tk.Entry(self.customer_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        # Add a Separator
        ttk.Separator(self.customer_frame, orient=tk.HORIZONTAL).grid(row=9, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # CRUD Buttons
        self.buttons = ["Add", "Update", "Delete", "Save"]
        self.button_commands = [self.add_customer, self.update_customer, self.delete_customer, self.save_changes]

        for i, (button_text, command) in enumerate(zip(self.buttons, self.button_commands)):
            button = tk.Button(self.customer_frame, text=button_text, command=command, bg=self.button_color, fg=self.text_color)
            button.grid(row=10, column=i, padx=5, pady=5, columnspan=1 if i < 3 else 2)

        # Customer Details Treeview
        self.customer_tree_frame = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE, bg=self.primary_color)
        self.customer_tree_frame.pack(pady=20, padx=20, side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.customer_tree = ttk.Treeview(self.customer_tree_frame, columns=("ref", "name", "gender", "mobile", "email", "nationality", "idproof", "idnumber", "address"), show="headings", height=15)
        self.customer_tree.pack(fill=tk.BOTH, expand=True)

        self.customer_tree.heading("ref", text="Ref", anchor=tk.CENTER)
        self.customer_tree.heading("name", text="Name", anchor=tk.CENTER)
        self.customer_tree.heading("gender", text="Gender", anchor=tk.CENTER)
        self.customer_tree.heading("mobile", text="Mobile", anchor=tk.CENTER)
        self.customer_tree.heading("email", text="Email", anchor=tk.CENTER)
        self.customer_tree.heading("nationality", text="Nationality", anchor=tk.CENTER)
        self.customer_tree.heading("idproof", text="ID Proof", anchor=tk.CENTER)
        self.customer_tree.heading("idnumber", text="ID Number", anchor=tk.CENTER)
        self.customer_tree.heading("address", text="Address", anchor=tk.CENTER)

        # Set column widths
        for column in self.customer_tree['columns']:
            self.customer_tree.column(column, width=100, stretch=tk.NO)

        self.populate_treeview()

        # Navigation button to go back to home page
        self.home_button = tk.Button(self.main_frame, text="Home", command=self.go_to_home, bg=self.button_color, fg=self.text_color)
        self.home_button.pack(pady=10, padx=10)

        # Add Book Room Button
        self.book_room_button = tk.Button(self.main_frame, text="Room", command=self.open_book_room, bg=self.button_color, fg=self.text_color)
        self.book_room_button.pack(pady=10, padx=10)
    
    def populate_treeview(self):
        # Clear existing items in treeview
        records = self.customer_tree.get_children()
        for record in records:
            self.customer_tree.delete(record)

        # Fetch data from database
        self.cursor.execute("SELECT * FROM customer")
        rows = self.cursor.fetchall()

        # Insert data into treeview
        for row in rows:
            self.customer_tree.insert("", "end", values=row)

    def add_customer(self):
        ref = self.entries[0].get()
        name = self.entries[1].get()
        gender = self.entries[2].get()
        mobile = self.entries[3].get()
        email = self.entries[4].get()
        nationality = self.entries[5].get()
        idproof = self.entries[6].get()
        idnumber = self.entries[7].get()
        address = self.entries[8].get()

        if len(mobile) != 10:
            messagebox.showerror("Error", "Mobile number should be 10 digits")
            return
        
        if ref and name and gender and mobile and email and nationality and idproof and idnumber and address:
            self.cursor.execute("INSERT INTO customer (Ref, Name, Gender, Mobile, Email, Nationality, Idproof, Idnumber, Address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (ref, name, gender, mobile, email, nationality, idproof, idnumber, address))
            self.conn.commit()
            self.populate_treeview()
            messagebox.showinfo("Success", "Customer added successfully")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def update_customer(self):
        selected_item = self.customer_tree.focus()
        if selected_item:
            ref = self.entries[0].get()
            name = self.entries[1].get()
            gender = self.entries[2].get()
            mobile = self.entries[3].get()
            email = self.entries[4].get()
            nationality = self.entries[5].get()
            idproof = self.entries[6].get()
            idnumber = self.entries[7].get()
            address = self.entries[8].get()

            if ref and name and gender and mobile and email and nationality and idproof and idnumber and address:
                customer_ref = self.customer_tree.item(selected_item)['values'][0]
                self.cursor.execute("UPDATE customer SET Ref=%s, Name=%s, Gender=%s, Mobile=%s, Email=%s, Nationality=%s, Idproof=%s, Idnumber=%s, Address=%s WHERE Ref=%s",
                                    (ref, name, gender, mobile, email, nationality, idproof, idnumber, address, customer_ref))
                self.conn.commit()
                self.populate_treeview()
                messagebox.showinfo("Success", "Customer updated successfully")
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        else:
            messagebox.showerror("Error", "Please select a customer to update")

    def delete_customer(self):
        selected_item = self.customer_tree.focus()
        if selected_item:
            ref = self.customer_tree.item(selected_item)['values'][0]
            self.cursor.execute("DELETE FROM customer WHERE Ref=%s", (ref,))
            self.conn.commit()
            self.populate_treeview()
            messagebox.showinfo("Success", "Customer deleted successfully")
        else:
            messagebox.showerror("Error", "Please select a customer to delete")

    def save_changes(self):
        self.conn.commit()
        messagebox.showinfo("Success", "Changes saved successfully")

    def go_to_home(self):
    # Destroy all widgets inside the main_frame
        for widget in self.main_frame.winfo_children():
         widget.destroy()

    # Open the home page
        import home
        home_root = tk.Tk()
        app = home.HotelManagementApp(home_root)
        home_root.mainloop()
    
    def open_book_room(self):
        room_window = tk.Toplevel(self.root)
        room_app = room.BookRoomApp(room_window)
    
# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManagementApp(root)
    root.mainloop()
