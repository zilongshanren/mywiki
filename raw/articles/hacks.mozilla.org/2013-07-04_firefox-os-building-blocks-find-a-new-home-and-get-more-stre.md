---
title: Firefox OS Building Blocks find a new home, and get more streamlined – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/firefox-os-building-blocks-find-a-new-home-and-get-more-streamlined/
author: Arnau March
published: '2013-07-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One year ago we started working on what is known as “Firefox OS Building Blocks” with the idea of creating a set of reusable components in HTML/CSS which could be used to speed up markup development in pre-installed Firefox OS apps.

When we started to implement the UI of Firefox OS’ core apps, we soon realized that the more components we were creating, the more classes, roles and data types we had to control to build a view using Building Blocks, so we had the need to start documenting our progress in a consistent and scalable way.

Firefox OS’ code is stored in github as part of the [Gaia](https://github.com/mozilla-b2g/gaia) project, as you may know, so we created a new repository there for our components and used the magic of “gh-pages” to preview the generated examples. We also used that approach to keep track of the reviewing status for each Building Block so it would be possible for devs and project contributors to know if it was ready to use. We defined some states, from “Review pending” to “Stable”, and provided that information through a website.

Here’s a screenshot on how the Building Blocks site looked like at that moment:

## “Building Firefox OS” is born!

Making Building Blocks publicly available online and being able to track their status was a great step forward because for the first time in the project it was possible for anyone in the team to know the step in the reviewing process for each Building Block. But we still had some problems, being the most important one having two different repositories to upload and maintain Building Blocks: in the official repo, Gaia, and in the Building Blocks repo. We decided to discontinue that last one and keep everything related to Building Blocks available through the official Gaia repository.

This change made our documentation source to become obsolete so we thought it was necessary to create a new site to replicate the one we had previously linked with github. I started working together with @[sergiov](https://twitter.com/sergiov), UX designer at Telefónica Digital, in the new site structure. We got a lot of inspiration from [Twitter Bootstrap](http://twitter.github.io/bootstrap/), and we decided to design the new Building Blocks documentation site using Firefox OS’ Building Blocks themselves. We wanted to know if it was possible to use Building Blocks not only for its main purpose, that’s creating phone applications, but also as a base to create a standard web site. You know: The web is the platform! That was the beginning of [Building Firefox OS](http://buildingfirefoxos.com) (BFFOS)

@sergiov wanted to contribute to the site updating content, so I replicated it using WordPress. That also gave us an easy way to include comments for each section and we started to receive feedback from users. We traded that for a slower performance.

## Adding more content and resources

The next step after documenting Building Blocks was improving UI transitions and how they were displayed in the site. At that moment we had a pdf document describing how these transitions should be in Firefox OS apps, but the problem is it’s usually difficult to transmit things like UI interactions and animation timings from design to development teams, so we added a new section to the site using real CSS transitions which let us to better communicate them.

Here’s a page from the original PDF document describing one transition…

… And here’s a page for you to [check that same transition in CSS with code snippets attached](http://buildingfirefoxos.com/transitions/app-invokes-app.html).

We were really happy with the progress we made in just a few months taking into account [Building Firefox OS](http://buildingfirefoxos.com) started as a personal project. From the first Building Blocks site, where we tried to provide a tool to share the implementation status for each Building Block, to a full-fleshed site with all Building Blocks we were using to build Firefox OS core apps, together with UI transitions and design resources.

We published [BFFOS](http://buildingfirefoxos.com) and started to use it as an internal tool to have everything related to Firefox OS’ UI in one place. We also decided to leave it open just in case someone found it as useful as we did, but without making promotions at any level. To our surprise a lot of users found the content we were offering good enough to share it, so we hit 20,000 visits during the first weekend.

## Looking for a new home for Building Blocks

Arrived to this point, and given that Mozilla had plans to document Firefox OS’ UI, it made sense for us to talk and try to make a joint effort in order to provide this through [BFFOS](http://buildingfirefoxos.com). We were concerned about the scalability of the site and the contribution model, so we agreed to work in improving that, moving back to github to solve these two concerns.

We started the 4th redesign of [BFFOS](http://buildingfirefoxos.com), this time using Jekyll and some web templates from Mozilla as a starting point. Now we are proud to announce that what we started as a small personal project is a reality thanks to the help of a lot of great people and the huge support provided by Mozilla to make this happen.

## Collaborate with us!

But this is just the beginning! We’re working hard with the solely objective of making all the information available through [BFFOS](http://buildingfirefoxos.com) truly useful for the dev and design community. We want to make all Building Blocks compatible with all modern browsers, we want to provide you with the javascript code needed to easily bring Building Blocks to life, we want to deliver new UI themes and component skins…

We invite you to collaborate with us. Feel free to submit any improvement or request to the [site repo](https://github.com/buildingfirefoxos/site/) and help us to make [Building Firefox OS](http://buildingfirefoxos.com) bigger and better!

## About Arnau March

Arnau March is a "designloper" working for Telefonica. Not good enough to tell you why a button should be right aligned in a header, neither to code perfect javascript. But he is the guy who can apply visual solutions to programming limitations.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 3 comments

Victor PorofJuly 4th, 2013 at 07:15Gervase MarkhamJuly 5th, 2013 at 03:41Robert Rex EDWARDSJuly 6th, 2013 at 21:18