---
title: 'Trainspotting: Firefox 44 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/02/trainspotting-firefox-44/
author: Sergi Mansilla
published: '2016-02-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Trainspotting is a series of articles highlighting features in the lastest version of Firefox. A new version of Firefox is shipped every six weeks or sometimes eight– we at Mozilla call this pattern “release trains”.*

It’s a new year, and of course there’s a new Firefox! Let’s take a look at some of the goodies inside the latest update.

## ServiceWorkers and Web Push

ServiceWorkers and Web Push are two truly transformational web technologies, because they enable web pages and web applications to do things that were simply not possible before. [ServiceWorkers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) allow a website to register a script that can intercept navigation requests, cache assets and data offline, and run even when the webpage isn’t open! This allows for more responsive UIs, better offline support, and lays the groundwork for more application-grade experiences.

![A working test notification! Hooray!](../../assets/487dd2c59d27f0ab.png)


[Web Push](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) builds on top of ServiceWorkers and, with user consent, allows web content to receive push notificatons from a server and to trigger system notifications that can return a user to the page, even after they’ve closed the browser tab.

There’s a lot to say about each of these technologies- more than I can cover here. If you’re interested in learning more about ServiceWorkers and Web Push or want to start experimenting, here are some resources:

[Read more about Web Push in Firefox 44](https://hacks.mozilla.org/2016/01/web-push-arrives-in-firefox-44/)- View example code and demos in the Service Worker Cookbook
[ServiceWorker documentation on MDN](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers)


## Design Tools in Firefox

![Diagram of a submarine with Developer Tools labeled on it](../../assets/e661a6e3b1653f40.png)


We’re going to need a bigger boat. Firefox 44 puts an emphasis on designer productivity tools with a fantastic animation inspector to complement existing style tools. Climb aboard the [DevTools Challenger](http://devtoolschallenger.com/) to learn about these tools, and explore both the deep ocean as you learn how to inspect animations, live-edit keyframes, tweak CSS filters, and more.


## More DevTools Goodness

In addition to the aquatic wonders and animation tools, there are other great changes and additions to the [Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools).

### WebSocket Debugging

[WebSocket debugging](https://bugzilla.mozilla.org/show_bug.cgi?id=1203802) is now available as an API in the Developer Tools. While an official UI is under development, you can start debugging WebSockets today with a [purpose-built extension](https://addons.mozilla.org/en-US/firefox/addon/websocket-monitor/).

### Use Logged Object in the Web Console

![Assigning a logged object to a temporary variable using the Web Console](../../assets/81cdc484b35cafb9.png)


If you’d like to manipulate or more deeply inspect an object logged in the console, you can now assign it to a temporary variable via the context menu.

## Dive Deeper

There’s lots more to love for developers and users alike in Firefox 44- check out the [full release notes](https://www.mozilla.org/en-US/firefox/44.0/releasenotes/) or [view the list of developer-facing changes](https://developer.mozilla.org/en-US/Firefox/Releases/44). Keep on rocking the free Web!

## One comment

AxelFebruary 27th, 2016 at 04:46