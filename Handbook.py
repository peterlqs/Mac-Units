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

# Read the Excel file
df = pd.read_excel("course_data.xlsx")

# Remove duplicate course codes and get corresponding course names
unique_courses = df.drop_duplicates(subset="Course Code")
course_codes = unique_courses["Course Code"]
course_names = unique_courses["Course Name"]

all_course_code = []
all_course_name = []
period = []
error_list = []
firefox_option = Options()
firefox_option.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_option)
# Scrape the website for each course code
for course_code, course_name in zip(course_codes, course_names):
    url = f"https://coursehandbook.mq.edu.au/2023/units/{course_code}"
    driver.get(url)
    time.sleep(0.3)
    html = driver.page_source
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the div with the ID "Offerings"
    div_offerings = soup.find("div", id="Offerings")

    if div_offerings:
        # Find all div elements within the div_offerings element
        div_elements = div_offerings.find_all("div")
        print(len(div_elements))

        if len(div_elements) >= 2:
            # Get the second div element
            second_div = div_elements[3]
            sessions = second_div.get_text(strip=True).split("Session ")
            formatted_sessions = "\n".join(
                ["Session " + s for s in sessions if s.strip()]
            )
            print(formatted_sessions)
            period.append(formatted_sessions)
            all_course_code.append(course_code)
            all_course_name.append(course_name)

    # # Process the response as needed
    # # For example, you can print the course code, course name, and response status code
    print(f"Course Code: {course_code}")
    print(f"Course Name: {course_name}")
    print("------------------------------")

## EXPORT TO EXCEL FILE
# Assuming you have the following lists:
# Create a DataFrame with the data
data = {
    "Course Code": all_course_code,
    "Course Name": all_course_name,
    "Period": period,
}
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
filename = "course_name.xlsx"
sheet_name = "course_name"
df.to_excel(filename, sheet_name=sheet_name, index=False)
