import time
import os
import sys
import pathlib
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options

FILENAME_ZFILL = 8
URL_MIN_LEN = 10
LOAD_PAGE_TIMEOUT = 600
EXTRA_SLEEP = 8

url_list_file = os.environ['URL_LIST_FILE']

#if len(sys.argv) < 2:
if not url_list_file:
	print("no url list file")
	sys.exit(1)

targeturls = []
with open(url_list_file) as infile:#//note this technique does not load whole file. it loads line by line
	for line in infile:
		lineleft = line.strip()
		if len(lineleft) >= URL_MIN_LEN and urlparse(lineleft).scheme:
			targeturls.append(lineleft)


if not len(targeturls):
	print("no targeturls found")
	sys.exit(1)

file_write_dir = os.environ['FILE_WRITE_DIR']

if not file_write_dir:
	print("no file_write_dir")
	sys.exit(1)

wait_css_selector = os.environ['WAIT_CSS_SELECTOR']

if not wait_css_selector:
	print("no wait condition")
	sys.exit(1)

options = Options()
options.headless = True
with webdriver.Firefox(options=options) as driver:
	wait = WebDriverWait(driver, LOAD_PAGE_TIMEOUT)#timeout in seconds
	for idx, targ_url in enumerate(targeturls):
		#if idx:
		#	driver.url = targ_url
		#	driver.navigate()#//?python has no navigate? only get? //https://stackoverflow.com/questions/65246011/webdriver-object-has-no-attribute-navigate
		#else:
		driver.get(targ_url)
		print('driver.get finished')
		first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, wait_css_selector)))
		print('element presence found')
		time.sleep(EXTRA_SLEEP)
		#note page_source (PageSource) might not be what you want. Because >If the page has been modified after loading (for example, by JavaScript) there is no guarantee that the returned text is that of the modified page. Please consult the documentation of the particular driver being used to determine whether the returned text reflects the current state of the page or the text last sent by the web server. The page source returned is a representation of the underlying DOM: do not expect it to be formatted or escaped in the same way as the response sent from the web server.
		str_to_write = '<!DOCTYPE html>'+driver.execute_script("return document.documentElement.outerHTML")
		pathlib.Path(os.path.join(file_write_dir, str(idx).zfill(FILENAME_ZFILL)+'.htm')).write_text(str_to_write)
