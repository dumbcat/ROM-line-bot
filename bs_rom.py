import requests
from bs4 import BeautifulSoup as bs

from bs_mini_dict import mini_dict

mini_dict = mini_dict()


def rom_boss(name):
    """Compare boss name entered by user with this week's endless tower table.

    Args:
        name (string): The boss name entered by user.

    Returns:
        list: Comparison result.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }

    res = requests.get(
        'https://ro.fws.tw/db/endless/tower/50', headers=headers
    )

    soup = bs(res.text, 'html.parser')
    # Each <tr> is the endless tower information of a server.
    trs = soup.find_all('tr')
    return_list = list()

    for i in range(0, len(trs)):
        if i > 0:
            floor_dict = {}
            td = trs[i].find_all('td')
            server_id = td[0].get('data-sort')
            items = td[1].find_all('a', {'class': 'monster_mini mf'})
            # Use data-sort attribute of HTML <td> tag as server id
            floor_dict['server'] = server_id

            # Generate dictionary with floor as key and list of boss numbers 
            # as value.
            for item in items:
                if item.get('data-lv') in floor_dict:
                    floor_dict[item.get('data-lv')].append(
                        mini_dict[item.get('data-mid')]
                    )
                else:
                    floor_dict[item.get('data-lv')
                               ] = [mini_dict[item.get('data-mid')]]

            # Compare user input with floor dictionary. If the boss name
            # entered by user show twice in one floor, append return_str into
            # return_list.
            for key in floor_dict:
                if floor_dict[key].count(name) > 1:
                    return_str = '分流「%s」的 %s 樓有 %s ' % (
                        floor_dict['server'], key, ','.join(floor_dict[key]))
                    if len(return_list) != 0:
                        return_list.append(return_str)
                    else:
                        return_list = [return_str]

    # Append return_str to return_list if the boss name entered by user 
    # without show twice in any server.
    if len(return_list) == 0:
        return_str = '沒有任何分流同一樓層有兩隻 %s' % (name)
        return_list = [return_str]

    return_list.append('Endless Tower資料由 https://ro.fws.tw/ 提供')
    return return_list


if __name__ == '__main__':
    name = input("Please enter monster name: ")
    print(rom_boss(name))
