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

import time

degree = []
degree_type = []

# Set up Selenium
driver = webdriver.Firefox()
# url3 = "https://www.mq.edu.au/search#courses"
url = "https://www.mq.edu.au/search?Study+level=All+levels&Study+type=Course&profile=domestic#courses"
# url2 = "https://www.mq.edu.au/search?Study+level=All+levels&Study+type=Course&Area+of+Study=Information+technologies&profile=domestic#courses"
driver.get(url)
# Cookie
wait1 = WebDriverWait(driver, 10)
element1 = wait1.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//button[contains(@class, 'sc-dkrFOg') and contains(@class, 'hPRBUw')]",
        )
    )
)
element1.click()
time.sleep(1)

time_amount = 0.3
while True:
    time.sleep(time_amount)
    driver.get(url)
    ## Get the data
    html = driver.page_source
    # Replace 'html' with your HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Find all <a> elements with data="title"
    title_elements = soup.find_all("a", attrs={"data": "title"})

    # Extract the titles from the <a> elements
    titles = [element.text.strip() for element in title_elements]

    # Print the titles
    for title in titles:
        degree.append(title)
        print(title)

    # Find all <div> elements with class "flex order-md--1 margin--16"
    divs = soup.find_all("div", class_="flex order-md--1 margin--16")

    # Iterate over the found divs
    for div in divs:
        # Find the first <div> element inside the current div
        inner_div = div.find("div")

        # Extract the text content of the inner <div>
        course = inner_div.text

        # Print the extracted text
        degree_type.append(course)
        print(course)
    ## Scroll
    time.sleep(time_amount)
    last_element = driver.find_element(By.CSS_SELECTOR, ".story-list > div:last-child")

    # Scroll the page to bring the last element into view
    last_element.location_once_scrolled_into_view

    # Find the next button element using XPath
    next_button = driver.find_element(
        By.XPATH,
        "//li[@class='pagination__arrow']/button/i[contains(@class, 'ico--f-chevron-r-s')]",
    )
    time.sleep(time_amount)
    # Click the next button
    if "is-disabled" in next_button.get_attribute("class"):
        break
    next_button.click()

## EXPORT
# Create a DataFrame from the lists
df = pd.DataFrame({"Column 1": degree, "Column 2": degree_type})

# Export the DataFrame to an Excel file
df.to_excel("single.xlsx", index=False)

print("Data exported successfully.")
