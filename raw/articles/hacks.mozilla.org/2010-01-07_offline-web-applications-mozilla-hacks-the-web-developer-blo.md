---
title: offline web applications – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/01/offline-web-applications/
author: Paul Rouget
published: '2010-01-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The network is a key component of any web application, whether it is used to download JavaScript, CSS, and HTML source files and accompanying resources (images, videos, …) or to reach web services (XMLHttpRequest and `<forms>`

).

Yet having offline support for web applications can be very useful to users. Imagine, for example, a webmail application that allows users to read emails already in their inbox and write new messages even when they are not connected.

The mechanism used to support offline web applications can also be used to improve an application’s performance by storing data in the cache or to make data persistent between user sessions and when reloading and restoring pages.

### Demo: a To Do List Manager

To see an offline web application in action, watch Vivien Nicolas’ demo ([OGV](http://videos.mozilla.org/serv/marketing/offlinewebapps/20100105_offlinewebapps.ogv), [MP4](http://videos.mozilla.org/serv/marketing/offlinewebapps/20100105_offlinewebapps.mp4)), which shows a to do list manager working online and offline on an N900 running Firefox.

You can also check out the [live demo](https://developer.mozilla.org/media/uploads/demos/p/a/paulrouget/8bfba7f0b6c62d877a2b82dd5e10931e/hacksmozillaorg-achi_1334270447_demo_package/todo/) of the application.

### Creating your Own Offline Application

For a web application to work offline, you need to consider three things:

- Store user inputs through
[localStorage](https://developer.mozilla.org/en/DOM/Storage) - Define which files should be cached via a
[manifest file](https://developer.mozilla.org/en/Offline_resources_in_Firefox#Specifying_a_cache_manifest) - Manage connection changes with
[online and offline events](https://developer.mozilla.org/en/Online_and_offline_events)

Let’s see how to use each of these components.

### Storage: Persistent Data

[DOM storage](https://developer.mozilla.org/en/DOM/Storage) lets you store data between browser sessions, share data between tabs and prevent data loss (for example from page reloads or browser restarts). The data are stored as strings (for example a JSONified JavaScript object) in a Storage object.

There are two kinds of storage global objects: `sessionStorage`

and `localStorage`

.

`sessionStorage`

maintains a storage area that’s available for the duration of the page session. A page session lasts for as long as the browser is open and survives over page reloads and restores. Opening a page in a new tab or window causes a new session to be initiated.`localStorage`

maintains a storage area that can be used to hold data over a long period of time (e.g. over multiple pages and browser sessions). It’s not destroyed when the user closes the browser or switches off the computer.

Both localStorage and sessionStorage use the following API:

```
window.localStorage and window.sessionStorage {
long length; // Number of items stored
string key(long index); // Name of the key at index
string getItem(string key); // Get value of the key
void setItem(string key, string data); // Add a new key with value data
void removeItem(string key); // Remove the item key
void clear(); // Clear the storage
};
```

Here is an example showing how to store and how to read a string:

```
// save the string
function saveStatusLocally(txt) {
window.localStorage.setItem("status", txt);
}
// read the string
function readStatus() {
return window.localStorage.getItem("status");
}
```

Note that the storage properties are limited to an HTML5 origin (scheme + hostname + non-standard port). This means that window.localStorage from http://foo.com is a different instance of window.localStorage from http://bar.com. For example, http://google.com can’t access the storage of http://yahoo.com.

### Are We Offline?

Before storing data, you may want to [know if the user is online or not](https://developer.mozilla.org/en/Online_and_offline_events). This can be useful, for example, to decide whether to store a value locally (client side) or to send it to the server.

Check if the user is online with the `navigator.onLine`

property.

In addition, you can be notified of any connectivity changes by listening to the `online`

and `offline`

events of the window element.

Here is a very simple piece of JavaScript code, which sends your status to a server (à la twitter).

- If you set your status and you’re online, it sends the status.
- If you set your status and you’re offline, it stores your status.
- If you go online and have a stored status, it sends the stored status.
- If you load the page, are online, and have a stored status, it sends the stored status.

```
function whatIsYourCurrentStatus() {
var status = window.prompt("What is your current status?");
if (!status) return;
if (navigator.onLine) {
sendToServer(status);
} else {
saveStatusLocally(status);
}
}
function sendLocalStatus() {
var status = readStatus();
if (status) {
sendToServer(status);
window.localStorage.removeItem("status");
}
}
window.addEventListener("load", function() {
if (navigator.onLine) {
sendLocalStatus();
}
}, true);
window.addEventListener("online", function() {
sendLocalStatus();
}, true);
window.addEventListener("offline", function() {
alert("You're now offline. If you update your status, it will be sent when you go back online");
}, true);
```

### Offline Resources: the Cache Manifest

When offline, a user’s browser can’t reach the server to get any files that might be needed. You can’t always count on the browser’s cache to include the needed resources because the user may have cleared the cache, for example. This is why you need to define explicitly which files must be stored so that all needed files and resources are available when the user goes offline: HTML, CSS, JavaScript files, and other resources like images and video.

The [manifest file](https://developer.mozilla.org/en/Offline_resources_in_Firefox#Specifying_a_cache_manifest) is specified in the HTML and contains the explicit list of files that should be cached for offline use by the application.

```
```

Here is an example of the contents of a manifest file:

```
CACHE MANIFEST
fonts/MarketingScript.ttf
css/main.css
css/fonts.css
img/face.gif
js/main.js
index.xhtml
```

The MIME-Type type of the manifest file must be: `text/cache-manifest`

.

[See the documentation](https://developer.mozilla.org/en/Offline_resources_in_Firefox#Specifying_a_cache_manifest) for more details on the manifest file format and cache behavior.

### Summary

The key components you should remember to think about when making your application work offline are to [store the user inputs](https://developer.mozilla.org/en/DOM/Storage) in localStorage, create a [cache manifest](https://developer.mozilla.org/en/Offline_resources_in_Firefox#Specifying_a_cache_manifest) file, and [monitor connection changes](https://developer.mozilla.org/en/Online_and_offline_events).

Visit the [Mozilla Developer Center](https://developer.mozilla.org/) for the complete documentation.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 34 comments

Paul RougetJanuary 7th, 2010 at 12:45ChrisJanuary 7th, 2010 at 21:49EeveeJanuary 7th, 2010 at 22:33zahraJanuary 12th, 2011 at 08:02frank goossensJanuary 8th, 2010 at 00:33Jon RimmerJanuary 8th, 2010 at 03:23mattJanuary 8th, 2010 at 04:51Natanael LJanuary 8th, 2010 at 06:30Cedric DugasJanuary 8th, 2010 at 08:33nemoJanuary 9th, 2010 at 20:11yannskiJanuary 12th, 2010 at 07:11Paul RougetJanuary 15th, 2010 at 08:05yannskiJanuary 17th, 2010 at 15:44PeteFebruary 18th, 2010 at 12:50Aris MicroFebruary 21st, 2010 at 18:49Omkar KandarpaJune 1st, 2010 at 01:21PatrickJuly 28th, 2010 at 04:49GünterOctober 31st, 2010 at 05:28Pedro MoraisNovember 28th, 2010 at 09:38ManiMay 22nd, 2011 at 20:49louisremiMay 23rd, 2011 at 08:42ManiMay 23rd, 2011 at 08:54Yv.RFebruary 12th, 2013 at 07:56IMEVERFebruary 19th, 2013 at 03:04