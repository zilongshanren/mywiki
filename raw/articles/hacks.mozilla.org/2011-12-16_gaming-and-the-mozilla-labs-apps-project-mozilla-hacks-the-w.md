---
title: Gaming and the Mozilla Labs Apps Project – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/12/gaming-and-the-mozilla-labs-apps-project/
author: Robin Hawkes
published: '2011-12-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In this post I give a quick overview of the Mozilla Labs Apps project and how it and the other technologies at Mozilla relate to gaming. We really are at a point where amazing games can be created on the Web with nothing but open technologies.*

A few days ago we launched the developer preview of the [Mozilla Labs Apps project](https://developer.mozilla.org/en/Apps), our vision of a distributed Web application platform. This apps project is directly related to our overall mission to better the Web, [as recently described](https://hacks.mozilla.org/2011/12/mozilla-labs-apps-preview/) by Ragavan Srinivasan:

As part of Mozilla’s mission to make the Web better we believe that apps should be available on any modern Web-connected device, operating system or browser, allowing billions of people worldwide to use and interact with apps.

Today, apps are tied to closed ecosystems. Apps also can’t be used across all devices; data within apps is silo-ed and inaccessible to other apps or Web services; and user choice is limited and undervalued.

In an open ecosystem, developers should have the ability to build apps using open Web technologies and resources. They should then be able to distribute and sell those apps with the reach, flexibility and choice that the Web provides.


It’s important to remember that although we often talk about apps as pieces of software that each serve a particular task, they can also be games. After all, if you pull away the story and graphics, a game is really no different to what you would normally consider as an application — it uses the same platform and programming languages, HTML and JavaScript in this case.

So how does the Mozilla Labs Apps project and the other technologies that we’re working on relate to open Web games? I hope to shed some light on this question in the brief overviews that follow.

Rest assured, Mozilla is very much focused on making the Web a better platform for open Web gaming.

## Identifying players with BrowserID

Just like how iOS has services like [OpenFeint](http://openfeint.com/) and the [Apple Game Center](http://www.apple.com/game-center/), games on the Web need open and reliable methods of identifying players. [BrowserID](https://browserid.org/) is one of our solutions to this problem. It allows players to log into your game using their existing email address, providing a password only once per browser session.

Implementing BrowserID within your game is a simple 3-step process. I advise you to [check out the documentation](https://github.com/mozilla/browserid/wiki/How-to-Use-BrowserID-on-Your-Site) about installation, where you’ll also find some fancy BrowserID buttons to show your players that you support distributed authentication. Right now BrowserID is provided via a JavaScript library. However in the near-future it will be built into Firefox for a seamless experience.

Identifying players in this way is just the first step in providing all sorts of functionality with your game, like friends lists, leader boards, chat, and multiplayer.

## Creating immersive gameplay with the Full Screen API

Something that prevents current games on the Web from feeling immersive is that they look like they’re just tiny boxes embedded into another website. Why do they feel like that? Well, because they *are* just tiny boxes embedded into other websites. The odd 5-minute puzzle game during your lunch hour might feel OK in a tiny box surrounded by browser UI and other distractions, but a first-person shooter or driving game certainly wouldn’t.

Fortunately, the [Full Screen API](https://developer.mozilla.org/en/DOM/Using_full-screen_mode) has arrived to solve this problem. It allows you to make any DOM element fill the player’s entire screen, something normally only considered for videos. Using this in a game can make the difference between 5 minutes of relative fun and hours of immersive delight.

Like most of the JavaScript APIs, it’s pretty easy to implement full-screen functionality in your game. All you need to do is call the `requestFullScreen`

method on the desired DOM element:

`var elem = document.getElementById("myGame"); if (elem.requestFullScreen) { elem.requestFullScreen(); } else if (elem.mozRequestFullScreen) { elem.mozRequestFullScreen(); } else if (elem.webkitRequestFullScreen) { elem.webkitRequestFullScreen(); } `


## Taming mouse input with the Mouse Lock API

An issue related to input in games is that of misbehaving cursors, where the mouse is used to rotate a player around a fixed point, like moving the viewpoint in a 3D first-person shooter, or rotating the player in a top-down 2D game.

In both of these situations, the mouse cursor is visible at all times, which is generally annoying and ruins the experience. However, the most debilitating problem is that when the mouse cursor leaves the browser window all movement stops. This same behaviour occurs in full-screen mode when the mouse cursor hits the edge of the screen. It’s a horribly simple problem for players that completely ruins the experience.

The good news is that the [Mouse Lock API](https://developer.mozilla.org/en/API/Mouse_Lock_API) has been created to solve this problem, and it [just landed in experimental builds of Firefox Nightly](http://hacks.mozilla.org/2011/12/paving-the-way-for-open-games-on-the-web-with-the-gamepad-and-mouse-lock-apis/). Its sole purpose is to tame the mouse by hiding the cursor and locking it in place so it doesn’t hit the edges of the screen. This means that instead of relying on `x`

and `y`

coordinate values for mouse position in related to the top-left corner of the browser, you instead rely on `x`

and `y`

distance values from the position that the mouse was locked to.

Using the Mouse Lock API is really just a case of calling the `navigator.pointer.lock`

method. However this must be done in full screen mode to work properly (and remember to use the experimental build of Firefox linked previously).

The [following example](http://humphd.github.com/mozilla-central/mouselock/) expands a `<div>`

element to full screen and locks the mouse in place at the same time:

`<script> function fullAndLock() { var div = document.getElementById("div"); document.addEventListener("mozfullscreenchange", function() { var pointer = navigator.pointer; if (document.mozFullScreen && document.mozFullScreenElement === div && !pointer.islocked()) { function onMouseLockSuccess() { console.log("Mouse successfully locked"); } function onMouseLockError() { console.log("Error locking mouse"); } pointer.lock(div, onMouseLockSuccess, onMouseLockError); } }, false); div.mozRequestFullScreen(); } </script> <button onclick="fullAndLock();">Mouse Lock</button> <div id="div">Element to receive mouse lock</div> `


Here is a quick video of the Mouse Lock API in action, with comparison to non-mouse lock game-play to see the improvement:

## Providing a console-like experience with the Gamepad API

Another input-related improvement that is coming to the Web is that of the [Gamepad API](https://wiki.mozilla.org/GamepadAPI). No longer are the keyboard and mouse the only options available for your players to engage with your game. The Gamepad API now allows for all sorts of gamepads to be accessed via JavaScript. This even includes some of the console controllers like those on the xBox 360 and Playstation 3 (with third-party drivers)!

Like the Mouse Lock API, the Gamepad API has [just landed in experimental builds of Firefox Nightly](http://hacks.mozilla.org/2011/12/paving-the-way-for-open-games-on-the-web-with-the-gamepad-and-mouse-lock-apis/) and it’s nice and simple to use. Coupled with the Full Screen API, gamepad support can really change the experience of your game from that of a game within a website to that of a desktop game or console.

To find out when a gamepad has been connected, you need only listen to the `MozGamepadConnected`

event on the `window`

object (remember to use the experimental build linked previously):

`<div id="gamepads"></div> <script> function gamepadConnected(e) { var gamepads = document.getElementById("gamepads"), gamepadId = e.gamepad.id; gamepads.innerHTML += " Gamepad Connected (id=" + gamepadId + ")"; } window.addEventListener("MozGamepadConnected", gamepadConnected, false); </script> `


Receiving updates about all the buttons and joysticks on a gamepad is also a case of listening for events, or you can manually poll the status of buttons and joysticks whenever you want. Check out the [Gamepad API documentation](https://wiki.mozilla.org/GamepadAPI) and the [input.js library](https://github.com/jbuck/input.js) for more information.

The video below shows the Gamepad API in action, controlling a player in the game [Rawkets](http://rawkets.com):

## Adding real-time multiplayer game-play with WebSockets

If you’re thinking of creating a multiplayer game then before now you would either have put up with the latency involved in constant AJAX requests, or you would have moved to Flash. Neither option is ideal. What’s cool is that since last year this is no longer the case, [WebSockets](https://developer.mozilla.org/en/WebSockets) have now arrived to allow for real-time *bi-directional* communication between the browser and a server.

But why is bi-directional real-time communication important for games? Well, this means that you can now literally *stream* data to and from a player’s browser in real time. One obvious benefit to this is that it saves bandwidth by no longer requiring constant AJAX requests to check for new data. Instead the WebSocket connection is left open and data is instantly pushed to the player or server as soon as it is needed. This is perfect for fast-paced games that require updates every few milliseconds. On top of this, the bi-directional nature of WebSockets means that data can be instantly sent both from the server to the player and from the player to the server *at the same time*.

[Using WebSockets](https://developer.mozilla.org/en/WebSockets/Writing_WebSocket_client_applications) is a case of connecting to the socket server by initialising the `WebSocket`

object:

`var mySocket = new WebSocket("http://www.example.com/socketserver",); `


From there you can send data using the `send`

method of the `WebSocket`

object:

`mySocket.send("Here's some text that the server is urgently awaiting!"); `


And you can receive data by listening for the `onmessage`

event on the `WebSocket`

object:

`mySocket.onmessage = function(e) { console.log(e.data); } `


A full code example for game communication would be too much for this post but you should definitely [check out the tutorial that that I made](http://rawkes.com/blog/2011/11/06/creating-a-real-time-multiplayer-game-with-websockets-and-node.js) a couple months ago. In it I detail exactly how to create a real-time multiplayer game using Node.js and WebSockets.

## Using games offline with local storage and the application cache

Creating games on the Web is all well and good, but what about if you want to play that game offline? Or, what if the player’s Internet connection drops out half way through an epic gaming session? Most open Web games today would at worst simply stop working as soon as an Internet connection fails, and at best they would stop sending data to your server and saving player data. When your player refreshes the page that the game is on, they’ll just see a blank page and all their hard work achieved while offline will have been lost. That probably won’t make your players very happy, and unhappy players are not ideal.

There [are a few solutions available](https://developer.mozilla.org/en/Apps/Using_apps_offline) today that can help solve these issues. The first is the [application cache](https://developer.mozilla.org/en/Using_Application_Cache), which allows you to use a cache manifest to declare particular assets (like HTML, CSS, images, and JavaScript) that you would like the browser to cache for offline use. Not only that, the browser uses the cached versions of the files when when online to speed up the loading process.

You can include a cache manifest within your game by using the `manifest`

attribute of the `<html>`

element:

`<html manifest="example.appcache"> <h1>Application Cache Example</h1> </html> `


Writing a cache manifest is straightforward and requires you to follow a simple format to declare the files that you want cached. For example, the manifest below looks for `/example/bar`

online and falls back to the locally-cached `example.html`

file if your player is offline or experiencing network issues:

`CACHE MANIFEST FALLBACK: example/bar/ example.html `


There is much more to cache manifest than this, so I advise you to [read the documentation](https://developer.mozilla.org/en/Using_Application_Cache) to discover it in detail.

Another technique you can use is to store a player’s game data locally and periodically sync it with the game server. Normally you wouldn’t be able to store enough data in the browser to achieve this (like with cookies) but with [Local Storage](https://developer.mozilla.org/en/DOM/Storage) and [IndexedDB](https://developer.mozilla.org/en/IndexedDB), you can now store many megabytes of data in a structured way.

You can also add functionality to your game so it is alerted when a player’s Internet connection goes offline. The [ navigator.onLine property](https://developer.mozilla.org/en/Online_and_offline_events) allows you to use JavaScript to see if your player is currently online or not. You can also use the

[to trigger automatic behaviour in your game when a change in connection occurs, like stopping all WebSockets communication and caching player data locally until the connection is back.](https://developer.mozilla.org/en/Online_and_offline_events)

`offline`

and `online`

events## Creating native OS applications with WebRT

One of the more profound aspects of the Mozilla Labs Apps project is the integration of a [Web run-time (WebRT)](https://developer.mozilla.org/en/Apps/Apps_architecture). This allows players to install your game [“natively” on their chosen operating system](https://developer.mozilla.org/en/Apps/Platform-specific_details) (Windows, Mac, and Android right now), with a launch icon just like standard OS applications.

WebRT also runs your game using an app-centric user agent (in contrast to browser-centric user agents like Firefox) and runs your game using a separate user profile and OS process to your player’s normal Firefox that they use for browsing.

The ability of WebRT to break away into another process and remove all the browser UI makes the experience for gaming that much sweeter. There’s something about having an icon in the dock on a Mac that launches your game in it’s own “native” window with no mention or feel that this is a browser.

As a developer this is slightly magical. It allows you to break free from a game being a glorified website, instead turning it into an application, an experience in its own right. Mark my words, this will be a turning point in the transition from 5-minute puzzle games on the Web to professional-grade games that have a console-like experience.

The great news is that enabling WebRT on your game is just a case of [creating an app manifest](https://developer.mozilla.org/en/Apps/Manifest) and calling the [ navigator.mozApps.install method](https://developer.mozilla.org/en/Apps/Apps_JavaScript_API/navigator.mozApps.install) through JavaScript.

This is an example app manifest from the Rawkets game:

`{ "name":"Rawkets", "developer": { "name":"Rob Hawkes", "url":"http://rawkes.com" }, "description":"Space shooter game.", "icons": { "16": "/style/img/icon-16.png", "48": "/style/img/icon-48.png", "128": "/style/img/icon-128.png" }, "launch_path": "/index.html", "installs_allowed_from": ["*"] } `


As you can see it’s a simple JSON structure. You would then need to pass that manifest file in the call to the `navigator.mozApps.install`

method:

`function installCallback(result) { // great - display a message, or redirect to a launch page } function errorCallback(result) { // whoops - result.code and result.message have details } navigator.mozApps.install( "http://rawkets.dev:8000/manifest.webapp", installCallback, errorCallback ) `


This is the most basic implementation possible and would result in a panel popping up in the player’s browser asking if they’d like to install your game and whether they’d like that installation to be a native app or not (like the screenshot above).

## Making money from your passion with the Mozilla Labs Apps project

Finally, the last thing about the apps project that I want to cover is that of making money from your game. Let’s be honest, if you can’t make a living from something then you’re going to have a hard time keeping it up for a long period of time.

For the Mozilla app marketplace [we are using PayPal as the payment provider](https://developer.mozilla.org/en/Apps/FAQs/Payments). All you need do is set a price on the store and the rest will happen automatically as people start paying for your game — you’ll start receiving money in your PayPal account.

In the future you’ll be able to provide your game on your own website or another store and charge for it there also. This means you’ll be able to use your own payment provider.

## Scratching the surface

These technologies are really just scratching the surface when it comes to creating games on the Web using open technologies. At Mozilla we’re working hard to bring you these APIs and services to help make the Web a better place for games. The year 2012 will be a game-changer, for sure (pun intended).

Keep an eye on this blog as we’ll be sure to post more updates and guides as our gaming technologies and the apps project mature.

In the meantime, here are a few of places to go for extra information on the Mozilla Labs Apps project and gaming at Mozilla:

[Mozilla Labs Apps project developer documentation](https://developer.mozilla.org/en/Apps)[Documentation on developing games with the apps project](https://developer.mozilla.org/en/Apps/Developing_game_apps)[Blog post about the Gamepad and Mouse Lock APIs](https://hacks.mozilla.org/2011/12/paving-the-way-for-open-games-on-the-web-with-the-gamepad-and-mouse-lock-apis/)[Wiki page about Mozilla’s Paladin team](https://wiki.mozilla.org/Paladin). These are the guys working on the Gamepad and Mouse Lock APIs, amongst other awesome things.

## About
[
Robin Hawkes ](http://rawkes.com)

Robin thrives on solving problems through code. He's a Digital Tinkerer, Head of Developer Relations at Pusher, former Evangelist at Mozilla, book author, and a Brit.

## 10 comments

Francois MAROTDecember 19th, 2011 at 05:54Rob HawkesDecember 19th, 2011 at 08:03Randell JesupDecember 19th, 2011 at 13:31sungDecember 20th, 2011 at 20:20Justin ScottDecember 22nd, 2011 at 04:19sungDecember 22nd, 2011 at 12:08peteDecember 22nd, 2011 at 09:39Rob HawkesDecember 22nd, 2011 at 10:00GabeDecember 23rd, 2011 at 08:34MikeMay 30th, 2012 at 23:03