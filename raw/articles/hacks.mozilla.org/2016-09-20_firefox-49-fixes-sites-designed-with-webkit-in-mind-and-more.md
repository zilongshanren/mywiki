---
title: Firefox 49 fixes sites designed with WebKit in mind, and more – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2016/09/firefox-49-fixes-sites-designed-with-webkit-in-mind-and-more/
author: Mike Taylor
published: '2016-09-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Several recent articles on the Hacks blog explain [why web developers should care about cross-browser compatibility](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/) and [how great web developers achieve it](https://hacks.mozilla.org/category/a-web-for-everyone-interviews/). Web developers have a critical role in making the web work for everyone. And so do browser makers. As of today we’re introducing a number of [compatibility](https://developer.mozilla.org/en-US/Firefox/Releases/49#Compatibility) features to the Gecko rendering engine, bringing us up to date with the [WHATWG Compatibility Standard](https://compat.spec.whatwg.org/).

Some notable changes in this release include support for several `-webkit-`

prefixes and WebKit-specific interfaces. These platform features are non-standard, vendor-specific, and quite prevalent.

Non-standard, incompatible CSS breaks websites for user agents designed around standards. When a browser that doesn’t support `-webkit-`

prefixes (such as Firefox 48 and below) visits one of these sites, the web looks broken. This will be the case until those sites update their CSS. That’s why Firefox 49 includes the following changes to accommodate WebKit-specific content:

interface support`WebKitCSSMatrix()`

`-webkit-gradient()`

support`-webkit-`

prefix property mappings to their standard equivalents.- Mappings from some
`-webkit-`

prefixed (old) flexbox props to`-moz-`

prefixed flexbox props. - Support for the following CSS properties that don’t yet have an unprefixed equivalent:
`-webkit-text-fill-color`

`-webkit-text-stroke-color`

`-webkit-text-stroke-width`

`-webkit-text-stroke`


(in)Frequently Asked Questions (iFAQ):

**Q.** So, what does this mean for me?

**A.** As a user, improved compatibility with sites that were designed for WebKit browsers only, especially on mobile.

![okcupid](../../assets/b1f961e4a7fd3725.png)


As a developer, you might want to go back and add unprefixed equivalents to your `-webkit-`

only CSS so we can remove these from the web platform one day in the future (theoretically). Pro Tip: Unprefixed properties always come last.

**Q.** Did you just break my site?

**A.** We hope not! But you can toggle this for testing with the following preference:

`about:config?filter=layout.css.prefixes.webkit`


If there’s a difference (for the worse!), please report bugs to [bugzilla.mozilla.org](https://bugzilla.mozilla.org) and cc [mitaylor@mozilla.com](mailto:mitaylor@mozilla.com), or report them on [webcompat.com](https://webcompat.com).

**Q.** Should I only use -webkit- prefixes from now on?

**A.** No, that’s unnecessary and inadvisable. Keep using web standards and keep testing in multiple browsers. If you must use -webkit- prefixes (and there are fewer reasons to do so than ever before), make sure they’re above the unprefixed property in your CSS.

*Full disclosure: Mike edits the Compatibility Standard, but there’s work to be done if you’d like to contribute!*

## About
[
Mike Taylor ](https://miketaylr.com)

Mike works at Mozilla as a Web Compatibility Engineer from Austin, TX.

## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.

## 32 comments

anonSeptember 20th, 2016 at 14:58mitaylor@mozilla.comSeptember 20th, 2016 at 16:57LukeSeptember 20th, 2016 at 20:38mitaylor@mozilla.comSeptember 21st, 2016 at 10:20Anand KumriaSeptember 20th, 2016 at 17:25Karl DubostSeptember 22nd, 2016 at 13:50undefinedSeptember 20th, 2016 at 22:09mitaylor@mozilla.comSeptember 21st, 2016 at 10:29Karl DubostSeptember 22nd, 2016 at 13:58gnzSeptember 20th, 2016 at 23:56mitaylor@mozilla.comSeptember 21st, 2016 at 10:26Maxime ThiersSeptember 21st, 2016 at 12:53mitaylor@mozilla.comSeptember 22nd, 2016 at 09:24nevermindSeptember 22nd, 2016 at 15:09mitaylor@mozilla.comSeptember 22nd, 2016 at 15:38Karl DubostSeptember 22nd, 2016 at 16:35JakoDSeptember 25th, 2016 at 01:58Šime VidasSeptember 21st, 2016 at 00:31Brian LeanySeptember 22nd, 2016 at 06:49mitaylor@mozilla.comSeptember 22nd, 2016 at 07:19waltSeptember 24th, 2016 at 16:35Dan CallahanSeptember 26th, 2016 at 09:17Justin CrawfordSeptember 26th, 2016 at 09:29Andy GongeaSeptember 25th, 2016 at 01:17Firefox userSeptember 25th, 2016 at 17:19Nicolas ChevobbeSeptember 26th, 2016 at 03:19Justin CrawfordSeptember 26th, 2016 at 09:27Daniel HolbertSeptember 26th, 2016 at 14:59JBSeptember 26th, 2016 at 08:58Jan-Peter HolmströmSeptember 26th, 2016 at 13:30mitaylor@mozilla.comSeptember 26th, 2016 at 14:42JohnOctober 6th, 2016 at 04:19