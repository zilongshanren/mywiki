---
title: ClassList in Firefox 3.6 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/01/classlist-in-firefox-3-6/
author: Paul Rouget
published: '2010-01-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This article was writt by Anthony Ricaud, French OpenWeb enthusiast.*

### Why you need classList

A dynamic web application usually needs visual feedback from its inner mechanism or needs to display different visual elements based on users’ actions.

To change the user interface easily, you can add/remove/edit elements through the DOM API (`document.createElement`

, `div.removeChild`

, `elt.style.color`

, …) but it’s easier to just update the elements’ `class`

attribute to change how they are displayed and styled by CSS.

Let’s take an example. Suppose you want to display a form with two modes: a *basic* mode, and an *expert* mode with extra options.

This can be done with CSS rules: each mode has its own class and set of CSS code.

```
#anexpertinput.basic {
display: none;
}
#anexpertinput.expert {
display: inline;
}
```

To dynamically change the classes of elements, you can use `element.className`

. However, you may want to add, remove, or toggle just one class. There used to be two ways to do this, by using a library or by writing complex code with regular expressions. There is now another way with the new HTML5 API called `classList`

, which is implemented in Firefox 3.6.

Let’s see how it can simplify your code and improve performance at the same time.

### The classList API

Here is an example to show you what the classList API looks like:

```
// By default, start without a class in the div:
```

### Demo

Let’s go back to our initial example of a form with both a basic and an expert mode – check out the [live demo](https://developer.mozilla.org/media/uploads/demos/p/a/paulrouget/8bfba7f0b6c62d877a2b82dd5e10931e/hacksmozillaorg-achi_1334270447_demo_package/classList/) to see it in action.

As you can see in the code below, you can switch between the two modes with one line of JavaScript.

```
``` Blablablablabla...


```
#box.expert > #help,
#box.expert > label[for="postpone"],
#box.expert > label[for="lang"] {
display: none;
}
```

See the [Mozilla documentation](https://developer.mozilla.org/en/DOM/element.classList) and the [HTML5 specification](http://www.whatwg.org/specs/web-apps/current-work/multipage/urls.html#domtokenlist-0) for more details on classList.

## Performance

Using the classList API is not only easier, it’s also more powerful. Take a look at [what we observed](https://developer.mozilla.org/media/uploads/demos/p/a/paulrouget/8bfba7f0b6c62d877a2b82dd5e10931e/hacksmozillaorg-achi_1334270447_demo_package/classList/) using Firefox 3.6.

## Interoperability

Since other browser vendors have not yet implemented the HTML5 classList API, you still need fallback code. You can use [this sample code](https://developer.mozilla.org/media/uploads/demos/p/a/paulrouget/8bfba7f0b6c62d877a2b82dd5e10931e/hacksmozillaorg-achi_1334270447_demo_package/classList/classList.js) as fallback.

To know more about the current implementation of classList in well-known JavaScript libraries, see:

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 16 comments

thinsoldierJanuary 29th, 2010 at 13:00shawneeJanuary 29th, 2010 at 13:11BorisJanuary 29th, 2010 at 13:12Edwin MartinJanuary 29th, 2010 at 13:27shawneeJanuary 29th, 2010 at 14:15BorisJanuary 29th, 2010 at 19:28Azat RazetdinovJanuary 31st, 2010 at 03:35Anthony RicaudFebruary 1st, 2010 at 10:42Paul RougetFebruary 1st, 2010 at 11:15BorisFebruary 1st, 2010 at 11:41WalterKFebruary 3rd, 2010 at 13:31nemoFebruary 4th, 2010 at 12:35austinJune 22nd, 2010 at 11:55cc youngJuly 18th, 2011 at 06:46