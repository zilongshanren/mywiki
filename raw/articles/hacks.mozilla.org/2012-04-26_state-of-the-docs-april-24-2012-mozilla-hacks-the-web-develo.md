---
title: State of the Docs, April 24, 2012 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/04/state-of-the-docs-april-24-2012/
author: Janet Swisher
published: '2012-04-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The following is a sample of the changes to the documentation on MDN in the past four weeks. We expect a large flurry of activity during the [Documentation sprint](https://wiki.mozilla.org/MDN/Doc_Sprints/2012April) this weekend. If you’re in the Bay Area, you’re welcome to join in person for any part of the sprint, or join remotely if you’re elsewhere.

## Help needed

A reader provided feedback that they don’t understand the domQuery example in the [global Function object](http://developer.mozilla.org/Talk:en/JavaScript/Reference/Global_Objects/Function). It needs to be more clearly explained.

## Web standards docs

**Vikash Agrawal**added a code example to[:only-child](https://developer.mozilla.org/en/CSS/%3Aonly-child). Vikash is starting a Google Summer of Code project to add code examples for HTML and CSS reference pages. Good luck, Vikash!**“aHref”**created CSS[border-image-outset](https://developer.mozilla.org/en/CSS/border-image-outset).**Eric Bidelman**updated the compatibility info in[Function bind()](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Function/bind).**Frédéric Bourgeon**updated the spec table for[:invalid](https://developer.mozilla.org/en/CSS/%3Ainvalid)and added a French translation.**David Bruant**wrote an article on[JavaScript memory management](https://developer.mozilla.org/en/JavaScript/Memory_Management).**Giles Burdett**updated[Writing Websocket client applications](https://developer.mozilla.org/en/WebSockets/Writing_WebSocket_client_applications).**Dan Callahan**added`privacyURL`

and`toURL`

to[navigator.id.get](https://developer.mozilla.org/en/DOM/navigator.id.get).**Simon Chan**added IE compatibility to[Manipulating the browser history](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history).**Pamela Fox**added the ‘download’ attribute to the[<a> element](https://developer.mozilla.org/en/HTML/Element/a).**Fusionchess**has been very active, including:- adding a section on embedded workers and a code example to
[Using Web workers](https://developer.mozilla.org/En/DOM/Using_web_workers) - adding code examples to
[defineProperties](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Object/defineProperties),[Bitwise operators](https://developer.mozilla.org/en/JavaScript/Reference/Operators/Bitwise_Operators),[the structured clone algorithm](https://developer.mozilla.org/en/DOM/The_structured_clone_algorithm),[Blob](https://developer.mozilla.org/en/DOM/Blob), and[window.location](https://developer.mozilla.org/en/DOM/window.location) - creating pages for
[window.onbeforeprint](https://developer.mozilla.org/en/DOM/window.onbeforeprint)and[window.onafterprint](https://developer.mozilla.org/en/DOM/window.onafterprint) - adding information on sending a Blob object to
[Using HMLttpRequest](https://developer.mozilla.org/en/DOM/XMLHttpRequest/Using_XMLHttpRequest)

- adding a section on embedded workers and a code example to
**David Humphrey**updated the text and examples of[Pointer lock API](https://developer.mozilla.org/en/API/Pointer_Lock_API).**Husky**add info about calling history.pushState to[window.onpopstate](https://developer.mozilla.org/en/DOM/window.onpopstate).**Kenan**added IE Mobile compatibility info to[window.btoa](https://developer.mozilla.org/en/DOM/window.btoa)and[window.atob](https://developer.mozilla.org/en/DOM/window.atob).**Jesper Kristensen**updated[Fixing common validation problems](https://developer.mozilla.org/en/Fixing_common_validation_problems), including changing the examples to HTML5, and updated[XHTML](https://developer.mozilla.org/en/XHTML).**Gijs Kruitbosch**added compatibility info to[JSON](http://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/JSON).**Jeremie Patonnier**created pages for the SVG attributes[opacity](https://developer.mozilla.org/en/SVG/Attribute/opacity),[color-interpolation](https://developer.mozilla.org/en/SVG/Attribute/color-interpolation),[color-interpolation-filters](https://developer.mozilla.org/en/SVG/Attribute/color-interpolation-filters), and[color-rendering](https://developer.mozilla.org/en/SVG/Attribute/color-rendering).**Jean-Yves Perrier**created an article on[CSS WebKit extensions](https://developer.mozilla.org/en/CSS/CSS_Reference/Webkit_Extensions), added Greek alphabet examples to[CSS text-transform](https://developer.mozilla.org/en/CSS/text-transform)[, added browser compatibility table and info to][text-indent](https://developer.mozilla.org/en/CSS/text-indent), and created a page for[-webkit-box-reflect](https://developer.mozilla.org/en/CSS/-webkit-box-reflect).**Nickolay Ponomarev**created[Mutation events](https://developer.mozilla.org/en/DOM/Mutation_events), and expanded and clarified[error](https://developer.mozilla.org/en/DOM/DOM_event_reference/error)in the DOM event reference.**Florian Scholz**created a page for[window.navigator.connection](https://developer.mozilla.org/en/DOM/window.navigator.connection), added compatibility tables to MathML[mfrac](https://developer.mozilla.org/en/MathML/Element/mfrac),[mfenced](https://developer.mozilla.org/en/MathML/Element/mfenced), and[mglyph](https://developer.mozilla.org/en/MathML/Element/mglyph), and updated vendor neutrality and browser compatibility on 17 MathML elements.**Eric Shepherd**created a page for[XMLHttpRequestEventTarget](https://developer.mozilla.org/en/DOM/XMLHttpRequestEventTarget), added a section on convenience functions to[Touch events](https://developer.mozilla.org/en/DOM/Touch_events), and added an example of using a timeout to[Using HTMLHttpRequest](https://developer.mozilla.org/en/DOM/XMLHttpRequest/Using_XMLHttpRequest).**Caesar Shinas**added IE compatibility to[Using media queries from code](https://developer.mozilla.org/en/CSS/Using_media_queries_from_code)[and][MediaQueryList](https://developer.mozilla.org/en/DOM/MediaQueryList).**Wes**expanded[Touch events](https://developer.mozilla.org/en/DOM/Touch_events)to cover handling clicks and second touches.**Ziyunfei**translated or updated translations for something like a bazillion Chinese pages.

## Mozilla technology docs

- A number of people contributed to
[Building B2G for Samsung Galaxy S2](https://developer.mozilla.org/en/Mozilla/Boot_to_Gecko/Building_B2G_for_Samsung_Galaxy_S2), including**Ben Adida**,**Dietrich Ayala**,**John Hammink**,**Tobias Renz**,**Philipp von Weitershausen**, and**Zbigniew Braniecki**. **Will Bamberg**created[Bootstrapping BrowserID](https://developer.mozilla.org/en/BrowserID/Bootstrapping_BrowserID).**Ian Bicking**documented the ‘install’ and ‘uninstall’ events in

[navigator.mozApps.mgmt.addEventListener](https://developer.mozilla.org/en/Apps/Apps_JavaScript_API/navigator.mozApps.mgmt.addEventListener)and added a code example to[navigator.mozApps.mgmt.removeEventListener](https://developer.mozilla.org/en/Apps/Apps_JavaScript_API/navigator.mozApps.mgmt.removeEventListener).**Dan Callahan**created a[BrowserID Glossary](https://developer.mozilla.org/en/BrowserID/Glossary), revamped the main[BrowserID](https://developer.mozilla.org/en/BrowserID)page, and updated the[BrowserID FAQ](https://developer.mozilla.org/en/BrowserID/FAQ).**Luke Crouch**started documenting Kuma, the new wiki platform that MDN will be moving to soon:[Getting started with Kuma](https://developer.mozilla.org/Project:en/Getting_started_with_Kuma)and[Introduction to KumaScript](https://developer.mozilla.org/Project:en/Introduction_to_KumaScript).**Malini Das**added several function definitions to[Marionette](https://developer.mozilla.org/en/Marionette/Marionette)and added a section on running tests via make to Marionette[Running tests](https://developer.mozilla.org/en/Marionette/Running_Tests).**Fabrice Desré**and**Reuben Morais**updated the code examples in

[Getting started with apps](https://developer.mozilla.org/en/Apps/Getting_Started).**Mike Conley**documented how to use[Thunderbird Filelink providers](https://developer.mozilla.org/en/Thunderbird/Filelink_Providers).**Mark Giffin**updated[Apps manifest](https://developer.mozilla.org/en/Apps/Manifest)and the[Apps JavaScript API](https://developer.mozilla.org/en/Apps/Apps_JavaScript_API).**Jeff Griffiths**revamped the[Boot to Gecko](https://developer.mozilla.org/en/Mozilla/Boot_to_Gecko)landing page and created[Using Gaia using Firefox Nightly](https://developer.mozilla.org/en/Mozilla/Boot_to_Gecko/Running_Gaia_using_Firefox_Nightly).**Joliclic**added a section on returned values to[Declaring and calling functions](https://developer.mozilla.org/en/Mozilla/js-ctypes/Using_js-ctypes/Declaring_and_calling_functions)in[Using js-ctypes](https://developer.mozilla.org/en/Mozilla/js-ctypes/Using_js-ctypes).**Geoff Lankow**updated[nsIFile](https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIFile)based on its merger with[nsILocalFile](https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsILocalFile)in Gecko 14.**Philipp von Weitershausen**created[Writing a web app](https://developer.mozilla.org/en/Mozilla/Boot_to_Gecko/Writing_a_web_app)for Boot to Gecko,and updated

Building B2G for Samsung Nexus S[Setting up the Boot to Gecko build environment](https://developer.mozilla.org/en/Mozilla/Boot_to_Gecko/Setting_Up_Boot_to_Gecko_Build_Environment).

## Mozilla project docs

**Joel Maher**added a section on Mochitest-Robocop to[Mozilla automated testing](https://developer.mozilla.org/en/Mozilla_automated_testing).**Pc.wit.tt**created[Rebranding SpiderMonkey (1.8.5)](https://developer.mozilla.org/En/SpiderMonkey/Build_Documentation/Rebranding_SpiderMonkey_(1.8.5))[.]**Hassadee Pimsuwan**added Thai to the list of[MDN translations](https://developer.mozilla.org/Project:en/Localization_Projects)[.]

Translators are also needed for Spanish, German, Greek, Russion, traditional Chinese, Hebrew, and Romanian.**Thierry Régagnon**improved a number of the MDN templates for the French translation.

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.

## One comment

4esn0kApril 27th, 2012 at 20:47