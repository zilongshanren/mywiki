---
title: Using window.matchMedia to do media queries in JavaScript – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2012/06/using-window-matchmedia-to-do-media-queries-in-javascript/
author: Robert Nyman
published: '2012-06-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For people building web sites, [Responsive Web Design](http://en.wikipedia.org/wiki/Responsive_Web_Design) has become a natural approach to making sure the content is available for as many users as possible. This is usually attended to via [CSS media queries](https://developer.mozilla.org/en/CSS/Media_queries). However, there is a JavaScript alternative as well.

## Introducing window.matchMedia

The way to approach media queries in JavaScript is through [window.matchMedia](https://developer.mozilla.org/en/DOM/window.matchMedia). Basically, you just use the same approach as with CSS, but with a JavaScript call:

```
var widthQuery = window.matchMedia("(min-width: 600px)");
```

This query returns a [MediaQueryList](https://developer.mozilla.org/en/DOM/MediaQueryList) object, on which you can do a few things:

- matches
- Boolean whether the query matched or not.
- media
- Serialized media query list.
- addListener
- Adding event listener to a media query. Much preferred over polling values or similar.
- removeListener
- Removing event listener from a media query.

Therefore, the easy way to determine if a media query matched is using the `matches`

property:

```
var widthMatch = window.matchMedia("(min-height: 500px)").matches;
```

Adding listeners is very easy:

```
function getOrientationValue (mediaQueryList) {
console.log(mediaQueryList.matches);
}
portraitOrientationCheck = window.matchMedia("(orientation: portrait)");
portraitOrientationCheck.addListener(getOrientationValue);
```

## Demo and code

I’ve put together a [window.matchMedia demo](http://robnyman.github.com/matchmedia/) where you can see some queries in action. Try resizing the window and see the values change.

The complete JavaScript code for that demo, which is of course [available on GitHub](https://github.com/robnyman/robnyman.github.com/tree/master/matchmedia), is as follows:



```
(function () {
var matchMediaSupported = document.querySelector("#matchmedia-supported"),
width600 = document.querySelector("#width-600"),
height500 = document.querySelector("#height-500"),
portraitOrientation = document.querySelector("#portrait-orientation"),
width600Check,
height500Check,
portraitOrientationCheck;
if (window.matchMedia) {
matchMediaSupported.innerHTML = "supported";
// Establishing media check
width600Check = window.matchMedia("(min-width: 600px)"),
height500Check = window.matchMedia("(min-height: 500px)"),
portraitOrientationCheck = window.matchMedia("(orientation: portrait)");
// Add listeners for detecting changes
width600Check.addListener(setWidthValue);
height500Check.addListener(setHeightValue);
portraitOrientationCheck.addListener(setOrientationValue);
}
function setWidthValue (mediaQueryList) {
width600.innerHTML = mediaQueryList.media;
}
function setHeightValue (mediaQueryList) {
height500.innerHTML = mediaQueryList.matches;
}
function setOrientationValue (mediaQueryList) {
portraitOrientation.innerHTML = mediaQueryList.matches;
}
// Setting initial values at load
function setValues () {
width600.innerHTML = width600Check.matches;
height500.innerHTML = height500Check.matches;
portraitOrientation.innerHTML = portraitOrientationCheck.matches;
}
window.addEventListener("DOMContentLoaded", setValues, false);
})();
```

## Web browser support

At this time, window.matchMedia has been implemented in:

- Firefox 6+
- Google Chrome 9+
- Safari 5.1+. Note: doesn’t support
`addListener`

. - Firefox mobile
- Google Chrome beta on Android. Note: doesn’t support
`addListener`

. - Safari 5 on iOS. Note: doesn’t support
`addListener`

. - Android stock browser. Note: doesn’t support
`addListener`

.

It is also planned to be in Internet Explorer 10.

For older/unsupported web browsers, you can try the [matchMedia() polyfill](https://github.com/paulirish/matchMedia.js/), although it doesn’t support `addListener`

.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 15 comments

Moldován EduárdJune 5th, 2012 at 06:34Robert NymanJune 6th, 2012 at 23:06d7keJune 5th, 2012 at 13:45Robert NymanJune 6th, 2012 at 23:06John A. Bilicki IIIJune 7th, 2012 at 06:30Robert NymanJune 7th, 2012 at 10:44John A. Bilicki IIIJune 7th, 2012 at 11:30Robert NymanJune 7th, 2012 at 11:52John A. Bilicki IIIJune 7th, 2012 at 12:08Robert NymanJune 8th, 2012 at 02:02rdeckJuly 17th, 2012 at 03:15Robert NymanJuly 31st, 2012 at 08:36AlonNovember 8th, 2012 at 02:38MatFebruary 2nd, 2013 at 12:39Robert Nyman [Editor]February 4th, 2013 at 03:02