import tkinter as tk
from tkinter import ttk, messagebox
from typing import Self
import mysql.connector

class BookRoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Room")
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

        # Main frame
        self.main_frame = tk.Frame(root, bg="#0B2044")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Search Bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.main_frame, textvariable=self.search_var, width=20)
        self.search_entry.grid(row=0, column=0, padx=20, pady=5)
        self.search_button = tk.Button(self.main_frame, text="Search", command=self.search, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.search_button.grid(row=0, column=1, padx=20, pady=5)
        
        # Home Button
        self.home_button = tk.Button(self.main_frame, text="Home", command=self.go_to_home, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.home_button.grid(row=0, column=2, padx=20, pady=5)

        # Entry Fields
        self.entry_labels = ["Room Available", "Contact", "Check-In", "Check-Out", "No. of Days", "Paid", "Subtotal", "Remaining Amount"]
        self.entries = {}
        for i, label in enumerate(self.entry_labels):
            entry_label = tk.Label(self.main_frame, text=label, bg="#0B2044", fg="white")
            entry_label.grid(row=i+1, column=0, padx=20, pady=5, sticky="w")
            entry = tk.Entry(self.main_frame, width=20)
            entry.grid(row=i+1, column=1, padx=20, pady=5)
            self.entries[label] = entry

        # Room Type Dropdown
        room_type_label = tk.Label(self.main_frame, text="Room Type", bg="#0B2044", fg="white")
        room_type_label.grid(row=len(self.entry_labels)+1, column=0, padx=20, pady=5, sticky="w")
        self.room_type_var = tk.StringVar(self.main_frame)
        self.room_type_var.set("")  # Set default value
        self.room_type_dropdown = ttk.Combobox(self.main_frame, textvariable=self.room_type_var, state="readonly")
        self.room_type_dropdown['values'] = ("Single", "Double")
        self.room_type_dropdown.grid(row=len(self.entry_labels)+1, column=1, padx=20, pady=5)

        # Meal Dropdown
        meal_label = tk.Label(self.main_frame, text="Meal", bg="#0B2044", fg="white")
        meal_label.grid(row=len(self.entry_labels)+2, column=0, padx=20, pady=5, sticky="w")
        self.meal_var = tk.StringVar(self.main_frame)
        self.meal_var.set("")  # Set default value
        self.meal_dropdown = ttk.Combobox(self.main_frame, textvariable=self.meal_var, state="readonly")
        self.meal_dropdown['values'] = ("Breakfast", "Lunch", "Dinner")
        self.meal_dropdown.grid(row=len(self.entry_labels)+2, column=1, padx=20, pady=5)
        
        # Fetch Button
        self.fetch_button = tk.Button(self.main_frame, text="Fetch", command=self.fetch_customer_details, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.fetch_button.grid(row=1, column=2, padx=20, pady=5)

        # Customer Detail Box
        self.detail_box = tk.Text(self.main_frame, height=10, width=50, bg="#6FB0C5", fg="#0B2044")
        self.detail_box.grid(row=2, column=2, rowspan=len(self.entry_labels), padx=20, pady=5, sticky="n")

        # Buttons
        self.add_booking_button = tk.Button(self.main_frame, text="Add Booking", command=self.add_booking, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.add_booking_button.grid(row=len(self.entry_labels) + 3, column=0, padx=20, pady=10)

        self.update_booking_button = tk.Button(self.main_frame, text="Update Booking", command=self.update_booking, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.update_booking_button.grid(row=len(self.entry_labels) + 3, column=1, padx=20, pady=10)

        self.delete_booking_button = tk.Button(self.main_frame, text="Delete Booking", command=self.delete_booking, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.delete_booking_button.grid(row=len(self.entry_labels) + 3, column=2, padx=20, pady=10)

        self.generate_bill_button = tk.Button(self.main_frame, text="Generate Bill", command=self.generate_bill, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
        self.generate_bill_button.grid(row=len(self.entry_labels) + 4, column=0, columnspan=2, padx=20, pady=10)

        # Treeview Table
        self.bookings_tree = ttk.Treeview(root, columns=("RoomAvailable", "Contact", "CheckIn", "CheckOut", "RoomType", "Meal", "NoOfDays", "Paid", "Subtotal", "RemainingAmount"), show="headings")
        self.bookings_tree.heading("RoomAvailable", text="Room Available", anchor=tk.CENTER)
        self.bookings_tree.heading("Contact", text="Contact", anchor=tk.CENTER)
        self.bookings_tree.heading("CheckIn", text="Check-In", anchor=tk.CENTER)
        self.bookings_tree.heading("CheckOut", text="Check-Out", anchor=tk.CENTER)
        self.bookings_tree.heading("RoomType", text="Room Type", anchor=tk.CENTER)
        self.bookings_tree.heading("Meal", text="Meal", anchor=tk.CENTER)
        self.bookings_tree.heading("NoOfDays", text="No. of Days", anchor=tk.CENTER)
        self.bookings_tree.heading("Paid", text="Paid", anchor=tk.CENTER)
        self.bookings_tree.heading("Subtotal", text="Subtotal", anchor=tk.CENTER)
        self.bookings_tree.heading("RemainingAmount", text="Remaining Amount", anchor=tk.CENTER)

        self.bookings_tree.column("RoomAvailable", width=80)
        self.bookings_tree.column("Contact", width=80)
        self.bookings_tree.column("CheckIn", width=100)
        self.bookings_tree.column("CheckOut", width=100)
        self.bookings_tree.column("RoomType", width=80)
        self.bookings_tree.column("Meal", width=80)
        self.bookings_tree.column("NoOfDays", width=80)
        self.bookings_tree.column("Paid", width=80)
        self.bookings_tree.column("Subtotal", width=80)
        self.bookings_tree.column("RemainingAmount", width=120)

        self.bookings_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Populate Treeview
        self.populate_treeview()

        # Calculate subtotal automatically based on room type
        self.room_type_var.trace("w", self.calculate_subtotal)

    def calculate_subtotal(self, *args):
        room_type = self.room_type_var.get()
        subtotal = {"Single": 1000, "Double": 2000}.get(room_type, 0)
        self.entries["Subtotal"].delete(0, tk.END)
        self.entries["Subtotal"].insert(0, subtotal)

    def search(self):
        contact = self.search_var.get()
        if not contact:
            self.populate_treeview()  # If no contact is entered, display all bookings
            return

        # Clear existing entries in Treeview
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)

        # Fetch data from the database based on contact
        self.cursor.execute("SELECT * FROM bookings WHERE contact=%s", (contact,))
        bookings = self.cursor.fetchall()

        # Insert filtered bookings into the Treeview
        for booking in bookings:
            self.bookings_tree.insert("", "end", values=booking)

    def fetch_customer_details(self):
        contact = self.entries["Contact"].get()

        if contact:
            try:
                # Fetch customer data from the database using contact
                self.cursor.execute("SELECT * FROM customer WHERE Mobile = %s", (contact,))
                customer_data = self.cursor.fetchone()

                if customer_data:
                    # Display fetched data in the detail box
                    self.detail_box.delete(1.0, tk.END)
                    self.detail_box.insert(tk.END, f"Name: {customer_data[1]}\nGender: {customer_data[2]}\nMobile: {customer_data[3]}\nEmail: {customer_data[4]}\nNationality: {customer_data[5]}\n")
                else:
                    messagebox.showinfo("Info", "No customer found with the provided contact")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please provide a contact")

    def add_booking(self):
        room_available = self.entries["Room Available"].get()
        contact = self.entries["Contact"].get()
        check_in = self.entries["Check-In"].get()
        check_out = self.entries["Check-Out"].get()
        room_type = self.room_type_var.get()
        meal = self.meal_var.get()
        no_of_days = self.entries["No. of Days"].get()
        paid = self.entries["Paid"].get()
        subtotal = self.entries["Subtotal"].get()
        remaining_amount = self.entries["Remaining Amount"].get()

        if all([room_available, contact, check_in, check_out, no_of_days, paid, subtotal, remaining_amount]):
            try:
                # Insert booking into the database
                self.cursor.execute("INSERT INTO bookings (roomavailable, contact, check_in, check_out, Roomtype, meal, noOfdays, paid, subtotal, total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (room_available, contact, check_in, check_out, room_type, meal, no_of_days, paid, subtotal, remaining_amount))
                self.conn.commit()
                messagebox.showinfo("Success", "Booking added successfully")
                self.populate_treeview()  # Update Treeview
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def update_booking(self):
        selected_item = self.bookings_tree.focus()
        if selected_item:
            contact = self.bookings_tree.item(selected_item)['values'][1]
            if contact:
                try:
                    room_available = self.entries["Room Available"].get()
                    check_in = self.entries["Check-In"].get()
                    check_out = self.entries["Check-Out"].get()
                    room_type = self.room_type_var.get()
                    meal = self.meal_var.get()
                    no_of_days = self.entries["No. of Days"].get()
                    paid = self.entries["Paid"].get()
                    subtotal = self.entries["Subtotal"].get()
                    remaining_amount = self.entries["Remaining Amount"].get()

                    existing_values = self.bookings_tree.item(selected_item)['values']
                    if room_available == "":
                        room_available = existing_values[0]
                    if check_in == "":
                        check_in = existing_values[2]
                    if check_out == "":
                        check_out = existing_values[3]
                    if no_of_days == "":
                        no_of_days = existing_values[6]
                    if paid == "":
                        paid = existing_values[7]

                    query = "UPDATE bookings SET roomavailable=%s, check_in=%s, check_out=%s, Roomtype=%s, meal=%s, noOfdays=%s, paid=%s, subtotal=%s, total=%s WHERE contact=%s"
                    self.cursor.execute(query, (room_available, check_in, check_out, room_type, meal, no_of_days, paid, subtotal, remaining_amount, contact))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Booking updated successfully")
                    self.populate_treeview()  # Update Treeview
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
            else:
                messagebox.showerror("Error", "Please select a booking to update")
        else:
            messagebox.showerror("Error", "Please select a booking to update")

    def delete_booking(self):
        selected_item = self.bookings_tree.focus()
        if selected_item:
            contact = self.bookings_tree.item(selected_item)['values'][1]
            if contact:
                try:
                    self.cursor.execute("DELETE FROM bookings WHERE contact=%s", (contact,))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Booking deleted successfully")
                    self.populate_treeview()  # Update Treeview
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
            else:
                messagebox.showerror("Error", "Please select a booking to delete")
        else:
            messagebox.showerror("Error", "Please select a booking to delete")

    def generate_bill(self):
        try:
            subtotal = float(self.entries["Subtotal"].get())
            paid = float(self.entries["Paid"].get())

            remaining_amount = subtotal - paid

            bill_window = tk.Toplevel(self.root)
            bill_window.title("Bill")
            bill_window.geometry("300x150")

            tk.Label(bill_window, text=f"Paid: ${paid}").pack(pady=5)
            tk.Label(bill_window, text=f"Subtotal: ${subtotal}").pack(pady=5)
            tk.Label(bill_window, text=f"Remaining Amount: ${remaining_amount}").pack(pady=5)

            print_button = tk.Button(bill_window, text="Print", command=lambda: self.print_bill(subtotal))
            print_button.pack(pady=10)

            bill_window.mainloop()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for Subtotal and Paid")

    def print_bill(self, total):
        # This function can be customized to implement printing functionality
        print("Printing bill...")
        print("Total Amount:", total)

    def populate_treeview(self):
        # Clear existing entries in Treeview
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)

        # Fetch all bookings from the database
        self.cursor.execute("SELECT * FROM bookings")
        bookings = self.cursor.fetchall()

        # Insert bookings into the Treeview
        for booking in bookings:
            self.bookings_tree.insert("", "end", values=booking)
    
    def go_to_home(self):
    # Destroy all widgets inside the main_frame
        for widget in self.main_frame.winfo_children():
         widget.destroy()

    # Open the home page
        import home
        home_root = tk.Tk()
        app = home.HotelManagementApp(home_root)
        home_root.mainloop()
    
    
# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = BookRoomApp(root)
    root.mainloop()
