---
title: An easier way of using polyfills – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/11/an-easier-way-of-using-polyfills/
author: Andrew Betts
published: '2014-11-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Polyfills are a fantastic way to enable the use of modern code even while supporting legacy browsers, but currently using polyfills is too hard, so at the FT we’ve built a new service to make it easier. We’d like to invite you to use it, and help us [improve it](https://github.com/Financial-Times/polyfill-service).

![Image from https://www.flickr.com/photos/hamur0w0/6984884135](../../assets/76bae723033170d9.jpg)


*More pictures, they said. So here’s a unicorn, which is basically a horse with a polyfill.*

## The challenge

Here are some of the issues we are trying to solve:

- Developers do not necessarily know which features need to be polyfilled. You load your site in some old version of IE beloved by a frustratingly large number of your users, see that the site doesn’t work, and have to debug it to figure out which feature is causing the problem. Sometimes the culprit is obvious, but often not, especially when legacy browsers also lack good developer tools.
- There are often multiple polyfills available for each feature. It can be hard to know which one most faithfully emulates the missing feature.
- Some polyfills come as a big bundle with lots of other polyfills that you don’t need, to provide comprehensive coverage of a large feature set, such as ES6. It should not be necessary to ship all of this code to the browser to fix something very simple.
- Newer browsers don’t need the polyfill, but typically the polyfill is served to all browsers. This reduces performance in modern browsers in order to improve compatibility with legacy ones. We don’t want to make that compromise. We’d rather serve polyfills only to browsers that lack a native implementation of the feature.

## Our solution: polyfills as a service

To solve these problems, we created the polyfill service. It’s a similar idea to going to an optometrist, having your eyes tested, and getting a pair of glasses perfectly designed to correct your particular vision problem. We are doing the same for browsers. Here’s how it works:

- Developers insert a script tag into their page, which loads the polyfill service endpoint.
- The service analyses the browser’s user-agent header and a list of requested features (or uses a default list of everything polyfillable) and builds a list of polyfills that are required for this browser
- The polyfills are ordered using a graph sort to place them in the right dependency order.
- The bundle is minified and served through a CDN (for which we’re very grateful to Fastly for their support)

Do we really need this solution? Well, consider this: [Modernizr](http://modernizr.com/) is a big grab bag of feature detects, and all sensible use cases benefit from a custom build, but a large proportion of Modernizr users just use the default build, often from cdnjs.com or as [part of html5boilerplate](https://github.com/h5bp/html5-boilerplate/blob/master/src/index.html). Why include Modernizr if you aren’t using its feature detects? Maybe you misunderstand the purpose of the library and just think that Modernizr “fixes stuff”? I have to admit, I did, when I first heard the name, and I was mildly disappointed to find that rather than doing any actual modernising, Modernizr actually just defines modernness.

The polyfill service, on the other hand, does fix stuff. There’s really nothing wrong with not wanting to spend time gaining intimate knowledge of all the foibles of legacy browsers. Let someone figure it out once, and then we can all benefit from it without needing or wanting to understand the details.

## How to use it

The simplest use case is:

This includes our default polyfill set. The default set is a manually curated list of features that we think are most essential to modern web development, and where the polyfills are reasonably small and highly accurate. If you want to specify which features you want to polyfill though, go right ahead:

```
```

If it’s important that you have loaded the polyfills before parsing your own code, you can remove the `async`

and `defer`

attributes, or use a script loader (one that doesn’t require any polyfills!).

## Testing and documenting feature support

This table shows the polyfill service’s effect for a number of key web technologies and a range of popular browsers:

The full list of features we support is shown on our feature matrix. To build this grid we use [Sauce Labs’](https://saucelabs.com) test automation platform, which runs each polyfill through a barrage of tests in each browser, and documents the results.

## So, er, user-agent sniffing? Really?

Yes. There are several reasons why [UA analysis](https://hacks.mozilla.org/2013/09/user-agent-detection-history-and-checklist/) wins out over feature detection for us:

- In some cases, we have multiple polyfills for the same feature, because some browsers offer a non-compliant implementation that just needs to be bashed into shape, while others lack any implementation at all. With UA detection you can choose to serve the right variant of the polyfill.
- With UA detection, the first HTTP request can respond directly with polyfill code. If we used feature detection, the first request would serve feature-detect code, and then a second one would be needed to fetch specific polyfills.

Almost all websites with significant scale do UA detection. This isn’t to say the stigma attached to it is necessarily bad. It’s easy to write bad UA detect rules, and hard to write good ones. And we’re not ruling out making a way of using the service via feature-detects (in fact there’s an issue in our tracker for it).

## A service for everyone

The service part of the app is maintained by the FT, and we are working on expanding and improving the tools, documentation, testing and service features all the time. The source is freely available [on GitHub](https://github.com/Financial-Times/polyfill-service) so you can easily host it yourself, but we also host an instance of the service on cdn.polyfill.io which you can use for free, and our friends at [Fastly](https://www.fastly.com) are providing free CDN distribution and SSL.

We’ve made a platform. We need the community’s help to populate it. We already serve some of the best polyfills from [Jonathan Neal](http://www.jonathantneal.com/), [Mathias Bynens](https://mathiasbynens.be/) and others, but we’d love to be more comprehensive. Bring your polyfills, improve our tests, and make this a resource that can help move the web forward!

## About Andrew Betts

Director of FT Labs, which develops and promotes experimental web technologies at the Financial Times

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 11 comments

PetterNovember 6th, 2014 at 06:51BartNovember 7th, 2014 at 11:38Conor LuddyNovember 6th, 2014 at 07:02AlfonsoNovember 6th, 2014 at 09:52marioNovember 6th, 2014 at 12:09DorianNovember 6th, 2014 at 13:17BrentonNovember 6th, 2014 at 15:08Farid Nouri NeshatNovember 7th, 2014 at 05:09Oisin G.November 10th, 2014 at 09:03ingeeNovember 27th, 2014 at 10:25Robert Nyman [Editor]November 28th, 2014 at 10:33