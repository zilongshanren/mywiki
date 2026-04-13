---
title: Announcing Boot to Gecko (B2G) – Booting to the Web – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2011/07/announcing-boot-to-gecko-b2g-booting-to-the-web/
author: Robert Nyman
published: '2011-07-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Mozilla recently announced the [Boot to Gecko (B2G) Project](https://wiki.mozilla.org/B2G) which is a project towards the goal of building a complete, standalone operating system for the open web.


## The aim of B2G

The idea is that open web technologies can supersede single vendor control over application environments, and instead use something that will be open for all and consistent across the board. The first main aim is mobile/tablet devices and to be able in such an environment to give access through web technologies to all the capabilities native applications have.

The project is in a very early stage right now, but we believe in communicating this early and getting as much valuable input, help and suggestions as possible to make this out to be all it can be.

## Areas of work

The main areas we see right now that will need a lot of work and input are:

- New web APIs
- Build prototype APIs for exposing device and OS capabilities to content (Telephony, SMS, Camera, USB, Bluetooth, NFC, etc.)
- Privilege model
- Making sure that these new capabilities are safely exposed to pages and applications
- Booting
- Prototype a low-level substrate for an Android-compatible device
- Applications
- Choose and port or build apps to prove out and prioritize the power of the system.

## Helping out with B2G

Let me re-emphasize that the work with B2G has just begun. As you understand, the possibilities, work and collaboration being needed here are huge, and being open about the whole process, we would love to get your thoughts, suggestions, ideas, practical help or anything else you can think of to make this happen!

Feel free to comment below or add your takes to the [Booting to the Web thread](http://groups.google.com/group/mozilla.dev.platform/browse_thread/thread/7668a9d46a43e482?pli=1). Please read more in the [B2G](https://wiki.mozilla.org/B2G) page about what you can do to contribute.

## FAQ about B2G

To cover some common ground and questions, here are the [Frequently Asked Questions for B2G](https://wiki.mozilla.org/B2G/FAQ):

### What is Boot to Gecko?

Boot to Gecko (B2G) is an early-stage, exploratory project with the goal of building a complete, standalone operating system for the open web. It is not a product offering, but if successful, could form the basis for one.

### When can we expect to see something?

We’re very early in the project, soliciting suggestions and contributions from a lot of people. As we have more specific estimates for different pieces of functionality, they’ll be shared widely.

### What is the size of the team working on this project?

It’s very small right now: just 3 people working part time, but we’re looking to ramp up and as an open project we are actively inviting participation of developers, designers, and others from across the Web. We’re seeing lots of excitement and offers of help already, and we’re also obviously leaning heavily on the existing Gecko and Firefox mobile work.

### Why are you doing this now?

We believe that the next frontier for Web applications is full device integration, so that Web developers have the same capabilities as those building for OS-specific stacks.

### What does it mean for your relationships with Apple, Google, Microsoft?

We don’t expect that it will affect our relationships with other organizations.

### Does this replace work that’s already being done on Web APIs for desktop and mobile?

We are already pushing hard on new Web APIs, and have been for some time. We’ll continue to implement and standardize new APIs for Web content while the B2G project ramps up.

### How is this different than the Webian Shell project?

The Webian shell is an impressive project even in its early stages. Where Webian is focused on a Web-centric desktop experience, we’re focused on extending the Web to include more of what is traditionally the domain of OS-specific code. We think we can work together on a bunch of things, and we’re looking forward to it.

### How is this different from Chrome OS?

We’re aiming at mobile/tablet devices rather than a notebook form factor. This is an early-stage project to expose all device capabilities such that infrastructure like phone dialers can be built with Web APIs, and not only “high level” apps like word processors and presentation software. We will of course be happy to work with the Chrome OS team on standards activities, and indeed to share source code where appropriate.

### Are OEMs interested in B2G?

This is an early-stage project. We just got started, so we haven’t had any of those discussions yet. If an OEM shares our vision of a standard and open platform from top to bottom, we’d be happy to work together to get such a platform into the hands of users.

### Whose hardware will you support?

We’ll be selecting initial hardware for hackability and general availability, but we haven’t settled on that yet. A Tegra 2 device is likely to be selected, due to its support for VP8 hardware acceleration. Over time we expect that B2G will work on the majority of devices that support modern Android versions.

### Will this mean a Firefox Phone?

We don’t have any plans to build or distribute a custom device.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 27 comments

StephenJuly 27th, 2011 at 09:21SkouaJuly 27th, 2011 at 09:53VaremenosJuly 27th, 2011 at 09:58VaremenosJuly 27th, 2011 at 09:57Robert Nyman [Mozilla – post author]July 27th, 2011 at 10:15JossJuly 27th, 2011 at 20:20markmbJuly 30th, 2011 at 04:47louisremiAugust 1st, 2011 at 02:54Stefan ConstantinescuAugust 1st, 2011 at 22:37Robert NymanAugust 2nd, 2011 at 01:45Ashish TyagiAugust 2nd, 2011 at 03:16Robert NymanAugust 2nd, 2011 at 04:41DerekAugust 2nd, 2011 at 15:45Robert NymanAugust 2nd, 2011 at 15:55MJaeAugust 3rd, 2011 at 22:11Robert NymanAugust 4th, 2011 at 10:01aleksanderSeptember 13th, 2011 at 09:48Robert NymanSeptember 13th, 2011 at 10:02aleksanderSeptember 13th, 2011 at 12:52Robert NymanSeptember 19th, 2011 at 02:36robertSeptember 18th, 2011 at 05:10Robert NymanSeptember 19th, 2011 at 02:36OvidiuSeptember 23rd, 2011 at 10:59Robert NymanSeptember 26th, 2011 at 01:00alexSeptember 27th, 2011 at 02:43Robert NymanSeptember 27th, 2011 at 02:52alexSeptember 27th, 2011 at 03:17