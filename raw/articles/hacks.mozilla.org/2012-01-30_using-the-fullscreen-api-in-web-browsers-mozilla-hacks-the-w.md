---
title: Using the Fullscreen API in web browsers – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/01/using-the-fullscreen-api-in-web-browsers/
author: Robert Nyman
published: '2012-01-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One thing which has been very important when it comes to creating special end user experiences have been the ability to show something fullscreen, effectively hiding all the other content etc.


Remember when web sites gave you instructions how to configure your web browser with hiding toolbars and more, just to get a slightly better user experience? Or maybe it’s just me… :-)

Either way, some time ago we got fullscreen support in web browsers where the user could choose to view the current web site in fullscreen. That’s all good and well, but as an extension to that, as web developers we want to be able to trigger that. Either for the entire web site or just a specific element.

And now we can!

## Requesting fullscreen

We now have access to a method called `requestFullScreen`

, so far implemented in Firefox, Google Chrome, Safari and Internet Explorer. Therefore, to make it work at the moment, we need this code:



Please note that the [Fullscreen standard in the W3C specification](http://dvcs.w3.org/hg/fullscreen/raw-file/tip/Overview.html) uses a lowercase ‘s’ in all methods, whereas Firefox, Google Chrome and Safari use an uppercase one.

What the code above does is just getting a reference to the documentElement and request for it to be displayed fullscreen. Naturally, you could also make just a certain element fullscreen, for instance, a video, with the same method called for the element you wish.

## Cancelling fullscreen

If you want to cancel the fullscreen state, you need to call it on the document element:



Note here that there have been differences in this naming, and in some implementations it’s about exiting the state, in others cancelling it.

## Detecting fullscreen state change

The user could, for instance, exit fullscreen, something that might be good for you to know. For that we have a `fullscreenchange`

event, that you can apply both to the element that requested fullscreen, but also to the document. Then we just detect the fullscreen state and take act accordingly, like this:



document.addEventListener("mozfullscreenchange", function () {

fullscreenState.innerHTML = (document.mozFullScreen)? "" : "not ";

}, false);

document.addEventListener("webkitfullscreenchange", function () {

fullscreenState.innerHTML = (document.webkitIsFullScreen)? "" : "not ";

}, false);

document.addEventListener("msfullscreenchange", function () {

fullscreenState.innerHTML = (document.msFullscreenElement)? "" : "not ";

}, false);

## Styling fullscreen

In CSS, we get a number of pseudo-classes for styling fullscreen elements. The most reliable one is for full-screen and automatically gets triggered when the document/element is in fullscreen mode:



html:-webkit-full-screen {

background: red;

}

html:-ms-fullscreen {

background: red;

width: 100%; /* needed to center contents in IE */

}

html:fullscreen {

background: red;

}

Notice here that the W3C approach doesn’t use a hyphen between the word ‘full’ and the word ‘screen’.

It should also be added that Firefox is the only web browser that applies a width and height of 100% to the element that is requesting fullscreen, since we believe that is the desired behavior. This can of course be overridden with the above CSS.

## Full screen with key input

For security reasons, most keyboard inputs have been blocked in the fullscreen mode. However, in Google Chrome you can request keyboard support by calling the method with a flag:

`docElm.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);`


This does not work in Safari, and the method won’t be called.

With Firefox, we are discussing and looking into various ways of how we we could add keyboard input support without jeopardizing the end user’s security. One suggestion, that no one has implemented yet, is the `requestFullscreenWithKeys`

method, which in turn would trigger certain notifications for the user.

## Web browser support

This feature is currently available in [Firefox beta](http://www.mozilla.org/firefox/beta/), but it’s due to land in the official release of Firefox, version 10, tomorrow! It has also been available in Google Chrome since version 15, Safari since 5.1 and Internet Explorer since version 11.

## Play with fullscreen!

I have a [Fullscreen API demo](http://robnyman.github.com/fullscreen/) available for you to play with, and all the code is available in the [Fullscreen repository on GitHub](https://github.com/robnyman/robnyman.github.com/tree/master/fullscreen).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 92 comments

Rodrigo AyalaJanuary 30th, 2012 at 10:57Robert NymanJanuary 30th, 2012 at 10:59JamesJanuary 30th, 2012 at 11:23Robert NymanJanuary 31st, 2012 at 02:41marcusklaasJanuary 30th, 2012 at 11:39marcusklaasJanuary 30th, 2012 at 13:44Robert NymanJanuary 31st, 2012 at 02:42André LuísJanuary 30th, 2012 at 15:00Robert NymanJanuary 31st, 2012 at 02:42Chris PearceJanuary 30th, 2012 at 18:17Oliver CaldwellJanuary 31st, 2012 at 08:19Robert NymanJanuary 31st, 2012 at 09:53John DyerJanuary 31st, 2012 at 15:15Robert NymanFebruary 1st, 2012 at 06:28Joe ShelbyFebruary 2nd, 2012 at 20:22Robert NymanFebruary 3rd, 2012 at 01:20krisFebruary 9th, 2012 at 04:53John DyerFebruary 9th, 2012 at 06:58Robert NymanFebruary 9th, 2012 at 12:1640kgFebruary 19th, 2012 at 23:16Robert NymanFebruary 20th, 2012 at 01:4340kgFebruary 20th, 2012 at 18:16Robert NymanFebruary 21st, 2012 at 00:20TobyMarch 8th, 2012 at 10:09Chris PearceMarch 8th, 2012 at 14:52Robert NymanMarch 9th, 2012 at 00:51TobyMarch 12th, 2012 at 07:10Robert NymanMarch 12th, 2012 at 13:40cpearceFebruary 21st, 2012 at 13:58Robert NymanFebruary 22nd, 2012 at 01:1040kgFebruary 22nd, 2012 at 02:24Robert NymanFebruary 22nd, 2012 at 02:26Front Row TicketsFebruary 28th, 2012 at 08:41Robert NymanFebruary 28th, 2012 at 08:55Gustav EvertssonMarch 5th, 2012 at 23:47Robert NymanMarch 6th, 2012 at 01:01Gustav EvertssonMarch 6th, 2012 at 05:51Robert NymanMarch 6th, 2012 at 05:53Neel MehtaMarch 11th, 2012 at 17:52Chris PearceMarch 11th, 2012 at 18:02Robert NymanMarch 12th, 2012 at 13:40Sindre SorhusApril 22nd, 2012 at 07:16Robert NymanApril 24th, 2012 at 15:03NikhilApril 24th, 2012 at 00:52Robert NymanApril 24th, 2012 at 15:05NikhilApril 24th, 2012 at 22:16SazzadApril 27th, 2012 at 06:51Robert NymanApril 29th, 2012 at 08:38SazzadApril 29th, 2012 at 22:50Robert NymanMay 8th, 2012 at 05:50sreeMay 21st, 2012 at 04:13Jean-Yves PerrierMay 21st, 2012 at 23:59DionMay 23rd, 2012 at 06:07Robert NymanMay 23rd, 2012 at 07:09Chris PearceMay 23rd, 2012 at 14:24Kos KorolevMay 29th, 2012 at 04:47Robert NymanMay 29th, 2012 at 05:08RyanJune 22nd, 2012 at 19:26Robert NymanJune 25th, 2012 at 06:35jinzhouwangJuly 22nd, 2012 at 07:49Robert NymanJuly 31st, 2012 at 12:52Robert NymanAugust 3rd, 2012 at 01:29gustavoJuly 31st, 2012 at 13:51gustavoJuly 31st, 2012 at 13:53Robert NymanJuly 31st, 2012 at 14:00JuniorDeveloperSeptember 26th, 2012 at 04:07JuniorDeveloperSeptember 26th, 2012 at 04:08JuniorDeveloperSeptember 26th, 2012 at 05:03Robert NymanSeptember 26th, 2012 at 05:35Balsey Dean De Witt, Jr.September 29th, 2012 at 19:52Robert NymanOctober 1st, 2012 at 03:36BalduinOctober 10th, 2012 at 15:06Robert NymanOctober 11th, 2012 at 03:50StevenNovember 8th, 2012 at 17:50Robert NymanNovember 9th, 2012 at 14:51Chris PearceNovember 9th, 2012 at 23:08StevenNovember 11th, 2012 at 18:35Gaurav MNovember 27th, 2012 at 01:31RiccardoDecember 4th, 2012 at 03:18RiccardoDecember 4th, 2012 at 03:24Robert NymanDecember 5th, 2012 at 02:51RiccardoDecember 5th, 2012 at 02:59ganeshDecember 30th, 2012 at 06:20Robert NymanDecember 30th, 2012 at 13:15ganeshDecember 31st, 2012 at 01:46Robert NymanJanuary 1st, 2013 at 22:58EvyatarJanuary 17th, 2013 at 12:20Robert NymanJanuary 18th, 2013 at 07:44EvyatarJanuary 18th, 2013 at 12:47Robert NymanJanuary 19th, 2013 at 11:53Blue MoonApril 2nd, 2013 at 12:08Robert Nyman [Editor]April 3rd, 2013 at 08:12