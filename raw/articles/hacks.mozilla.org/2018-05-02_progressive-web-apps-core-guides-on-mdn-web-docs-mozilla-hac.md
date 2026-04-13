---
title: Progressive Web Apps core guides on MDN Web Docs – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2018/05/progressive-web-apps-core-guides-on-mdn-web-docs/
author: Andrzej Mazur
published: '2018-05-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Progressive web apps (PWAs) are a [new way of building websites](https://blog.mozilla.org/firefox/progressive-web-apps-whats-big-deal/), but are they really all that new? The basic principles of PWAs came out of older strategies for app design such as progressive enhancement, responsive design, mobile-first, etc. Progressive web apps bring together proven techniques such as these with a new set of APIs and other features under one umbrella term; 2018 could be *the year of PWA*.

On MDN Web Docs you’ll find a set of [Core PWA Guides](https://developer.mozilla.org/en-US/Apps/Progressive#Core_PWA_guides) published for everyone who’s interested in checking them out. As a game developer I couldn’t stop myself from including a gamedev-related example in the series. [js13kPWA](https://mdn.github.io/pwa-examples/js13kpwa/) is my website listing all the entries from the [A-Frame category](http://js13kgames.com/aframe) in the [js13kGames 2017](http://2017.js13kgames.com/) competition.

*When the user visits the PWA with a supporting mobile browser, it should display a banner indicating that it’s possible to install the app as a PWA:*

It is still *just* a website like any other, so you can try it yourself with no extra steps needed. The [source code is available on GitHub](https://github.com/mdn/pwa-examples/tree/master/js13kpwa), and you can also [view it live](https://mdn.github.io/pwa-examples/js13kpwa/).

There are currently five [Core PWA Guide](https://developer.mozilla.org/en-US/Apps/Progressive#Core_PWA_guides) articles:

[PWA introduction](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Introduction)[App structure](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/App_structure)[Working offline with Service Workers](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Offline_Service_workers)[Installing on home screen](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Installable_PWAs)[Re-engaging with Notifications and Push](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive/Re-engageable_Notifications_Push).

## Introduction to progressive web apps

The first article of the series introduces progressive web apps: defining what is a PWA, what makes an app progressive, whether it’s worth building, and the advantages it brings over regular web apps.

You can see the browser support, and check the js13k PWA example — the implementation of its contents is explained in subsequent articles.

## Progressive web app structure

Now that you’ve learned the theory behind PWAs, you can look at the recommended structure of an actual app. This article goes through the differences between server-side rendering and client-side rendering, shows how you can mix them both, and explains how PWAs can be built using any approach you like.

The *app shell* concept is the most popular approach for building the structure of an app. It’s important to follow the rules of being linkable, progressive, and responsive by design. We also discuss briefly how the [Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) will be able to help with faster progressive loading in the near future.

## Making PWAs work offline with service workers

This article goes into details of implementing offline capabilities with service workers, explains the offline first approach, and looks at why the “progressive” in PWA is important.

We then inspect the js13kPWA source code to learn how to register a service worker, and what its lifecycle looks like, with installation, activation and updates explained in detail, and how to clear the cache if needed.

## How to make PWAs installable

The fourth article describes how to install PWAs on your mobile device with supporting mobile browsers, so the app can be used as if it were native.


If the user clicks the button, there will be an extra step showing what the app will look like. When confirmed, the app will be installed on the home screen:

This section reviews basic requirements, the contents of the manifest file, the add-to-home-screen feature, and splash screen configuration.

## How to make PWAs reengageable using notifications and push

The last article in the Core Guide offers a way to stay engaged with users. Both the Push API and the Notifications API help achieve this goal – the first one can deliver new content whenever it is available while the other is used to show its details to the user.

Up until now, we’ve use js13kPWA, which is served from backend-less GitHub Pages, to illustrate key PWA concepts, but the Push API requires the server side to work. That’s why I’ve taken the [Push Payload Demo](https://serviceworke.rs/push-payload_demo.html) example from the Service Workers Cookbook and explained it in detail: subscribing, getting [VAPID](https://blog.mozilla.org/services/2016/08/23/sending-vapid-identified-webpush-notifications-via-mozillas-push-service/) keys, and posting and receiving content.

## Conclusion

I hope these excerpts have sparked your interest. Dive into the content right away to learn about implementing PWA features in your apps. The benefits greatly exceed the effort it will take to make your apps more engaging.

It’s possible that in the next few years we may forget the term PWA, as it becomes the primary technique used to build interactive websites. Be sure to learn how to do it effectively now. Just as responsive web design approach is now the standard for building mobile optimized websites, PWA techniques are on track to become the standard of the future.

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.