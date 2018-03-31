from bs4 import BeautifulSoup as bs
import requests

# 指定request的header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

res = requests.get(
    'https://ro.fws.tw/db/endless/tower/50', headers=headers
)


def mini_dict():
    # 指定BeautifulSoup解析文件與格式
    soup = bs(res.text, 'html.parser')
    minis = soup.find_all(
        'a', {'class': 'monster_mini', 'data-toggle': 'tooltip'}
    )
    mini_dict = {}
    # if webside without information, the boss number will be 0
    mini_dict['0'] = 'No info.'
    # get all boss name that match the boss name
    for mini in minis:
        mini_dict[mini.get('data-mid')] = mini.get('title')

    return mini_dict


if __name__ == '__main__':
    print(mini_dict())
