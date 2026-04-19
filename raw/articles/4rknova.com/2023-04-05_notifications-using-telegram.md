---
title: Notifications Using Telegram
url: https://www.4rknova.com/blog/2023/04/05/telegram-notifications
author: Nikolaos Papadopoulos
published: '2023-04-05'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

In this short blog post, I experiment with using a Telegram bot to send arbitrary notifications as chat messages. There are many instances where this can be very useful. The process is fairly trivial, and it only takes a few minutes to set everything up.

# Creating a Telegram bot

First we need to create a telegram bot. In telegram, start a new chat with @BotFather. This special account is a bot itself and facilitates the creation and management of other bots.

![01](../../assets/b5f1ef851874b9a9.png)


Issue the */newbot* command and follow the prompts in the chat.

![02](../../assets/f23bc20af8f2906a.png)


Once the bot is created, a token is issued. This token can be used to access Telegram’s HTTP API. Take a note of it as it will soon become useful.

# Getting the Chat ID

Next we need to find our chat ID. This is easy to do when using Telegram’s web interface. Visit [https://web.telegram.org](https://web.telegram.org/) and login. Once the interface is loaded, navigate to your contacts view via the main menu.

![03](../../assets/20bd04e0425689dd.png)


Find your name and click on it. Then, observe the url in the browser’s address bar. It will be similar to: *https://web.telegram.org/z/#0123456789*. The number at the end of that url is the chat ID.

# Sending notifications

Following the steps described above, all the required information is obtained. Notifications can be sent using curl, with a simple POST request to Telegram’s API.

The following bash script demonstrates how that works.

```
#!/bin/bash
BOT_TOKEN="<replace-with-your-token>"
CHAT_ID="<replace-with-your-chat-id>"
MESSAGE="$@"
curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text="$MESSAGE"
```


# Example

Notifications can be issued by running the above script and passing a message as its input.

$ ./telegram_notify "hello world"

On the client side, a message should be received in a private chat with the bot account. This is what that will look like in Telegram’s Android application.

![04](../../assets/e1d0c346b2ef5788.png)