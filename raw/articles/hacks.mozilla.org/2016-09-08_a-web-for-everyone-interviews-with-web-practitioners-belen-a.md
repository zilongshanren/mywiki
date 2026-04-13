---
title: 'A Web for Everyone: Interviews with Web Practitioners — Belén Albeza – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-belen-albeza/
author: Justin Crawford
published: '2016-09-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For the third interview in our cross-browser compatibility series we talk with Belén Albeza ([@ladybenko](https://twitter.com/ladybenko)). Belén is an engineer and a game developer who works on developer relations at Mozilla. She is the author of several books about web development, including “[Power-up Your Front-End Development with Grunt](https://leanpub.com/grunt)” and “[XHTML + CSS ¡de una maldita vez!](http://cafeina.ladybenko.net/xhtml.pdf)” She is a frequent speaker at conferences on topics such as game development, Web APIs and more. Next week she’ll speak at [View Source 2016 in Berlin](https://viewsourceconf.org/berlin-2016/schedule/#css-framework)! She also [contributes often to Mozilla Hacks](https://hacks.mozilla.org/author/balbezamozilla-com/).

We’ve heard from two great web developers so far about how (and why) they integrate web compatibility into their workflows. Two weeks ago, Rachel Andrew said, [“I’ve always worked from the assumption that the web is for everyone.”](https://hacks.mozilla.org/2016/08/a-web-for-everyone-interviews-with-web-practitioners-rachel-andrew/) Last week, Chris Coyier said he is motivated to make cross-browser compatible sites by a simple economic reality: [“People pay for websites that work for them.”](https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-chris-coyier/)

What motivates Belén to make the web work for everyone? Read on to find out.

![Belén Albeza](../../assets/bdb240192d6b8f2c.jpg)


**Belén, what does cross-browser compatibility mean to you?**

It means having a website or a web app that is *functional* – not necessarily *identical* – across different browsers.

** How often do you have to think about cross-browser compatibility? Have you found ways to work that allow you to reduce the amount of time you think about it compared to when you were less experienced?**

You always have to think about that. It is hard, however, since it’s natural to do 90% of the development under the same system. The only shortcut to this is to use web standards, so you know that your code will have a good chance of working in other browsers and systems, but you still never know for sure until someone tries it in a real browser, on a real device.

The only shortcut is to use web standards, so you know that your code will have a good chance of working in other browsers.


** What motivates you to make the extra effort to build a cross-browser compatible site?**

From my point of view, cross-browser compatibility is not a nice bonus to have: it is a *must*. You just cannot afford to have your product not work in one of the major browsers (or OSes). So I don’t see it as “extra effort”, I see it as “mandatory effort”.

**Could anything convince you not to make that effort? What?**

Cross-browser compatibility is not a binary switch in which you either have it or not – it is a spectrum. I consider it mandatory to have the product work under major browsers (Chrome, Firefox, Edge, Safari, Android Browser) and in major OSes (Windows, Mac, iOS, Android). Beyond that, unless it is a client requirement – like legacy support for older systems/browsers – I think that making sure that your code complies with Web Standards is a good sanity point. Most of the time you don’t have the resources to test in every browser, on every system, on every device.

There is also the issue of needing a particular feature that is core to your product, for instance, WebRTC, Websockets, or Web Audio. In this case, you are making a conscious decision or leaving out browsers with no implementation or a partial one.

** Have you ever had to convince a client or boss that building a cross-browser compatible site was important? How’d you do it?**

My experience so far has been usually the opposite: clients or product owners wanting to support as many browsers and systems as possible! I have had to convince them to ditch support for obsolete browsers so our code base could be more modern and smaller.

**Did you ever have a specific experience that caused you to take cross-browser compatibility more seriously with your next project?**

In one of my previous jobs we were developing a web app and we used both Firefox and Chrome for development. But these were the regular versions of the browsers. We built a release candidate of our app and patted ourselves on the back… just to find out the next day that the QA team had found a really nasty bug in our web app! How that could be?

Well, it turned out that the day after we submitted the release candidate for QA, a new version of a browser was released, and it fixed a bug that we had a workaround for. And this workaround – which was no longer necessary – was causing a bug! From that day on, we added the nightly builds of [Chrome](https://www.google.com/chrome/browser/canary.html) and [Firefox](http://nightly.mozilla.org/) to our development stack of tools, so we knew what to expect in the future!

** You’re speaking this September at View Source in Berlin. Your session is called, “ You might not need a CSS framework.” Do you think frameworks make cross-browser compatibility better or worse? Does any framework stand out as particularly good for compatibility?**

I think that framework creators have a huge responsibility with respect to cross-browser compatibility. If a framework only supports a subset of major browsers, and somehow it manages to become extremely popular… the Web would be doomed. My recommendation, in general, is to avoid the use of third-party frameworks except in very specific circumstances (like developing a prototype).

**You’ve done quite a bit of work with HTML5 games. What special compatibility challenges do HTML5 game developers face? Do you use a different set of tools for preventing/debugging compatibility issues in HTML5 games?**

It is challenging in many ways: performance varies across browsers, across devices… There are also some quirks you need to be aware of: for instance, different browsers support different formats for audio files, some mobile browsers require a user interaction to be able to play sounds, etc. But you have similar issues when creating native games, because not all devices are equal, do not perform the same and have different hardware capabilities!

When working on a commercial game there is usually a QA stage where the game is tested on different devices and OSes – you would “just” need to add different browsers as well. Now that I make games on my own, I pick a game framework which is known for good cross-browser compatibility ([Phaser](http://phaser.io/)) and test the game on the handful of devices I have at home.

**What would you tell a brand new developer graduating from a coding bootcamp about cross-browser compatibility?**

This is not an option, it is a must. You cannot afford to lose 50%, 40% or 30% of your potential audience. You have to care! And [caniuse.com](http://caniuse.com) works wonders ;)

You cannot afford to lose 50%, 40% or 30% of your potential audience. You have to care!


**Tips from Belén’s interview**

- Cross-browser compatibility does not mean making things look identical in every browser — it just means making them usable for everyone.
- The only shortcut for building a cross-browser compatible website is to stick to standards.
- Remember to test your site or application on the nightly versions of browsers, which include features soon to land in release channels.

## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.