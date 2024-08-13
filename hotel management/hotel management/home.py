import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os

from customer import CustomerManagementApp
from report import ReportPage
from room import BookRoomApp

class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("Hotel Management System")
        
        # Fetch screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Download the image from URL
        response = requests.get("https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")
        image_data = response.content
        self.background_image = Image.open(BytesIO(image_data))

        # Resize the image to fit the screen
        self.background_image = self.background_image.resize((screen_width, screen_height))
        self.background_image = ImageTk.PhotoImage(self.background_image)
        
        # Background Label
        background_label = tk.Label(root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menu Frame
        menu_frame = tk.Frame(root, bg="white", pady=20)
        menu_frame.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Customer Details Button with Image
        customer_button = tk.Button(menu_frame, text="Customer Details", command=self.open_customer_page, bg="#4CAF50", fg="white", padx=20, pady=10, font=("Arial", 12, "bold"))
        customer_button.grid(row=0, column=0, padx=10)

        # Book Room Button with Image
        book_room_button = tk.Button(menu_frame, text="Book Room", command=self.open_book_room, bg="#008CBA", fg="white", padx=20, pady=10, font=("Arial", 12, "bold"))
        book_room_button.grid(row=0, column=1, padx=10)

        # Report Button with Image
        report_button = tk.Button(menu_frame, text="Report", command=self.open_report, bg="#f44336", fg="white", padx=20, pady=10, font=("Arial", 12, "bold"))
        report_button.grid(row=0, column=2, padx=10)

        # Logout Button with Image
        logout_button = tk.Button(menu_frame, text="Logout", command=self.logout, bg="#555555", fg="white", padx=20, pady=10, font=("Arial", 12, "bold"))
        logout_button.grid(row=0, column=3, padx=10)

    def open_customer_page(self):
        customer_window = tk.Toplevel(self.root)
        customer_app = CustomerManagementApp(customer_window)

    def open_book_room(self):
        room_window = tk.Toplevel(self.root)
        room_app = BookRoomApp(room_window)
        
    def open_report(self):
        report_window = tk.Toplevel(self.root)
        report_app = ReportPage(report_window)

    def logout(self):
        # Perform logout and direct to register.py
        os.system("python register.py")
        self.root.destroy()  # Close the current window

# Create the main window
if __name__ == "__main__":
    root = tk.Tk()

    # Create an instance of HotelManagementApp
    app = HotelManagementApp(root)

    # Run the Tkinter event loop
    root.mainloop()
