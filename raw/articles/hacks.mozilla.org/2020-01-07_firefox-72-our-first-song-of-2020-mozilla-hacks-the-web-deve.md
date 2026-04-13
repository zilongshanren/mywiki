---
title: Firefox 72 — our first song of 2020 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/01/firefox-72-our-first-song-of-2020/
author: Chris Mills
published: '2020-01-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

2020 is upon us, folks. We’d like to wish everyone reading this a happy new year, wherever you are. As you take your first steps of the new year, figuring out what your next move is, you may find it comforting to know that there’s a new Firefox release to try out!

Version 72 to be exact.

One of the highlights that we are most proud of is that user gestures are now required for a number of permission-reliant methods, such as `Notification.requestPermission()`

. User research commonly brings up *permission prompt spam* as a top user annoyance, so we decided to do something about it. This change reduces permission spam and strengthens users’ agency over their online experience.

This release brings several other new features, including DevTool improvements such as Watchpoints, WebSockets inspector improvements, and resource download times; support for CSS features like shadow parts, motion path, and transform properties; and JS/API features such as event-based form participation and the nullish coalescing operator.

Read on for more highlights. To find the full list of additions, check out the following MDN articles:

Now that we’ve moved to a 4-week browser release cycle, you’ll see fewer new features in each individual release, but features will be added to Firefox more often. This gives you faster access to new functionality and bug fixes. You can read our full rationale for the change in [Moving Firefox to a faster 4-week release cycle](https://hacks.mozilla.org/2019/09/moving-firefox-to-a-faster-4-week-release-cycle/).

## DevTools improvements

First, we’ll look at Firefox 72 DevTools improvements in more detail.

### Pause on variable access or change

Watchpoints are a new type of breakpoint that can pause execution when an object property gets read or set. You can set watchpoints from the context menu of any object listed in the *Scopes* panel.

This feature is described in more detail in the [Use watchpoints](https://developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Use_watchpoints) article on MDN, and [Debugging Variables With Watchpoints in Firefox 72](https://hacks.mozilla.org/2019/12/debugging-variables-with-watchpoints-in-firefox-72/) on Hacks.

### Firefox DevEdition only: Asynchronous Stacks in Console

Console stacks capture the full async execution flow for `<a href="https://developer.mozilla.org/en-US/docs/Web/API/console/trace">console.trace()</a>`

and `<a href="https://developer.mozilla.org/en-US/docs/Web/API/console/error">console.error()</a>`

. This lets you understand scheduling of timers, events, promises, generators, etc. over time, which would otherwise be invisible.

They are only enabled in [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) for now. We are working to make this feature available to all users after improving performance. Async stacks will also be rolled out to more types of logs, and of course the Debugger.

### SignalR formatting & download/upload size for WebSockets

Before shipping the new [WebSocket inspector in 71](https://hacks.mozilla.org/2019/10/firefoxs-new-websocket-inspector/) we had it available in [Firefox DevEdition](https://www.mozilla.org/en-US/firefox/developer/) and asked for your input. We didn’t just get a lot of fantastic ideas, some of you even stepped up to contribute code. Thanks a lot for that, and [keep it coming](https://codetribute.mozilla.org/projects/devtools?tag%3Dgood-first-bug)!

Messages sent in [ASP.NET’s Core SignalR](https://dotnet.microsoft.com/apps/aspnet/signalr) format are now parsed to show nicely-formatted metadata. The [bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1589068) was filed thanks to [feedback](https://twitter.com/davidfowl/status/1184364405766545408) from the ASP.NET community and then picked up by contributor [Bryan Kok](https://github.com/Transfusion).

Similarly, the community [asked](https://discourse.mozilla.org/t/feedback-wanted-websocket-inspector-in-devedition-70/46859/10) to have the total transfer size for download and upload available. This is now a reality thanks to [contributor Hayden Huang](https://bugzilla.mozilla.org/show_bug.cgi?id=1593831#c6), who took up [the bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1593831) as their first Firefox patch.

### Start and end times for Network resources

The [Timings](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor/request_details#Timings) tab of the [Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) now displays timings for each downloaded resource, making dependency analysis a lot easier:

- Queued — When the resource was queued for download.
- Started — When the resource started downloading.
- Downloaded — When the the resource finished downloading.

### And as always, faster and more reliable

Here are just a few highlights from our continued performance and quality investments:

- In the
[Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector), editing CSS is no longer blocked by[CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)rules. - The
[Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector)‘s badge for[Custom Elements](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements)now correctly opens the original script for source maps. - The
[Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector)now correctly preserves the selected element for`<a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe"><iframes></a>`

when reloading. - The
[Debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger)now loads faster when many tabs are open, by prioritizing visible tabs first.

## CSS additions

Now let’s move on to the most interesting new CSS features in Firefox 72.

### Shadow Parts

One problem with styling elements contained inside a [Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM) is that you can’t just style them from CSS applied to the main document. To make this possible, we’ve implemented Shadow Parts, which allow shadow hosts to selectively expose chosen elements from their shadow tree to the outside page for styling purposes.

Shadow parts require two new features. The [ part attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/part) exposes an element inside a shadow tree to the outside page:

```
<custom-element>
<p part="example">A paragraph</p>
</custom-element>
```


The [ ::part() pseudo-element](https://developer.mozilla.org/en-US/docs/Web/CSS/::part) is then used to select elements with a specific

`part`

attribute value:```
custom-element::part(example) {
border: solid 1px black;
border-radius: 5px;
padding: 5px;
}
```


### CSS Motion Path

[Motion Path](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Motion_Path) is an interesting new spec for all you animators out there. The idea here is that you can define a path shape and then animate a DOM node along that path. The spec proposes an alternative to having to animate `transform: translate()`

, position properties like `top`

, `right`

, and so on, or use some other property that often isn’t ideal and could result in very complex sets of keyframes.

With motion path, you define the shape of the path using [ offset-path](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-path):

`offset-path: path('M20,20 C20,100 200,0 200,100');`


Define an animation to animate the element between different values of the [ offset-distance](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-distance) property, which defines how far along the defined path you want the element to appear:

```
@keyframes move {
0% {
offset-distance: 0%;
}
100% {
offset-distance: 100%;
}
}
```


Then, animate the element using those keyframes:

`animation: move 3000ms infinite alternate ease-in-out;`


This is a simple example. There are additional properties available, such as [ offset-rotate](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-rotate) and

[. With](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-anchor)

`offset-anchor`

[, you can specify how much you want to rotate the element being animated. Use](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-rotate)

`offset-rotate`

[to specify which background-position of the animated element is anchored to the path.](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-anchor)

`offset-anchor`

### Individual transform properties

In this release the following individual transform properties are enabled by default: [ scale](https://developer.mozilla.org/en-US/docs/Web/CSS/scale),

[, and](https://developer.mozilla.org/en-US/docs/Web/CSS/rotate)

`rotate`

[. These can be used to set transforms on an element, like so:](https://developer.mozilla.org/en-US/docs/Web/CSS/translate)

`translate`

```
scale: 2;
rotate: 90deg;
translate: 100px 200px;
```


These can be used in place of:

```
transform: scale(2);
transform: rotate(90deg);
transform: translate(100px 200px);
```


Or even:

`transform: scale(2) rotate(90deg) translate(100px 200px);`


These properties are easier to write than the equivalent individual transforms, map better to typical user interface usage, and save you having to remember the exact order of multiple transform functions specified in the transform property.

## JavaScript and WebAPI updates

If JavaScript is more your thing, this is the section for you. 72 has the following updates.

### User gestures required for a number of permission-reliant methods

Notification permission prompts always show up in research as a top web annoyance, so we decided to do something about it. To improve security and avoid unwanted and annoying permission prompts, a number of methods have been changed so that they can only be called in response to a user gesture, such as a click event. These are [ Notification.requestPermission()](https://developer.mozilla.org/en-US/docs/Web/API/Notification/requestPermission),

[, and](https://developer.mozilla.org/en-US/docs/Web/API/PushManager/subscribe)

`PushManager.subscribe()`

[.](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia)

`MediaDevices.getDisplayMedia()`

By requiring a user gesture before the permission prompts are shown, Firefox significantly reduces permission spam, thereby strengthening users’ agency over their online experience.

So, for example, prompting for notification permission on initial page load is no longer possible. You now need something like this:

```
btn.addEventListener('click', function() {
Notification.requestPermission();
// Handle other notification permission stuff in here
});
```


For more detail on associated coding best practices for Notification permissions, read [Using the Notifications API](https://wiki.developer.mozilla.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications_API).

### Nullish coalescing operator

The [nullish coalescing operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator), `??`

, returns its right-hand side operand when its left-hand side operand is null or undefined. Otherwise, it returns its left-hand side operand.

This is a useful timesaver in a number of ways, and it is also useful when you only consider null and undefined to be unwanted values, and not other falsy values like `0`

and `' '`

.

For example, if you want to check whether a value has been set and return a default value if not, you might do something like this:

```
let value;
if(!value) {
value = 'default';
}
```


That’s a bit long, so you might instead use this common pattern:

```
let value;
let value = value || 'default';
```


This also works OK, but will return unexpected results if you want to accept values of `0`

or `' '`

.

With `??`

, you can do this instead, which is concise and solves the problem described above:

```
let value;
value = value ?? 'default';
```


### Event-based form participation

Event-based form participation is now enabled by default. This involves [using the new FormData event](https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects#Using_a_formdata_event), which fires when the form is submitted, but can also be triggered by the invocation of a [ FormData()](https://developer.mozilla.org/en-US/docs/Web/API/FormData/FormData) constructor. This allows a

[object to be quickly obtained in response to a formdata event firing, rather than needing to create it yourself — useful when you want to submit a form via XHR, for example.](https://developer.mozilla.org/en-US/docs/Web/API/FormData)

`FormData`

Here’s a look at this feature in action:

```
formElem.addEventListener('submit', (e) => {
// on form submission, prevent default
e.preventDefault();
// construct a FormData object, which fires the formdata event
new FormData(formElem);
});
formElem.addEventListener('formdata', (e) => {
console.log('formdata fired');
// Get the form data from the event object
let data = e.formData;
// submit the data via XHR
let request = new XMLHttpRequest();
request.open("POST", "/formHandler");
request.send(data);
});
```


## Picture-in-picture for video now available on macOS & Linux

In the [previous release post](https://hacks.mozilla.org/2019/12/firefox-71-a-year-end-arrival/), we announced that Picture-in-picture had been enabled in Firefox 71, albeit this was for Windows only. However,today we have the goods that this very popular feature is now available on macOS and Linux too!

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 14 comments

paolaJanuary 7th, 2020 at 14:19ChrisJanuary 8th, 2020 at 15:47Chris MillsJanuary 8th, 2020 at 23:53ChrisJanuary 12th, 2020 at 13:16BillJanuary 13th, 2020 at 15:30Chris MillsJanuary 14th, 2020 at 00:21ShawnJanuary 15th, 2020 at 08:11Shubham ShahJanuary 30th, 2020 at 04:30Alexandre LeducJanuary 8th, 2020 at 19:41RomanJanuary 9th, 2020 at 06:22ScottJanuary 9th, 2020 at 13:52Ana CostaJanuary 14th, 2020 at 05:00Ian DickinsonJanuary 20th, 2020 at 05:48Chris MillsJanuary 20th, 2020 at 05:53