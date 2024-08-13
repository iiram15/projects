import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os

class ReportPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Report")
        self.root.geometry("1920x1080")
        
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

        # Room Selection Frame
        self.room_frame = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE, bg=self.secondary_color)
        self.room_frame.pack(pady=20, padx=20)

        # Room Selection Labels and Dropdowns
        tk.Label(self.room_frame, text="Room No:", bg=self.secondary_color, fg=self.text_color).grid(row=0, column=0, padx=5, pady=5)
        self.room_no_var = tk.StringVar()
        self.room_no_var.set("100")  # Default value
        self.room_no_dropdown = ttk.Combobox(self.room_frame, textvariable=self.room_no_var, state="readonly")
        self.room_no_dropdown['values'] = [str(i) for i in range(100, 201)]
        self.room_no_dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.room_frame, text="Room Type:", bg=self.secondary_color, fg=self.text_color).grid(row=1, column=0, padx=5, pady=5)
        self.room_type_var = tk.StringVar()
        self.room_type_var.set("Single")  # Default value
        self.room_type_dropdown = ttk.Combobox(self.room_frame, textvariable=self.room_type_var, state="readonly")
        self.room_type_dropdown['values'] = ["Single", "Double"]
        self.room_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.room_frame, text="Floor:", bg=self.secondary_color, fg=self.text_color).grid(row=2, column=0, padx=5, pady=5)
        self.floor_var = tk.StringVar()
        self.floor_var.set("1")  # Default value
        self.floor_dropdown = ttk.Combobox(self.room_frame, textvariable=self.floor_var, state="readonly")
        self.floor_dropdown['values'] = ["1", "2"]
        self.floor_dropdown.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.room_frame, text="Status:", bg=self.secondary_color, fg=self.text_color).grid(row=3, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Available")  # Default value
        self.status_dropdown = ttk.Combobox(self.room_frame, textvariable=self.status_var, state="readonly")
        self.status_dropdown['values'] = ["Booked", "Available"]
        self.status_dropdown.grid(row=3, column=1, padx=5, pady=5)

        # CRUD Buttons
        self.update_button = tk.Button(self.room_frame, text="Update", command=self.update_room_status, bg=self.button_color, fg=self.text_color)
        self.update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.add_button = tk.Button(self.room_frame, text="Add", command=self.add_room_status, bg=self.button_color, fg=self.text_color)
        self.add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Book Button
        self.book_button = tk.Button(self.room_frame, text="Book", command=self.open_room_page, bg=self.button_color, fg=self.text_color)
        self.book_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Fetch Button
        self.fetch_button = tk.Button(self.room_frame, text="Fetch", command=self.fetch_status, bg=self.button_color, fg=self.text_color)
        self.fetch_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Status Display Label
        self.status_label = tk.Label(root, text="", bg="white", width=30)
        self.status_label.pack()

    def update_room_status(self):
        room_no = self.room_no_var.get()
        status = self.status_var.get()

        if room_no:
            try:
                # Construct and execute the SQL query
                sql_query = "UPDATE report SET Status = %s WHERE RoomNo = %s"
                values = (status, room_no)
                self.cursor.execute(sql_query, values)
                self.conn.commit()

                # Display success message
                messagebox.showinfo("Success", f"Room {room_no} status updated successfully")
            except mysql.connector.Error as err:
                # Handle any errors that occur during execution
                print("Error:", err)
                messagebox.showerror("Error", f"An error occurred: {err}")
        else:
            messagebox.showerror("Error", "Please select a room number")

    def add_room_status(self):
        room_no = self.room_no_var.get()
        room_type = self.room_type_var.get()
        floor = self.floor_var.get()
        status = self.status_var.get()

        try:
            # Construct and execute the SQL query
            sql_query = "INSERT INTO report (RoomNo, RoomType, Floor, Status) VALUES (%s, %s, %s, %s)"
            values = (room_no, room_type, floor, status)
            self.cursor.execute(sql_query, values)
            self.conn.commit()

            # Display success message
            messagebox.showinfo("Success", f"Room {room_no} added successfully")
        except mysql.connector.Error as err:
            # Handle any errors that occur during execution
            print("Error:", err)
            messagebox.showerror("Error", f"An error occurred: {err}")

    def fetch_status(self):
        try:
            self.cursor.execute("SELECT * FROM report")
            data = self.cursor.fetchall()

            message = "Room Details:\n\n"
            for row in data:
                message += f"Room No: {row[0]}\n"
                message += f"Room Type: {row[1]}\n"
                message += f"Floor: {row[2]}\n"
                message += f"Status: {row[3]}\n\n"

            messagebox.showinfo("Room Details", message)
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", f"An error occurred: {err}")

    def open_room_page(self):
        # Open room.py file upon clicking the Book button
        os.system("python room.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportPage(root)
    root.mainloop()
