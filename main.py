import sys
import getopt
import getpass
import requests
import zipfile
import traceback
import io
import time
from selenium import webdriver
import selenium
import pathlib
import platform
import os
import stat


def main(argv):
    """
    Default behavior for the auto-liker when it is run from the command line.
    Automatically likes posts from Instagram feed.

    argv: List of command line arguments (sys.argv[1:])
    """
    # use the correct chromedriver for your chrome version!
    CHROMEDRIVER_URL_BASE = "https://chromedriver.storage.googleapis.com/79.0.3945.36"
    CHROMEDRIVER_URL_EXTENSION = {
        "Linux": "/chromedriver_linux64.zip",
        "Darwin": "/chromedriver_mac64.zip",
        "Windows": "/chromedriver_win32.zip"
    }
    CHROMEDRIVER_URL = CHROMEDRIVER_URL_BASE + CHROMEDRIVER_URL_EXTENSION[platform.system()]

    # parse command line arguments
    try:
        opts, args = getopt.getopt(
            argv, "", ["username=", "password=", "stop-condition=", "period=", "headless"])
        opts = {opt[0]: opt[1] for opt in opts}
    except:
        print("Error parsing command-line arguments. Continuing...")
        opts = {}

    # get username and password
    username = opts["--username"] if "--username" in opts.keys() else \
        input("Instagram username: ")
    password = opts["--password"] if "--password" in opts.keys() else \
        getpass.getpass("Instagram password: ")

    # download chromedriver
    CACHE_DIR = ".cache/"

    try:
        request = requests.get(CHROMEDRIVER_URL)
        archive = zipfile.ZipFile(io.BytesIO(request.content))

        # extract first file from the archive
        file = archive.namelist()[0]
        chromedriver_file = archive.extract(file, CACHE_DIR)
        archive.close()

        # mark executable
        os.chmod(chromedriver_file, os.stat(chromedriver_file).st_mode | 0o111)

        print("Downloaded and extracted chromedriver to", chromedriver_file + ".")
    except:
        traceback.print_exc()
        chromedriver_file = CACHE_DIR + "chromedriver.exe"
        print("Exception while extracting chromedriver. Using default location of",
              chromedriver_file + ".")

    # parse stop-condition
    stop_condition = int(opts["--stop-condition"]) \
        if "--stop-condition" in opts.keys() else 5  # defualt value

    # parse period
    period = int(opts["--period"]) if "--period" in opts.keys() else None

    # run the script forever! unless period is not set, which we check at the end
    while True:
        print("Starting auto-liker...")

        # setup driver
        try:
            USER_DATA_DIR = CACHE_DIR + "chrome-user-data/"
            chrome_options = selenium.webdriver.chrome.options.Options()
            chrome_options.add_argument("--user-data-dir=" + USER_DATA_DIR)
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--allow-insecure-localhost")
            chrome_options.add_argument("--disable-extensions")
            if "--headless" in opts.keys():
                chrome_options.add_argument("--headless")

                # fix! must be set to some unused port
                chrome_options.add_argument("--remote-debugging-port=9222")
            driver = selenium.webdriver.Chrome(
                chromedriver_file, options=chrome_options)
            driver.implicitly_wait(0)
            print("Launched driver.")
        except:
            traceback.print_exc()
            print("Failed to launch driver.")
            return

        # like posts!
        SCREENSHOT_DIR = CACHE_DIR + "screenshots/"
        pathlib.Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)

        try:
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.save_screenshot(SCREENSHOT_DIR + "instagram.png")

            # login
            try:
                driver.find_element_by_link_text("Log in").click()
                time.sleep(5)
                driver.save_screenshot(SCREENSHOT_DIR + "login.png")
                driver.find_element_by_name("username").send_keys(username)
                driver.find_element_by_name("password").send_keys(password)
                time.sleep(3)
                driver.find_element_by_xpath(
                    "//button[@type=\"submit\"]").click()
                time.sleep(5)
                print("Logged in.")
            except:
                # if profile is being used, then we won't need to login
                print("Did not log in (perhaps we are already logged in?).")

            driver.save_screenshot(SCREENSHOT_DIR + "feed.png")
            article = driver.find_element_by_css_selector("article")
            windowHeight = driver.execute_script(
                "return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight")
            consecutive_skipped = 0
            while consecutive_skipped < stop_condition:
                driver.execute_script("window.scrollBy(0, arguments[0]);", driver.execute_script(
                    "return (arguments[0].getBoundingClientRect().top + arguments[0].getBoundingClientRect().bottom) / 2;", article) - windowHeight / 2)
                time.sleep(3)
                likes = article.find_elements_by_css_selector(
                    "span[aria-label=\"Like\"]")

                if len(likes) == 0 or "glyphsSpriteComment_like" in likes[0].get_attribute("class").split(" "):
                    consecutive_skipped += 1
                    print("Skipped post (" + str(consecutive_skipped),
                          "skipped in a row).")
                else:
                    consecutive_skipped = 0
                    likes[0].click()
                    print("Liked a post.")

                article = driver.execute_script(
                    "return arguments[0].nextElementSibling;", article)

            # give window time to send all relevant likes to backend
            time.sleep(3)
        except:
            traceback.print_exc()
        finally:
            try:
                driver.close()
                print("Closed driver.")
            except:
                print("Failed to close driver. Finishing...")

        # sleep for period if set! otherwise exit
        if period is None:
            break
        else:
            print("Waiting", period, "seconds...")
            try:
                time.sleep(period)
            except:
                break


if __name__ == "__main__":
    main(sys.argv[1:])
