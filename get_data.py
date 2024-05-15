# get_linkedin_jobs_data.py

import time 

import random
import pandas as pd

import utils
import scrape



def get_linkedin_jobs_data(
        api_key : str, 
        field : str = 'data scientist', 
        geoid : str = '102095887', 
        page : int = 1, 
        sort_by : str = None,
        verbose : bool = False
    ) -> pd.DataFrame:
    r"""
    Get the latest LinkedIn jobs for a specified job position.

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
    jobs_df : pd.DataFrame
        The DataFrame of LinkedIn job postings.
    """

    # Get Scraping Dog LiknedIn jobs data
    jobs_data = scrape.sd_fetch_jobs_from_page(
        api_key=api_key,
        field=field,
        geoid=geoid,
        page=page,
        sort_by=sort_by,
        verbose=verbose
    )

    # For each url, use BeautifulSoup to scrape additional data
    for index, job_dict in enumerate(jobs_data.copy()):

        # randomly wait some number of seconds before the next request
        # to avoid HTTP error 429
        sleep = random.randint(5,15)
        if verbose:
            print(f"Sleeping for {sleep} seconds")
        time.sleep(sleep)

        url = job_dict['job_link']

        if verbose:
            print(f"#{index} Trying to scrape LinkedIn job url: {url}")

        jobs_json = scrape.bs_scrape_linkedin_job_url(url, verbose=verbose)

        if len(jobs_json) != 0 and 'description' in jobs_json:
            jobs_json = utils.filter_dict_fields(jobs_json, key=['description'])
            merged_job_data = {**job_dict, **jobs_json}
            jobs_data[index] = merged_job_data

    jobs_df = pd.json_normalize(jobs_data)

    return jobs_df



if __name__ == '__main__':
    import os
    from datetime import datetime
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--field', help='the job search query')
    parser.add_argument('--sort_by', default=None, help='the optional parameter to sort jobs based on their posting date')
    args = parser.parse_args()

    if args.sort_by not in ['day', 'week', 'month', None]:
        raise ValueError("Argument --sort_by only accepts {'day', 'week', 'month'} as values")

    SCRAPING_DOG_API_KEY = utils.get_scraping_dog_api_key()

    jobs_df = get_linkedin_jobs_data(
        api_key=SCRAPING_DOG_API_KEY, 
        field=args.field, 
        sort_by=args.sort_by, 
        verbose=True
    )

    os.makedirs('data', exist_ok=True)
    timestamp = datetime.now().strftime(r'%Y%m%d_%H%M%S')
    field = '_'.join([w for w in args.field.split()])
    jobs_df.to_csv('data/{}_{}_linkedin_jobs.csv'.format(timestamp, field), index=False, lineterminator='\n')
