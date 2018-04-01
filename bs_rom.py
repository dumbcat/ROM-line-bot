from bs4 import BeautifulSoup as bs
import requests
from bs_mini_dict import mini_dict
# from urllib.request import urlopen
# import os

# Get monster number mapping
mini_dict = mini_dict()


def rom_boss(name):
    # 指定request的header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/60.0.3112.101 Safari/537.36'
    }

    res = requests.get(
        'https://ro.fws.tw/db/endless/tower/50', headers=headers)
    # 指定BeautifulSoup解析文件與格式
    soup = bs(res.text, 'html.parser')
    trs = soup.find_all('tr')
    return_list = list()
    # 每個分流為一個row，迭代每個row取得資料
    for i in range(0, len(trs)):
        if i > 0:
            # 儲存該樓層資訊的空字典
            floor_dict = {}
            td = trs[i].find_all('td')
            server_id = td[0].get('data-sort')
            items = td[1].find_all('a', {'class': 'monster_mini mf'})
            # 紀錄分流編號
            floor_dict['server'] = server_id
            # 將每個樓層的層數與該層的Boss名稱儲存為字典鍵值對
            for item in items:
                if item.get('data-lv') in floor_dict:
                    floor_dict[
                        item.get('data-lv')].append(
                            mini_dict[item.get('data-mid')])

                else:
                    floor_dict[item.get('data-lv')
                               ] = [mini_dict[item.get('data-mid')]]
            # 比對使用者輸入與樓層字典
            # 如果使用者輸入的Boss名稱在一個樓層出現過兩次，就把資訊字串加入return_list中
            for key in floor_dict:
                if floor_dict[key].count(name) > 1:
                    return_str = '分流「%s」的 %s 樓有 %s ' % (
                        floor_dict['server'], key, ','.join(floor_dict[key]))
                    # print(return_str)
                    if len(return_list) != 0:
                        return_list.append(return_str)
                    else:
                        return_list = [return_str]
    # 如果所有樓層中，該Boss於同一層都沒有出現過兩次
    if len(return_list) == 0:
        return_str = '沒有任何分流同一樓層有兩隻 %s' % (name)
        return_list = [return_str]
    return_list.append('Endless Tower資料由https://ro.fws.tw/提供')
    return return_list


if __name__ == '__main__':
    name = input("Please enter monster name: ")
    print(rom_boss(name))
