---
title: 'Hidden Gems of HTML5: classList – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/01/hidden-gems-of-html5-classlist/
author: Chris Heilmann
published: '2012-01-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If you are a web developer, you surely must know how handy it is to dynamically change the class attribute on an element. The benefits this technique are quite a few:

- You leave any changes in the look and feel to the CSS
- You avoid having to loop lots of elements as you can allow CSS to do that job for you by assigning a class on a parent element
- You can trigger CSS transitions and avoid having to write your own animation
- And many more…

The issue with classes is that it is not too simple to work with because of their representation in the DOM. When you read out `className`

you get one string and you need to split it and use regex to find if a class was used and all kind of other annoyances. This is also why it is a very common interview questions for web developers to write a function to deal with classes.

Well, you might not be aware of it, but HTML has a very cool new way to deal with classes called [classList](https://developer.mozilla.org/en/DOM/element.classList). This makes it dead easy to add, remove, toggle and check for classes on an element – natively in your browser. You can play with it at [JSFiddle](http://jsfiddle.net/codepo8/xk6zh/):

The methods you have are all you really need:

`element.classList.add('foo')`

adds the class`foo`

to the element (if it already exists it does nothing)`element.classList.remove('foo')`

removes the class`foo`

from the element`element.classList.toggle('foo')`

alternatively adds and removes the class`foo`

from the element`element.classList.contains('foo')`

returns if the class is applied to the element or not`element.classList.toString()`

returns all the classes as a string (same as reading out`className`

)

The [browser support is very good](http://caniuse.com/#search=classList) with IE being the party pooper. However, there is a [polyfill by Eli Grey available](https://github.com/eligrey/classList.js) for you to use.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 21 comments

CalveinJanuary 30th, 2012 at 05:23Chris HeilmannJanuary 30th, 2012 at 05:33CalveinJanuary 30th, 2012 at 05:36GregJanuary 30th, 2012 at 06:07MTJanuary 30th, 2012 at 06:10migJanuary 30th, 2012 at 07:12MustafaJanuary 30th, 2012 at 05:24Chris HeilmannJanuary 30th, 2012 at 05:34MustafaJanuary 31st, 2012 at 13:48Joost ElferingJanuary 30th, 2012 at 05:46MotyarJanuary 30th, 2012 at 06:25MTJanuary 30th, 2012 at 07:47MTJanuary 30th, 2012 at 07:49RobJanuary 30th, 2012 at 07:53Chris HeilmannJanuary 30th, 2012 at 08:42louisremiJanuary 30th, 2012 at 08:22Brian BirtlesJanuary 30th, 2012 at 16:38Brian BirtlesJanuary 30th, 2012 at 16:40DrewJanuary 31st, 2012 at 10:35CourseworkMarch 15th, 2012 at 04:33samOctober 18th, 2012 at 14:41