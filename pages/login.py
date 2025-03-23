from customtkinter import *
from tkinter import messagebox
from datetime import datetime

target_date = datetime(2026, 12, 13)
current_date = datetime.now()

class LoginPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.configure(fg_color="#CFCFCF")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = CTkFrame(self, width=400, height=300, corner_radius=10, fg_color="#CFCFCF")
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(0, weight=1)

        self.center_frame = CTkFrame(self.login_frame, width=500, height=300, corner_radius=10, fg_color="#CFCFCF")
        self.center_frame.grid(row=0, column=0, padx=20, pady=20)

        self.center_frame.grid_columnconfigure(1, weight=1)

        self.username_label = CTkLabel(self.center_frame, text="Username:", font=("Arial", 14))
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.username_entry = CTkEntry(self.center_frame, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.password_label = CTkLabel(self.center_frame, text="Password:", font=("Arial", 14))
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = CTkEntry(self.center_frame, show="*", font=("Arial", 14))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.login_button = CTkButton(self.center_frame, text="Login", fg_color=("#2B2B2B"), hover_color=("black"), font=("Arial", 14), command=self.validate_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        self.error_label = CTkLabel(self.center_frame, text="", text_color="red", font=("Arial", 14))
        self.error_label.grid(row=3, column=0, columnspan=2)
        self.error_label.grid_remove()  # Hide the error label initially

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if current_date > target_date:
            self.error_label.configure(text="Subscription expired")
            self.error_label.grid()  # Show the error label if subscription is expired
        elif username == "admin" and password == "admin":
            self.error_label.grid_remove()  # Hide the error label if login is successful
            self.master.on_login_success()
        else:
            self.error_label.configure(text="Invalid username or password")
            self.error_label.grid()  # Show the error label if login fails