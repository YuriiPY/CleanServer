import os
import base64

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

wait = WebDriverWait(driver=driver, timeout=10)

driver.get('https://www.polityka.pl')


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


input_data = input("Enter search data:")
search_input.send_keys(input_data)

submit_search_btn = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button[type='submit'].btn-outline-secondary")))
submit_search_btn.click()


results = driver.find_elements(By.CSS_SELECTOR, "li.cg_search_result_item")

articles = []

start_date = date = datetime.strptime("01.10.2025", "%d.%m.%Y")
end_date = date = datetime.strptime("31.10.2025", "%d.%m.%Y")
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
        author_element = item.find_element(By.CSS_SELECTOR, "div.cg_author")
        link_element = item.find_element(By.CSS_SELECTOR, "a")

        title = title_element.text.strip()
        author = author_element.text.strip()
        link = link_element.get_attribute("href")

        articles.append({
            "id": id,
            "title": title,
            "author": author,
            "link": link
        })

        id += 1
    except Exception as e:
        print(e)


print(tabulate(articles, headers="keys", tablefmt="fancy_grid"))

os.makedirs("texts", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)

for article in articles:
    try:
        driver.get(article.get('link'))

        main_text_element = driver.find_element(
            By.CSS_SELECTOR, "div.cg_article_content")

        paragraphs = main_text_element.find_elements(By.CSS_SELECTOR, "p")

        text_file_path = os.path.join("texts", f"{article.get('id')}.txt")
        with open(text_file_path, "w", encoding="utf-8") as file:
            for paragraph in paragraphs:
                file.write(paragraph.text.strip() + '\n')
                print(paragraph.text.strip(),
                      end='\n ___________________________________ \n')

        pdf_file_path = os.path.join("pdfs", f"{article.get('id')}.pdf")
        with open(pdf_file_path, "wb") as file:
            pdf = driver.execute_cdp_cmd("Page.printToPDF", {
                "printBackground": True,  # include background graphics
                "paperWidth": 8.27,       # A4 size in inches
                "paperHeight": 11.69,
            })
            file.write(base64.b64decode(pdf["data"]))

    except Exception as e:
        print(e)

driver.quit()
