from customtkinter import *
from pages.settings import SettingsPage
from pages.home import HomePage
from pages.login import LoginPage
from datetime import datetime
from PIL import Image  # Import PIL for image handling

target_date = datetime(2024, 12, 13)
current_date = datetime.now()

set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light")
set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue")


class DashboardApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Amazon App Dashboard")
        self.geometry("1000x700")

        # Initially, show the login page
        self.show_login_page()

    def show_login_page(self):
        """Displays the login page."""
        self.login_page = LoginPage(self)
        self.login_page.pack(fill="both", expand=True)

    def on_login_success(self):
        """Callback for successful login."""
        self.login_page.destroy()
        self.show_dashboard()

    def show_dashboard(self):
        """Displays the main dashboard after login."""
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)  # Main content area
        self.grid_rowconfigure(0, weight=1)

        # Create Left Side Menu
        self.menu_frame = CTkFrame(self, width=200, fg_color="#2B2B2B", corner_radius=0)  # Set fg_color to a green shade
        self.menu_frame.grid(row=0, column=0, sticky="nswe")

        self.current_button = None  # Track the currently selected button
        self.menu_buttons = {}  # Store menu buttons for resetting colors

        self.create_menu_buttons()

        # Create Main Content Frame
        self.content_frame = CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Pages Dictionary
        self.pages = {
            "Home": HomePage(self.content_frame),
            "Settings": SettingsPage(self.content_frame),
        }

        # Default page
        self.show_page("Home")

    def create_menu_buttons(self):
        """Creates buttons for the menu individually without a loop."""
        # Load icons
        home_icon_image = Image.open("icons/home.png")
        home_icon = CTkImage(home_icon_image)
        settings_icon_image = Image.open("icons/settings.png")
        settings_icon = CTkImage(settings_icon_image)
        logout_icon_image = Image.open("icons/logout.png")
        logout_icon = CTkImage(logout_icon_image)

        # Create Home button
        home_button = CTkButton(
            self.menu_frame,
            text="Home",
            command=lambda: self.on_button_click("Home", "Home"),
            fg_color="black",
            hover_color="black",
            image=home_icon,
            compound="left",  # Display image to the left of the text
            anchor="w"  # Align content to the west (left)
        )
        home_button.grid(row=0, column=0, pady=(20, 5), padx=10, sticky="ew")
        self.menu_buttons["Home"] = home_button

        # Create Settings button
        settings_button = CTkButton(
            self.menu_frame,
            text="Settings",
            command=lambda: self.on_button_click("Settings", "Settings"),
            fg_color="#2B2B2B",
            hover_color="black",
            image=settings_icon,
            compound="left",  # Display image to the left of the text
            anchor="w"  # Align content to the west (left)
        )
        settings_button.grid(row=1, column=0, pady=(5, 5), padx=10, sticky="ew")
        self.menu_buttons["Settings"] = settings_button

        # Create Logout button
        logout_button = CTkButton(
            self.menu_frame,
            text="Logout",
            command=self.logout,
            fg_color="#2B2B2B",
            hover_color="darkred",
            image=logout_icon,
            compound="left",  # Display image to the left of the text
            anchor="w",  # Align content to the west (left)
        )
        logout_button.grid(row=2, column=0, pady=(10, 20), padx=10, sticky="ew")
        self.menu_buttons["Logout"] = logout_button

        self.menu_frame.grid_rowconfigure(3, weight=1)
        logout_button.grid(row=3, column=0, pady=(10, 20), padx=10, sticky="sew")

    def on_button_click(self, page_name, button_label):
        """Handles button click events."""
        self.show_page(page_name)

        # Reset the colors of all buttons
        for btn_label, btn in self.menu_buttons.items():
            btn.configure(fg_color="#2B2B2B")  # Reset to default

        # Highlight the selected button
        selected_button = self.menu_buttons.get(button_label)
        if selected_button:
            selected_button.configure(fg_color="black")
            self.current_button = selected_button

    def show_page(self, page_name):
        """Displays the selected page."""
        # Destroy existing widgets
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

        # Add the selected page
        page = self.pages.get(page_name)
        if page:
            page.pack(fill="both", expand=True)

    def logout(self):
        """Handles logout."""
        for widget in self.winfo_children():
            widget.destroy()
        self.show_login_page()


if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()