from bs4 import BeautifulSoup
import re
import sys
import httpx
import asyncio

PHONE_NUMBER_PATTERN = "((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))"
URL_PATTERN = "((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\"]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
IMAGE_FORMAT_LIST = ['.tif', '.tiff', '.jpg', '.jpeg', '.gif', '.png', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2']
MIN_NUMBER_LENGHT = 10


async def get_async(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)


async def make_request(websites_list):
    response_list = await asyncio.gather(*map(get_async, websites_list))
    return response_list


def main():
    websites_list = []
    website_info = []

    for website in sys.stdin:
        if '' == website.rstrip():
            break
        websites_list.append(website.strip())
    
    websites_content = asyncio.run(make_request(websites_list))

    for site_content in websites_content:
        if site_content.status_code  != 200:
            sys.stderr.write(str({'Error code': site_content.status_code})) 
            continue
        parsed_site = BeautifulSoup(site_content, 'html.parser').prettify()
    
        match_url_list = [url[0] for url in re.findall(URL_PATTERN, parsed_site)]
        all_number_found = re.findall(PHONE_NUMBER_PATTERN, parsed_site)

        image_url_list = set([url for url in match_url_list if any(extension in url for extension in IMAGE_FORMAT_LIST)])

        match_phone = set(filter(lambda x: len(x) >= MIN_NUMBER_LENGHT, all_number_found))
            
        website_info.append({ 'logo': image_url_list, 'phone': match_phone, 'website': str(site_content.url) })
        sys.stdout.write(str(website_info))


if __name__ == "__main__":
    main()