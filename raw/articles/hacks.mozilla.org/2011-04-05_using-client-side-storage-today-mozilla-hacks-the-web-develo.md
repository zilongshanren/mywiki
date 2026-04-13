---
title: Using client-side storage, today. – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/04/using-client-side-storage-today/
author: Louisremi
published: '2011-04-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I recently tried to store locally the content of a form to make it resilient to inadvertent tab closing and crashes. Here is what I learned about the different ways to achieve client-side storage.

### Cookies can crumble

Cookies are not a valid storage mean, as their size is limited to roughly 4000 characters (4KB) and act as a ball and chain, [slowing down the responsiveness](http://yuiblog.com/blog/2007/03/01/performance-research-part-3/) of websites. [localStorage](https://developer.mozilla.org/en/DOM/Storage#section_7) on the other hand, has been designed for that exact purpose, but [is not available in IE6, IE7 and Firefox3](http://caniuse.com/#feat=namevalue-storage).

### store.js to the rescue

The first task was thus to search for a [fallback solution](https://github.com/Modernizr/Modernizr/wiki/HTML5-Cross-browser-Polyfills/) (or *shim* or *polyfill*) available in those older browsers. It turns out that [store.js](https://github.com/marcuswestin/store.js), by [Marcus Westin](http://marcuswest.in/) ([@marcuswestin](http://twitter.com/#!/marcuswestin)), wraps localStorage and fallbacks together in a concise API, with a light file-size (2KB once minified and gzipped along with json2.js). Here is a short usage example:

### How does it work?

On Firefox2 and Firefox 3, it uses the globalStorage API, and on IE6 and IE7 it falls back to [userData behavior](http://msdn.microsoft.com/en-us/library/ms531424%28v=VS.85%29.aspx), which has two important limitations you should be aware of:

- storage is limited to 128KB (vs. 5-10MB for localStorage), that’s still a lot of text,
- storage is subject to a
*same folder policy*, meaning that pages in different folders should not be able to access the same stored items.

The second limitation can be really annoying, but it is possible to [work around it](https://github.com/louisremi/store.js) by loading the code in an iframe. This trick will likely be integrated into Marcus’ own code.

Although localStorage can only store strings, store.js uses the [JSON API](https://developer.mozilla.org/en/json#Using_JSON) to make it possible to store Javascript objects and arrays as well.

### Crash proof forms

With this script, I was able to build [Persival](https://github.com/louisremi/jquery.persival.js), a simple jQuery plugin that can watch a form for changes and persist the values immediately:

A more complex [demonstration page](http://louisremi.github.com/jquery.persival.js/) features the form people face when they want to report a bug affecting Firefox (you’ll see that it’s actually not as hard as it seems). If you start to fill the form, then close the tab and click on the same link again you should see the magic happening. A simple but welcome improvement to the user experience, isn’t it?

[Chris Heilmann](http://hacks.mozilla.org/author/cheilmann/) also demonstrated how client-side storage can be used to cache Web services data and maintain the state of a User Interface: [localStorage and how to use it](http://www.smashingmagazine.com/2010/10/11/local-storage-and-how-to-use-it/).

### Your turn

Persival is young but already yours, feel free to use it, learn from it and improve it.

Maybe there is a similar topic you would like to see covered in a next blog post? **Let us know!**

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 20 comments

MathiasApril 5th, 2011 at 08:04louisremiApril 5th, 2011 at 08:19MathiasApril 5th, 2011 at 08:31DextroApril 5th, 2011 at 08:51HemiltonApril 5th, 2011 at 13:58Mohamed JamaApril 5th, 2011 at 16:02Joss CrowcroftApril 5th, 2011 at 23:28louisremiApril 6th, 2011 at 02:13JazApril 6th, 2011 at 07:06louisremiApril 6th, 2011 at 07:25JazApril 6th, 2011 at 07:49louisremiApril 7th, 2011 at 01:20iLamaApril 6th, 2011 at 09:14louisremiApril 7th, 2011 at 01:16lobo_tuertoApril 6th, 2011 at 09:28Jonatan LittkeApril 7th, 2011 at 05:50louisremiApril 7th, 2011 at 06:00RyanApril 8th, 2011 at 10:25louisremiApril 8th, 2011 at 10:30RyanApril 8th, 2011 at 10:35