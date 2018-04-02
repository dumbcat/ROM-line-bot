import gspread
from oauth2client.service_account import ServiceAccountCredentials


def gsheet():
    # 連接google sheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'python-455eb62bc054.json', scope)
    gc = gspread.authorize(credentials)
    # 連接試算表
    sh1 = gc.open_by_key('1QQOXE_WasDzkHnQ9aXvc--eXjRso7U77lCEM7Mug8Zc')
    # 連接試算表分頁
    worksheet = sh1.worksheet("imgur")
    # 取得第二列所有元素儲存為list
    values_list = worksheet.col_values(2)

    return values_list


if __name__ == '__main__':
    print(gsheet())
