# utils.py

import tomli



def get_scraping_dog_api_key() -> str:
    r"""
    Get the Scraping Dog API key stored in a local secrets.toml file.

    Returns
    -------
    api_key : str
        The Scraping Dog API key obtained in the 
        [member area](https://api.scrapingdog.com/login).
    """

    with open('./secrets.toml', 'rb') as read_file:
        secrets = tomli.load(read_file)

    return secrets['api']['key1']



def filter_dict_fields(d : dict, key : list[str]) -> dict:
    r"""
    Filter a dictionary to only certain fields/keys.
    """
    return {k : d[k] for k in key}
