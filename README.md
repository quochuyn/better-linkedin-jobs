# LinkedIn Jobs API 

The goal of this project is to get the latest LinkedIn jobs for a specified job position to avoid promoted job listings. We start with an API call to Scraping Dog to obtain a basic dataset with metadata on the position, link, company, and posting date. Afterwards, we use BeautifulSoup, a Python web scraping package, to scrape the provided url link to obtain key data missing such as the description.

# Getting Started

Clone the repository to a local directory:
```
git clone https://github.com/quochuyn/linkedin_api_demo
```

Change directory into the repository
```
cd linkedin_api_demo
```

## Credentials

The key feature of this program uses the web-scraping Scraping Dog's API to access LinkedIn job postings. Using a web-scraping API is easy to use (no CATPCHAS, etc.), bypasses proxy limits, and avoids any legal trouble. However, we are limited by API rates and the current functionality of the API. Official documentation can be found with this [link](https://docs.scrapingdog.com/linkedin-jobs-scraper). The Scraping Dog API key can be obtained in the [member area](https://api.scrapingdog.com/dashboard/65cdb16ffac36d5508c81b26).

## Plugging in Credentials

You will need to create a `secrets.toml` file with the below code or try your hand with the `linkedin_jobs_api_demo.ipynb` notebook and simply insert your own API key.

```
# secrets.toml
# 

# scraping dog API
[api]
key1 = "your_key"
```

## Running the Script

You can simply call the below command into your shell prompt and the script will create a `data` folder with corresponding csv files. If you'd like more control, then feel free to use the `linkedin_jobs_api_demo.ipynb` notebook.

`python get_data.py --field "data scientist" --sort_by day`
