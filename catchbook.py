import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import pyperclip
import os

def run_catchbook(input_file):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        output_file = os.path.join(download_path, "查價結果.xlsx")
        ??
        df_input = pd.read_excel(input_file, header=None)
        book_titles = [str(t).strip() for t in df_input[0].tolist() if pd.notna(t)]

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        def wait_for_copy():
            old_content = pyperclip.paste()
            while True:
                current_content = pyperclip.paste()
                if current_content != old_content:
                    return current_content.strip()

        results = []
        for title in book_titles:
            current_data = {"書名": title, "ISBN": "", "出版社": "", "年份": "", "價錢": ""}
            driver.get(f"https://www.google.com/search?q={urllib.parse.quote(title + ' 出版資料')}")
            current_data["ISBN"] = wait_for_copy()
            current_data["出版社"] = wait_for_copy()
            current_data["年份"] = wait_for_copy()
            
            driver.get(f"https://www.google.com/search?q={urllib.parse.quote(title + ' 定價')}")
            current_data["價錢"] = wait_for_copy()
            results.append(current_data)

        pd.DataFrame(results).to_excel(output_file, index=False)
        driver.quit()
        return True, output_file
    except Exception as e:
        return False, str(e)
