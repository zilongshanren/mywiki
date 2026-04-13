---
title: Firefox 4 beta 1 is here – what's in it for web developers? – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2010/07/firefox-4-beta-1-is-here-whats-in-it-for-web-developers/
author: Christopher Blizzard
published: '2010-07-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today we’re [releasing the first beta-quality version of Firefox 4](http://www.mozilla.com/en-US/firefox/beta/), which starts us down the path to a final release of Firefox 4. We’re handling this beta differently than we’ve done other releases. In previous betas we’ve made milestone-like releases. For this beta we’ll be making more frequent updates during the beta program. So if you download the beta build and run it you’ll likely get updates every two to three weeks, instead of a couple of months apart. We believe that this will give us the ability to reply to people’s feedback quickly and get fixes and changes tested earlier. This, in turn, will mean we’ll be able to release a much higher quality browser as a result.

First, let’s talk about feedback. This beta includes two ways to give us feedback.

![](http://farm2.static.flickr.com/1373/4728758428_bc8645d408.jpg)


**The Feedback Button** – Pictured above and included with the beta is a Feedback Add-on. This puts a big Feedback button on the right hand side of the browser that lets you give quick and easy feedback about something you like or something you don’t. We’ll be reviewing this feedback through the beta process, so please leave comments. The Add-On also uses [Test Pilot](https://testpilot.mozillalabs.com/) to figure out how people use the browser – [menus](http://mozillalabs.com/testpilot/2010/03/17/popular-menu-buttons/), [how people use passwords](http://mozillalabs.com/testpilot/2009/12/15/accounts-and-passwords/), etc. But through this beta process we’ll also be using it to measure things like platform performance and other interesting data we need to build a great browser. Just like Test Pilot, no data will be collected without you knowing about it, you’ll always be asked before any collected data is sent from your computer to Mozilla, and that data will be subject to very strict [privacy policies](http://www.mozilla.com/firefox/beta/feedbackprivacypolicy/).

If you’re a web developer the beta process will be especially valuable. There are a lot of new features in Firefox 4.0b1 that weren’t in 3.6 – which we’ll go over – but we’ll keep adding and fixing features throughout the beta process and your feedback will be incredibly important. So please take the time to download the beta and try it. Run it all the time, if you can, and watch it change over time.

**Performance**

Firefox 4 contains a large number of performance improvements over Firefox 3.6. As a web developer you’re likely to notice big improvements in overall performance.

**DOM and Style Performance** – We’ve made huge improvements in our DOM and style resolution engine, meaning that pages that have complex CSS rules and selector matching will generally work faster and better. (On some tests in the Zimbra performance test suite we’ve seen a solid 2x improvement.)

**Reduced IO in the page load path** – One big area where we’ve made huge improvements in Firefox 4 vs. 3.6 is the [removal of tons of I/O from the main UI thread](https://wiki.mozilla.org/Firefox/Goals/2010Q1/IO_Reduction). This means making sure that when we do history look-ups for coloring links based on browser history, that those look-ups are done off the main thread, to making sure that we’re not synchronously writing data to the HTTP cache on the main thread. This alone has improved the overall feel of the browser more than anything else.

**JavaScript** – The JavaScript engine is much faster as well, although beta 1 does *not* include the new [JägerMonkey](http://hacks.mozilla.org/2010/03/improving-javascript-performance-with-jagermonkey/) work. That work is well underway and will be landing through the beta process, and is already [showing positive results](http://arewefastyet.com/).

**Hardware Acceleration via Layers** – We’ve also got excellent support in this beta for Hardware Acceleration. If you’re using HTML5 video and you go full screen, we’ll use OpenGL on Macs or Linux and DirectX 9 on Windows to accelerate video rendering. (As we expand our [Gecko Layers](https://wiki.mozilla.org/Gecko:Layers) work we’ll also be extending this acceleration to in-page content where it makes sense.)

**Hardware Acceleration via D2D** If you’re on Windows 7 or an updated Windows Vista we also have [full support for D2D-enabled rendering](http://www.basschouten.com/blog1.php/2009/11/22/direct2d-hardware-rendering-a-browser). This can be a *substantial* performance improvement for many types of rendering and is also something the IE team is also doing for IE9. It’s not on by default in this beta but you can easily [turn it on](http://www.basschouten.com/blog1.php/2010/03/02/presenting-direct2d-hardware-acceleratio) and try it out. The best demos that we’ve seen for D2D support are actually the [IE Flying Images](http://ie.microsoft.com/testdrive/Performance/01FlyingImages/Default.html) and the [IE Flickr Explorer](http://ie.microsoft.com/testdrive/Performance/10FlickrExplorer/Default.html) demo. Firefox actually performs wonderfully on these demos, better than the IE9 builds in most cases.

**Out of process plugins – even for the Mac** – We already delivered out of process plugins to Windows and Linux users using 3.6 a couple of weeks ago, but it’s now available on OSX as well. Moving plugins out of process improves stability, responsiveness and memory consumption. For OSX we have support for running Flash 10.1 out of process on OSX 10.6. (It requires support from 10.6 and changes to the event models for both Firefox and individual plugins.)

**HTML5 support**

Firefox has had [early and excellent support for HTML5](http://caniuse.com/#cats=HTML5&statuses=rec,pr,cr,wd,ietf) and the beta release continues to build on that history.

**HTML5 Forms** – We’ve started to land support for many [HTML5 forms](https://wiki.mozilla.org/User:Mounir.lamouri/HTML5_Forms). We’ll be landing more HTML5 form features during the beta process opportunistically depending on pretty tough [shipping criteria](https://wiki.mozilla.org/User:Mounir.lamouri/HTML5_Forms#Shipping_Criteria).

**HTML5 Sections** – We now support HTML5 sections like `<article>, <section>, <nav>, <aside>, <hgroup>, <header> and <footer>.`


**WebSockets** – This release includes support for [WebSockets](http://jimbergman.net/tag/websocket-example/), based on version -76 of the spec.

**HTML5 History** – We’ve also got support for the new HTML5 history items: [ pushState and replaceState](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history#Adding_and_modifying_history_entries). These are very important calls that make it easier to build pages-as-applications and can also be very important for improving privacy as you move from site to site.


**HTML5 Parser** – We’re also the first browser to fully support the HTML5 parsing algorithm, one of the most important parts of the HTML5 spec. The parser allows us to [embed SVG and MathML directly into HTML content](http://hacks.mozilla.org/2010/05/firefox-4-the-html5-parser-inline-svg-speed-and-more/), but also promises developers the ability to have the same behaviour in different browsers, even when developers make mistakes in their mark-up. Our hope is that other browsers will follow us on this work since it’s one of the biggest interoperability parts of the HTML5 specification and will really help developers.

And, of course, we have support for HTML5 Canvas (including D2D hardware acceleration), Video and a huge pile of other HTML5 technologies.

**HTML5 Video**

**WebM Support** – The biggest change here so far is that we’ve got support for [WebM](http://hacks.mozilla.org/2010/05/firefox-youtube-and-webm/). If you’re part of the [Youtube HTML5](http://www.youtube.com/html5) beta WebM videos should play pretty well.

**Other, upcoming interfaces** – Note that through the beta process we’ll also be adding support for a JavaScript-driven full screen API for video, support for the `buffered`

attribute and be renaming the `autobuffer`

attribute to `preload`

.

**Storage and File API**

**IndexedDB** – Firefox 4 beta 1 also includes a super-early snapshot of the new [IndexedDB standard for storage](http://dvcs.w3.org/hg/IndexedDB/raw-file/tip/Overview.html). Due to the fast pace in changes in the standard, the object is available on the privately-namespaced `window.moz_indexedDB`

object. This is a pretty complex item, and we’ll have more posts on it soon.

**URI Support for the File API** – We’ve also early support for the URI support inside of the File API. This means that it’s possible to process large amounts of data like images or videos from the File API without having to load the entire file into memory. You should also be able to reference private File API URLs in image and video tags for preview or manipulation.

**FormData** – We also have support for the [FormData](http://hacks.mozilla.org/2010/05/formdata-interface-coming-to-firefox/) method, which makes it much easier to send complex data from the File API and other sources to servers.

**Animation and Graphics**

**SMIL** – We’ve added support for SVG Animation (SMIL.) If you’re running a 4.0 beta there are a huge number of [beautiful examples on this page by David Dailey](http://srufaculty.sru.edu/david.dailey/svg/SVGAnimations.htm#SMIL) worth looking through.

**SVG Everywhere** – Later in the Firefox beta release cycle we’ll also be adding support for SVG-as-img and SVG-as-CSS-background. Most of that work is done, but it hasn’t landed yet.

**CSS Transitions** – This beta release contains a nearly complete implementation of [CSS Transitions](https://developer.mozilla.org/en/CSS/CSS_transitions), privately namespaced with a `-moz`

prefix. The only big things left here are the animation of transforms and gradients. (Gradients is still waiting on working group feedback, code for transitions is under review.)

**WebGL** – This build also has improved support for WebGL, although it is not yet on by default. (You can learn how to [turn it on in an older post from Vlad](http://blog.vlad1.com/2009/09/18/webgl-in-firefox-nightly-builds/).) The WebGL spec is on its way to a 1.0 release and is being implemented in Chrome, Safari and Firefox. We would like to ship it in Firefox 4, but that decision will be based on spec stability as well as the availability of drivers. If you’re on a Mac WebGL should work very well. On Windows with ATI and NVIDIA drivers, it should also work very well. Windows people with Intel drivers are in less luck due to very poor driver support from Intel. (Including your author!) Linux is more complicated due to wildly varying driver support – people with NVIDIA drivers seem to work well, others less so, but work is underway to help fix many issues on Linux.

**CSS**

**Resizable textarea Elements** – Textarea elements are now resizable by default. You can use the

`<a href="https://developer.mozilla.org/en/CSS/-moz-resize">-moz-resize</a>`

property to change the default.**New -moz-any selector** – The

`-moz-any`

is a powerful selector that lets you replace large and complicated selectors with much smaller ones. Please see the [post for more examples.](http://hacks.mozilla.org/2010/05/moz-any-selector-grouping/)

**New CSS3 calc() support** – This beta includes support for the new CSS3 calc() value. This lets you specify sizes that include a combination of percentages and absolute values and is hugely popular with developers. Please see the

[post on CSS3 calc](http://hacks.mozilla.org/2010/06/css3-calc/)for examples.

**Selecting a section of a background image** – You can now use the new `-moz-image-rect`

selector to select only a section of a background for display.

**Removed support for -moz-background-size** – The

`-moz-background-size`

property has been renamed to its final `<a href="https://developer.mozilla.org/en/CSS/background-size">background-size</a>`

name. `-moz-background-size`

is no longer supported.**DOM and Events**

**CSS Touch Source on Input Events** – You can now tell if an input event came from a mouse or touch with `<a href="https://developer.mozilla.org/en/DOM/event.mozInputSource">event.mozInputSource</a>`

.

**Obtaining boundary rectangles for ranges** – The Range object now has `getClientRects()`

and `getBoundingClientRect()`

methods.

**Capturing mouse events on arbitrary elements** – Support for the Internet Explorer-originated `setCapture()`

and `releaseCapture()`

APIs has been added.

**Support for document.onreadystatechange** – We now support the

`<a href="https://developer.mozilla.org/en/DOM/document.onreadystatechange">document.onreadystatechange</a>`

.**Security**

**Content Security Policy** – This beta contains support for [Content Security Policy](http://people.mozilla.org/~bsterne/content-security-policy/). CSP allows you to control what the browser is allowed to do when loading content from your site. CSP is built to mitigate Cross-site Scripting Attacks and Cross Site Request Forgery. It also contains an automated reporting mechanism so that admins can get reports of problems that may affect other browsers.

**In Closing**

So that’s about it for the start of the Firefox 4 beta. We’ll be adding a few more features during the beta release process and we’ll post about is as they land. And we’ll also have more information coming about some of these features in depth. And, of course, we’ll continue to work on performance through the beta process as well. Please test and post comments if you have them here, or use the Feedback system in Firefox.

Enjoy!

## 55 comments

Johannes FahrenkrugJuly 6th, 2010 at 23:12JonJuly 6th, 2010 at 23:40MaxenceJuly 6th, 2010 at 23:53jpvincentJuly 7th, 2010 at 02:38bohwazJuly 7th, 2010 at 03:29brightsideJuly 7th, 2010 at 06:44tiredofsyncNovember 12th, 2010 at 09:52aleemJuly 7th, 2010 at 06:11Christopher BlizzardJuly 15th, 2010 at 20:50MarcelJuly 7th, 2010 at 06:36SevishJuly 7th, 2010 at 07:46peteruhdsJuly 7th, 2010 at 07:58Christopher BlizzardJuly 15th, 2010 at 20:50j2July 7th, 2010 at 08:37bliblibliJuly 7th, 2010 at 08:42shmerlJuly 7th, 2010 at 21:03Kobold AvengerJuly 7th, 2010 at 09:58Christopher BlizzardJuly 15th, 2010 at 20:52enotionzJuly 7th, 2010 at 10:07David StarrJuly 7th, 2010 at 10:21Christopher BlizzardJuly 15th, 2010 at 20:52shmerlJuly 7th, 2010 at 12:28Christopher BlizzardJuly 15th, 2010 at 20:52shmerlJuly 21st, 2010 at 18:23bobJuly 7th, 2010 at 18:14Pikadude No. 1July 7th, 2010 at 18:57Christopher BlizzardJuly 15th, 2010 at 20:55Manojr TiwariJuly 7th, 2010 at 23:41standrJuly 8th, 2010 at 19:13Christopher BlizzardJuly 15th, 2010 at 20:56DerFichtlJuly 9th, 2010 at 05:03Christopher BlizzardJuly 15th, 2010 at 20:57Ivan KruchkoffJuly 9th, 2010 at 08:30thiagoJuly 9th, 2010 at 13:19MortezaJuly 13th, 2010 at 04:46PradanaJuly 13th, 2010 at 06:11Mike WilcoxJuly 15th, 2010 at 10:55Christopher BlizzardJuly 15th, 2010 at 20:59MortezaJuly 15th, 2010 at 23:16TihomirJuly 16th, 2010 at 02:37amosngweienJuly 16th, 2010 at 20:10MortezaJuly 17th, 2010 at 02:47philjamlineJuly 22nd, 2010 at 08:50Komrade KilljoyJuly 28th, 2010 at 05:54Komrade KilljoyJuly 28th, 2010 at 06:11ArthurAugust 4th, 2010 at 15:48HarshaAugust 11th, 2010 at 02:24ArthurAugust 11th, 2010 at 09:24designerashishNovember 12th, 2010 at 02:15Beto G.November 18th, 2010 at 18:55DougDecember 30th, 2010 at 10:02designerashishDecember 7th, 2011 at 03:16David C.February 2nd, 2011 at 00:17Er.Batish, MCSEAugust 31st, 2011 at 20:09Puneet BatishAugust 6th, 2012 at 07:01