---
title: 'WebAPIs – Firefox OS for developers: the platform HTML5 deserves – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/08/webapis-firefox-os-for-developers-the-platform-html5-deserves/
author: Chris Heilmann
published: '2013-08-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the fifth video of our “Firefox OS – the platform HTML5 deserves” series ([part one](https://hacks.mozilla.org/2013/06/firefox-os-for-developers-the-platform-html5-deserves/), [part two](https://hacks.mozilla.org/2013/07/app-discovery-firefox-os-for-developers-the-platform-html5-deserves/), [part three](https://hacks.mozilla.org/?p=21869) and [part four](https://hacks.mozilla.org/2013/08/firefox-marketplace-and-alternatives-firefox-os-for-developers-the-platform-html5-deserves/) have already been published) we talk about how Firefox OS extends the capabilities of the Web by adding new APIs, called [WebAPIs](https://wiki.mozilla.org/WebAPI) to the existing stack of technologies.

![Firefox OS - be the future](../../assets/b0198161368b9b8c.png)


Check out the video featuring Chris Heilmann ([@codepo8](http://twitter.com/codepo8)) from Mozilla and Daniel Appelquist ([@torgo](http://twitter.com/torgo)) from [Telefónica Digital](http://blog.digital.telefonica.com)/ W3C talking about the need for device APIs on the Web, how some of the existing APIs can be used and how the work on Firefox OS benefits the Web as a whole. You can [watch the video here](http://www.youtube.com/watch?v=oNgsvxTaqao).

The WebAPI work is important as it allows apps built with Web technologies to access the hardware. For the work on Firefox OS (which is fully built in HTML5 itself), we very much needed to know the status of the phone, how much battery is left, what the connectivity is like, the screen orientation and many more features. Thus we defined access to the various parts of the hardware as JavaScript APIs and sent these as proposals to the standard bodies.

If you want to learn more about these new APIs the canonical place to go to is [the WebAPI Wiki Page](https://wiki.mozilla.org/WebAPI) where you can find an up-to-date list of all the APIs, their implementation status in the different Firefox platforms, the standards bodies involved and where to file bugs for them. You can also click through to bugzilla to see demos of the APIs in action. We’ve blogged here about WebAPIs in detail before: [Using WebAPIs to make the web layer more capable](https://hacks.mozilla.org/2013/02/using-webapis-to-make-the-web-layer-more-capable/) and you can see a lot of information and demos in that post.

In general, all the APIs follow a simple model: you ask for access and you define a success and failure handler. You also get methods to ask for various properties in detail and some have Boolean values available to you. This makes it very easy to test for the support of a certain API before trying to access it.

Not all APIs can be available on the open Web as we can not trust every server out there. That is why the APIs come in three flavours: regular, privileged and certified. Regular APIs can be used in any app, regardless of its location (you can self-host these apps). Examples for that are the geolocation or the battery API. Privileged and Certified APIs both need your app to have a [content security policy](http://www.w3.org/TR/CSP/) and be hosted on Mozilla servers. That way we can give you access to the hardware but minimise the potential of abuse and malware at the same time.

Take a look at the [exhaustive list of blog posts here dealing with WebAPIs](https://hacks.mozilla.org/category/webapi/) for more reading and we’ll be back with the next video covering WebActivities soon.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## One comment

Gabriel OrtizAugust 15th, 2013 at 09:47