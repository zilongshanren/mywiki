---
title: JavaScriptOO.com, to find what meets your JavaScript needs – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/01/javascriptoo-com-to-find-what-meets-your-javascript-needs/
author: Joe Maddalone
published: '2014-01-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The JavaScript Renaissance

We all know the major players in JavaScript projects. MV* frameworks like AngularJS, Backbone, and Ember.js are inspiring a whole new breed of client applications. Utility libraries like underscore and lodash simplify constructs once reserved for academic exercise. And of course, the monolithic namespace jQuery is everywhere. The large teams and growing communities behind these projects (a little corporate backing never hurts) are moving forward and providing very solid platforms for developers to build upon. However, they are merely a precursor for the renaissance that is happening in the world of JavaScript right now.

Enter the micro-libraries, the drop-in replacements, and the “I-Had-No-Idea-JS-Could-Do-That” projects. Thanks to tooling like Grunt, bower, and npm, testing suites like Jasmine and QUnit, and of course the social coding site github; dozens of peer-reviewed and test-driven JavaScript libraries are sprouting up every day. Fresh approaches on everything from the core JavaScript functionality to abstractions of the ridiculously complex are in abundance and expanding the very foundation of the web.

[VerbalExpression](https://github.com/VerbalExpressions/JSVerbalExpressions) lets you write regular expressions in English; [Knwl.js](https://github.com/loadfive/knwl.js) is a natural language processor; [140medley](https://github.com/honza/140medley) is an entire framework in 821 bytes. Want a DOM selector engine other than sizzle? Try [micro-selector](https://github.com/fabiomcosta/micro-selector), [nut](https://github.com/pyrsmk/nut), [zest](https://github.com/chjj/zest), [qwery](https://github.com/ded/qwery), [Sly](https://github.com/digitarald/sly), or [Satisfy](https://github.com/padolsey/satisfy). Need a templating engine? Try [T-Lite](https://github.com/CapMousse/T-Lite), [Grips](http://getify.github.io/grips/), [gloomy](http://pazguille.github.io/gloomy/), [Transparency](http://leonidas.github.io/transparency/), [dust](http://akdubya.github.io/dustjs/), [hogan.js](http://twitter.github.io/hogan.js/), [Tempo](http://twigkit.github.io/tempo/), [Plates](https://github.com/flatiron/plates), [Mold](http://marijnhaverbeke.nl/mold/), [shorttag](https://github.com/jeromeetienne/shorttag.js), [doT.js](http://olado.github.io/doT/index.html), [t.js](https://github.com/jasonmoo/t.js), [Milk](https://github.com/pvande/Milk), or at least 10 others. Dates got you down? Check out [Date-Utils](https://github.com/JerrySievert/node-date-utils), [moment.js](http://momentjs.com/), [datejs](http://www.datejs.com/), [an.hour.ago](https://github.com/davidchambers/an.hour.ago), [time.js](https://github.com/zever/time/). Route with [Pilot](http://rubaxa.github.io/Pilot/), filter images with [CamanJS](http://camanjs.com/), write games in [Crafty](http://craftyjs.com/), or make a presentation with [RevealJS](http://lab.hakim.se/reveal-js/) or [impress.js](http://bartaz.github.io/impress.js/).

Of course, along with this prolific creativity in the JS universe comes some serious overload. A bit of natural selection will eventually get the best of these projects on your radar, but if you want to see the really exciting bits of evolution occurring you have to watch. Constantly.

## JavaScriptOO.com

Watching constantly is exactly what I do with JavaScriptOO.com. I watch, I lurk, I read, and eventually I find something that really inspires me.

The elevator pitch for the site is that it is a directory of JavaScript libraries with examples, CDN links, statistics, and sometimes videos about each library.

Behind the scenes, after sifting through github, twitter, hacker news, pineapple, and an endless stream of sites and finding something exciting, I begin the slow process of adding a library to the site. Slow is a relative term, but for me, in this context, it means anywhere from 30 minutes to a few days. Adding a library to the site is a purposefully manual process that requires I actually spend some time with the library, writing an example for it, categorizing it as best I can, and sometimes even creating a video about it.

This slow process is a huge bottleneck for updates on JSOO, and boy, do I hear about it. However, it also keeps the site from becoming just a directory of github links and it keeps the single curator excited about maintaining the site.

## Examples and submitting your library

There are currently ~~401~~ ~~405~~ 409 examples on the site… almost one for every day it has been online. There are 79 libraries in the “Needed Examples” section where visitors can submit a gist or fiddle for that library and are encouraged to “include your Twitter handle or any other marketing you may like to, but keep it simple”. Lastly, there is a section for submitting your own library. Not all libraries submitted are added to the site, but they are given immediate priority, and if they are a fit, added to the queue. There is no editorial, no blog, no opinion at all other than hoping every visitor feels like this:

```
```When I browse this [http://t.co/hnfqKoQqdB](http://t.co/hnfqKoQqdB) I just swoon everytime. It's such an awesome JS resource.

— ★ (@SoHiggo) [November 15, 2013](https://twitter.com/SoHiggo/statuses/401434949296738304)


Beyond the very manual process of adding a library, the site is also a chance for me to experiment with all sorts of tech and see in real time how it performs under a moderate load. Originally launched as a .NET application most of what you see today is running node.js under iisnode using Express w/ Jade templates (moving to doT.js as I write), a gulpjs build process, a homegrown CMS using AngularJS and VB.NET (gasp!), and a Lucene.NET search application in C#.

## About
[
Joe Maddalone ](http://joemaddalone.com)

Joe is a father of five, lives in Chicago, works as a freelance web developer, shares coding tutorials on youtube, and codes for fun when not for work.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 13 comments

BastianJanuary 29th, 2014 at 04:14Robert Nyman [Editor]January 29th, 2014 at 04:44Mte90January 29th, 2014 at 08:54Joe MaddaloneJanuary 29th, 2014 at 09:19Mitchell SimoensJanuary 29th, 2014 at 08:57Joe MaddaloneJanuary 29th, 2014 at 09:27jerome etienneJanuary 29th, 2014 at 10:03Ivan DejanovicJanuary 29th, 2014 at 12:18Sean SmithJanuary 31st, 2014 at 08:49Joe MaddaloneJanuary 31st, 2014 at 09:44Nico BelgraverFebruary 2nd, 2014 at 04:41dbcFebruary 3rd, 2014 at 06:29MMFebruary 4th, 2014 at 06:09