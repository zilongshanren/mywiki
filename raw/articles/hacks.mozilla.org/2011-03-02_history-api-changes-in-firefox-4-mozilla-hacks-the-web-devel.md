---
title: History API changes in Firefox 4 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/03/history-api-changes-in-firefox-4/
author: Janet Swisher
published: '2011-03-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is a guest post by Jonas Sicking, one of the Gecko developers.

As I’m sure you know we’re getting ready to ship Firefox 4. And as you

might know Firefox 4 includes the [history](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history) API (which includes the pushState() and replaceState() methods) defined in HTML5. This API is also implemented in Safari and Chrome, but Firefox 4 has important differences, which I describe in this post.

A few weeks ago someone discovered a pretty big flaw in the pushState API. The problem is that if you use the *state* argument to pushState() or replaceState(), and the user later reloads page with such a state, there is no way to get access to said state until after the `load`

event fires. This because the only way to get access to said state is through the `popstate`

event which doesn’t fire until after `load`

has fired.

This means that for pages that use the *state* argument, the page has to render without knowledge of said state, and only after the page has been fully loaded can the correct state be shown to the user.

Note that the “state” that I’m talking about here is the *state* argument passed to pushState()/replaceState(). The URL (which arguably is the much more useful argument to pushState()/replaceState()) is always accessible using the normal APIs like [document.location](https://developer.mozilla.org/en/document.location) and [window.location](https://developer.mozilla.org/en/DOM/window.location).

To fix this problem we are making two changes in our implementation compared to the current working draft:

- Always expose the current
*state*through a`window.history.state`

property. This way a page immediately gets access to the current state of the page and doesn’t have to wait until the first`popstate`

event fires. - Don’t always fire a
`popstate`

event right after the`load`

event.

Instead, only fire it during real session history transitions (i.e., when the user clicks Back or Forward or when history.back()/forward()/go() is called)

The whole purpose of this extra`popstate`

event was to give access to the page’s state. However the`window.history.state`

property makes this redundant. We have found that pages just find this event unexpected and a source of bugs.

The first change should be fully backwards compatible since it’s a purely additive change. It doesn’t affect existing code, which presumably doesn’t use this property.

The second change is the bigger concern. If your code is expecting this event to always fire, then this might result in problems. Another thing that alleviates the risk with this change is that Safari 5 appears to have misunderstood the working draft on this issue, and doesn’t fire this `popstate`

unless a *state* is specifically passed to pushState()/replaceState(). So basically Firefox will behave like Safari 5 as long as you don’t use the *state* argument.

We are also making a third change:

- Allow
`popstate`

to fire while the page is loading.

The working draft currently has a somewhat surprising limitation in that it forbids any `popstate`

events from firing before the `load`

event for a page has fired. If the user clicks on a pushState-backed link while the page is loading (for example due to a slow-loading image), and then presses the Back button, no `popstate`

event fires. Only after the `load`

event for the page has fired is the first `popstate`

allowed to fire. We have removed this limitation and always fire `popstate`

when the Back or Forward button is pressed or when history.back()/forward()/go() is called.

I have done some testing and so far have not seen any problems due to these changes. Unfortunately, due to discovering these problems so late, these changes won’t appear in Firefox betas until Firefox 4 RC. There are [test builds available](http://ftp.mozilla.org/pub/mozilla.org/firefox/tryserver-builds/sicking@mozilla.com-23e215e53733/), which you can test with right away.

## About Jonas Sicking

Jonas has been hacking on web browsers for over a decade. He started as a open source contributor in 2000 contributing to the newly open sourced mozilla project. In 2005 he joined mozilla full time and has since been working on the DOM and other parts of the web platform. He is now the Tech Lead of the Web API project at mozilla as well as an editor for the IndexedDB and File API specifications at W3C.

## 10 comments

Christoph PojerMarch 4th, 2011 at 14:25WahooneyMarch 4th, 2011 at 22:38André LuísMarch 7th, 2011 at 02:33André LuísMarch 7th, 2011 at 09:45raduMarch 8th, 2011 at 05:59Benjamin LuptonMarch 11th, 2011 at 07:43JohnMarch 31st, 2011 at 18:07Benjamin LuptonMarch 31st, 2011 at 21:17ChrisJune 21st, 2011 at 07:51Alan KesselmannJuly 14th, 2011 at 07:40