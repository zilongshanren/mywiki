---
title: Hopping on Firefox 91 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/08/hopping-on-firefox-91/
author: Ruth John
published: '2021-08-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Hopping on Firefox 91**

August is already here, which means so is Firefox 91! This release has a Scottish locale added and, if the ‘increased contrast’ setting is checked, auto enables High Contrast mode on macOS.

Private browsing windows have an HTTPS-first policy and will automatically attempt to make all connections to websites secure. Connections will fall back to HTTP if the website does not support HTTPS.

For developers Firefox 91 supports the [Visual Viewport API](https://developer.mozilla.org/en-US/docs/Web/API/Visual_Viewport_API) and adds some more additions to the [Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) object.

This blog post provides merely a set of highlights; for all the details, check out the following:

**Visual Viewport API**

Implemented back in Firefox 63, the [Visual Viewport API](https://developer.mozilla.org/en-US/docs/Web/API/Visual_Viewport_API) was behind the pref `dom.visualviewport.enabled`

in the desktop release. It is now no longer behind that pref and enabled by default, meaning the API is now supported in all major browsers.

There are two viewports on the mobile web, the layout viewport and the visual viewport. The layout viewport covers all the elements on a page and the visual viewport represents what is actually visible on screen. If a keyboard appears on screen, the visual viewport dimensions will shrink, but the layout viewport will remain the same.

This API gives you information about the size, offset and scale of the visual viewport and allows you to listen for resize and scroll events. You access it via the [visualViewport](https://developer.mozilla.org/en-US/docs/Web/API/Window/visualViewport) property of the [window](https://developer.mozilla.org/en-US/docs/Web/API/Window) interface.

In this simple example the `resize`

event is listened for and when a user zooms in, hides an element in the layout, so as not to clutter the interface.

```
const elToHide = document.getElementById('to-hide');
var viewport = window.visualViewport;
function resizeHandler() {
if (viewport.scale > 1.3)
elToHide.style.display = "none";
else
elToHide.style.display = "block";
}
window.visualViewport.addEventListener('resize', resizeHandler);
```


**New formats for Intl.DateTimeFormat**

A couple of updates to the [Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) object include new [timeZoneName](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat) options for formatting how a timezone is displayed. These include the localized GMT formats `shortOffset`

and `longOffset`

, and generic non-location formats `shortGeneric`

and `longGeneric`

. The below code shows all the different options for the `timeZoneName`

and their format.

```
var date = Date.UTC(2021, 11, 17, 3, 0, 42);
const timezoneNames = ['short', 'long', 'shortOffset', 'longOffset', 'shortGeneric', 'longGeneric']
for (const zoneName of timezoneNames) {
// Do something with currentValue
var formatter = new Intl.DateTimeFormat('en-US', {
timeZone: 'America/Los_Angeles',
timeZoneName: zoneName,
});
console.log(zoneName + ": " + formatter.format(date) );
}
// expected output:
// > "short: 12/16/2021, PST"
// > "long: 12/16/2021, Pacific Standard Time"
// > "shortOffset: 12/16/2021, GMT-8"
// > "longOffset: 12/16/2021, GMT-08:00"
// > "shortGeneric: 12/16/2021, PT"
// > "longGeneric: 12/16/2021, Pacific Time"
```


You can now format date ranges as well with the new [formatRange()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/formatRange) and [formatRangeToParts()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/formatRangeToParts) methods. The former returns a localized and formatted string for the range between two [Date objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date):

```
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
const startDate = new Date(Date.UTC(2007, 0, 10, 10, 0, 0));
const endDate = new Date(Date.UTC(2008, 0, 10, 11, 0, 0));
const dateTimeFormat = new Intl.DateTimeFormat('en', options1);
console.log(dateTimeFormat.formatRange(startDate, endDate));
// expected output: Wednesday, January 10, 2007 – Thursday, January 10, 2008
```


And the latter returns an array containing the locale-specific parts of a date range:

```
const startDate = new Date(Date.UTC(2007, 0, 10, 10, 0, 0)); // > 'Wed, 10 Jan 2007 10:00:00 GMT'
const endDate = new Date(Date.UTC(2007, 0, 10, 11, 0, 0)); // > 'Wed, 10 Jan 2007 11:00:00 GMT'
const dateTimeFormat = new Intl.DateTimeFormat('en', {
hour: 'numeric',
minute: 'numeric'
});
const parts = dateTimeFormat.formatRangeToParts(startDate, endDate);
for (const part of parts) {
console.log(part);
}
// expected output (in GMT timezone):
// Object { type: "hour", value: "2", source: "startRange" }
// Object { type: "literal", value: ":", source: "startRange" }
// Object { type: "minute", value: "00", source: "startRange" }
// Object { type: "literal", value: " – ", source: "shared" }
// Object { type: "hour", value: "3", source: "endRange" }
// Object { type: "literal", value: ":", source: "endRange" }
// Object { type: "minute", value: "00", source: "endRange" }
// Object { type: "literal", value: " ", source: "shared" }
// Object { type: "dayPeriod", value: "AM", source: "shared" }
```


**Securing the Gamepad API**

There have been a few updates to the [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API) to fall in line with the spec. It is now only available in secure contexts (HTTPS) and is protected by [Feature Policy: gamepad](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy/gamepad). If access to gamepads is *disallowed,* calls to [Navigator.getGamepads()](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getGamepads) will throw an error and the `gamepadconnected`

and `gamepaddisconnected`

events will not fire.


## About Ruth John

Ruth John works as a Technical Writer at Mozilla. A recent addition to the MDN team, she's a big fan of web technologies, and not only enjoys writing about them, but building demos with them as well.

## One comment

LukeAugust 26th, 2021 at 04:09