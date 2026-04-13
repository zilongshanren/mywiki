---
title: Introducing sphinx-js, a better way to document large JavaScript projects –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/07/introducing-sphinx-js-a-better-way-to-document-large-javascript-projects/
author: Erik Rose
published: '2017-07-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Until now, there has been no good tool for documenting large JavaScript projects. [JSDoc](http://usejsdoc.org/), long the sole contender, has some nice properties:

- A well-defined set of tags for describing common structures
- Tooling like the
[Closure Compiler](https://developers.google.com/closure/compiler/)which hooks into those tags

But the output is always a mere alphabetical list of everything in your project. JSDoc scrambles up and flattens out your functions, leaving new users to infer their relationships and mentally sort them into comprehensible groups. While you can get away with this for tiny libraries, it fails badly for large ones like [Fathom](https://hacks.mozilla.org/2017/04/fathom-a-framework-for-understanding-web-pages/), which has complex new concepts to explain. What I wanted for [Fathom’s manual](http://mozilla.github.io/fathom/) was the ability to organize it logically, intersperse explanatory prose with extracted docs, and add entire sections which are nothing but conceptual overview and yet link into the rest of the work.[1](https://hacks.mozilla.org#footnote-tutorials)

The Python world has long favored [Sphinx](http://www.sphinx-doc.org/en/stable/), a mature documentation tool with support for many languages and output formats, along with top-notch indexing, glossary generation, search, and cross-referencing. People have written entire books in it. Via plugins, it supports everything from Graphviz diagrams to YouTube videos. However, its JavaScript support has always lacked the ability to extract docs from code.

Now [sphinx-js](https://pypi.python.org/pypi/sphinx-js/) adds that ability, giving JavaScript developers the best of both worlds.

sphinx-js consumes standard JSDoc comments and tags—you don’t have to do anything weird to your source code. (In fact, it delegates the parsing and extraction to JSDoc itself, letting it weather future changes smoothly.) You just have Sphinx initialize a `docs`

folder in the root of your project, activate sphinx-js as a plugin, and then write docs to your heart’s content using simple [reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html). When it comes time to call in some extracted documentation, you use one of sphinx-js’s special directives, modeled after the Python-centric [autodoc](http://www.sphinx-doc.org/en/latest/ext/autodoc.html)’s mature example. The simplest looks like this:

```
.. autofunction:: linkDensity
```


That would go and find this function…

```
/**
* Return the ratio of the inline text length of the links in an element to
* the inline text length of the entire element.
*
* @param {Node} node - The node whose density to measure
* @throws {EldritchHorrorError|BoredomError} If the expected laws of the
* universe change, raise EldritchHorrorError. If we're getting bored of
* said laws, raise BoredomError.
* @returns {Number} A ratio of link length to overall text length: 0..1
*/
function linkDensity(node) {
...
}
```


…and spit out a nicely formatted block like this:

Sphinx begins to show its flexibility when you want to do something like adding a series of long examples. Rather than cluttering the source code around `linkDensity`

, the additional material can live in the reStructuredText files that comprise your manual:

```
.. autofunction:: linkDensity
Anything you type here will be appended to the function's description right
after its return value. It's a great place for lengthy examples!
```


There is also a sphinx-js directive for classes, either the ECMAScript 2015 sugared variety or the classic functions-as-constructors kind decorated with `@class`

. It can optionally iterate over class members, documenting as it goes. You can control ordering, turn private members on or off, or even include or exclude specific ones by name—all the well-thought-out corner cases Sphinx supports for Python code. Here’s a real-world example that shows a few truly public methods while hiding some framework-only “friend” ones:

```
.. autoclass:: Ruleset(rule[, rule, ...])
:members: against, rules
```


Going beyond the well-established Python conventions, sphinx-js supports references to same-named JS entities that would otherwise collide: for example, one `foo`

that is a static method on an object and another `foo`

that is an instance method on the same. It does this using a variant of JSDoc’s [namepaths](http://usejsdoc.org/about-namepaths.html). For example…

`someObject#foo`

is the instance method.`someObject.foo`

is the static method.- And
`someObject~foo`

is an inner member, the third possible kind of overlapping thing.

Because JSDoc is still doing the analysis behind the scenes, we get to take advantage of its understanding of these JS intricacies.

Of course, JS is a language of heavy nesting, so things can get deep and dark in a hurry. Who wants to type this full path in order to document `innerMember`

?

`some/file.SomeClass#someInstanceMethod.staticMethod~innerMember`


Yuck! Fortunately, sphinx-js indexes all such object paths using a suffix tree, so you can use any suffix that unambiguously refers to an object. You could likely say just `innerMember`

. Or, if there were 2 objects called “innerMember” in your codebase, you could disambiguate by saying `staticMethod~innerMember`

and so on, moving to the left until you have a unique hit. This delivers brevity and, as a bonus, saves you having to touch your docs as things move around your codebase.

With the maturity and power of Sphinx, backed by the ubiquitous syntactical conventions and proven analytic machinery of JSDoc, sphinx-js is an excellent way to document any large JS project. To get started, see [the readme](https://pypi.python.org/pypi/sphinx-js/). Or, for a large-scale example, see the Fathom documentation. A particularly juicy page is the [Rule and Ruleset Reference](https://mozilla.github.io/fathom/ruleset.html), which intersperses tutorial paragraphs with extracted class and function docs; its [source code](https://mozilla.github.io/fathom/_sources/ruleset.rst.txt) is available behind a link in its upper right, as for all such pages.

I look forward to your success stories and [bug reports](https://github.com/erikrose/sphinx-js/issues/new)—and to the coming growth of rich, comprehensibly organized JS documentation!

1JSDoc has

*, but they are little more than single HTML pages. They have no particular ability to cross-link with the rest of the documentation nor to call in extracted comments.*

[tutorials](http://usejsdoc.org/about-tutorials.html)## About
[
Erik Rose ](https://www.grinchcentral.com/)

Erik chips away at the barrier between human cognition and machine execution, through projects like DXR (search & static analysis on Mozilla codebases), Fathom (semantic extraction from web pages), parsers, new languages, and a whole mess of Python libraries.

## 15 comments

Rudolf OlahJuly 17th, 2017 at 08:57Carol WillingJuly 17th, 2017 at 19:36Erik RoseJuly 18th, 2017 at 06:44Roy SuttonJuly 17th, 2017 at 14:29Erik RoseJuly 18th, 2017 at 06:50Tom MacWrightJuly 20th, 2017 at 19:58Erik RoseJuly 21st, 2017 at 13:23VeeraJuly 18th, 2017 at 21:54ShrikeJuly 20th, 2017 at 02:47Erik RoseJuly 20th, 2017 at 06:57yahikoJuly 20th, 2017 at 04:02Erik RoseJuly 20th, 2017 at 07:03Axel RauschmayerJuly 20th, 2017 at 11:42Erik RoseJuly 20th, 2017 at 12:06Erik RoseJuly 20th, 2017 at 12:14