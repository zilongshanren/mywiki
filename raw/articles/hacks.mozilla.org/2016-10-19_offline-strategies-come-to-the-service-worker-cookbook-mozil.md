---
title: Offline strategies come to the Service Worker Cookbook – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2016/10/offline-strategies-come-to-the-service-worker-cookbook/
author: Salva
published: '2016-10-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

serviceworke.rs is a compendium of common and [uncommon](https://hacks.mozilla.org/2015/12/beyond-offline/) Service Worker use cases including push examples, usage patterns, performance tips and caching strategies.

Service Worker Cookbook recipes are presented as playgrounds or labs, with fully functional client-server setups, where you can learn and experiment with results using in-browser developer tools.

Still, the cookbook is far from comprehensive, and we realised it lacked some basic materials and user feedback mechanisms. Today, I’m proud to announce some changes to the Service Worker Cookbook starting with a new section about **caching strategies**.

## Caching Strategies

Caching strategies includes recipes that demo several ways of serving content from a service worker. The recipes follow an identical layout in which two iframes are displayed side by side. Both show an image element pointing to the same online picture.

The first iframe is not under service worker interception, so the picture always displays fresh content from the server. In contrast, the second iframe is controlled by the service worker and the content is served according to the implemented cache strategy.

Picture content changes on the server every 10 seconds and you have a button to refresh both iframes at the same time and compare what happens to the images.

Some of the caching strategies are taken from an inspiring article from [Jake Archibald’s “The offline cookbook”](https://jakearchibald.com/2014/offline-cookbook/#on-network-response) and others are homegrown.

### Cache only

The most basic example: With *cache only*, requests will never reach the network. Instead, they will be served by the service worker from a local cache.

```
self.addEventListener('fetch', function(evt) {
evt.respondWith(fromCache(evt.request));
});
function fromCache(request) {
return caches.open(CACHE).then(function (cache) {
return cache.match(request).then(function (matching) {
return matching || Promise.reject('no-match');
});
});
}
```


In this implementation, cache-only assets are stored while installing the service worker and they will remain there until a new version of the worker is installed.

```
self.addEventListener('install', function(evt) {
evt.waitUntil(precache());
});
function precache() {
return caches.open(CACHE).then(function (cache) {
return cache.addAll([
'./controlled.html',
'./asset'
]);
});
}
```


You can use the **cache-only strategy** for your site’s UI related assets such as images, HTML, sprite sheets or CSS files.

### Cache and update

This slight variation on the cache-only strategy also serves assets from a local cache but it also sends network requests for updated versions of the assets. The new content then replaces the older asset in the local cache.

```
self.addEventListener('fetch', function(evt) {
evt.respondWith(fromCache(evt.request));
evt.waitUntil(update(evt.request));
});
function update(request) {
return caches.open(CACHE).then(function (cache) {
return fetch(request).then(function (response) {
return cache.put(request, response);
});
});
}
```


With this **cache and update strategy**, there comes a point when your assets are no longer synched with those online, but they will be synched upon a second request, which roughly translates to a second visit.

It is totally fine to use this strategy when delivering independent, non-critical content such as avatars or icons. Avoid relying on this strategy for dependent assets (such a complete UI theme) since there is nothing ensuring that the assets will update as needed at the same time.

### Cache, update and refresh

Another twist on the previous strategy, now with a **refreshing ingredient**.

With **cache, update and refresh** the client will be notified by the service worker once new content is available. This way your site can show content without waiting for the network responses, while providing the UI with the means to display up-to-date content in a controlled way.

```
self.addEventListener('fetch', function(evt) {
evt.respondWith(fromCache(evt.request));
evt.waitUntil(
update(evt.request)
.then(refresh)
);
});
function refresh(response) {
return self.clients.matchAll().then(function (clients) {
clients.forEach(function (client) {
var message = {
type: 'refresh',
url: response.url,
eTag: response.headers.get('ETag')
};
client.postMessage(JSON.stringify(message));
});
});
}
```


This is especially useful when fetching any kind of content. This is different than the previous strategy in that there is no need for a user to refresh or visit the site a second time. Because the client is aware of new content, the UI could update in smart, non-intrusive ways.

### Embedded fallback

There are situations in which you always want to always display something to replace content that’s missing for whatever reason (network error, 404, no connection). It’s possible to ensure always available offline content by **embedding that content into the service worker**.

```
self.addEventListener('fetch', function(evt) {
evt.respondWith(networkOrCache(evt.request).catch(function () {
return useFallback();
}));
});
// Dunno why this is shown as the actual SVG in WordPress but it looks awesome!
// You can see the source code in the recipe.
var FALLBACK =
'' +
' ' +
' ' +
' ' +
' ' +
'';
function useFallback() {
return Promise.resolve(new Response(FALLBACK, { headers: {
'Content-Type': 'image/svg+xml'
}}));
}
```



In this recipe, the SVG which acts as a replacement for missing content is included in the worker. As soon as it is installed, fallbacks will be available without performing new network requests.

### Network or cache

Service Workers place themselves between the client and the Internet. To some extent, they allow the developer to model their ideal network behaviour. This strategy exploits/enhances that idea by imposing time limits on network responses.

```
self.addEventListener('fetch', function(evt) {
evt.respondWith(fromNetwork(evt.request, 400).catch(function () {
return fromCache(evt.request);
}));
});
function fromNetwork(request, timeout) {
return new Promise(function (fulfill, reject) {
var timeoutId = setTimeout(reject, timeout);
fetch(request).then(function (response) {
clearTimeout(timeoutId);
fulfill(response);
}, reject);
});
}
```



With this recipe, requests are intercepted by the service worker and passed to the network. If the response takes too long, the process is interrupted and the content is served from a local cache instead.

**Time limited network or cache** can actually be combined with any other technique. The strategy simply gives the network a chance to answer quickly with fresh content.

## User feedback

We want to know if recipes are useful, and if you find them clear or confusing. Do they provide unique value or are they redundant? We’ve added Disqus comments to recipes so you can share your feedback. Log in with Facebook, Twitter, Google or Disqus, and tell us how this recipe has served you or participate in the discussion about recommended use cases.

## And more to come

We won’t stop here. More recipes are coming and new enhancements are on their way: a improved way to ask for recipes, an easier contribution pipeline, a visual refresh and a renewed recipe layout are things on our radar. If you like **serviceworke.rs** please share them with your friends and colleagues. Feel free to use these recipes in your talks or presentations, and, most importantly, help us by providing feedback in the form of on site comments, filing GitHub issues or by [tweeting me directly](https://twitter.com/salvadelapuente) ;)

Your opinion is really appreciated!

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## 4 comments

jxnOctober 19th, 2016 at 22:48SalvaOctober 20th, 2016 at 12:40jxnOctober 27th, 2016 at 07:12jxnOctober 27th, 2016 at 07:23