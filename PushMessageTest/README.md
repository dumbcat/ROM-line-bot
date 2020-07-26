# Line Bot Push Message

Use Line message api push text message to specify user, gourp, or room.

## Require Packages

+ requests
+ configparser

## Structure

+ **config&#46;ini:** Setting message api channel access token and specify id of user, gourp, or room
+ **pushmessage&#46;py:** Push message by http POST method.

## Setp

1. Create config.ini and enter the following content:

<pre><code>
[BASE]
token = Bearer <i>&lt;channel access token></i>
id = <i>&lt;user, group, or room id></i>
</code></pre>

2. run `$ python pushmessage.py` and type your text message

## Reference

&#91;1] https://developers.line.biz/en/reference/messaging-api/#http-request-8