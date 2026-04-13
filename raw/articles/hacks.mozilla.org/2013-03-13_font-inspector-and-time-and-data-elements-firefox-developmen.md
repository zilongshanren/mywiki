---
title: Font Inspector and <time> and <data> elements – Firefox Development Highlights
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/03/font-inspector-and-elements-firefox-development-highlights/
author: Robert Nyman
published: '2013-03-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Time for another look at the latest developments with Firefox. This is part of our [Bleeding Edge](https://hacks.mozilla.org/category/bleeding-edge/) and [Firefox Development Highlights](https://hacks.mozilla.org/category/firefox/firefox-development-highlights/) series, and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## Font Inspector

A Font Inspector is now available in the Firefox DevTools.

In the Firefox Inspector, a “Fonts” panel is now available. It exposes different information about the `@font-faces`

used in the page:

- Font name and font family
- Its location (system vs. remote, and URL)
- A preview (you can change it)
- @font-face code

## HTML5 and

We have implemented support for two new elements:

### <time> element

The HTML time element (

Example:

The concert took place on .


More information can be found in the [MDN documentation for the <time> element](https://developer.mozilla.org/en-US/docs/HTML/HTML_Elements/time), and in the [W3C specification](http://www.w3.org/html/wg/drafts/html/master/text-level-semantics.html#the-time-element).

### <data> element

The data element represents its contents, along with a machine-readable form of those contents in the value attribute. The value attribute must be present and its value must be a representation of the element’s contents in a machine-readable format.

The <data> element adds a new attribute, `value`

, which contains a string representation of the data. In script we can use the `.value`

property to get the reflected value:

Example:

```
David Humphrey
document.getElementById("user").value; // "humphd"
```

It’s available in the [WHATWG specification](http://www.whatwg.org/specs/web-apps/current-work/multipage/text-level-semantics.html#the-data-element), and David Humphrey’s wrote more about it in [HTML5 time and data elements in Firefox](http://vocamus.net/dave/?p=1585).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 5 comments

Chris AdamsMarch 13th, 2013 at 16:09Anthony CaudillMarch 13th, 2013 at 17:07Aftab KhalidMarch 13th, 2013 at 23:54BastianMarch 15th, 2013 at 10:32Robert Nyman [Editor]March 18th, 2013 at 02:51