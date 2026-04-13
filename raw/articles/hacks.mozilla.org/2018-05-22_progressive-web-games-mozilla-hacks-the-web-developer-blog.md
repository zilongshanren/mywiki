---
title: Progressive Web Games – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/05/progressive-web-games/
author: Andrzej Mazur
published: '2018-05-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With the recent release of the [Progressive Web Apps core guides](https://hacks.mozilla.org/2018/05/progressive-web-apps-core-guides-on-mdn-web-docs/) on MDN, it’s easier than ever to make your website look and feel as responsive as native on mobile devices. But how about games?

In this article, we’ll explore the concept of *Progressive Web Games* to see if the concept is practical and viable in a modern web development environment, using PWA features built with Web APIs.

Let’s look at the [Enclave Phaser Template](https://github.com/EnclaveGames/Enclave-Phaser-Template/) (EPT) — a free, open sourced mobile boilerplate for HTML5 games that I created using the [Phaser game engine](https://phaser.io/). I’m using it myself to build all my [Enclave Games](https://enclavegames.com/) projects.

The template was recently upgraded with some PWA features: [Service Workers](https://developer.mozilla.org/en-US/Apps/Progressive/Offline_Service_workers) provide the ability to cache and serve the game when offline, and a manifest file allows it to be [installed](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Installable_PWAs) on the home screen. We also provide access to [notifications](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Re-engageable_Notifications_Push), and much more. These PWA features are already built-in into the template, so you can focus on developing the game itself.

We will see how those features can solve problems developers have today: adding to home screen and working offline. The third part of this article will introduce the concept of progressive loading.

## Add to Home screen

Web games can show their full potential on mobile, especially if we create some features and shortcuts for developers. The *Add to Home screen* feature makes it easier to build games that can compete with native games for screen placement and act as first class citizens on mobile devices.

Progressive Web Apps can be installed on modern devices with the help of this feature. You enable it by including a manifest file — the icon, modals and install banners are created based on the information from *ept.webmanifest*:

```
{
"name": "Enclave Phaser Template",
"short_name": "EPT",
"description": "Mobile template for HTML5 games created using the Phaser game engine.",
"icons": [
{
"src": "img/icons/icon-32.png",
"sizes": "32x32",
"type": "image/png"
},
// ...
{
"src": "img/icons/icon-512.png",
"sizes": "512x512",
"type": "image/png"
}
],
"start_url": "/index.html",
"display": "fullscreen",
"theme_color": "#DECCCC",
"background_color": "#CCCCCC"
}
```


It’s not the only requirement though — be sure to check the [Add to Home Screen article](https://developer.mozilla.org/en-US/Apps/Progressive/Add_to_home_screen) for all the details.

## Offline capabilities

Developers often have issues getting desktop games (or mobile-friendly games showcased on a PC with a monitor) to work offline. This is especially challenging when demoing a game at a conference with unreliable wifi! Best practice is to plan ahead and have all the files of the game available locally, so that you can launch them offline.

Offline builds can be tricky, as you’ll have to manage the files yourself, remember your versions, and whether you’ve applied the latest patch or fixed that bug from previous conferences, work out the hardware setup, etc. This takes time and extra preparation.

Web games are easier to handle online when you have reliable connectivity: You point the browser to a URL and you have the latest version of your game running in no time. The network connection is the problem. It would be nice to have an offline solution.

The good news is that Progressive Web Apps can help — Service Workers cache and serve assets [offline](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Offline_Service_workers), so an unstable network connection is not the problem it used to be.

The [Service Worker file](https://github.com/EnclaveGames/Enclave-Phaser-Template/blob/gh-pages/src/sw.js) in the Enclave Phaser Template contains everything we need. It starts with the list of files to be cached:

```
var cacheName = 'EPT-v1';
var appShellFiles = [
'./',
'./index.html',
// ...
'./img/overlay.png',
'./img/particle.png',
'./img/title.png'
];
```


Then the install event is handled, which adds all the files to the cache:

```
self.addEventListener('install', function(e) {
e.waitUntil(
caches.open(cacheName).then(function(cache) {
return cache.addAll(appShellFiles);
})
);
});
```


Next comes the fetch event, which will serve content from cache and add a new one, if needed:

```
self.addEventListener('fetch', function(e) {
e.respondWith(
caches.match(e.request).then(function(r) {
return r || fetch(e.request).then(function(response) {
return caches.open(cacheName).then(function(cache) {
cache.put(e.request, response.clone());
return response;
});
});
})
);
});
```


Be sure to check the [Service Worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers) article for a detailed explanation.

## Progressive loading

[Progressive loading](https://developer.mozilla.org/en-US/Apps/Progressive/Loading) is an interesting concept that can provide many benefits for web game development. Progressive loading is basically “lazy loading” in the background. It’s not dependent on a specific API, but it follows the PWA approach and uses several of the key features we’ve just described, focused on games, and their specific requirements.

Games are heavier than apps in terms of resources — even for small and casual ones, you usually have to download 5-15 MB of assets, from images to sounds. This is supposed to be instantaneous, but you still have to wait through the loading screen when everything is downloaded. Or, if might be problematic if the player has a poor connection: the longer the download time, the bigger the chance that gameplay will be abandoned and the tab will be closed.

But what if instead of downloading everything, you loaded only what’s really needed first, and then downloaded the rest in the background? This way the player would see the main menu of your game way faster than with the traditional approach. They would spend at least a few seconds looking around while the files for the gameplay are retrieved in the background invisibly. And even if they clicked the play button really quickly, we could show a loading animation while everything else is loaded.

Instant Games are gaining in popularity, and a game developer building casual mobile HTML5 games should probably consider putting them on the [Facebook](https://developers.facebook.com/blog/post/2018/03/14/instant-games-platform-open) or [Google](https://blog.google/products/google-play/introducing-google-play-instant-faster-way-try-apps-and-games/) platforms. There are some requirements to meet, especially concerning the initial file size and download time, as the games are supposed to be instantly available for play.

Using the *lazy loading* technique, the game will feel faster than it would otherwise, given the amount of data required for it to be playable. You can achieve these results using the [Phaser framework](https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_breakout_game_Phaser), which is pre-built to load most of the assets after the main menu resources arrive. You can also implement this yourself in pure JavaScript, using the link prefetch/defer mechanism. There’s more than one way to achieve progressive loading – it’s a powerful idea that’s independent of the specific approach or tools you choose, following the principles of Progressive Web Apps.

## Conclusion

Do you have any more ideas on how to enhance the gaming experience? Feel free to play and experiment, and shape the future of web games. Drop a comment here if you’ve got ideas to share.

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.

## 3 comments

NjibhuMay 24th, 2018 at 07:53Andrzej MazurMay 26th, 2018 at 07:38James C, DeeringMay 29th, 2018 at 18:37