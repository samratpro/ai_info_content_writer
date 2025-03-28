from playwright.sync_api import sync_playwright

# Define browser arguments
args = [
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
]


class SerpScrap:
    def __init__(self, keyword, log, END):
        self.keyword = keyword
        self.log = log
        self.END = END

    def visit_serp(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, executable_path="../chrome/chrome.exe", args=args)
            context = browser.new_context(no_viewport=True, locale='en-US',
                                          geolocation={"longitude": 12.4924, "latitude": 41.8902})
            page = context.new_page()
            print("[DEBUG] Go to google...")
            self.log.insert(self.END, "[DEBUG] Go to google...")
            page.goto("https://www.google.com/?gl=us&hl=en&pws=0&gws_rd=cr")
            page.wait_for_load_state("load")
            search_box = page.locator("textarea[name='q']")
            page.screenshot(path="img/1.google_home.png")
            if search_box.count() > 0:
                page.locator("textarea[name='q']").fill(self.keyword)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
                get_main = page.locator("#main")
                page.screenshot(path="img/2.google_serp.png")
                if get_main.count() > 0:
                    text = page.locator("#main").inner_text()
                    browser.close()
                    print("[DEBUG] SERP Scrapped from Google")
                    self.log.insert(self.END, "[DEBUG] SERP Scrapped from Google")
                    return text
                else:
                    print("[DEBUG] Fail google to load main...")
                    self.log.insert(self.END, "[DEBUG] Fail google to load main...")
            else:
                print("[DEBUG] Fail google to load homepage...")
                self.log.insert(self.END, "[DEBUG] Fail google to load homepage...")

            print("[DEBUG] Go to bing...")
            self.log.insert(self.END, "[DEBUG] Go to bing...")
            page.goto("https://www.bing.com")
            page.wait_for_load_state("load")
            search_box = page.locator("textarea[name='q']")
            page.screenshot(path="img/3.bing_home.png")
            if search_box.count() > 0:
                page.locator("textarea[name='q']").fill(self.keyword)
                page.wait_for_timeout(1000)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
                get_main = page.locator("//main")
                page.screenshot(path="img/4.bing_serp.png")
                if get_main.count() > 0:
                    text = page.locator("//main").inner_text()
                    browser.close()
                    print("[DEBUG] SERP Scrapped from Bing")
                    self.log.insert(self.END, "[DEBUG] SERP Scrapped from Bing")
                    return text
                else:
                    print("[DEBUG] Fail bing to load main...")
                    self.log.insert(self.END, "[DEBUG] Fail bing to load main...")
            else:
                print("[DEBUG] Fail bing to load homepage...")
                self.log.insert(self.END, "[DEBUG] Fail bing to load homepage...")

            print("[DEBUG] Go to duckduckgo...")
            self.log.insert(self.END, "[DEBUG] Go to duckduckgo...")
            page.goto("https://duckduckgo.com/")
            page.wait_for_load_state("load")
            search_box = page.locator("input[name='q']")
            page.screenshot(path="img/5.duckduckgo_home.png")
            if search_box.count() > 0:
                page.locator("input[name='q']").fill(self.keyword)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
                get_main = page.locator("//ol[@class='react-results--main']")
                page.screenshot(path="img/6.duckduckgo_serp.png")
                if get_main.count() > 0:
                    text = page.locator("//ol[@class='react-results--main']").inner_text()
                    browser.close()
                    print("[DEBUG] SERP Scrapped from duckduckgo")
                    self.log.insert(self.END, "[DEBUG] SERP Scrapped from duckduckgo")
                    return text
                else:
                    print("[DEBUG] Fail duckduckgo to load main...")
                    self.log.insert(self.END, "[DEBUG] Fail duckduckgo to load main...")
            else:
                print("[DEBUG] Fail duckduckgo to load homepage...")
                self.log.insert(self.END, "[DEBUG] Fail duckduckgo to load homepage...")

            print("[DEBUG] Go to ecosia..")
            self.log.insert(self.END, "[DEBUG] Go to ecosia..")
            page.goto("https://www.ecosia.org/")
            page.wait_for_load_state("load")
            search_box = page.locator("input[name='q']")
            page.screenshot(path="img/7.ecosia_home.png")
            if search_box.count() > 0:
                page.locator("input[name='q']").fill(self.keyword)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
                get_main = page.locator("//main")
                page.screenshot(path="img/8.ecosia_serp.png")
                if get_main.count() > 0:
                    text = page.locator("//main").inner_text()
                    browser.close()
                    print("[DEBUG] SERP Scrapped from duckduckgo")
                    self.log.insert(self.END, "[DEBUG] SERP Scrapped from duckduckgo")
                    return text
                else:
                    print("[DEBUG] Fail ecosia to load main...")
                    self.log.insert(self.END, "[DEBUG] Fail ecosia to load main...")
                    browser.close()
                    return ''
            else:
                print("[DEBUG] Fail ecosia to load homepage...")
                self.log.insert(self.END, "[DEBUG] Fail ecosia to load homepage...")
                browser.close()
                return ''
