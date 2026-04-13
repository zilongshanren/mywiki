---
title: 'Firefox 71: A year-end arrival – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/12/firefox-71-a-year-end-arrival/
author: Chris Mills
published: '2019-12-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Another release is upon us: please welcome Firefox 71 to the stage! This time around, we have a plethora of new developer tools features. These include the web socket message inspector, console multi-line editor mode, log on events, and network panel full text search!

And as if that wasn’t good enough, there are important new web platform features available, like CSS subgrid, column-span, Promise.allSettled, and the Media Session API.

Read on for more details of the highlights, and find the full list of additions with the links below:

## Developer tools

Let’s start with our new developer tool features! Many of these were first made available in [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/?utm_source=hacks&utm_medium=release_71), and then improved based on feedback from early adopters. We’d like to thank you all for your help!

### Continued speed and reliability improvements

Improvements in Firefox 71 continue our promise to provide a [rock-solid and fast DevTools experience.](https://hacks.mozilla.org/2019/05/faster-smarter-javascript-debugging-in-firefox/)

We know it’s important that DevTools load quickly. We have automation in place to help ensure we keep driving this time down. In 71 we got some help from the JavaScript team, when their improvements to caching scripts for startup not only made Firefox start faster, but DevTools too. One Console test got an astonishing 40% improvement while times across every panel were boosted by 8-15%!

Interaction with pretty-printed code has gotten a lot of attention. Over past releases we’ve already improved breakpoint handling and pausing. In 71, links to scripts (like from the [event handler tooltip](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_event_listeners) in the Inspector or the stack traces in the Console) reliably get you to the expected line, and [debugging sources loaded through eval()](https://developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Debug_eval_sources) now also works as expected.

### WebSocket Message Inspector

The [Network panel](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) has a new *Messages* tab. You can observe all messages sent and received through a WebSocket connection:

Sent frames have a green up-arrow icon, while received frames have a red down-arrow icon. You can click on an individual frame to view its formatted data.

Find out more about WebSockets and how to use the tool in this post about [Firefox’s New WebSocket Inspector](https://hacks.mozilla.org/2019/10/firefoxs-new-websocket-inspector/). Thanks a lot to [Heng Yeow Tan](https://github.com/tanhengyeow), who worked on this feature as part of his [Google Summer of Code (GSoC) internship](https://wiki.mozilla.org/SummerOfCode).

### Network full-text search

Sometimes you need to find a CSS file that defines a color, or work out which file generates a button label on a page. Full-text search makes this possible by letting you search through all resources in the [Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor). Similar to other DevTools, you can open the new panel by clicking the new “Search” icon in the toolbar or using the shortcut (Windows: *Ctrl + Shift + F*, Mac: *Cmd + Shift + F*). The full-text search will highlight matches in request/response bodies, headers, and cookies.

Tip: You can use the Network panel’s existing URL and type filters to limit which requests are being matched in search.

Thanks a lot to [lloan Alas](https://www.lloan.dev/), who worked on this feature as part of his [Outreachy internship](https://wiki.mozilla.org/Outreachy).

### Network request blocking

Simulating [blocked requests](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor/request_list#Blocking_specific_URLs) lets you test how a page loads and functions without specific files, like CSS or JavaScript. The panel is right next to the new full-text search.

You can toggle request blocking as a whole or enter individual patterns to experiment with. To make entering lists easier you can paste in multiple lines of patterns, which will be split into individual rules.

Note how blocked requests are shown in red, with a red “no entry sign” icon next to them.

### Console multi-line editor mode

Another great developer tools feature in Firefox 71 is the new multi-line console. It combines the benefits of IDEs to authoring code with the workflow of repeatedly executing code in the context of the page.

If you open the regular console, you’ll see a new icon at the end of the prompt row.

Clicking this will switch the console to multi-line mode:

Here you can enter multiple lines of code, pressing enter after each one, and then run the code using *Ctrl + Enter*. You can also move between statements using the next and previous arrows. The editor includes regular IDE features you’d expect, such as open/close bracket pair highlighting and automatic indentation.

We are starting with a small, simple feature set for now. We will add more based on the feedback we are already collecting.

### Inline variable preview in Debugger

The [JavaScript Debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger) now provides inline variable previewing, which is a useful timesaver when stepping through your code. Previously you’d have to scroll through the scope panel to find variable values. Or, you could hover over a variable in the source pane. Now when execution pauses, you can view relevant variable and property values directly in the source.

Using our babel-powered source mapping, preview also works for variables that have been renamed or minified by build steps. Make sure to enable this power-feature by checking *Map* in the Scopes pane.

If you prefer less output you can toggle preview off in the new context menu option in the source pane.

Thanks a lot to [Dhyey Thakore](http://www.dhyeythakore.net/), who worked on this feature as part of his GSoC internship.

### Log on Event Listeners

Finally, we’d like to talk a bit about updates to [event listener breakpoints](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Set_event_listener_breakpoints) in 71. There are a couple of nice improvements available.

Log on events lets you explore which event handlers are being fired in which order without the need for pausing and stepping. This is inspired by Firebug’s [Log DOM Event functionality](http://www.softwareishard.com/blog/firebug/firebug-tip-log-dom-events/) but with more control over which events are monitored thanks to its tie in with Event Breakpoints.

So if we choose to log keyboard events, for example, the code no longer pauses as each event is fired:

Instead, we can then switch to the console, and whenever we press a key we are given a log of where related events were fired.

One issue here is that the console is showing that the [ keypress event](https://developer.mozilla.org/en-US/docs/Web/API/Document/keydown_event) is being fired somewhere inside jQuery. Instead, it’d be far more useful if we showed where in our own app code is calling the jQuery that fired the event. This can be done by finding jquery.js in the Sources panel, and choosing the

*Blackbox source*option from its context menu.

Now the logs will show where in your app jQuery was called, rather than where in jQuery the event was fired:

There is also a new *Filter by event type…* text input. When you click in this input and type a search term, the list of event listener types will filter by that term, allowing you to find the events you want to break on more easily.

## CSS

New in CSS in 71 we have subgrid, multicol, `clip-path: path`

, and aspect ratio mapping.

### Subgrid

A feature that has been enabled in 71 after being supported behind a pref for a while, the `subgrid`

value of [ grid-template-columns](https://wiki.developer.mozilla.org/en-US/docs/Web/CSS/grid-template-columns) and

[allows you to create a nested grid inside a grid item that will use the main grid’s tracks. This means that grid items inside the subgrid will line up with the parent’s grid tracks, making various layout techniques much easier.](https://wiki.developer.mozilla.org/en-US/docs/Web/CSS/grid-template-rows)

`grid-template-rows`

```
.grid {
display: grid;
grid-template-columns: repeat(9, 1fr);
grid-template-rows: repeat(4, minmax(100px, auto));
}
.item {
display: grid;
grid-column: 2 / 7;
grid-row: 2 / 4;
grid-template-columns: subgrid;
grid-template-rows: subgrid;
}
.subitem {
grid-column: 3 / 6;
grid-row: 1 / 3;
}
```


We’ve also updated the developer tools’ [Grid Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_grid_layouts) to support subgrid! Specifically, we have:

- allowed highlighting of multiple grids simultaneously.
- added a “subgrid” badge to the
[HTML pane](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/UI_Tour#HTML_pane)that appears next to elements which have been designated as a subgrid, in the same way that the “grid” and “flex” badges already work. - made it so that when a subgrid is highlighted, the parent is also subtly highlighted.

See the [MDN Subgrid page](https://wiki.developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Subgrid) for more details.

### Multicol — column-span

[CSS multicol](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Columns) support has moved forward in a big way with the inclusion of the [ column-span](https://developer.mozilla.org/en-US/docs/Web/CSS/column-span) property in Firefox 71. This allows you to make an element span across all the columns in a multicol container (generated using

[or](https://developer.mozilla.org/en-US/docs/Web/CSS/column-width)

`column-width`

[).](https://developer.mozilla.org/en-US/docs/Web/CSS/column-count)

`column-count`

```
article {
columns: 3;
}
h2 {
column-span: all;
}
```


You can find a number of useful details about `column-span`

in the article [Spanning and balancing columns](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Columns/Spanning_Columns).

## Clip-path: path()

The `path()`

value of the [ clip-path property](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path) is now enabled by default — this allows you to create a custom mask shape using a

`path()`

function, as opposed to a predefined shape like a circle or ellipse.```
#clipped {
clip-path: path('M 0 200 L 0,110 A 110,90 0,0,1 240,100 L 200 340 z');
}
```


### Aspect ratio mapping

Finally, the `height`

and `width`

HTML attributes on the [ <img> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img) are now mapped to an internal

[.](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio)

`aspect-ratio`

propertyThis allows the browser to calculate the image’s aspect ratio early on and correct its display size before it has loaded if CSS has been applied that causes problems with the display size.

Read [Mapping the width and height attributes of media container elements to their aspect-ratio](https://wiki.developer.mozilla.org/en-US/docs/Web/Media/images/aspect_ratio_mapping) for the full story.

## JavaScript and Web APIs

We’ve had a few minor JavaScript changes in this release as well: `Promise.allSettled()`

, the Media Session API, and WebGL multiview.

## Promise.allSettled()

The most significant change comes with the support of the [ Promise.allSettled() method](https://wiki.developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled), which takes an array of promise objects as a parameter just like

[.](https://wiki.developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)

`Promise.all()`

However, whereas `Promise.all()`

will fulfill only when all the promises passed to it have been fulfilled, `Promise.allSettled()`

will fulfill when all the promises passed to it have been resolved (fulfilled *or* rejected).

```
const promise1 = Promise.resolve(3);
const promise2 = new Promise((resolve, reject) => setTimeout(reject, 100, 'foo'));
const promises = [promise1, promise2];
Promise.allSettled(promises).
then((results) => results.forEach((result) => console.log(result.status)));
// expected output:
// "fulfilled"
// "rejected"
```


### Media Session API

Over in Web API land, the main new addition is partial support for the [Media Session API](https://developer.mozilla.org/en-US/docs/Web/API/Media_Session_API). This API provides a standard mechanism for your content to share information about the state of media playing with the underlying operating system. It includes metadata such as artist, album, track name, or album artwork, for example.

```
if ('mediaSession' in navigator) {
navigator.mediaSession.metadata = new MediaMetadata({
title: 'Unforgettable',
artist: 'Nat King Cole',
album: 'The Ultimate Collection (Remastered)',
artwork: [
{ src: 'https://dummyimage.com/96x96', sizes: '96x96', type: 'image/png' },
{ src: 'https://dummyimage.com/128x128', sizes: '128x128', type: 'image/png' },
{ src: 'https://dummyimage.com/192x192', sizes: '192x192', type: 'image/png' },
{ src: 'https://dummyimage.com/256x256', sizes: '256x256', type: 'image/png' },
{ src: 'https://dummyimage.com/384x384', sizes: '384x384', type: 'image/png' },
{ src: 'https://dummyimage.com/512x512', sizes: '512x512', type: 'image/png' },
]
});
navigator.mediaSession.setActionHandler('play', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('pause', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('seekbackward', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('seekforward', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('previoustrack', function() { /* Code excerpted. */ });
navigator.mediaSession.setActionHandler('nexttrack', function() { /* Code excerpted. */ });
}
```


The aim of this API is to allow users to know what’s playing, and to control it, without opening the specific page that launched it.

## WebGL multiview

71 also sees the [ OVR_multiview2 WebGL extension](https://developer.mozilla.org/en-US/docs/Web/API/OVR_multiview2) exposed by default. This is an exciting new addition to the web platform that allows WebGL code to draw on multiple targets with a single draw call, improving performance in the process.

Multiview is especially exciting for WebXR code, in which case you always have to draw everything twice! Read [Multiview on WebXR](https://blog.mozvr.com/multiview-on-webxr/) for more information.

## User features

You can read about the most interesting user features added to Firefox 71 in the main [Firefox 71 Release Notes](https://www.mozilla.org/en-US/firefox/71.0/releasenotes/).

We would however like to highlight Picture-in-picture (PIP). If you start playing a video on a web page, but then want to check out other content, you can activate PIP and keep the video playing in a small overlay while you continue to navigate the rest of the page (or other pages).

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 14 comments

Brian HauerDecember 3rd, 2019 at 10:42Chris MillsDecember 4th, 2019 at 00:57GeraldDecember 3rd, 2019 at 16:19Chris MillsDecember 4th, 2019 at 00:57GeraldDecember 4th, 2019 at 11:47AnonymousDecember 4th, 2019 at 02:33Chris MillsDecember 4th, 2019 at 02:34RobertDecember 5th, 2019 at 10:25Patrick BreitenbachDecember 5th, 2019 at 10:55LuizDecember 6th, 2019 at 06:10Adam BogartDecember 8th, 2019 at 07:26Chris MillsDecember 8th, 2019 at 23:34Christopher SpencerDecember 17th, 2019 at 03:15Chris MillsDecember 17th, 2019 at 03:38