---
title: 'Interview: Ondřej Žára, Websockets Dev Derby winner – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2012/08/interview-ondrej-zara-websockets-dev-derby-winner/
author: John Karahalis
published: '2012-08-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Ondřej Žára](https://developer.mozilla.org/profiles/ondras/) achieved a first in the [Websockets Dev Derby](https://developer.mozilla.org/demos/devderby/2012/may/) this past May. In one month, he won three spots in the top five: a finalist spot for [Collaborative Draw](https://developer.mozilla.org/demos/detail/collaborative-draw), third place for [Atoms](https://developer.mozilla.org/demos/detail/atoms), and first place for [Just Spaceships!](https://developer.mozilla.org/demos/detail/just-spaceships).

*I recently had the chance to learn more about Ondras, his work, and his thoughts on the future of web development. In our interview, he shared insight that should be interesting to new web developers and veterans alike.*

### Tell us about developing your winning demos. Was anything especially exciting, challenging, or rewarding?

I have submitted quite a number of projects to [Mozilla Demo Studio](https://developer.mozilla.org/demos/), but the most critically acclaimed were related to WebSocket technology. Writing WebSocket demos was truly challenging, as the Mozilla Demo Studio site is hosted at HTTPS, which means that (at least in Firefox) the WebSocket backend must communicate via WSS. Therefore, in order to publish a working demo, I had to completely add TLS support to my [TeaJS](http://code.google.com/p/teajs/)-based server.

Generally speaking, this was very beneficial: implementing TLS capabilities to TeaJS resulted in a [new release](https://plus.google.com/105346527211268283692/posts/HtCydJsNbJC) with exciting features :-)

### How did you get interested in web development?

I experimented with new and interesting web technologies from my early age: first with [VRML](http://en.wikipedia.org/wiki/VRML), later with JavaScript. One of my hobby projects, the [WWW SQL Designer](http://code.google.com/p/wwwsqldesigner/), was highly praised by many users: that convinced me that I should indeed focus on Web/JS development.

### What makes the web an exciting platform for you?

The complete and immediate availability; in every computer, every OS, every sufficiently advanced mobile device. Web browser is one of the most sophisticated and optimized piece of software today; most of the interesting stuff in IT is related to the Web.

### What up-and-coming web technologies are you most excited about?

I watch the new [ECMA stuff](http://www.slideshare.net/BrendanEich/jslol-9539395) with interest; the [Dart language](http://www.dartlang.org/) also looks very promising – mostly because of a much better DOM. When is Mozilla going to add Dart bindings to Firefox?

The [Boot to Gecko](http://www.mozilla.org/b2g/) project is also something to look at; along with [Emscripten](https://github.com/kripken/emscripten) and [jslinux](http://bellard.org/jslinux/).

Finally, the very recent [E4H](http://www.hixie.ch/specs/e4h/strawman) proposal looks rather sexy :-)

### If you could change one thing about the web, what would it be?

As a JavaScript person, my answer here is obvious: the HTMLElement should be fully cross-browser prototype extensible. That would be awesome. That would make this world definitely a better place :-)

### What advice would you give to aspiring web developers?

Do not trust what most other people say; try stuff for yourself! Most of the long discussion/support threads on the Web are old and obsolete; the same often applies to articles and news reports.

Also, do not use tools you don’t 100% understand. Avoid working with an external library/toolkit unless you are very familiar with what – and how – it does. To understand stuff, you need to look under the hood.

### Is there anything else you would like to share?

I would like to thank Mozilla for the wonderful work it does, including the Firefox browser, Demo Studio website, Hacks weblog and Dev Derby competition :-)

*Further Reading*

[MDN articles on WebSockets](https://developer.mozilla.org/en/WebSockets)[BrowserQuest – a massively multiplayer HTML5 (WebSocket + Canvas) game experiment](https://hacks.mozilla.org/2012/03/browserquest/)[Adding real-time multiplayer game-play with WebSockets](http://hacks.mozilla.org/2011/12/gaming-and-the-mozilla-labs-apps-project/#websockets-gaming)