# Line Bot for Ragnarok Mobile Game

+ **Main Features**

  + According to user input, return the imsage message of the specified ruins picture.

  + According to user input, return the test message of the specified endless tower boss information.

  + Guild war alert schedule.

+ **Test Features**

  + Print group id or user id in the console.

  + Broadcast message to all groups in group list.

## Require Packages

+ flask
+ line-bot-sdk
+ schedule
+ beautifulsoup4
+ requestss

## Structure

+ **PushMessageTest:** Use Line message api push text message to specify users, gourps, or rooms.

+ **app&#46;py:** Use flask application to link line bot sdk

+ **bs_mini_dict&#46;py:** Form game site crawl and parser all boss names and numbers. Then return a dictionary with number as key name as value.

+ **bs_rom&#46;py:** Form game site crawl and parser specify boss location information. Then return a list with all location of the boss.

+ **config&#46;ini:** Configure message api channel access token, channel secret, and id list of groups.

+ **Procfile:** Specifies the commands that are executed by the Heroku app on startup.

## Attention

You need to create config.ini and enter the following content.

<pre><code>[BASE]
channel_access_token = <i>&lt;channel access token></i>
channel_secret = <i>&lt;channel secret></i>
group_list = <i>&lt;group 1 id>, &lt;group 2 id></i>
</code></pre>

And follow the tutorial to deploy the program to your application server.

## Reference

&#91;1] https://developers.line.biz/en/docs/messaging-api/getting-started/

&#91;2] https://github.com/line/line-bot-sdk-python

&#91;3] https://github.com/yaoandy107/line-bot-tutorial