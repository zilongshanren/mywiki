---
title: Selling HTML5 to a consulting company – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/09/selling-html5-to-a-consulting-company/
author: Chris Heilmann
published: '2012-09-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I just spent a weekend in a resort in Mallorca. I was invited by an IT consultancy from Frankfurt to join them at their off-site and give a two hour (re)introduction to HTML5.

## The audience and the challenge

The consultancy is very successful in what they do and are very much a Java / native code shop. Their clients are insurance companies, banks and the like which means the topic of HTML5 came up only peripherally in their discussions. With more and more clients looking for iPad apps and other demands for cross-platform solutions they wanted to know more about HTML5, what is possible and what can be done.

This sounded like a great opportunity to go out of my comfort zone and see how good my skills as an advocate for web technology are. Ever the optimist, I also considered this a great opportunity to inspire in a field in which IT is used to make a difference to the lives of a lot of people. So I said yes.

## The presentation

Without any preparation (there was no time), without knowing who the audience will be (turns out it was the whole company, including non-technical employees and some contractors) and being asked to deliver the talk in German I found myself in front of a room with about 70 people, set up my computer (which failed to do so the first time, it will go to the farm of old computers soon), happily realised that the WIFI worked and went right into it.

Instead of talking about HTML5 in isolation, I thought it best to show off the web as a development platform and the advancements that happened in the last few years that may not be known. Turns out this was exactly what was needed and I’ve had a lot of 1:1 conversations later on with people who want to seriously give HTML5 a go. Their idea is converting some of the tools used now in the company to move from Java and fixed-size, Photoshop driven interfaces to more flexible solutions using HTML5 and JavaScript. Score, I’d say.

## What I’ve done

Seeing that it was more or less an open 2.5 hours show and tell with questions from the audience I have no notes. So here is a list of the things I showed and mentioned which had quite some impact and the techniques how I presented them.

## Laying the groundwork

I started by explaining the need for HTML5 (document to app transition) and that with a unified and defined HTML parser, we finally have a level playing field across browsers. I explained that a face to face comparison of HTML5 apps and native apps is not fair as the performance of browsers and webviews is hindered in many cases by hardware and the OS. Which means that browers can not use the same resources native code can which of course is a difference in performance. That said, web apps can be more nimble and update much easier than native ones.

In the spirit of [pre-emptive writing](http://christianheilmann.com/2012/07/21/developer-evangelism-tasks-pre-emptive-writing/) I also took the Mark Zuckerberg quote from TechCrunch disrupt a few weeks ago and explained that he didn’t say that HTML5 was a mistake but that the way they approached it was. I also pointed out his quote stating that Facebook’s number of mobile web users are more than the ones of Android and iOS combined.

## Techniques

I think the most impactful part of the presentation was that I didn’t prepare any slides but used the browser to show everything to the audience. I used [Mozilla Thimble](https://thimble.webmaker.org) to show live code and the immediate impact of my changes. I used the developer tools in Firefox and Chrome to show how to change a live site and try out some of the new technology in existing pages instead of showing demos that are impressive but don’t apply to the audience.

## Platform demos

All in all my aim was to show that HTML5 is an interesting thing to bet on as it is part of the web ecosystem. This means instead of starting with code I showed:

- Collaborative editing using online editors
- GitHub as a place to get code, meet other developers and submit fixes
- Developer tools of browsers to show that now we can test and fix things outside of a code first, deploy, find bug development cycle
- MDN as a resource for demos and documentation
[Browserstack.com](http://www.browserstack.com/)to test on browsers and operating system you don’t have

## Technology demos

The technology demos were simple, but I got lots of good feedback on them as I kept them relevant.

- Introducing HTML5 form elements and showing that simply adding a
`number`

attribute and a`required`

attribute means that this field will always be a number and users can not send the form (in the browser) without satisfactorily having filled the field. This means there is no need for writing client-side validation any longer which is a big headache for non-JavaScript enthusiasts. - Adding a
`video`

element in the page, playing it with a right-click, adding the`controls`

attribute to add controls and adding a CSS transformation (rotation for example) to prove that video is just another page element in a HTML5 world. - Showing a simple example on how to use MediaQueries to do responsive designs and showing the
[Responsive Mode](http://www.youtube.com/watch?v=t07cLJhJkjQ)in the Firefox developer tools - Showing a simple hover state in CSS and adding a transition to prove that these days you can make things look smooth very simply without having to add another JavaScript
- Showing how to progressively enhance a simple HTML document using some CSS transitions to make it look much more engaging.
- Showing the simplicity of local storage (using the
[123done task list example](http://thewebrocks.com/123done/)) and explaining how AppCache and manifest files can turn a web page into a locally cached app. - Showing how easy it is to plot something in the page using Canvas and explaining that canvas using drag and drop can also allow for
[image cropping](http://thewebrocks.com/demos/crop/)and[thumbnail generation](http://thewebrocks.com/demos/canvasthumber/). - Showing that file uploaders can be much more convenient for the end users these days with the Flickr image uploader as an example
- Showing how to make a video interact with web content using Mozilla Popcorn – explaining that this could be used for interactive training materials

## Near future gazing

As requested by the audience I also showcased some of the near-future parts of web tech:

- The
[toycam demo](http://neave.com/webcam/)explaining that it uses WebRTC which can be used to get video input and manipulate it using WebGL live in the browser. I also pointed out that WebRTC is not limited to that but could be used for all kind of other data streaming tasks - Firefox OS, how it is architected and why we do it
- Mozilla’s Web APIs and how they are used in Firefox OS (showing the FFOS desktop build, playing with the dialer and showing that even they keytones are created using JavaScript)
- Explaining Persona and how it allows you to simply verify users on the web without having to ask for a username and password
- Showing off the
[Banabread demo](https://developer.mozilla.org/en-US/demos/detail/bananabread)and explaining how it was done by converting C++ code using[Emscripten](https://github.com/kripken/emscripten) - Showing the Mozilla App store preview and how an HTML5 app can be installed natively and run from the Application folder and full-screen

## Your turn

All in all I have to say this was thoroughly enjoyable and I got out of it with a sense of satisfaction of having narrowed the gap between the webdesign world and the world of corporate IT a bit more. Give it a go, too, I am sure you’ll enjoy it.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 2 comments

mustafaSeptember 18th, 2012 at 01:34Schalk NeethlingSeptember 18th, 2012 at 06:19