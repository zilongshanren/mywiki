---
title: Firefox Aurora 13 is out – SPDY on by default and a list of other improvements
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/03/firefox-aurora-13-is-out-spdy-on-by-default-and-a-list-of-other-improvements/
author: Robert Nyman
published: '2012-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We have just released [Aurora 13](http://www.mozilla.org/en-US/firefox/aurora/), together with a number of improvements.


## Highlights

There are a couple of things we’d like to shine some extra light on here:

### SPDY on by default

The SPDY control brings [responsive and scalable transport to Firefox](http://hacks.mozilla.org/2012/02/spdy-brings-responsive-and-scalable-transport-to-firefox-11/). It allows for multiplexing and connection sharing and is SSL only. It will offer faster page loads and better scalability for SPDY-enabled web servers.

Our first implementation was in Firefox 11, but now with Firefox Aurora 13 it is on by default!

### User Agent change for Mobile

The preferred way for web sites to offer content depending on the device is to use CSS Media Queries. However, there is a good amount of user agent sniffing still going on out there, so we wanted to make you aware of the change/difference between Firefox on mobile phones and on tablets, as outlined in [Mobile and Tablet indicators](https://developer.mozilla.org/en/Gecko_user_agent_string_reference#Mobile_and_Tablet_indicators).

For Firefox on mobile it will be:

`Mozilla/5.0 (Android; Mobile; rv:13.0) Gecko/13.0 Firefox/13.0`

Firefox on tablets will be:

`Mozilla/5.0 (Android; Tablet; rv:13.0) Gecko/13.0 Firefox/13.0`

## List of improvements

Here are all the improvements we’ve made complete with links to each bug listing for those who want to read up more on respective implementation.

### DOM

[Move plugins to content – plugins should withstand a reframe of the object frame](https://bugzilla.mozilla.org/show_bug.cgi?id=90268)[Enable multitouch, for Android](https://bugzilla.mozilla.org/show_bug.cgi?id=723200)[Screen orientation API reading and event implementation in Android](https://bugzilla.mozilla.org/show_bug.cgi?id=720795)[Unprefix Blob.mozSlice](https://bugzilla.mozilla.org/show_bug.cgi?id=725289)[Implement DOMRequest](https://bugzilla.mozilla.org/show_bug.cgi?id=722626)[Implement index property on <option> in <datalist>](https://bugzilla.mozilla.org/show_bug.cgi?id=720385)[Remove support for globalStorage](https://bugzilla.mozilla.org/show_bug.cgi?id=687579)

### Plugins

### JavaScript

### Layout

[Support “turn” unit from CSS3 Values and Units](https://bugzilla.mozilla.org/show_bug.cgi?id=716628)[[css3-background] Accept background-position values like “bottom 10px right 10px”](https://bugzilla.mozilla.org/show_bug.cgi?id=522607)[Drop support for prefixes from border-radius* and box-shadow](https://bugzilla.mozilla.org/show_bug.cgi?id=693510)[Implement background-repeat as a keyword pair as well as just a single keyword](https://bugzilla.mozilla.org/show_bug.cgi?id=548375)[Expose alternative content in Canvas element to ATs](https://bugzilla.mozilla.org/show_bug.cgi?id=495912)

### Network

[UA Change for Mobile](https://bugzilla.mozilla.org/show_bug.cgi?id=671634)[SPDY on by default](https://bugzilla.mozilla.org/show_bug.cgi?id=724563)[XHR rewrites non-POST methods upon 301/302 redirects](https://bugzilla.mozilla.org/show_bug.cgi?id=598304)[XHR for data URIs should support content-type header field](https://bugzilla.mozilla.org/show_bug.cgi?id=727530)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 13 comments

ohforfMarch 20th, 2012 at 07:58Robert NymanMarch 21st, 2012 at 03:05Capt. ObviousMarch 23rd, 2012 at 14:40Robert NymanMarch 23rd, 2012 at 17:26JayMarch 20th, 2012 at 09:44Robert NymanMarch 21st, 2012 at 17:58Tin Aung LinnMarch 25th, 2012 at 21:07Robert NymanMarch 29th, 2012 at 11:19madovskyJune 6th, 2012 at 02:55madovskyJune 6th, 2012 at 14:07veliFebruary 20th, 2013 at 12:32Jimmie JohnsonMarch 5th, 2013 at 21:33Jimmie JohnsonMarch 5th, 2013 at 21:36