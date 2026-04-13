---
title: HTML5 conversion and information at Mosync hackathon in Stockholm, Sweden –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/04/html5-conversion-and-information-at-mosync-hackathon-in-stockholm-sweden/
author: Chris Heilmann
published: '2012-04-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It is not often that you find yourself in a disused nuclear reactor from the 50s to talk about state-of-the-art web technology. For about a hundred developers and designers this is exactly what happened last Saturday in Stockholm, Sweden.

The [R1 reactor](http://atlasobscura.com/place/r1-nuclear-reactor) played host to the [Mosync hackathon](http://www.mosync.com/hackathon) organised to get developers to try out the [Wormhole](http://www.mosync.com/content/html5-javascript-wormhole) and [Reload](http://www.mosync.com/content/using-mosync-reload) technologies, both of which make it very easy to build apps based on HTML5 or C++ for both feature and smartphones.

Mosync asked Mozilla to participate after a quick brownbag in their office on HTML5 a few weeks ago. So we went and gave an introduction on “HTML5 and the near-future of the web”. You can [read the slides here](http://icant.co.uk/talks/mosynchack/) and see a [screencast with audio on YouTube](http://www.youtube.com/watch?v=pNcKLd7w4-A).

The topics covered in the talk are:

- Converting C++ to JavaScript using
[Emscripten](https://github.com/kripken/emscripten/wiki) - A few CSS demos:
[Impress.js](http://bartaz.github.com/impress.js/#/bored)for fancy presentations using 3D transformation[The CSS book](https://developer.mozilla.org/en-US/demos/detail/the-css-book/launch)for 3D transformations simulating a book[Paperfold CSS](https://developer.mozilla.org/en-US/demos/detail/paperfold-css/launch)to spice up a collapsible list[CSS 3D Clouds](https://developer.mozilla.org/en-US/demos/detail/css3d-clouds/launch)to render realistic clouds[The Box](https://developer.mozilla.org/en-US/demos/detail/the-box/launch)using[Sprite3D.js](http://minimal.be/lab/Sprite3D/)for simulating a 3D environment like WebGL in CSS

- Issues with HTML5 Audio
[Native audio events](http://www.jplayer.org/HTML5.Media.Event.Inspector/)[Audio Sprites](http://hacks.mozilla.org/2012/04/html5-audio-and-audio-sprites-this-should-be-simple/)and how it shouldn’t be a problem using them[Are we playing yet?](http://areweplayingyet.com/)as a test platform to see just how much of audio support in browsers is broken[Probably, Maybe, No](http://24ways.org/2010/the-state-of-html5-audio): The State of HTML5 Audio –[long video](http://www.youtube.com/watch?v=ffk65q5Rl9I)–[short video](http://www.youtube.com/watch?v=C2Tw0BeZb8Q)(Scott Schiller explaining in detail what the issues are)[Soundmanager 2](http://www.schillmania.com/projects/soundmanager2/)as an option to work around the issues with sound.

- Taking audio further:
[Mozilla Audio Data API](https://wiki.mozilla.org/Audio_Data_API)(Firefox only)[Dance.js](http://jsantell.github.com/dance.js/)– a hack developed by[Jordan Santell](http://github.com/jsantell)and[Brian Hassinger](http://github.com/brainss)using the Mozilla Audio API.[Web Audio specification](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html)(Webkit)[Work in progress on syncing the efforts and libraries to use](http://happyworm.com/blog/2011/11/15/html5-audio-apis-how-low-can-we-go)

- Games
[Are we fun yet?](https://wiki.mozilla.org/Platform/AreWeFunYet)gaming specific efforts in Firefox[Browserquest](http://browserquest.mozilla.org/)a multiplayer game in HTML5 using WebSockets[Building a game from semantic HTML](http://thewebrocks.com/demos/html5catcher/)[Page Visibility (Chrome)](http://www.samdutton.com/pageVisibility/)[RequestAnimationFrame]([Microsoft’s post](http://blogs.msdn.com/b/ie/archive/2011/07/05/using-pc-hardware-more-efficiently-in-html5-new-web-performance-apis-part-1.aspx))[Fullscreen API](https://wiki.mozilla.org/Gecko:FullScreenAPI)([Demo](http://html5-demos.appspot.com/static/fullscreen.html))[Mouselock API](http://hacks.mozilla.org/2011/12/paving-the-way-for-open-games-on-the-web-with-the-gamepad-and-mouse-lock-apis/)[Gamepad API](http://hacks.mozilla.org/2011/12/paving-the-way-for-open-games-on-the-web-with-the-gamepad-and-mouse-lock-apis/)

- GetUserMedia:
- Mobile
[Are we mobile yet?](http://arewemobileyet.com)– showing what parts of mobile hardware can be reached via JavaScript and which can’t yet[APIs available for testing](http://hacks.mozilla.org/2011/12/state-of-the-web-apis-an-interview-with-john-hammink/): Battery, Camera access, Vibration, IndexDB, sending SMS[Boot to Gecko](https://wiki.mozilla.org/B2G)[WebRTC draft](http://dev.w3.org/2011/webrtc/editor/webrtc.html)[WebRTC efforts at Mozilla](http://hacks.mozilla.org/2012/04/webrtc-efforts-underway-at-mozilla/)


And as I had some time and brought my trusty Competition Pro joystick, I thought I should give the Gamepad API a whirl and created the [world’s first joystick powered kitten cube](http://christianheilmann.com/2012/04/14/a-joystick-powered-kitten-cube/) (maybe).

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!