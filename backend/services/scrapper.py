from pathlib import Path
import os
import base64

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from db.session import SessionLocal
from db.models.articles import Articles
from db.models.article_content import ArticleContent
from services.save_article import save_article
from services.webdriver_factory import create_driver


def scrapper(word: str, input_start_date: str, input_end_date: str):
    driver, wait = create_driver()
    driver.get('https://www.polityka.pl')

    try:
        cookies_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div/div[2]/button[4]")))
        cookies_btn.click()

        search_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "li.cg_nav_search_icon > div.nav-link")))
        search_btn.click()

        search_input = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input.form-control[name='phrase']")
        ))
        search_input.clear()

        search_input.send_keys(word)

        submit_search_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit'].btn-outline-secondary")))
        submit_search_btn.click()

        results = driver.find_elements(
            By.CSS_SELECTOR, "li.cg_search_result_item")

        articles = []

        start_date = date = datetime.strptime(input_start_date, "%d.%m.%Y")
        end_date = date = datetime.strptime(input_end_date, "%d.%m.%Y")
        id = 0

        for item in results:
            try:
                date_element = item.find_element(By.CSS_SELECTOR, ".cg_date")
                date_text = date_element.text.strip()
                date = datetime.strptime(date_text, "%d.%m.%Y")
                print(date)

                if not (start_date <= date <= end_date):
                    continue

                title_element = item.find_element(By.CSS_SELECTOR, "h3")
                author_element = item.find_element(
                    By.CSS_SELECTOR, "div.cg_author")
                link_element = item.find_element(By.CSS_SELECTOR, "a")

                title = title_element.text.strip()
                author = author_element.text.strip()
                link = link_element.get_attribute("href")

                articles.append({
                    "id": id,
                    "title": title,
                    "author": author,
                    "link": link,
                    "date": date
                })

                id += 1
            except Exception as e:
                print(e)

        BASE_DIR = Path(__file__).resolve().parents[1]
        PDF_PATH = BASE_DIR / "pdfs"

        PDF_PATH.mkdir(exist_ok=True)

        print(articles)

        save_articles = []

        for article in articles:
            try:
                driver.get(article.get('link'))

                main_text_element = driver.find_element(
                    By.CSS_SELECTOR, "div.cg_article_content")

                paragraphs = main_text_element.find_elements(
                    By.CSS_SELECTOR, "p")

                paragraphs_text = ""
                for paragraph in paragraphs:
                    paragraphs_text += paragraph.text.strip() + '\n'
                file_path = f"{article.get('id')}_{article.get('title')}_{article.get('author')}.pdf"

                pdf_file_path = PDF_PATH / file_path

                pdf_path = str(pdf_file_path.relative_to(BASE_DIR))

                db_article_data = save_article(
                    article, paragraphs_text, pdf_path)

                if not db_article_data.get("exist_status"):
                    print(
                        "Article isn`t exist in database, adding to db and creating pdfs...")

                    with open(pdf_file_path, "wb") as file:
                        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
                            "printBackground": True,
                            "paperWidth": 8.27,
                            "paperHeight": 11.69,
                        })
                        file.write(base64.b64decode(pdf["data"]))

                save_articles.append(db_article_data.get("article"))

            except Exception as e:
                print(e)

        return save_articles
    finally:
        driver.quit()
