---
title: 'A Web for Everyone: Interviews with Web Practitioners — David Walsh – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-david-walsh/
author: Justin Crawford
published: '2016-09-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’ve heard now from [Rachel Andrew](https://hacks.mozilla.org/2016/08/a-web-for-everyone-interviews-with-web-practitioners-rachel-andrew/), [Chris Coyier](https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-chris-coyier/), and [Belén Albeza](https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-belen-albeza/). Each of these great web developers offered ideas for accomplishing cross-browser compatibility. The fourth interviewee in our web-compatibility interview series brings some new tools to the table.

David Walsh ([@davidwalshblog](https://twitter.com/davidwalshblog)) taught himself HTML, CSS and JavaScript at a young age, and soon turned those skills into a vocation. He started blogging about front-end development after landing his first job in the field. Now, a decade later, [David’s blog ](https://davidwalsh.name)is daily reading for tens of thousands of web developers who go there for tips, tutorials, and reflections about the life of a developer. David has spoken at JavaScript conferences around the world including LondonAJAX and BrazilJS. He works as a front-end developer and evangelist at Mozilla.

![David Walsh](../../assets/58706658f6c916ff.jpg)


**David, what does cross-browser compatibility mean to you?**

Cross-browser compatibility means functionality and design working across not only different desktop browsers but also browser apps on different mobile devices, sometimes extending to gaming machines like the Xbox One.

**How often do you have to think about cross-browser compatibility? Have you found ways to work that allow you to reduce the amount of time you think about it compared to when you were less experienced?**

Working with some bleeding edge APIs at Mozilla, including [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers), [WebVR](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API), and [A-Frame](https://aframe.io/), cross-browser compatibility is something I have to think of often.

Cross-browser compatibility changes meaning but has always been present.


Earlier in my career I would also think of cross-browser compatibility but it was a different environment: IE6 had stalled, [user-agent checking](https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent) was commonplace, and both WebKit/Safari and Firefox were implementing features with [their own prefixes](https://developer.mozilla.org/en-US/docs/Glossary/Vendor_Prefix), making using new features difficult.

Cross-browser compatibility changes meaning but has always been present.

**What motivates you to make the extra effort to build a cross-browser compatible site?**

Mozilla properties are visited by millions of users on different browsers, devices, and variant versions of each, meaning that cross-browser compatibility is a must. Also the idea that everyone deserves the same experience if possible.

Everyone deserves the same experience if possible.


**Could anything convince you not to make that effort? What?**

I suspect that some developers and/or organizations may see cross-browser compatibility as a bloat in time and cost. Luckily, the browsers have come together on the importance of standards and are roughly on the same timeline with features, so unless you’re using bleeding edge capabilities, cross-browser compatibility isn’t as difficult as it used to be.

**Have you ever had to convince a client or boss that building a cross-browser compatible site was important? How’d you do it?**

Absolutely, especially in the days that I worked at a small agency. Cross-browser compatibility was seen as a time-consuming task, one that the analytics didn’t justify. I made the case that cross-browser compatibility would “future-proof” sites in case new browsers came along, and I was right: Chrome debuted with a WebKit engine, quickly took hold. Mac users (Safari) were no longer the only users of the WebKit engine and set of style/feature differences.

**Did you ever have a specific experience that caused you to take cross-browser compatibility more seriously with your next project?**

Yes — the growth of Chrome! Chrome not only used WebKit but then moved to its own engine and started implementing features on its own timeline. This all seemed to happen fairly quickly and it was very eye-opening to me to see!

**You’ve blogged a lot about tools — for example, just this summer you talked about **[Slimer.js](http://slimerjs.org/), [Phantom.js](http://phantomjs.org/), and [Wraith](http://bbc-news.github.io/wraith/), among many others. Which tools (or techniques) would be at the top of your list for coding compatible sites or testing for compatibility?

Selenium testing is a great place to start, regardless of which abstraction you use on top of it. I really liked [Slimer.js](http://slimerjs.org/), [Phantom.js](http://phantomjs.org/), and [Wraith](http://bbc-news.github.io/wraith/), as you’ve mentioned. The truth is new tools are popping up all the time!

**What would you tell a brand new developer graduating from a coding bootcamp about cross-browser compatibility?**

I would tell them they’re incredibly lucky to have missed the early days of browsers doing their own thing! They should start with the mindset that cross-browser compatibility (outside of bleeding edge features) is a must, and that if they start with that attitude, they’d always have it.

**Tips from David’s interview**

- Don’t overestimate the difficulty of making a site compatible across browsers. Cross-browser compatibility isn’t as hard as it used to be.
- Try automating parts of your browser testing using command-line tools like
[Slimer.js](http://slimerjs.org/),[Phantom.js](http://phantomjs.org/), and[Wraith](http://bbc-news.github.io/wraith/). - Functional testing with
[Selenium](http://docs.seleniumhq.org/)— using multiple browsers, of course — can make it easier to discover browser-breaking bugs in new code.

## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.