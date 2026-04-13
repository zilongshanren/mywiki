---
title: A Wall Powered by EventSource and Server-Sent Events – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2011/06/a-wall-powered-by-eventsource-and-server-sent-events/
author: Louisremi
published: '2011-06-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[EventSource](http://www.w3.org/TR/eventsource/) [landed in Aurora 6](http://hacks.mozilla.org/2011/05/aurora-6-is-here/). It is a new and simplified way to open long-lived connections to a server, and let the browser create events as the server streams messages to the client. It is also available in Chrome and Opera and there are fallback solutions for other browsers.

### Creating a wall/feed for a social app…

…in a few lines of code (full project [available on Github](https://github.com/mozilla/webowonder-demos/tree/master/demos/friends%20timeline)).

### The messages

The server will send two kinds of messages:

● simple messages, starting on a new line prefixed with “data:”

● messages with specific event names, similar to simple messages but with “event: <anEventName>” on the previous line


In this case, simple messages are treated as users’ statuses and specific events will be inserted in the timeline with specific colors, although they could appear in different places on the page. The message data will be sent as JSON, although it could be flat text strings.

### The server

The server will be a dummy .php script that reads sample statuses from a text files and stream them, one at a time, to the client, using appropriate headers.


### The Client

The client will create an event source and register event handlers for each specific event name, as well as an `onmessage`

handler for *simple messages*.


The missing pieces of the code are [available on Github](https://github.com/mozilla/webowonder-demos/tree/master/demos/friends%20timeline).

### Fallbacks

Here is a short list of polyfills/fallbacks available for other browsers:

● Remy Sharp’s [polyfill](https://github.com/remy/polyfills/blob/master/EventSource.js)

● Yaffle’s [polyfill](https://github.com/Yaffle/polyfills)

● Rick Waldron’s [jquery plugin](https://github.com/rwldrn/jquery.eventsource)

**Have you got examples of EventSource based Web app to share?**

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 23 comments

louisremiJune 16th, 2011 at 07:44David illsleyJune 16th, 2011 at 11:09louisremiJune 16th, 2011 at 11:18David IllsleyJune 16th, 2011 at 11:37sonnyJune 18th, 2011 at 10:39louisremiJune 20th, 2011 at 08:13alainJune 21st, 2011 at 05:53louisremiJune 21st, 2011 at 06:18alainJune 21st, 2011 at 06:26Vitaliy KupetsJuly 11th, 2011 at 05:54davideJuly 16th, 2011 at 04:52louisremiJuly 20th, 2011 at 06:40Jerome LouvelJuly 21st, 2011 at 12:09Louis-Pierre BeaumontAugust 9th, 2011 at 02:06louisremiAugust 13th, 2011 at 00:21Louis-Pierre BeaumontAugust 9th, 2011 at 17:16AaronAugust 16th, 2011 at 09:12louisremiAugust 17th, 2011 at 02:11DavideAugust 17th, 2011 at 02:23Srirang (brahmana)September 7th, 2011 at 03:28SergiuMarch 20th, 2013 at 03:04VictorSeptember 28th, 2011 at 04:46Gary TessmanOctober 27th, 2012 at 17:02