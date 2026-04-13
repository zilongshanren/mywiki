---
title: HiDPI support, HTML5 notifications, Parallel JS, asm.js and more – Firefox
  Development Highlights – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/04/hidpi-support-html5-notifications-parallel-js-asm-js-and-more-firefox-development-highlights/
author: Robert Nyman
published: '2013-04-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Time for another look at the latest developments with Firefox. This is part of our [Bleeding Edge](https://hacks.mozilla.org/category/bleeding-edge/) and [Firefox Development Highlights](https://hacks.mozilla.org/category/firefox/firefox-development-highlights/) series, and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## HiDPI support

We’re happy to say that ico/icns with multiple images are now supported: the highest resolution icon is now used on HiDPI/Retina displays.

Favicon implementation is described in [bug 828508](https://bugzilla.mozilla.org/show_bug.cgi?id=828508) and ico/icns is described in [bug 419588](https://bugzilla.mozilla.org/show_bug.cgi?id=419588).

## Performance improvements/Snappy:

Numerous [performance improvements](http://taras.glek.net/blog/2013/03/25/snappy-number-53-faster-startup/) have been made, such as faster startup, better scrolling on touchpads and smoother animations.

The most important improvement, however, is probably multithreaded image decoder. The result should be faster page loads and tab switching. All the nitty-gritty detalis are described in [bug 716140](https://bugzilla.mozilla.org/show_bug.cgi?id=716140).

## HTML5

When it comes to the world of HTML5 & friends, we have some good additional support:

### <input type=”range”>

We now support the `<input type="range">`

element in forms. To style it, you can use the `::-moz-range-progress`

:

```
::-moz-range-progress {
background: #f00;
}
```

You can see this [<input type=”range”> demo in action on jsFiddle](http://jsfiddle.net/robnyman/YnnjF/).

### HTML5 notifications

HTML5 notifications have now been implemented. Basically, you ask for permission and then you can create a notification:

```
function authorizeNotification() {
Notification.requestPermission(function(perm) {
alert(perm);
});
}
function showNotification() {
var notification = new Notification("This is a title", {
dir: "auto",
lang: "",
body: "This is a notification body",
tag: "sometag",
});
}
```

See the [HTML5 notification demo in action on jsFiddle](http://jsfiddle.net/robnyman/TuJHx/).

### WebAudio API activated by default

WebAudio API has been activated by default in Firefox Nightly. Testers welcome, though there are still work to be done before it can be released.

## JavaScript

### Parallel JS

The first version of Parallel JS has landed for Firefox. A lot more details in the [Parallel JS Lands](http://smallcultfollowing.com/babysteps/blog/2013/03/20/parallel-js-lands/) article.

### asm.js

We’re happy to say that asm.js is now in Firefox, scheduled to be released in Firefox 22! Luke Wagner has written more about it in [asm.js in Firefox Nightly](https://blog.mozilla.org/luke/2013/03/21/asm-js-in-firefox-nightly/).

### ES6 Arrow function syntax

We now support the ES6 Arrow function syntax

```
let square = x => x*x;
console.log(square(3));
```

## CSS

### @supports activated by default

We plan on releasing this with Firefox 22. More about [@supports on MDN](https://developer.mozilla.org/en-US/docs/CSS/@supports).

### min-width and min-height ‘auto’ keyword

`min-width`

and `min-height 'auto'`

keyword is no more supported. It has been removed from CSS3 Flexbox. More about that in [bug 848539](https://bugzilla.mozilla.org/show_bug.cgi?id=848539).

### CSS Flexbox has been re-enabled

Happy to let you know that CSS Flexbox has been re-enabled by default in Firefox 22, which is currently in [Firefox Aurora](http://www.mozilla.org/en-US/firefox/aurora/)!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## About Jean-Yves Perrier

Jean-Yves is a program manager in the Developer Outreach team at Mozilla. Previous he was an MDN Technical Writer specialized in Web platform technologies (HTML, CSS, APIs), and for several years the MDN Content Lead.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 25 comments

thinsoldierApril 25th, 2013 at 14:10WulfTheSaxonApril 25th, 2013 at 19:18Daniel HolbertApril 25th, 2013 at 17:06Adam ReinekeApril 25th, 2013 at 22:14Robert Nyman [Editor]April 26th, 2013 at 01:41ScrewtapeApril 26th, 2013 at 00:41Robert Nyman [Editor]April 26th, 2013 at 01:41Walid DamounyApril 26th, 2013 at 02:23nemoMay 1st, 2013 at 12:19Walid DamounyMay 1st, 2013 at 16:43FabianApril 26th, 2013 at 10:53Robert Nyman [Editor]April 29th, 2013 at 05:27xsohApril 26th, 2013 at 21:32Robert Nyman [Editor]April 29th, 2013 at 05:26nemoMay 1st, 2013 at 12:22Robert Nyman [Editor]May 2nd, 2013 at 02:10nemoMay 2nd, 2013 at 07:29Robert Nyman [Editor]May 2nd, 2013 at 13:45HanushMay 1st, 2013 at 12:04Robert Nyman [Editor]May 2nd, 2013 at 02:12Mathew PorterMay 2nd, 2013 at 10:24Robert Nyman [Editor]May 2nd, 2013 at 13:39CyrilMay 2nd, 2013 at 22:38Robert Nyman [Editor]May 3rd, 2013 at 13:41KWiersoMay 16th, 2013 at 13:01