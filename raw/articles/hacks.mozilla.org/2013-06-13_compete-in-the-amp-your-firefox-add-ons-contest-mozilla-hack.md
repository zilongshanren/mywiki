---
title: Compete in the "Amp Your Firefox" Add-ons Contest – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/06/compete-in-the-amp-your-firefox-add-ons-contest/
author: Amy Tsay
published: '2013-06-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

People love their add-ons—85% of Firefox users have them installed, and there have been over [3 billion downloads](https://blog.mozilla.org/blog/2012/07/26/firefox-add-ons-cross-more-than-3-billion-downloads/) since they revolutionized browsing in 2004. There are add-ons for almost everything under the sun: [fun](https://addons.mozilla.org/en-US/firefox/addon/puzzle/), [productivity](https://addons.mozilla.org/en-US/firefox/addon/leechblock/), [personalization](http://www.mozilla.org/en-US/firefox/customize/), even for [making tea](https://addons.mozilla.org/en-US/firefox/addon/tea-timer/). **Between June 13 – July 18, 2013**, we challenge you to delight these fans by creating or updating add-ons that amp up their Firefox.

We’re also challenging you on the mobile front—with more than 10 million people using [Firefox for Android](http://www.mozilla.org/en-US/firefox/fx/#mobile), this is your chance to take the fun and personalization of add-ons to a fast-growing and passionate fan base.

A panel of [judges](https://blog.mozilla.org/addons/amp-your-firefox-judges) will pick the best add-on from each prize [category](https://blog.mozilla.org/addons/amp-your-firefox-winner-selection), and the community will choose which category winner is the best overall add-on. Category winners will receive [Android tablets](https://blog.mozilla.org/addons/amp-your-firefox-prizes/), and the Best Overall winner will receive an 11-inch [Macbook Air](https://blog.mozilla.org/addons/amp-your-firefox-prizes/). All participants whose entry is approved (fully reviewed) for AMO will receive “Amp Your Firefox” [t-shirts](http://blog.mozilla.org/addons/files/2013/05/Amp_Up_tshirt_concept.jpg)! The winning add-ons will also get tons of exposure on AMO and other Mozilla properties.

## The Categories

### Best Mobile Add-on

Create add-ons that take Firefox for Android to the next level for over 10 million users by improving readability, enhancing the web experience across devices, and rounding out browsing features—[get creative](https://developer.mozilla.org/docs/Extensions/Mobile)!

### Best Mobile Add-on Port

If you’ve created an add-on for desktop and think it would be great for a mobile audience, [port it over](https://developer.mozilla.org/docs/Extensions/Mobile) to Firefox for Android!

### Best Game Add-on

It takes creativity and imagination to make a great game add-on like [Cheevos](https://addons.mozilla.org/firefox/addon/cheevos/) or [Destroy the Web](https://addons.mozilla.org/firefox/addon/destroy-the-web/)—are you up for taking the challenge?

### Best Complete Theme

[Complete themes](https://addons.mozilla.org/firefox/complete-themes/) can dramatically change the look of your Firefox—everything from buttons, window frames, tabs, and menus can be customized—the sky’s the limit. Create complete themes that are both aesthetically pleasing and transform the appearance of Firefox.

### Best Updated Add-on

If you’ve created an add-on and want to freshen it up by adding new features, making it restartless, or porting it to the [SDK](https://addons.mozilla.org/developers/builder), this is the category for you.

## Mobile Next!

One of the key categories we’re excited about for this competition is Mobile. Firefox for Android has done incredibly well in terms of user uptake and reviews in the Play marketplace, and the Android and Jetpack teams have both been working hard to make developing Add-ons for Mobile Firefox as easy as possible. Having said that, developing mobile add-ons is different enough that we thought we’d call out some of the highlights.

### NativeWindow & BrowserApp

NativeWindow and BrowserApp are privileged JavaScript APIs that allow developers to add their own custom functionality to the Native Java UI that is used on Firefox for Android instead of XUL. BrowserApp provides add-on developers the ability to interact with mobile browser tabs. NativeWindow allows developers to add menu items to the main and context menus, and to trigger native notifications.

Mark Finkle has created a [handy github repo](https://github.com/mfinkle/skeleton-addon-fxandroid/blob/master/bootstrap.js) that includes all of the boilerplate code you’ll need to get started. Using this restartless add-on skeleton as the basis for your work, NativeWindow and BrowserApp are easy to access as properties off of the window object:

```
// show a toast immediately
aWindow.NativeWindow.toast.show("Showing you a toast", "short");
// add a menu item that shows a toast when clicked
let menuId = aWindow.NativeWindow.menu.add(“Hello!”, icon, function() {
aWindow.NativeWindow.toast.show("I ran the callback!", "short");
});
```

### Jetpack – mobile ready

If you’re more comfortable with the Add-on SDK, I’m happy to report that the Jetpack team has done a lot of work to support mobile development. Most ( but not all ) Jetpack APIs work on Mobile, and the cfx command-line tool has been enhanced to be able to easily push your add-on onto the device for testing.

It is relatively simple to use NativeWindow from a Jetpack-based add-on:

```
// get the most recent window
const utils = require('api-utils/window/utils');
const recent = utils.getMostRecentBrowserWindow();
// show a toast notification
recent.NativeWindow.toast.show(opts.message, duration);
// listen for tabs events
let tabs = require('tabs');
tabs.on('ready', function(tab) {
console.log(recent.BrowserApp.selectedTab.id, tabs.activeTab.id);
});
```

### Caveats

Mobile phones present unique challenges for web browsers like Firefox mobile, so there are some very real limitations on what you can do with extensions as compared to desktop Firefox:

- Add-on Builder does not support packaging or running extensions on a phone
- Firefox for Android does not support XUL overlays
- not all of the Add-on SDK’s modules are compatible with Firefox for Android, please consult this
[compatibility guide](https://addons.mozilla.org/en-US/developers/docs/sdk/latest/dev-guide/tutorials/mobile.html#modules-compatibility)for more information.

For even more detail on using the NativeWindow api and Jetpack for hacking on mobile extensions, see [the Jetpack, Fennec and NativeWindow blog post in the Mozilla Add-ons blog](https://blog.mozilla.org/addons/2013/06/13/jetpack-fennec-and-nativewindow/).

## Get going!

- See complete
[contest details](https://blog.mozilla.org/addons/amp-your-firefox/)on the AMO blog - See tutorials, articles, and connect with add-on developers in the
[Developer Community](https://developer.mozilla.org/en-US/addons)and[Developer Hub](https://addons.mozilla.org/en-US/developers/) - See articles on
[developing extensions for Firefox on Android](https://developer.mozilla.org/docs/Extensions/Mobile)

Have fun, and good luck!

## About Amy Tsay

Lead for Firefox Add-ons at Mozilla.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 8 comments

DanielJune 15th, 2013 at 09:41Robert Nyman [Editor]June 17th, 2013 at 01:47Pikadude No. 1June 15th, 2013 at 21:21Amy TsayJune 17th, 2013 at 09:53Pikadude No. 1June 17th, 2013 at 14:56pdJune 26th, 2013 at 06:07Robert Nyman [Editor]June 26th, 2013 at 09:27pdJune 26th, 2013 at 11:12