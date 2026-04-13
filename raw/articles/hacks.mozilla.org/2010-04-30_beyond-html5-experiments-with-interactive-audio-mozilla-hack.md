---
title: 'Beyond HTML5: experiments with interactive audio – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2010/04/beyond-html5-experiments-with-interactive-audio/
author: Christopher Blizzard
published: '2010-04-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a re-post of an important post from David Humphrey who has been doing a lot of experiments on top of Mozilla’s extensible platform and doing experiments with multi-touch, sound, video, WebGL and all sorts of other goodies. It’s worth going through all of the demos below. You’ll find some stuff that will amaze and inspire you.*

*David’s work is important because it’s showing where the web is going, and where Mozilla is helping to take it. It’s not enough that we’re working on HTML5, which we’re about finished with, but we’re trying to figure out what’s next. Mozilla’s platform, Gecko, is a huge part of why we’re able to experiment and learn as fast as we can. And that’s reflected with what’s possible here. It’s a web you can see, touch and interact with in new ways.*

*David’s post follows:*

I’m working with an ever growing group of web, audio, and Mozilla developers on [a project](http://vocamus.net/dave/?p=974) to expose audio spectrum data to JavaScript from Firefox’s audio and video elements. Today we show what we did at www2010.

I’m in Raleigh, North Carolina, with [Al MacDonald](https://twitter.com/F1LT3R/) for the [www2010](http://www2010.org/www/) conference. We’re here to present our work on exposing audio data in the browser. Over the past month [Corban](https://twitter.com/corban), [Charles](https://twitter.com/ccliffe), and a bunch of other friends have been working with us to refine the API and get new types of demos ready. We ended-up with 11 demos, some of which I’ve shown here before. Here are the others.

The first was done by [Jacob Seidelin](http://twitter.com/jseidelin), and shows many cool 2D visualizations of audio using our API. You can see the [live version](http://blog.nihilogic.dk/2010/04/html5-audio-visualizations.html) on his site, or check out [this video](http://vimeo.com/11355121):

The second and third demos where done by [Charles Cliffe](https://twitter.com/ccliffe), and show 3D visualizations using WebGL and his [CubicVR engine](http://www.cubicvr.org/). These also show off his JavaScript beat detection code. Is JavaScript fast enough to do real-time analysis of audio and synchronized 3D graphics? Yes, yes it is. The live versions are [here](http://cubicvr.org/CubicVR.js/BeatDetektor2HD.html) and [here](http://cubicvr.org/CubicVR.js/BeatDetektor1HD.html), and here are [some](http://vimeo.com/11345262) [videos](http://vimeo.com/11345685):

The fourth demo was done by [Corban Brook](https://twitter.com/corban) and shows how audio data can be mixed live using script. Here he mutes the main audio, plays it, passes the data through a low pass filter written in JavaScript, then dumps the modified frames into a second audio element to be played. It’s a technique we need to apply more widely, as it holds a lot of potential. Here’s the [live version](http://weare.buildingsky.net/processing/dsp.js/examples/filter.html), and here’s a [video](http://vimeo.com/11335434) (check out his updated [JavaScript synthesizer](http://weare.buildingsky.net/processing/dsp.js/examples/synthesizer.html), which we also presented):

The fifth and sixth demos were done by Al (with the help of many). When I was last in Boston, for the Processing.js meetup at Bocoup, we met with [Doug Schepers](http://twitter.com/shepazu) from the W3C. He loved our stuff, and was talking to us about ideas that would be cool to build. He pulled out his iPhone and showed us [Brian Eno’s Bloom](http://vimeo.com/2184392) audio app. “It would be cool to do this in the browser.” Yeah, it is cool, and here it is, written in a [few hundred lines of JavaScript and Processing.js](http://code.bocoup.com/bloop/color/bloop.html) ([video 1](http://vimeo.com/11346141), [video 2](http://vimeo.com/11345133)):

This demo also showcases the awesome work of [Felipe Gomes](http://felipe.wordpress.com/), who has a patch to add [multi-touch DOM events to Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=508906). The method we’ve used here can be taken a lot further. Imagine being able to connect multiple browsers together for collaborative music creation, layering other audio underneath, mixing fragments vs. just oscillators, etc. We built this one in a week, and the web is capable of a lot more.

One of the main points of our talk was to emphasize that what we’re talking about here isn’t just a concept, and it isn’t some far away future. This is real code, running in a real browser, and it’s all being done in HTML5 and JavaScript. The web is fast enough to do real-time audio processing now, powerful enough and expressive enough to create music. And the community of digital music and audio hackers, visualizers, etc. are hungry for it. So hungry that they are seeking us out, downloading our hacked builds and creating gorgeous web audio applications.

We want to keep going, and we need help. We need help from those within Mozilla, the W3C, and other browsers to get this stuff into shipping browsers. We need the audio, digital music, accessibility, and web communities to come together in order to help us build js audio libraries and more sample applications. Yesterday [Joe Hewitt was talking on twitter](http://twitter.com/joehewitt/status/13090747143) about how web browser vendors need to experiment more with non-standard APIs. I couldn’t agree more, and here’s a chance for people to put their money where their mouth is. Let’s make audio a scriptable part of the open web.

I’m currently creating new builds of our updated patch for Firefox, and will post links to them here when I’m done. You can read more about the technical details of our work [here](https://wiki.mozilla.org/Audio_Data_API), and get involved in the bug [here](https://bugzilla.mozilla.org/show_bug.cgi?id=490705). You can talk more with me on irc in the [processing.js channel](irc://irc.mozilla.org/processing.js) (I’m *humph* on moznet), or talk to me on twitter ([@humphd](http://twitter.com/humphd)) or by [email](mailto:david.humphrey@senecac.on.ca). One way or another, get in touch so you can help us push this forward.

## 12 comments

discoleoApril 30th, 2010 at 12:58AndyMay 1st, 2010 at 03:12John NashMay 3rd, 2010 at 17:48guapoMay 4th, 2010 at 17:20QOALMay 5th, 2010 at 06:13Kenneth ArnoldMay 7th, 2010 at 08:50carlMay 10th, 2010 at 12:46Nicholas BieberMay 24th, 2010 at 00:45F1LT3RSeptember 8th, 2010 at 15:33Thomas ThelliezOctober 10th, 2011 at 06:47