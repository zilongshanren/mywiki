---
title: More details about the WebAPI effort – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/08/more-details-about-the-webapi-effort/
author: Jonas Sicking
published: '2011-08-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As we’ve hoped, there has been a lot of interest in the [newly announced WebAPI effort](http://hacks.mozilla.org/2011/08/introducing-webapi/). So I figured that I should explain in more detail some of my thinking around what we’re hoping to do and the challenges that are ahead of us.

## Goal

The goal of this effort is to create APIs to expand what the Web can do. We don’t want people to end up choosing to develop for a proprietary platform just because the Web is lacking some capability.

The main effort, at least initially, is to enable access to hardware connected to the device, and data which is stored or available to the device. As for hardware, we want to make the full range of hardware that people use available to the web platform. From common hardware like cameras, to more rarely used (but no less awesome) hardware like USB-driven Nerf cannons. We also want to enable communication hardware like Bluetooth and NFC.

For data stored on the device, the most commonly discussed data today is contacts and calendar. This includes the ability to both read and write data. That is, we both want the Web platform to be able to enumerate contacts stored on the device, and read their details, as well as add and remove contacts. In short, we want it to be possible to create a Web page or Web app which lets the user manage his contact list. Same thing for calendar events and other types of data stored on devices.

## Security and Privacy

One big reason these types of APIs haven’t been developed for the Web platform yet is because of their security and privacy implications. I would obviously not want every single Web page out there to be able to mess around with my contact list or my calendar. And being able to issue any commands to any USB device that I happen to have plugged in would likely result in everyone’s computer immediately being zombified.

So as we are developing these APIs, we always have to develop a security model to go along with them. In some cases simply asking the user, which is how we currently do Geolocation, might work. In others, where security implications are scarier or where describing the risk to the user is harder, we’ll have to come up with better solutions.

I really want to emphasize that we don’t yet know what the security story is going to be, but that we’re absolutely planning on having a solid security solution before we ship an API to millions of users.

[Robert O’Callahan](http://robert.ocallahan.org/) has a really great post about [permissions for Web applications](http://robert.ocallahan.org/2011/06/permissions-for-web-applications_30.html).

## Standards

Mozilla has always had a strong commitment to Web standards. This is of course not something we’re changing! All of the APIs that we are developing will be developed with the goal of being standardized and implemented across both browsers and devices.

But it’s important to ensure that standards are good standards. This takes experimenting. Especially in areas which are as new to the Web, and as security sensitive, as these are.

Standards organizations aren’t a good place to do research. This is why we want to experiment and do research outside the standards organizations first. But always in the open, and always listening to feedback. We’re also going to clearly prefix any APIs as to indicate that they are experiments and might change once they get standardized.

Once we have a better understanding of what we think makes a good API we will create a proposal and bring to working groups like the [Device API](http://www.w3.org/2009/dap/) group at [W3C](http://www.w3.org/), [WAC](http://www.wacapps.net/) and [WHATWG](http://www.whatwg.org/).

Throughout this process we will of course be in contact with other interested parties, such as other browser vendors and web developers. This is part of the normal research and making sure that an API is a good API.

Mozilla always has and always will be a good steward of the open Web. We are not interested in creating a Mozilla-specific Web platform. We are interested in moving the open Web platform forward.

## High Level vs. Low Level

One thing that often comes up with API design is whether we should do high level or low level APIs. For example, do we provide a low-level USB API, or a high-level API for cameras?

There are pros and cons with both. High level means that we can create more developer-friendly APIs. We can also provide a better security model since we can ensure that the page won’t issue any unexpected USB commands, and we can ensure that no privacy-sensitive access is made without user approval. But high level also means that developers can’t access a type of device until we’ve added support for it. So until we’ve added an API for Nerf cannons, there will be no way to talk to them.

Exposing a low-level USB API on the other hand, means that web pages can talk to any USB device in existence, with no need for us to add an explicit API for them. However it also requires developers to get their hands dirty with the details of the USB protocol and differences between devices.

The approach we’re planning on taking is to do both high-level and low-level APIs, as well as give people the proper incentives to use the one that is best for the user. But a very important point is to provide low-level APIs early to ensure that Mozilla isn’t on the critical path for innovation. Over time, we can add high-level APIs where that makes sense.

## How you can join

As with all things Mozilla, we’re planning on doing all our work in the open. In fact, we’ll be relying on your help to make this successful! As to keep discussions focused, we’re going to use the a new mozilla.dev.webapi discussion forum for all communication. This means that you can participate through email, newsgroups, or the web-based google group UI.

You can subscribe to the mailing list at [https://lists.mozilla.org/listinfo/dev-webapi](https://lists.mozilla.org/listinfo/dev-webapi)

For other methods go to: [http://www.mozilla.org/about/forums/#dev-webapi](http://www.mozilla.org/about/forums/#dev-webapi)

We also use the [#webapi](irc://irc.mozilla.org/#webapi) IRC channel on [irc.mozilla.org](irc://irc.mozilla.org/).

We’ll also be tracking progress on the wiki page [https://wiki.mozilla.org/WebAPI](https://wiki.mozilla.org/WebAPI)

Looking forward to hearing from you to help build the next stage for the web platform!

## Hiring developers

**Edit:** Forgot to mention, we are hiring several full time engineers for working on the WebAPI team! [Read the job description and apply](http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qpX9Vfwa&cs=9Kt9Vfw1&page=Job%20Description&j=oIvPVfwH).

## About Jonas Sicking

Jonas has been hacking on web browsers for over a decade. He started as a open source contributor in 2000 contributing to the newly open sourced mozilla project. In 2005 he joined mozilla full time and has since been working on the DOM and other parts of the web platform. He is now the Tech Lead of the Web API project at mozilla as well as an editor for the IndexedDB and File API specifications at W3C.

## 18 comments

Ferenc MihalyAugust 29th, 2011 at 15:12Robert NymanAugust 30th, 2011 at 12:37AndrewAugust 29th, 2011 at 21:12Robert NymanAugust 30th, 2011 at 12:37Natanael LAugust 30th, 2011 at 02:28Robert NymanAugust 30th, 2011 at 12:37Robert SchultzAugust 30th, 2011 at 09:07Robert NymanAugust 30th, 2011 at 12:38Jonas SickingAugust 30th, 2011 at 16:27knygarAugust 30th, 2011 at 15:48Jonas SickingAugust 30th, 2011 at 16:39knygarAugust 30th, 2011 at 17:58Jonas SickingAugust 30th, 2011 at 19:06MounirSeptember 4th, 2011 at 17:57Robert NymanSeptember 5th, 2011 at 01:35Jonas SickingSeptember 6th, 2011 at 00:33sungSeptember 4th, 2011 at 20:04Robert NymanSeptember 5th, 2011 at 01:35