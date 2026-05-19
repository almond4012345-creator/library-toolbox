import os
import time
import requests
import base64
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_get_covers(input_file):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        image_folder = os.path.join(download_path, "抓取的封面圖片")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        df = pd.read_excel(input_file, usecols=[0, 1], names=['編號', 'ISBN'], dtype=str)
        books = df.dropna(subset=['編號', 'ISBN'])

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.set_window_size(1100, 850)
        
        driver.get("https://www.google.com")
        time.sleep(15)

        for index, row in books.iterrows():
            book_id = str(row['編號']).strip()
            isbn = str(row['ISBN']).replace('-', '').replace(' ', '').strip()
            if not book_id.isdigit() or len(isbn) < 10:
                continue

            driver.get(f"https://www.google.com/search?q={isbn}&tbm=isch")
            try:
                img_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img.YQ4gaf, img.Q4LuWd, img.rg_i'))
                )
                time.sleep(1)
                img_src = img_element.get_attribute('src') or img_element.get_attribute('data-src')
                file_path = os.path.join(image_folder, f"{book_id}.jpg")
                if img_src and img_src.startswith('data:image'):
                    header, data = img_src.split(',', 1)
                    img_data = base64.b64decode(data)
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                elif img_src and img_src.startswith('http'):
                    img_data = requests.get(img_src, timeout=10).content
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
            except:
                continue
        driver.quit()
        return True, image_folder
    except Exception as e:
        return False, str(e)