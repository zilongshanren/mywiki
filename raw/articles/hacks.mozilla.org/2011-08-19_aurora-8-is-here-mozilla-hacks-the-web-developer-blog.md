---
title: Aurora 8 is here – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/08/aurora8/
author: Louisremi
published: '2011-08-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Today we release Aurora Update 8. We’ve got even more HTML5 support, support for cross-origin textures in WebGL, support for insertAdjacentHTML() and reduced resource requirements for media elements.*

### Cross-origin WebGL textures

We disabled support for cross-origin textures in Firefox 5 due to [security concerns](http://hacks.mozilla.org/2011/06/cross-domain-webgl-textures-disabled-in-firefox-5/). You can now use cross-origin textures in Aurora Update 8, although servers that serve the images need to use [CORS headers](https://developer.mozilla.org/En/HTTP_access_control) to be sent with them.

### insertAdjacentHTML()

This is a method first implemented in Internet Explorer 4 and was added to the

HTML5 standard. This function allows you to insert HTML strings inside a document, just like the innerHTML property, but is more flexible and is [much faster](http://jsperf.com/insertadjacenthtml).


We expect that JavaScript libraries will quickly [adopt this](http://ejohn.org/blog/dom-insertadjacenthtml/) because it’s faster and vastly simplifies DOM manipulation code.

### Reduced memory usage

Media elements (<audio> and <video>) now use [fewer threads](https://bugzilla.mozilla.org/show_bug.cgi?id=592833) and [less memory](https://bugzilla.mozilla.org/show_bug.cgi?id=664341). This is part of our efforts to reduce overall memory consumption of Firefox and it is a welcome improvement as websites switch to using native media elements.

### Other changes

#### HTML

- The
`<a href="https://developer.mozilla.org/en/DOM/HTMLImageElement">HTMLImageElement</a>`

`crossOrigin`

property has been added. (see[bug 664299](https://bugzilla.mozilla.org/show_bug.cgi?id=664299)) - The
`<a href="https://developer.mozilla.org/en/DOM/HTMLSelectElement#add%28%29">HTMLSelectElement.add()</a>`

method now supports either an item or index of an item that the new item should be inserted before. Previously it only supported an item. (see[bug 666200](https://bugzilla.mozilla.org/show_bug.cgi?id=666200)) - The
constructor has been removed. No elements have implemented this interface since Firefox 4. (see`HTMLIsIndexElement`

[bug 666665](https://bugzilla.mozilla.org/show_bug.cgi?id=666665)and[bug 611352](https://bugzilla.mozilla.org/show_bug.cgi?id=611352)) - The HTML5 “context menu” feature (contextmenu attribute), which lets you add custom element specific items to native context menu, is now supported. (the implementation is still experimental awaiting changes in the specification, see
[bug 617528](https://bugzilla.mozilla.org/show_bug.cgi?id=617528))

#### DOM

- The
`<a href="https://developer.mozilla.org/en/DOM/Element.insertAdjacentHTML">insertAdjacentHTML</a>`

method has been implemented. (see[bug 613662](https://bugzilla.mozilla.org/show_bug.cgi?id=613662)) `<a href="https://developer.mozilla.org/en/DOM/BlobBuilder">BlobBuilder</a>`

now has a getFile() method that returns the content of the blob as a file (see[bug 669437](https://bugzilla.mozilla.org/show_bug.cgi?id=669437))- Event handling in nested <label>s has been fixed (see
[bug 646157](https://bugzilla.mozilla.org/show_bug.cgi?id=646157)) - Two bugs fixed when text insertion cursor is at the beginning of an editable text:
[bug 414526](https://bugzilla.mozilla.org/show_bug.cgi?id=414526)and[bug 442186](https://bugzilla.mozilla.org/show_bug.cgi?id=442186) `<a href="https://developer.mozilla.org/en/DOM/document.getSelection">document.getSelection()</a>`

now returns the same Selection object as`<a href="https://developer.mozilla.org/en/DOM/window.getSelection">window.getSelection()</a>`

, instead of*stringifying*it (see[bug 636512](https://bugzilla.mozilla.org/show_bug.cgi?id=636512))- the HTML5 selectionDirection property makes it possible to define the direction of the selection in an editable text (see
[bug 674558](https://bugzilla.mozilla.org/show_bug.cgi?id=674558)) - Range and Selection are now behaving according to their specification when splitText() and normalize() are used (see
[bug 191864](https://bugzilla.mozilla.org/show_bug.cgi?id=191864)) - Media elements now have a seekable() method that return a TimeRange object (see
[bug 462960](https://bugzilla.mozilla.org/show_bug.cgi?id=462960)) - crossOrigin property defaults to “Anonymous” when an invalid value is used (see
[bug 676413](https://bugzilla.mozilla.org/show_bug.cgi?id=676413))

#### CSS

`<a href="https://developer.mozilla.org/en/CSS/resolution">resolution</a>`

now accepts`<a href="https://developer.mozilla.org/en/CSS/number"><number></a>`

, not just`<a href="https://developer.mozilla.org/en/CSS/integer"><integer></a>`

values as per the specification. (see[bug 677642](https://bugzilla.mozilla.org/show_bug.cgi?id=677642))

#### Audio & Video

- New threading model for Audio and Video (see
[bug 592833](https://bugzilla.mozilla.org/show_bug.cgi?id=592833)) - Video thread stack size has been reduced (see
[bug 664341](https://bugzilla.mozilla.org/show_bug.cgi?id=664341))

#### Network

- Double quotes are no longer accepted as a delimiter for 2231/5987 encoding (see
[bug 651185](https://bugzilla.mozilla.org/show_bug.cgi?id=651185)) - Content-Disposition parser does not require presence of “=” anymore in parameters (see
[bug 670333](https://bugzilla.mozilla.org/show_bug.cgi?id=670333)) - Mixed-content is not allowed with WebSockets (see
[bug 662692](https://bugzilla.mozilla.org/show_bug.cgi?id=662692)) - Connection errors with WebSockets now trigger the onerror handler (see
[bug 676025](https://bugzilla.mozilla.org/show_bug.cgi?id=676025)) [WebSocket](https://developer.mozilla.org/en/WebSocket)API has been updated to the latest draft of the specification (see[bug 674890](https://bugzilla.mozilla.org/show_bug.cgi?id=674890),[bug 674527](https://bugzilla.mozilla.org/show_bug.cgi?id=674527)and[bug 674716](https://bugzilla.mozilla.org/show_bug.cgi?id=674716))- Script files are not any more downloaded when javascript has been disabled (see
[bug 668690](https://bugzilla.mozilla.org/show_bug.cgi?id=668690)) - DNS entries are now blacklisted when the first request failed (see
[bug 641937](https://bugzilla.mozilla.org/show_bug.cgi?id=641937))

#### WebGL

- Cross-domain textures can now be allowed with CORS approval (see
[bug 662599](https://bugzilla.mozilla.org/show_bug.cgi?id=662599)) - Cross-process rendering with Direct2d/Direct3d 10 (see
[bug 648484](https://bugzilla.mozilla.org/show_bug.cgi?id=648484))

#### MathML

- Support for the
`displaystyle`

attribute on the top-level`<a href="https://developer.mozilla.org/en/MathML/Element/math"><math></a>`

element has been added. - The interpretation of
*negative*rownumbers for the`align`

attribute on`<a href="https://developer.mozilla.org/en/MathML/Element/mtable"><mtable></a>`

has been corrected (see[bug 601436](https://bugzilla.mozilla.org/show_bug.cgi?id=601436)).

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 10 comments

mekalAugust 20th, 2011 at 10:27louisremiAugust 21st, 2011 at 14:58JasonAugust 22nd, 2011 at 11:43OrNotAugust 22nd, 2011 at 18:58louisremiAugust 23rd, 2011 at 01:56OrNotAugust 23rd, 2011 at 04:09NeoFaxAugust 24th, 2011 at 15:08JoseAugust 27th, 2011 at 06:08CindySeptember 20th, 2011 at 12:18Girish MonyOctober 24th, 2011 at 03:12