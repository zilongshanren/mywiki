---
title: An Update on Web Components and Firefox – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/11/an-update-on-web-components-and-firefox/
author: Soledad Penadés
published: '2015-11-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Web Components](https://developer.mozilla.org/en-US/docs/Web/Web_Components) is an umbrella term for four technologies that aim to make UI development easier and more modular. It has been in development since about 2011: a very long time for Internet standards!

All the specifications have been changing constantly as more vendors have started *implementing* them, and also as developers have gained real world experience in *using* them.

Therefore, **it’s only natural that we are all confused as to what is and what is not natively available in each browser**.

To date, in Firefox:

- Only
is natively available.`<template>` - The first iteration of the new consensus-based
[Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Shadow_DOM)is expected to ship in the first half of 2016. You can read[Anne’s](https://annevankesteren.nl/2015/07/shadow-dom-custom-elements-update)and[Wilson’s](https://hacks.mozilla.org/2015/06/the-state-of-web-components/)posts for more details. - There was an initial implementation of
[Custom Elements](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Custom_Elements), based on prototypes, which is also the version Blink shipped, but Apple’s Ryosuke Niwa is fleshing out some experiments to come up with new approaches that use the ES6 class syntax instead. There won’t be active work on Custom Elements on Firefox until consensus is reached. [HTML Imports](https://developer.mozilla.org/en-US/docs/Web/Web_Components/HTML_Imports)are*not*shipping, as we want to wait to see what developers do with[ES6 modules](https://hacks.mozilla.org/2015/08/es6-in-depth-modules/). There was an early unfinished implementation which will be removed.

We are very aware that **keeping track of these changes is time consuming** for developers who want to make sure their web components code works in more than just one browser. We’re addressing this issue by creating the [Web Components Status in Firefox](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Status_in_Firefox) page in MDN. It will hold up to date information on what is implemented in Firefox, and any caveats you might encounter, so you can refer to it whenever you want to check what is available or not.

*With thanks to Wilson Page, Anne van Kesteren, Andrew Overholt and Jean-Yves Perrier for their insights on this topic!*

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

## 7 comments

philNovember 23rd, 2015 at 15:16Soledad PenadésNovember 30th, 2015 at 02:00Uruguayan SalamanderNovember 25th, 2015 at 05:50gianNovember 26th, 2015 at 09:00Lunatic LambdaNovember 29th, 2015 at 19:09Ivan DejanovicDecember 2nd, 2015 at 03:18Soledad PenadésDecember 2nd, 2015 at 06:37