---
title: Make your web layouts bust out of the rectangle with the Firefox Shape Path
  Editor – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/09/make-your-web-layouts-bust-out-of-the-rectangle-with-the-firefox-shape-path-editor/
author: Josh Marinacci
published: '2018-09-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The web doesn’t have to be boxy. Historically, every element in a page is rendered as a rectangle of some kind, but it doesn’t have to be this way. With CSS Shapes you can create web layouts every bit as stylish as print magazines, but with all of the advantages of the web.

CSS Shapes let your web designs break out of the rectangular grid. All of those classic magazine design elements like non-rectangular text flow and shaped images can be yours, for the low low price of using a new CSS standard. Text can flow, images can be rounded, even just a few non-parallel lines can make your site stand out and make your brand distinctive. Standing out is the biggest challenge most sites face today. Shapes can help!

## The Standard

The shape of your elements can be controlled with just two CSS properties: `shape-outside`

and `clip-path`

.

The [ shape-outside](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside) property changes the way content flows outside of a

*floated*DOM element. It affects layout, not drawing. The

[property changes the clipping boundary of how the DOM element is drawn. It affects drawing, not layout.](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path)

`clip-path`

Because these two properties are separate, you can use one, or both, or none — to get just exactly the effect you are looking for. The good news is that both of these use the same [ basic-shape syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape).

Want to clip your image to be in a circle? Just use `clip-path: circle(50%)`

. Want to make text wrap around your image as if it were a circle, just use `shape-outside: circle(50%)`

. The shape syntax supports rectangles, circles, ellipses, and full polygons. Of course, manually positioning polygons with numbers is slow and painful. Fortunately there is a better way.

## The Shape Path Editor

With the Shape Path Editor in Firefox 62, you can visually edit the shape directly from the CSS inspector. Open your page in Firefox, and use Firefox Developer Tools to select the element whose shape you want to modify. Once you select the element there will be a little icon next to the `shape-outside`

and `clip-path`

properties if you have used one of them. If not, add `shape-outside`

and `clip-path`

to that element first. Click on that little icon to start the visual editor. Then you can *directly manipulate* the shape with your mouse.

Open the Inspector and select the element you want to modify:

Click the icon next to `clip-path`

or `shape-outside`

. If the element doesn’t have one of these properties, add it, then select it.

Edit the clip path:

Edit the outside shape:

Check out this [live demo](https://css-shapes-demo-1.glitch.me/) on glitch.


To learn more about how to use the CSS Shape Editor read the [full documentation](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_CSS_shapes).

## Progressive Enhancement

CSS shapes are here and they work today in most browsers, and most importantly they *degrade gracefully*. Readers with current browsers will get a beautiful experience and readers with non-compliant browsers *will never know they are missing anything*.

![kitten with shape support](../../assets/4cb7e0e53ccc6840.png)


![kitten with shape support](../../assets/4cb7e0e53ccc6840.png)

![kitten image without shape support degrades progressively](../../assets/5db30ad590f5aa1a.png)


![kitten image without shape support degrades progressively](../../assets/5db30ad590f5aa1a.png)

## Stunning Examples

Here are just a few examples of the amazing layouts you can do with CSS Shapes:

Plants and background effect using `clip-path`

:

Minion using `shape-outside`

:

## Break out of the Box

Shapes on the web are here today, thanks to `shape-outside`

and `clip-path`

. Using the [Firefox Shape Path Editor](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_CSS_shapes) makes them even easier to use.

How will you make your website break out of the box? Let us know how you’re using Shapes.

## About
[
Josh Marinacci ](https://joshondesign.com/)

I am an author, researcher, and recovering engineer. Formerly on the Swing Team at Sun, the webOS team at Palm, and Nokia Research. I spread the word of good user experiences. I live in sunny Eugene Oregon with my wife and genius Lego builder child.

## 2 comments

SeratorSeptember 6th, 2018 at 01:18Josh MarinacciSeptember 7th, 2018 at 12:10