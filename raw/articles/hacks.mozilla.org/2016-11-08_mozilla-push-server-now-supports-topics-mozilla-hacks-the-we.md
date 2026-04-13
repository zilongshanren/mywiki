---
title: Mozilla Push Server now supports topics – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/11/mozilla-push-server-now-supports-topics/
author: JR Conlin
published: '2016-11-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In Firefox 44, Mozilla added Web Push capability to the browser. This gives websites the ability to notify users when something important needs to be communicated. For example, you may have a web app that wants to notify users when they receive a WebRTC call, or when a new discussion is initiated in a group chat. Or with a message service, you may want to notify users when they have new messages available.

Dan Callahan covered the details of [adding WebPush to your Web Apps](https://hacks.mozilla.org/2016/01/web-push-arrives-in-firefox-44/) in an article on Hacks early this year. You can also get more [documentation on the Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) from MDN or take a look at the ServiceWorker Cookbook for examples of how to use Web Push as well as many other service worker scenarios.

While Web Push has many benefits, it does come with some drawbacks. For example, if you notify an offline user of unread messages, when they come back to the browser later, the user may be inundated with many notifications at once.

![notifications-notopic](../../assets/5cbe24c1dff5a8c5.gif)


This can be mitigated a bit on certain operating systems, but a better way is now available. The Mozilla Push Service now offers the capability to provide *topics* for notification messages. This means that any user agent subscribed to the application will only be provided with the last message in a topic when it returns from an offline state. The Push Service replaces all previous push messages with the same topic and only displays the most recent one. In the example referenced above, all the unread messages are grouped into one topic, and when an offline user opens the browser they only get one message from the topic, which is the last one received.

![notifications-bytopic](../../assets/d2ce7313af285497.gif)


As this is a change to the [WebPush specification](https://webpush-wg.github.io/webpush-protocol/#rfc.section.5.4), to get this to work you will need to modify the server code that actually pushes the messages to the Push Service. Essentially, you must add a header named “Topic” to the push message. Take a look at [my test example for topics](https://github.com/jrconlin/topics) on github for a simple example. You can see how the header is added in the pusher/main.py file with the following code:

```
pywebpush.WebPusher(sub_info).send(
args.msg,
headers={"topic": topic},
ttl=args.ttl,
)
```


If you are using Marco Castelluccio’s NodeJS [web-push library](https://github.com/marco-c/web-push), you can add the header in the following way:

```
webPush.sendNotification(req.body.endpoint, {
TTL: req.body.ttl,
payload: req.body.payload,
userPublicKey: req.body.key,
userAuth: req.body.authSecret,
headers: {
topic: topic
}
})
```


## About JR Conlin

Web Push server developer who would like to thank you to subscribing to Cat Facts.