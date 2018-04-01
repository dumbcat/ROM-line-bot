from bs4 import BeautifulSoup as bs
import requests

# 指定request的header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

# 從https://ro.fws.tw取得恩德勒斯塔50樓以上網頁資訊
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
    # 如果網站沒有該樓層資料，Boss編號會為0
    mini_dict['0'] = 'No info.'
    # 取得所有Boss編號與Boss名稱配對，儲存為字典
    for mini in minis:
        mini_dict[mini.get('data-mid')] = mini.get('title')

    return mini_dict


if __name__ == '__main__':
    print(mini_dict())
