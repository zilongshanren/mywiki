---
title: State of the Docs, November 9, 2011 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/11/state-of-the-docs-november-9-2011/
author: Janet Swisher
published: '2011-11-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the first in a series of posts about new or recently improved content on MDN. This series will alternate with Wiki Wednesday posts, which will switch to every other week.

The purpose of this series is to highlight articles that have changed recently, as well as to recognize the contributors who did the work. This doesn’t include every change, just “significant” ones. Future posts may be a bit shorter, as they’ll cover only the two weeks since the previous “state of the docs” post.

## Web standards docs

**Jean-Yves Perrier** documented the [<bdi> element](http://developer.mozilla.org/en/HTML/Element/bdi). It allows inserting spans of text with unknown directionality, like text coming out of a database, in the middle of text with a known fixed directionality. He also updated the CSS [unicode-bidi ](http://developer.mozilla.org/en/CSS/unicode-bidi) property to describe the two new values: `isolate`

and `plaintext`

, which are used to implement correctly bi-directionality for each HTML element (including, but not only, <bdi>, <bdo>, <pre> and <textarea>).

Jean-Yves rewrote the docs for the CSS property [text-overflow](http://developer.mozilla.org/en/CSS/text-overflow), to account for the new extended two-value syntax and the new allowed string values, as well as adding new examples.

Jean-Yves also added pages for [columns](https://developer.mozilla.org/en/CSS/columns), updated [column-width](https://developer.mozilla.org/en/CSS/column-width) and [column-count](https://developer.mozilla.org/en/CSS/column-count), and [Using CSS multi-column layout](https://developer.mozilla.org/en/CSS3_Columns).

**Paul Irish** made a rash of updates:

<

ul>

[image-rendering](https://developer.mozilla.org/En/CSS/Image-rendering)for crisp-edges/optimize-contrast

[JSON.stringify()](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/JSON/stringify).

[node.contains()](https://developer.mozilla.org/en/DOM/Node.contains).

[getComputedStyle](https://hacks.mozilla.org/en)can get pseudo-element styles. Also it can be used from the window object.

[creating and triggering custom events](https://developer.mozilla.org/en/DOM/Creating_and_triggering_events)(which he had always wanted spelled out)

[table.insertRow()](https://developer.mozilla.org/en/DOM/table.insertRow).

**Kevin Lim** continues to improve the IndexedDB docs:

- Added code examples to
[IDBEnvironment](https://developer.mozilla.org/en/IndexedDB/IDBEnvironment)and[IDBIndex](https://developer.mozilla.org/en/IndexedDB/IDBIndex). - Updated
[IDBCount](https://developer.mozilla.org/en/IndexedDB/IDBCount). - Added prefix-handling code to several code examples.
- Beefed up basic concepts and best practices in
[IDBDatabase](https://developer.mozilla.org/en/IndexedDB/IDBDatabase),[IDBTransaction](https://developer.mozilla.org/en/IndexedDB/IDBTransaction), and[IDBIndex](https://developer.mozilla.org/en/IndexedDB/IDBIndex).

**fusionchess** added a code example to [Using files from web applications](https://developer.mozilla.org/en/Using_files_from_web_applications).

**Aaron Leventhal** updated the [ARIA](https://developer.mozilla.org/en/ARIA) page with lots of doc and resource links, and wrote new articles on:

[live regions](http://developer.mozilla.org/en/ARIA/Live_Regions)[how to file ARIA-related bugs](https://developer.mozilla.org/en/ARIA/How_to_file_ARIA-related_bugs)[examples](https://developer.mozilla.org/en/ARIA/examples)[alerts for accessible forms](https://developer.mozilla.org/en/Accessibility/Accessible_forms/alerts)[multipart labels for forms](https://developer.mozilla.org/en/aria/forms/Multipart_labels)[ARIA widgets](https://developer.mozilla.org/en/ARIA/widgets/overview)

If you’re interested in ARIA and accessibility, please help out with these docs. If you’re not an expert, you can help identify where there are gaps, or things that don’t make sense. Accessibility geeks might also be interested in the [free-aria Google Group](https://groups.google.com/forum/#!forum/free-aria).

### New pages!

- Initial documentation for the
[<frame>](https://developer.mozilla.org/en/HTML/element/frame)and[<frameset>](https://developer.mozilla.org/en/HTML/Element/frameset)HTML elements, by**avsaro**. [SVG as an image](https://developer.mozilla.org/en/SVG/SVG_as_an_Image)by**Dholbert**.[Responsive Web design](https://developer.mozilla.org/en/Web_Development/Responsive_Web_design), by Janet Swisher; if you know of good resources that are not listed there, please add them.[Scaling of SVG backgrounds](https://developer.mozilla.org/en/CSS/Scaling_of_SVG_backgrounds)and[Drawing DOM objects into a canvas](https://developer.mozilla.org/en/HTML/Canvas/Drawing_DOM_objects_into_a_canvas), by Eric Shepherd.

### Help wanted!

Want to write an article on CSS positioning? That is, how positioning properties for margins, padding, etc. work together. MDN does not have this topic covered yet. Or, if you’ve already written such an article, would you be willing to contribute it to MDN under a CC-BY-SA license?

Check out the MDN [Getting started](https://developer.mozilla.org/Project:en/Getting_started) page. If you have questions, drop into #devmo IRC channel on irc.mozilla.org, or post to the [dev.mdc](http://www.mozilla.org/about/forums/#dev-mdc) discussion forum.

## Mozilla-specific documentation

**Henri Sivonen** wrote about [HTML parser threading in Gecko](https://developer.mozilla.org/en/Gecko/HTML_parser_threading).

**jbeatty** improved [Patching a localization](https://developer.mozilla.org/en/Patching_a_Localization), [Create a new localization](https://developer.mozilla.org/en/Create_a_new_localization) and several other localization-related pages.

**Tom Schuster** added to the SpiderMonkey JS API reference for:

Eric Shepherd wrote up complete reference docs for the new [JavaScript Debugger API](https://developer.mozilla.org/en/SpiderMonkey/JS_Debugger_API_Reference). However, the [user guide for the Debugger API](https://developer.mozilla.org/en/SpiderMonkey/JS_Debugger_API_Guide) needs a lot of attention. We don’t have any examples at this point. A sample add-on that uses the API should be written, but even the JSAPI team hasn’t done one yet.

Firefox 8 was released on November 8, and [Firefox 8 for developers](https://developer.mozilla.org/en/Firefox_8_for_developers) is complete except for a few lower-priority items.

**decoder** created an article on [Testing with Linux on ARM architecture using QEMU](https://developer.mozilla.org/en/Developer_Guide/Virtual_ARM_Linux_environment).

**Jorge Villalobos** updated several pages of the [XUL School tutorial](https://developer.mozilla.org/en/XUL_School).

Eric Shepherd created an article for the Mozilla Developer Guide on [Getting documentation updated](https://developer.mozilla.org/En/Developer_Guide/Getting_documentation_updated).

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.

## One comment

Manuel StrehlNovember 10th, 2011 at 05:46