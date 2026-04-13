---
title: Time for a review of Firefox 92 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/09/time-for-a-review-of-firefox-92/
author: Ruth John
published: '2021-09-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Release time comes around so quickly! This month we have quite a few CSS updates, along with the new `Object.hasOwn()`

static method for JavaScript.

This blog post provides merely a set of highlights; for all the details, check out the following:

**CSS Updates**

A couple of CSS features have moved from behind a preference and are now available by default: `accent-color`

and `size-adjust.`


**accent-color**

The `accent-color`

CSS property sets the color of an element’s accent. Accents appear in elements such as a checkbox or radio input. It’s default value is `auto`

which represents a UA-chosen color, which should match the accent color of the platform. You can also specify a color value. [Read more about the accent-color property here](https://developer.mozilla.org/en-US/docs/Web/CSS/accent-color).

**size-adjust**

The `size-adjust`

descriptor for `@font-face`

takes a percentage value which acts as a multiplier for glyph outlines and metrics. Another tool in the CSS box for controlling fonts, it can help to harmonize the designs of various fonts when rendered at the same font size. [Check out some examples on the size-adjust descriptor page on MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust).

**And more…**

Along with both of those, the `break-inside`

property now has support for values `avoid-page`

and `avoid-column`

, the `font-size-adjust`

property accepts two values *and* if that wasn’t enough `system-ui`

as a generic font family name for the `font-family`

property is now supported.

**Object.hasOwn arrives**

A nice addition to JavaScript is the `Object.hasOwn()`

static method. This returns `true`

if the specified property is a direct property of the object (even if that property’s value is `null`

or `undefined`

). `false`

is returned if the specified property is inherited or not declared. Unlike the [ in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/in) operator, this method does not check for the specified property in the object’s prototype chain.

`Object.hasOwn()`

is recommended over [ Object.hasOwnProperty()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty) as it works for objects created using

`Object.create(null)`

and with objects that have overridden the inherited `hasOwnProperty()`

method.## About Ruth John

Ruth John works as a Technical Writer at Mozilla. A recent addition to the MDN team, she's a big fan of web technologies, and not only enjoys writing about them, but building demos with them as well.

## 2 comments

JohnSeptember 14th, 2021 at 07:27Youdon TneedthatSeptember 22nd, 2021 at 02:50