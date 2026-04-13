---
title: Don't miss out on the real-time fun! Use Firefox OS Push Notifications – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/dont-miss-out-on-the-real-time-fun-use-firefox-os-push-notifications/
author: Nikhil Marathe
published: '2013-07-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox OS v1.1 introduces Push Notifications to Open Web Apps, allowing web developers to take advantage of real-time updates without implementing difficult polling logic themselves. Native Push Notifications support means

that only one connection has to be maintained by Firefox OS devices, and applications can be shutdown, improving battery life, and device responsiveness, while still offering immediate updates to users.

Firefox OS Push Notifications are designed for one thing – waking up apps. They do not deal with data, desktop notifications and other features, since there are other Web APIs that provide them. In this Hacks article, we’ll take a look at building a small chat application that uses Push Notifications to update the conversation.

## Scope and workflow

Before we start on the application, it is a good idea to take a look at the scope and work flow of Push Notifications.

### No polling

The scope of Push Notifications is to notify web applications on clients that something on the network has changed, so that the data the client has should be updated to the latest data on a remote server. Rather than the application having to constantly poll using XHR or use WebSockets, Push takes over responsibility and notifies the application of the change. This data is usually stored on the application server (*in the cloud*) and shared on multiple devices distributed amongst one or more user.

For example, a user can have a personal calendar, which is shared between a laptop, a mobile and a tablet. In addition the user may have a work calendar that is shared with co-workers. A good calendar application on these devices will keep the devices in sync with the ‘master’ calendar on the server. With Push Notifications, Firefox OS devices can now do this sync immediately and be very responsive.

### No data

Firefox OS Push Notifications *do not* support sending messages over push. From the very beginning Push Notifications was designed to explicitly not carry a payload. This might seem absurd, but it falls in line with Mozilla’s mission of ensuring its user’s privacy. Multiple organizations will be running Push Servers, and if data was to be allowed on the Push protocol, this data ends up in the hands of these third parties. It is very easy to accidentally leak confidential user data. For example if the chat application sent the actual messages over Push, and a user decided to send his credit card number to another user, the credit card number is now in the hands of the Push Server operator.

To prevent this, the protocol simply does not allow data. The only application specific data allowed is a *version number* (optional). This *version number* is useful for collaborative applications. If a version number is sent, and the client device has already received a message with the same or *older* version number, it will not be notified again. The version number can be used to merge changes made by the user on this device with changes received from the server.

### Workflow

Continuing with the calendar example, the flow of push notifications works like this. The mobile application *registers* for a *push endpoint*. This *push endpoint* is a unique URL that represents one channel for receiving updates. These URLs point to a third party Push Server, which is set on the device and may be operated by Mozilla or other organizations or individuals. Each application can have multiple push endpoints (imagine one for each calendar the user has). The mobile application then sends this endpoint to the application server. A calendar server would associate this endpoint with the user and the specific calendar. Every calendar would have a set of endpoints, one for every device of every user that is subscribed to the calendar.

When any user changes the calendar on his device, the application saves those changes to the server. This is the point at which Push Notifications kick in. The application server will make a HTTP request to every one of the endpoints in the set for the calendar that was modified. Each Push Server now takes responsibility for delivering messages to the devices. When each device receives the notification, it starts the calendar application on the device and notifies it. The calendar app can then go and fetch all the changes from the calendar server.

NOTE: This URL should be treated as *opaque* and your application and application server should not make any assumptions about them, nor edit them.

### What happens if my application is not running?

Push notifications aren’t just a convenience, they are essential to mobile applications that need to keep in sync but may not always be running. If your application is not running when a push notification is received, the application will be started, navigated to the handling page and the message delivered to it. If you open the application switcher after receiving a push, you’ll be able to see the application running in the background.

## Setting up the environment

There are many resources on writing applications for Firefox OS with proper tooling and using all the facilities provided by the system. The two part hacks series [Building a Todo app for Firefox OS](https://hacks.mozilla.org/2013/06/building-a-todo-app-for-firefox-os-part-1/) is a great example. The chat application will instead be very bare bones. We’ll not concern ourselves with extra tooling like Volo. Nor will the app be very good looking by using standard UX elements. We’ll stick to simple HTML and JavaScript, with only jQuery and Bootstrap to for a few utilities.

The server will be written in Python, using the Flask framework, which is small and should be easy to understand even if you haven’t used Python before. In addition the server uses [Redis](http://redis.io) for a persistent data store.

All the code is [available on Github](https://github.com/nikhilm/simplechat).

Since Push Notifications is available on Firefox OS v1.1 onwards, you’ll currently need preview builds of the Firefox OS Simulator (please note that these are experimental, and not all might work as expected). Paste the URL for your platform into Firefox, install the Simulator add-on and you should be good to go with using Push.

The stable builds of the simulator on addons.mozilla.org DO NOT have push.

## The app manifest

Using Push Notifications requires three important entries in the applications manifest.

The `push`

permission allows the application to use Push Notifications. We also request `desktop-notification`

permission so we can show a notification when a user is mentioned in the chat.

The `messages`

entries specify which page of the application should be notified when a push notification is received. In this case, since our application is a single page application, we set it to `/`

. Firefox OS v1.1 only allows the page that registers for Push Notifications to recieve them, so you cannot have `/`

call `navigator.push.register()`

and have `/push.html`

be the receiver that uses `navigator.mozSetMessageHandler()`

.

The `push`

message is the message delivered when an actual notification is recieved. The `push-register`

message is a error recovery mechanism. In rare cases the Push Server may suffer data loss or it may decide to free up some old endpoints. In either case, if your application’s endpoints are no longer valid, it will receive a `push-register`

message, in which case your application should register for new endpoints and update the app server.

## The main page

Our chat application will be a single page application with the latest 50 messages, followed by a field to enter a new message.

The unordered list `chat`

will hold the chat messages, which will be loaded by JavaScript. `theform`

is used to submit messages. The div `nickPrompt`

is used as a modal dialog to ask the user’s nickname the first time the application is run. Finally we include the various scripts that drive the application.

## Offline web apps

As web applications are used on mobile devices, it is important to design them such that they can be used offline as much as possible. A common pattern in such a case is to have persistent storage on the client side using localStorage or IndexedDB. This storage is updated when a network connection is available, and the user content is displayed *solely* from this offline copy. This way the user can always interact with content that is already on the device. Our application follows a similar model. The latest chat messages are stored on the device using IndexedDB. A push notification will first update this local data and then update the UI.

## Chat Database

The storage is implemented in [model.js](https://github.com/nikhilm/simplechat/blob/master/www/js/model.js) which abstracts an IndexedDB database to support the operations a simple chat implementation requires. Every message is stored as a object:

```
{
"id": 5, // Integer message ID. Unique for every message.
"nick": "EdwardSnowden", // The sender of the message.
"message": "The NSA is spying!" // The actual text.
}
```

Only the latest 50 messages are stored on both the server and the client in a bid to compete against Snapchat.

The `id`

field is a perfect candidate to use as the `version`

field of the push notifications. In the case of a chat, every message will be new, so the version field is not so important, but we’ll use it for the purposes of demonstration.

## Installing the application

In Firefox OS v1.1, Push Notifications are only available to *applications* and not to web pages loaded in the browser. So when the user visits our application in the browser, it will prompt to install the app.

## Registering for Push Notifications

When the user starts the application, `go()`

is called. This prompts the user for a nickname on the first run, and populates the chat list using any existing messages already available offline.

The important bit for Push Notifications is this:

`navigator.push`

is the PushManager object that provides the Push Notifications operations. You can check for

```
if ('push' in navigator) {
}
```

to see if the page can use Push Notifications.

`registrations()`

is used to check if the application has existing endpoints registered. Like several other Firefox OS APIs it returns a [DOMRequest](https://developer.mozilla.org/en-US/docs/Web/API/DOMRequest) object since it is a async operation. On success, the result is a list of PushRegistration objects. A PushRegistration has the following fields:

```
interface PushRegistration {
string pushEndpoint; // A URL specifying the endpoint.
unsigned long int version; // The latest known version.
}
```

If we have no registrations, we ask for a new registration using `navigator.push.register()`

. On a successful registration, the `result`

field of the DOMRequest will be a URL, which is the endpoint for this registration. Now that we have a endpoint, we use XHR to send it to our server.

On the server, lets just store all the endpoints in one list called `endpoints`

:

In addition we send a quick ping to the new endpoint that was added. We use the great [Requests](http://docs.python-requests.org/en/latest/) library for this, and you can see how easy it is to use Push Notifications on the server. Just do a HTTP PUT request to the *endpoint* with the body of the request being:

```
version=<number>
```

The call to `navigator.push.register()`

can fail due to several reasons. The most common is that the device does not have network connectivity. The DOMRequest’s `onerror`

handler will be fired in such a case and the request’s

`error`

will have a short descriptive name of the error.

## Dispatching notifications

Every time a new message is posted to the chat, we want to notify all clients via push notifications. When a form is submitted:

the server is sent the message text and the sender’s nickname.

We request an `id`

for the message from Redis using the [INCR](http://redis.io/commands/incr) atomic command. We also want to enforce two things on the server:

- Keep the messages sorted by this message id, so we can quickly serve messages from a certain ID onwards. For this we use Redis’
[sorted sets](http://redis.io/topics/data-types#sorted-sets)with the`score`

as the message id. This keeps it sorted, and allows us to quickly fetch messages from a certain ID onwards, so that clients do not have to download all messages but we do not have to maintain individual queues for clients. - Restrict the messages to the latest 50 (
`MAX_MESSAGES`

). We do this by truncating the set using[ZREMRANGEBYRANK](http://redis.io/commands/zremrangebyrank).

We use [redis-py](https://github.com/andymccurdy/redis-py)‘s pipeline system to do both of these atomically so that if adding fails, so does removing older messages. Your language/framework will have similar operations to achieve this consistency.

The message itself is stored as a string of the JSON representation so that sending messages to clients is just a matter of extracting elements and concatenating them into a JSON list.

After that we put the new message id in the `notification_queue`

. This brings us to a best practice when using push notifications. The application server will often be notifying multiple endpoints about changes. In such a case, blocking the main server is a bad idea, Instead you should have a dedicated thread or process that can ping endpoints. This can even be moved off to a dedicated machine. The version number system allows you to parallelize the pinging.

In this simple server, we’re using Python’s builtin [Queue](http://docs.python.org/2/library/queue.html#module-Queue) which lets us implement a producer-consumer system. The thread that notifies the push server is started in `app.py`

and runs the `notify()`

function:

The notify() function blocks on the `notification_queue`

. When a new message id is available, it loops through all the endpoints and notifies them of the new version.

A successful PUT will result in a `200 OK`

response from the endpoint. This means the notification has been queued for delivery. When the device is online and connected to the Push Server, delivery happens within a few seconds.

The server’s job is done! Now the application has to handle the push notification.

## Receiving push notifications

Receiving push notifications is done by setting a function to be invoked when the ‘push’ message is received. This is done using `mozSetMessageHandler`

. NOTE: The page that sets the receiver and the page listed as the message

receiver in the manifest file *must* match!

After the model is successfully initialized we set the handler. `message`

will be a:

```
interface PushMessage {
string pushEndpoint; // The push endpoint that changed.
unsigned long int version; // The new version.
}
```

The pushEndpoint allows the app to identify which endpoint (among the many it

may have registered) has changed.

In this case, we just want to use this version to download new chat messages if required.

`model.latest()`

returns the latest message ID in our local storage, and we download new messages only if the version of the push notification is newer.

The server has a `/message/<id>`

REST interface, which given a message ID will return all the messages after it:

It simply uses the message ID as the sorted set score and returns a JSON response.

On the client, we update the local storage. To handle mentions, we also loop through the new messages received and check if any of the messages have the user’s nickname. If one is found, a desktop notification is created containing the message, so that the user notices a presumably important message.

Finally the UI is updated:

Since old messages have to be removed from view, we remove all the list items and add new ones. Modern Web Runtimes will do only one repaint even if multiple new elements are added to the DOM, as long as they are all added at once. So there is no flickering. Here too, we give messages mentioning the user a different colour.

A little thing to handle is the `push-register`

message. If you remember, I mentioned that this is a error recovery mechanism that may be invoked.

Our demo application simply shows an error to the user, but ideally you’d silently register for new endpoints in the background.

## Unregistering

A very common design pattern with push notifications is to associate one endpoint per user, where the user has a unique ID in your application and application server (such as an email ID). In that case your application may be designed to support switching users. In this case you no longer want to receive notifications when something of interest to the old user happens. There may be other situations in which you are no longer interested in a push endpoint. The way to express this lack of interest is to use `navigator.push.unregister()`

.

```
// Assuming pushEndpoint1 is the endpoint associated with an old user
var request = navigator.push.unregister(pushEndpoint1);
```

`unregister()`

returns a DOMRequest whose `onsuccess`

will fire as soon as the registration is deleted by Firefox OS. It is extremely unlikely that a call to unregister() will fail. The most likely cause of failure is that the endpoint is not a valid endpoint that was issued to the application by Firefox OS.

## Good design: Decouple Push from the user flow

Although the most common use of Push Notifications for web apps will be to show a desktop notification to the user, the process of push registration, receiving pushes, and unregistering should be kept out of the user’s UI flow as

much as possible. This is most applicable during registration.

Similar to progressive enhancement of the Web Application user experience, your app should be ready to deal with lack of Push notifications. For example, you should not block the user from signing into your application simply because `navigator.push.register()`

failed due to lack of connectivity. Instead, let the user continue to use the offline part of your application and queue the registration request to try again after some time. The [Alarm API](https://developer.mozilla.org/en-US/docs/WebAPI/Alarm) is useful to wake your application up later to finish such ‘background’ tasks.

Similarly, data heavy applications should not wait around for the user to respond to a desktop notification before they fetch data. A good calendar application will immediately go and update its local storage on receiving a push. Only then will it pop up any reminders so that as soon as the user launches the application, he immediately sees new events and changes. At the same time it should `unregister()`

endpoints if the user selects a manual sync option.

## Important security considerations

The push endpoint obtained from `register()`

should be kept *secret*! The best way to do this is:

1) Always send endpoints to the application server over a *secure* (https) connection. Otherwise an attacker could perform a man-in-the-middle attack and capture endpoints going over the wire.

2) Keep your database secure. The endpoints should be just as well protected as users personal data.

If an attacker were to gain access to endpoints, he or she could affect devices that have those endpoints. For example they could cause your application to run frequently, affecting the user experience. Or they could do a push to the endpoint with a very high version number so that subsequent valid pushes that your application server does will not be passed on to the app.

Connections between the Push Server and the devices are always over a secure connection and thus there can be a reasonable expectation of safety on that part of the exchange.

With that we’ve taken a short tour of the Firefox OS Push Notifications API. It will be exciting to see how you developers will leverage this to create fantastic web applications.

The Push Notifications team may be reached on the `#push`

IRC channel on `irc.mozilla.org`

.

## Extras

### Push Notification delivery guarantees

Push Notifications is a best effort system. The Push Server will try to inform a device of the latest version it has received for an endpoint. This means that updates are collapsed. If a endpoint is updated to version 254 while the device is offline, and then updated to 255, and then the device comes online, it will receive only the update for 255. When device and server end up in a inconsistent state that cannot be fixed, `push-register`

is usually fired to allow applications to reset itself. Despite these precautions, there are rare situations in which:

#### Notifications may fail to be delivered

If the device has been offline for more than a few days (a week or more), the Push Server may drop pending notifications to conserve its resources. In such a case, the device will not receive updates after it comes back online until the application server sends new updates. This is possible if the user is travelling on roaming and switches off mobile data.

If the device battery dies or the device crashes just as the notification is being delivered to the application, the application will miss that notification. This is extremely rare.

#### push-register may not be delivered

push-register may not be delivered even after the Push Server has reached an inconsistent state with the device.

If the device was offline when the Push Server lost state, the Push Server may not be able to inform the device that all state was lost when it comes back online.

For most applications the above should not be a problem since they will occur very rarely. If your application requires more reliability, you can mitigate the above possibilities by using a few other methods to sync. One way is to acquire new endpoints periodically rather than waiting for a `push-register`

. The other way is to use the [Alarm API](https://developer.mozilla.org/en-US/docs/WebAPI/Alarm) to do an unconditional synchronization with the application server after an extended period of time. For example, the application would use push to receive regular updates, but set an alarm for midnight every day when it would go and fetch updates regardless of the push status.

### Statuatory warning about experimental nature

The Push Notifications API for Firefox OS is *experimental*. One of the major changes coming in newer versions of Firefox OS will be a switch away from [DOMRequest](https://developer.mozilla.org/en-US/docs/Web/API/DOMRequest) to [Promises](http://dom.spec.whatwg.org/#promise). Until [Bug 800431](https://bugzil.la/800431) is fixed, the page calling `register()`

will have to be the same one that handles the notifications (‘push’ system message). In the future we would like to add support for background services or workers to handle notifications instead. This will ensure that no UI is launched unless the application requests it. There may be additional features added and in an extremely rare case, existing APIs may change.

While Mozilla will do its best to not break existing applications, developers should be aware of and plan for changes that may be required to their applications.

## About
[
Nikhil Marathe ](http://blog.nikhilism.com)

Nikhil is a Platform Engineer at Mozilla. He likes technical writing, having written 'An Introduction to libuv', and blogs at http://blog.nikhilism.com. He can be found working when he is not hiking, climbing or reading.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

Ollie ParsleyJuly 26th, 2013 at 04:53NikhilJuly 26th, 2013 at 13:00Ollie ParsleyJuly 26th, 2013 at 13:02Gene Vayngrib (@urbien)August 3rd, 2013 at 20:54