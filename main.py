from bs4 import BeautifulSoup
import requests
import re

IMAGE_FORMAT_LIST = ['.tif', '.tiff', '.jpg', '.jpeg', '.gif', '.png', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2']
PHONE_NUMBER_PATTERN = r''
URL_PATTERN = r''

websites_content = []
websites_file = open('websites.txt', 'r')
websites_list = websites_file.readlines()
websites_list = [website.strip() for website in websites_list]

for website in websites_list:
    response = requests.get(website)
    parsed_site = BeautifulSoup(response.content, features='lxml').prettify()
    websites_content.append({ 'website': website, 'parsed_site': parsed_site })

match_phone = re.findall(PHONE_NUMBER_PATTERN, parsed_site)
all_urls = re.findall(URL_PATTERN, parsed_site)
