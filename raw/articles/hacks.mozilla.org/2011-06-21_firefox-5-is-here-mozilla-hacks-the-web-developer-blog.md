---
title: Firefox 5 is here – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/06/firefox5/
author: Jay Patel
published: '2011-06-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Today, three months after the release of Firefox 4, we release Firefox 5, thanks to our new development cycle. Developers will be able to create richer animations using CSS3 Animations. This release comes with various improvements, performance optimization and bug fixes.*

### CSS3 Animations

CSS Animations (check out the [documentation](https://developer.mozilla.org/en/CSS/CSS_animations)) are a new way to create animations using CSS. Like [CSS Transitions](https://developer.mozilla.org/en/CSS/CSS_transitions), they are efficient and run smoothly (see David Baron’s [article](http://dbaron.org/log/20110615-animations)), and the developers have a better controls over the intermediate steps (* keyframes*), and can now create much more complex animations.

### Notable changes

- You can now pass an image as a parameter to
[createImageData](https://developer.mozilla.org/En/HTML/Canvas/Pixel_manipulation_with_canvas)to copy its dimensions. [setTimeout](https://developer.mozilla.org/en/window.setTimeout)and[setInterval](https://developer.mozilla.org/En/window.setInterval)will only be able to execute callbacks once per second in inactive tabs. This follows the behavior of[requestAnimationFrame](https://developer.mozilla.org/en/DOM/window.mozRequestAnimationFrame)to save CPU and power consumption.

### Other Bug Fixes and Performance Improvements:

#### HTML

- All HTML elements now have the
`<a class="new" href="https://developer.mozilla.org/en/DOM/element.accessKey">accessKey</a>`

attribute, as well as the`<a href="https://developer.mozilla.org/en/DOM/element.blur">blur()</a>`

,`<a href="https://developer.mozilla.org/en/DOM/element.click">click()</a>`

, and`<a href="https://developer.mozilla.org/en/DOM/element.focus">focus()</a>`

methods. These are specified in the`<a href="https://developer.mozilla.org/en/DOM/HTMLElement">HTMLElement</a>`

interface. - In order to comply with the HTML5 specification, support for the UTF-7 and UTF-32
[character sets](https://developer.mozilla.org/en/Character_Sets_Supported_by_Gecko)has been removed. - When in quirks mode, empty
`<a href="https://developer.mozilla.org/en/HTML/Element/map"><map></a>`

s are no longer skipped over in favor of non-empty ones when matching. See the[Gecko notes](https://developer.mozilla.org/en/HTML/Element/map#Gecko_notes)on the`<a href="https://developer.mozilla.org/en/HTML/Element/map"><map></a>`

element for details. - Firefox mobile on Android now supports WOFF fonts for
`<a href="https://developer.mozilla.org/en/CSS/@font-face">@font-face</a>`

. - WebGL
[no longer loads textures from domains other than the originating domain](https://developer.mozilla.org/en/WebGL/Cross-Domain_Textures), as a security measure.

#### Canvas improvements

- The
`<a href="https://developer.mozilla.org/en/HTML/Element/canvas"><canvas></a>`

2D drawing context now supports specifying an`ImageData`

object as the input to the`createImageData()`

method; this[creates a new](https://developer.mozilla.org/En/HTML/Canvas/Pixel_manipulation_with_canvas#Creating_an_ImageData_object)initialized with the same dimensions as the specified object, but still with all pixels preset to transparent black.`ImageData`

object - Specifying non-finite values when adding color stops through a call to the
`<a href="https://developer.mozilla.org/en/DOM/CanvasGradient">CanvasGradient</a>`

method`addColorStop()`

now correctly throws`INDEX_SIZE_ERR`

instead of`SYNTAX_ERR`

. - The
`<a href="https://developer.mozilla.org/en/DOM/HTMLCanvasElement">HTMLCanvasElement</a>`

method`toDataURL()`

now correctly lower-cases the specified MIME type before matching. `getImageData()`

now correctly accepts rectangles that extend beyond the bounds of the canvas; pixels outside the canvas are returned as transparent black.`drawImage()`

and`createImageData()`

now handle negative arguments in accordance with the specification, by flipping the rectangle around the appropriate axis.- Specifying non-finite values when calling
`createImageData()`

now properly throws a`NOT_SUPPORTED_ERR`

exception. `createImageData()`

and`getImageData()`

now correctly return at least one pixel’s worth of image data if a rectangle smaller than one pixel is specified.- Specifying a negative radius when calling
`createRadialGradient()`

now correctly throws`INDEX_SIZE_ERR`

. - Specifying a
`null`

or`undefined`

image when calling`createPattern()`

or`drawImage()`

now correctly throws a`TYPE_MISMATCH_ERR`

exception. - Specifying invalid values for
`globalAlpha`

no longer throws a`SYNTAX_ERR`

exception; these are now correctly silently ignored. - Specifying invalid values when calling
`translate()`

,`transform()`

,`rect()`

,`clearRect()`

,`fillRect()`

,`strokeRect()`

,`lineTo()`

,`moveTo()`

,`quadraticCurveTo()`

, or`arc()`

no longer throws an exception; these calls are now correctly silently ignored. - Setting the value of
`shadowOffsetX`

,`shadowOffsetY`

, or`shadowBlur`

to an invalid value is now silently ignored. - Setting the value of
`rotate`

or`scale`

to an invalid value is now silently ignored.


#### DOM

- The
`<a href="https://developer.mozilla.org/en/DOM/selection">selection</a>`

object’smethod has been changed so that the “word” selection granularity no longer includes trailing spaces; this makes it more consistent across platforms and matches the behavior of WebKit’s implementation.`modify()`

- The
`<a href="https://developer.mozilla.org/en/DOM/window.setTimeout">window.setTimeout()</a>`

method now clamps to send no more than one timeout per second in inactive tabs. In addition, it now clamps nested timeouts to the smallest value allowed by the HTML5 specification: 4 ms (instead of the 10 ms it used to clamp to). - Similarly, the
`<a href="https://developer.mozilla.org/en/DOM/window.setInterval">window.setInterval()</a>`

method now clamps to no more than one interval per second in inactive tabs. now`XMLHttpRequest`

[supports the](https://developer.mozilla.org/En/XMLHttpRequest/Using_XMLHttpRequest#Detecting_any_load_end_condition)for progress listeners. This is sent after any transfer is finished (that is, after the`loadend`

event`abort`

,`error`

, or`load`

event). You can use this to handle any tasks that need to be performed regardless of success or failure of a transfer.- The
`<a href="https://developer.mozilla.org/en/DOM/Blob">Blob</a>`

and, by extension, the`<a href="https://developer.mozilla.org/en/DOM/File">File</a>`

objects’`slice()`

method has been removed and replaced with a new, proposed syntax that makes it more consistent withand`Array.slice()`

methods in JavaScript. This method is named`String.slice()`

for now.`mozSlice()`

- The value of
`<a href="https://developer.mozilla.org/en/DOM/window.navigator.language">window.navigator.language</a>`

is now determined by looking at the value of the`Accept-Language`

[HTTP header](https://developer.mozilla.org/en/HTTP/Headers).


#### JavaScript

- Regular expressions are no longer callable as if they were functions; this change has been made in concert with the WebKit team to ensure compatibility (see
[WebKit bug 28285](https://bugs.webkit.org/show_bug.cgi?id=28285)). - The
method is now supported; this lets you determine if a function is a`Function.prototype.isGenerator()`

[generator](https://developer.mozilla.org/en/JavaScript/Guide/Iterators_and_Generators#Generators.3a_a_better_way_to_build_Iterators).

#### SVG

- The
`<a href="https://developer.mozilla.org/en/SVG/Attribute/class">class</a>`

SVG attribute can now be animated. - The following SVG-related DOM interfaces representing lists of objects are now indexable and can be accessed like arrays; in addition, they have a
`length`

property indicating the number of items in the lists:`<a class="new" href="https://developer.mozilla.org/en/DOM/SVGLengthList">SVGLengthList</a>`

,`<a class="new" href="https://developer.mozilla.org/en/DOM/SVGNumberList">SVGNumberList</a>`

,`<a class="new" href="https://developer.mozilla.org/en/DOM/SVGPathSegList">SVGPathSegList</a>`

, and`<a class="new" href="https://developer.mozilla.org/en/DOM/SVGPointList">SVGPointList</a>`

.

#### HTTP

- Firefox no longer sends the “Keep-Alive” HTTP header; we weren’t formatting it correctly, and it was redundant since we were also sending the
`<a href="https://developer.mozilla.org/en/HTTP/Headers#Connection">Connection:</a>`

or`<a href="https://developer.mozilla.org/en/HTTP/Headers#Proxy-Connection">Proxy-Connection:</a>`

header with the value “keep-alive” anyway. - The HTTP transaction model has been updated to be more intelligent about reusing connections in the persistent connection pool; instead of treating the pool as a
[FIFO](http://en.wikipedia.org/wiki/FIFO)queue, Necko now attempts to sort the pool with connections with the largest[congestion window](http://en.wikipedia.org/wiki/congestion window)(CWND) first. This can reduce the round-trip time (RTT) of HTTP transactions by avoiding the need to grow connections’ windows in many cases. - Firefox now handles the Content-Disposition HTTP response header more effectively if both the
`filename`

and`filename*`

parameters are provided; it looks through all provided names, using the`filename*`

parameter if one is available, even if a`filename`

parameter is included first. Previously, the first matching parameter would be used, thereby preventing a more appropriate name from being used. See[bug 588781](https://bugzilla.mozilla.org/show_bug.cgi?id=588781).

#### Developer tools

- The
[Web Console’s](https://developer.mozilla.org/en/Using_the_Web_Console#The_console_object)now has a`Console`

object`debug()`

method, which is an alias for its`log()`

method; this improves compatibility with certain existing sites.

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 120 comments

Michael ButlerJune 21st, 2011 at 07:37SkatoxJune 21st, 2011 at 07:40BrandonJune 21st, 2011 at 07:51Jwalant Natvarlal SonejiJune 22nd, 2011 at 12:553615BuckJune 21st, 2011 at 07:57Broken SkeletonJune 21st, 2011 at 08:11louisremiJune 21st, 2011 at 08:30SamuelJune 21st, 2011 at 11:13RyanJune 21st, 2011 at 12:39Broken SkeletonJune 21st, 2011 at 23:21RicardoJune 22nd, 2011 at 06:55AnnaJune 22nd, 2011 at 09:38Stefan MielkeJune 22nd, 2011 at 10:39GeraldJune 21st, 2011 at 08:22Markus KlugJune 21st, 2011 at 08:22MoeJune 21st, 2011 at 08:24OzzypigJune 21st, 2011 at 08:25Jon ReidJune 21st, 2011 at 08:41pdJune 21st, 2011 at 09:11ErunnoJune 21st, 2011 at 12:17tongJune 21st, 2011 at 09:16IHWAN INDESIGNJune 21st, 2011 at 09:18FatihJune 21st, 2011 at 09:23JamoJune 21st, 2011 at 09:26DavidJune 21st, 2011 at 09:36lazJune 22nd, 2011 at 06:36MikeJune 21st, 2011 at 09:44zenwalkerJune 21st, 2011 at 09:44AlbertJune 21st, 2011 at 10:18Admiral PotatoJune 21st, 2011 at 19:44Jon ReidJune 21st, 2011 at 11:13SteveJune 22nd, 2011 at 07:27AlexJune 21st, 2011 at 11:26DebbieJune 21st, 2011 at 17:16AmithJune 21st, 2011 at 17:46MarkJune 21st, 2011 at 19:04Gaurav MJune 21st, 2011 at 23:29saurabh kumarJune 21st, 2011 at 23:45ionJune 22nd, 2011 at 01:35CJ SpencerJune 22nd, 2011 at 02:45WeboideJune 22nd, 2011 at 05:02Teodor SanduJune 22nd, 2011 at 06:48gregJune 22nd, 2011 at 07:15Christian SciberrasJune 22nd, 2011 at 07:24Mark JohnsonJune 22nd, 2011 at 07:25Christian SciberrasJune 22nd, 2011 at 07:28Max ZhaoJune 22nd, 2011 at 07:28bearmosJune 22nd, 2011 at 07:54deanJune 22nd, 2011 at 08:06HarryJune 22nd, 2011 at 08:37MikeJune 22nd, 2011 at 08:38Tim KeatingJune 22nd, 2011 at 09:01xLoneJune 22nd, 2011 at 10:36OliverJune 22nd, 2011 at 10:52JohnJune 22nd, 2011 at 11:59AldonioJune 22nd, 2011 at 12:20John from Zombie ProcessusJune 22nd, 2011 at 13:45DanielJune 22nd, 2011 at 14:53NanashiJune 22nd, 2011 at 17:47Dennis VJune 22nd, 2011 at 15:04Todd FoxJune 22nd, 2011 at 17:01Christian SciberrasJune 23rd, 2011 at 07:19Kabindra BakeyJune 22nd, 2011 at 22:45Tameem ZaaiterJune 23rd, 2011 at 08:41Bill TheodJune 23rd, 2011 at 09:08louisremiJune 24th, 2011 at 09:07Bill TheodJune 25th, 2011 at 02:31PaulJune 23rd, 2011 at 15:41louisremiJune 24th, 2011 at 09:11PaulJune 24th, 2011 at 16:45Big RedAugust 17th, 2011 at 10:56DonJune 23rd, 2011 at 20:26louisremiJune 24th, 2011 at 09:14volochJune 26th, 2011 at 11:25louisremiJune 27th, 2011 at 05:58DazzaJJune 24th, 2011 at 04:16jswidgetJune 24th, 2011 at 05:41SerpJune 24th, 2011 at 05:51DebbieJune 24th, 2011 at 10:10Carmen BrodeurJune 24th, 2011 at 10:44Rune JensenJune 24th, 2011 at 11:49WebgranthJune 24th, 2011 at 21:55RyanJune 25th, 2011 at 05:23But How?June 26th, 2011 at 20:41RyanJune 27th, 2011 at 07:06Big RedAugust 17th, 2011 at 10:58Alexander GelbukhJune 25th, 2011 at 06:30Anupam GangopadhyayJune 25th, 2011 at 08:01louisremiJune 27th, 2011 at 06:01obiwahnJune 25th, 2011 at 09:27Andres RiofrioJune 25th, 2011 at 15:01PigletJune 26th, 2011 at 10:28SnapafunJune 27th, 2011 at 05:04ericaJune 27th, 2011 at 18:57ArsimaelJune 28th, 2011 at 06:54R-JAugust 10th, 2011 at 16:29haroldandresmeJune 28th, 2011 at 19:20SnapafunJune 29th, 2011 at 02:32SnapafunJune 29th, 2011 at 03:04joshJuly 2nd, 2011 at 13:10SnapafunJuly 3rd, 2011 at 04:17obiwahnJuly 4th, 2011 at 03:03rayblanJuly 5th, 2011 at 01:20snoopyJuly 7th, 2011 at 04:18louisremiJuly 7th, 2011 at 05:36anandJuly 7th, 2011 at 14:37anandJuly 7th, 2011 at 14:38RobJuly 10th, 2011 at 06:26laz123July 10th, 2011 at 11:21SethJuly 12th, 2011 at 15:53GemmaAugust 15th, 2011 at 08:01PeterSeptember 1st, 2011 at 13:35Cookie MonsterSeptember 7th, 2011 at 18:43some random userSeptember 10th, 2011 at 02:54RobSeptember 21st, 2011 at 06:47Web DevOctober 12th, 2011 at 05:26F. DotzlerOctober 29th, 2011 at 11:47jeuxdotnetNovember 1st, 2011 at 10:27Gary BrownApril 25th, 2012 at 02:09Jean-Yves PerrierApril 25th, 2012 at 17:00