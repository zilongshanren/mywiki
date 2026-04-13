---
title: Multimedia on the web and using HTML5 sensibly – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/02/multimedia-on-the-web-and-using-html5-sensibly/
author: Chris Heilmann
published: '2011-02-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last week I went to the [London Ajax User Meetup](http://www.meetup.com/londonajax/events/16023271/) in London, England to deliver two talks about HTML5. One was a re-run of a talk I gave at MIT about Multimedia on the web and the second was a call to arms to use HTML5 sensibly. You can go over to [Skillsmatter web site to see both talks back to back](http://skillsmatter.com/podcast/ajax-ria/using-html5-sensibly-and-how-to-cheat-by-using-the-web/rl-311) – but be sure to catch the notes to the second talk in this post, too.

In addition to my notes here there is also a [great write-up of the evening by Ian Alderson](http://blog.caplin.com/2011/02/09/multimedia-on-the-webusing-html5-sensibly-review/) available on the web.

## Multimedia on the web

We’ve covered this talk before in the [blog post here ](http://hacks.mozilla.org/2011/01/talking-about-html5-games-development-at-mit-in-boston/) and you can [read the extensive notes for the whole talk with code examples on my blog](http://www.wait-till-i.com/2011/01/16/lecturing-at-mit-about-html5-video-slides-and-lots-of-notes/). The [slides of the multimedia talk are on slideshare](http://www.slideshare.net/cheilmann/multimedia-on-the-web-html5-video-and-audio) and here:

You can [see “Multimedia on the web” on any HTML5 enabled device here](http://vid.ly/8x6a9m) (courtesy of vid.ly) or embedded here:

## Using HTML5 sensibly

Using HTML5 sensibly was a talk I wanted to give for a long time. Rather than just giving the facts, I wanted to raise some questions every developer should ask themselves, the HTML5 working groups and everyone who cares to listen. We are in the middle of a big change in our development environment and not many people realise that we are breaking a lot of old conventions without fallback.

You can [get the slides on Slideshare or see them here:](http://www.slideshare.net/cheilmann/using-html5-sensibl)

You can [see “Using HTML5 sensibly” on any HTML5 enabled device here](http://vid.ly/4w0l0v) (courtesy of vid.ly).

### Notes on “Using HTML5 sensibly”

I started the talk by telling the story of [the Antarctic Snow Cruiser](http://en.wikipedia.org/wiki/Antarctic_Snow_Cruiser) – a marvel of technology built in 1939 to allow a crew to explore Antarctica. The job of the Cruiser was to give the crew all the neccesary creature comforts and allow them to drive through Antarctica, which is both very cold and also features massive cracks that the vehicle somehow needs to get over. The ingenious solution was to have huge wheels that can be retracted into the Cruiser to prevent them from getting brittle over night and to push the vehicle over the cracks. The Cruiser was built in a rush and tested on the way to the port to go down to Antarctica. It was a hit with the press and people delayed the whole trip even more by wanting to have their photo taken with it. Upon arrival the vehicle almost crashed into the sea as the ramp built for its delivery onto the ice was not strong enough. Even worse, once on the ice the Cruiser couldn’t get a grip and the wheels spun uselessly, almost overheating the engine. Despite all the hype, the cruiser was a massive failure.

A few things went wrong with the cruiser:

- It was purely engineering driven
- It was tested while on the road
- It was never tested in the real environment
- There was a massive media excitement before it proved its worth

Much like we deal with HTML5 nowadays. A lot of the information about HTML5 is marketing driven and used to sell a certain environment or browser to people. Instead of real applications and day-to-day use web sites we [create](http://studio.html5rocks.com/) [demo](http://www.apple.com/html5/) [sites](http://html5advent.com/) to show what “HTML5 can do for you”. The term HTML5 gets washed out as it is used both for implementations of parts of the specification but also for browser-specific code that only works in a certain environment.

This is partly because of the specifications and the different players in the HTML5 world itself. The specs do not only contain definitions of markup but also JavaScript APIs and instructions on how to write a browser that renders HTML5 content. This is great as it takes away the liberty browser vendors had in the past in “creatively” applying the HTML4 specs, but it also means that people can focus on parts of the spec and of course rant about all the other parts. You’ve probably seen one talk about the amazing cool new semantics of HTML5 markup and another about API implementations using completely non-sensical markup back to back. This is what we get right now as the specs are too big and all-encompassing for implementers.

One of the main topics of the HTML5 work is pragmatism – XML and strict HTML just used too many things we simply don’t need. This shows itself a lot in the simplification of a plain HTML document. In HTML4.01 strict this was:

```
```HTML - c'est moi!
# Heading! Everybody duck!

I am content, hear me roar!


Neither the long DOCTYPE definition nor the http-equiv was ever used by browsers. It is not needed for browsers to do their job. In HTML5 this is a plain Vanilla document:

```
```HTML5, c'est moi, ou HTML...
# Heading! Everybody duck!

I am content, hear me roar!


Much simpler and shorter. In addition to that HTML5 also includes new semantic elements:

```
```HTML5, c'est moi, ou HTML...
I am content, hear me roar!


This gives us handles for styling and tells the browser what the different parts are. The simplification goes further though. As people never seemed to have bothered to write valid XML in HTML it is now also completely OK to mix upper and lower case and omit quotation marks around the attributes (if the attributes have one value, multi value attributes like classes need quotes around them once you add more than one value):

```
```HTML5, c'est moi, ou HTML...
I am content, hear me roar!


Browsers are forgiving enough to fix these inconsistencies for us. For example the generated code in Firefox is:

```
```HTML5, c'est moi, ou HTML...
I am content, hear me roar!


However, if we were to omit the closing `</p>`

tag in the `<section>`

the generated code looks different:

```
```HTML5, c'est moi, ou HTML...
I am content, hear me roar!

By me!


As you can see, the `<footer>`

got moved into the paragraph inside the section. Why? Who knows? The issue is that we ask a browser to make an educated guess for us and as a browser doesn’t understand semantics, this is what we get.

Which leads me to a few questions we need to ask and find the answer to:

- Can innovation be based on “people never did this correctly anyways”?
- Is it HTML or BML? (HyperText Markup Language or Browser Markup Language)
- Should HTML be there only for browsers? What about conversion Services? Search bots? Content scrapers?

The next issue I wanted to discuss is legacy browsers which seems to be a euphemism for IE6. The issue with IE6 is that when you use the new semantic HTML elements exclusively then they can’t be styled in this browser. By using the correct new syntax that should bring us a lot of benefits you condemn older browser users to see unstyled documents.

There are a few ways around this. The first one requires JavaScript – if you create the element using the DOM first you can style it in IE:

```
```

This technique has been wrapped up nicely in a script called [HTML5 shiv](http://code.google.com/p/html5shiv/) by Remy Sharp. Of course, this means that you make markup dependent on JavaScript to work which is not what markup is about, according to purists of the web. You can work around that dependency in a few ways. You can [write HTML5 as XHTML](http://www.ibm.com/developerworks/xml/library/x-think45/), you can [use conditional comments or a namespace](http://www.debeterevormgever.nl/html5-ie-without-javascript/) or you can use both the new semantic elements and DIVs with a class around them to please all browsers:

```
```HTML5, c'est moi, ou HTML...
I am content, hear me roar!


This seems to be the most pragmatic solution but is a lot of extra effort.

The main issue is that not only legacy browsers are failing to support HTML5 properly which is why people tend to use a library like [Modernizr](http://www.modernizr.com/) to check for HTML5 support before applying it. Modernizr adds classes to the HTML element after checking what the current browser supports and thus gives you handles to use in progressive enhancement. All the hacks and fixes are also bundled in [HTML5 Boilerplate](http://html5boilerplate.com/), including server settings and ways to make legacy browsers behave. In essence, the much smaller Vanilla HTML5 markup becomes a lot of code again if you test it in the real world.

If you also want to use all the cool new JavaScript APIs you can use [Polyfills](https://github.com/Modernizr/Modernizr/wiki/HTML5-Cross-browser-Polyfills) to make legacy browsers do something with the code you write.

Which leads to more questions we need to answer:

- Should we shoe-horn new technology into legacy browsers?
- Do patches add complexity as we need to test their performance? (there is no point in giving an old browser functionality that simply looks bad or grinds it down to a halt)
- How about moving IE fixes to the server side? Padding with DIVs with classes in PHP/Ruby/Python after checking the browser and no JS for IE?

The last feature of HTML5 I want to talk about is Video and Audio. Again, there is much more complexity than meets the eye:

Tecnically, embedding an HTML5 video should be as simple as this:

Once you consider all the different formats needed for different browsers though it becomes a lot more work:

The reason is intellectual property, legal codec battles and implementation of video in different browsers and platforms. In essence, you need to provide the video in three formats. Of course when there is a need then some company will come up with a solution. [Vid.ly is a service by encoding.com](http://vid.ly) that provides you with a single URL that sends the video in the right format to the device you use. All in all they create 28 different formats for you to cater for all kind of mobiles and browsers.

The other big issue with HTML5 video is that there is no protection from downloading the videos. This is as intended but a big problem when it comes to premium content on the web. As [discussed in the comments of this post by Adobe](http://www.webkitchen.be/2011/01/26/stealing-content-was-never-easier-than-with-html5/) publishers want to have a way to stop people from downloading and reusing their videos but instead just want their audience to watch them in a closed environment.

All in all there are a few questions to answer when it comes to HTML5 video:

- Can we expect content creators to create video in many formats to support an open technology?
- Can a service like vid.ly be trusted for content creation and storage?
- Is HTML5 not applicable for premium content?

In the end, I want every developer and designer out there to take a stand and demand answers to these questions. There is no point in just saying “that’s how it is”. When we keep our technologies closed and when we rely on scripting to make web sites work we do break the web in the long run. The [current debate about hashbangs](http://simonwillison.net/tags/hashbanghell/) for links shows this.

Everybody can take part in the [HTML5 working group](http://www.whatwg.org/mailing-list) and [add documentation to MDN](https://developer.mozilla.org/) – time to get to work.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 9 comments

JamieFebruary 14th, 2011 at 11:22SimonFebruary 14th, 2011 at 13:28voracityFebruary 14th, 2011 at 21:15Luca SalviniFebruary 15th, 2011 at 04:18Chris HeilmannFebruary 15th, 2011 at 04:39JulienWFebruary 15th, 2011 at 00:17Felix PleșoianuFebruary 15th, 2011 at 00:21JulienWFebruary 15th, 2011 at 00:22WulfTheSaxonFebruary 15th, 2011 at 12:01