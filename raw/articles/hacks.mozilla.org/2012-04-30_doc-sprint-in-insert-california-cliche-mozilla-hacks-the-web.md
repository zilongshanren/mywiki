---
title: Doc sprint in [insert California cliché] – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/04/doc-sprint-in-insert-california-cliche/
author: Janet Swisher
published: '2012-04-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The last weekend in April saw yet another amazingly productive documentation sprint for MDN. A group of community members gathered at the Mozilla spaces in California, while others contributed remotely. The in-person group worked on Friday in Mozilla’s Mountain View headquarters, then spent Saturday and Sunday at the Mozilla space in San Francisco.

Here is the obligatory “OMG! Awesome view!” photo from the roof deck in San Francisco, showing just some of the doc sprinters getting in the way of the view:

![April 2012 doc sprinters April 2012 doc sprinters](../../assets/9b321ad60389722d.jpg)


Here are only some of the things that happened in MDN docs as a result of this weekend:

**Will Bamberg**researched and revamped the wiki page for[Web development for mobile devices](https://developer.mozilla.org/En/Mobile).**Michael Beckwith**:- made clarifying edits on a bunch of Web development articles
- added some suggestions to
[Tips for authoring fast-loading HTML pages](https://developer.mozilla.org/en/HTML/Tips_for_authoring_fast-loading_HTML_pages) - added browser compatibility info to
[HTMLCanvasElement](https://developer.mozilla.org/en/DOM/HTMLCanvasElement) - added code examples to
[::enabled](https://developer.mozilla.org/En/CSS/:enabled), and[BrowserID remote verification API](https://developer.mozilla.org/en/BrowserID/Remote_Verification_API) - documented why and how a developer might want to run
[multiple Firefox profiles](https://developer.mozilla.org/en/Mozilla/Multiple_Firefox_Profiles) - added descriptions to tools listed on the
[Development tools](https://developer.mozilla.org/en/Tools)page.

**Frederic Bourgeon**documented the Flexible Box Layout Model, including[Using CSS flexibile boxes](https://developer.mozilla.org/en/CSS/Using_CSS_flexible_boxes)and reference pages for:**David Bruant**wrote[JavaScript data structures](https://developer.mozilla.org/en/JavaScript/Data_structures), and cleaned up[defineProperty](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Object/defineProperty), moving non-reference examples to an[additional examples](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Object/defineProperty/Additional_examples)page, and made improvements to the main[JavaScript](https://developer.mozilla.org/en/JavaScript)page.**Anastasia Cheetham**organized the[ARIA documentation](https://developer.mozilla.org/en/Accessibility/ARIA), added techniques for using about a dozen ARIA attributes, updated[Using the slider role](https://developer.mozilla.org/en/Accessibility/ARIA/ARIA_Techniques/Using_the_slider_role), and retired a bunch of pages on CodeTalks.org that are now superceded by MDN pages.**Cory Gackenheimer**made[HTTP access control (CORS)](https://developer.mozilla.org/En/HTTP_access_control)browser-agnostic and added a compatibility table; split[Using XMLHttpRequest](https://developer.mozilla.org/en/DOM/XMLHttpRequest/Using_XMLHttpRequest)into smaller chunks (including[synchronous and asynchronous requests](https://developer.mozilla.org/en/DOM/XMLHttpRequest/Synchronous_and_Asynchronous_Requests)and[sending and receiving binary data](https://developer.mozilla.org/en/DOM/XMLHttpRequest/Sending_and_Receiving_Binary_Data)), made it more browser-agnostic, and added code examples; created[Why BrowserID](https://developer.mozilla.org/en/BrowserID/Why_BrowserID)from various sources, and updated the NodeJS example in the BrowserID[Remote verification API](https://developer.mozilla.org/en/BrowserID/Remote_Verification_API).**Mark Giffin**met with some of the Apps developers, researched app secrets, and updated[In-app payments](https://developer.mozilla.org/en/Apps/In-app_payments).**Kevin Lim**improved[Using the Page Visibility API](https://developer.mozilla.org/en/DOM/Using_the_Page_Visibility_API).**David Mandelin**drafted an article on[SpiderMonkey GC](https://developer.mozilla.org/En/SpiderMonkey/Internals/GC).**Jeremie Patonnier**translated his blog post about[getting started with MDN](http://jeremie.patonnier.net/post/2012/04/24/Bien-demarrer-avec-MDN)from French into English. Look for it soon on Hacks! He also documented SVG[word-spacing](https://developer.mozilla.org/en/SVG/Attribute/word-spacing)and[kerning](https://developer.mozilla.org/en/SVG/Attribute/kerning).**Jean-Yves Perrier**hit all the CSS reference pages with the consistency stick, from[animation](https://developer.mozilla.org/en/CSS/animation)to[z-index](https://developer.mozilla.org/en/CSS/z-index). He also documented[overflow-y](https://developer.mozilla.org/en/CSS/overflow-y).**Florian Scholz**updated[DOMException](https://developer.mozilla.org/en/DOM/DOMException)and[DOMError](https://developer.mozilla.org/en/DOM/DOMError), and researched and documented the[WebSMS API](https://developer.mozilla.org/en/API/WebSMS), including all the interfaces.**Eric Shepherd**finished documenting the[Telephony API](https://developer.mozilla.org/en/DOM/TelephonyCall), set versions and priorities for bugs that need docs, and made updates for about twenty fixed bugs, and documented[nsIPlacesImportExportService](https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIPlacesImportExportService).**Christian Sonne**worked on speeding up the compatibilityTableAggregatorNoCache template, by making these fixes:- Guides and tutorials are no longer included in the compatibility table if they don’t contain one themselves
- Fixed syntax of several compatibility tables
- Fixed typo in template called from :invalid compatibility table
- Introduced caches to individual content pages, meaning that the compatibility aggregator will have less work to do on a second run, if the first times out.

**Jeff Walden**created a release notes page for (future)[SpiderMonkey 1.8.8](https://developer.mozilla.org/en/SpiderMonkey/1.8.8), and reviewed and made lots of small updates in the[JSAPI reference](https://developer.mozilla.org/en/SpiderMonkey/JSAPI_Reference).**Kathy Walrath**improved[CanvasRenderingContext2D](https://developer.mozilla.org/en/DOM/CanvasRenderingContext2D).**Jonathan Wilsson**added compatibility tables to CSS[visibility](https://developer.mozilla.org/en/CSS/visibility),[element.getBoundingClientRect](https://developer.mozilla.org/en/DOM/element.getBoundingClientRect)and[window.setInterval](https://developer.mozilla.org/en/DOM/window.setInterval).

**Addendum** (2012-05-02): **Vikash Agrawal** created a code example for the `contextmenu`

attribute; it’s not on MDN yet, but you can [see it on github](https://github.com/ivikash/Examples-for-the-web/blob/master/src/ContextMenu.html).

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.