import selenium
from selenium import webdriver
import time
import configparser
import io
import traceback
import zipfile
import requests
import getpass
import getopt
import sys


def run():
    CHROMEDRIVER_DIR = ".cache/"

    # parse configuration
    config = configparser.ConfigParser()
    config.read("config.ini")
    config = config["default"]

    # get username and password from command line or prompt
    username = None
    password = None
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "", ["username=", "password="])
        for opt in opts:
            if opt[0] == "--username":
                username = opt[1]
            if opt[0] == "--password":
                password = opt[1]
    except:
        traceback.print_exc()
    if username is None:
        username = input("Instagram username: ")
    if password is None:
        password = getpass.getpass("Instagram password: ")

    # download chromedriver
    chromedriver_file = CHROMEDRIVER_DIR + "chromedriver.exe"
    try:
        request = requests.get(config["chromedriver"])
        archive = zipfile.ZipFile(io.BytesIO(request.content))

        # extract first file from the archive
        file = archive.namelist()[0]
        chromedriver_file = archive.extract(file, CHROMEDRIVER_DIR)
        archive.close()
        print("Downloaded and extracted chromedriver to", chromedriver_file + ".")
    except:
        traceback.print_exc()
        print("Exception while extracting chromedriver. Using default location of",
              chromedriver_file + ".")

    # setup driver
    USER_DATA_DIR = ".cache/chrome-user-data/"
    chrome_options = selenium.webdriver.chrome.options.Options()
    chrome_options.add_argument("--user-data-dir=" + USER_DATA_DIR)
    chrome_options.add_argument("--no-sandbox")
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
        chromedriver_file, options=chrome_options)
    driver.implicitly_wait(0)

    try:
        # login
        driver.get("https://www.instagram.com/")
        time.sleep(5)

        try:
            driver.find_element_by_link_text("Log in").click()
            time.sleep(2)
            driver.find_element_by_name("username").send_keys(username)
            driver.find_element_by_name("password").send_keys(password)
            time.sleep(1)
            driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
            time.sleep(5)
        except:
            # if profile is being used, then we won't need to login
            print("Did not log in. Perhaps user is already logged in?")

        article = driver.find_element_by_css_selector("article")
        windowHeight = driver.execute_script(
            "return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight")
        likedAlready = 0
        while likedAlready < 5:
            driver.execute_script("window.scrollBy(0, arguments[0]);", driver.execute_script(
                "return (arguments[0].getBoundingClientRect().top + arguments[0].getBoundingClientRect().bottom) / 2;", article) - windowHeight / 2)
            time.sleep(1)
            likes = article.find_elements_by_css_selector(
                "span[aria-label=\"Like\"]")
            if len(likes) == 0 or "glyphsSpriteComment_like" in likes[0].get_attribute("class").split(" "):
                likedAlready += 1
                print(article, "was liked already")
            else:
                likedAlready = 0
                likes[0].click()
                print(article, "liked!")
            article = driver.execute_script(
                "return arguments[0].nextElementSibling;", article)

        # clean up
        # to give window time to close
        driver.get("https://www.instagram.com/")
    except:
        traceback.print_exc()
        print("Exception while handling instagram feed; closing driver...")
    finally:
        driver.close()


if __name__ == "__main__":
    run()
