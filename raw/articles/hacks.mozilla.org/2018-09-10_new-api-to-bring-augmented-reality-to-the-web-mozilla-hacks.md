---
title: New API to Bring Augmented Reality to the Web – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2018/09/webxr/
author: Lars Bergstrom
published: '2018-09-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’re entering a new phase of work on JavaScript APIs here at Mozilla, that will help everyone create and share virtual reality (VR) and augmented reality (AR) projects on the open web.

As you might know, we [formally launched this work](https://medium.com/mozilla-tech/webvr-shipping-today-in-firefox-d54d490a2072) last year with the release of Firefox desktop support for the WebVR 1.1 API. Using that draft API, [early adopters like WITHIN](https://blog.mozilla.org/blog/2018/06/13/within-webvr/) were able to distribute 3D experiences on the web and have them work well on a range of devices, from mobile phones and cardboard viewers to full-fledged, immersive VR headsets.

### The Expansion of WebVR

WebVR has been instrumental in democratizing VR, so more people can experience 3D content without expensive headsets. It’s also been a huge time-saver for content creators, who need to test and verify that their work renders well on every viewing platform. Having a stable API to work with means 3D content can find a wider audience, and it cuts down on the rework creators have to do to deliver great web experiences to a range of devices.

Mozilla has been pushing the boundaries of VR in the browser, getting people together across the industry to support a standard way of rendering 3D content. That work has created a fast lane for artists and programmers to share web-based VR experiences with a growing user base. And with WebVR support in browsers like Firefox, we’ve started the work of liberating VR and AR content from silos and headset stores, and making them accessible on the open web.

### The Promise of Mixed Reality

Mixed Reality is going to be a powerful platform, bringing highly engaging and emotionally evocative immersive content to the web. Like any new creative medium, we want it to be widely accessible, so curious viewers can experience the next generation of digital media without having to shell out hundreds of dollars for a high-end viewer.

Today, the industry is taking another step toward these goals. We have ambitions to broaden the number of platforms and devices that can display VR and AR content. For instance, the camera on most mobile phones can be used to overlay information on physical reality – if it has a set of instructions on how to do that.

Experimentation continues with a new JavaScript API called the [WebXR Device API](https://immersive-web.github.io/webxr/). We expect this specification will replace WebVR in time and offer a smooth path forward for folks using WebVR today.

**What’s New in WebXR**

The new WebXR Device API has two new goals that differentiate it from WebVR. They are:

- To support
**a wider variety of user inputs**, such as voice and gestures, giving users options for navigating and interacting in virtual spaces - To establish
**a technical foundation for development of AR experiences**, letting creators integrate real-world media with contextual overlays that elevate the experience.

You can find details about WebXR Device API by visiting the [Immersive Web Community Group](https://github.com/immersive-web/). We expect that many of the same crew that worked on WebVR – talented engineers from Mozilla, Google, Samsung, Amazon and other companies – will continue to work on the WebXR Device API, along with new contributors like Magic Leap.

**AR Comes to the Web**

AR and VR both are at the cutting edge of creative expression. Some [museums offer AR experiences](https://www.wired.com/story/augmented-reality-art-museums/) to give depth and context to exhibits. Other projects include educational content, from geology lessons to what it’s like to [walk the streets in war-torn Syria](https://www.msn.com/en-gb/news/offbeat/experience-the-horror-of-a-syrian-air-raid-in-hero/ar-AAw7vFb#image=1).

What can augmented reality do on the web? Already there are examples that demonstrate powerful use cases. For instance, want to know how that new sofa will fit in your living room, before you buy it? Or how an [espresso machine would look](https://www.youtube.com/watch?v=l9RifUeEGN4) in your kitchen? Augmented reality can make online shopping a more sensory experience, so you can test-drive new products in your home in a way that preserves size and scale. It’s a great complement to online shopping, especially as companies start offering online visualizations of physical products.

Mozilla has some key tenets for how we’d like this next-generation media to work on behalf of users.

**We want to ensure user privacy.**You shouldn’t have to give an art store website access to pictures of your home and everything in it in order to see how a poster would look on your wall.**We want to make AR and VR accessible**to the widest possible audience. We’re committed to removing barriers for people.**We want to help creators make content that works on all devices**, so users can access mixed reality experiences with the device they have, or want to use.**We want to enable the long tail of creators,**not just big studios and well-known brands. Everyone who wants to should be able to augment the world, not just those who can get an app into a store.

The WebXR community is working on [draft specifications](https://github.com/immersive-web/proposals/issues) that target some of the constraints of today’s wireless devices. For instance, [creating a skybox](http://www.realityisagame.com/archives/1776/what-is-a-skybox/) setting you can use to can change the background image of a web page. We’re also working on a way to expose the world-sensing capabilities of early AR platforms to the web, so developers can determine where surfaces are without needing to run complex computer vision code on a battery-powered device.

### Support in Firefox

We’re proud that [Firefox supports WebVR today](https://blog.mozilla.org/blog/2017/08/08/webvr-new-speedy-features/), so people can use current technology while we’re working to implement the next-generation specification. We have begun work to add WebXR support to Firefox. An early implementation will be available in [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly) in the coming months, so developers and early adopters can turn it on and give it a test-drive.

Some parts of the WebXR specification are still in motion. Rather than waiting for a final version of the spec, we’re going to move forward with what we have now and adjust to any changes along the way. The roadmap for the upcoming [Firefox Reality browser](https://blog.mozilla.org/blog/2018/04/03/mozilla-brings-firefox-augmented-virtual-reality/) will be similar to the Firefox desktop version, with initial support for immersive browsing using WebVR, and WebXR support to follow.

In time, we plan to support WebXR everywhere that we support WebVR currently, including Windows, Linux, macOS, and Android/GeckoView platforms. We will continue supporting WebVR until most popular sites and engines have completed the transition to WebXR. Want more technical details? Check out this [WebXR explainer](https://github.com/immersive-web/webxr/blob/master/explainer.md).

### Today’s AR Experiments

If you can’t wait to dive into augmented reality, here’s something you can try today: [Mozilla’s WebXR Viewer for iOS](https://itunes.apple.com/us/app/webxr-viewer/id1295998056?mt=8). It’s a way you can get a glimpse of the future right on your iPhone (6s or newer) or iPad. To be clear: this app is an experiment based on a proposed interim API we created last year. We are currently converting it to use the WebXR Device API.

We created this app as a way to experiment with AR and to find out how easy it was to get it [working on iOS using Apple’s ARKit](https://blog.mozvr.com/experimenting-with-ar-and-the-web-on-ios/). If you want to have a look at the code for the iOS app, it’s posted on [GitHub](https://github.com/mozilla-mobile/webxr-ios). For Android users, Google has a similar experiment going with [early support for the immersive web](https://developers.google.com/web/updates/2018/05/welcome-to-immersive).

Want to keep up with the progress of WebXR and the new WebXR Device API? Follow [@mozillareality](https://twitter.com/mozillareality) on twitter, or [subscribe to the Mozilla Mixed Reality blog](https://blog.mozvr.com/subscribe/) for our weekly roundup of XR news.

## About
[
Lars Bergstrom ](http://www.lars.com)

Lars Bergstrom is the Research Engineering Manager for VR / AR at Mozilla. Previously, he obtained a Ph.D. in Computer Science working on compilers and runtimes for parallel languages and before that he was an engineer and lead at Microsoft on Visual Studio.

## 3 comments

MatutaSeptember 13th, 2018 at 19:16Bhuvana MeenakshiSeptember 13th, 2018 at 21:57Lars BergstromSeptember 15th, 2018 at 08:17