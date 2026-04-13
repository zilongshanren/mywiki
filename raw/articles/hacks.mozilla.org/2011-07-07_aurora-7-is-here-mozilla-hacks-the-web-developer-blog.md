---
title: Aurora 7 is here – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/07/aurora7/
author: Louisremi
published: '2011-07-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Keeping up the pace with our new development cycle, today we release Aurora 7. Enjoy its new features and performance improvements: CSS “ text-overflow: ellipsis“, Navigation Timing API, reduced memory usage, a faster javascript parser, and the first steps of Azure, our new graphics API.*

### text-overflow: ellipsis;

It is now possible to get Firefox to display “**…**” to give a visual clue that a text is longer than the element containing it.


### Navigation Timing

Performance is a key parameter of the user experience on the Web. To help Web developers monitor efficiently the performance of their Web pages, Aurora 7 implements the [Navigation Timing](http://dvcs.w3.org/hg/webperf/raw-file/tip/specs/NavigationTiming/Overview.html) specification: using the `window.performance.timing`

object, developers will be able to know the time when different navigation steps (such as `navigationStart`

, `connectStart`

/`End`

, `responseStart`

/`End`

, `domLoading`

/`Complete`

) happened and deduce how long one step or a sequence of steps took to complete.

### Reduced Memory Usage

Our continuous efforts to monitor and reduce memory consumption in Firefox will substantially pay off with Aurora 7:

- The memory “zone” where javascript objects reside gets fragmented as objects are created and deleted. To reduce the negative impact of this fragmentation, long-lived objects created by the browser’s own UI have been separated from the objects created by Web pages. The browser can now free memory more efficiently when a tab is closed or after a
[garbage collection](http://en.wikipedia.org/wiki/Garbage_collection_%28computer_science%29). - Speaking of garbage collection, as we successfully reduced the cost of this operation, we are able to execute it more often. Not only is memory freed more rapidly, but this also leads to shorter
*GC pauses*(the period where javascript execution stops to let the garbage collector do his job, which is sometime noticeable during heavy animations). - All those improvements are reflected in the about:memory page, which is now able to tell how much memory a particular Web page or the browser’s own UI, is using.

More frequent updates and detailed explanations of the *memshrink* effort are posted on [Nicholas Nethercote’s blog.](http://blog.mozilla.com/nnethercote/)

### Faster Javascript Parsing

A javascript **parser** is the part of the browser that reads the javascript before it gets executed by the javascript **engine**. With modern Web applications such as Gmail or Facebook sending close to 1Mb of javascript, being able to still read all of that code instantly matters in the quest of responsive user experience.

Thanks to [Nicholas’s work](http://blog.mozilla.com/nnethercote/2011/07/01/faster-javascript-parsing/), our parser is now almost twice as fast as it used to. This adds up well with our constant work to improve the [execution speed](http://arewefastyet.com) of our javascript engine.

### First Steps of Azure

After the **layout engine** (Gecko) has computed the visual appearance (position, dimension, colors, …) of all elements in the window, the browser *asks* the Operating System to actually draw them on the screen. The browser needs an abstraction layer to be able to *talk* to the different graphics libraries of the different OSes, but this layer has to be as thin and as adaptable as possible to deliver the promises of hardware acceleration.

*Azure* is the name of the new and better **graphics API**/abstraction layer that is going to gradually replace Cairo in hardware accelerated environments. In Aurora 7, it is already able to interact with Windows 7’s Direct2D API to render the content of a <canvas> element (in a 2D context). You can read a detailed explanation of [the Azure project and its next steps](http://blog.mozilla.com/joe/2011/04/26/introducing-the-azure-project/) on Joe Drew’s blog.

### Other Improvements

#### HTML

- The
`<a href="https://developer.mozilla.org/en/DOM/HTMLHeadElement" rel="custom nofollow">HTMLHeadElement</a>`

`profile`

property has been removed, this property has been deprecated since Gecko 2.0. (see[bug 664544](https://bugzilla.mozilla.org/show_bug.cgi?id=664544)) - The
`<a href="https://developer.mozilla.org/en/DOM/HTMLImageElement" rel="custom nofollow">HTMLImageElement</a>`

`x`

and`y`

properties have been removed. (see[bug 587021](https://bugzilla.mozilla.org/show_bug.cgi?id=587021)) - The
`<a href="https://developer.mozilla.org/en/DOM/HTMLSelectElement" rel="custom nofollow">HTMLSelectElement</a>`

`add()`

method`before`

parameter is now optional. (see[bug 182279](https://bugzilla.mozilla.org/show_bug.cgi?id=182279))

#### Canvas

- Specifying invalid values when calling
`setTransform()`

,`bezierCurveTo()`

, or`arcTo()`

no longer throws an exception; these calls are now correctly silently ignored. - Calling
`strokeRect`

with a zero width and height now correctly does nothing. (see[bug 663190](https://bugzilla.mozilla.org/show_bug.cgi?id=663190)) - Calling
`drawImage`

with a zero width or height`<a href="https://developer.mozilla.org/en/HTML/Element/canvas" rel="custom nofollow"><canvas></a>`

now throws`INVALID_STATE_ERR`

. (see[bug 663194](https://bugzilla.mozilla.org/show_bug.cgi?id=663194)) `toDataURL()`

method now accepts a second argument to control JPEG quality (see[bug 564388](https://bugzilla.mozilla.org/show_bug.cgi?id=564388))

### CSS

`<a href="https://developer.mozilla.org/en/CSS/text-overflow" rel="custom nofollow">text-overflow</a>`

is now supported.- The
`<a href="https://developer.mozilla.org/en/CSS/orient" rel="custom nofollow">-moz-orient</a>`

property has been fixed so that`<a href="https://developer.mozilla.org/en/HTML/Element/progress" rel="custom nofollow"><progress></a>`

elements that are vertically oriented have appropriate default dimensions.

### MathML

- XLink href has been restored and the MathML3
`href`

attribute is now supported. Developers are encouraged to move to the latter syntax. - Support for the
`voffset`

attribute on`<a href="https://developer.mozilla.org/en/MathML/Element/mpadded" rel="custom nofollow"><mpadded></a>`

elements has been added and behavior of`lspace`

attribute has been fixed. - The top-level
`<a href="https://developer.mozilla.org/en/MathML/Element/math" rel="custom nofollow"><math></a>`

element accepts any attributes of the`<a href="https://developer.mozilla.org/en/MathML/Element/mstyle" rel="custom nofollow"><mstyle></a>`

element. - The
`medium`

line thickness of fraction bars in`<a href="https://developer.mozilla.org/en/MathML/Element/mfrac" rel="custom nofollow"><mfrac></a>`

elements has been corrected to match the default thickness. [Names for negative spaces](https://developer.mozilla.org/en/MathML/Attributes/Values#Constants_%28namedspaces%29)are now supported.

### DOM

- The
`<a href="https://developer.mozilla.org/en/DOM/File" rel="custom nofollow">File</a>`

interface’s non-standard methods`getAsBinary()`

,`getAsDataURL()`

, and`getAsText()`

have been removed as well as the non-standard properties`fileName`

and`fileSize`

. - The
`<a href="https://developer.mozilla.org/en/DOM/FileReader" rel="custom nofollow">FileReader</a>`

`readAsArrayBuffer()`

method is now implemented. (see[bug 632255](https://bugzilla.mozilla.org/show_bug.cgi?id=632255)) `<a href="https://developer.mozilla.org/en/DOM/document.createEntityReference" rel="custom nofollow">document.createEntityReference</a>`

has been removed. It was never properly implemented and is not implemented in most other browsers. (see[bug 611983](https://bugzilla.mozilla.org/show_bug.cgi?id=611983))`document.normalizeDocument`

has been removed. Use`<a href="https://developer.mozilla.org/en/DOM/Node.normalize" rel="custom nofollow">Node.normalize</a>`

instead. (see[bug 641190](https://bugzilla.mozilla.org/show_bug.cgi?id=641190))`<a href="https://developer.mozilla.org/en/DOM/DOMTokenList.item" rel="external">DOMTokenList.item</a>`

now returns`undefined`

if the`index`

is out of bounds, previously it returned`null`

. (see[bug 529328](https://bugzilla.mozilla.org/show_bug.cgi?id=529328))`Node.getFeature`

has been removed. (see[bug 659053](https://bugzilla.mozilla.org/show_bug.cgi?id=659053))

### JavaScript

- The
`<a href="https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Function/arity" rel="internal">Function.arity()</a>`

function has been removed; use`<a href="https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Function/length" rel="internal">Function.length</a>`

instead. - The JSON parser has been re-written for improved speed and compliance. This includes a fix for
[bug 572279](https://bugzilla.mozilla.org/show_bug.cgi?id=572279).

### console API

- Implement
`console.<a href="http://getfirebug.com/wiki/index.php/Console_API#console.dir.28object.29">dir()</a>`

,`console.<a href="http://getfirebug.com/wiki/index.php/Console_API#console.time.28name.29">time()</a>`

,`console.<a href="http://getfirebug.com/wiki/index.php/Console_API#console.timeEnd.28name.29">timeEnd()</a>`

,`console.<a href="http://getfirebug.com/wiki/index.php/Console_API#console.group.28object.5B.2C_object.2C_....5D.29">group()</a>`

and`console.<a href="http://getfirebug.com/wiki/index.php/Console_API#console.groupEnd.28.29">groupEnd()</a>`

methods. - Message logged with console.log before the WebConsole is opened are now stored and displayed once the WebConsole is opened.

(see the [Web Console](https://wiki.mozilla.org/DevTools/Features/WebConsole7) page in the Wiki)

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 27 comments

GavraJuly 7th, 2011 at 13:13SkouaJuly 7th, 2011 at 14:09AldonioJuly 7th, 2011 at 14:11BorisJuly 7th, 2011 at 16:12David BruantJuly 7th, 2011 at 14:25Claudio CicaliJuly 7th, 2011 at 14:37louisremiJuly 8th, 2011 at 11:37Brian BlakelyJuly 7th, 2011 at 14:52MrSJuly 7th, 2011 at 15:08louisremiJuly 8th, 2011 at 11:29eobeJuly 7th, 2011 at 16:32PCビギナーJuly 7th, 2011 at 19:55nnethercoteJuly 7th, 2011 at 19:58Jeff WaldenJuly 7th, 2011 at 20:31Georgiy IvankinJuly 7th, 2011 at 21:46InsanoJuly 8th, 2011 at 02:07JasonJuly 8th, 2011 at 09:23louisremiJuly 8th, 2011 at 11:34RobJuly 10th, 2011 at 06:47juanJuly 11th, 2011 at 08:56artJuly 11th, 2011 at 14:00SethJuly 12th, 2011 at 15:55sunJuly 14th, 2011 at 09:51MajorJuly 19th, 2011 at 06:53SauAugust 20th, 2011 at 10:09AnnieAugust 25th, 2011 at 08:51Dennis SchultzeNovember 20th, 2011 at 08:52