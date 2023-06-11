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
all_links = []
all_pre = []
all_copre = []
all_cobadged = []
all_des = []
all_final = []
all_presentation = []

df = pd.read_excel("course_name.xlsx")
unique_courses = df.drop_duplicates(subset="Course Code")
course_codes = unique_courses["Course Code"]
course_names = unique_courses["Course Name"]
firefox_option = Options()
firefox_option.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_option)
for course_code, course_name in zip(course_codes, course_names):
    url = f"https://unitguides.mq.edu.au/units/archive_search?query={course_code}&year=2023"
    driver.get(url)
    time.sleep(0.3)
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
            all_links.append("")
            all_pre.append("")
            all_copre.append("")
            all_cobadged.append("")
            all_des.append("")
            all_final.append("No Idea")
            all_presentation.append("No Idea")
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
            div_elements = soup.find_all("div", class_="general-info-value")
            words = [div.get_text(strip=True) for div in div_elements]
            print("Words:", len(words))

            # Print the extracted words
            current_url = driver.current_url

            # Print the current page URL
            print("Current URL:", current_url)
            all_links.append(current_url)
            all_pre.append(words[1])
            all_copre.append(words[2])
            all_cobadged.append(words[3])
            all_des.append(words[4])

            section = soup.find("section", id="assessment-tasks-section")

            # Extract the text within the <h3> element
            text = section.get_text()
            if "final exam" in text.lower():
                all_final.append("Possibly")
            else:
                all_final.append("No")

            if (
                "presentation" in text.lower()
                or "presentations" in text.lower()
                or "team" in text.lower()
            ):
                all_presentation.append("Possibly")
            else:
                all_presentation.append("No")
            print("-----------------------------------")

        except NoSuchElementException:
            print("No <a> tag found within div_offerings")

    except NoSuchElementException:
        not_found.append(course_code)
        print("div_offerings element not found")
    print(not_found)
    not_found_length = len(not_found)
    all_links_length = len(all_links)
    all_pre_length = len(all_pre)
    all_copre_length = len(all_copre)
    all_cobadged_length = len(all_cobadged)
    all_des_length = len(all_des)
    all_final_length = len(all_final)
    all_presentation_length = len(all_presentation)

    print("all_links length:", all_links_length)
    print("all_pre length:", all_pre_length)
    print("all_copre length:", all_copre_length)
    print("all_cobadged length:", all_cobadged_length)
    print("all_des length:", all_des_length)
    print("all_final length:", all_final_length)
    print("all_presentation length:", all_presentation_length)

## EXPORT TO EXCEL

data = {
    "Course Code": course_codes,
    "Course Name": course_names,
    "Links": all_links,
    "Prerequisites": all_pre,
    "Corequisites": all_copre,
    "Co-badged Units": all_cobadged,
    "Description": all_des,
    "all_final": all_final,
    "all_presentation": all_presentation,
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
df.to_excel("unitguide.xlsx", index=False)
