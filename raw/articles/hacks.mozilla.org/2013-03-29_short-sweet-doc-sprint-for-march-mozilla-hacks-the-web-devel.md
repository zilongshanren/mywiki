---
title: Short sweet doc sprint for March – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/03/short-sweet-doc-sprint-for-march/
author: Janet Swisher
published: '2013-03-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This past weekend, a small band of hardy MDN contributors pitched in for the first of a monthly series of doc sprints. This sprint was organized on fairly short notice, yet a significant amount of work was accomplished.

## Web standards docs

**Jérémie Patonnier**created a bunch of API reference pages for[MozMobileConnection](https://developer.mozilla.org/en-US/docs/DOM/MozMobileConnection), and SVG attributes[dx](https://developer.mozilla.org/en-US/docs/SVG/Attribute/dx)and[dy](https://developer.mozilla.org/en-US/docs/SVG/Attribute/dy), and did a “crazy bunch of clean up” on the[SVG](https://developer.mozilla.org/en-US/docs/SVG)documentation.**Michael Beckwith**cleaned up writing on[isNan](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Number/isNaN)and[indexOf](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Array/indexOf), and made minor touchups to[:active](https://developer.mozilla.org/en-US/docs/CSS/:active).**Kevin Brosnan**updated the compatibility info in[Supported media formats](https://developer.mozilla.org/en-US/docs/HTML/Supported_media_formats).**fusionchess**expanded the paragraph on passing data in[Using web workers](https://developer.mozilla.org/en-US/docs/DOM/Using_web_workers)and added an example of a generic “asynchronous eval()”.

## Firefox OS and Apps

**Gangadhar Nittala**made his first contribution to MDN by changing the[Apps manifest](https://developer.mozilla.org/en-US/docs/Apps/Manifest)article to indicate that the .webapp extension for the file is mandatory, not just recommended.**Jonathan Watt**added a section to[Preparing for your first B2G build](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Preparing_for_your_first_B2G_build)on how to update your B2G tree.**nullspace**further clarified in[Preparing for your first B2G build](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Preparing_for_your_first_B2G_build)that there are gigabytes of Android libraries to download, which can take tens of hours (or days).

## Mozilla technology

**Cory Gackenheimer**updated[Web Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console)for[bug 623749](https://bugzilla.mozilla.org/show_bug.cgi?id=623749).**Trevor Hobson**updated[Styling a tree](https://developer.mozilla.org/en-US/docs/XUL/Tutorial/Styling_a_Tree)to reflect changes in Gecko 22.**Florian Scholz**worked on Firefox[dev-doc-needed](http://beta.elchi3.de/doctracker/)issues:- Documented that a Mac OS X backend for the DeviceLightEvent is now implemented.
- Updated
[CanvasRenderingContext2D](https://developer.mozilla.org/en-US/docs/DOM/CanvasRenderingContext2D)for the now-implemented isPointInStroke method. - Documented the rename of the allowfullscreen attribute of the HTML
[iframe](https://developer.mozilla.org/en-US/docs/HTML/element/iframe)element in Firefox 18 and WebKit Nightly (was prefixed). - Documented that DOMImplementation.hasFeature() and Node.isSupported() will always return true starting with Firefox 19.
- Noted that createElement(null) works like createElement(“null”) starting with Firefox 19.

**Tom Schuster**worked on lots of little[dev-doc-needed](http://beta.elchi3.de/doctracker/)bugs.**donghao526**updated the simplified Chinese translation of[The essentials of an extension](https://developer.mozilla.org/zh-CN/docs/XUL_School/The_Essentials_of_an_Extension).**darktrojan**added a table about bootstrap data in[Bootstrapped extensions](https://developer.mozilla.org/en-US/docs/Extensions/Bootstrapped_extensions).**Cykesiopka**updated the join() example in[Path manipulation](https://developer.mozilla.org/en-US/docs/JavaScript_OS.File/OS.Path)so that the MDN and Gecko in-source documentation match.**the prisoner**updated the French translations of[Firefox 19 for developers](https://developer.mozilla.org/fr/docs/Firefox_19_pour_les_developpeurs)and[Firefox 20 for developers](https://developer.mozilla.org/fr/docs/Firefox_20_pour_developeurs).**complynx**fixed links to mutation observers in[Mozilla event reference](https://developer.mozilla.org/en-US/docs/DOM/Mozilla_event_reference).**Ernest Chiang**updated the traditional Chinese translation of[Persona Quick Setup](https://developer.mozilla.org/zh-TW/docs/Persona/Quick_Setup).

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.

## 4 comments

tom jonesMarch 29th, 2013 at 11:37Janet SwisherMarch 30th, 2013 at 21:27tom jonesApril 1st, 2013 at 15:52Janet SwisherApril 1st, 2013 at 16:38