---
title: 'Trainspotting: Firefox 39 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/06/trainspotting-firefox-39/
author: Sergi Mansilla
published: '2015-06-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

__Trainspotting__ is a series of articles highlighting features in the lastest version of Firefox. A new version of Firefox is shipped every six weeks – we at Mozilla call this pattern “release trains.”

A new version of Firefox is here, and with it come some great improvements and additions to the Web platform and developer tools. This post will call out a few highlights.

*For a full list of changes and additions, take a look at the Firefox 39 release notes.*

## DevTools Love

The Firefox Developer Tools are constantly getting better. We’re listening to developers on [UserVoice](https://ffdevtools.uservoice.com/), and using their feedback to make tools that are more powerful and easier to use. One requested feature was the ability to re-order elements in the Inspector:

Editing and tweaking CSS Animations is easier than ever – Firefox 39 lets developers pause, restart, slow down, and preview new timings without having to switch applications.

![Menu of animation easing presets in the Inspector](../../assets/f196b0ab0775cb9a.gif)


## CSS Scroll Snap Points

![CSS Scroll Snap Points in action](../../assets/d62e6adc54f8c5c7.gif)


CSS Scroll Snap Points let web developers instruct the browser to smoothly snap element scrolling to specific points along an axis, creating smoother, easier to interact with interfaces with fewer lines of code.

## Improvements to Firefox on Mac OS X

Firefox gets some Mac- specific improvements and updates in version 39:

**Project Silk enabled –**Improves scrolling and animation performance by more closely timing painting with hardware vsync.[Read more about Project Silk](https://hacks.mozilla.org/2015/01/project-silk/).**Unicode 8.0 skin tone emoji –**Fixed a bug in the rendering of skin tone modifiers for emoji.**Dashed line performance –**Rendering of dotted and dashed lines is vastly improved.[Check out the fixed bug for more information](https://bugzilla.mozilla.org/show_bug.cgi?id=1123019).

## Service Workers Progress

Firefox’s implementation of the Service Workers API continues – `fetch`

is enabled for workers and is now generally available to web content, and the `Cache`

and `CacheStorage`

are now [available behind a flag](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorker_API#Browser_compatibility).

There’s lots more changes and improvements in Firefox 39 – check out the [Developer Release Notes](https://developer.mozilla.org/en-US/Firefox/Releases/39) for developer-oriented changes or the [full list of bugs fixed](https://bugzilla.mozilla.org/buglist.cgi?j_top=OR&f1=target_milestone&o3=equals&v3=Firefox%2039&o1=equals&resolution=FIXED&o2=anyexact&query_format=advanced&f3=target_milestone&f2=cf_status_firefox39&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&v1=mozilla39&v2=fixed%2Cverified&limit=0) in this release. Enjoy!

## 14 comments

ChristophJuly 1st, 2015 at 00:18PotchJuly 1st, 2015 at 17:30ChristophJuly 1st, 2015 at 23:52SirquiniJuly 2nd, 2015 at 20:20John DoeJuly 2nd, 2015 at 02:05MonessemJuly 2nd, 2015 at 18:42Andrew KavanaghJuly 2nd, 2015 at 14:53Tim HamiltonJuly 4th, 2015 at 11:16MarcelJuly 5th, 2015 at 08:50LukeJuly 6th, 2015 at 07:45Andrew KavanaghJuly 6th, 2015 at 21:12Havi Hoffman [Editor]July 7th, 2015 at 11:09Andrew KavanaghJuly 7th, 2015 at 14:17RandyJuly 14th, 2015 at 20:14