---
title: 'Introducing Brick: Minimal-markup Web Components for Faster App Development
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/08/introducing-brick-minimal-markup-web-components-for-faster-app-development/
author: Leon Zhang
published: '2013-08-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Those of you on the cutting HTML5 edge may have already heard of the exciting [Web Components](http://www.w3.org/TR/2013/WD-components-intro-20130606/) specification. If you haven’t, [you’ll probably want to read up on what makes this so exciting](http://techcrunch.com/2013/05/19/google-believes-web-components-are-the-future-of-web-development/), but long story short, Web Components promise to open up a new realm of development by letting web developers write custom, reusable HTML tags. Think of them as JavaScript plugins without the need for additional code initialization or boilerplate markup/styling.

Unfortunately, it will be a while before we see native browser support for the spec, but that doesn’t mean developers can’t start taking advantage of the component concept now, thanks to [Google’s Polymer framework](http://www.polymer-project.org/) and [Mozilla’s x-tags polyfill library](https://hacks.mozilla.org/2013/05/speed-up-app-development-with-x-tag-and-web-components/) (both X-Tag and Polymer share the same low-level, Web Component polyfills).

We’re proud to announce the beta release of [Brick](http://mozilla.github.io/brick/), a cross-browser library that provides new **custom HTML tags** to abstract away common user interface patterns into easy-to-use, flexible, and semantic Web Components. Built on Mozilla’s [x-tags](http://www.x-tags.org/) library, Brick allows you to plug simple HTML tags into your markup to implement widgets like sliders or datepickers, speeding up development by saving you from having to initially think about the under-the-hood HTML/CSS/JavaScript.

## Putting Brick into Action

Say that you wanted to implement a cross-browser, mobile-friendly calendar widget in your application. With current JavaScript plug-ins, such as jQuery UI, this would require putting boilerplate, non-semantic markup into your HTML, as well as explicitly initializing and managing it through JavaScript. However, with Brick, you can implement such a component simply by adding a custom HTML tag that you can treat as a normal native tag.

For our calendar example, this means just including the library’s CSS and Javascript file in your application, then adding the following tag to your markup:


which creates a DOM element that looks like this:

![](../../assets/9e378abd6ef469f9.png)


Want to edit how the component behaves, such as by adding navigational controls or pre-selecting a date? Like any other native tag, you can change how a component behaves just by changing the attributes of the tag!


![](../../assets/eb85c6e5579ddff1.png)


## Available Bricks

At the time of writing, Brick consists of thirteen different tags, most of which are completely independent of one another, and can even be downloaded separately instead of a single bundle.

Some tags abstract away complex widgets into simple HTML tags, such as:

[<x-calendar>](http://mozilla.github.io/brick/demos/calendar/index.html)(calendars, as seen from the example)[<x-deck>](http://mozilla.github.io/brick/demos/deck/index.html)(a cyclable slide gallery)[<x-tooltip>](http://mozilla.github.io/brick/demos/tooltip/index.html)(exactly as it sounds).

Others are cross-browser polyfill implementations of existing native not-yet-globally-supported elements, such as:

which polyfill `<input type="range">`

and `<input type="date">`

, respectively. Still others are structural components simplifying the styling and markup of certain components, such as [<x-layout>](http://mozilla.github.io/brick/demos/layout/index.html), which ensures that content, headers, and footers can fill a container element without explicit styling markup.

Each tag comes with a flexible attribute/JavaScript API and can be fully styled to match your application.

## Start Building with Bricks

Want to start using components in your own applications? Head to [mozilla.github.io/brick](http://mozilla.github.io/brick/) to download a release bundles, view demos, and read the documentation for the available tags. Alternatively, visit the [Brick Github page](https://github.com/mozilla/brick/) to view the source code and contribute to the effort!

The library is still in a beta release, so we appreciate all user feedback! Brick is already [starting to crop up in the wild](https://developer.mozilla.org/en-US/docs/Web/Apps/app_layout/responsive_design_building_blocks), so we’d love to hear about how you’re using it!

## About
[
Leon Zhang ](http://www.contrib.andrew.cmu.edu/~lwzhang/)

I am a Mozilla WebDev Intern working with the Apps/DevEcosystem team for Summer 2013. I'm currently a student at Carnegie Mellon University, where I study Computer Science/Human Computer Interaction.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 45 comments

Lech RzedzickiAugust 27th, 2013 at 06:50PotchAugust 27th, 2013 at 13:15TAugust 28th, 2013 at 16:30RobotAugust 30th, 2013 at 10:39Rand McRandersonSeptember 2nd, 2013 at 09:44PhunkyAugust 27th, 2013 at 06:56PotchAugust 27th, 2013 at 13:17PhunkyAugust 29th, 2013 at 02:43PhunkyAugust 27th, 2013 at 07:04barduAugust 27th, 2013 at 08:03Angelina FabbroAugust 27th, 2013 at 10:23barduAugust 27th, 2013 at 15:28romulo santosSeptember 15th, 2013 at 12:11PotchAugust 27th, 2013 at 13:13Ted DrakeAugust 27th, 2013 at 08:04Leon ZhangAugust 27th, 2013 at 14:17Leon ZhangAugust 27th, 2013 at 14:18PotchAugust 27th, 2013 at 14:47Gerardo CapielAugust 27th, 2013 at 08:45PotchAugust 27th, 2013 at 14:53James MeldrumAugust 27th, 2013 at 09:05FredAugust 27th, 2013 at 13:56ArasAugust 27th, 2013 at 12:04PixnBitsOrgAugust 27th, 2013 at 13:08PotchAugust 27th, 2013 at 14:49Igor CostaAugust 27th, 2013 at 14:07NobodyAugust 27th, 2013 at 14:44RichardAugust 28th, 2013 at 12:33PotchAugust 29th, 2013 at 11:27Alexander VoroninAugust 27th, 2013 at 23:53Mark McDonnellAugust 28th, 2013 at 01:19PotchAugust 29th, 2013 at 11:31Semih AkalinAugust 28th, 2013 at 03:47OkAugust 28th, 2013 at 07:00PotchAugust 29th, 2013 at 11:34Zach MorenoAugust 28th, 2013 at 08:03PotchAugust 29th, 2013 at 11:35mintypoohsAugust 28th, 2013 at 10:14garbasAugust 28th, 2013 at 11:06niutechAugust 28th, 2013 at 15:21Zach MorenoAugust 29th, 2013 at 13:56niutechAugust 30th, 2013 at 15:05Rand McRandersonSeptember 2nd, 2013 at 09:48pdSeptember 8th, 2013 at 10:10niutechSeptember 8th, 2013 at 16:22