---
title: Firefox 64 Released – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/12/firefox-64-released/
author: Dan Callahan
published: '2018-12-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 64 is [available today](https://www.mozilla.org/firefox/new/)! Our new browser has a wealth of exciting developer additions both in terms of interface features and web platform features, and we can’t wait to tell you about them. You can find out all the news in the sections below — please check them out, have a play around, and let us know your feedback in the comment section below.

## New Firefox interface features

### Multiple tab selection

We’re excited to introduce **multiple tab selection**, which makes it easier to manage windows with many open tabs. Simply hold Control (Windows, Linux) or Command (macOS) and click on tabs to select them.

Once selected, click and drag to move the tabs as a group — either within a given window, or out into a new window.

### Devtools improvements

Our Developer Tools also gained a notable new feature: when hovering over text, the [Accessibility Inspector](https://developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector) now displays **text contrast ratios** in the pop-up infobar.

The infobar also indicates whether or not the text meets [WCAG 2.0 Level AA or AAA accessibility guidelines](https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html) for minimum contrast.

Another great addition is related to [Responsive Design Mode](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_Mode) — device selection is now saved between sessions.

## New CSS features in 64

### Standardizing proprietary styling features

As part of our platform work, we’re trying to standardize some of the non-standard CSS features that have often caused developers cross-browser headaches. Landing in 64 we’ve got the following:

- CSS Scrollbars: The
[CSS Scrollbars Level 1 spec](https://drafts.csswg.org/css-scrollbars-1/)standardizes features for setting scrollbar width and color, which were originally only available in Internet Explorer. See[CSS Scrollbars on MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scrollbars)and[Scrollbars on CSS Tricks](https://css-tricks.com/almanac/properties/s/scrollbar/)for more information. `-webkit-appearance`

: To make the effects of the`appearance`

property more consistent across browsers, Firefox has unshipped all of its own proprietary values from web content, and added support for all the`-webkit-`

prefixed versions that are in common use. See[https://developer.mozilla.org/en-US/docs/Web/CSS/appearance on MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/appearance)for more information.- Going forward in Firefox, if a selector chain or group includes a
`-webkit-`

prefixed pseudo-element, that pseudo-element no longer invalidates the whole group.

### New media queries

Firefox 64 sees the addition of new media queries from the [Level 4](https://drafts.csswg.org/mediaqueries-4/) and [Level 5](https://drafts.csswg.org/mediaqueries-5/) specifications for [detecting pointers/touchscreens](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/any-pointer), [whether the user can hover](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/any-hover) over something, and whether the user prefers [reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

### Multi-position color stop gradients

CSS gradients now support multi-position color stops (e.g. see their use on [linear gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient#Gradient_with_multi-position_color_stops)). So now `yellow 25%, yellow 50%`

can now be written `yellow 25% 50%`

, for example.

## JavaScript improvements

There were a lot of internal improvements this time around. In terms of developer facing improvements:

- The TC39
[Well-formed JSON.stringify proposal](https://github.com/tc39/proposal-well-formed-stringify)has been implemented, to prevent[JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)from returning ill-formed Unicode strings. - Proxied functions can now be be passed to
[Function.prototype.toString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/toString)`.call()`

.

## New Web API highlights

### Fullscreen API unprefixed

Goodbye `mozRequestFullScreen`

! The [Fullscreen API](https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API) is now available in Firefox without a prefix. The [requestFullscreen](https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen) and [exitFullscreen](https://developer.mozilla.org/en-US/docs/Web/API/Document/exitFullscreen) APIs now also return promises that resolve once the browser finishes transitioning between states.

### WebVR 1.1 in macOS

What’s more immersive than Fullscreen? Virtual reality, of course. And Firefox 64 now supports [WebVR 1.1](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API) on macOS!

![](../../assets/56e9e064dfa8b997.jpg)


### startMessages() for Service Workers

On a completely unrelated note, pages with Service Workers can now use the [startMessages() API](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/startMessages) to begin receiving queued worker messages, even before page loading has completed.

## New Add-ons Features

What follows are the highlights. For more details, see [Extensions in Firefox 64](https://blog.mozilla.org/addons/2018/11/08/extensions-in-firefox-64/).

### Context menu enhancements

Firefox 64 introduces an entirely new API, `browser.menus.overrideContext`

, which allows complete customization of the context menu shown within add-on content like sidebars, popups, etc. These context menus can also automatically include custom entries from *other* add-ons, as though the user had right-clicked on a tab or bookmark. [Piro’s blog post](https://piro.sakura.ne.jp/latest/blosxom/mozilla/xul/2018-10-14_override-context-on-fx64.htm) explains how it all works.

In addition:

- You can now restrict where context menus can appear in an add-on using the new
`viewTypes`

property in[menus.create()](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/create)and[menus.update()](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/update). [menus.update()](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/update)can now be used to update the icon of an existing menu item.- Extensions can now detect which mouse button was used when a menu item was clicked — this can be found using the new
`button`

property of[menus.OnClickData](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/OnClickData).

### Custom content in the Dev Tools inspector

Also, add-ons can now display custom content within the Dev Tools Inspector sidebar by calling the new [sidebar.setPage()](https://bugzilla.mozilla.org/show_bug.cgi?id=1398734) API.

### Managing add-ons updated

For users, the add-on management interface, `about:addons`

, was redesigned to match Firefox’s preferences page, and right-clicking an add-on icon in the browser toolbar now offers options to directly remove or manage that add-on.

## Privacy features for your protection

### Symantec CA Distrust

Due to a [history of malpractice](https://wiki.mozilla.org/CA:Symantec_Issues), Firefox 64 will not trust TLS certificates issued by Symantec (including under their GeoTrust, RapidSSL, and Thawte brands). Microsoft, Google, and Apple are implementing similar measures for their respective browsers.

### Referrer-Policy for stylesheets

The [Referrer-Policy header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) now applies to requests [initiated by CSS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy#Integration_with_CSS) (e.g., `background-image: url("http://...")`

). The default policy, `no-referrer-when-downgrade`

, omits referrer information when a secure origin (`https`

) requests data from an insecure origin (`http`

).

### buildID fixed timestamp

Lastly, from now on the non-standard [navigator.buildID](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/buildID) property will always return a fixed timestamp, `20181001000000`

, to mitigate its potential abuse for fingerprinting.

## Further Reading

For more information, see [Firefox 64 for Developers](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/64) on MDN, and the official [Firefox 64 Release Notes](https://www.mozilla.org/en-US/firefox/64.0/releasenotes/). If you’re a web developer, you may also be interested in the [Firefox 64 Site Compatibility](https://www.fxsitecompat.com/en-CA/versions/64/) notes.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 4 comments

rk4391December 11th, 2018 at 11:43Dan CallahanDecember 11th, 2018 at 16:17marioDecember 11th, 2018 at 13:27Dan CallahanDecember 11th, 2018 at 16:10