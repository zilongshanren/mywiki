---
title: 'ES6 In Depth: An Introduction – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/04/es6-in-depth-an-introduction/
author: Jason Orendorff
published: '2015-04-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Welcome to *ES6 In Depth*! In this new weekly series, we’ll be exploring ECMAScript 6, the upcoming new edition of the JavaScript language. ES6 contains many new language features that will make JS more powerful and expressive, and we’ll visit them one by one in weeks to come. But before we start in on the details, maybe it’s worth taking a minute to talk about what ES6 is and what you can expect.

### What falls under the scope of ECMAScript?

The JavaScript programming language is standardized by ECMA (a standards body like W3C) under the name ECMAScript. Among other things, ECMAScript defines:

[Language syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar)– parsing rules, keywords, statements, declarations, operators, etc.[Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures)– boolean, number, string, object, etc.[Prototypes and inheritance](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)[The standard library](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)of built-in objects and functions –,`JSON`

,`Math`

,`Array`

methods[Object introspection methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object), etc.

What it doesn’t define is anything to do with HTML or CSS, or the [Web APIs](https://developer.mozilla.org/en-US/docs/Web/API), such as the DOM (Document Object Model). Those are defined in separate standards. ECMAScript covers the aspects of JS that are present not only in the browser, but also in non-browser environments such as [node.js](http://nodejs.org/).

### The new standard

Last week, the final draft of the ECMAScript Language Specification, Edition 6, was submitted to the Ecma General Assembly for review. What does that mean?

It means that this summer, **we’ll have a new standard for the core JavaScript programming language.**

This is big news. A new JS language standard doesn’t drop every day. The last one, ES5, happened back in 2009. The ES standards committee has been working on ES6 ever since.

ES6 is a major upgrade to the language. At the same time, your JS code will continue to work. ES6 was designed for maximum compatibility with existing code. In fact, many browsers already support various ES6 features, and implementation efforts are ongoing. This means all your JS code has *already* been running in browsers that implement some ES6 features! If you haven’t seen any compatibility issues by now, you probably never will.

### Counting to 6

The previous editions of the ECMAScript standard were numbered 1, 2, 3, and 5.

What happened to Edition 4? An ECMAScript Edition 4 was once planned—and in fact a ton of work was done on it—but it was eventually scrapped as too ambitious. (It had, for example, a sophisticated opt-in static type system with generics and type inference.)

ES4 was contentious. When the standards committee finally stopped work on it, the committee members agreed to publish a relatively modest ES5 and then proceed to work on more substantial new features. This explicit, negotiated agreement was called “Harmony,” and it’s why the ES5 spec contains these two sentences:

ECMAScript is a vibrant language and the evolution of the language is not complete. Significant technical enhancement will continue with future editions of this specification.


This statement could be seen as something of a promise.

### Promises resolved

ES5, the 2009 update to the language, introduced [ Object.create()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create),

[,](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty)

`Object.defineProperty()`

[getters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get)and

[setters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/set),

[strict mode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode), and the

[object. I’ve used all these features, and I like what ES5 did for the language. But it would be too much to say any of these features had a dramatic impact on the way I write JS code. The most important innovation, for me, was probably the new](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON)

`JSON`

[methods:](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)

`Array`

[,](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)

`.map()`

[, and so on.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)

`.filter()`

Well, ES6 is different. It’s the product of years of harmonious work. And it’s a treasure trove of new language and library features, the most substantial upgrade for JS *ever*. The new features range from welcome conveniences, like arrow functions and simple string interpolation, to brain-melting new concepts like proxies and generators.

ES6 will change the way you write JS code.

This series aims to show you how, by examining the new features ES6 offers to JavaScript programmers.

We’ll start with a classic “missing feature” that I’ve been eager to see in JavaScript for the better part of a decade. So join us next week for a look at ES6 iterators and the new `for-of`

loop.

## 7 comments

OlegApril 26th, 2015 at 04:28Jaydson GomesApril 26th, 2015 at 17:21Havi Hoffman [Editor]April 27th, 2015 at 15:17MatijaApril 30th, 2015 at 02:30Taylor JonesApril 28th, 2015 at 09:05Joshua JarmanMay 5th, 2015 at 13:43KevinMMay 5th, 2015 at 13:59