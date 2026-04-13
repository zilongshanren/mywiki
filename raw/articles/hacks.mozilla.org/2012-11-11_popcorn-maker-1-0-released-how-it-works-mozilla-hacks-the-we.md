---
title: Popcorn Maker 1.0 released – how it works – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/11/popcorn-maker-1-0-released-how-it-works/
author: Bobby Richter
published: '2012-11-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This week Mozilla is in London at the [Mozilla Festival 2012](http://mozillafestival.org/). A year ago at last year’s Festival, we released [Popcorn.js 1.0](https://blog.mozilla.org/blog/2011/11/05/popcorn-1-0-launch-and-world-premier-of-one-millionth-tower/), and with it a way for filmmakers, journalists, artists, and bloggers to integrate audio and video into web experiences. Popcorn has since become one of the most popular ways to build time-based media experiences for the web. It has proven to be uniquely powerful for bespoke web demos, films, visualizations, etc. This year, we’ve come to the Mozilla Festival with an even bigger 1.0 release: [Popcorn Maker 1.0](https://popcorn.webmaker.org/).

## Popcorn.js and Popcorn Maker

With Popcorn.js, and its plugin ecosystem, we created a tool for developers. Popcorn lets developers work dynamically using timing information from web media, using [a simple API and plugin system](http://popcornjs.org/). With Popcorn Maker we wanted to go further and give this same power to bloggers, educators, remixers, and artists — web makers.

![](../../assets/db4bdc1463e8496e.jpg)


At its core, Popcorn Maker is an HTML5 web app for combining web media with images, text, maps, and other dynamic web content. Its appearance is unique, but not unfamiliar, providing a timeline-based video editing experience for the web. Once created, Popcorn Maker hosts remixes as simple HTML pages in the cloud, which can be shared or embedded in blogs or other sites. Furthermore, every remix provides a “Remix” button, allowing anyone watching to become a creator themselves by using the current remix as a base project for their own creation. This “view source” experience for web media is a key aspect of Popcorn Maker’s goals as part of the larger Mozilla Webmaker project.

On a technical level, Popcorn Maker is the combination of a number of separate projects, each heavily influenced by the [“12 factor” philosophy](http://www.12factor.net/): a node.js-based web service called Cornfield; a JavaScript framework for creating highly-interactive web apps; and Popcorn.js, with a set of custom Popcorn.js plugins.

## Coming from Butter

![](../../assets/69652c6dec57c844.jpg)


When we first started we thought we’d create a simple library named Butter, and that Popcorn Maker would be injectable — something you would add to existing web pages, like a toolbar. Many of the original ideas for Popcorn Maker were taken from an early prototype created by Rick Waldron, Boaz Sender, and Al MacDonald of [Bocoup](http://www.bocoup.com/). Over time these ideas evolved, Seneca College and [CDOT](http://cdot.senecac.on.ca/) got involved — bringing their heavy experience with web media and Pocorn.js — and more prototypes ensued. Soon it became clear that what was really needed was a full web app: an infrastructure including client, server, and a community.

This realization occurred as the Popcorn Maker team continued to grow. More developers joined our team some of whom brought much-needed design experience with them. [Ocupop](http://ocupop.com/) was consulted to enhance the design of the project, and gave us the same expertise that was used to produce the branding for HTML5.

![](../../assets/2e29839946601b44.png)


## Using LESS for CSS

Thanks to talented designer-hacker hybrids like [Kate Hudson](https://twitter.com/k88hudson), Popcorn Maker’s design became modern and responsive. We worked with her to integrate [LESS](http://lesscss.org/) — a dynamic stylesheet language which compiles to CSS. LESS made challenges like cross-browser compatibility — something key to Popcorn Maker’s goals — less painful. It also allowed much more flexibility for a rapid prototype approach to our UI. Consequently, a significant amount of our CSS is constructed in functions and stored in variables, both of which are included in files throughout our style implementation. We can make changes that let us try new approaches very quickly, touching and creating as little boilerplate CSS as possible.

## Popcorn Media Wrappers

Of course, in order to complete the features we desired, we needed to extend Popcorn.js with new features. One such feature is Popcorn Media Wrappers, which wrap non-HTML5 media with an interface and set of behaviours that allow them to be used exactly like HTML5 video and audio elements. By building wrappers for YouTube, Vimeo, and SoundCloud, we were able to standardize all our media code on the HTML5 media interface. More wrappers are in production, allowing more types of media to be included in future releases, and the current wrappers will ship as part of Popcorn.js 1.4 later this year.

## Evolving into a modern tool

Eventually, Butter and its constituents allowed us to present a full-featured, responsive, end-user tool using nothing more than HTML, CSS, and JavaScript. Currently, Butter uses a modular development environment provided by require.js, and provides a UI toolkit with widgets that were used to build the timeline, scrubber, editors, dialogs and more. In cooperation with require.js’ text plugin, Document Fragments are used to allowed us to build all of our UI in static HTML, and load and render it dynamically at runtime. This approach lets us treat our HTML as it was meant to be treated (i.e., as layout), but also include it in our source tree to be referenced and linted like anything else.

While building Butter was a large part of the execution of our app, it comprises only a portion of Popcorn Maker. Cornfield, Popcorn Maker’s server, allows users to save and publish their content, completing the Popcorn universe. It uses node.js, Express, Jade templates, and Amazon S3 to provide a RESTful API and hosting environment for Butter. To avoid the thorny issue of user authentication and credential management, Cornfield leverages Mozilla Persona. During development, attempting to use Persona exposed the need to build the express-persona node module to help make Persona work more easily in [Express](https://github.com/jbuck/express-persona).

## Based on community input

The Popcorn Maker team owes a great deal of gratitude to its community and users. Their feedback heavily influenced the direction of Popcorn Maker. The most successful and compelling Popcorn.js demos we saw used the video as a canvas, on which to place pieces of the web dynamically. Further, we found that our users wanted to embed their projects — not just host them. These insights were instrumental in moving our focus to creating embeddable content, rather than full-page content.

Gathering feedback from our users also influenced our development. In Popcorn Maker we’ve experimented with user feedback collection and JavaScript crash reporting, both built directly into the web app. The app’s Feedback button lets users submit general feedback, which is then stored as JSON in S3. Through such feedback we’ve been able to get valuable information about issues users have encountered and ideas for new features.

## JavaScript crash reports

Even more significant has been our experiment with JavaScript crash reports. This technique is used to great effect with Mozilla’s native development, for products like [Firefox and it s crash stats](https://crash-stats.mozilla.com/products/Firefox). However, this technique is not often applied to JavaScript web apps. We use `window.onerror`

to detect top-level exceptions being thrown in our code, and present the user with a dialog to allow them to submit an anonymous report, optionally with details about what they encountered. We log various types of edge cases (e.g., `null`

node access in the DOM by wrapping DOM methods) and send this data with the report. This has been an incredible source of data for our team. Since our [0.9 release for the TED talk release](http://blog.ted.com/2012/10/19/meet-popcorn-maker-beau-lotto/) we’ve fixed more than a dozen crash bugs, almost all of which our developers were never able to hit locally.

## Influenced by other Mozilla projects

The development of Popcorn Maker was also heavily influenced by processes used on other Mozilla projects. In particular an emphasis on automation, tooling, and open source best practices. We accelerated our development by using linting in all of our code, from JavaScript (jshint), to CSS (csslint), to HTML, where we created [a client-server solution based on the HTML5 parser](https://github.com/mozilla/html5-lint). We use many automation systems, from [botio](https://github.com/arturadib/botio), to TravisCI, to Jenkins to run our tests and help us trust the rapid pace of code changes. Most importantly, we also employed a two-stage code review process, similar to Firefox’s Peer-Review and Super-Review. By having every patch reviewed twice, we not only reduced regressions, but also helped grow our developer team by ensuring that multiple people understood every change.

Popcorn Maker has already touched a large community and is the result of the hard work and collective influence of a growing team of dedicated developers, thinkers, and increasingly active community members. We’re incredibly proud to be releasing a year’s worth of work today with the 1.0 launch. The only question left is what you’ll make with it – [https://popcorn.webmaker.org](https://popcorn.webmaker.org)!

## More information on the code and development process

For more info about the code and development team/process:

### Repositories

### Bug Tracker

### IRC

### Instances

## About Bobby Richter

Bobby is the Tech Lead for Popcorn Maker, working out of Toronto for the Mozilla Foundation. He can be reached on Twitter as [@secretrobotron](https://hacks.mozilla.org/twitter.com/secretrobotron).

## 7 comments

arnoldNovember 11th, 2012 at 11:37Robert NymanNovember 11th, 2012 at 14:24Johan SundströmNovember 11th, 2012 at 17:09Robert NymanNovember 12th, 2012 at 05:18Johan SundströmNovember 11th, 2012 at 17:17TapoNovember 12th, 2012 at 03:05Robert NymanNovember 12th, 2012 at 06:01