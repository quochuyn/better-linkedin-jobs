# get_linkedin_jobs_data.py

import tomli
import requests



def get_scraping_dog_api_key() -> str:
    r"""
    Returns
    -------
    api_key : str
        The Scraping Dog API key obtained in the 
        [member area](https://api.scrapingdog.com/dashboard/65cdb16ffac36d5508c81b26).
    """

    with open('./secrets.toml', 'rb') as read_file:
        secrets = tomli.load(read_file)

    return secrets['api']['key1']




def fetch_jobs_from_page(
        api_key : str, 
        field : str = 'data scientist', 
        geoid : str = '102095887', 
        page : int = 1, 
        sort_by : str = None
    ) -> list[dict]:
    r"""
    Parameters
    ----------
    api_key : str
        The Scraping Dog API key obtained in the 
        [member area](https://api.scrapingdog.com/dashboard/65cdb16ffac36d5508c81b26).
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
        return data
    else:
        print("Request for page", page, "failed with status code:", response.status_code)
        return None



def get_linkedin_jobs_data():
    pass


