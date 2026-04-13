---
title: Scroll snapping explained – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/09/scroll-snapping-explained/
author: Sebastian Zartner
published: '2015-09-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Have you ever tried to snap your page’s contents after scrolling? There are many JavaScript libraries out there providing this functionality. Here are a few examples:

[https://github.com/peachananr/purejs-onepage-scroll](https://github.com/peachananr/purejs-onepage-scroll)[http://wtm.github.io/jquery.snapscroll/](http://wtm.github.io/jquery.snapscroll/)[http://guidobouman.github.io/jquery-panelsnap/](http://guidobouman.github.io/jquery-panelsnap/)[http://alvarotrigo.com/fullPage/](http://alvarotrigo.com/fullPage/)

As this is a common use case related to page layout and behavior, the W3C has published a pure [CSS approach to scroll snapping](http://www.w3.org/TR/css-snappoints-1/).

CSS scroll snapping, (available since July’s [Firefox 39 release](https://hacks.mozilla.org/2015/06/trainspotting-firefox-39/)), allows you to control where to stop on an overflowing element when it’s scrolled. This lets you section your page into logical divisions and thus create smoother, easier-to-interact-with user interfaces. Touch devices in particular benefit from this feature, where it is easier for people to pan through pages instead of tapping through hierarchical structures.

## Image gallery

Image galleries are surely the most common use case for scroll snapping: Users can flip through the images, viewing one image at a time by swiping or scrolling the page. So let’s see how this can be achieved with the new properties:

`<pre>img {`


width: 200px;

}

.photoGallery {

width: 200px;

overflow: auto;

white-space: nowrap;

scroll-snap-points-x: repeat(100%);

scroll-snap-type: mandatory;

}

</pre>

The related HTML code looks like this:

`<pre><div class="photoGallery">`


<img src="img1.png"><img src="img2.png"><img src="img3.png">

</div>

</pre>

Here’s a live demo:

See the Pen [wKvYdK](http://codepen.io/potch/pen/wKvYdK/) by Potch ([@potch](http://codepen.io/potch)) on [CodePen](http://codepen.io).

The code above creates a simple image gallery with three images, which can be scrolled through horizontally.

In this case the size of the images and their containing `<div>`

are set to 200 pixels. The `overflow: auto;`

displays a scrollbar on clients that support it. `white-space: nowrap;`

serves to keep all images horizontally aligned. The definition “`<a href="https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-points-x" target="_blank">scroll-snap-points-x</a>: repeat(100%);`

” sets a repeated horizontal snap point at 100% of the viewport width of the container <div>, in this case at 200 pixel intervals. Setting `<a href="https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-points-x">scroll-snap-type</a>: mandatory;`

has the effect that snapping is forced. The viewport will always snap at a snap point, so the display will never stay in between two images.

## Item lists

You’ve probably seen plenty of online product pages listing different features with an image of each feature and a description next to it, or an interface displaying a series of user testimonials.

In these cases, scroll snapping lets you align the sections so that maximal display space is used.

`<pre>.features {`


width: 400px;

height: 250px;

padding: 0;

overflow: auto;

scroll-snap-type: proximity;

scroll-snap-destination: 0 16px;

}

.features > section {

clear: both;

margin: 20px 0;

scroll-snap-coordinate: 0 0;

}

img {

width: 50px;

height: 50px;

margin: 5px 10px;

float: left;

}

section:last-child {

margin-bottom: 60px;

}

</pre>

And here’s the related HTML code:

`<pre><div class="features">`


<section id="feature1">

<img src="feature1.png"/>

<p>Lorem ipsum...</p>

</section>

<section id="feature2">

<img src="feature2.png"/>

<p>Lorem ipsum...</p>

</section>

...

</div>

</pre>

Here’s a live demo:

See the Pen [NGWOjN](http://codepen.io/potch/pen/NGWOjN/) by Potch ([@potch](http://codepen.io/potch)) on [CodePen](http://codepen.io).

When you scroll within the example above, each feature section is positioned so that the top is aligned with the top of the viewport to display as much text as possible. This is achieved by applying `<a href="https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-coordinate" target="_blank">scroll-snap-coordinate</a>: 0 0;`

to the sections. The two zeros refer to the x and y coordinates of the element where it will snap to the container element. `<a href="https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-destination" target="_blank">scroll-snap-destination</a>: 0 16px;`

defines the offset position within the container element to which the inner elements should snap. In this case, that’s 16 pixels below the top of the container so that the text at top of the section has some margin at the top.

In addition to the properties currently defined within the [CSS Scroll Snap Points specification](http://www.w3.org/TR/css-snappoints-1/), Gecko implements the additional properties [scroll-snap-type-x](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-type-x) and [scroll-snap-type-y](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-type-y), for setting the snap type individually per axis. These long-hand properties may be added to the specification in the future.

Currently snap points can only be set through coordinates, either referring to the start edge of the container element or the ones within it. Sometimes this requires some calculation to set them at the right position. Future extensions to this feature may extend the functionality to be able to set snap points on the box model instead, which would make it easier to place them. There’s already a [discussion about this within the www-style mailing list](http://lists.w3.org/Archives/Public/www-style/2015Jul/0325.html).

Has this new functionality caught your interest? Then it’s time to give it a try! And if you don’t remember how to use the different properties, you can always refer to the [documentation on MDN](https://developer.mozilla.org/en-US/docs/tag/CSS%20Scroll%20Snap%20Points).

## 7 comments

JSeptember 2nd, 2015 at 12:27Sebastian ZartnerSeptember 2nd, 2015 at 22:55Šime VidasSeptember 2nd, 2015 at 20:20Sebastian ZartnerSeptember 5th, 2015 at 01:30Alexander GoncharovSeptember 7th, 2015 at 14:02Havi Hoffman [Editor]September 17th, 2015 at 11:27Wilson PageSeptember 10th, 2015 at 05:38