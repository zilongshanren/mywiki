---
title: Firefox Add-on Enables Web Development Across Browsers and Devices – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/09/firefox-tools-adapter/
author: Dave Camp
published: '2014-09-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Developing across multiple browsers and devices is the main issue developers have when building applications. Wouldn’t it be great to debug your app across desktop, Android and iOS with one tool? We believe the Web is powerful enough to offer a Mobile Web development solution that meets these needs!

Enter an experimental Firefox add-on called the Firefox Tools Adaptor that connects the Firefox Developer Tools to other major browser engines. This add-on is taking the awesome tools we’ve built to debug [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS) and [Firefox on Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox&hl=en) to the other major mobile browsers starting with Chrome on Android and Safari on iOS. So far these tools include our Inspector, Debugger and Console.

Nothing can replace on-device testing. But developer tools on devices have been cumbersome and vendor-specific. Cross-platform development involved learning and switching between all the different browsers developer tools.

This add-on allows you to use your desktop environment to work on several small screen devices without using up precious screen space. You simply use the device and find out what is going wrong on your computer – regardless of platform and browser engine on the device.

**How the Add-on Works**

## Now Try it Out

This project is still in the early stages, but we put together a preview for developers who are curious or want to contribute. All it takes is the latest copy of [Firefox Nightly](http://nightly.mozilla.org/) and the add-on. Follow the [Firefox Tools Adapter instructions](https://developer.mozilla.org/en-US/docs/Tools/Firefox_Tools_Adapter) to get started.

This preview works with Chrome 37 on Android, currently available as Chrome Beta, and Safari on iOS. Some parts work pretty well, some parts need some work. Give it a try and let us know what you think!

## So What’s Under the Hood?

This add-on is a new implementation of the Firefox Developer Tools Protocol. Rather than interfacing directly with content, it speaks to the remote debugging protocol surfaced by Chrome and iOS. This implementation is hosted inside the Firefox process, and used internally by the Firefox Developer Tools.

## When Will It Be Ready?

What we’re showing today is an early preview release. We’ll be actively developing it in the coming months, directed in large part by your feedback. We’ll keep you posted on new updates when they happen!

## How to Contribute

The [GitHub project page](http://github.com/campd/fxdt-adapters) has instructions for getting involved with the code. Your feedback is also helpful: Talk to us on Twitter at [@FirefoxDevTools](http://twitter.com/FirefoxDevTools), [GitHub issues](http://github.com/campd/fxdt-adapters/issues) or [UserVoice](http://mzl.la/devtools).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 28 comments

Chris HSeptember 11th, 2014 at 09:17Robert Nyman [Editor]September 11th, 2014 at 09:35LukeSeptember 12th, 2014 at 21:24Jeff GriffithsSeptember 13th, 2014 at 00:53AvicennaSeptember 11th, 2014 at 10:47Jeff GriffithsSeptember 12th, 2014 at 01:22JonasSeptember 11th, 2014 at 15:11Robert Nyman [Editor]September 12th, 2014 at 00:50Tim RiggsSeptember 12th, 2014 at 09:26Robert Nyman [Editor]September 14th, 2014 at 11:08M. Edward (Ed) BoraskySeptember 29th, 2014 at 16:02Robert Nyman [Editor]September 30th, 2014 at 01:32netguySeptember 12th, 2014 at 10:22former firefox fanboySeptember 12th, 2014 at 18:13Lachlan FordSeptember 11th, 2014 at 16:57Jeff GriffithsSeptember 12th, 2014 at 01:21meSeptember 11th, 2014 at 17:45Robert Nyman [Editor]September 12th, 2014 at 00:16former firefox fanboySeptember 12th, 2014 at 18:27Robert Nyman [Editor]September 14th, 2014 at 11:04ChetanSeptember 12th, 2014 at 00:43Jeff GriffithsSeptember 12th, 2014 at 02:51Mark JohnsonSeptember 12th, 2014 at 01:58Robert Nyman [Editor]September 12th, 2014 at 02:09Filip DabrowskiSeptember 16th, 2014 at 15:12Robert Nyman [Editor]September 17th, 2014 at 00:04Alireza BehroozSeptember 17th, 2014 at 03:35Panos AstithasSeptember 17th, 2014 at 23:46