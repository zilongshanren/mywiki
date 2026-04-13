---
title: Firefox 4 Beta 9 – a huge pile of awesome – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/01/firefox-4-beta-9-a-huge-pile-of-awesome/
author: Christopher Blizzard
published: '2011-01-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Hello, and welcome to the post for Firefox 4 beta 9. If you’re reading this then you’re interested in what we’ve got coming down the pipe for the latest beta for the wonderful browser known as Firefox 4. We’re starting to reach the end of our development cycle for the next release of Firefox and I thought it might be worth it to give a full overview of everything that we’ve got in store for web developers vs. Firefox 3.6. So if you’ve read previous releases, some of this will look familiar. But this is a new beta and we’ve been busy, so there’s something new in here for everyone.

### Performance

One of Firefox 4’s main themes is Performance. As such, we’ve done a huge amount of work to improve browser performance across the board, from startup time, to JavaScript performance, to interactive performance and making the user interface easier and more efficient to drive. That being said, here are some of the things we’ve done to improve performance up to Beta 9.

**The JaegerMonkey has landed.**

And you might have noticed that it’s [really fast](http://blog.mozilla.com/rob-sayre/2010/09/14/release-the-kraken/). This is the world’s first third-generation JavaScript engine, using Baseline JIT technology similar to engines found in other browsers and kicked up a level with the Tracing engine found in Firefox 3.6. As such, we’re competitive on benchmarks such as [Sunspider and V8](http://arewefastyet.com/), but we’re also fast at a whole mess of things that we expect to see in the set of next-generation web applications, hence [Kraken](http://krakenbenchmark.mozilla.com/).

**Hardware Acceleration**

Firefox 4 supports full hardware acceleration on Windows 7 and Windows Vista via a combination of D2D, DX9 and DX10. This allows us to accelerate everything from Canvas drawing to video rendering. Windows XP users will also enjoy hardware acceleration for many operations because we’re using our new Layers infrastructure along with DX9. And, of course, OSX users have excellent OpenGL support, so we’ve got that covered as well.

**Compartments**

[Compartments](http://andreasgal.wordpress.com/2010/10/13/compartments/), added in Beta 7, is infrastructure that we’ve added to Firefox to improve performance, give us a better base for security and, over the long term, give us better responsiveness because of its positive effects on garbage collection. (Note that there are some parts of Compartments that still have not landed.) If you want to learn about why Compartments are so important, have a look at [Andreas Gal’s great post on the topic](http://andreasgal.wordpress.com/2010/10/13/compartments/). He does a great job of explaining what they are and how they work.

**Improved DOM performance and style resolution**

We’ve made a huge number of improvements to our overall DOM and style resolution performance as well. Although JavaScript gets much of the focus these days, it turns out that in page load and interactive performance, the DOM and style resolution (usually as part of reflowing a document) often affect page performance more than JavaScript. And as such we’ve seen improvement across the board in this area with Firefox 4. In some tests we’re a solid 2x faster than Firefox 3.6.

**JavaScript typed arrays**

If you’re doing processing with JavaScript and you want to process low-level data, Firefox now supports [native typed arrays in JavaScript](https://developer.mozilla.org/en/JavaScript_typed_arrays). This can make a [gigantic difference in how fast items are processed if you’re doing WebGL or image manipulation](http://blog.vlad1.com/2010/07/30/fun-with-fast-javascript/).

In addition, if you’re getting data from an XHR request, you can get that data as a [JavaScript native typed array for fast processing with mozResponseArrayBuffer.](https://developer.mozilla.org/en/using_xmlhttprequest#Receiving_binary_data_using_JavaScript_typed_arrays)

**JavaScript animation scheduling APIs**

We now support events that let you [schedule animations from JavaScript](https://developer.mozilla.org/en/DOM/Animations_using_MozBeforePaint). Doing this means you aren’t wasting CPU and battery by running your animations as fast as possible when the underlying rendering engine isn’t going to draw them anyway. (Gecko now has an internal timer for all drawing and will render at a maximum of 60fps, the edge of human perception. It will also turn this timer down to 1fps for tabs that aren’t in the foreground. Use it.) This is most useful for people building libraries, but you should be aware that there’s a better way to animate in Gecko.

**Retained layers**

As mentioned above, Firefox now has an internal Layers system for improved drawing performance for many types of web pages. Images, fixed backgrounds, inline video, etc. are now rendered to an internal layer and then composited with other parts of a web page in a way that can take advantage of hardware acceleration. This improves the page load time and interactive performance of many web pages.

**Asynchronous plug-in painting**

On Windows and Linux we now paint plug-ins asynchronously. In previous releases when we wanted to paint a web page that included a plug-in, we would have to ask the plug-in for the data to paint. If a plug-in was slow or was hung, it would make the browser feel slow. Now we’re able to get that data asynchronously, which means that the overall responsiveness of the browser should be improved.

**Vastly improved cache**

Firefox 4 has a vastly improved disk cache. This disk cache should result in faster start-up performance and runtime performance. But why mention this here? Our expectation is that site owners should see much higher cache hit rates with Firefox 4 as we dynamically set the cache size based on how much space is free on an end-user’s hard drive.

### WebGL

Firefox 4 now has WebGL enabled by default. Based on the original [3-D Canvas](http://blog.vlad1.com/canvas-3d/) work by Vladimir Vukićević, this is being widely implemented in browsers. The WebGL spec is on the short path to a 1.0 release and we’re very excited to see this be used in the wild.

Want a demo? Try the amazing [Flight of the Navigator](http://vocamus.net/dave/?p=1233) where we combine WebGL with a number of other technologies in Firefox 4 — HTML5 video, the Audio API, all remixed with live data from the web.

### JavaScript

The new JaegerMonkey engine in Firefox 4 isn’t just faster, it’s also got some new tricks as well. Our goal is to bring new tools to developers and that includes evolving the JavaScript language. Here are two examples of where we’ve made other improvements:

**ECMAScript 5**

Firefox 4 Beta 9 contains much of the [new version of the JavaScript language](http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/). Our goal with Firefox 4 is to have industry-leading support for ECMAScript 5, including the new `strict`

mode. You can track our progress on the [ES5 bug.](https://bugzilla.mozilla.org/show_bug.cgi?id=445494)

### Web Console

Firefox 4 will include the [Web Console](https://developer.mozilla.org/en/Using_the_Web_Console). This is a new tool that will let you inspect a web page as it’s running, see network activity, see messages logged with `console.log`

, see warnings for a page’s CSS, and a number of other things.

Note this that is something that we’ll be including with Firefox 4 directly. It’s not an add-on.

(Also Firebug will be ready for the final Firefox 4 release.)

### HTML5

Firefox has always had excellent support for HTML5, even as far back as Firefox 3.5. Firefox 4 builds on that history with a bunch of new HTML5-related features.

**Forms**

We’ve started to implement much of HTML5 forms. We include support for new input types, `datalist`

support, new input attributes like `autofocus`

and `placeholder`

, decoupled forms, form options, validation mechanisms, constraint validation and new CSS selectors to bind them all together. There’s a [great post up on the Hacks site](http://hacks.mozilla.org/2010/11/firefox-4-html5-forms/) covering our HTML5 forms support in Firefox 4. If you want more information, [check it out](http://hacks.mozilla.org/2010/11/firefox-4-html5-forms/).

**Parser**

Firefox 4 includes an HTML5-ready parser. This parser brings with it some [new capabilities, most notably inline SVG](http://hacks.mozilla.org/2010/05/firefox-4-the-html5-parser-inline-svg-speed-and-more/), but also improves performance by running the parsing algorithm on its own processor. It also brings our parser algorithm closer to the standard and lays the foundation for consistent parsing across browsers.

**Support for WebM**

Firefox 4 includes support for [WebM](http://www.webmproject.org/), the new royalty-free format for video on the web. It works on YouTube if you join their [HTML5 beta](http://www.youtube.com/html5). It also works with embedded YouTube videos if you use their new [iframe embedding API](http://apiblog.youtube.com/2010/07/new-way-to-embed-youtube-videos.html). (Join the beta and see an example [at the bottom of this post](http://www.0xdeadbeef.com/weblog/2010/08/24-hours-of-lemons/).)

**Video Buffer API**

We now support the [buffered attribute](http://blog.pearce.org.nz/2010/08/buffered-attribute-landed-for-html5.html) for HTML5 video. This means it’s possible to give users an accurate measure of how much video has been buffered instead of having to guess from the download rate and your current position in the stream.

**Video “preload” support**

We’ve replaced the [“autobuffer” attribute for HTML5 video with the new “preload” attribute](http://hacks.mozilla.org/2010/08/video_preload_attribute/). This attribute gives you much better control over how videos are pre-buffered if they are included on a page rather than the old on/off system that was included with Firefox 3.5.

**History pushState and replaceState**

Firefox 4 now supports the HTML5 [pushState and replaceState history modification calls](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history). These allow you to create or modify the browser navigation history. These are extremely useful for applications that might want to generate history entries using the hash after the URL (useful for HTML-based slides, for example.) Other sites have been using these APIs to hide history information so that site-internal navigation aids aren’t revealed as part of HTTP-referrers.

**Audio sampling and generation API**

Firefox 4 includes the [Firefox Audio Data API](https://wiki.mozilla.org/Audio_Data_API). This API allows you read, modify and write data from audio and video elements. This is now being widely experimented with and people are building some very beautiful things with it.

### DOM

Firefox 4 includes a bunch of new DOM functionality, in addition to the performance improvements I mentioned before.

**Added support for .click() to the File upload control**

You can now [call .click() on a hidden File control](https://developer.mozilla.org/en/using_files_from_web_applications#Using_hidden_file_input_elements_using_the_click%28%29_method) in order to bring up the platform file upload widget. This means you don’t have to expose the (ugly) file upload control; instead you can build your own. If you combine this with the new

[File APIs](https://developer.mozilla.org/en/Using_files_from_web_applications)and

[progress events](https://developer.mozilla.org/En/XMLHttpRequest/Using_XMLHttpRequest#Monitoring_progress)and you’ve got a recipe for a very nice file upload experience.

**Support for .slice in the File API**

We now support the [Blob API and the .slice APIs that come with it](https://developer.mozilla.org/en/DOM/Blob). This is useful for people who want to want to process small parts of an otherwise large File object from JavaScript. You no longer have to load the entire file into memory.

It’s also useful for people who want to reliably upload large files. With some server and JS code you can now split a large file into small sections and upload those chunks, including re-retrying failed sections, or even uploading several sections in parallel.

**Support for File API URLs**

We now support the [ .url attribute for the File API.](http://hacks.mozilla.org/2010/07/firefox-4-formdata-and-the-new-file-url-object/) This lets you take objects that you’ve gotten through the File API and use them for images, video, HTML or other URL-powered objects.

**Touch and multi-touch events**

Firefox 4 supports both [touch and multi-touch events, exposed to the DOM](http://hacks.mozilla.org/2010/08/firefox4-beta3/). Support for this functionality is available on Windows 7 systems.

**Detect click-to-touch**

You can now tell if a mouse or finger generated an event with the [mozInputSource](https://developer.mozilla.org/en/DOM/event.mozInputSource) property. This is useful with the touch and multi-touch events and makes it possible to build apps that treat touch and mouse input differently.

**IndexedDB**

Firefox 4 will include a super-early version of [IndexedDB](http://www.w3.org/TR/IndexedDB/). This emerging standard for local storage is still undergoing change and will be private-prefixed until it’s stable. We have some early [API docs](https://developer.mozilla.org/en/IndexedDB) on IndexedDB, but the spec and implementation we have in Firefox 4 have both changed since the docs were last updated. As we get closer to release time we’ll be updating the docs and talk more about the implementation. Meanwhile, you can read the [IndexedDB primer](https://developer.mozilla.org/en/IndexedDB/IndexedDB_primer) for an overview of using the IndexedDB API.

**FormData**

Firefox 4 includes support for the new [FormData](http://hacks.mozilla.org/2010/07/firefox-4-formdata-and-the-new-file-url-object/) object, which makes it easier to interact with HTML forms. It also enables some new capabilities, like making it easy to upload a file as part of a form accessed via the File API.

**SVG Animation and SMIL**

In Firefox 4 you can now [animate SVG with SMIL.](https://developer.mozilla.org/en/SVG/SVG_animation_with_SMIL)

**SVG as Images and CSS backgrounds**

You can now use SVG as the source of an <img> tag. You can even animate them with SMIL. And you can also use SVGs as backgrounds in CSS.

**Get a Canvas as a File object**

Many people wanted a Canvas accessible as a file object for uploads and other purposes. You can now use the `mozGetAsFile()`

method [on a canvas](https://developer.mozilla.org/en/DOM/HTMLCanvasElement) and it will return an image file.

**Resizable text areas**

If you’ve been using a beta, you’ve noticed that text areas are now resizable by default. You can disable that with the new [ resize](https://developer.mozilla.org/en/CSS/resize) CSS property.

### CSS

Firefox 4 includes a huge pile of new CSS properties and promotions from the private CSS namespace into the final namespace due to the maturation of some of the standards in this space.

**CSS Transitions**

Firefox 4 will include support for [CSS Transitions](https://developer.mozilla.org/en/CSS/CSS_transitions). Since the spec is still early, these are still `-moz`

prefixed extensions.

**calc()**

We now support an early version of `calc`

private-namespaced as `<a href="https://developer.mozilla.org/en/CSS/-moz-calc">-moz-calc</a>`

. This will let you use simple expressions anywhere you would normally want to use a length. This can make the CSS layout of pages much simpler. (No more divs for spacing!)

**-moz-any()**

We now support a new extremely useful CSS extension: [-moz-any()](http://hacks.mozilla.org/2010/05/moz-any-selector-grouping/) selector grouping. This will be very useful in HTML5 contexts. Please read the post for more information.

**-moz-element()**

The `<a href="http://hacks.mozilla.org/2010/08/mozelement/">-moz-element</a>`

is an extension to the `background-image`

property that lets you use any element as the background for another element. This is hugely useful & powerful and we hope that other browsers will adopt it as well.

**-moz-placeholder()**

The `<a href="https://developer.mozilla.org/en/CSS/%3A-moz-placeholder">:-moz-placeholder</a>`

allows you to change the attributes of background text that’s a placeholder in an HTML5 form. This allows you to change the color or other attribute of the text. This can be very useful if you’ve changed the style of the actual text box and you want the background text to match.

**border-radius**

The `border-radius`

attribute is now supported, replacing the old [ -moz-border-radius](https://developer.mozilla.org/en/css/-moz-border-radius) attribute.

**box-shadow**

`<a href="https://developer.mozilla.org/En/CSS/Box-shadow">box-shadow</a>`

has replaced `-moz-box-shadow`

.

**-moz-font-feature-settings**

Firefox 4 will include support for [exposing much more of the capabilities of TrueType fonts](http://hacks.mozilla.org/2010/11/firefox-4-font-feature-support/) with the `<a href="https://developer.mozilla.org/en/CSS/-moz-font-feature-settings">-moz-font-feature-settings</a>`

property. It’s possible to take advantage of all kinds of font capabilities — kerning, ligatures, alternates, real small caps, and stylistic sets, to name just a few.

**Consistent CSS units**

We’ve changed our handling of pixel sizes to match Internet Explorer, Safari and Chrome so that 1 inch always equals 96 pixels. See [Robert’s post for more information](http://weblogs.mozillazine.org/roc/archives/2010/08/css_units_chang.html) on these changes.

**Support for a physical CSS unit**

We’ve introduced a new CSS unit, [ mozmm](http://weblogs.mozillazine.org/roc/archives/2010/08/css_units_chang.html) for the rare instance where you actually want a physical size to be used. Once again, see

[Robert’s post for more information](http://weblogs.mozillazine.org/roc/archives/2010/08/css_units_chang.html)on this new unit.

**device-pixel-ratio**

Firefox now supports the `<a href="https://developer.mozilla.org/En/CSS/Media_queries#-moz-device-pixel-ratio">-moz-device-pixel-ratio</a>`

media query that gives you the number of device pixels per CSS pixel.

**resize**

As mentioned above, we now have a `<a href="https://developer.mozilla.org/en/CSS/resize">resize</a>`

CSS property that lets you disable resizable input text areas.

**-moz-tab-size**

We now support the [ -moz-tab-size](https://developer.mozilla.org/en/CSS/-moz-tab-size) property that lets you specify the width in space characters of how to render a tab character (U+0009) when rendering text.

**-moz-focusring**

The new CSS pseudo-selector, [ -moz-focusring](https://developer.mozilla.org/en/CSS/%3a-moz-focusring) lets you specify the appearance of an element when it’s focused and it would have a focus ring drawn around it. Different operating systems have different conventions for when to draw a focus ring or not and this lets you control the look of form controls while keeping to platform conventions.

**-moz-image-rect**

The new [ -moz-image-rect](https://developer.mozilla.org/en/CSS/-moz-image-rect) lets you use a sub-rectangle of an image as part of a

[or](https://developer.mozilla.org/en/CSS/background)

`background`

[.](https://developer.mozilla.org/en/CSS/background-image)

`background-image`

### Security

Last but not least, Firefox 4 supports a huge number of new security tools, useful for both users and web developers alike. Here’s a quick overview of the new technologies we’re delivering:

**Content Security Policy**

[Content Security Policy (CSP)](https://developer.mozilla.org/en/Security/CSP) is a set of tools that web developers can use to help prevent a couple different classes of attacks. In particular, it offers tools to mitigate cross-site scripting attacks, click-jacking and packet sniffing attacks.

Another important piece of CSP is that when one of the rules is violated, Firefox can send back information about that violation to the web site, making it a useful canary to improve security for other browsers too.

**X-Frame-Options**

Firefox 4 now supports the [X-Frame-Options header](https://developer.mozilla.org/en/The_X-FRAME-OPTIONS_response_header), one defense against clickjacking. This response header is supported by other browsers as well. (This was also delivered as part of a Firefox 3.6 update, but is worth calling out since it’s new since the original 3.6 release.)

**HSTS (ForceTLS)**

Firefox 4 supports the obtusely-named [HTTP Strict Transport Security (HSTS) headers](http://tools.ietf.org/html/draft-hodges-strict-transport-sec-02). You can use these headers to tell the browser that it should never, ever contact a site over unencrypted HTTP.

Firefox users can also use the [STS UI add-on to add and remove sites from the HSTS list](https://addons.mozilla.org/en-US/firefox/addon/246797/), even sites that don’t natively support HSTS.

**CORS Improvements**

We’ve fixed some bugs in our CORS implementation.

**:visited changes**

Firefox 4 includes the changes required to help improve your privacy online by [closing a decade-old hole in CSS rules that let any website query your browsing history](http://hacks.mozilla.org/2010/03/privacy-related-changes-coming-to-css-vistited/). These changes have also been picked up by WebKit-based browsers and we’ve heard rumors that IE 9 might pick up this important change as well.

### That’s a lot of stuff

Yes, it really is! We hope that you like it.

## 109 comments

Alfred KayserJanuary 14th, 2011 at 12:25Ryan GroveJanuary 14th, 2011 at 13:20ShmerlJanuary 14th, 2011 at 13:24BorisJanuary 14th, 2011 at 13:39Arpad BorsosJanuary 15th, 2011 at 02:18DavidJanuary 15th, 2011 at 02:49BorisJanuary 15th, 2011 at 08:44MartinJanuary 15th, 2011 at 04:03BorisJanuary 15th, 2011 at 16:35pdJanuary 15th, 2011 at 04:13oiaohmJanuary 15th, 2011 at 04:30MomijiJanuary 15th, 2011 at 09:12BertJanuary 15th, 2011 at 05:23BorisJanuary 15th, 2011 at 16:28Ernst SjöstrandJanuary 18th, 2011 at 12:30dudeJanuary 14th, 2011 at 14:00TaimarJanuary 14th, 2011 at 14:12NormanJanuary 14th, 2011 at 17:47Anthony RicaudJanuary 15th, 2011 at 06:52jkulakJanuary 14th, 2011 at 14:22RodolfoJanuary 14th, 2011 at 14:51Janet SwisherJanuary 14th, 2011 at 15:47thinsoldierJanuary 14th, 2011 at 15:59BorisJanuary 14th, 2011 at 18:03thinsoldierJanuary 15th, 2011 at 07:57another_samJanuary 14th, 2011 at 15:59BorisJanuary 14th, 2011 at 18:07oiaohmJanuary 15th, 2011 at 04:33BorisJanuary 15th, 2011 at 16:31ShmerlJanuary 17th, 2011 at 09:45helena boydJanuary 14th, 2011 at 16:11IrekJanuary 15th, 2011 at 16:25tagada456January 14th, 2011 at 16:46Pam GriffithJanuary 14th, 2011 at 17:43BorisJanuary 15th, 2011 at 20:35ravenJanuary 15th, 2011 at 01:29BorisJanuary 15th, 2011 at 20:31ravenJanuary 16th, 2011 at 00:50BorisJanuary 16th, 2011 at 09:08pdJanuary 16th, 2011 at 10:38Georg PortenkirchnerJanuary 15th, 2011 at 02:49David BruantJanuary 15th, 2011 at 02:50guybrushJanuary 15th, 2011 at 04:43fjpoblamJanuary 15th, 2011 at 09:00bobzJanuary 15th, 2011 at 09:05Isaac AggreyJanuary 15th, 2011 at 11:05fanenJanuary 15th, 2011 at 09:21wiltjkJanuary 15th, 2011 at 09:54BorisJanuary 16th, 2011 at 19:00Bill FrankJanuary 15th, 2011 at 10:20BorisJanuary 16th, 2011 at 18:18SleepingJanuary 15th, 2011 at 10:39Ken SaundersJanuary 15th, 2011 at 10:57KitsuneJanuary 15th, 2011 at 11:14Hans W.January 17th, 2011 at 04:47Bret TreasureJanuary 15th, 2011 at 12:51LaCJanuary 15th, 2011 at 14:37William DorseyJanuary 15th, 2011 at 16:05joseJanuary 15th, 2011 at 16:48kn33ch41January 15th, 2011 at 19:34Jeff WJanuary 15th, 2011 at 19:43abu abdullaJanuary 15th, 2011 at 20:48Pam GriffithJanuary 15th, 2011 at 21:20BorisJanuary 16th, 2011 at 18:08componentes informaticosJanuary 15th, 2011 at 21:25Marush DenchevJanuary 16th, 2011 at 02:57StuartJanuary 16th, 2011 at 04:03pdJanuary 16th, 2011 at 04:46Henri SivonenJanuary 16th, 2011 at 06:04rahimJanuary 16th, 2011 at 08:41BorisJanuary 17th, 2011 at 08:15namesJanuary 16th, 2011 at 17:01Anthony RicaudJanuary 17th, 2011 at 06:01BorisJanuary 17th, 2011 at 08:14Hans W.January 17th, 2011 at 04:53thinsoldierJanuary 18th, 2011 at 09:44another_samJanuary 18th, 2011 at 10:08PhilJanuary 17th, 2011 at 05:55BorisJanuary 17th, 2011 at 09:39PhilJanuary 17th, 2011 at 10:00BorisJanuary 17th, 2011 at 10:14PhilJanuary 19th, 2011 at 02:56jospoortvlietMarch 24th, 2011 at 10:40Philippe V.January 17th, 2011 at 09:02michaelJanuary 18th, 2011 at 06:00llewtonJanuary 18th, 2011 at 09:15pdJanuary 18th, 2011 at 23:52PhilJanuary 19th, 2011 at 02:51AricJanuary 18th, 2011 at 15:24BorisJanuary 19th, 2011 at 10:05MattJanuary 19th, 2011 at 16:41PhilJanuary 21st, 2011 at 04:34PhilJanuary 21st, 2011 at 04:52MattJanuary 29th, 2011 at 18:39bahramJanuary 20th, 2011 at 12:33Daquan WrightJanuary 20th, 2011 at 22:41ManjurulJanuary 25th, 2011 at 05:51Matt RichardsonJanuary 25th, 2011 at 08:01MaximilianJanuary 26th, 2011 at 13:09MikeJanuary 29th, 2011 at 13:17RFebruary 9th, 2011 at 16:06EUGENE TAGTMEYERFebruary 14th, 2011 at 21:38WissemMarch 3rd, 2011 at 17:31Paul RougetMarch 3rd, 2011 at 18:34SiddharthMarch 3rd, 2011 at 22:41LarsMarch 4th, 2011 at 04:26pip010April 18th, 2011 at 03:37louisremiApril 18th, 2011 at 09:09arbsbDecember 12th, 2012 at 11:18