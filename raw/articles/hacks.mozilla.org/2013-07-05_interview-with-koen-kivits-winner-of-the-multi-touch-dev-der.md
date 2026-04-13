---
title: Interview with Koen Kivits, winner of the Multi-touch Dev Derby – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2013/07/interview-with-koen-kivits-winner-of-the-multi-touch-dev-derby/
author: John Karahalis
published: '2013-07-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Koen Kivits won the Multi-touch Dev Derby with TouchCycle, his wonderful TRON-inspired mobile game. Recently, I had the chance to learn more about Koen: his work, his ambitions, and his thoughts on the future of web development.*

![Koen Kivits](../../assets/926690fd1001344b.jpg)


## The interview

### How did you become interested in web development?

I’ve been creating websites since high school, but I didn’t really get serious about web development until I started working two and a half years ago. I wasn’t specifically hired for web development, but I kind of ended up there. I came in just as our company was launching a major new web based product, which has grown immensely since then. The challenges we faced during this ongoing growth and how we were able to solve them really made me view the web as a serious platform.

### Can you tell us a little about how TouchCycle works?

The game itself basically consists of an arena with 2 or more players on it. Each player has a position and a target to which it is moving. As each player moves, it leaves a trail in the arena.

Each segment in a player’s trail is defined as simple linear equation, which makes it really easy to calculate intersections between segments. Collision detection is then done by checking whether a player’s upcoming trail segment intersects with an already existing trail segment.

The arena is drawn on a [<canvas> element](https://developer.mozilla.org/docs/HTML/Canvas) that is sized to fit the screen when the game starts. The <canvas> has 3 [touch event](https://developer.mozilla.org/docs/Web/Guide/DOM/Events/Touch_events) handlers registered to it:

[touchstart](https://developer.mozilla.org/docs/Web/Reference/Events/touchstart): register nearest unregistered player (if any) to the new touch and set its target[touchmove](https://developer.mozilla.org/docs/Web/Reference/Events/touchmove): update the target of the player that is registered to the moving touch[touchend](https://developer.mozilla.org/docs/Web/Reference/Events/touchend): unregister the player

Any touch events on the document itself are cancelled while the game is running in order to prevent any scrolling and zooming.

Everything around the main game (the menus, the notifications, etc.) is just plain [HTML](https://developer.mozilla.org/docs/Web/HTML). Menu navigation is done with HTML anchors and a hashchange event handler that hides or shows content relevant to the current URL. Note that this means you can use your browser’s back and forward buttons to navigate within the game.

### What was your biggest challenge in developing TouchCycle?

Multitouch interaction was completely new to me and I had done very little work with the <canvas> element before, so it took me a while to read up on everything and get to work. I also had to spend some time tweaking the collision detection and the way a player follows your touch in order to not have players crash into their own trails easily.

### What makes the web an exciting platform for you?

The openness of the platform, in several ways. Anyone with an internet connection can access the web using any device running a browser. Anyone can publish to the web–there’s no license required, no approval process and no being locked in to a specific vendor. Anyone can open up their browser’s developer tools to see how an app works and even tinker with it. Anyone can even contribute to the standards that make up the very platform itself!

### What new web technologies are you most excited about?

I’m probably most excited about [WebRTC](https://developer.mozilla.org/docs/WebRTC). It opens up a lot of possibilities for web developers, especially when mobile support increases. For example, just think of how combining WebRTC, the [Geolocation API](https://developer.mozilla.org/docs/WebAPI/Using_geolocation) and [Device Orientation API](https://developer.mozilla.org/docs/WebAPI/Detecting_device_orientation) would make for an awesome augmented reality app. The possibilities are limitless.

### If you could change one thing about the web, what would it be?

I really like how the web is a collaborative effort. A problem of that collaboration, however, is conflicting interests leading to delayed or crippled new standards. A good example is the HTML [<video> element](https://developer.mozilla.org/docs/Web/HTML/Element/video), which I think is still not very usable today despite being such a basic feature.

Browser vendors should be allowed some flexibility in the formats they support, but I think it would be a good thing if there was a minimum requirement of supporting at least 1 common open format.

### Do you have any advice for other ambitious web developers?

As a developer I think I’ve learnt most from reading other people’s code. If you like a library or web app, it really pays to spend some time analysing its source code. It can be really inspiring to look at how other people solve problems; it can give you pointers on how to structure your own code and it can teach you about technologies you didn’t even know about.

Also, don’t be afraid to read the specification of a standard every now and then to really learn about the technologies you’re using.

## Further reading

[Detecting touch: it’s the ‘why’, not the ‘how’](https://hacks.mozilla.org/2013/04/detecting-touch-its-the-why-not-the-how/)[Building a simple paint game with HTML5 Canvas and Vanilla JavaScript](https://hacks.mozilla.org/2013/06/building-a-simple-paint-game-with-html5-canvas-and-vanilla-javascript/)[Optimizing your JavaScript game for Firefox OS](https://hacks.mozilla.org/2013/05/optimizing-your-javascript-game-for-firefox-os/)