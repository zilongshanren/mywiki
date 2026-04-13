---
title: Results of the Fall 2012 MDN virtual doc sprint – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/12/results-of-the-fall-2012-mdn-virtual-doc-sprint/
author: Janet Swisher
published: '2012-12-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Over the weekend of November 30 to December 2, a hardy band of MDN contributors came together virtually (via IRC and etherpad) to work on improving documentation on MDN for Web standards and for Mozilla’s open technology and the project itself. Below are the highlights of the weekend’s activities.

## Web standards docs

**Saurabh Anand**added browser compatibility info to five CSS properties (in addition to creating a screencast! — see below).**Fred Bourgeon**translated, updated, or fixed a bunch of CSS articles in French (including fixing the article structure and property tables for*all*CSS reference articles in French), and also improved[CSS value definition syntax](https://developer.mozilla.org/en-US/docs/CSS/Value_definition_syntax)in English.**Marc-Aurèle Darche**finalized the “Storage Limits” section of[IndexedDB](https://developer.mozilla.org/en-US/docs/IndexedDB#Storage_limits); added a note to the type of key to be passed to the[IDBObjectStore delete method](https://developer.mozilla.org/en-US/docs/IndexedDB/IDBObjectStore#delete%28%29); extensively rewrote and added example code to[Using files from web applications](https://developer.mozilla.org/en-US/docs/Using_files_from_web_applications); and added a long example to[Using IndexedDB](https://developer.mozilla.org/en-US/docs/IndexedDB/Using_IndexedDB).**Ethertank**performed huge amount of cleanup of markup and links across a wide range of articles, including HTML elements, JavaScript global objects, CSS properties, and miscellaneous other areas.**Ronan Jouchet**met up in person with Fred to make his first contributions to MDN, which included making the example in[:nth-child](https://developer.mozilla.org/en-US/docs/CSS/:nth-child#Odd_Selector_Example)a live example, and adding live examples to[:enabled](https://developer.mozilla.org/en-US/docs/CSS/:enabled)and[contextmenu](https://developer.mozilla.org/en-US/docs/HTML/Global_attributes#attr-contextmenu), the latter based on code that**Vikash Agrawal**wrote last summer. And he reported a[bug in the live example feature](https://bugzilla.mozilla.org/show_bug.cgi?id=817344).**Jérémie Pationnier**added articles for eight SVG attributes, and added an example to[feDiffuseLighting](https://developer.mozilla.org/en-US/docs/SVG/Element/feDiffuseLighting).**Jean-Yves Perrier**drafted an article on[Using CSS variables](https://developer.mozilla.org/en-US/docs/CSS/Using_CSS_variables).**Angel Fernando Quiroz Campos**translated[Using audio and video with HTML5](https://developer.mozilla.org/en-US/docs/Usando_audio_y_video_con_HTML5)into Spanish.**Brett Zamir**added shim code to[String](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/String/fromCharCode)and[fromCharCode](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/String/fromCharCode); and moved String and Array generic methods from[New in JavaScript 1.6](https://developer.mozilla.org/en-US/docs/JavaScript/New_in_JavaScript/1.6)to their respective articles.

## Mozilla technology and project docs

**Saurabh Anand**created a[screencast about building Firefox on Ubuntu](https://developer.mozilla.org/en-US/docs/User:teoli/TestPopcorn), and remixed it with Mozilla Popcorn; and drafted[Compiling Firefox with Clang on Linux](https://developer.mozilla.org/en-US/docs/Compiling_Firefox_With_Clang_On_Linux).**Cortega**started translating[Firefox OS architecture](https://developer.mozilla.org/es/docs/Mozilla/Firefox_OS/Architecture)into Spanish.**Vladan Djeric**wrote an article on[Adding a new Telemetry probe](https://developer.mozilla.org/en-US/docs/Performance/Adding_a_new_Telemetry_probe).**Trevor Hobson**added his[MDN Interface Documentation Generator](https://github.com/trevorhobson/mdni)add-on (for XPCOM interfaces) to Github, and documented several`dev-doc-needed`

bugs.**Eric Shepherd**wrote an article on[Using the remote web console](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Debugging_on_Boot_to_Gecko/Using_the_Remote_Web_Console)with Firefox OS, and made various improvements to Debugger docs.**Andreas Wagner**created a Firefox[add-on to show the interfaces (XPCOM and DOM) documentation coverage on MDN](http://img443.imageshack.us/img443/9847/mdnidca.png)(with collaborative help from**Trevor Hobson**). The first draft implementation is[available on Github](https://github.com/wagnerand/mdnidca).**Fred Wang**updated[MathML torture test](https://developer.mozilla.org/en-US/docs/Mozilla_MathML_Project/MathML_Torture_Test)and a bunch of other MathML demos to use live example code, as well as quite a few other updates to[Mozilla MathML project](https://developer.mozilla.org/en-US/docs/Mozilla_MathML_Project).**Yoric**made significant improvements to[Contributing to the Mozilla codebase](https://developer.mozilla.org/en-US/docs/Introduction).

Many thanks to all who participated!

P.S. Look for “State of the Docs” posts to resume in 2013.

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.