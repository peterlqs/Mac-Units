import pandas as pd
from selenium import webdriver
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import collections
from selenium.common.exceptions import TimeoutException
import pandas as pd
import requests
import time

reviews = []
stars = []
not_found = []

df = pd.read_excel("course_name.xlsx")
unique_courses = df.drop_duplicates(subset="Course Code")
course_codes = unique_courses["Course Code"]
course_names = unique_courses["Course Name"]
firefox_option = Options()
firefox_option.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_option)
for course_code, course_name in zip(course_codes, course_names):
    url = f"https://studentvip.com.au/macquarie/subjects/{course_code}"
    driver.get(url)
    time.sleep(0.3)
    html = driver.page_source
    # Parse the HTML content using BeautifulSoup
    # Assuming you have the HTML content in the 'html' variable
    soup = BeautifulSoup(html, "html.parser")
    div_element = soup.find("div", class_="page-header")
    div_element2 = soup.find("h2", class_="subject-rating no-rating")
    if (div_element and "Oh no" in div_element.get_text()) or (
        div_element2 and "rate me" in div_element2.get_text()
    ):
        not_found.append(course_code)
        reviews.append("")
        stars.append("")
        continue
    div_element = soup.find("div", class_="rating")
    stars_count = len(div_element.find_all(class_="fas fa-star"))
    stars.append(stars_count)
    print(stars_count)

    div_element = soup.find_all("div", class_="list-group")
    div_element = div_element[-1]
    elements = div_element.find_all(["p"])
    elements2 = div_element.find_all(["small"])
    review = []
    for i in range(len(elements)):
        review.append(f"{elements[i].get_text()} - {elements2[i].get_text()}")
    reviews.append(review)

    print("Number of reviews:", len(reviews))
    print("Number of stars:", len(stars))
    print("Number of course codes:", len(course_codes))
    print("Number of course names:", len(course_names))


# Create a dictionary with the data
data = {
    "reviews": reviews,
    "stars": stars,
    "course_codes": course_codes,
    "course_names": course_names,
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
df.to_excel("studentvip.xlsx", index=False)

print("Data exported to studentvip.xlsx successfully.")
