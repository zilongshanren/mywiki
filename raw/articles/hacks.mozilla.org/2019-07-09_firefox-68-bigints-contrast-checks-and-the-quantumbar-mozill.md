---
title: 'Firefox 68: BigInts, Contrast Checks, and the QuantumBar – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2019/07/firefox-68-bigints-contrast-checks-and-the-quantumbar/
author: Dan Callahan
published: '2019-07-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 68 is available today, featuring support for big integers, whole-page contrast checks, and a completely new implementation of a core Firefox feature: the URL bar.

These are just the highlights. For complete information, see:

## BigInts for JavaScript

Firefox 68 now supports JavaScript’s new `BigInt`

numeric type.

Since its introduction, JavaScript has only had a single numeric type: [ Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number). By definition, Numbers in JavaScript are

*floating point*numbers, which means they can represent both integers (like

`22`

or `451`

) and decimal fractions (like `6.28`

or `<a href="https://0.30000000000000004.com/" rel="nofollow">0.30000000000000004</a>`

). However, this flexibility comes at a cost: 64-bit floats cannot reliably represent integers larger than `2 ** 53`

.```
» 2 ** 53
9007199254740992
» (2 ** 53) + 1
9007199254740992 // <- Shouldn't that end in 3?
» (2 ** 53) + 2
9007199254740994
```

This limitation makes it difficult to work with very large numbers. For example, it’s why [Twitter’s JSON API](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json.html) returns Tweet IDs as strings instead of literal numbers.

[BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) makes it possible to represent *arbitrarily large* integers.

```
» 2n ** 53n // <-- the "n" means BigInt
9007199254740992n
» (2n ** 53n) + 1n
9007199254740993n // <- It ends in 3!
» (2n ** 53n) + 2n
9007199254740994n
```

JavaScript does not automatically convert between BigInts and Numbers, so you can’t mix and match them in the same expression, nor can you serialize them to JSON.

```
» 1n + 2
TypeError: can't convert BigInt to number
» JSON.stringify(2n)
TypeError: BigInt value can't be serialized in JSON
```

You can, however, losslessly convert BigInt values to and from strings:

```
» BigInt("994633657141813248")
994633657141813248n
» String(994633657141813248n)
"994633657141813248" // <-- The "n" goes away
```

The same is not true for Numbers — they can lose precision when being parsed from a string:

```
» Number("994633657141813248")
994633657141813200 // <-- Off by 48!
```

MDN has much [more information on BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt).

## Accessibility Checks in DevTools

Each release of Firefox brings improved DevTools, but Firefox 68 marks the debut of a brand new capability: checking for basic accessibility issues.

With Firefox 68, the Accessibility panel can now report any [color contrast](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Understanding_WCAG/Perceivable/Color_contrast) issues with text on a page. More checks are planned for the future.

We’ve also:

- Included a button in the Inspector that enables “print media emulation,” making it easy to see what elements of a page would be visible when printed. (Try it on
[Wikipedia](https://en.wikipedia.org/wiki/Fennec_fox)!) - Improved CSS warnings in the console to show more information and include a link to related nodes.
![Screenshot of the Firefox DevTools showing a CSS warnings in the Console of the form "unknown property 'foo', declaration dropped." The warning shows a list of nodes matching the selector with the erroneous rule.](../../assets/d2f7fcb39f1f8006.png)

- Added support for
[adjusting letter spacing](https://bugzilla.mozilla.org/show_bug.cgi?id=1536237)in the[Font Editor](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_fonts). - Implemented
[RegEx-based filtering](https://bugzilla.mozilla.org/show_bug.cgi?id=1441079)in the DevTools Console: just enclose your query in slashes, like`/(foo|bar)/`

. - Made it possible to block specific requests by right-clicking on them in the Network panel.

Firefox 68 also includes refinements to the [smarter debugging features](https://hacks.mozilla.org/2019/05/faster-smarter-javascript-debugging-in-firefox/) we wrote about a few weeks ago.

## Web Compatibility

Keeping the Web open is hard work. Sometimes browsers disagree on how to interpret web standards. Other times, browsers implement and ship their own ideas without going through the standards process. Even worse, some developers intentionally block certain browsers from their sites, regardless of whether or not those browsers would have worked.

At Mozilla, we call these “Web Compatibility” problems, or “webcompat” for short.

Each release of Firefox contains fixes for webcompat issues. For example, Firefox 68 implements:

- Internet Explorer’s
`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet/addRule" rel="nofollow">addRule()</a>`

and`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet/removeRule" rel="nofollow">removeRule()</a>`

CSS methods. - Safari’s
`<a href="https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-line-clamp" rel="nofollow">-webkit-line-clamp</a>`

CSS property.

In the latter case, even with a standard `line-clamp`

property in the works, we have to support the `-webkit-`

version to ensure that existing sites work in Firefox.

Unfortunately, not all webcompat issues are as simple as implementing non-standard APIs from other browsers. Some problems can only be fixed by modifying how Firefox works on a specific site, or even telling Firefox to pretend to be something else in order to evade browser sniffing.

We deliver these targeted fixes as part of the [webcompat system add-on](https://github.com/mozilla/webcompat-addon) that’s bundled with Firefox. This makes it easier to update our webcompat interventions as sites change, without needing to bake those fixes directly into Firefox itself. And as of Firefox 68, you can view (and disable) these interventions by visiting `about:compat`

and toggling the relevant switches.

Our first preference is always to help developers ensure their sites work on all modern browsers, but we can only address the problems that we’re aware of. If you run into a web compatibility issue, please report it at [webcompat.com](https://webcompat.com/).

## CSS: Scroll Snapping and Marker Styling

Firefox 68 supports the latest syntax for [CSS scroll snapping](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap), which provides a standardized way to control the behavior of scrolling inside containers. You can find out more in Rachel Andrew’s article, [ CSS Scroll Snap Updated in Firefox 68](https://hacks.mozilla.org/2019/06/css-scroll-snap-updated-in-firefox-68/).

As shown in the video above, scroll snapping allows you to start scrolling a container so that, when a certain threshold is reached, letting go will neatly finish scrolling to the next available snap point. It is easier to understand this if you try it yourself, so [download Firefox 68](https://mozilla.org/firefox) and try it out on some of the examples in the [MDN Scroll Snapping docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap).

And if you are wondering where this leaves the now old-and-deprecated Scroll Snap Points spec, read [ Browser compatibility and Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap/Browser_compat).

Today’s release of Firefox also adds support for the `<a href="https://developer.mozilla.org/en-US/docs/Web/CSS/::marker" rel="nofollow">::marker</a>`

pseudo-element. This makes it possible to style the bullets or counters that appear to the side of [list items](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/li) and [summary](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/summary) elements.

Last but not least, CSS transforms now work on SVG elements like `mark`

, `marker`

, `pattern`

and `clipPath`

, which are indirectly rendered.

We have an entire article in the works diving into these and other CSS changes in Firefox 68; look for it later this month.

## Browser: WebRender and QuantumBar Updates

Two months ago, Firefox 67 became the first Firefox release with [WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) enabled by default, though limited to users with NVIDIA GPUs on Windows 10. Firefox 68 expands that audience to include people with AMD GPUs on Windows 10, with more platforms on the way.

We’ve also been hard at work in other areas of Firefox’s foundation. The URL bar (affectionately known as the “AwesomeBar”) has been completely reimplemented using web technologies: HTML, CSS, and JavaScript. This new ”[QuantumBar](https://bugzilla.mozilla.org/show_bug.cgi?id=quantumbar)” should be indistinguishable from the previous AwesomeBar, but its architecture makes it easier to maintain and extend in the future. We move one step closer to the eventual elimination of our legacy XUL/XBL toolkit with this overhaul.

## DOM APIs

Firefox 68 brings several changes to existing DOM APIs, notably:

- Access to cameras, microphones, and other media devices is no longer allowed in insecure contexts like plain HTTP.
- You can now pass the
`noreferrer`

option to`<a href="https://developer.mozilla.org/en-US/docs/Web/API/Window/open" rel="nofollow">window.open()</a>`

to avoid leaking referrer information upon opening a link in a new window.

We’ve also added a few new APIs, including support for the [Visual Viewport API](https://developer.mozilla.org/en-US/docs/Web/API/Visual_Viewport_API) on Android, which returns the viewport taking into consideration things like on-screen keyboards or pinch-zooming. These may result in a smaller visible area than the overall [layout viewport](https://developer.mozilla.org/en-US/docs/Glossary/viewport).

It is also now possible to use the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/decode" rel="nofollow">.decode()</a>`

method on [HTMLImageElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement) to download and decode elements before adding them to the DOM. For example, this API simplifies replacing low-resolution placeholders with higher resolution images: it provides a way to know that a new image can be immediately displayed upon insertion into the page.

## More Inside

These highlights just scratch the surface. In addition to these changes in Firefox, the last month has seen us release [Lockwise](https://lockwise.firefox.com/), a password manager that lets you take your saved credentials with you on mobile. We’ve also released a brand new [Firefox Preview](https://app.adjust.com/n9x7nra) on Android, and more.

From all of us at your favorite nominee for [Internet Villain of the Year](https://techcrunch.com/2019/07/05/isp-group-mozilla-internet-villain-dns-privacy/), thank you for [choosing Firefox](https://www.mozilla.org/firefox/).

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 15 comments

PotchJuly 9th, 2019 at 13:45RobertJuly 9th, 2019 at 22:39Dan CallahanJuly 10th, 2019 at 08:14FlimmJuly 11th, 2019 at 01:33SebastianJuly 12th, 2019 at 01:16Dan CallahanJuly 12th, 2019 at 05:22KrishJuly 18th, 2019 at 09:01Dan CallahanJuly 18th, 2019 at 09:42Daniele VisaggioJuly 18th, 2019 at 09:08Dan CallahanJuly 18th, 2019 at 11:50Daniele VisaggioJuly 19th, 2019 at 00:48Dan CallahanJuly 19th, 2019 at 08:07BuvJuly 19th, 2019 at 03:51OkaokiJuly 19th, 2019 at 03:56Dan CallahanJuly 19th, 2019 at 08:23