---
title: 'The Web Developer Toolbox: Raphaël – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/05/the-web-developer-toolbox-raphael/
author: Jeremie Patonnier
published: '2012-05-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the first of a series of articles dedicated to the useful libraries that all web developers should have in their toolbox. My intent is to show you what those libraries can do and help you to use them at their best. This first article is dedicated to the [Raphaël](http://raphaeljs.com/) library.

## Introduction

Raphaël is a library originally written by [Dmitry Baranovskiy](http://dmitry.baranovskiy.com/) and is now part of [Sencha Labs](http://www.senchalabs.org/).

The goal of this library is to simplify work with vector graphics on the Web. Raphaël relies on the [SVG W3C Recommendation](http://www.w3.org/TR/SVG11/) (which is well supported in all modern browsers) and falls back to the Micrsoft VML language in order to address legacy versions of Internet Explorer. It also tries to harmonize some working issues across SVG implementations such as the SVG Animations. As a consequence, Raphaël is a very nice wrapper to produce consistent kick-ass graphics all over the Web.

## Basic usage

The library has [very good documentation](http://raphaeljs.com/reference.html) with many examples. Do not hesitate to use it extensively.

The following example will draw a simple red circle inside an HTML element with the id “myPaper”.

```
// the following example creates a drawing zone
// that is 100px wide by 100px high.
// This drawing zone is created at the top left corner
// of the #myPaper element (or its top right corner in
// dir="rtl" elements)
var paper = Raphael("myPaper", 100, 100);
// The circle will have a radius of 40
// and its center will be at coordinate 50,50
var c = paper.circle(50, 50, 40);
// The circle will be filled with red
// Note that the name of each element property
// follow the SVG recommendation
c.attr({
fill: "#900"
});
```


## Advanced usage

Despite the fact that Raphaël reduces the possibilities offered by SVG (mainly because of the VML fallback) it allows one to perform very advanced stuff:

- Advance Matrix transformation
- Advance event handler
- Cross browser animations
- Easy drag system
- Path intersection detection

Raphaël is also extensible through an extension system that allows you to build custom functions.

For example, here’s an extension to draw pie charts:

```
/**
* Pie method
*
* cx: x position of the rotating center of the pie
* cy: y position of the rotating center of the pie
* r : radius of the pie
* a1: angle expressed in degrees where the pie start
* a2: angle expressed in degrees where the pie end
*/
Raphael.fn.pie = function (cx, cy, r, a1, a2) {
var d,
flag = (a2 - a1) > 180;
a1 = (a1 % 360) * Math.PI / 180;
a2 = (a2 % 360) * Math.PI / 180;
d = [
// Setting the rotating axe of the pie
"M", cx, cy,
// Go to the start of the curve
"l", r * Math.cos(a1), r * Math.sin(a1),
// Drawing the curve to its end
"A", r, r, "0", +flag, "1",
cx + r * Math.cos(a2), cy + r * Math.sin(a2),
// Closing the path
"z"
];
return this.path(d.join(' '));
};
```


Note: In the example above, you have to be familiar with the SVG path syntax (Raphaël will convert it to the VML syntax under the hood), but once it’s done you can reuse it as any other Raphaël primitive. Look at this extension working to draw [a color wheel on jsFiddle](http://jsfiddle.net/5t93R/).

## Limits and precaution

If you are not familiar with SVG and/or want to support legacy MS Internet Explorer browsers, this tool is made for you. However, it’s a JavaScript library, which means that you have to know JavaScript to use it. You cannot use SVG and ask Raphaël to parse it and interpret it (to do that, it exists other libraries).

In terms of browser support, Raphaël gives you a large base. Raphaël currently supports Firefox 3.0+, Safari 3.0+, Chrome 5.0+, Opera 9.5+ and Internet Explorer 6.0+.

In fact, the only browser that can not take advantage of Raphaël is the native browser for Android 1.x and 2.x (and obviously many feature phone browsers). This is due to the fact that those browsers do not support any vector language. Android starts (partially) supporting SVG with Android 3.0 so take care if you want to work with all mobile devices.

## Conclusion

Raphaël was the first library to allow web designers and web developers to use SVG in the wild. If you want to write some nice applications without the need of the full SVG DOM API or if you have to support legacy browsers, this library will give you some power.

In conclusion, here are some cool usages of Raphaël:

[http://vlog.it/](http://vlog.it/)[http://type.method.ac/](http://type.method.ac/)[http://shape.method.ac/](http://shape.method.ac/)[http://www.nissanusa.com/leaf-electric-car/index](http://www.nissanusa.com/leaf-electric-car/index)[http://ilovedemocracy.arte.tv/fr/](http://ilovedemocracy.arte.tv/fr/)

## About
[
Jeremie Patonnier ](https://developer.mozilla.org)

Jeremie is a long time contributor/employee to the Mozilla Developer Network, and a professional web developer since 2000. He's advocating web standards, writing documentation and creating all sort of content about web technologies with the will to make them accessible to everybody.

## 4 comments

pdMay 15th, 2012 at 07:57Jeremie PatonnierMay 15th, 2012 at 08:54zoomclubMay 16th, 2012 at 23:52Jeremie PatonnierMay 17th, 2012 at 00:15