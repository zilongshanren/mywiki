---
title: State of the Docs, Feb. 1, 2012 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/02/state-of-the-docs-feb-1-2012/
author: Janet Swisher
published: '2012-02-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here are some of the changes to the [Mozilla Developer Network](https://developer.mozilla.org) site in the week and a half since the recent doc sprint.

## Infrastructure woes

We had a snafu for a few days last week when a server crashed in the middle of a move of the DOM reference hierarchy, causing many DOM reference pages to apparently disappear. That situation has now been fixed.

We have a recurring issue with the wiki software, where the syntax highlighting extension fails to load, causing an error message to appear in place of code examples. While we wait for a patch to be backported by the vendor, we have a script in place that detects this situation and corrects it. While you might still occasionally see those error messages, they should be less frequent and persistent than previously.

## Web standards docs

**Eric Bidelman**updated the[Mouse Lock API](https://developer.mozilla.org/en/API/Mouse_Lock_API).**Luke Crouch**added an Apache example to[Server-side access control](https://developer.mozilla.org/En/Server-Side_Access_Control).**fusionchess**added a compatibility workaround for the JavaScript[JSON global object](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/JSON).**Has Hillen**expanded the ARIA technique article on[Using the dialog role](https://developer.mozilla.org/en/ARIA/ARIA_Techniques/Using_the_dialog_role).**Burak Yigit Kaya**added a JSFiddle example to[HTML in XMLHttpRequest](https://developer.mozilla.org/en/HTML_in_XMLHttpRequest).**Gijs Kruitbosch**added a compatibility table to[window.frameElement](https://developer.mozilla.org/en/DOM/window.frameElement).**Jeremie Patonnier**updated[DOMParser](https://developer.mozilla.org/en/DOM/DOMParser)to cover parsing HTML fragments.**Eric Shepherd**documented the DOM[console](https://developer.mozilla.org/en/DOM/console)and related objects.**yyss**translated a number of pages into Japanese, related to[JavaScript typed arrays](https://developer.mozilla.org/en/JavaScript_typed_arrays),[full-screen mode](https://developer.mozilla.org/en/DOM/Using_full-screen_mode), WebGL, and writing forward-compatible websites.

## Mozilla-specific docs

**Wolfgang Germund**updated[nsIZioReader](https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIZipReader)and[nsIZipReaderCache](https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIZipReaderCache).**Sam Hanes**updated[Document Loading – From Load Start to Finding a Handler](https://developer.mozilla.org/en/Document_Loading_-_From_Load_Start_to_Finding_a_Handler). The diagram in this article still needs to be updated.**Anthony Hughes**documented[Merging the ESR branch](https://developer.mozilla.org/en/Mozmill_Tests/Branch_Merge/Merging_ESR_Branch).**Nickolay Ponomarev**added a list of mouse gesture events to[Gecko-specific DOM events](https://developer.mozilla.org/en/Gecko-Specific_DOM_Events).**Colby Russell**expanded[DOM Inspector internals](https://developer.mozilla.org/en/DOM_Inspector/Internals).**Eric Shepherd**beefed up the coverage of the[Web console](https://developer.mozilla.org/en/Tools/Web_Console).**Sid0**update the article on[Windows SDK versions](https://developer.mozilla.org/En/Windows_SDK_versions).

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.