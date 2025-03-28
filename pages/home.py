from customtkinter import *
from playwright.sync_api import sync_playwright
import webbrowser, threading, os, json
from tkinter import END
from time import sleep
from random import choice
import re
import requests
import httpx
import base64
from task.feature_img_generator import FeatureImageCreate
from task.content_writer import ContentWriter
from task.serp_scrapper import SerpScrap
from task.create_category import create_category
from models import Postdata, Session


class HomePage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_path = os.path.join(os.getcwd(), "appdata/info_data")
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.template_path = os.path.join(self.base_path, "template")
        if not os.path.exists(self.template_path):
            os.makedirs(self.template_path)
        self.chrome_path = os.path.join(os.getcwd(), "chrome/chrome.exe")
        self.db_path = os.path.join(self.base_path, "database.db")
        self.keyword_path = 'no_path'

        ## checking number of logins and path
        self.json_files = [f for f in os.listdir(self.base_path) if f.endswith('.json')]
        self.cookie_path = os.path.join(os.getcwd(), f"{self.base_path}/cookie.json")

        # main labale
        self.label = CTkLabel(self, text="Info Writer Page", height=30, width=200, font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # main scroll frame
        self.scrollable_frame = CTkScrollableFrame(self, width=500, height=400, border_width=1)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # API Frame
        self.api_frame = CTkFrame(self.scrollable_frame)
        self.api_frame.grid(pady=10, padx=20)

        self.open_button = CTkButton(self.api_frame, text="Open Browser", width=200, fg_color=('#006262'),
                                     corner_radius=20, command=lambda: self.browser_open())
        self.open_button.grid(row=1, column=0, padx=10, pady=10)

        self.close_button = CTkButton(self.api_frame, text="Save Cookie", width=200, fg_color=('#006262'),
                                      corner_radius=20, command=lambda: self.browser_close())
        self.close_button.grid(row=1, column=1, padx=10, pady=10)

        self.cookie_status = CTkLabel(self.api_frame, width=300, text=f"Cookie Status: ", corner_radius=20,
                                      fg_color=('#9457EB'), text_color=('#E1E8FF'))
        if os.path.exists(self.cookie_path):
            self.cookie_status.configure(text="Cookie Status : True")
        else:
            self.cookie_status.configure(text="Cookie Status : False")
        self.cookie_status.grid(row=1, column=2, padx=10, pady=10)

        # Keyword frame
        def select_file():
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text File", "*.txt")])
            self.keyword_path = os.path.join(os.getcwd(), file_path)
            if self.keyword_path:
                self.file_label.configure(text=self.keyword_path)

        self.keyword_frame = CTkFrame(self.scrollable_frame, border_width=1)
        self.keyword_frame.grid(pady=10, padx=10)
        self.keyword_label = CTkLabel(self.keyword_frame,
                                      text='Select Keyword File : ',
                                      anchor='w',
                                      width=60
                                      )
        self.keyword_label.grid(row=0, column=0, pady=10, padx=10)

        self.upload_button = CTkButton(self.keyword_frame,
                                       text="Select File",
                                       command=lambda: select_file(),
                                       anchor='center',
                                       width=30
                                       )
        self.upload_button.grid(row=0, column=1, pady=10, padx=10)

        self.file_label = CTkLabel(self.keyword_frame,
                                   text="No file selected",
                                   anchor='e',
                                   width=480
                                   )
        self.file_label.grid(row=0, column=2, pady=10, padx=10)

        # Command
        self.command_label = CTkFrame(self.scrollable_frame, fg_color=('#DBDBDB'))
        self.command_label.grid(pady=10, padx=20)
        self.start = CTkButton(self.command_label, text="▶️ Run", width=167, fg_color=('#006262'), corner_radius=20,
                               command=lambda: self.operation_start())
        self.start.grid(row=0, column=0, padx=5, pady=10, ipadx=5)
        self.stop = CTkButton(self.command_label, text="⏹️ Stop", width=167, fg_color=('#9457EB'), corner_radius=20,
                              command=lambda: self.operation_close())
        self.stop.grid(row=0, column=1, padx=5, pady=10, ipadx=5)

        # Log
        self.log = CTkTextbox(self.scrollable_frame, width=750, height=300, fg_color=('black', 'white'),
                              text_color=('white', 'black'), wrap="none")
        self.log.grid(row=11, column=0, padx=5, pady=(5, 10))

        self.copyright = CTkLabel(self.scrollable_frame, text="Need any help ?", width=700)
        self.copyright.grid(row=12, column=0, padx=5, pady=(5, 0))
        self.copy_button = CTkButton(self.scrollable_frame, text="Contact With Developer", fg_color=('#2374E1'),
                                     command=lambda: webbrowser.open_new('https://www.facebook.com/samratprodev/'))
        self.copy_button.grid(row=13, column=0, padx=5, pady=(5, 300))

        # login funcationality
        self.browser_close_event = threading.Event()
        self.args = [
            '--disable-blink-features=AutomationControlled',
            '--start-maximized',
            '--disable-infobars',
            '--no-sandbox',
            '--enable-gpu',
            '--use-gl=desktop',
            '--enable-webgl',
            '--enable-accelerated-2d-canvas',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--remote-debugging-port=0',
            '--disable-web-security',
            '--enable-features=WebRTCPeerConnectionWithBlockIceAddresses',
            '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',
            '--disable-third-party-cookies',  # Prevent third-party cookies from being blocked
        ]

    def is_storage_state_valid(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    return bool(data)  # true false depend data exist
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return False
        else:
            open(file_path, 'w').close()  # Create an empty file
            return False

    def cookie_save(self, log, close_event):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=self.chrome_path,
                headless=False,
                args=self.args
            )
            # Create a new context and page
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            try:
                page.goto("https://Info.com", timeout=120000)
            except Exception as e:
                log.insert(END, f"Error navigating to Info: {e}\n")
                log.see(END)
                browser.close()
                return

            def check_close_event():
                if page.is_closed():
                    log.insert(END, "Browser closed or crashed. Exiting...\n")
                    log.see(END)
                    print("Browser closed or crashed. Exiting...")
                    return

                # Check if the close_event is set
                if not close_event.is_set():
                    sleep(5)  # Wait for 5 seconds
                    check_close_event()  # Recursive call
                else:
                    try:
                        context.storage_state(path=self.cookie_path)
                        self.cookie_status.configure(text=f"Cookie Status : True")
                        print("Login Data saved...")
                        log.insert(END, "Login Data saved...\n")
                        log.see(END)
                    except Exception as e:
                        log.insert(END, f"Error saving login data: {e}\n")
                        log.see(END)
                    finally:
                        if browser.is_connected():
                            browser.close()
                        log.insert(END, "Browser closed.\n")
                        log.see(END)

            check_close_event()

    def browser_open(self):
        thread = threading.Thread(target=self.browser_open_thread)
        thread.start()

    def browser_open_thread(self):
        # Clear the event if the browser is being opened
        self.browser_close_event.clear()
        self.cookie_save(self.log, close_event=self.browser_close_event)

    def browser_close(self):
        # Set the event to signal the browser should close
        self.browser_close_event.set()

    operation_close_event = threading.Event()

    def operation_start(self):
        if self.keyword_path != 'no_path':
            self.start.configure(text="⌛️ Running...")
            thread = threading.Thread(target=self.operation_start_thread)
            thread.start()
        else:
            print(f'Please select Keyword path..\n\n')
            self.log.insert(END, f'Please select Keyword path..\n\n')

    def operation_close(self):
        self.start.configure(text="▶️ Run")
        self.operation_close_event.set()

    def stop_check(self, event, log) -> bool:
        if event:
            print("⏹️ Stopped...")
            log.insert(END, f"⏹️ Stopped...\n\n")
            log.see(END)
            return True
        else:
            return False

    def operation_start_thread(self):
        keyword_path = self.keyword_path
        with open(keyword_path, 'r') as file:
            keyword_data = file.readlines()
            file.close()
        keywords_list = [x.strip() for x in keyword_data if len(x) > 0]

        self.operation_close_event.clear()

        print('keywords_list : ', keywords_list)

        self.posting_loop(keywords_list, self.log, close_event=self.operation_close_event)

    # Seperate function

    # Main posting loop
    def posting_loop(self, keywords_list, log, close_event):
        session = Session()
        settings = session.query(Postdata).filter_by(id=1).first()
        website = settings.website_name
        username = settings.username
        app_pass = settings.app_pass
        credentials = f"{username}:{app_pass}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        headers = {"Authorization": f"Basic {encoded_credentials}", }
        i = 1
        for keyword in keywords_list:
            if self.stop_check(close_event.is_set(), log):
                break  # Stop if the close_event is triggered
            log.insert(END, f"{str(i)}. Keyword : {keyword}\n\n")
            serp = SerpScrap(keyword, log, END)
            serp_data = serp.visit_serp()

            content_writer = ContentWriter(keyword, serp_data, log, END)
            title = content_writer.title_section()
            wp_content = content_writer.generate_content()
            category_id = create_category()

            Img = FeatureImageCreate()

            if category_id is None:
                post_data = {
                    'title': title,
                    'slug': keyword.replace(' ', '-'),
                    'status': "publish",
                    'content': wp_content,
                    'format': 'standard',
                    'featured_media': Img.feature_image(keyword, log, END),
                }
            else:
                post_data = {
                    'title': title,
                    'slug': keyword.replace(' ', '-'),
                    'status': "publish",
                    'content': wp_content,
                    'categories': [category_id],  # Ensure category_id is a list with an integer ID
                    'format': 'standard',
                    'featured_media': Img.feature_image(keyword, log, END),
                }

                # Posting Request
            try:
                # Posting Request
                response = httpx.post(website + 'wp-json/wp/v2/posts', headers=headers, json=post_data,
                                      timeout=30)

                if response.status_code == 201:
                    print("Post created successfully!")
                    print("Response:", response.json())  # The created post data
                    print('link : ', response.json().get('guid').get('rendered'))
                    log.insert(END, f'[DEBUG] Success, link : {response.json().get('guid').get('rendered')}\n\n')
                else:
                    print(f"Failed to create post. Status code: {response.status_code}")
                    print("Response:", response.json())  # Error details
                    print("[DEBUG]Fail, Response:", response.json())  # Error details
                    log.insert(END, f"[DEBUG]Fail, Response: {response.json()}\n\n")  # Error details
            except httpx.ConnectError as e:
                self.log.insert(END, f"[DEBUG] Connection error: {e}\n\n")
                print(f"Connection error: {e}")
            except httpx.RequestError as e:
                self.log.insert(END, f"[DEBUG] Request error: {e}\n\n")
                print(f"Request error: {e}")
            except Exception as e:
                self.log.insert(END, f"[DEBUG] General error: {e}\n\n")
                print(f"General error: {e}")
            i += 1
