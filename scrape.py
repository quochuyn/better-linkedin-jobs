# scrape.py

import ssl
import certifi
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlopen

import json
from json.decoder import JSONDecodeError



def sd_fetch_jobs_from_page(
        api_key : str, 
        field : str = 'data scientist', 
        geoid : str = '102095887', 
        page : int = 1, 
        sort_by : str = None,
        verbose : bool = False
    ) -> list[dict]:
    r"""
    Fetch LinkedIn jobs from the Scraping Dog API.

    Parameters
    ----------
    api_key : str
        The Scraping Dog API key obtained in the 
        [member area](https://api.scrapingdog.com/login).
    field : str, default='data scientist'
        The search query which can either be a job title or the name 
        of a company.
    geoid : str, default='102095887'
        The unique location ID issued by LinkedIn itself which can be 
        found on the LinkedIn jobs URL.
    page : str, default=1
        The page number of the LinkedIn jobs page. The output will 
        not exceed 25 jobs.
    sort_by : {`day`, `week`, `month`}, optional
        An optional parameter to sort jobs based on their posting 
        date. Possible values include `day` for jobs within 24 hours,
        `week` for jobs within 7 days, and `month` for jobs within 30 days.
    verbose : bool, default=False
        Boolean value whether to display messages.

    Returns
    -------
    data : list[dict]
        The list of LinkedIn job postings.
    """

    # Define the URL and parameters
    url = "https://api.scrapingdog.com/linkedinjobs/"
    params = {
        "api_key": api_key,
        "field": field,
        "geoid": geoid,
        "page": str(page)
    }

    if sort_by is not None:
        params['sort_by'] = sort_by

    # Send a GET request with the parameters
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Access the response content
        data = response.json()
        if verbose:
            print("Successful call to Scraping Dog API")
            print(f"Returning {len(data)} job listings")
        return data
    else:
        print(f"Request for page {page} failed with status code: {response.status_code}")
        return None
    


def bs_scrape_linkedin_job_url(url : str, verbose : bool = False):
    r"""
    Scrape a LinkedIn Job URL using BeautifulSoup.

    Parameters
    ----------
    url : str
        The LinkedIn job URL to scrape from.
    verbose : bool, default=False
        Boolean value whether to display messages.

    Returns
    -------
    job_json : dict
        The dictionary from a JSON decoded string.
    """

    job_json = None

    # Credits to this StackOverflow post to bypass SSL certificate vertification:
    # https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    try:
        page = urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    except HTTPError as error:
        # TODO: create a log file
        if verbose:
            print(error)
        return {}
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('script')

    if len(tags) == 0:
        # TODO: create a log file
        if verbose:
            print(f"No tags were found for url: {url}")
        return {}
    else:
        for tag in tags:
            try:
                job_json = json.loads(tag.string)
                if verbose:
                    print(f"Succesfully scraped the url")
                return job_json
            except JSONDecodeError:
                # pass silently and try next tag
                pass
        
        # No tags returned desired JSON output
        # TODO: create a log file
        if verbose:
            print(f"No tags returned desired JSON output for url: {url}")
        return {}
    