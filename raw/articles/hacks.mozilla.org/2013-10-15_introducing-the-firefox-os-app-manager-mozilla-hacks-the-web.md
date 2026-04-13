---
title: Introducing the Firefox OS App Manager – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/10/introducing-the-firefox-os-app-manager/
author: Paulrouget Com
published: '2013-10-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Firefox OS App Manager is a new developer tool available in Firefox 26 that greatly improves the process of building and debugging Firefox OS apps, either in the Simulator or on a connected device. Based on the the Firefox OS Simulator add-on, it bridges the gap between existing Firefox Developer tools and the Firefox OS Simulator, allowing developers to fully debug and deploy their web apps to Firefox OS with ease.

![AppManager](../../assets/d89df3886df672fc.jpg)


Additional features made available in Firefox 26 are discussed in this [post](https://hacks.mozilla.org/2013/09/new-features-in-the-firefox-developer-tools-episode-26/).

## App Manager In Action

The App Manager replaces the current Simulator Dashboard and provides an integrated debug and deployment environment for your Firefox OS apps, by leveraging the existing Firefox Developer Tools. You can install hosted or packaged apps and debug them in the Simulator or with a connected device. The App Manager also provides additional information to the developer including the current Firefox OS version of a connected device, the ability to take screenshots, a list of all currently installed apps and a list of all the APIs and what privilege level is required to use each. Here is [a screencast of the App Manager](http://www.youtube.com/embed/z1Bxg1UJVf0) showing off some of the features available for Firefox OS Development.

In addition to debugging your own apps, the App Manager also provides the ability to update, start, stop and debug system level apps. Debugging an app using the Developer Tools is similar to debugging any other Web app and changes made in the Tools are automatically reflected real-time to the app either in the Simulator or the connected device. You can use the Console to see warnings and errors within the app, the Inspector to view and modify the currently loaded HTML and CSS, or debug your JavaScript using the Debugger.

![Developer Tools](../../assets/c2d4c536b5374cfa.jpg)


For more information about using the Developer Tools be sure to check out the [Developer Tools series](https://hacks.mozilla.org/2013/09/reintroducing-the-firefox-developer-tools-part-1-the-web-console-and-the-javascript-debugger/) on this blog and for the most up to date information take a look at the [Developer Tools](https://developer.mozilla.org/en-US/docs/tools) section of MDN.

## Getting Started with the App Manager

To get started using the App Manager take a look at the MDN Documentation on [Using the The App Manager](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Using_the_App_Manager). Do keep in mind that to see what is shown above you need:

- Firefox 26 or later
- Firefox OS 1.2 or later
- at least the 1.2 version of the Firefox OS Simulator
- either the ADB SDK or the ADB Helper Add-on

Details for these are described in the above MDN link.

Mozilla is very interested in your feedback as that is the best way to make useful tools, so please be sure to reach out to us through [Bugzilla](http://is.gd/ZPaPDN) or in the comments and let us know what you think about the new App Manager.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 19 comments

Peter RukavinaOctober 15th, 2013 at 10:01Paul RougetOctober 15th, 2013 at 10:08Luigi MaselliOctober 15th, 2013 at 12:02Robert Nyman [Editor]October 16th, 2013 at 00:58LorenzoOctober 15th, 2013 at 12:07Robert Nyman [Editor]October 16th, 2013 at 00:53Brett ZamirOctober 15th, 2013 at 14:53Robert Nyman [Editor]October 16th, 2013 at 00:53RenaOctober 15th, 2013 at 16:09Robert Nyman [Editor]October 16th, 2013 at 00:54Ken SaundersOctober 16th, 2013 at 09:26Myk MelezOctober 17th, 2013 at 09:28Robert Nyman [Editor]October 18th, 2013 at 12:19Michael GreenwoodOctober 19th, 2013 at 16:46WolfOctober 21st, 2013 at 03:54Jason WeathersbyOctober 21st, 2013 at 08:27Gabriele VidaliOctober 22nd, 2013 at 13:09Jesus Israel Perales MartinezNovember 5th, 2013 at 10:33Robert Nyman [Editor]November 5th, 2013 at 10:46