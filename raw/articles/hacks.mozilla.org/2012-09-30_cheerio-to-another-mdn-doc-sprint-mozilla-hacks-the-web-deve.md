---
title: Cheerio! to another MDN doc sprint – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/09/cheerio-to-another-mdn-doc-sprint/
author: Janet Swisher
published: '2012-09-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This past weekend, a group of MDN contributors finished another fun and productive documentation sprint, while enjoying the environment of Mozilla’s London office.


Here’s a sampling of what we accomplished:

<

ul>

**Onur Avsar**added the last remaining HTML elements that were undocumented (

[noframes](https://developer.mozilla.org/en-US/docs/HTML/Element/noframes),

[isindex](https://developer.mozilla.org/en-US/docs/HTML/Element/isindex),

[spacer](https://developer.mozilla.org/en-US/docs/HTML/Element/spacer),

[ruby](https://developer.mozilla.org/en-US/docs/HTML/Element/ruby),

[rt](https://developer.mozilla.org/en-US/docs/HTML/Element/rt), and

[rp](https://developer.mozilla.org/en-US/docs/HTML/Element/rp)). The

[HTML element reference](https://developer.mozilla.org/en-US/docs/HTML/element)on MDN now has

**complete coverage**. Woot! (Of course, all the reference pages can always be improved, especially with browser compatibility info and code examples.)

**Louis-Rémi Babé**installed Kuma, improved the

[Kuma installation docs](https://github.com/mozilla/kuma/blob/master/docs/installation-vagrant.rst)as a result, and submitted a pull request to enable creating tab components.

**Frédéric Bourgeon**(participating remotely!) translated

[::first-line](https://developer.mozilla.org/fr/docs/CSS/::first-line),

[transition-duration](https://developer.mozilla.org/fr/docs/CSS/transition-duration), and

[transition-property](https://developer.mozilla.org/fr/docs/CSS/transition-property)into French.

**Julia Buchner**created French translations for

[border-image](https://developer.mozilla.org/fr/docs/CSS/border-image),

[border-image-width](https://developer.mozilla.org/fr/docs/CSS/border-image-source>border-image-source</a>, and <a href=), and learned about compatibility table templates and live examples, and worked on automating testing of HTML and CSS properties. She also submitted several bugs, related to localizing in Kuma.

**Marc-Aurèle Darche**wrote

[Open Web Apps and Web standards](https://developer.mozilla.org/en-US/docs/Open_Web_apps_and_Web_standards), based on partly on

[Kumar McMillan’s recent blog post](https://blog.mozilla.org/webdev/2012/09/14/apps-the-web-is-the-platform/), rewrote

[What is the difference between an app and an add-on?](https://developer.mozilla.org/en-US/docs/Apps/FAQs/About_apps#What_is_the_difference_between_an_app_and_an_add-on.3F), fixed the rendering of

[mozIStorageService](https://developer.mozilla.org/en-US/docs/XPCOM_Interface_Reference/mozIStorageService), and added

`--class X11`

to the [command-line options](https://developer.mozilla.org/en-US/docs/Command_Line_Options)for Mozilla applications.

**Christian Heilmann**created a demo and corresponding article on

[taking webcam photos](https://developer.mozilla.org/en-US/docs/WebRTC/Taking_webcam_photos)using WebRTC. Thanks also to Chris for making sure we had lots of good coffee!

**Trevor Hobson**(participating remotely!) updated

[nsINavBookmarksService](https://developer.mozilla.org/en-US/docs/XPCOM_Interface_Reference/nsINavBookmarksService)with Gecko 14 changes, and also fixed broken links and compatibility tables that were out of order.

**Jérémie Patonnier**documented a bunch of SVG attribute pages, such as

[mode](https://developer.mozilla.org/en-US/docs/SVG/Attribute/mode)and

[type](https://developer.mozilla.org/en-US/docs/SVG/Attribute/type); edited some of the SVG filter element pages to make them clearer; and worked on an upcoming post for the Hacks blog.

**Jean-Yves Perrier**documented the

[value definition syntax](https://developer.mozilla.org/en-US/docs/CSS/Value_definition_syntax)for CSS property values and the CSS

[cascade algorithm](https://developer.mozilla.org/en-US/docs/CSS/Cascade); added images to

[padding-top](https://developer.mozilla.org/en-US/docs/CSS/padding-top),

[padding-bottom](https://developer.mozilla.org/en-US/docs/CSS/margin-top>margin-top</a>, <a href=); and started rewriting

[background-size](https://developer.mozilla.org/en-US/docs/CSS/background-size).

**Florian Scholz**created a new

[WebAPI landing page](https://developer.mozilla.org/en-US/docs/WebAPI), documented the Web APIs for

[Ambient Light](https://developer.mozilla.org/en-US/docs/DOM/DeviceLightEvent), and <a href=”https://developer.mozilla.org/en-US/docs/DOM/DeviceProximityEvent>Device Proximity,and

[Screen Brightness](https://developer.mozilla.org/en-US/docs/DOM/window.screen.mozBrightness); updated

[WebSMS](https://developer.mozilla.org/en-US/docs/API/WebSMS)and

[Battery API](https://developer.mozilla.org/en-US/docs/DOM/window.navigator.battery); and documented several issues marked “dev-doc-needed” in Bugzilla. Florian also helped Louis-Remi set up Kuma and submit a pull request!

**Till Schneidereit**updated all the obsolete

[JSAPI functions](https://developer.mozilla.org/en-US/docs/SpiderMonkey/JSAPI_Reference)with the version where they were removed, documented some new functions, and updated some changed ones.

**Julien Wajsberg**and Marc-Aurèle worked together on improving the

[IndexedDB](https://developer.mozilla.org/en-US/docs/IndexedDB)docs, testing and writing code examples. Julien, who works for

[Orange Labs](http://www.orange.com), says that he owes most of his knowledge of IndexedDB to the work of his intern there,

**Samy Kantari**.

Thanks to **Chris Mills** from Opera for hanging out with the group while working on a related project. (Look for more news about that later this week.)

**Kadir Topal** from the [SUMO](https://support.mozilla.org) team also joined us, and talked with localizers about their workflow and needs. Since MDN’s Kuma platform is based on SUMO’s Kitsune platform, relevant improvements in one will eventually flow to the other.

Thanks also to **Ali Spivak** for organizing all the logistics, and to **Shannon Clayton** for helping us feel welcome. I’m afraid we put a bit of a dent in the office’s supply of chocolate:

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.