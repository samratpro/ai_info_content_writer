import urllib
import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright
from models import Postdata, Session

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

class AmazonVisit:
    _playwright = None
    browser = None
    page = None

    def __init__(self, link, log, END):
        self.link = link
        self.log = log
        self.END = END

    @classmethod
    def start_playwright(cls):
        if cls._playwright is None:
            cls._playwright = sync_playwright().start()
            cls.browser = cls._playwright.chromium.launch(headless=False, args=args, executable_path="chrome/chrome.exe")
            cls.page = cls.browser.new_page(storage_state="appdata/amazon_data/cookie.json", no_viewport=True)

    @classmethod
    def stop_playwright(cls):
        if cls._playwright is not None:
            cls.browser.close()
            cls._playwright.stop()
            cls._playwright = None
            cls.browser = None
            cls.page = None

    def visit_amazon(self):
        print(f"[DEBUG]  Visiting Amazon link with httpx: {self.link}")
        # self.log.insert(self.END, f"[DEBUG]  Visiting Amazon link with httpx: {self.link}\n")
        session = httpx.Client()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1"
        }
        response = session.get(self.link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find("h1")
            if title:
                return response.text
        print("[DEBUG]  Visiting Amazon link with httpx failed (Trying with Playwright)...")
        self.log.insert(self.END, "[DEBUG]  Visiting Amazon link with httpx failed (Trying with Playwright)...\n")
        return self.visit_amazon_with_playwright()

    def visit_amazon_with_playwright(self):
        AmazonVisit.start_playwright()
        print(f"[DEBUG]  Now visiting Amazon link with Playwright: {self.link}")
        self.log.insert(self.END, f"[DEBUG]  Now visiting Amazon link with Playwright: {self.link}\n")
        AmazonVisit.page.goto(self.link, timeout=60000)
        AmazonVisit.page.wait_for_load_state("load")
        content = AmazonVisit.page.content()
        return content

class AmazonSERPExtractor(AmazonVisit):
    session = Session()
    setting = session.query(Postdata).filter_by(id=1).first()
    if setting:
        product_number = setting.product_number
    else:
        product_number = 10

    def __init__(self, keyword, log, END):
        self.keyword = keyword
        self.search_link = f"https://www.amazon.com/s?k={self.keyword.replace(' ', '+')}"
        super().__init__(self.search_link, log, END)

    def search_amazon(self):
        html_content = self.visit_amazon()
        return self.extract_links(html_content)

    def get_product_number(self):
        try:
            if int(self.product_number) > 0:
                return int(self.product_number)
            else:
                return 10
        except:
            return 10

    def extract_links(self, html_content):
        print("[DEBUG]  Extracting Product links From Amazon...")
        self.log.insert(self.END, "[DEBUG]  Extracting Products From Amazon...\n")
        soup = BeautifulSoup(html_content, "html.parser")
        links = []
        for element in soup.find_all("div", {"data-component-type": "s-search-result"}):
            a_tag = element.find("a", {"class": "a-link-normal"})
            if a_tag:
                href = a_tag["href"]
                if "/dp/" in href and href not in links:  # Look for product links
                    links.append("https://www.amazon.com" + href.split("ref")[0])
                if len(links) >= self.get_product_number():
                    break
        return links

class ProductDataExtractor(AmazonVisit):
    def __init__(self, link_list, log, END):
        self.link_list = link_list
        self.product_data = []
        self.log = log
        self.END = END

    def extract_product_data(self):
        for link in self.link_list:
            print(f"[DEBUG]  Extracting data from product link: {link}")
            # self.log.insert(self.END, f"[DEBUG]  Extracting data from product link: {link}\n")
            super().__init__(link, self.log, self.END)
            html_content = self.visit_amazon()
            self.product_data.append(self.parse_product_page(html_content, link))
        AmazonVisit.stop_playwright()
        return self.product_data

    def parse_product_page(self, html_content, link):
        print("[DEBUG]  Parsing product page...")
        # self.log.insert(self.END, "[DEBUG]  Parsing product page...\n")
        soup = BeautifulSoup(html_content, "html.parser")
        product_title = soup.find(id="productTitle").get_text(strip=True) if soup.find(id="productTitle") else "NO Title"
        img_tag_wrapper = soup.find('div', {"id": "imgTagWrapperId"})
        image = img_tag_wrapper.find('img').get('src') if img_tag_wrapper else "Image not found"
        price = soup.find("span", {"class": "a-price-whole"}).get_text(strip=True) if soup.find("span", {
            "class": "a-price-whole"}) else "Price not found"
        description = soup.find("div", {"id": "feature-bullets"}).get_text(strip=True) if soup.find("div", {
            "id": "feature-bullets"}) else ""
        technical_data = soup.find("table", {'class': 'a-keyvalue prodDetTable'}).get_text(strip=True) if soup.find("table",
            {'class': 'a-keyvalue prodDetTable'}) else ""
        review = soup.find("div", {'data-hook':'review-collapsed'}).get_text(strip=True) if soup.find("div",
            {'data-hook':'review-collapsed'}) else ""
        data_ok = True
        if product_title == "NO Title":
            data_ok = False
        return {
            "data_ok": data_ok,
            "link": link,
            "title": product_title.replace("Amazon.com: ",""),
            "image": image,
            "price": price,
            "description": description,
            "technical_data": technical_data,
            "review": review
        }