---
title: Firefox OS Simulator 4.0 released – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/firefox-os-simulator-4-0-released/
author: Angelina Fabbro
published: '2013-07-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s a good day for Firefox OS developers as we are releasing version 4.0 of the Firefox OS Simulator to the masses. In particular, this release is a boon for those developers that want to make money using their app in the Marketplace.

## What’s New in 4.0

![4.0 Updated Simulator Dashboard](../../assets/e8d9475ea5adf920.jpg)


*An overview shot of the revised Dashboard*

### New Connect Button

There is a new ‘Connect’ button for each app that opens a developer toolbox connected to that specific app. This means that you won’t have to search through messages in the Console or filter through scripts in the Debugger in order to find information specific to your app.

### Testing Receipts for Paid Apps

There is now a dropdown menu in each app’s dashboard where you can select a receipt type. The simulator add-on will then download a test receipt from a Marketplace receipt service and reinstall the app using it. This way you can test receipt verification with the various types of receipts that you may require – valid, invalid, and refunded.

![4.0 Updated Simulator Dashboard Buttons](../../assets/54bf2d829a903172.jpg)


*The new Connect button, Refresh Button, and Receipts drop-down*

### Remote CSS Styling

If you connect to an app while using a Nightly or Aurora build of Firefox, there is a Style Editor tool you can use to edit the style sheets for your app. Changes are applied instantaneously.

![4.0 Updated Simulator Live Style Editing](../../assets/f22bc16e85fc4d61.jpg)


*Live editing the Firefox OS Boilerplate app to have a less than charming red background*

### Simulated Touch Events

Gaia’s touch events simulation has been integrated such that interacting with the Simulator using a mouse now generates real touch events. This fixes a myriad of issues in core Gaia apps that assume touch interactions. It also means you can test third party apps that rely on touch events without needing to fall back to mouse events.

### Hidden Feature: Shift-Ctrl/Cmd-R

When using the keyboard shortcut Ctrl-R (Cmd-R on Mac) to refresh an app, if you also hold down the Shift key, then the Simulator will clear persistent data such as AppCache, localStorage, sessionStorage, and IndexedDB while refreshing the app.

## Check Out The Simulator Walkthrough

Still want to get into grittier details? Check out [the simulator walkthrough](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator/Simulator_Walkthrough) to get a deep dive into the details of the Simulator, and the MDN documentation [here](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator).

## Download and Install the Simulator

You can [install or update the Simulator](https://addons.mozilla.org/en-US/firefox/addon/firefox-os-simulator/) from the add-ons website.

## Bugs? Feedback?

Leave general feedback in the comments below, we’re listening! If you encounter a bug we would be grateful if you could [file it here](https://github.com/mozilla/r2d2b2g/issues).

## About
[
Angelina Fabbro ](http://realityhacking.net)

I'm a developer from Vancouver, BC Canada working at Mozilla as a Technical Evangelist and developer advocate for Firefox OS. I love JavaScript, web components, Node.js, mobile app development, and this cool place I hang out a lot called the world wide web. Oh, and let's not forget Firefox OS. In my spare time I take singing lessons, play Magic: The Gathering, teach people to program, and collaborate with scientists for better programmer-scientist engagement.

## 8 comments

Patrick H. LaukeJuly 11th, 2013 at 15:30Nick DesaulniersJuly 11th, 2013 at 15:53SteveJuly 11th, 2013 at 18:17Robert Nyman [Editor]July 12th, 2013 at 00:24SteveJuly 12th, 2013 at 03:20SteveJuly 12th, 2013 at 03:22Robert Nyman [Editor]July 12th, 2013 at 05:41RavensunJuly 12th, 2013 at 05:00