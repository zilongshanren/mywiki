---
title: ServiceWorkers and Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/06/serviceworkers-and-firefox/
author: Nikhil Marathe
published: '2014-06-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Since early 2013, Mozillians have been involved with the design of the [Service Worker](https://github.com/slightlyoff/ServiceWorker/). Thanks to work by Google, Samsung, Mozilla, and others, this exciting new feature of the web platform has evolved to the point that it is being implemented in various web browser engines.

## What are Service Workers?

At their simplest, Service Workers are scripts that act as client-side proxies for web pages. JavaScript code can intercept network requests, deliver manufactured responses and perform granular caching based on the unique needs of the application, a feature that the web platform has lacked before now. This powerful capability being made available to web developers enables, among other things, the creation of fully-functioning offline experiences. Jake Archibald has summarized some of these features in [his blog post](http://jakearchibald.com/2014/service-worker-first-draft/).

Since Service Workers run in the “background”, they open up several possibilities for the Web that were previously only available on native platforms. Apart from the networking capabilities provided by the base specification, Service Workers are intended to be used by the [Push API](https://dvcs.w3.org/hg/push/raw-file/tip/index.html) and the [Background Sync API](https://github.com/slightlyoff/BackgroundSync/blob/master/explainer.md) to deliver messages from the user-agent to web applications.

## Service Workers in Firefox

A number of Mozillians have been hard at work implementing Service Workers in Gecko while Anne van Kesteren and Jonas Sicking help with the design and specification. Members of the [Necko](https://developer.mozilla.org/en-US/docs/Necko) team and others have provided input from networking and related perspectives. Nikhil Marathe recently published a blog post about [the status of Service Workers in Gecko](http://blog.nikhilism.com/2014/05/serviceworker-implementation-status-in-firefox.html).

The Service Worker implementation in Gecko is landing in pieces as soon as they are finished and reviewed. For the time being, as the specification continues toward stability and other implementations — notably Blink’s — progress, all functionality in Gecko is behind the `dom.serviceWorkers.enabled`

preference which is set to false by default but can be toggled in `about:config`

.

Our plan is that web developers will soon be able to exercise most Service Worker functionality in [Firefox Nightly](https://www.mozilla.org/firefox/nightly) with the above preference flipped to true. The best plans can always be waylaid but we hope for this to happen by the end of September 2014 at the latest.

## Status of Service Worker implementations

The inimitable Jake Archibald has written a tool to easily see the [status of Service Worker implementations](https://jakearchibald.github.io/isserviceworkerready/). You can follow along with the gecko implementation via the [meta bug](https://bugzilla.mozilla.org/show_bug.cgi?id=903441).

## About
[
Nikhil Marathe ](http://blog.nikhilism.com)

Nikhil is a Platform Engineer at Mozilla. He likes technical writing, having written 'An Introduction to libuv', and blogs at http://blog.nikhilism.com. He can be found working when he is not hiking, climbing or reading.

## About Andrew Overholt

Andrew is an engineering manager on the DOM team at Mozilla.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

Filip Bech-LarsenJune 26th, 2014 at 00:34NikhilJune 27th, 2014 at 11:17Ivan DejanovicJune 26th, 2014 at 06:49NikhilJune 27th, 2014 at 11:21