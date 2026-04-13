---
title: Introducing Aurora 9 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/09/introducing-aurora-9/
author: Robert Nyman
published: '2011-09-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We have just released Aurora 9 ([download and test Aurora 9](http://www.mozilla.org/en-US/firefox/channel/)), which is planned to be the upcoming Firefox 9. In it, we have a number of new things that we hope will get you excited!


## JavaScript Type Inference

We’ve improved JavaScript performance once again with type inference. We’ve made significant improvements on both the V8 and Kraken benchmarks, and you should see real-world improvements to JavaScript performance as well.

## JavaScript Interface for Do Not Track

Firefox 4 introduced [Do Not Track](https://developer.mozilla.org/en/The_Do_Not_Track_Field_Guide/Introduction/How_Do_Not_Track_works), and now there is a way to detect a users’prefence through JavaScript as well:

## mouseenter and mouseleave events

For some time now, [web developers have been struggling](http://www.quirksmode.org/dom/events/mouseover.html) with handling `mouseover`

and `mouseout`

events on elements, since when child elements have gained focus, the event has bubbled up and triggered `mouseout`

on the parent element – something you would in most cases not like to happen.

Therefore, we are now happy to introduce support for `mouseenter`

and `mouseleave`

events:

## Camera UI for Mobile

You can now use an input element to trigger a native app to take pictures. Please try the [Camera UI for Mobile demo](http://jsbin.com/iwerow/27/).

## Support for chunked XMLHttpRequest

When doing XMLHttpRequest requests with large data sets, you can now [get partial data](https://bugzilla.mozilla.org/show_bug.cgi?id=687087) as it arrives instead of waiting for it all to show up. You can use this to build more responsive and more efficient web sites.

## Other changes

We’ve also got support for a bunch of other changes as well. These will be added to the [Firefox 9 for Developers page over the next few weeks.](https://developer.mozilla.org/en/Firefox_9_for_developers)

#### HTML

- We now support
[document.caretPositionFromPoint](https://bugzilla.mozilla.org/show_bug.cgi?id=654352) - We now support
[Node.contains(node)](https://bugzilla.mozilla.org/show_bug.cgi?id=683852) - We now
[return true for node.contains(node)](https://bugzilla.mozilla.org/show_bug.cgi?id=685139), as other browsers do. (The spec says we should return false but the spec is probably wrong given the behaviour of all browsers.) - We now support
[Node.parentElement](https://bugzilla.mozilla.org/show_bug.cgi?id=685798) - We no longer
[taint the canvas data when drawing images where @crossorigin is set on them](https://bugzilla.mozilla.org/show_bug.cgi?id=685518) - We now only
[fire onreadystatechange on the document element](https://bugzilla.mozilla.org/show_bug.cgi?id=682554) - There is now
[UI for HTML5 Forms Validation in Fennec](https://bugzilla.mozilla.org/show_bug.cgi?id=605365) - We now fire
[load and error events on stylesheet link elements that are loaded dynamically](https://bugzilla.mozilla.org/show_bug.cgi?id=185236) - We now support
[DOM3 composition events](https://bugzilla.mozilla.org/show_bug.cgi?id=543789)

#### Graphics

- We now support
[Vista-style ICO files](https://bugzilla.mozilla.org/show_bug.cgi?id=600556) - We now
[decode images only when drawing them](https://bugzilla.mozilla.org/show_bug.cgi?id=573583), instead of ahead of time

#### Layout

- We now support the
[CSS3 columns shorthand where column-count and column-width can be combined](https://bugzilla.mozilla.org/show_bug.cgi?id=446569) - We now support
[CSS3 text-overflow: <left> <right>](https://bugzilla.mozilla.org/show_bug.cgi?id=677582) - We now support the font-stretch property (
[bug number 3512, filed in 1999!](https://bugzilla.mozilla.org/show_bug.cgi?id=3512)) - You can now use
[65534 rowspans instead of 8190](https://bugzilla.mozilla.org/show_bug.cgi?id=688405), to match IE.

#### Network

- We’ve changed the way we handle
[semicolons during URL parsing](https://bugzilla.mozilla.org/show_bug.cgi?id=665706) - We no longer pop up a
[download dialog bog when a server returns no data](https://bugzilla.mozilla.org/show_bug.cgi?id=423506)and instead show a corrupted content error, to match other browsers. - We’ve made some
[minor](https://bugzilla.mozilla.org/show_bug.cgi?id=686312)[protocol](https://bugzilla.mozilla.org/show_bug.cgi?id=687243)fixes to WebSockets - If you include an
[empty disposition type it’s treated as an “attachment”](https://bugzilla.mozilla.org/show_bug.cgi?id=272541) - We don’t
[show redirect content after denying automatic redirect to javascript: URL](https://bugzilla.mozilla.org/show_bug.cgi?id=255119)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 30 comments

JasonSeptember 30th, 2011 at 16:55MarkSeptember 30th, 2011 at 18:32LizSeptember 30th, 2011 at 18:55mehOctober 1st, 2011 at 05:56BorisOctober 1st, 2011 at 15:10LizOctober 1st, 2011 at 21:10BorisOctober 1st, 2011 at 21:35Jonas SickingSeptember 30th, 2011 at 19:16Tim NiilerOctober 1st, 2011 at 06:05BorisOctober 1st, 2011 at 15:11RyanVMOctober 1st, 2011 at 07:23Jesper KristensenOctober 1st, 2011 at 09:28greg russellOctober 1st, 2011 at 12:37greg russellOctober 1st, 2011 at 12:38Robert NymanOctober 1st, 2011 at 19:18besrOctober 1st, 2011 at 14:54Sean McArthurOctober 12th, 2011 at 10:10Benoit JacobOctober 1st, 2011 at 15:09Aryeh GregorOctober 2nd, 2011 at 11:16Robert NymanOctober 2nd, 2011 at 16:48j.j.October 8th, 2011 at 11:53marcOctober 19th, 2011 at 01:07Robert NymanOctober 19th, 2011 at 02:24Saeed NeamatiNovember 1st, 2011 at 05:48Robert NymanNovember 2nd, 2011 at 08:38BradNovember 4th, 2011 at 01:38Robert NymanNovember 4th, 2011 at 08:48friesecustomsApril 5th, 2012 at 21:45Janet SwisherApril 6th, 2012 at 09:27LoganJune 22nd, 2012 at 16:48