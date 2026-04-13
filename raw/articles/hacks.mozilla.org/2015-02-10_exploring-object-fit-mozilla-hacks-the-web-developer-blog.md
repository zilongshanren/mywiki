---
title: Exploring object-fit – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/02/exploring-object-fit/
author: Chris Mills
published: '2015-02-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

On web documents, a common problem concerns the display of different sized images (or videos) in the same place. Perhaps you are writing a dynamic gallery app that accepts user submissions. You can’t guarantee that everyone will upload images of exactly the same aspect ratio, so what do you do?

Letting the aspect ratio distort to fit the containing replaced element nearly always looks horrible. And doing some kind of dynamic cropping or resizing on the fly each time might be more work than you have the capability to implement. (For instance, maybe you’re working on a CMS and don’t have permission to edit anything except the page content.)

The [CSS Image Values and Replaced Content](http://dev.w3.org/csswg/css-images/) module provides properties called [object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit) — which solves such problems, and [object-position](https://developer.mozilla.org/en-US/docs/Web/CSS/object-position) — which sets the horizontal and vertical position of the content inside the element.

These elements have decent support across modern browsers (with the exception of IE). In this article we’ll look at a few examples of how they can be used.

Note: `object-fit`

works with SVG content, but the same effect can also be achieved by setting the `preserveAspectRatio=""`

attribute in the SVG itself.

## How do object-fit and object-position work?

You can successfully apply `object-fit`

to any replaced element, for example:

```
img {
height: 100px;
width: 100px;
object-fit: contain;
}
```

The five possible values of `object-fit`

are as follows:

`contain`

: The content (e.g. the image) will be resized so that it is fully displayed with intrinsic aspect ratio preserved, but still fits inside the dimensions set for the element.`fill`

: The content will expand to exactly fill the dimensions set for the element, even if this does break its aspect ratio.`cover`

: Preserves the aspect ratio of the content, but alters the width and height so that the content completely covers the element. The smaller of the two is made to fit the element exactly, and the larger overflows the element and is cropped.`none`

: Completely ignores any height or weight set on the element, and just uses the replaced element content’s intrinsic dimensions.`scale-down`

: The content is sized as if`none`

or`contain`

were specified, whichever would result in a smaller replaced element size.

`object-position`

works in exactly the same way as [background-position](https://developer.mozilla.org/en-US/docs/Web/CSS/background-position) does for background images; for example:

```
img {
height: 100px;
width: 100px;
object-fit: contain;
object-position: top 70px;
}
```

Percentages work, but they’re actually resolved against the excess available space — the difference between the element’s width & the replaced content’s final rendered width. So `object-position: 50% 50%`

(the default value) will always exactly center the replaced element. Furthermore, `object-position: 0% 0%`

always means *align with top-left corner*, `object-position: 100% 100%`

*always* means *align with bottom-right corner*, etc.

The keywords `top`

, `center`

, `right`

, etc. are really just handy aliases for 0%, 50%, 100%, etc.

Note: You can see some [object position examples](http://mdn.github.io/object-fit-basics/#position) in our basic example page.

## The effects of the different object-fit values

The following code examples show the effects of the different `object-fit`

values.

### Letterboxing images with object-fit: contain

Sometimes referred to as letter-boxing, there are times when you will want to preserve the aspect ratio of the images on a page, but get them to fit inside the same area. For example, you might have a content management system that allows you to upload products on an e-commerce site or images for an image gallery, with lots of different content authors. They may upload images in roughly the right size, but the dimensions are not always exact, and you want to fit each image into the same amount of space.

Having images with the aspect ratio shifted usually looks horrible, so you can *letterbox* them instead with `object-fit: contain`

([object-fit: contain example](http://mdn.github.io/object-fit-basics/#contain)):

```
img {
width: 480px;
height: 320px;
background: black;
}
.contain {
object-fit: contain;
}
```

### Cropping images with object-fit:cover

A different solution is to maintain aspect ratio, but crop each image to the same size so it completely envelops the `<img>`

element, with any overflow being hidden. This can be done easily with `object-fit:cover`

([object-fit: cover example](http://mdn.github.io/object-fit-basics/#cover)):

```
.cover {
object-fit: cover;
}
```

### Overriding a video’s aspect ratio with object-fit: fill

Going in the opposite direction, it is also possible to take a video and force it to change aspect ratio. Maybe some of your content editor’s videos have a broken aspect ratio, and you want to fix them all on the fly, in one easy fell swoop?

Take the following video image:

If we embedded it into a page with this:![a video with a broken aspect ratio](../../assets/dc5dd245cce4b0f7.png)


```
<video controls="controls" src="windowsill.webm"
width="426" height="240">
…
</video>
```

It would look terrible: the video would appear letter-boxed, since the `<video>`

element always tries to maintain the source file’s intrinsic aspect ratio. We could fix this by applying `object-fit: fill`

([object-fit: fill example](http://mdn.github.io/object-fit-basics/#fill)):

```
.fill {
object-fit: fill;
}
```

This overrides the video’s intrinsic aspect ratio, forcing it to completely fill the `<video>`

element so it displays correctly.

### Interesting transition effects

Combining `object-fit`

and `object-position`

with CSS transitions can lead to some pretty interesting effects for image or video galleries. For example:

```
.none {
width: 200px;
height: 200px;
overflow: hidden;
object-fit: none;
object-position: 25% 50%;
transition: 1s width, 1s height;
}
.none:hover, .none:focus {
height: 350px;
width: 350px;
}
```

Only a small part of the image is shown, and the element grows to reveal more of the image when it is focused/hovered ([object-fit: none example](http://mdn.github.io/object-fit-basics/#none)).

This is because by setting `object-fit: none`

on the `<img>`

, we cause the content to completely ignore any width and height set earlier, and spill out of the sides of the element. We then use [overflow: hidden](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow) to crop anything that spills out. A transition is then used to smoothly increase the size of the `<img>`

element when it’s hovered/focused, which reveals more of the image.

## Gallery example

To show a slightly more applied usage of `object-fit`

, we have created a [gallery example](http://mdn.github.io/object-fit-gallery/):

The 16 images are loaded via [XHR](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest), and inserted into the images as [ObjectURLs](https://developer.mozilla.org/en-US/docs/Web/API/URL.createObjectURL).

```
for(i = 1; i <= thumbs.length ; i++) {
var requestObj = 'images/pic' + i + '.jpg';
retrieveImage(requestObj,i-1);
}
function retrieveImage(requestObj,imageNo) {
var request = new XMLHttpRequest();
request.open('GET', requestObj, true);
request.responseType = 'blob';
request.onload = function() {
var objectURL = URL.createObjectURL(request.response);
thumbs[imageNo].setAttribute('src',objectURL);
thumbs[imageNo].onclick = function() {
...
}
}
request.send();
}
```

Each image in turn is given an `onclick`

handler so that when clicked the images appear full size, filling the screen (the main image, initially set to `display: none;`

in the CSS is given a class of `blowup`

, which makes it display and fill the whole screen; the main image’s `src`

is then set to the same object URL as the thumb that was clicked).

```
thumbs[imageNo].onclick = function() {
mainImg.setAttribute('src',objectURL);
mainImg.className = 'blowup';
for(i = 0; i < thumbs.length; i++) {
thumbs[i].className = 'thumb darken';
}
}
```

Clicking a full size image makes it disappear again.

```
mainImg.onclick = function() {
mainImg.className = 'main';
for(i = 0; i < thumbs.length; i++) {
thumbs[i].className = 'thumb';
}
}
```

All the sizing is done with percentages so that the grid remains in proportion whatever the screen size.

```
body > div {
height: 25%;
}
.thumb {
float: left;
width: 25%;
height: 100%;
object-fit: cover;
}
```

Note: the thumbnails have all been given `tabindex="0"`

to make them focusable by tabbing (you can make anything appear in the page’s tab order by setting on `tabindex="0"`

on it), and the `onclick`

handler that makes the full size images appear has been doubled up with an `onfocus`

handler to provide basic keyboard accessibility:

```
thumbs[imageNo].onfocus = function() {
mainImg.setAttribute('src',objectURL);
mainImg.className = 'blowup';
for(i = 0; i < thumbs.length; i++) {
thumbs[i].className = 'thumb darken';
}
}
```

The clever parts come with the usage of `object-fit`

:

- The thumbnails: These have
`object-fit: cover`

set on them so that all image thumbs will appear at the same size, at the proper aspect ratio, but cropped different amounts. This looks pretty decent, and creates a nice effect when you resize the window. - The main image: This has
`object-fit: contain`

and`object-position: center`

set on it, so that it will appear in full, at the correct aspect ratio and as big as it can be.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 15 comments

thinsoldierFebruary 10th, 2015 at 14:12PotchFebruary 11th, 2015 at 12:48jperrier@mozilla.comFebruary 15th, 2015 at 02:20MontoyaFebruary 12th, 2015 at 11:14NoOneFebruary 13th, 2015 at 07:45Scott RodFebruary 16th, 2015 at 08:05Chris MillsFebruary 20th, 2015 at 03:56Anselm HannemannFebruary 18th, 2015 at 00:48DavidFebruary 18th, 2015 at 10:35Daniel HolbertFebruary 19th, 2015 at 10:27Chris MillsFebruary 20th, 2015 at 03:54zcorpanFebruary 19th, 2015 at 01:50Daniel HolbertFebruary 19th, 2015 at 10:25Chris MillsFebruary 20th, 2015 at 03:56zcorpanMarch 4th, 2015 at 05:34