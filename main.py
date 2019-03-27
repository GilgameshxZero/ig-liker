import selenium
from selenium import webdriver
import requests
import time
import configparser
import zipfile
import io

print("Running ig-liker...")

# download chromedriver
try:
    request = requests.get(
        "https://chromedriver.storage.googleapis.com/73.0.3683.20/chromedriver_win32.zip")
    file = zipfile.ZipFile(io.BytesIO(request.content))
    file.extractall("cache/")
    file.close()
except:
    pass

# parse configuration
config = configparser.ConfigParser()
config.read("config.ini")
config = config["default"]

# setup driver
chrome_options = selenium.webdriver.chrome.options.Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--silent")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-extensions")
if config["headless"] == "true":
    chrome_options.add_argument("--headless")
driver = selenium.webdriver.Chrome(
    "cache/chromedriver.exe", options=chrome_options)
driver.implicitly_wait(0)

# login
driver.get("https://www.instagram.com/")
driver.find_element_by_link_text("Log in").click()
time.sleep(3)
driver.find_element_by_name("username").send_keys(config["username"])
driver.find_element_by_name("password").send_keys(config["password"])
time.sleep(3)
# TODO: this sometimes fails...
driver.find_element_by_xpath("//button[@type=\"submit\"]").click()

# scoll pages and heart posts until many current pages contain no more hearts
windowHeight = driver.execute_script(
    "return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight")
while True:
    likes = driver.find_elements_by_css_selector(
        "span[aria-label=\"Like\"]")
    if len(likes) == 0:
        break

    for a in range(len(likes)):
        # not a comment
        if not "glyphsSpriteComment_like" in likes[a].get_attribute("class").split(" "):
            # scroll element into the middle of page
            driver.execute_script("window.scrollBy(0, arguments[0]);", driver.execute_script(
                "return arguments[0].getBoundingClientRect().top;", likes[a]) - windowHeight / 2)
            likes[a].click()
            time.sleep(1)

# clean up
driver.get("https://www.instagram.com/")  # to give window time to close
driver.close()
