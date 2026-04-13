---
title: BroadcastChannel API in Firefox 38 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/02/broadcastchannel-api-in-firefox-38/
author: Posted
published: '2015-02-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Recently the [BroadcastChannel API](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API) landed in Firefox 38. This API can be used for simple messaging between browser contexts that have the same user agent and origin. This API is exposed to both Windows and Workers and allows communication between iframes, browser tabs, and worker threads.

The intent of the BroadcastChannel API is to provide an API that facilitates communicating simple messages between browser contexts within a web app. For example, when a user logs into one page of an app it can update all the other contexts (e.g. tabs or separate windows) with the user’s information, or if a user uploads a photo to a browser window, the image can be passed around to other open pages within the app. This API is not intended to handle complex operations like shared resource locking or synchronizing multiple clients with a server. In those cases, a shared worker is more appropriate.

### API Overview

A BroadcastChannel object can be created by using the following code:

`var myChannel = new BroadcastChannel("channelname");`

The channelname is case sensitive. The BroadcastChannel instance contains two methods, postMessage and close. The postMessage method is used for sending messages to the channel. The message contents can be any object, including complex objects such as images, arrays, and arrays of objects. When the message is posted, all browser contexts with the same origin, user agent, and a BroadcastChannel with the same channel name are notified of the message. For example, the following code posts a simple string:

`myChannel.postMessage("Simple String");`

The dispatched message can be handled by any page with the channel opened by using the onmessage event handler of the BroadcastChannel instance.

```
myChannel.onmessage = function(event) {
console.log(event.data);
}
```

Note that the data attribute of the event contains the data of the message. Other attributes of the event may be of interest as well. For example, you can check the web app origin using the event.origin attribute or the channel name is available in the event.target.name attribute.

The close method is used to close the channel for the particular browser context and can be called by simply using:

`broadCastChannel.close();`

### Blob Message Posting

While posting strings and other primitive types is fairly simple, the BroadcastChannel API supports more complex objects as well. For example, to post an Image from one context to another the following code could be used.

```
var broadcastExample = {};
broadcastExample.setupChannel = function() {
if ("BroadcastChannel" in window) {
if (typeof broadcastExample.channel === 'undefined' ||
!broadcastExample.channel) {
//create channel
broadcastExample.channel = new BroadcastChannel("foo");
}
}
}
broadcastExample.pMessage = function() {
broadcastExample.setupChannel();
//get image element
var img = document.getElementById("ffimg");
//create canvas with image
var canvas = document.createElement("canvas");
canvas.width = img.width;
canvas.height = img.height;
var ctx = canvas.getContext("2d");
ctx.drawImage(img, 0, 0);
//get blob of canvas
canvas.toBlob(function(blob) {
//broadcast blob
broadcastExample.channel.postMessage(blob);
});
}
```

The above code contains two functions and represents the sender side of a BroadcastChannel client. The setupChannel method just opens the Broadcast Channel and the pMessage method retrieves an image element from the page and converts it to a Blob. Lastly the Blob is posted to the BroadcastChannel. The receiver page will need to already be listening to the BroadcastChannel in order to receive the message and can be coded similar to the following.

```
var broadcastFrame = {};
//setup broadcast channel
broadcastFrame.setup = function() {
if ("BroadcastChannel" in window) {
if (typeof broadcastFrame.channel === 'undefined' || !broadcastFrame.channel) {
broadcastFrame.channel = new BroadcastChannel("foo");
}
//function to process broadcast messages
function func(e) {
if (e.data instanceof Blob) {
//if message is a blob create a new image element and add to page
var blob = e.data;
var newImg = document.createElement("img"),
url = URL.createObjectURL(blob);
newImg.onload = function() {
// no longer need to read the blob so it's revoked
URL.revokeObjectURL(url);
};
newImg.src = url;
var content = document.getElementById("content");
content.innerHTML = "";
content.appendChild(newImg);
}
};
//set broadcast channel message handler
broadcastFrame.channel.onmessage = func;
}
}
window.onload = broadcastFrame.setup();
```

This code takes the blob from the broadcast message and creates an image element, which is added to the receiver page.

### Workers and BroadcastChannel messages

The BroadcastChannel API also works with dedicated and shared [workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/basic_usage). As a simple example, assume a worker is started and when a message is sent to the worker through the main script, the worker then broadcasts a message to the Broadcast Channel.

```
var broadcastExample = {};
broadcastExample.setupChannel = function() {
if ("BroadcastChannel" in window) {
if (typeof broadcastExample.channel === 'undefined' ||
!broadcastExample.channel) {
//create channel
broadcastExample.channel = new BroadcastChannel("foo");
}
}
}
function callWorker() {
broadcastExample.setupChannel();
//verify compat
if (!!window.Worker) {
var myWorker = new Worker("worker.js");
//ping worker to post to Broadcast Channel
myWorker.postMessage("Broadcast from Worker");
}
}
//Worker.js
onmessage = function(e) {
//Broadcast Channel Message with Worker
if ("BroadcastChannel" in this) {
var workerChannel = new BroadcastChannel("foo");
workerChannel.postMessage("BroadcastChannel Message Sent from Worker");
workerChannel.close();
}
}
```

The message can be handled in the main page in the same way as described in previous sections of this post.

![workerbroadcast](../../assets/5000baa16e84f354.png)


*Using a Worker to Broadcast a message to an iframe*

### More Information

In addition to demonstrating how to use in an iframe, another example of using the code in this post is available on [github](https://github.com/JasonWeathersby/broadcastchannelexample). More information about the BroadcastChannel API is available in the [specification](https://html.spec.whatwg.org/multipage/comms.html#broadcasting-to-other-browsing-contexts), [bugzilla entry](https://bugzilla.mozilla.org/show_bug.cgi?id=966439), and on [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API). The code and test pages for the API are located in the gecko [source code](https://github.com/mozilla/gecko-dev/tree/master/dom/broadcastchannel).

## 8 comments

Hubert SABLONNIEREFebruary 3rd, 2015 at 01:05Jason WeathersbyFebruary 4th, 2015 at 08:24LukeFebruary 4th, 2015 at 21:36Hubert SABLONNIEREFebruary 5th, 2015 at 08:32Nick DesaulniersFebruary 5th, 2015 at 12:27anonFebruary 5th, 2015 at 13:50jperrier@mozilla.comFebruary 6th, 2015 at 01:09Jason WeathersbyFebruary 6th, 2015 at 05:49