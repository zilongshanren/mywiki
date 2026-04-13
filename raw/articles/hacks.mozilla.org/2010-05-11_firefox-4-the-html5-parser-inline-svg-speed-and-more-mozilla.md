---
title: 'Firefox 4: the HTML5 parser – inline SVG, speed and more – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2010/05/firefox-4-the-html5-parser-inline-svg-speed-and-more/
author: Christopher Blizzard
published: '2010-05-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post from Henri Sivonen, who has been working on Firefox’s new HTML5 parser. The HTML parser is one of the most complicated and sensitive pieces of a browser. It controls how your HTML source is turned into web pages and as such changes to it are rare and need to be well-tested. While most of Gecko has been rebuilt since its initial inception in the late 90s, the parser was one of the stand-outs as being “original.” This replaces that code with a new parser that’s faster, compliant with the new HTML5 standard and enables a lot of new functionality as well.*

A project to replace Gecko’s old HTML parser, dating from 1998, has been ongoing for some time now. The parser was just turned on by default on the trunk, so you can now try it out by simply [downloading a nightly build](http://nightly.mozilla.org/) without having to flip any configuration switch.

There are four main things that improve with the new HTML5 parser:

- You can now use SVG and MathML inline in HTML5 pages, without XML namespaces.
- Parsing is now done off Firefox’s main UI thread, improving overall browser responsiveness.
- It’s improved the speed of
`innerHTML`

calls by about 20%. - With the landing of the new parser we’ve fixed
[dozens of long-standing parser related bugs](https://bugzilla.mozilla.org/buglist.cgi?status_whiteboard_type=substring&status_whiteboard=[fixed%20by%20the%20HTML5%20parser]&resolution=FIXED).

[Try the demo with a](http://hsivonen.iki.fi/test/moz/html5-hacks-demo.html) [Firefox Nightly](http://nightly.mozilla.org) or another HTML5-ready browser. It should look like this:

**What Is It?**

The HTML5 parser in Gecko turns a stream of bytes into a DOM tree according to the [HTML5 parsing algorithm](http://www.whatwg.org/specs/web-apps/current-work/multipage/tokenization.html).

HTML5 is the first specification that tells implementors, in detail, how parse HTML. Before HTML5, HTML specifications didn’t say how to turn a stream of bytes into a DOM tree. In theory, HTML before HTML5 was supposed to be defined in terms of SGML. This implied a certain relationship between the source of valid HTML documents and the DOM. However, parsing wasn’t well-defined for invalid documents (and Web content most often isn’t valid HTML4) and there are SGML constructs that were in theory part of HTML but that in reality popular browsers didn’t implement.

The lack of a proper specification led to browser developers filling in the blanks on their own and reverse engineering the browser with the largest market share (first Mosaic, then Netscape, then IE) when in doubt about how to get compatible behavior. This led to a lot of unwritten common rules but also to different behavior across browsers.

The HTML5 parsing algorithm standardizes well-defined behavior that browsers and other applications that consume HTML can converge on. By design, the HTML5 parsing algorithm is suitable for processing existing HTML content, so applications don’t need to continue maintaining their legacy parsers for legacy content. Concretely, in the trunk nightlies, the HTML5 parser is used for all `text/html`

content.

**How Is It Different?**

The HTML5 parsing algorithm has two major parts: tokenization and tree building. Tokenization is the process of splitting the source stream into tags, text, comments and attributes inside tags. The tree building phase takes the tags and the interleaving text and comments and builds the DOM tree. The tokenization part of the HTML5 parsing algorithm is closer to what Internet Explorer does than what Gecko used to do. Internet Explorer has had the majority market share for a while, so sites have generally been tested not to break when subjected to IE’s tokenizer. The tree building part is close to what WebKit does already. Of the major browser engines WebKit had the most reasonable tree building solution prior to HTML5.

Furthermore, the new HTML5 parser parses network streams off the main thread. Traditionally, browsers have performed most tasks on the main thread. Radical changes like off-the-main-thread parsing are made possible by the more maintainable code base of the HTML5 parser compared to Gecko’s old HTML parser.

**What’s In It for Web Developers?**

The changes mentioned above are mainly of interest to browser developers. A key feature of the HTML5 parser is that you don’t notice that anything has changed.

However, there is one big new Web developer-facing feature, too: inline MathML and SVG. HTML5 parsing liberates MathML and SVG from XML and makes them available in the main file format of the Web.

This means that you can include typographically sophisticated math in your HTML document without having to recast the entire document as XHTML or, more importantly, without having to retrofit the software that powers your site to output well-formed XHTML. For example, you can now include the solution for quadratic equations inline in HTML:

```
```

Likewise, you can include scalable inline art as SVG without having to recast your HTML as XHTML. As screen sized and pixel densities become more varied, making graphics look crisp at all zoom levels becomes more important. Although it has previously been possible to use SVG graphics in HTML documents by reference (using the `object`

element), putting SVG inline is more convenient in some cases. For example, an icon such as a warning sign can now be included inline instead of including it from an external file.

```
```

Make yourself a page that starts with `<!DOCTYPE html>`

and put these two pieces of code in it and it should work with a new nightly.

In general, if you have a piece of MathML or SVG as XML, you can just copy and paste the XML markup inline into HTML (omitting the XML declaration and the doctype if any). There are two caveats: The markup must not use namespace prefixes for elements (i.e. no `svg:svg`

or `math:math`

) and the namespace prefix for the XLink namespace has to be `xlink`

.

In the MathML and SVG snippits above you’ll see that the inline MathML and SVG pieces above are more HTML-like and less crufty than merely XML pasted inline. There are no namespace declarations and unnecessary quotes around attribute values have been omitted. The quote omission works, because the tags are tokenized by the HTML5 tokenizer—not by an XML tokenizer. The namespace declaration omission works, because the HTML5 tree builder doesn’t use attributes looking like namespace declarations to assign MathMLness or SVGness to elements. Instead, `<svg>`

establishes a scope of elements that get assigned to the SVG namespace in the DOM and `<math>`

establishes a scope of elements that get assigned to the MathML namespace in the DOM. You’ll also notice that the MathML example uses named character references that previously haven’t been supported in HTML.

Here’s a quick summary of inline MathML and SVG parsing for Web authors:

`<svg>`

…`</svg>`

is assigned to the SVG namespace in the DOM.`<math>`

…`</math>`

is assigned to the MathML namespace in the DOM.`foreignObject`

and`annotation-xml`

(an various less important elements) establish a nested HTML scope, so you can nest SVG, MathML and HTML as you’d expect to be able to nest them.- The parser case-corrects markup so
`<SVG VIEWBOX='0 0 10 10'>`

works in HTML source. - The DOM methods and CSS selectors behave case-sensitively, so you need to write your DOM calls and CSS selectors using the canonical case, which is camelCase for various parts of SVG such as
`viewBox`

. - The syntax
`<foo/>`

opens and immediately closes the`foo`

element if it is a MathML or SVG element (i.e. not an HTML element). - Attributes are tokenized the same way they are tokenized in HTML, so you can omit quotes in the same situations where you can omit quotes in HTML (i.e. when the attribute value is not the empty string and does not contain whitespace,
`"`

,`'`

,```

,`<`

,`=`

, or`>`

). **Warning:**the two above features do not combine well due to the reuse of legacy-compatible HTML tokenization. If you omit quotes on the last attribute value, you must have a space before the closing slash.`<circle fill=green />`

is OK but`<circle fill=red/>`

is not.- Attributes starting with
`xmlns`

have*absolutely no effect*on what namespace elements or attributes end up in, so you don’t need to use attributes starting with`xmlns`

. - Attributes in the XLink namespace must use the prefix
`xlink`

(e.g.`xlink:href`

). - Element names must not have prefixes or colons in them.
- The content of SVG
`script`

elements is tokenized like they are tokenized in XML—not like the content of HTML`script`

elements is tokenized. - When an SVG or MathML element is open
`<![CDATA[`

…`]]>`

sections work the way they do in XML. You can use this to hide text content from older browsers that don’t support SVG or MathML in`text/html`

. - The MathML named characters are available for use in named character references everywhere in the document (also in HTML content).
- To deal with legacy pages where authors have pasted partial SVG fragments into HTML (who knows why) or used a
`<math>`

tag for non-MathML purposes, attempts to nest various common HTML elements as children of SVG elements (without`foreignObject`

) will immediately break out of SVG or MathML context. This may make some typos have surprising effects.

## 66 comments

jpvincentMay 11th, 2010 at 09:23jngMay 11th, 2010 at 10:35voidmindMay 11th, 2010 at 10:00Christopher BlizzardMay 17th, 2010 at 09:39DanielMay 11th, 2010 at 10:37Doug SchepersMay 11th, 2010 at 10:48Henri SivonenMay 11th, 2010 at 10:50SilverWaveMay 18th, 2010 at 09:42BorisMay 18th, 2010 at 09:59SilverWaveMay 18th, 2010 at 10:36Lars GuntherMay 11th, 2010 at 11:20Brian HermanMay 11th, 2010 at 13:34ALanMay 11th, 2010 at 14:09pascalMay 11th, 2010 at 14:34Jeff WaldenMay 11th, 2010 at 14:41AdamMay 11th, 2010 at 15:25Hans WurestMay 11th, 2010 at 17:12SilverWaveMay 11th, 2010 at 20:40voracityMay 12th, 2010 at 01:04pawelMay 12th, 2010 at 02:59Henri SivonenMay 12th, 2010 at 06:23A. DavisMay 12th, 2010 at 06:49A. DavisMay 12th, 2010 at 06:51Henri SivonenMay 12th, 2010 at 07:13Lars GuntherMay 12th, 2010 at 08:36Lars GuntherMay 12th, 2010 at 08:39Henri SivonenMay 12th, 2010 at 10:39Lars GuntherMay 12th, 2010 at 13:08marcoosMay 12th, 2010 at 13:11Brad NeubergMay 12th, 2010 at 17:08Brad NeubergMay 12th, 2010 at 17:10mike503May 13th, 2010 at 12:19BorisMay 14th, 2010 at 00:14SilverWaveMay 14th, 2010 at 02:58Henri SivonenMay 14th, 2010 at 01:37Michael NewtonMay 14th, 2010 at 15:09Darren GovoniMay 15th, 2010 at 23:40BorisMay 17th, 2010 at 15:20Darren GovoniMay 17th, 2010 at 19:42davidMay 18th, 2010 at 12:06Henri SivonenMay 18th, 2010 at 23:27SteveJune 5th, 2010 at 12:16Ant GrayJune 16th, 2010 at 14:54Guillermo AnayaJune 25th, 2010 at 02:18Tim NiilerSeptember 7th, 2010 at 15:25mattSeptember 7th, 2010 at 17:45voidmindSeptember 7th, 2010 at 18:18Zach HauriSeptember 8th, 2010 at 18:54AlexOctober 5th, 2010 at 17:39WebManWalkingOctober 29th, 2010 at 14:15WebManWalkingOctober 29th, 2010 at 14:57BorisOctober 30th, 2010 at 19:14WebManWalkingNovember 2nd, 2010 at 07:54BorisNovember 2nd, 2010 at 08:25Jukka K. KorpelaMarch 9th, 2011 at 10:53BorisMarch 9th, 2011 at 16:06ybochatayAugust 29th, 2011 at 01:53