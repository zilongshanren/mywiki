---
title: Rormix – Discover Emerging Music Videos with Firefox OS – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2014/04/rormix-discover-emerging-music-videos-with-firefox-os/
author: Mark Wheeler
published: '2014-04-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Rormix](http://rormix.com/) is a platform for discovering emerging music videos. Music videos are tagged by genre and similar commercial artists, making it easy to discover new music videos.

The Rormix app was made using PhoneGap and released on [iOS](http://ror.mx/ios) and [Android](http://ror.mx/android). Development took just over a month from the first line of code, to the app submissions in the app stores. The [Firefox OS](https://marketplace.firefox.com/app/rormix/) port took one developer just one day!

![](../../assets/6ef13c3e320709c0.png)

![](../../assets/6f138c7119059360.png)

![](../../assets/a0c76681a0cb78a7.png)


Listed below are a few things we learnt along the way:

## What screen sizes am I developing for?

When you develop an open web app you can install it in the actual desktop browser, the Android Firefox browser or Firefox OS devices.

If you want to support all of them in one app, responsive designs are a must (you can also select just the platform you want to support). The [current crop of Firefox OS phones](http://www.mozilla.org/en-US/firefox/os/devices/) have a resolution of 320×480. They have a pixel density of 1 so no special graphics need to be produced.

## Back Button?

iOS devices don’t have a back button, Android devices have a hardware back button, so where does Firefox OS stand? It has a software back button that you can optionally hide or show when building the [manifest for the app](https://developer.mozilla.org/en-US/Apps/Build/Manifest#chrome). The back button can be hidden at the bottom of the screen however it can be hard to press.

I recommend that you build a back button into your app and hide the default one to make the app easier to navigate.

```
//jQuery example
$('.backbutton').click(function(){
history.go(-1);
});
```

## Stateful design

As a back button has a presence in Firefox OS you need to build a stateful application in order to go back in state when the user presses the back button.

A simple way to implement this is using one of the various JS frameworks that use fragment identifiers to load different states (e.g. [Sammy JS](http://sammyjs.org)).

```
//jQuery example
//Sammy app
var app;
$(function(){
app = Sammy(function() {
this.get('#/', function() {
//Load default content
});
this.get('#/trending', function() {
//Get trending content
});
this.get('#/fresh', function() {
//Get fresh content
});
});
});
//Load the default content on app load
app.run('#/');
//Go to fresh content
$('.freshbutton').click(function(){
app.setLocation('#/fresh');
});
```

## Creating a menu

The trick with making menus for Firefox OS is to use CSS3 transforms for speed, but also making them simple enough to limit the redraw cycle when the menu comes into play. Firefox OS phones have the same width in reference pixels as all iPhones (at the time of writing), and the same pixel height as iPhones previous to the iPhone 5, so if you have a design that works for iOS then you’re all set.

## Adding some Firefox OS flavour

There are a set of [design guidelines](http://www.mozilla.org/en-US/styleguide/products/firefox-os/) that give you an idea of the colour scheme etc of the Firefox OS platform. They also detail how to make the icon for your app, the fonts used etc.

![](../../assets/44bc435c49e1dda4.png)

![](../../assets/33aaeded4c6e9c63.png)

![](../../assets/c79b84c4d359757a.png)


## Submitting your app

When you have finished building your app you have a choice of how to submit it. You can [package it up](https://developer.mozilla.org/en-US/Apps/Publishing/Packaged_Apps) in a zip file:

zip -r package.zip *

You can send this zip to the [Marketplace](https://marketplace.firefox.com/developers/submit/) or you can [host it yourself](https://developer.mozilla.org/en-US/Marketplace/Publishing/Publish_options#Self-publishing_apps).

The other option is to simply [host the code](https://developer.mozilla.org/en-US/Marketplace/Publishing/Publish_options#Hosted_apps) as a web page (rather than zip it), and with a [little extra JS](https://developer.mozilla.org/en-US/Apps/Build/JavaScript_API#Installation_API) prompt the user to download the app to their phone.

## Aside: Using PhoneGap / Cordova and HTML5

Building web apps allows you to quickly and easily build cross platform apps. Even better, with responsive designs it can all be in one project. Advancing tools and workflows ([Sass](http://sass-lang.com) and [Yeoman](http://yeoman.io) for example) makes developing apps even easier.

PhoneGap / Cordova supports Firefox OS from [version 3.4](http://phonegap.com/blog/2014/03/04/phonegap-3-4-release/) (more information in [Building Cordova apps for Firefox OS](https://hacks.mozilla.org/2014/02/building-cordova-apps-for-firefox-os/)). The biggest advantage of using PhoneGap is that you only need to support a single codebase for all your apps. We all know some browsers have niggles, and PhoneGap has a built in merge mechanism that allows you to put platform specific code aside from the main code and it will merge them when building the app.

PhoneGap also has a [bunch of libraries](http://plugins.cordova.io) for accessing [native properties of the phone](http://docs.phonegap.com/en/3.4.0/cordova_plugins_pluginapis.md.html#Plugin%20APIs) (native dialogue boxes for example) and this code is the same across all platforms, minimising duplicate code.

The best thing about PhoneGap is the ability for you to create your own plugins, harnessing the power of mobile devices in a really easy way, effortlessly switching between JS and native mobile code.

Contact:

[@pixelcodeUK](https://twitter.com/pixelcodeUK)

## About
[
Mark Wheeler ](http://pixelcode.co.uk)

CTO at Rormix - Music worth watching

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.