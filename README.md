# Technical assignment for Cial dun&amp;bradStreet

## How to launch application
Check if *docker* is installed in your pc, otherwise follow the official tutorial:

For **windows**: https://docs.docker.com/desktop/install/windows-install/

For **linux**: https://docs.docker.com/desktop/install/linux-install/

- Now, assuming docker is installed, run:

`docker build -t my_image --rm .`

*Just wait for the installation of the dependencies and env setup*

- Finally, run:

`docker run -it --name my_app --rm my_image`

and insert the website(s) valid URL


## How it works
The algorithm in main.py can be separated into 3 main parts:
- Input reading
    - The cli application running inside a docker image receives the websites URL list by the bash and pass to make_request() method, that will create a async requests routine using asyncio and httpx lib, and finally pass the list of the requests response to websites_handler() method.
- Website handler method
    - Basically receives the response list, get the content of the websites, parse using the BeautifulSoup lib and returns a lxml object contains the whole site. After that, with the parsed site, the app uses a regular expression pattern to find all occurrences of image URLs in each site, and do the same with the international phone numbers. All phone numbers in the found list are passed to a formatter method, following the criteria and returning formatted numbers.
- Output writing 
    - The app uses the handler output to print, a formatted object using standard output in console.
