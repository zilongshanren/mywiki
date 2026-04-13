---
title: Beyond Offline – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/12/beyond-offline/
author: Salva
published: '2015-12-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is my first post on Mozilla Hacks and despite my personal blog, it is my first post as a mozillian (yay!). During this month I’ve been working in the Service Worker Cookbook project —part of the [Web Application Developer Initiative](https://wiki.mozilla.org/Apps) (WADI)— which gives me the opportunity to put my expertise in Service Workers into practice while at the same time learning new ways to exploit this exciting new web technology for the good of the Web. Let me share with you some of my latest thoughts.

The previous post in this series involved my colleague [David Walsh](http://davidwalsh.name/) talking about [Application Cache](https://developer.mozilla.org/en-US/docs/Web/HTML/Using_the_application_cache) and its lack of flexibility, so I won’t delve more into this topic. I will however look at some more of the recipes available in the Service Worker Cookbook. David introduced it and discussed some [offline recipes](https://hacks.mozilla.org/2015/11/offline-service-workers/); I want to go a little bit further and look at some other uses of Service Workers.

## Service workers today

Despite having been under development for some time, it’s only now that we are starting to hear about [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) being used in the wild. To recap, this API was originally committed to do right what Application Cache did wrong. [Some web archaeology](https://github.com/slightlyoff/ServiceWorker/tree/63a184996d1fd199dea8e922b6edbd1fd4642748#whats-going-on-here) reveals that the intention was precisely to fix offline caching, allowing Web developers to build URL-friendly, offline-by-default applications in a sane and layered way

.

The initial approach introduced the concept of navigation control through a concept that evolved into the Service Worker’s [fetch functional event](https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent): a way to intercept network requests and respond with data obtained from the network, databases or procedurally generated. The best part? Controlled pages do not have to know that they are actually being hijacked (although they can be told) so the service logic is completely decoupled from the application logic. A perfect “man in the middle”.

But as hackers (this is the Hacks blog, after all!) what we like is to craft ingenious solutions to relevant problems in which “ingenious” often means abusing the real intention of something. In Mozilla, from our WADI and Firefox OS initiative we are exploring the following off-label uses of Service Workers.

## API analytics

Let’s start with a direct application of the man in the middle: **API analytics**. Imagine you want to get statistics about the usage of an API and do not have access to the server. Current solutions manipulate the client code generating HTTP requests, sending appropriate logs to the analytics service. A Service Worker could go one better, intercepting each request, extracting its parameters, sending the log for analysis and leaving the original request to reach the network.

## Installing packaged apps

Before exploring other exotic uses, here is a more traditional one —a Service Worker can be used to offline resources, by **installing packaged applications**. It is possible to download a single zip package and unzip it at the time of enabling of a Service Worker. This reduces the overhead introduced by each of the HTTP requests and makes downloading the resources an atomic operation. Smart and automatic caching of large static assets such as fonts or images is another good example of offlining.

## Impersonating servers

Recalling the man in the middle approach, by acting as proxy a service worker could **impersonate a server** and implement the API that the client expects to reach through the network. [ServiceWorkerWare](https://github.com/gaia-components/serviceworkerware/), developed within Firefox OS, is a library to support the [New Gaia Architecture](https://wiki.mozilla.org/Gaia/Architecture_Proposal) for applications and allows developers to write Service Workers in a *declarative way*, following the philosophy of the popular Node.js [Express](http://expressjs.com/starter/hello-world.html) library but on the client side.

## Implementing modern framework functionality

Service Workers have their own place as building blocks for modern frameworks too. Consider template interpolation as an example. Lots of current popular web application frameworks such as [backbone.js](http://backbonejs.org/) and [Angular](https://angular.io/) render models by interpolating their properties in a template. The New Gaia Architecture we spoke of previously introduces the concept of a **render store**, an offline cache that stores the result of interpolating the template with the data model so that the second time the client requests the same model, it can be retrieved from the render store, avoiding [interpolation delays](http://unoyunodiez.com/2015/09/07/modern-mobile-web-development-breaking-the-rules-beating-delays-improving-responsiveness-and-performance-ii/).

## Dependency injection

Another popular concept in modern frameworks is **dependency injection**, which states that dependent code need not know how its dependencies have been built. It only knows about abstract interfaces, and the specific implementations are provided by an abstract factory called an injector. A Service Worker could act as a dependency injector. A framework could make its components declare API dependencies via script tags, then the Service Worker, acting as the injector, could identify requests to the abstract resources and respond with the actual modules.

## Deferring requests

If the device does not have connectivity but the app continues accepting operations, the client application and the service in the cloud will be eventually out of sync. An interesting feature for a framework could be to offer a **request deferrer**. For instance, while offline a Service Worker could withhold requests to the API and release them when the connection comes back. In the meantime, the Service Worker could imitate the server by answering with generic OK ([status code 200](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#200)) or ACCEPTED ([status code 202](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#202)) responses to client operations. Once connectivity returns, the Service Worker could sync with the cloud by recreating the requests against the network from a queue of deferred requests.

## Network logic ideas

And to finish, the Service Worker could also contain network logic, perhaps multiplexing a request to multiple sources, measuring the availability and quality of each source and returning the data via the right channel. Let me provide a little example before wrapping up. Suppose we have an online video application. The user wants to see an HD movie so the application requests the movie URL, but before starting to serve the content the Service Worker intercepts the request, asks for the load levels of the servers, selects the one with the lowest value and starts serving the content from that specific server. Sounds familiar? It’s a **load balancer**, yes, but now achievable on the client side! Nice, isn’t it?

## Summary

That’s all for now folks! Seven uses, seven exotic recipes beyond simply caching content for offline availability. At this time, the [Service Worker Cookbook project](https://serviceworke.rs/) exposes all these ways (and others besides) to take advantage of the features provided by the Service Workers API. And we will not stop here —there is much more to explore; the [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) is here to stay and [Background Sync](https://github.com/slightlyoff/BackgroundSync) is coming soon, with streamed HTTP responses and cancellable requests on the horizon. Who knows what opportunities lie ahead?

For more info about Service Workers and other platform implementation status, take a look at [Platatus](https://platatus.herokuapp.com/), and we’ll keep you informed!

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## 2 comments

James NadeauDecember 28th, 2015 at 12:02lv7777January 7th, 2016 at 16:46