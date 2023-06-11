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

not_found = []
all_tasks = []
all_date = []

df = pd.read_excel("course_name.xlsx")
unique_courses = df.drop_duplicates(subset="Course Code")
course_codes = unique_courses["Course Code"]
# course_codes = ["COMP1000"]
course_names = unique_courses["Course Name"]
firefox_option = Options()
firefox_option.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_option)
for course_code, course_name in zip(course_codes, course_names):
    url = f"https://unitguides.mq.edu.au/units/archive_search?query={course_code}&year=2023"
    driver.get(url)
    html = driver.page_source
    # Parse the HTML content using BeautifulSoup
    # Assuming you have the HTML content in the 'html' variable
    soup = BeautifulSoup(html, "html.parser")

    # Find the <div> element with the class "alert alert-info"
    div_element = soup.find("div", class_="alert alert-info")

    # Check if the specific message is present in the HTML
    if div_element and "No results found" in div_element.get_text():
        # Update the URL or take any other desired action
        url = f"https://unitguides.mq.edu.au/units/archive_search?query={course_code}&year="
        driver.get(url)
        time.sleep(0.3)
        html = driver.page_source
        # Parse the HTML content using BeautifulSoup
        # Assuming you have the HTML content in the 'html' variable
        soup = BeautifulSoup(html, "html.parser")

        # Find the <div> element with the class "alert alert-info"
        div_element = soup.find("div", class_="alert alert-info")
        if div_element and "No results found" in div_element.get_text():
            not_found.append(course_code)
            all_tasks.append("")
            all_date.append("")
            continue

    try:
        # Find the div_offerings element by class name
        div_offerings = driver.find_element("css selector", ".table-search-results")

        try:
            print("Course Code:", course_code)
            print("Course Name:", course_name)
            # Find the first <a> tag within div_offerings
            a_tag = div_offerings.find_element("tag name", "a")

            # Click on the <a> tag
            a_tag.click()

            # Continue with the rest of your scraping logic or actions after the click
            # Find all <div> elements with class "general-info-value"

            # Extract the text within each <div> element
            html = driver.page_source
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            div_elements = soup.find("header", class_="unit-guide-header-container")
            h3 = div_elements.find("h3")
            print(h3.text.strip())
            all_date.append(h3.text.strip())

            div_elements = soup.find_all("tr", class_="assessment-task-row")
            task = []
            for div in div_elements:
                td_title = div.find("td", class_="title")
                td_weighting = div.find("td", class_="weighting")

                if td_title:
                    # Do something with the td_title
                    task.append(
                        f"{td_title.text.strip()} - {td_weighting.text.strip()}"
                    )
            print(task)
            all_tasks.append(task)

            print(len(all_date))
            print(len(all_tasks))
            print("------------------------------------")

        except NoSuchElementException:
            print("No <a> tag found within div_offerings")

    except NoSuchElementException:
        not_found.append(course_code)
        print("div_offerings element not found")


## EXPORT TO EXCEL

data = {
    "Course Code": course_codes,
    "Course Name": course_names,
    "Tasks": all_tasks,
    "Date": all_date,
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
df.to_excel("unitguide_task.xlsx", index=False)
