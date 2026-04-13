---
title: Offline Recipes for Service Workers – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/11/offline-service-workers/
author: David Walsh
published: '2015-11-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

“Offline” is a big topic these days, especially as many web apps look to also function as mobile apps. The original offline helper API, the Application Cache API (also known as “appcache”), has a host of problems, many of which can be found in Jake Archibald’s [Application Cache is a Douchebag](http://alistapart.com/article/application-cache-is-a-douchebag) post. Problems with appcache include:

- Files are served from cache even when the user is online.
- There’s no dynamism: the appcache file is simply a list of files to cache.
- One is able to
[cache the .appcache file itself](https://developer.mozilla.org/en-US/docs/Web/HTML/Using_the_application_cache#Gotchas)and that leads to update problems. [Other gotchas](https://developer.mozilla.org/en-US/docs/Web/HTML/Using_the_application_cache#Gotchas).

Today there’s a new API available to developers to ensure their web apps work properly: [the Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API). The Service Worker API allows developers to manage what does and doesn’t go into cache for offline use with JavaScript.

## Introducing the Service Worker Cookbook

To introduce you to the Service Worker API we’ll be using examples from Mozilla’s new Service Worker Cookbook! The Cookbook is a collection of working, practical examples of service workers in use in modern web apps. We’ll be introducing service workers within this three-part series:

- Offline Recipes for Service Workers (today’s post)
- At Your Service for More Than Just appcache
- Web Push Updates to the Masses

Of course this API has advantages other than enabling offline capabilities, such as performance for one, but I’d like to start by introducing basic service worker strategies for offline.

## What do we mean by *offline*?

Offline doesn’t just mean the user doesn’t have an internet connection — it can also mean that the user is on a flaky network connection. Essentially “offline” means that the user doesn’t have a reliable connection, and we’ve all been there before!

## Recipe: Offline Status

The Offline Status recipe illustrates how to use a service worker to cache a known asset list and then notify the user that they may now go offline and use the app. The app itself is quite simple: show a random image when a button is clicked. Let’s have a look at the components involved in making this happen.

### The Service Worker

We’ll start by looking at the `service-worker.js`

file to see what we’re caching. We’ll be caching the random images to display, as well as the display page and critical JavaScript resources, in a cache named `dependencies-cache`

:

```
var CACHE_NAME = 'dependencies-cache';
// Files required to make this app work offline
var REQUIRED_FILES = [
'random-1.png',
'random-2.png',
'random-3.png',
'random-4.png',
'random-5.png',
'random-6.png',
'style.css',
'index.html',
'/', // Separate URL than index.html!
'index.js',
'app.js'
];
```


The service worker’s `install`

event will open the cache and use `addAll`

to direct the service worker to cache our specified files:

```
self.addEventListener('install', function(event) {
// Perform install step: loading each required file into cache
event.waitUntil(
caches.open(CACHE_NAME)
.then(function(cache) {
// Add all offline dependencies to the cache
return cache.addAll(REQUIRED_FILES);
})
.then(function() {
// At this point everything has been cached
return self.skipWaiting();
})
);
});
```


The `fetch`

event of a service worker is fired for every single request the page makes. The `fetch`

event also allows you to serve alternate content than was actually requested. For the purposes of offline content, however, our `fetch`

listener will be very simple: if the file is cached, return it from cache; if not, retrieve the file from server:

```
self.addEventListener('fetch', function(event) {
event.respondWith(
caches.match(event.request)
.then(function(response) {
// Cache hit - return the response from the cached version
if (response) {
return response;
}
// Not in cache - return the result from the live server
// `fetch` is essentially a "fallback"
return fetch(event.request);
}
)
);
});
```


The last part of this `service-worker.js`

file is the `activate`

event listener where we immediately claim the service worker so that the user doesn’t need to refresh the page to activate the service worker. The `activate event`

fires when a previous version of a service worker (if any) has been replaced and the updated service worker takes control of the scope.

```
self.addEventListener('activate', function(event) {
// Calling claim() to force a "controllerchange" event on navigator.serviceWorker
event.waitUntil(self.clients.claim());
});
```


Essentially we don’t want to require the user to refresh the page for the service worker to begin — we want the service worker to activate upon initial page load.

### Service worker registration

With the simple service worker created, it’s time to register the service worker:

```
// Register the ServiceWorker
navigator.serviceWorker.register('service-worker.js', {
scope: '.'
}).then(function(registration) {
// The service worker has been registered!
});
```


Remember that the goal of the recipe is to notify the user when required files have been cached. To do that we’ll need to listen to the service worker’s `state`

. When the `state`

has become `activated`

, we know that essential files have been cached, our app is ready to go offline, and we can notify our user:

```
// Listen for claiming of our ServiceWorker
navigator.serviceWorker.addEventListener('controllerchange', function(event) {
// Listen for changes in the state of our ServiceWorker
navigator.serviceWorker.controller.addEventListener('statechange', function() {
// If the ServiceWorker becomes "activated", let the user know they can go offline!
if (this.state === 'activated') {
// Show the "You may now use offline" notification
document.getElementById('offlineNotification').classList.remove('hidden');
}
});
});
```


Testing the registration and verifying that the app works offline simply requires using the recipe! This recipe provides a button to load a random image by changing the image’s `src`

attribute:

```
// This file is required to make the "app" work offline
document.querySelector('#randomButton').addEventListener('click', function() {
var image = document.querySelector('#logoImage');
var currentIndex = Number(image.src.match('random-([0-9])')[1]);
var newIndex = getRandomNumber();
// Ensure that we receive a different image than the current
while (newIndex === currentIndex) {
newIndex = getRandomNumber();
}
image.src = 'random-' + newIndex + '.png';
function getRandomNumber() {
return Math.floor(Math.random() * 6) + 1;
}
});
```


Changing the image’s `src`

would trigger a network request for that image, but since we have the image cached by the service worker, there’s no need to make the network request.

This recipe covers probably the most simple of offline cases: caching required static files for offline use.

## Recipe: Offline Fallback

This recipe follows another simple use case: fetch a page via AJAX but respond with another cached HTML resource (`offline.html`

) if the request fails.

### The service worker

The `install`

step of the service worker fetches the `offline.html`

file and places it into a cache called `offline`

:

```
self.addEventListener('install', function(event) {
// Put `offline.html` page into cache
var offlineRequest = new Request('offline.html');
event.waitUntil(
fetch(offlineRequest).then(function(response) {
return caches.open('offline').then(function(cache) {
return cache.put(offlineRequest, response);
});
})
);
});
```


If that request fails the service worker won’t register because the promise is rejected.

The `fetch`

listener listens for a request for the page and, upon failure, responds with the `offline.html`

file we cached during the event registration:

```
self.addEventListener('fetch', function(event) {
// Only fall back for HTML documents.
var request = event.request;
// && request.headers.get('accept').includes('text/html')
if (request.method === 'GET') {
// `fetch()` will use the cache when possible, to this examples
// depends on cache-busting URL parameter to avoid the cache.
event.respondWith(
fetch(request).catch(function(error) {
// `fetch()` throws an exception when the server is unreachable but not
// for valid HTTP responses, even `4xx` or `5xx` range.
return caches.open('offline').then(function(cache) {
return cache.match('offline.html');
});
})
);
}
// Any other handlers come here. Without calls to `event.respondWith()` the
// request will be handled without the ServiceWorker.
});
```


Notice we use `catch`

to detect if the request has failed and that therefore we should respond with `offline.html`

content.

### Service Worker Registration

A service worker needs to be registered only once. This example shows how to bypass registration if it’s already been done by checking the presence of the `navigator.serviceWorker.controller`

property; if the `controller`

property doesn’t exist, we move on to registering the service worker.

```
if (navigator.serviceWorker.controller) {
// A ServiceWorker controls the site on load and therefor can handle offline
// fallbacks.
console.log('DEBUG: serviceWorker.controller is truthy');
debug(navigator.serviceWorker.controller.scriptURL + ' (onload)', 'controller');
}
else {
// Register the ServiceWorker
console.log('DEBUG: serviceWorker.controller is falsy');
navigator.serviceWorker.register('service-worker.js', {
scope: './'
}).then(function(reg) {
debug(reg.scope, 'register');
});
}
```


With the service worker confirmed as registered, you can test the recipe (and trigger the new page request) by clicking the “refresh” link: (which then triggers a page refresh with a cache-busting parameter):

```
// The refresh link needs a cache-busting URL parameter
document.querySelector('#refresh').search = Date.now();
```


Providing the user an offline message instead of allowing the browser to show its own (sometimes ugly) message is an excellent way of keeping a dialog with the user about why the app isn’t available while they’re offline!

## Go offline!

Service workers have moved offline experience and control into a powerful new space. Today you can use the Service Worker API in Chrome and [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/). Many websites are using service workers today as you can see for yourself by going to `about:serviceworkers`

in Firefox Developer Edition; you’ll see a listing of installed service workers from websites you’ve visited!

The Service Worker Cookbook is full of excellent, practical recipes and we continue to add more. Keep an eye out for the next post in this series, *At Your Service for More than Just appcache*, where you’ll learn about using the Service Worker API for more than just offline purposes.

## About
[
David Walsh ](http://davidwalsh.name/)

David Walsh is a Web Developer for Mozilla, working primarily on the Mozilla Developer Network. He's also a conference speaker, blogger, and web enthusiast.

## 2 comments

LukeNovember 21st, 2015 at 20:15VollutaNovember 22nd, 2015 at 05:01