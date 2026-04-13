---
title: Creating the future of mobile with Firefox OS – resources, docs and more! –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/10/creating-the-future-of-mobile-with-firefox-os/
author: Robin Hawkes
published: '2012-10-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Just under a month ago I wrote a personal post about [my thoughts on Firefox OS](http://rawkes.com/articles/there-is-something-magical-about-firefox-os) and why I think there is something ‘magical’ about what it stands for and the possibilities it brings to the table. This post is a follow-up that aims to cover much of the same ground but with extra detail and more of a technical focus.

## What is Firefox OS?

In short, [Firefox OS](http://www.mozilla.org/en-US/firefoxos/) is about taking the technologies behind the Web, like JavaScript, and using them to produce an entire mobile operating system. It’s effectively a mobile OS powered by JavaScript!

![Firefox OS screenshots](https://hacks.mozilla.org/wp-content/uploads/2012/10/firefox-os-combined-500x373.jpg)


This is achieved with a custom version of Gecko, the rendering engine in Firefox, that introduces a variety of new [JavaScript APIs needed to create a phone-like experience](https://wiki.mozilla.org/WebAPI#APIs); things like WebSMS to send text messages, and WebTelephony to make phone calls.

You might be wondering what’s running Gecko, as a phone can’t naturally boot directly into Gecko. To do that, the phone boots into a very lightweight Linux kernel that, in turn, boots the Gecko process. The process is a little more involved than that and much more detail can be found in the [B2G Architecture documentation](https://wiki.mozilla.org/B2G/Architecture), including how Gecko accesses the radio hardware and other phone-specific functionality.

The Firefox OS project also aims to combine many of the other projects at Mozilla into a single vision, what we refer to as the Web as the platform. These projects include the [Open Web Apps initiative](https://developer.mozilla.org/en-US/docs/Apps) and [Persona](https://login.persona.org/about), our solution to identity and logins on the Web (formally known as BrowserID). It’s the combination of these various technologies that completes Firefox OS.

If you want to find out more technical information about the OS then definitely check out the [Firefox OS pages on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS).

## Why Firefox OS?

A couple of common questions that come up are, “Why Firefox OS?” and more specifically, “Why build a mobile OS using JavaScript?” These are incredibly important questions so let’s take a moment to delve into them in a little detail.

### Why build a mobile OS using JavaScript?

Answering this question can quite simply be boiled down to one sentence; because it’s possible. It’s not the one and only answer but it succinctly handles most of the arguments against JavaScript being used in this way.

A longer answer is that a JavaScript-powered OS unlocks a whole range of possibilities that aren’t normally or easily available to developers and users with existing operating systems.

The most obvious of the possibilities is the ability to build applications using the technologies that we already use to build websites; namely JavaScript, CSS, and HTML. While not a truly unique feature of Firefox OS — projects like PhoneGap have done this for years on ‘native’ platforms — it allows developers everywhere to create mobile applications without having to learn native languages and APIs.

Another draw of JavaScript is that it’s both [extremely well documented](https://developer.mozilla.org/en-US/docs/JavaScript) and free to develop with. Anyone could sit down for a weekend and put together an application without having to pay for a single thing. Obviously that’s not true in the majority of cases, as people tend to buy their own hosting or tooling, but theoretically there is nothing to stop you building with these technologies for free.

What’s arguably most interesting about JavaScript being used in this way is that it inherently enables physical devices to communicate using the same APIs that we already use on websites. In effect, instead of accessing the Web through a mobile browser the entire phone is now capable of accessing and communicating with any Web API. For example, there is nothing to stop you building an application for Firefox OS that uses WebRTC (once added) to create Skype-like P2P video communication between phones, desktop computers, or anything else that supports WebRTC.

This really only scrapes the surface of “Why JavaScript?” but it certainly gives you a feel of how this is both interesting and important, beyond the tired debate of ‘native’ vs. Web. If you’re still not convinced, just think for a moment about how you can now customise an entire mobile OS using nothing by JavaScript. You’d be hard pushed to deny that it’s pretty darn interesting!

### OK, but why Firefox OS?

Effectively, Firefox OS has been built to put our money where our mouth is (so to speak) and prove that JavaScript is capable of doing what we say it can do. However, there is much more to the project than just proving the the technology is fast enough.

The first reason ‘Why Firefox OS’ is that the mobile ecosystem is overrun with proprietary platforms, most of which prevent you from easily moving between various platforms. What Firefox OS aims to achieve is a truly ‘open’ platform that doesn’t lock you in and inherently makes it as easy and possible to move between devices as and when you choose.

Mozilla is effectively replicating its success with Firefox, in which it stormed the browser market and showed users that there is an alternative, one that lets them be in control of how they use the Web. In this case, it’s less about browsers and more about mobile platforms and application portability.

Another reason is that Firefox OS is an attempt to push the Web forward into the world of physical devices. One direct benefit of this is the addition of [brand new Web standards and APIs](https://wiki.mozilla.org/WebAPI) that allow for things like hardware access using JavaScript.

## Plenty of challenges

It’s fair to say that the Firefox OS journey will contain a number of technical challenges along the way, however that’s part of the fun and the reasons why we’re working on it.

One of those challenges is how to manage an apps ecosystem that is open and distributed. This is something that we are tackling with the [Open Web Apps initiative](https://developer.mozilla.org/en-US/docs/Apps) and the [Mozilla Marketplace](https://marketplace.mozilla.org/). It’s a challenge that we are dealing with as things progress and as we learn more about how things work best, as is the nature with new ways of thinking.

Another of the challenges is making sure that the phone runs as fast as possible, creating the best experience possible. This also relates to questions raised within the developer community around the performance capabilities of JavaScript, particularly when it is used to do things that are perceived to be complex, or when it is compared against ‘native’ technologies. This is a challenge that we are taking very seriously and one which we feel we can overcome. In fact, it’s a challenge that I believe we have already overcome.

One prime example of how capable JavaScript has become is seeing [beautiful JavaScript games](http://playbiolab.com/) running in Firefox OS at near-enough 60 frames per-second, on a low-end, cheap phone.

## Beyond the mobile phone

While the phone aspect of Firefox OS is immediately interesting, you should consider the wider implications of a JavaScript OS and what possibilities it unlocks. For example, what other devices could benefit from being powered by JavaScript? And, what would a network of JavaScript-powered devices allow us to do — things like [Ubiquitous Computing](http://en.wikipedia.org/wiki/Ubiquitous_computing), perhaps?

These aren’t things that we are exploring directly at Mozilla, but they are things that are now inherently possible as a result of the work that we’re doing. There is nothing to stop you taking the [Firefox OS source code from GitHub](https://github.com/mozilla-b2g) and porting it to a device that we’ve never even considered.

We’re already starting to see this happen with examples like a [Firefox OS port for the Raspberry Pi](http://www.youtube.com/watch?v=rk1oTO6cYH0), as well as [another for the Pandaboard](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Pandaboard).

What about a game console powered by Firefox OS? A TV, or set-top box? What about a fridge? Individually, these are all interesting projects, but together they offer something we don’t really have at the moment, a network of different devices powered by the same, open technologies and able to access and communicate across the Web with the same APIs.

We are a long way away from that kind of world but it is projects like Firefox OS that may pave the way for it to happen. You could even be a part of it!

## Getting started with Firefox OS

The hope is that by now you’re sufficiently interested in Firefox OS to begin exploring, experimenting and playing with it. The good news is that there are a whole host of ways that you can do that.

### Documentation

One of the first places to start is the [MDN documentation surrounding Firefox OS and its related technologies](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS). This is where you’ll find everything you need to know about the developer-facing aspects of the platform.

If you’re more interested with the inner-workings of the platform then you’ll want to [cast an eye over the B2G wiki](https://wiki.mozilla.org/B2G), which outlines much of the internals in plenty of detail.

### Source code

If you’re keen to get to grips with the source code of Firefox OS then you’ll want to [head over to GitHub and check it out](https://github.com/mozilla-b2g). The two main repositories that you want are ‘b2g’ (the underlying Gecko engine) and ‘gaia’ (everything you can see, the OS).

### Getting involved

There are a few ways to get involved with the project. You could [check out some of the issues](https://github.com/mozilla-b2g/gaia/issues) and get involved in fixing them, or perhaps just hang out in the [mailing list for B2G](https://groups.google.com/forum/#!forum/mozilla.dev.b2g), or [the one for Gaia](https://groups.google.com/forum/#!forum/mozilla.dev.gaia), and take part in the discussions there.

If you just want to ask a few immediate questions then try out the #b2g and #gaia rooms on irc.mozilla.org. We’re all pretty friendly!

### Development options

If you just want to dig in and make some applications, or perhaps customise the OS, then you’ll need to know about the various development options available to you. They are [covered in some detail on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Choosing_how_to_run_Gaia_or_B2G) but here is a brief overview.

The simplest method to get started is [running Gaia (the visual side of Firefox OS) within Firefox Nightly](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Using_Gaia_in_Firefox). This doesn’t give you a true representation of a phone environment but it will allow you to install applications and use all of the developer tools within the browser that you’re already used to.

Slightly more involved than Nightly is [using the desktop B2G client](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Using_the_B2G_desktop_client). This is effectively a chromeless build of Firefox that looks phone-like has some added APIs that aren’t normally available in standard Firefox. This doesn’t replicate phone hardware but it’s the next best thing before starting to develop on an actual device.

Setting up the desktop B2G client isn’t too hard, but it could be made easier. In the meantime, [projects like r2d2b2g](https://hacks.mozilla.org/2012/10/r2d2b2g-an-experimental-prototype-firefox-os-test-environment/) aim to make the process super simple. Definitely worth checking out.

The last method, and arguably the most important one, is [developing on an actual Firefox OS device](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Installing_Boot_to_Gecko_on_a_mobile_device). This is the only method that will give you a true representation of how your application will perform. It is also the only method that will give you access to the all the new APIs that come with Firefox OS.

Right now, you’ll need to [build and install Firefox OS on one of the supported devices](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/B2G_build_prerequisites). In the future you will be able to skip this step and get access to devices that already run Firefox OS. We don’t have any dates for that just yet.

## Go forth and be part of something big

My hope is that by now you should now have enough inspiration and information to go forth and begin building for this new platform, powered by the technologies you already use. We hope you do and we’d love to see what you come up with.

It’s not every day that you get the opportunity to be a part of something that could quite literally change the way we do things.

## About
[
Robin Hawkes ](http://rawkes.com)

Robin thrives on solving problems through code. He's a Digital Tinkerer, Head of Developer Relations at Pusher, former Evangelist at Mozilla, book author, and a Brit.

## 55 comments

BrianMBOctober 9th, 2012 at 06:49Robert Nyman [Mozilla]October 9th, 2012 at 07:33BrianMBOctober 9th, 2012 at 08:57Robert NymanOctober 9th, 2012 at 10:11PravinOctober 9th, 2012 at 07:55Robert NymanOctober 9th, 2012 at 10:20Matthew BabbsOctober 9th, 2012 at 08:47Robert NymanOctober 9th, 2012 at 10:20David NemeskeyOctober 11th, 2012 at 01:04Robert NymanOctober 11th, 2012 at 04:07Ben DarlowOctober 9th, 2012 at 08:22Robert NymanOctober 9th, 2012 at 10:29MaurizioOctober 9th, 2012 at 08:43Robert NymanOctober 9th, 2012 at 10:30HamuSumoOctober 10th, 2012 at 01:22Robert NymanOctober 10th, 2012 at 06:39MaurizioOctober 10th, 2012 at 08:17Marek MularczykOctober 9th, 2012 at 10:33Robert NymanOctober 10th, 2012 at 00:15tim petersonOctober 9th, 2012 at 14:32Robert NymanOctober 10th, 2012 at 00:15Ken SaundersOctober 9th, 2012 at 15:05Robert NymanOctober 10th, 2012 at 00:15Ken SaundersOctober 9th, 2012 at 15:12Robert NymanOctober 10th, 2012 at 00:16JeffreyOctober 9th, 2012 at 19:35Robert NymanOctober 10th, 2012 at 00:17Larry GarfieldOctober 9th, 2012 at 22:39Robert NymanOctober 10th, 2012 at 01:16XenOctober 9th, 2012 at 22:53Robert NymanOctober 10th, 2012 at 01:17XenOctober 10th, 2012 at 01:56XenOctober 10th, 2012 at 01:57Robert NymanOctober 10th, 2012 at 06:47Rob HawkesOctober 10th, 2012 at 06:52DipankarOctober 10th, 2012 at 03:28Robert NymanOctober 10th, 2012 at 06:42Matthew BabbsOctober 10th, 2012 at 07:42Brian LoweOctober 10th, 2012 at 16:00Robert NymanOctober 11th, 2012 at 04:12Ken CoreyOctober 10th, 2012 at 23:05Rob HawkesOctober 11th, 2012 at 04:43MikeOctober 11th, 2012 at 04:34Robert NymanOctober 11th, 2012 at 04:50Ahmed NefzaouiOctober 14th, 2012 at 07:49Robert NymanOctober 14th, 2012 at 20:36Steve PriceOctober 15th, 2012 at 19:45FabienOctober 27th, 2012 at 13:08Robert NymanOctober 28th, 2012 at 16:39Ahmed NefzaouiOctober 28th, 2012 at 18:21Phil HoldenNovember 4th, 2012 at 02:32AndyDecember 29th, 2012 at 18:44Robert NymanDecember 30th, 2012 at 13:17AndyJanuary 1st, 2013 at 15:36RonnieJanuary 4th, 2013 at 01:05