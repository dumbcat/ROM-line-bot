import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

res = requests.get(
    'https://ro.fws.tw/db/endless/tower/50', headers=headers
)


def mini_dict():
    """Get all boss numbers and boss names of endless tower.

    Returns:
        dictionary: Dictionary with all boss numbers as key and boss names as value
    """
    # Search HTML <a> tag which match the class and data-toggle attributes.
    soup = bs(res.text, 'html.parser')
    minis = soup.find_all(
        'a', {'class': 'monster_mini', 'data-toggle': 'tooltip'}
    )
    mini_dict = {}
    # Define the key value when bs_rom.py without boss info.
    mini_dict['0'] = 'No info.'

    # Generate dictionary with boss numbers and nemes.
    for mini in minis:
        mini_dict[mini.get('data-mid')] = mini.get('title')

    return mini_dict


if __name__ == '__main__':
    print(mini_dict())
