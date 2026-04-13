---
title: Developing a simple HTML5 space shooter – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/03/developing-a-simple-html5-space-shooter/
author: Ondřej Žára
published: '2012-03-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![just-spaceships](../../assets/813b52ac34aca6b7.png)


Experimenting with modern web technologies is always fun. For my latest project, I came up with the following requirements:

- Not a complex game, rather a proof-of-concept
- Space shooter theme
- Canvas-based rendering, but no WebGL
- Re-use of existing sprites (I am no artist)
- Rudimentary audio support
- AI/Bots
- Working network multiplayer

I worked on this project only in my spare time; after approx. two weeks, the work was done: [Just Spaceships!](http://ondras.zarovi.cz/games/just-spaceships/) This article describes some decisions and approaches I took during the development. If you are interested in the code, you can check the relevant [Google Code project](http://code.google.com/p/just-spaceships/).

## Animation & timing

There are two basic ways to maintain an animation: `requestAnimationFrame`

and `setTimeout/setInterval`

. What are their strengths and weaknesses?

**requestAnimationFrame**instructs the browser to execute a callback function*when it is a good time (for animation)*. In most browsers this means 60fps, but other values are used as well (30fps on certain tablets). Deciding the correct timing is up to the browser; the developer has no control over it. When the page is in background (user switches to another tab), animation can be automatically slowed down or even completely stopped. This approach is well suited for fluent animation tasks.**setTimeout**instructs the browser to execute your next (animation) step after a given time has passed; the browser will try to fulfill this request as precisely as possible. No slowdowns are performed when the page is in background, which means that this approach is well suited for physics simulation.

To solve animation-related stuff, I created a [HTML5 Animation Framework](http://code.google.com/p/html5-animation-framework/) (HAF), which combines both approaches together. Two independent loops are used: one for simulation, the second one for rendering. Our objects (*actors* in HAF terminology) must implement two basic methods:

```
/* simulation: this is called in a setTimeout-based loop */
Ship.prototype.tick = function(dt) {
var oldPosition = this._position;
this._position += dt * this._velocity;
return (oldPosition != this._position);
}
/* animation: this is called in a requestAnimationFrame loop */
Ship.prototype.draw = function(context) {
context.drawImage(this._image, this._position);
}
```

Note that the `tick`

method returns a boolean value: it corresponds to the fact that a (visual) position of an object might (or might not) change during the simulation. HAF takes care of this – when it comes to rendering, it redraws only those actors that returned `true`

in their `tick`

method.

## Rendering

Just Spaceships makes extensive use of *sprites*; pre-rendered images which are drawn to canvas using its `drawImage`

method. I created a [benchmarking page](http://ondras.zarovi.cz/misc/haf/benchmark.html) which you can try online; it turns out that using sprites is way faster than drawing stuff via `beginPath`

or `putImageData`

.

Most sprites are animated: their source images contain all animation frames (such as in [CSS sprites](http://css-tricks.com/css-sprites/)) and only one frame (rectangular part of the full source image) is drawn at a time. Therefore, the core drawing part for an animated sprite looks like this:

```
Ship.prototype.draw = function(context) {
var fps = 10; /* frames per second */
var totalFrames = 100; /* how many frames the whole animation has? */
var currentFrame = Math.floor(this._currentTime * fps) % totalFrames;
var size = 16; /* size of one sprite frame */
context.drawImage(
/* HTML <img> or another canvas */
this._image,
/* position and size within source sprite */
0, currentFrame * size, size, size,
/* position and size within target canvas */
this._x, this._y, size, size
);
}
```

*By the way: the sprites for Just Spaceships! have been taken from Space Rangers 2, my favourite game.*

The golden rule of rendering is intuitive: *redraw only those parts of the screen which actually changed*. While it sounds pretty simple, following it might turn out to be rather challenging. In Just Spaceships, I took two different approaches for re-drawing sprites:

**Ships, lasers and explosions**use technique known as “dirty rectangles”; when an object changes (moves, animates, …), we redraw (`clearRect`

+`drawImage`

) only the area covered by its bounding box. Some deeper bounding box analysis must be performed, because bounding boxes of multiple objects can overlap; in this case, all overlapping objects must be redrawn.**Starfield background**has its own layer (canvas), positioned below other objects. The full background image is first pre-rendered into a large (3000×3000px) hidden canvas; when the viewport changes, a subset of this large canvas is drawn into background’s layer.

## Sound

Using HTML5 audio is a piece of cake – at least for desktop browsers. There were only two issues that needed to be taken care of:

**File format**– the format war is[far from being over](http://stackoverflow.com/questions/4923136/why-doesnt-firefox-support-mp3-file-format-in-audio); the most universal approach is to offer both MP3 and OGG versions.**Performance issues**on certain slower configurations when playing multiple sounds simultaneously. More particularly, my Linux box exhibited some slowdowns; it would be best to offer an option to turn the whole audio off (not implemented yet).

At the end of the day, the audio code looks basically like this:

```
/* detection */
var supported = !!window.Audio && !audio_disabled_for_performance_reasons;
/* format */
var format = new Audio().canPlayType("audio/ogg") ? "ogg" : "mp3";
/* playback */
if (supported) { new Audio(file + "." + format).play(); }
```

## Multiplayer & networking model

Choosing a proper networking model is crucial for user experience. For a realtime game, I decided to go with a client-server architecture. Every client maintains a [WebSocket](http://en.wikipedia.org/wiki/WebSocket) connection to central server, which controls the game flow.

In an ideal world, clients would send just keystrokes and the server would repeat them to other clients. Unfortunately, this is not possible (due to latency); to maintain consistency and synchronicity between players, it is necessary to run the full simulation at server and periodically notify clients about various physical attributes of ships and other entities. This approach is known as an* authoritative server*.

Finally, clients cannot just wait for server packets to update their state; players need the game to work even between periodical server messages. This means that browsers run their version of the simulation as well – and *correct* their internal state by data sent by server. This is known as a *client-side prediction*. A sample implementation of these principles looks like this:

```
/* physical simulation step - client-side prediction */
Ship.prototype.tick = function(dt) {
/*
assume only these physical properties:
acceleration, velocity and position
*/
this._position += dt * this._velocity;
this._velocity += dt * this._acceleration;
}
/* "onmessage" event handler for a WebSocket data connection;
used to override our physical attributes by server-sent values */
Ship.prototype.onMessage = function(e) {
var data = JSON.parse(e.data);
this._position = data.position;
this._velocity = data.velocity;
this._acceleration = data.acceleration;
}
```

You can find very useful reading about this at [Glenn Fiedler’s site](http://gafferongames.com/networking-for-game-programmers/what-every-programmer-needs-to-know-about-game-networking/).

## Multiplayer & server

Choosing a server-side solution was very easy: I decided to go with[ v8cgi](http://code.google.com/p/v8cgi/), a multi-purpose server-side javascripting environment, based on V8. Not only it is older than Node, but (most importantly) it was created and maintained by myself ;-).

The advantage of using server-side JavaScript is obvious: game’s server runs the *identical* code that is executed in browser. Even HAF works server-side; I just turned off its rendering loop and the simulation works as expected. This is a cool demonstration of client-server code sharing; something we will probably see more and more in the upcoming years.

## Modulus

In order to make the game more interesting and challenging, I decided that the whole playing area should wrap around – think of the game universe as of a large toroidal surface. When a spaceship flies far to the left, it will appear from the right; the same holds for other directions as well. How do we implement this? Let’s have a look at a typical simulation time step:

```
/* Variant #1 - no wrapping */
Ship.prototype.tick = function(dt) {
this._position += dt * this._velocity;
}
```

To create an illusion of a wrapped surface, we need the ship to remain in a fixed area of a given size. A modulus operator comes to help:

```
/* Variant #2 - wrapping using modulus operator */
Ship.prototype.tick = function(dt) {
var universe_size = 3000; // some large constant number
this._position += (dt * this._velocity) % universe_size;
}
```

However, there is a glitch. To see it, we have to solve this (elementary school) formula:

`(-7) % 5 = ?`

JavaScript’s answer is `-2`

; Python says `3`

. Who is the winner? The correctness of the result depends on the definition, but for my purpose, the positive value is certainly more useful. A simple trick was necessary to correct JavaScript’s behavior:

```
/* Returned value is always >= 0 && < n */
Number.prototype.mod = function(n) {
return ((this % n) + n) % n;
}
/* Variant #3 - wrapping using custom modulus method */
Ship.prototype.tick = function(dt) {
var universe_size = 3000; // some large constant number
this._position += (dt * this._velocity).mod(universe_size);
}
```

## Lessons learned

Here is a short summary of general tips & hints I gathered when developing JS games in general, but mostly during Just Spaceships development:

- Know the language! It is very difficult to create anything without properly understanding the programming language.
- Lack of art (sprites, music, sfx, …) should not stop you from developing. There are tons of resources for getting these assets; the need for original art is relevant only it later stages of the project.
- Use the paper, Luke! You know what my favorite development tools are? A pen and a sheet of squared paper.
- If you are not 100% sure about the whole game architecture, start with smaller (working) parts. Refactoring them later to form a larger project is natural, useful and easy.
- Collect feedback as soon as possible – at the end of the day, it is the users’ opinion that matters the most.

## TODO

As stated before, Just Spaceships is not a complete project. There is definitely room for improvements, most notably:

- Optimize the network protocol by reducing the amount of data sent.
- Offer more options to optimize canvas performance (decrease simulation FPS, turn off background, turn off audio, …).
- Improve the AI by implementing different behavior models.

Even with these unfinished issues, I think the game reached a playable state. We had quite a lot of fun testing its multiplayer component; I hope you will enjoy playing it!


## About
[
Ondřej Žára ](http://ondras.zarovi.cz/)

Ondřej Žára likes to experiment with anything related to JavaScript, HTML5 and other web technologies. He showcases many of his projects at [http://ondras.zarovi.cz/](http://ondras.zarovi.cz/).
He is currently employed at [Seznam.cz, a.s.](http://www.seznam.cz/), focusing mainly on popular mapping service [Mapy.cz](http://mapy.cz/) as well as HTML5 evangelism. From time to time, he tweets about JS stuff as [@0ndras](https://twitter.com/0ndras).

## About
[
Robin Hawkes ](http://rawkes.com)

Robin thrives on solving problems through code. He's a Digital Tinkerer, Head of Developer Relations at Pusher, former Evangelist at Mozilla, book author, and a Brit.

## 4 comments

karlMarch 9th, 2012 at 12:18Haitham El-GhareebMarch 9th, 2012 at 12:32client server architectureMarch 10th, 2012 at 01:59PhilSeptember 25th, 2012 at 04:31