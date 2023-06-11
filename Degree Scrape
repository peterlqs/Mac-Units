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


# Read data from Excel file
df = pd.read_excel("degree_type.xlsx")
# df = pd.DataFrame({"Column 1": ["Master of Data Science", "Bachelor of Business"]})
# Create a new column with modified titles
df["Modified Title"] = df["Column 1"].str.replace(" ", "-").str.lower()

firefox_option = Options()
firefox_option.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_option)

# Click cancel button
cancel = True

not_found = []
all_degree = collections.defaultdict(lambda: collections.defaultdict(dict))

# Loop through the DataFrame rows
for index, row in df.iterrows():
    # Get the modified title and construct the URL
    modified_title = row["Modified Title"]
    print("Modified title: ", modified_title)
    # Construct the URL with the modified title
    url = f"https://www.mq.edu.au/study/find-a-course/courses/2024/{modified_title}#course-structure"
    print("URL: ", url)

    # Open the webpage
    driver.get(url)

    if cancel:
        time.sleep(1)
        # Find the button element
        button = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div[2]/aside[2]/div/div/button"
        )
        button.location_once_scrolled_into_view
        time.sleep(2)
        # Click the button
        button.click()
        cancel = False

    # Edge case: 2024
    # Search for the "Page Not Found" heading
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    page_not_found_heading = soup.find("h1", text="Page Not Found")
    if page_not_found_heading:
        try:
            if page_not_found_heading:
                url = f"https://www.mq.edu.au/study/find-a-course/courses/{modified_title}#course-structure"
                # Open the alternative URL
                driver.get(url)
                time.sleep(0.4)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                wait = WebDriverWait(driver, 1)  # Maximum wait time of 10 seconds
                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "tbody.padded.table--expandable")
                    )
                )

        except TimeoutException:
            not_found.append(row["Column 1"])
            continue
    try:
        wait = WebDriverWait(driver, 1)  # Maximum wait time of 10 seconds
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "tbody.padded.table--expandable")
            )
        )

    except TimeoutException:
        # Check if the heading is found
        not_found.append(row["Column 1"])
        continue

    print("Not found: ", not_found)

    ## SCRAPE
    # all_degree["Bachelor of Business"]
    # Find all <div> elements with class "flex order-md--1 margin--16"
    time.sleep(0.1)
    divs = soup.find_all("div", class_="table--structure-subhead")

    course_type = []
    # Iterate over the found divs
    for div in divs:
        # Find the first <div> element inside the current div
        inner_div = div.find("h5")

        # Extract the text content of the inner <div>
        course = inner_div.text

        # Print the extracted text
        course_type.append(course)
    print("Course type: ", course_type)
    time.sleep(0.1)
    # Find all <div> elements with class "flex order-md--1 margin--16"
    divs = soup.find_all("tbody", class_="padded table--expandable")
    count = 0
    for div in divs:
        if len(course_type) == 0:
            not_found.append(row["Column 1"])
            break
        inner_divs = div.find_all(["p", "a"])
        courses = []
        for p in inner_divs:
            # Extract the text content of the inner <div>
            course = p.text
            # if "flexible zone" in course.lower():
            #     break
            print(course)
            courses.append(course)
        # if count >= len(course_type):
        #     not_found.append(row["Column 1"])
        #     break
        # print("row: ", row["Column 1"])
        # print("div: ", divs)
        # print(soup)
        all_degree[row["Column 1"]][course_type[count]] = (
            list(all_degree[row["Column 1"]][course_type[count]]) + courses
        )
        count += 1
        if count >= len(course_type):
            break
    print("-------------------")

## EXPORT TO EXCEL
data = []
for degree, categories in all_degree.items():
    for category, courses in categories.items():
        data.extend(
            [(degree, category, *courses[i : i + 2]) for i in range(0, len(courses), 2)]
        )

df = pd.DataFrame(data, columns=["Degree", "Category", "Course Code", "Course Name"])

# Export the DataFrame to an Excel file
df.to_excel("course_data4.xlsx", index=False)
