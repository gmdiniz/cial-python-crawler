from bs4 import BeautifulSoup
import re
import sys
import httpx
import json
import asyncio

# Phone number regex pattern coverage: https://regexr.com/74l55
PHONE_NUMBER_PATTERN = "((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))"
# Url regex pattern coverage: https://regexr.com/74l5e
URL_PATTERN = "((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\"]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
IMAGE_FORMAT_LIST = ['.tif', '.tiff', '.jpg', '.jpeg', '.gif', '.png', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2']
MIN_NUMBER_LENGHT = 8
MAX_NUMBER_LENGHT = 11


async def get_async(url):
    try:
        async with httpx.AsyncClient() as client:
            return await client.get(url)
    except:
        sys.stderr.write('Request error') 
        return


async def make_request(websites_list):
    response_list = await asyncio.gather(*map(get_async, websites_list))
    return response_list


def validate_phone_number(number):
    only_digits_number_len = len(re.findall(r'\d+', number)[0])
    if only_digits_number_len >= MIN_NUMBER_LENGHT and only_digits_number_len <= MAX_NUMBER_LENGHT:
        return number


def main():
    websites_list = []
    website_info = []

    for website in sys.stdin:
        if '' == website.rstrip():
            break
        websites_list.append(website.strip())
    
    websites_content = asyncio.run(make_request(websites_list))

    for site_content in websites_content:
        if site_content.status_code != 200:
            sys.stderr.write('DeadPage\n') 
            continue
        parsed_site = BeautifulSoup(site_content, 'html.parser').prettify()
    
        match_url_list = [url[0] for url in re.findall(URL_PATTERN, parsed_site)]
        all_number_found = re.findall(PHONE_NUMBER_PATTERN, parsed_site)

        image_url_list = set([url for url in match_url_list if any(extension in url for extension in IMAGE_FORMAT_LIST)])

        match_phone = set(filter(lambda x: validate_phone_number(x), all_number_found))
            
        website_info.append({ 'logo': list(image_url_list), 'phone': list(match_phone), 'website': str(site_content.url) })
        sys.stdout.write(json.dumps(website_info)+ '\n')


if __name__ == '__main__':
    main()