import selenium
from selenium import webdriver
import requests
import time
import configparser
import zipfile
import io

# download chromedriver
try:
	request = requests.get("https://chromedriver.storage.googleapis.com/73.0.3683.20/chromedriver_win32.zip")
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
chrome_options.add_argument("--disable-notifications --mute-audio --log-level=3 --silent --disable-gpu --allow-insecure-localhost")
if config["headless"] == "true":
	chrome_options.add_argument("--headless")
driver = selenium.webdriver.Chrome("cache/chromedriver.exe", options=chrome_options)
driver.implicitly_wait(0)

# login
driver.get("https://www.instagram.com/")
driver.find_element_by_link_text("Log in").click()
time.sleep(3)
driver.find_element_by_name("username").send_keys(config["username"])
driver.find_element_by_name("password").send_keys(config["password"])
time.sleep(1)
driver.find_element_by_xpath("//button[contains(.//div, \"Log in\")]").click()

# scoll pages and heart posts until many current pages contain no more hearts
curheight = 0
totalhearts = 0
nohearts = 0
windowHeight = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight")
while nohearts <= 20:
	driver.execute_script("window.scrollTo(0, arguments[0]);", curheight)
	curheight += windowHeight
	time.sleep(3)

	hearts = driver.find_elements_by_class_name("coreSpriteHeartOpen")

	clicked = False

	for a in range(len(hearts)):
		if hearts[a].is_displayed():
			#only if the child element has aria-label "Like"
			unlikeChilds = hearts[a].find_elements_by_css_selector("span[aria-label=\"Unlike\"]")
			if len(unlikeChilds) > 0:
				continue

			# scroll element into the middle of page
			driver.execute_script("window.scrollBy(0, arguments[0]);", driver.execute_script("return arguments[0].getBoundingClientRect().top;", hearts[a]) - windowHeight / 2)

			hearts[a].click()
			time.sleep(1)
			totalhearts += 1
			print(str(totalhearts) + " hearts")
			clicked = True

	if clicked:
		nohearts = 0
	else:
		nohearts += 1

# clean up
driver.get("https://www.instagram.com/") # to give window time to close
driver.close()