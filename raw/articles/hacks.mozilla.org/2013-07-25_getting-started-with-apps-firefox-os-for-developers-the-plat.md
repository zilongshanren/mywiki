---
title: 'Getting started with apps – Firefox OS for developers: the platform HTML5
  deserves – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/07/getting-started-with-apps-firefox-os-for-developers-the-platform-html5-deserves/
author: Chris Heilmann
published: '2013-07-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the third instance of our “Firefox OS – the platform HTML5 deserves” video series ([part one](https://hacks.mozilla.org/2013/06/firefox-os-for-developers-the-platform-html5-deserves/) and [part two](https://hacks.mozilla.org/2013/07/app-discovery-firefox-os-for-developers-the-platform-html5-deserves/) have already been published here) we talk about tools available for building apps for Firefox OS.

![Firefox OS - be the future](../../assets/b0198161368b9b8c.png)


Check the short video featuring Chris Heilmann ([@codepo8](http://twitter.com/codepo8)) from Mozilla and Daniel Appelquist ([@torgo](http://twitter.com/torgo)) from [Telefónica Digital](http://blog.digital.telefonica.com)/ W3C talking about starting your first HTML5 app. You can [watch the video here](http://youtu.be/8dvQe2orzvo).

First things first: you don’t build apps for Firefox OS – you build HTML5 apps for the Web. Firefox OS enables you as a developer to access the hardware of the phone by means of [Web APIs](https://wiki.mozilla.org/WebAPI) – JavaScript APIs that are proposals to the standards bodies to give secure and simple access.

This means first and foremost that for web developers, nothing changes. There is no SDK for the web you need to download and install. You can use the editor and tool chain you are familiar with. This could be as simple as VI on the command line, or Eclipse as you are working with other languages than the web ones. Firefox OS doesn’t demand any fixed environment, much like the Web doesn’t. That said, there are efforts to create HTML5 tools out there and Mozilla is keeping a close eye on these efforts to see where and if partnering makes sense.

To get you started with building a Firefox OS app, you simply start with an HTML5 application in your browser. Whilst the first wave of Firefox OS devices have a resolution of 320 x 480 pixels, you should not fix your app to that size. Embracing the ubiquitous nature of the web, it seems prudent to use a responsive design approach. We’ve collected a lot of information on how to design a good HTML5 app on the [Firefox OS developer hub](https://marketplace.firefox.com/developers/).

One great feature of the Firefox Developer Tools is the responsive view mode. You can turn this one on by opening the developer tools and clicking the ![responsive mode](../../assets/0cdd032a0797241a.png)

![the responsive mode in the Firefox developer tools allows you to resize your app without resizing the browser](../../assets/bfb369c008cc2381.gif)


Firefox is not the only browser with great developer tools built in. Chrome, for example allows you to simulate touch events when you are not on a touch device. To enable this, go to the developer tools settings, click “Overrides” and check the “Enable touch events” checkbox. For some great tips on when to use touch and when to use click, check out this [video by Peter-Paul Koch](http://vimeopro.com/mirabeaunl/mobilism-2013/video/69018217) ([@ppk](http://twitter.com/ppk)).

If you want to test Firefox OS itself or how your app performs in it – including the install process – you can download the [Firefox OS simulator](https://addons.mozilla.org/en-US/firefox/addon/firefox-os-simulator/), a no-restart-required add-on for Firefox.

Once installed, you get a dashboard that allows you to manage your applications on your computer and start or stop the emulator:![firefox emulator dashboard](../../assets/2029014e3b09b9fb.png)


When you start the simulator, you get a clean instance of Firefox OS running on your computer in a window of the right dimensions. You

can try out the OS, install your apps and see what the experience is like. ![simulator](../../assets/eb25f4374e490765.png)


More detailed testing of the performance of your apps requires a Firefox OS device. If you have one of them, you can connect the phone via USB and send your app directly from the simulator to the phone.

![device connected](../../assets/f05cc3589e770e11.png)


The tooling space of HTML5 applications is one of the most discussed markets on the Web right now. We are confident that in the nearer future a lot of new, amazing tools will become available to make HTML5 app development easy and give developers the insights they need when they develop. For now, using the browsers’ developer tools and the Firefox OS sSimulator will get you 90% on the way.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## One comment

Cesar AntonAugust 5th, 2013 at 17:58