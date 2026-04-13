---
title: Paving the way for open games on the Web with the Gamepad and Mouse Lock APIs
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/12/paving-the-way-for-open-games-on-the-web-with-the-gamepad-and-mouse-lock-apis/
author: Robin Hawkes
published: '2011-12-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In this post I’ll be introducing the Gamepad and Mouse Lock APIs, two additions to Firefox that are paving the way for high quality games on the Web.*



Update: The Gamepad API, Mouse Lock API, and Full Screen API are now all available within [a single experimental build of Firefox](http://people.mozilla.com/~tmielczarek/mouselock+gamepad/).

The Web is proving to be a valuable and capable platform for games, particularly those produced using open technologies baked into the browser. These HTML and JavaScript games are beginning to shine, all thanks to the amazing APIs and functionality that come with Firefox and other modern browsers.

The Gamepad and Mouse Lock APIs are just two of the new additions coming to Firefox that are going to help mature this platform. We’ll be posting more about them as they develop but let’s take a quick look at them today.

## Breaking free from the keyboard with the Gamepad API

The ability to control games with a gamepad is something that has only been available to consoles and desktop computer games, until today. You can now connect a gamepad to your computer via USB or bluetooth and immediately access it within Firefox using JavaScript, it’s that cool.

Accessing gamepads using JavaScript is massively valuable for games developers who want to break away from traditional keyboard and mouse input. Combined with the [Full Screen API](http://blog.pearce.org.nz/2011/11/firefoxs-html-full-screen-api-enabled.html) it can allow you to create a much more immersive experience that feels more like a console than a browser.

The Gamepad API is being worked on at Mozilla by [Ted Mielczarek and others from our Paladin team](https://wiki.mozilla.org/GamepadAPI).

### Use it today

You can use the Gamepad API today in a [custom build of Firefox](http://people.mozilla.com/~tmielczarek/mouselock+gamepad/), that also contains the Mouse Lock API (more details on that below). When you have installed the build you can then [use the demonstration file](https://bug604039.bugzilla.mozilla.org/attachment.cgi?id=565617) to test it out. The wiki page contains information about [implementing the API in your own project](https://wiki.mozilla.org/GamepadAPI).

I have put together a short video showing off the Gamepad API an action with an xBox 360 controller:

### More information

The Gamepad API has a [draft W3C specification](http://dvcs.w3.org/hg/webevents/raw-file/default/gamepad.html) edited by Scott Graham from Google and our very own Ted Mielczarek. Find out more about [our progress with the Gamepad API](https://wiki.mozilla.org/GamepadAPI) on the Mozilla wiki.

## Making the mouse behave with the Mouse Lock API

Until recently, it has been impossible to lock down the mouse cursor and contain movement within the browser. This has made it incredibly difficult for developers to implement games and visualisations that allow a player to look around in a large or 3D world. What would happen is the player would start looking around but would be prevented from looking when the mouse would go off the edge of the browser or hit the side of the monitor.

The Mouse Lock API solves this by hiding the cursor and locking it to the centre of the screen. When the API is enabled and the mouse is moved the developer is given details about the distance the mouse has travelled, rather than the coordinates of the mouse on the screen. These distance values allow infinite movement on the X and Y axis, letting the player to look around a 3D world without hitting any restrictions.

It is being worked on at Mozilla by [David Humphrey and his students at Seneca College](http://zenit.senecac.on.ca/wiki/index.php/Implementing_the_Mouse_Lock_API_in_Firefox) in Canada.

### Use it today

You can use the Mouse Lock API today in the same [custom build of Firefox](http://people.mozilla.com/~tmielczarek/mouselock+gamepad/) that contains the Gamepad API. When you have installed the build you can then [use the demonstration files](http://humphd.github.com/mozilla-central/mouselock/) to test it out.

David has also put together a short video showing off the Mouse Lock API in action:

### More information

The Mouse Lock API has a [draft W3C specification](http://dvcs.w3.org/hg/webevents/raw-file/default/mouse-lock.html) edited by Vincent Scheib from Google. Find out more about [our progress with the Mouse Lock API](https://bugzilla.mozilla.org/show_bug.cgi?id=633602) on Bugzilla. You can also check out David Humphrey’s series of posts on the [development of the Mouse Lock API](http://vocamus.net/dave/?p=1382).

## About
[
Robin Hawkes ](http://rawkes.com)

Robin thrives on solving problems through code. He's a Digital Tinkerer, Head of Developer Relations at Pusher, former Evangelist at Mozilla, book author, and a Brit.

## 10 comments

Andrei EichlerDecember 1st, 2011 at 10:17Jon BuckleyDecember 8th, 2011 at 14:44John HamminkDecember 11th, 2011 at 17:17Rob HawkesDecember 12th, 2011 at 13:43John HamminkDecember 12th, 2011 at 18:14Rob HawkesDecember 13th, 2011 at 02:27momendoDecember 14th, 2011 at 13:16Rob HawkesDecember 16th, 2011 at 10:32KATIE VETRANOJanuary 13th, 2012 at 17:19Rob HawkesJanuary 16th, 2012 at 04:52