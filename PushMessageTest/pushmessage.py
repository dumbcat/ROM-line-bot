import json
import requests
import configparser


def sender(token, id, message):
    """Use line message api to push message to line user, group, or chat room.

    Args:
        token (string): Channel access token of message api.
        id (string): Line ser, group, or chat room id.
        message (string): A message which wants to push.

    Returns:
        tuple: A tuple include response code and message.
    """
    url = 'https://api.line.me/v2/bot/message/push'
    header = {'Content-Type': 'application/json',
              'Authorization': token}
    data = json.dumps({
        "to": id,
        "messages": [
            {
                "type": "text",
                "text": message
            }]
    })

    r = requests.post(url, headers=header, data=data)

    if r.status_code == 200:
        return r.status_code, 'Send Message Success'
    else:
        error_message = r.text.split(':', 1)[1].strip('}').strip('"')
        return r.status_code, error_message


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    channel_access_token = config.get('BASE', 'token')
    uesr_id = config.get('BASE', 'id')

    message = input('Please input message to send: ')
    code, message = sender(channel_access_token, uesr_id, message)
    print(f'Response Code: {code}')
    print(f'Response Message: {message}')
