from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import requests


# Google Locators.
GOOGLE_I_AGREE = (By.CSS_SELECTOR, '#L2AGLb')
GOOGLE_SEARCH_BAR = (By.NAME, 'q')
GOOGLE_SEARCH_BUTTON = (By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
GOOGLE_UNSPLASH_LINK = (By.XPATH, '//a[@href="https://unsplash.com/"]')

# Unsplash Locators.
UNSPLASH_SEARCH_BAR = (By.XPATH, '//input[@type="search"]')
UNSPLASH_SEARCH_BUTTON = (By.XPATH, '//button[@title="Search Unsplash"]')
UNSPLASH_IMAGES = "//img[@class='YVj9w']"

# Initilizing the webdriver.
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-extensions")
# options.add_argument("--headless")
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)

# Setting explicit waits.
wait10 = WebDriverWait(driver, 10)
wait5 = WebDriverWait(driver, 5)

# Accessing google search page.
driver.get("https://www.google.com/")

# Google navigation.
try:
    wait10.until(ec.element_to_be_clickable(GOOGLE_I_AGREE)).click()
except NoSuchElementException:
    print("Cookies agreement pop up didn't show")
wait10.until(ec.presence_of_element_located(GOOGLE_SEARCH_BAR)).send_keys('unsplash')
wait5.until(ec.element_to_be_clickable(GOOGLE_SEARCH_BUTTON)).click()
wait10.until(ec.element_to_be_clickable(GOOGLE_UNSPLASH_LINK)).click()

# Unsplash navigation.
wait10.until(ec.presence_of_element_located(UNSPLASH_SEARCH_BAR)).send_keys('abstract art')
wait5.until(ec.element_to_be_clickable(UNSPLASH_SEARCH_BUTTON)).click()
wait10.until(ec.presence_of_all_elements_located((By.XPATH, UNSPLASH_IMAGES)))
links = driver.find_elements(By.XPATH, UNSPLASH_IMAGES)

# Creating a .txt file to hold the filtered image URLs.
with open('ImageFilteredURLs.txt', 'w+') as f:
    for link in links:
        img_url = link.get_attribute('src')
        img_url = img_url.partition('?')[0]
        f.write(f'{img_url}\n')

# Reading from the created file to create a list of the image URLs.
with open('ImageFilteredURLs.txt', 'r+') as f:
    img_urls = [line.strip('\n') for line in f]

# Set the start time.
t1 = perf_counter()

# The function that downloads the images
def download_img(img_url: str):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[3] + '.jpg'

    # An if statement to avoid downloading the ad photo (starts with "file" not "photo")
    if img_name[:5] == 'photo':
        with open(f'Pictures\Downloaded\{img_name}', 'wb') as image:
            image.write(img_bytes)
            print(f'"{img_name}" is now downloaded!')

# Using threading to download the pictures more efficiently.
with ThreadPoolExecutor() as executor:
    executor.map(download_img, img_urls)

# Set the end time.
t2 = perf_counter()

# Printing the elapsed time.
elapsed_time = round(t2 - t1, 2)
print(f'Images took {elapsed_time} sec(s) to finish downloading')

# Tearing down the webdriver.
driver.quit()