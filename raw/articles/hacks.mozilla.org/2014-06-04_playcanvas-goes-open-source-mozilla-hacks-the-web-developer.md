---
title: PlayCanvas Goes Open Source – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/06/playcanvas-goes-open-source/
author: Will Eastcott
published: '2014-06-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post by Will Eastcott of the PlayCanvas engine. As outlined in What Mozilla Hacks is, we constantly cover interesting information about open source and the Open Web, both from external as well as Mozilla authors, so feel free to share with us!*

On March 22nd 2011, Mozilla released Firefox 4.0 which enabled WebGL by default. A month later, we formed PlayCanvas and started building a game engine unlike anything that had gone before. Fast forward three years, and WebGL is everywhere. Only this week, Apple announced support for WebGL in both OS X and iOS 8. So what better time pass on some more exciting news for you:

The [PlayCanvas](https://playcanvas.com/) Engine has been open sourced!

## Introducing the PlayCanvas Engine

The PlayCanvas Engine is a JavaScript library engineered specifically for building video games. It implements all of the major components that you need to write high quality games:

- Graphics: model loading, per-pixel lighting, shadow mapping, post effects
- Physics: rigid body simulation, ray casting, joints, trigger volumes, vehicles
- Animation: keyframing, skeletal blending, skinning
- Audio engine: 2D and 3D audio sources
- Input devices: mouse, keyboard, touch and gamepad support
- Entity-component system: high level game object management

We had a couple of goals in mind when we originally designed the engine.

- It had to be easy to work with.
- It had to be blazingly fast.

## Simple Yet Powerful

As a developer, you want well documented and well architected APIs. But you also want to be able to understand what’s going on under the hood and to debug when things go wrong. For this, there’s no substitute for a carefully hand-crafted, unminified, open source codebase.

Additionally, you need great graphics, physics and audio engines. But the PlayCanvas Engine takes things a step further. It exposes a game framework that implements an entity-component system, allowing you to build the objects in your games as if they were made of Lego-like blocks of functionality. So what does this look like? Let’s check out a simple example on CodePen: [a cannonball smashing a wall](http://codepen.io/playcanvas/pen/ctxoD):

As you can see from the Pen’s JS panel, in just over 100 lines of code, you can create, light, simulate and view interesting 3D scenes. Try forking the CodePen and change some values for yourself.

## Need For Speed

To ensure we get great performance, we’ve built PlayCanvas as a hybrid of hand-written JavaScript and machine generated [asm.js](http://asmjs.org/). The most performance critical portion of the codebase is the physics engine. This is implemented as a thin, hand-written layer that wraps Ammo.js, the Emscripten-generated JavaScript port of the open source physics engine Bullet. If you haven’t heard of Bullet before, it powers amazing AAA games like Red Dead Redemption and GTAV. So thanks to Mozilla’s pioneering work on Emscripten and asm.js, all of this power is also exposed via the PlayCanvas engine. Ammo.js executes at approximately [1.5x native code](https://hacks.mozilla.org/2014/05/asm-js-performance-improvements-in-the-latest-version-of-firefox-make-games-fly/) speed in recent builds of Firefox so if you think that complex physics simulation is just not practical with JavaScript, think again.

But what about the non-asm.js parts of the codebase? Performance is clearly still super-important, especially for the graphics engine. The renderer is highly optimized to sort draw calls by material and eliminate redundant WebGL calls. It has also been carefully written to avoid making dynamic allocations to head off potential stalls due to garbage collection. So the code performs brilliantly but is also lightweight and human readable.

## Powering Awesome Projects

The PlayCanvas Engine is already powering some great projects. By far and away, the biggest is the PlayCanvas web site: the world’s first cloud-hosted game development platform.

For years, we’ve been frustrated with the limitations of current generation game engines. So shortly after starting work on the PlayCanvas Engine, we began designing a new breed of game development environment that would be:

- Accessible
- using any device with a web browser, plug in a URL and instantly access simple, intuitive yet powerful tools.
- Collaborative
- See what you teammates are working on in real-time or just sit back and watch a game as it’s built live before your eyes.
- Social
- Making games is easier with the help of others. Be part of an online community of developers like you.

PlayCanvas ticks all of these boxes beautifully. But don’t take our word for it – head to [https://playcanvas.com](https://playcanvas.com/) and discover a better way to make games.

In fact, here’s a game we have built using these very tools. It’s called SWOOOP:

It’s a great demonstration of what you can achieve with HTML5 and WebGL today. The game runs great in both mobile and desktop browsers, and you are free to deploy your PlayCanvas games to app stores as well. For Google Play and the iOS App Store, there are wrapping technologies available that can generate a native app of your game. Examples of these are Ludei’s CocoonJS and the open source Ejecta project. For Firefox OS, the process is a breeze since the OS treats HTML5 apps as first class citizens. PlayCanvas games will run out of the box.

## Want!

So if you think this is sounding tasty, where should you go to get started? The [entire engine sourcebase is now live on GitHub](https://github.com/playcanvas/engine):

Get cloning, starring and forking while it’s fresh!

## Stay in the Loop

Lastly, I want to give you some useful links that should help you stay informed and find help whenever you need it.

- Follow us on Twitter,
[@playcanvas](https://twitter.com/playcanvas), for largely technical updates on PlayCanvas. - Like the
[PlayCanvas Facebook page](https://www.facebook.com/playcanvas)for our whimsical views on the game dev scene. - Join and start discussions on the
[PlayCanvas Forum](http://forum.playcanvas.com/). - Get expert responses to your questions on
[PlayCanvas Answers](http://answers.playcanvas.com/).

We’re super excited to see what the open source community will do with the PlayCanvas Engine. So get creative and be sure to let us know about your projects.

Toodle pip!

## About
[
Will Eastcott ](https://playcanvas.com)

Will is co-creator of PlayCanvas, the open source game engine backed up by a powerful set of collaborative cloud development tools. He's worked in the video game industry for 17 years and been credited in lots of AAA titles like Call of Duty, Max Payne, DJ Hero and many more besides. He's passionate about making the web a more dynamic and beautiful place.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 6 comments

AndreiJune 4th, 2014 at 10:36RenkaiJune 4th, 2014 at 15:08renderhjsJune 4th, 2014 at 18:02Robert Nyman [Editor]June 5th, 2014 at 08:48paulJune 5th, 2014 at 06:43Robert Nyman [Editor]June 5th, 2014 at 08:46