---
title: CSS Variables in Firefox Nightly – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/12/css-variables-in-firefox-nightly/
author: Chris Heilmann
published: '2013-12-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As reported by [Cameron McCormack](http://mcc.id.au/blog/2013/12/variables), Firefox Nightly (version 29) now supports [CSS variables](http://dev.w3.org/csswg/css-variables/). You can get a quick overview in this [short screencast](http://www.youtube.com/watch?v=AYCYzSC4qFU):

You can define variables in a context with a `var-`

prefix and then implement them using the `var()`

instruction. For example:

```
:root {
var-companyblue: #369;
var-lighterblue: powderblue;
}
h1 {
color: var(companyblue);
}
h2 {
color: var(lighterblue);
}
```

```
```# Header on page

## Subheader on page


This defines the two variables `companyblue`

and `lighterblue`

for the root element of the document which results in ([you can try it here](http://jsfiddle.net/codepo8/rrmWV/1/) using [Firefox Nightly](http://nightly.mozilla.org/)):

![](../../assets/d3acaf76d6157a3c.jpeg)


Variables are scoped, which means you can overwrite them:

```
:root {
var-companyblue: #369;
var-lighterblue: powderblue;
}
.partnerbadge {
var-companyblue: #036;
var-lighterblue: #cfc;
}
h1 {
color: var(companyblue);
}
h2 {
color: var(lighterblue);
}
```

```
```# Header on page

## Subheader on page

# Header on page

## Subheader on page


Using these settings, headings inside an element with a class of `partnerbadge`

will now [get the other blue settings](http://jsfiddle.net/codepo8/rrmWV/2):

![](../../assets/b93d9b909457f997.jpeg)


Variables can be any value you want to define and you can use them like any other value, for example inside a `calc()`

calculation. You can also reset them to other values, for example inside a media query. [This example](http://jsfiddle.net/codepo8/rrmWV/3) shows many of these possibilities.

```
:root {
var-companyblue: #369;
var-lighterblue: powderblue;
var-largemargin: 20px;
var-smallmargin: calc(var(largemargin) / 2);
var-borderstyle: 5px solid #000;
var-headersize: 24px;
}
.partnerbadge {
var-companyblue: #036;
var-lighterblue: #369;
var-headersize: calc(var(headersize)/2);
transition: 0.5s;
}
@media (max-width: 400px) {
.partnerbadge {
var-borderstyle: none;
background: #eee;
}
}
/* Applying the variables */
body {font-family: 'open sans', sans-serif;}
h1 {
color: var(companyblue);
margin: var(largemargin) 0;
font-size: var(headersize);
}
h2 {
color: var(lighterblue);
margin: var(smallmargin) 0;
font-size: calc(var(headersize) - 5px);
}
.partnerbadge {
padding: var(smallmargin) 10px;
border: var(borderstyle);
}
```

![](../../assets/11d886ae7eed524d.jpeg)


Try resizing the window to less than 400 pixels to see the mediaQuery change in action.

An initial implementation of CSS Variables has just landed in Firefox Nightly, which is currently at version 29 and after the February 3 merge, in Firefox Aurora. There are still a few parts of the specification which still need to be supported before the can go into the release cycle of Firefox Beta and Firefox. Cameron has the details on that:

The only part of the specification that has not yet been implemented is the

`CSSVariableMap`

part, which provides an object that behaves like an ECMAScript`Map`

, with`get`

,`set`

and other methods, to get the values of variables on a`CSSStyleDeclaration`

. Note however that you can still get at them in the DOM by using the`getPropertyValue`

and`setProperty`

methods, as long as you use the full property names such as`"var-theme-colour-1"`

.The work for this feature was done in

[bug 773296], and my thanks to[David Baron]for doing the reviews there and to[Emmanuele Bassi]who did some initial work on the implementation. If you encounter any problems using the feature, please[file a bug]!

For now, have fun playing with CSS variables in Nightly and tell us about issues you find.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 46 comments

BrandonDecember 15th, 2013 at 09:29Chris HeilmannDecember 15th, 2013 at 12:06Sebastian ZartnerJanuary 8th, 2014 at 06:15TransDecember 15th, 2013 at 10:13Chris HeilmannDecember 15th, 2013 at 12:06Brian KardellDecember 15th, 2013 at 12:51m_golDecember 15th, 2013 at 13:33dougDecember 15th, 2013 at 11:42Tin Aung LinDecember 15th, 2013 at 11:54Steve vDecember 15th, 2013 at 11:58Chris HeilmannDecember 15th, 2013 at 12:03Moeed MohammadDecember 15th, 2013 at 13:36Chris HeilmannDecember 15th, 2013 at 16:21Robert O’CallahanDecember 15th, 2013 at 17:34m_golDecember 15th, 2013 at 20:55cokeboys_run_nyDecember 15th, 2013 at 11:56Chris HeilmannDecember 15th, 2013 at 12:04Robert O’CallahanDecember 15th, 2013 at 17:33mattDecember 15th, 2013 at 13:17Moeed MohammadDecember 15th, 2013 at 13:34Chris HeilmannDecember 15th, 2013 at 16:22Robert O’CallahanDecember 15th, 2013 at 17:31BastianDecember 15th, 2013 at 13:41DougDecember 15th, 2013 at 14:42BastianDecember 15th, 2013 at 23:49m_golDecember 17th, 2013 at 10:01BastianDecember 17th, 2013 at 10:19marc fawziDecember 15th, 2013 at 16:07Chris HeilmannDecember 15th, 2013 at 16:19Marc FawziDecember 15th, 2013 at 16:47AlexDecember 15th, 2013 at 18:57m_golDecember 15th, 2013 at 20:50pokeDecember 15th, 2013 at 20:42JérémyDecember 16th, 2013 at 01:10Niloy MondalDecember 15th, 2013 at 23:28TimDecember 16th, 2013 at 12:12l2aelbaDecember 16th, 2013 at 01:04Brian KnappDecember 16th, 2013 at 16:35Robert Nyman [Editor]December 17th, 2013 at 04:19absDecember 16th, 2013 at 18:52Vishnu HaridasDecember 19th, 2013 at 10:06Alex BellDecember 19th, 2013 at 11:37David BaughmanDecember 19th, 2013 at 12:51DanielDecember 20th, 2013 at 08:11Jonathan PratesDecember 28th, 2013 at 13:39AlexDecember 30th, 2013 at 06:59