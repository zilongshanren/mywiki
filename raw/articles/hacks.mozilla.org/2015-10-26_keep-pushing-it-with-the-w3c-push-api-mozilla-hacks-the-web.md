---
title: Keep pushing it, with the W3C Push API – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/10/keep-pushing-it-with-the-w3c-push-api/
author: Chris Mills
published: '2015-10-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You are all familiar with this experience — a little bubble pops up on your phone without warning, containing a nagging message along the lines of *“your insipidly cute little monsters are rested, and want to go and fight more battles!”*, or *“You’ve got unanswered friend requests from people you don’t know. Hurry up and reply!”*

Push messages are definitely not a new concept, having been a popular feature of mobile platforms for years. It is only recently however that *Push* has come to the web platform. This article takes you through the basics, and outlines the current status of *Push*.

The advantage of Push over other technology choices for sending messages to users is that push messages can allow users to opt in to updates without any intervention from the client whatsoever — as long as the server has the endpoint (see below), it can send updates to a subscribed client only when required (i.e. it doesn’t require a constant connection like sockets, which is good for battery life, etc.)

Note: MDN includes [full reference docs for the Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) as well as a detailed tutorial, [Using the Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API/Using_the_Push_API).

## Browser support

The Push API is currently at Working Draft stage. (The [latest editor’s draft is here](https://w3c.github.io/push-api/).) Most of the API is supported in recent release versions of Chrome (42+), and Firefox (42+) in pre-release channels only for now (e.g. Nightly, Developer Edition, and Beta). The exception is [PushMessageData](https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData), which is currently supported only in Firefox 44+ (again not in release channels.)

Push requires [service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) to run, which are also mostly supported in the latest versions of Chrome and Firefox (although disabled by default in the latest Firefox release version.) Since service workers require `https`

to work for security purposes, Push also requires `https`

.

It is worth noting that Push is often used along with communication APIs like [Web Notifications](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API) and [Channel Messaging](https://developer.mozilla.org/en-US/docs/Web/API/Channel_Messaging_API) for communicating the results of Push messages being sent. These both have fairly widespread support across modern browsers.

## The process of push

In this section we will go through a typical process by which an app utilizing push messages could be set up.

Note: You can find a [demo showing the Push API in use](https://github.com/chrisdavidmills/push-api-demo) on Github. It will be useful for you to get this running so you can follow along as you read the sections below.

### Requesting permission

The first thing you should do is request permission for web notifications, or anything else you are using that requires permissions. For example:

`Notification.requestPermission();`


### Registering a service worker and subscribing to push

The next thing is to register a service worker to control the page, using `ServiceWorkerContainer.register()`

. This returns a promise that resolves with a `ServiceWorkerRegistration`

object:

```
navigator.serviceWorker.register('sw.js').then(function(reg) {
// do something with reg object
});
```


Once we have this registration object, we can start registering for Push. Often you will send the `ServiceWorkerRegistration`

object to some kind of subscription function.

At any point we can check that the service worker is active and ready to start doing things using the `ServiceWorkerContainer.ready`

property, which returns a promise that resolves with the aforementioned `ServiceWorkerRegistration`

object. Once we have this, we can access the `PushManager`

using the `ServiceWorkerRegistration.pushManager`

property. Then we can subscribe to the push service using `PushManager.subscribe()`

, which returns a promise that resolves with a `PushSubscription`

object.

```
navigator.serviceWorker.ready.then(function(reg) {
reg.pushManager.getSubscription()
.then(function(subscription) {
// do something with your PushSubscription object
});
}
```


To unsubscribe, the code is similar, but you must use the `PushSubscription.unsubscribe()`

method to unsubscribe from push:

```
navigator.serviceWorker.ready.then(function(reg) {
reg.pushManager.getSubscription()
.then(function(subscription) {
subscription.unsubscribe().then(function(successful) {
// unsubscribe was successful
})
});
}
```


### Push servers, and sending push messages

To send push messages, you need a server component. This can be written in any server-side language you like, as long as it can handle secure requests/responses and data encryption. (Push messages require `https`

, and data sent by push needs to be encrypted.)

Note: Support for `PushMessageData`

and encryption is currently Firefox-only, with the encryption process still being worked out. (Encryption and `getKey()`

don’t yet appear in the spec.)

Once we have our PushSubscription object, we need to grab two pieces of information that are used for sending push messages:

`PushSubscription.endpoint`

: This is a unique URL pointing at the push server that handles sending the push messages (each browser will have its own push server). For example:`https://updates.push.services.mozilla.com/push/gAAAAABWJ-VZaQ9DhwvjZJHEHlZCzNJBPTPAcucU9mprtyzisSow75qHbY5lrjglEXE7G6SIfWvz-QSwhBcjpRjx2PAnKCAHd-5XHh1RFXa1ngqq_2-I0-PZoEqigI7E3ISO5zE1tNy29_Iyiu06m0tc_2nfKyuEcjwDPLyOC8c3IvawhBUUzMM=`

. This is used by your server to send the push message — the request hits the push server, and the random string on the end makes sure the push message is sent to the service worker associated with that particular push subscription.`PushSubscription.getKey('p256dh')`

: This method generates a public client key, one of the components used to encrypt the data. These details should then be sent to the server so it can send push messages when required. (You could use[Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)or[XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest)to do this.)

On the server-side, you should store the endpoint and any other required details so they are available when a push message needs to be sent to a push subscriber (use a database or whatever you like). In a production app, make sure these details are hidden, so malicious parties can’t steal endpoints and spam subscribers with push messages. Anyone with the endpoint can send a push message, as long as the subscription stays alive.

To send a push message without data, you need to send it to the endpoint URL with a method of POST. To send it with data in Firefox, you need to encrypt it, which involves the client public key. This is a pretty complex procedure (read [Message Encryption for Web Push](https://tools.ietf.org/html/draft-ietf-webpush-encryption-01) for more details). As time goes on, libraries will be written to do this kind of thing for you; Marco Castelluccio’s NodeJS [web-push library](https://github.com/marco-c/web-push) is a good current option for NodeJS.

### The service worker, and responding to push messages

Over in your service worker, you need to set up an `onpush`

handler to respond to push messages being received.

```
self.addEventListener('push', function(event) {
var obj = event.data.json();
// do something with JSON
});
```


Note that the event object is of type [PushEvent](https://developer.mozilla.org/en-US/docs/Web/API/PushEvent); its data property contains a [PushMessageData](https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData) object, which contains the data sent over the push message. This object has methods available for returning the message payload as a blob, array buffer, JSON object, or plain text string (we are converting it to JSON above). Once you have the payload, you can do what you want with it.

#### Sending a channel message

If you want respond to the push event by sending a [channel message](https://developer.mozilla.org/en-US/docs/Web/API/Channel_Messaging_API) back to the main context, you first need to open a message channel between the main context and the service worker. In the main context, you can do something like this:

```
navigator.serviceWorker.ready.then(function(reg) {
var channel = new MessageChannel();
channel.port1.onmessage = function(e) {
handleChannelMessage(e.data);
}
mySW = reg.active;
mySW.postMessage('hello', [channel.port2]);
});
```


First we create a new [MessageChannel](https://developer.mozilla.org/en-US/docs/Web/API/MessageChannel) object using a constructor, then set up an onmessage handler to handle messages coming across the channel to the main context.

Then, as before, we get a reference to our [ServiceWorkerRegistration](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration) object. We then use its `active`

property to return a [ ServiceWorker](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorker) object. We can use the

`ServiceWorker`

object’s `postMessage()`

method to post a message to the service worker context, along with `port2`

of the message channel.Over in the service worker, we grab a reference to `port2`

using the following:

```
var port;
self.onmessage = function(e) {
port = e.ports[0];
}
```


Once this link is established, data can be sent back to the main context using:

```
port.postMessage('my message');
```


#### Firing a notification

If you want to respond by firing a system notification, you can do this using `ServiceWorkerRegistration.showNotification`

:

```
function fireNotification(obj, event) {
var title = 'Subscription change';
var body = obj.name + ' has ' + obj.action + 'd.';
var icon = 'push-icon.png';
var tag = 'push';
event.waitUntil(self.registration.showNotification(title, {
body: body,
icon: icon,
tag: tag
}));
}
```


Note that here we have run this inside an [ ExtendableEvent.waitUntil](https://developer.mozilla.org/en-US/docs/Web/API/ExtendableEvent/waitUntil) method — this extends the lifetime of the event until after the notification has been fired, so we can make sure everything has happened as we intended.

### Handling premature subscription expiration

Sometimes push subscriptions expire prematurely, without `unsubscribe()`

being called. This can happen when the server gets overloaded, or if you are offline for a long time. This is highly server-dependent, so the exact behavior is difficult to predict. In any case, you can handle this problem using the `onsubscriptionchange`

handler, which will be invoked only in this specific case.

```
self.addEventListener('subscriptionchange', function() {
// do something, usually resubscribe to push and
// send the new subscription details back to the
// server via XHR or Fetch
});
```


### Chrome support for Push

Chrome has good support for Push as well, but with a few differences from Firefox. For a start, it doesn’t yet support sending `PushMessageData`

in push messages; it also relies on the Google Cloud Messaging service. Read [Extra steps for Chrome support](https://developer.mozilla.org/en-US/docs/Web/API/Push_API/Using_the_Push_API#Extra_steps_for_Chrome_support) for full details.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 11 comments

PhistucKOctober 26th, 2015 at 14:09Chris MillsOctober 27th, 2015 at 01:38ChaoOctober 26th, 2015 at 15:36Chris MillsOctober 27th, 2015 at 01:39voracityOctober 26th, 2015 at 19:57PhistucKOctober 27th, 2015 at 01:31RafaelOctober 29th, 2015 at 12:47Tyf0xOctober 29th, 2015 at 22:59Chris MillsOctober 30th, 2015 at 05:51Chris MillsOctober 30th, 2015 at 06:27Tyf0xOctober 30th, 2015 at 07:14