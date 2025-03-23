import urllib
import httpx
from random import choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageFile, UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True
import base64
import os
import json
from models import Postdata, Session


class FeatureImageCreate:
    session = Session()
    settings = session.query(Postdata).filter_by(id=1).first()
    if settings:
        username = settings.username
        app_pass = settings.app_pass
        website = settings.website_name
    else:
        username = "admin"
        app_pass = "xxx"
        website = "https://website.com"

    def __init__(self):
        self.website = self.website
        self.credentials = f"{self.username}:{self.app_pass}"
        self.encoded_credentials = base64.b64encode(self.credentials.encode('utf-8')).decode('utf-8')
        self.headers = {"Authorization": f"Basic {self.encoded_credentials}", }

    def feature_image(self, keyword, product_data, log, END):
        # Create an img name Folder
        link1 = product_data[0]['image']
        link2 = product_data[1]['image']
        print("link1 : ", link1)
        print("link2 : ", link2)
        print("self.headers : ", self.headers)

        dirName = 'appdata/img'
        if not os.path.exists(dirName):
            os.mkdir(dirName)

        try:
            urllib.request.urlretrieve(link1, 'appdata/img/1.jpg')
            urllib.request.urlretrieve(link2, 'appdata/img/2.jpg')
        except Exception as e:
            print(f"[ERROR] Image download failed: {e}")
            return 0

        try:
            image1 = Image.open('appdata/img/1.jpg')
            image2 = Image.open('appdata/img/2.jpg')
        except UnidentifiedImageError as e:
            print(f"[ERROR] Cannot identify image file: {e}")
            return 0

        # Fixed final size
        final_width, final_height = 720, 480
        max_product_width, max_product_height = 320, 400

        # Resize images proportionally to fit within max size
        image1.thumbnail((max_product_width, max_product_height), Image.LANCZOS)
        image2.thumbnail((max_product_width, max_product_height), Image.LANCZOS)

        # Create a new blank image
        new_image = Image.new('RGB', (final_width, final_height), (255, 255, 255))

        # Calculate positions to center images
        x1 = (final_width // 2 - image1.width) // 2
        x2 = final_width // 2 + ((final_width // 2 - image2.width) // 2)
        y_offset = (final_height - max(image1.height, image2.height)) // 2

        # Paste images
        new_image.paste(image1, (x1, y_offset))
        new_image.paste(image2, (x2, y_offset))

        # Save image
        image_name = keyword.replace('/', ' ').replace('#', ' ').strip()
        new_image.save(f'appdata/img/{image_name}.jpg')

        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(new_image)
        words = keyword.title().split()
        max_words_per_line = 10
        wrapped_text = [" ".join(words[i:i + max_words_per_line]) for i in range(0, len(words), max_words_per_line)]
        line_height = font.getbbox('A')[3] - font.getbbox('A')[1]
        total_text_height = len(wrapped_text) * line_height + (len(wrapped_text) - 1) * 10
        text_y = final_height - total_text_height - 20
        text_color = choice(['#1E1F22', '#000000', '#3C3F41'])

        for line in wrapped_text:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (final_width - text_width) // 2
            draw.text((text_x, text_y), line, font=font, fill=text_color)
            text_y += line_height + 10

        new_image.save(f'appdata/img/{image_name}.jpg')

        # Upload to WordPress
        try:
            media = {'file': open(f'appdata/img/{image_name}.jpg', 'rb')}
            image = httpx.post(self.website + 'wp-json/wp/v2/media', headers=self.headers, files=media, timeout=30)
            image_data = image.json()
            post_id = image_data['id']

            print("post_id : ", post_id)
            return post_id
        except Exception as e:
            print('[ERROR] WordPress posting failed:', str(e))
            return 0



