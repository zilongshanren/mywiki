---
title: New CSS Features in Firefox 68 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/07/new-css-features-in-firefox-68/
author: Rachel Andrew
published: '2019-07-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 68 landed earlier this month with a bunch of CSS additions and changes. In this blog post we will take a look at some of the things you can expect to find, that might have been missed in earlier announcements.

## CSS Scroll Snapping

The headline CSS feature this time round is CSS Scroll Snapping. I won’t spend much time on it here as you can [read the blog post](https://hacks.mozilla.org/2019/06/css-scroll-snap-updated-in-firefox-68/) for more details. The update in Firefox 68 brings the Firefox implementation in line with Scroll Snap as implemented in Chrome and Safari. In addition, it removes the old properties which were part of the earlier Scroll Snap Points Specification.

## The `::marker`

pseudo-element

The `::marker`

pseudo-element lets you select the marker box of a list item. This will typically contain the list bullet, or a number. If you have ever used an image as a list bullet, or wrapped the text of a list item in a span in order to have different bullet and text colors, this pseudo-element is for you!

With the marker pseudo-element, you can target the bullet itself. The following code will turn the bullet on unordered lists to hot pink, and make the number on an ordered list item larger and blue.

```
ul ::marker {
color: hotpink;
}
ol ::marker {
color: blue;
font-size: 200%;
}
```


![An ordered and unordered list with styled bullets](../../assets/2e9b8e6b4bb2d928.png)

With `::marker`

we can style our list markers

There are only a few CSS properties that may be used on `::marker`

. These include all font properties. Therefore you can change the font-size or family to be something different to the text. You can also color the bullets as shown above, and insert generated content.

### Using `::marker`

on non-list items

A marker can only be shown on list items, however you can turn any element into a list-item by using `display: list-item`

. In the example below I use `::marker`

, along with generated content and a CSS counter. This code outputs the step number before each `h2`

heading in my page, preceded by the word “step”. [You can see the full example on CodePen](https://codepen.io/rachelandrew/pen/OepQry).

```
h2 {
display: list-item;
counter-increment: h2-counter;
}
h2::marker {
content: "Step: " counter(h2-counter) ". ";
}
```


If you take a look at [ the bug for the implementation of ::marker](https://bugzilla.mozilla.org/show_bug.cgi?id=205202#c1) you will discover that it is 16 years old! You might wonder why a browser has 16 year old implementation bugs and feature requests sitting around. To find out more read through the issue, where you can discover that it wasn’t clear originally if the

`::marker`

pseudo-element would make it into the spec.There were some Mozilla-specific properties that achieved the result developers were looking for with something like `::marker`

. The properties `::moz-list-bullet`

and `::moz-list-marker`

allowed for the styling of bullets and markers respectively, using a moz- vendor prefix.

The `::marker`

pseudo-element is standardized in [CSS Lists Level 3](https://www.w3.org/TR/css-lists-3/), and [CSS Pseudo-elements Level 4](https://www.w3.org/TR/css-pseudo-4/#marker-pseudo), and currently implemented as of Firefox 68, and Safari. Chrome has yet to implement `::marker`

. However, in most cases you should be able to use `::marker`

as an enhancement for those browsers which support it. You can allow the markers to fall back to the same color and size as the rest of the list text where it is not available.

## CSS Fixes

It makes web developers sad when we run into a feature which is supported but works differently in different browsers. These interoperability issues are often caused by the sheer age of the web platform. In fact, some things were never fully specified in terms of how they should work. Many changes to our CSS specifications are made due to these interoperability issues. Developers depend on the browsers to update their implementations to match the clarified spec.

Most browser releases contain fixes for these issues, making the web platform incrementally better as there are fewer issues for you to run into when working with CSS. The latest Firefox release is no different – we’ve got [fixes for the ch unit](https://bugzilla.mozilla.org/show_bug.cgi?id=282126), and [list numbering](https://bugzilla.mozilla.org/show_bug.cgi?id=288704) shipping.

## Developer Tools

In addition to changes to the implementation of CSS in Firefox, Firefox 68 brings you some great new additions to Developer Tools to help you work with CSS.

In the Rules Panel, look for the new print styles button. This button allows you to toggle to the print styles for your document, making it easier to test a print stylesheet that you are working on.


Staying with the Rules Panel, Firefox 68 shows an icon next to any invalid or unsupported CSS. If you have ever spent a lot of time puzzling over why something isn’t working, only to realise you made a typo in the property name, this will really help!

![A property named flagged invalid in the console](../../assets/7e8aee58b1895918.png)


![A property named flagged invalid in the console](../../assets/7e8aee58b1895918.png)

In this example I have spelled padding as “pudding”. There is (sadly) no pudding property so it is highlighted as an error.


The console now shows more information about CSS errors and warnings. This includes a nodelist of places the property is used. You will need to click CSS in the filter bar to turn this on.


So that’s my short roundup of the features you can start to use in Firefox 68. Take a look at the [Firefox 68 release notes](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/68) to get a full overview of all the changes and additions that Firefox 68 brings you.

## About
[
Rachel Andrew ](https://rachelandrew.co.uk)

Rachel Andrew is a front and back-end web developer, one half of the company behind Perch CMS, and Editor in Chief of Smashing Magazine. She is a Google Developer Expert for web technologies and a member of the CSS Working Group representing Fronteers, where she is co-editor of the Multi-column Layout spec. Author of 22 books, and a frequent public speaker at conferences worldwide, you can find out what she is up to at https://rachelandrew.co.uk.

## 3 comments

Davi HosogiriAugust 1st, 2019 at 10:59EnsoStudioAugust 2nd, 2019 at 02:53Brandon McConnellAugust 7th, 2019 at 10:05