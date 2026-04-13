---
title: Debugging Web Push in Mozilla Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/05/debugging-web-push-in-mozilla-firefox/
author: JR Conlin
published: '2017-05-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Introduction

*This article is part of an ongoing series about using and working with Web Push and Mozilla’s Web Push service. This article is not meant to be a general guide, but instead offers suggestions and insight into best using the service. Some knowledge of Javascript, Python, or other technologies is presumed.*

One of the challenges with Web Push implementation issues is trying to figure out what went wrong. Web Push has a large number of “moving parts”, systems and components that need to work together in order for your message to be successfully sent and received. While this article can’t address all the reasons that a given Push message might fail, I will try to provide tools and guidance for the more common problems.

## Common Problems

### Error reporting

The largest problem we see is from sites that do not pay attention to the return codes we provide. A [previous post](https://blog.mozilla.org/services/2017/02/23/managing-push-subscriptions/) mentioned how you can manage subscriptions to reduce your cost of sending out messages that will never be delivered. It’s also important to pay attention to the error that is returned.

An error can return a body that looks like the following:

```
{
'errno': 102,
'message': 'Request did not validate invalid token',
'code': 404,
'more_info': 'http://autopush.readthedocs.io/en/latest/http.html#error-codes',
'error': 'Not Found'
}
```


The list of `errno`

values are available in [the Autopush documentation](http://autopush.readthedocs.io/en/latest/http.html#error-codes). (*Autopush* is the name of the open source server we run to handle receiving and forwarding push subscription updates.) The server tries to provide as much detail and help as possible, so if your messages aren’t getting through, the Autopush messages may help quite a bit.

### VAPID concerns

Another potential problem is confusion around [VAPID](https://blog.mozilla.org/services/2016/04/04/using-vapid-with-webpush). VAPID is a developing specification for subscription-providing sites to “self identify”. This means that if there’s a significant problem, the push server operator has a way to contact whomever is sending the problematic messages. If you are seeing a large number of “401” status code response messages, chances are you have a problem with your VAPID authentication.

VAPID also allows a site to create “[restricted subscriptions](https://tools.ietf.org/html/draft-ietf-webpush-vapid-02#section-4)“. These subscriptions are locked down so that only the party that has the VAPID key can send them. This can be a bit confusing.

Very simply, VAPID is a block of data cryptographically signed with a key that has two parts: a Private key that you never share and is used to sign the VAPID token, and a Public key that is safe to share and is used to create the restricted subscription. Generally, you have a VAPID key that lasts for quite some time. It’s not a good idea to have it last forever, but it can certainly last for a year or so. I’ll talk about the implications of that in a bit.

When your app [requests a push endpoint](https://developer.mozilla.org/en-US/docs/Web/API/PushManager/subscribe), you have the option of providing your VAPID Public key as the `applicationServerKey`

. This will create a new subscription endpoint that is locked to that key. In order to send a successful subscription request, you must sign the VAPID block using the corresponding Private key, and include the Public key with your request. (How you include the public key [changed](https://tools.ietf.org/rfcdiff?url2=draft-ietf-webpush-vapid-02.txt) between Draft 01 and [Draft 02](https://tools.ietf.org/html/draft-ietf-webpush-vapid-02). You probably want to find [a library](https://github.com/web-push-libs/) that does the signing. You’ll also want to consult the documentation for the push service you choose to see which forms they accept. Most push platforms accept Draft 02.)

Note that the VAPID Public key is tied to the URL that you’ve requested. That means that you need to use that same key pair every time you want to send data to that URL. If you ever want to change the VAPID key, you’ll need to fetch a new endpoint and discard the old one. You decide how to do this, of course. Your app could simply fetch the new Public key from a known location, generate a new URL request and send the new registration information back to your server. This exercises much of the same code that you would want in place for a [ pushsubscriptionchange](https://developer.mozilla.org/en-US/docs/Web/Events/pushsubscriptionchange) event.

So, for VAPID 401 errors, you will want to check:

- Are you using the same key pair you used to acquire the restricted subscription?
- Have you properly signed your VAPID authorization key?
- Have you included all required VAPID headers with your request?

### Data encryption

Finally, there’s the actual message encryption. This can be the trickiest to debug because the push server has no way of knowing if the encryption is correct when it accepts a message for delivery. In addition, a message is only delivered by the User Agent (UA) if the UA can successfully decrypt it. This prevents your app from waking up to false messages, which can drain battery life.

Again, the best way to solve these sorts of problems is to use [a library](https://github.com/web-push-libs/). This isn’t always possible, and you may have a situation where you need to “hand roll” your own. There is [a page](https://mozilla-services.github.io/WebPushDataTestPage/) that can help walk you through the process of encrypting your data, however it currently only works on Firefox.

Be advised that there are several changes in the specs that may not be supported yet. As of publication date, most push implementations will accept ECE Draft 03 “aesgcm” encoding. There is [a proposal](https://github.com/w3c/push-api/commit/813f9af75d59e3fa1522db9aeeaa2bd158ff10bf) that the User Agent report back the forms of cryptography it supports, but this has not been formally accepted yet. Unfortunately, this is one of the issues with using a technology that’s still in development. If you wish to follow the changes that are being proposed, you should follow the working groups.

Unfortunately, many encryption errors are not detected by the Push Service. This is because the Push Service cannot decrypt your message. Fortunately, it is possible to “peek inside” the client to see if there might be an error.

## Debugging the Desktop

Use the [Browser Console](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) to help debug the desktop. Note, this is different than the “Web Console” that appears as part of the [developer tools panel](https://developer.mozilla.org/en-US/docs/Tools). The Browser Console displays much higher level messages that may not be visible to the page or the web console.

The benefit is that you will be able to see messages that your service worker may log, as well as other push messages. For instance, if you look at a testing page that we use, you might see something similar in your browser:


Near the bottom of that window, you’ll notice four messages from “sw.js”. The first three are `console.info()`

messages stating that a new message has arrived, what the content of the new message is, and the associated clients. Note that the fourth message is a `console.error()`

saying `"Service worker couldn't send message: Error: No valid client to send to."`

This can happen when a service worker loses its claimed association with the parent. In short: the good news is that the message came in fine, the bad news is it had nowhere to go.

Another useful tool to consider is the *service worker debugging* page at `about:debugging#workers`

. This page shows all the registered service worker scripts and allows you to unregister them, optionally send push events, and debug the service worker scripts. Mozilla Hacks has more [details about the about:debugging page](https://hacks.mozilla.org/2016/03/debugging-service-workers-and-push-with-firefox-devtools/).

### Debugging Android

Debugging push on Android is somewhat similar. Much like the desktop, you will want to set `dom.push.debug`

to `true`

and `dom.push.loglevel`

to `debug`

. Unfortunately, unlike the desktop, there is no easy way to view the browser console from Android. Messages are logged to the android error log, so it’s possible to use a command like `<a href="https://developer.android.com/studio/command-line/adb.html">adb</a> logcat`

to tail the error log. Some developers may be able to use `grep`

to look for only records containing `"Gecko(Push|Console)"`

.

Sadly, this view isn’t quite as pretty, but does show much the same, including console messages from service workers which may help identify and resolve bugs. It is worth noting that adb may truncate very long messages.

A sample adb log might look like:

```
04-24 15:18:04.432 7015 7037 I GeckoPushGCM: Cached GCM token exists: crWSbvAk4e4:APA91bHozW8bSTCrBwPerd7...
04-24 15:18:04.432 7015 7037 D GeckoPushManager: Existing uaid is fresh; no need to request from autopush endpoint.
04-24 15:18:04.488 7015 7037 I GeckoPushManager: Got chid: c0ef2... and endpoint: https://updates.push.services...
04-24 15:18:04.500 7015 7038 I GeckoPush: console.debug: PushServiceAndroidGCM:
04-24 15:18:04.520 7015 7038 I GeckoConsole: put() [object Object]
04-24 15:18:04.521 7015 7038 I Gecko : put()
04-24 15:18:04.522 7015 7038 I Gecko : Object
04-24 15:18:04.522 7015 7038 I Gecko : - pushEndpoint = https://updates.push.services.mozilla.com/wpush/v1/...
04-24 15:18:04.522 7015 7038 I Gecko : - scope = https://jrconlin.github.io/Webpush_QA/
...
04-24 15:18:04.526 7015 7038 I Gecko : console.debug: PushDB:
04-24 15:18:04.528 7015 7038 I GeckoConsole: put: Request successful. Updated record c0ef2...
04-24 15:18:04.528 7015 7038 I Gecko : put: Request successful. Updated record
04-24 15:18:04.528 7015 7038 I Gecko : c0ef2...
04-24 15:18:04.563 7015 7038 I GeckoConsole: receiverKey BNPFRn...
04-24 15:18:04.565 7015 7038 I GeckoConsole: Auth key: 0Gkt8...
04-24 15:18:04.567 7015 7038 I GeckoConsole: data: Amidst the mists and coldest frosts, I thrust my fists against ...
...
04-24 15:18:04.650 7015 7038 I GeckoConsole: echo -ne "\xa\xc6\xfb\xd3\x13\x0e\xa\xa\xa\xad\x59\xad\x71\xa\xa\...
04-24 15:18:04.652 7015 7038 I GeckoConsole: payload 191,40,74,54,29,62,188,190,133,70,86,70,120,194,173,100,62,...
04-24 15:18:04.653 7015 7038 I GeckoConsole: Fetching: https://updates.push.services.mozilla.com/wpush/v1/gAAAAA...
04-24 15:18:04.960 7015 7038 I GeckoConsole: Message sent 201
04-24 15:18:05.753 7015 9696 D GeckoPushGCM: Message received. Processing on background thread.
04-24 15:18:05.754 7015 7037 I GeckoPushService: Google Play Services GCM message received; delivering.
...
04-24 15:18:05.774 7015 7038 I Gecko : console.debug: PushService:
04-24 15:18:05.774 7015 7037 I GeckoPushService: Delivering dom/push message to Gecko!
04-24 15:18:05.777 7015 7038 I GeckoPush: console.debug: PushServiceAndroidGCM:
04-24 15:18:05.781 7015 7038 I GeckoPush: ReceivedPushMessage with data
04-24 15:18:05.782 7015 7038 I GeckoPush: Object
04-24 15:18:05.782 7015 7038 I GeckoPush: - channelID = c0ef2...
04-24 15:18:05.782 7015 7038 I GeckoPush: - con = aesgcm
...
04-24 15:18:05.783 7015 7038 I GeckoPush: console.debug: PushServiceAndroidGCM:
04-24 15:18:05.784 7015 7038 I GeckoConsole: Delivering message to main PushService: [object ArrayBuffer] ...
...
04-24 15:18:05.786 7015 7038 I Gecko : console.debug: PushService:
04-24 15:18:05.787 7015 7038 I GeckoConsole: receivedPushMessage()
04-24 15:18:05.787 7015 7038 I Gecko : receivedPushMessage()
04-24 15:18:05.788 7015 7038 I Gecko : console.debug: PushDB:
04-24 15:18:05.789 7015 7038 I GeckoConsole: getByKeyID()
04-24 15:18:05.789 7015 7038 I Gecko : getByKeyID()
04-24 15:18:05.795 7015 7038 I Gecko : console.debug: PushDB:
04-24 15:18:05.797 7015 7038 I GeckoConsole: getByKeyID: Got record [object Object]
04-24 15:18:05.810 7015 7038 I Gecko : console.debug: PushDB:
04-24 15:18:05.811 7015 7038 I GeckoConsole: update: Update successful c0ef2...
...
04-24 15:18:05.840 7015 7038 I Gecko : console.debug: PushService:
04-24 15:18:05.841 7015 7038 I GeckoConsole: notifyApp() https://jrconlin.github.io/Webpush_QA/
04-24 15:18:05.841 7015 7038 I Gecko : notifyApp()
04-24 15:18:05.841 7015 7038 I Gecko : https://jrconlin.github.io/Webpush_QA/
04-24 15:18:05.848 7015 7038 I GeckoConsole: **** Recv'd a push message:: {"isTrusted":true}
04-24 15:18:05.850 7015 7038 I GeckoConsole: Service worker just got: Amidst the mists and coldest frosts, I ...
04-24 15:18:05.853 7015 7038 I GeckoConsole: Service worker found clients {}
04-24 15:18:05.854 7015 7038 I GeckoConsole: Service worker sending to client... [object WindowClient]
04-24 15:18:05.857 7015 7038 I GeckoConsole: Service Worker sent: {"type":"content","content":"Amidst the mists ...
04-24 15:18:08.033 527 32517 E ResourceManagerService: Rejected removeResource call with invalid pid.
04-24 15:18:05.865 7015 7015 D GeckoToolbar: onTabChanged: LOCATION_CHANGE
```


Note that you get a bit more information here, including messages indicating that GCM received the message and relayed it to Gecko. Many log messages have been removed or trimmed for space for publication, but these can help isolate if the problem is in your app vs. in the network.

## Conclusion

Working with Push is rewarding, but remember that it is a new technology. This means that things can change, and there may be rough bits to watch out for. As always, we appreciate bugs when you find them and suggestions on how to make things easier. You can find us on [irc.mozilla.org](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Getting_Started_with_IRC) in the #push channel if you have questions.

## About JR Conlin

Web Push server developer who would like to thank you to subscribing to Cat Facts.

## 5 comments

Martin GrayMay 4th, 2017 at 09:27JR ConlinMay 4th, 2017 at 09:32AlfonsoMay 9th, 2017 at 11:26Havi Hoffman [Editor]May 9th, 2017 at 13:47jr conlinMay 9th, 2017 at 13:50