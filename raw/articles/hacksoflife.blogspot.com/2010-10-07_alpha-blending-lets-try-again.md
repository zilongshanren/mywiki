---
title: Alpha Blending, Lets Try Again
url: http://hacksoflife.blogspot.com/2010/10/alpha-blending-lets-try-again.html
author: Benjamin Supnik
published: '2010-10-07'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[this convoluted mess](http://hacksoflife.blogspot.com/2010/02/alpha-blending-back-to-front-front-to.html)of recipes for blending back to front and front to back. I've had some time to revisit the code, and the actual formulas are simpler than I realized and more consistent; they also don't require split blending functions for the back to front composited case, which is nice if you want to run on, well, on dinosour hardware (since pretty much anything you can find has split blending functions from the Radeon 8500 on).

Premultiplied Alpha

The goal is to composite several translucent textures together, and then composite them over our scene as if the whole scene had been drawn in order. In order to make this work, we want to use premultiplied alpha - that is, textures where the RGB color has already been made 'darker' if the alpha channel is not 1.0. In this scheme our blend function can be (1.0, 1.0 - SA) instead of the normal (SA, 1.0-SA) because the source pixel is already multiplied by SA. That would be the premultiplication.

Why is

[premultiplication a good idea](http://hacksoflife.blogspot.com/2010/10/premultiplication-pros-and-cons.html)? We have to solve the problem of "what is under translucent", and premultiplication does that. In a premultiplied texture, the RGB channel becomes more black as it becomes more transparent, and thus "nothing" has a valid color representation (black). In a traditional texture, there is color behind transparent, and that can cause sampling artifacts.

So our goal is to composite a premultiplied texture. That means that the "clear" will be 0,0,0,0 (black, transparent). Note that while the color is black (meaning nothing to add color-wise) we still need that alpha channel to be 0 (transparent) too to tell us that the background won't be occluded.

Fixing Back to Front

If you have ever blended together a bunch of geometry (back to front) and then composited the result on top of something else, you know that the alpha channel for that back-to-front geometry is going to be pretty screwed up. To see the problem, imagine blending a really light (10% alpha) screen over an already opaque scene. That light screen will (by a "strength" of 10%) move the alpha channel away from opacity and toward translucency. The problem is that the alpha blends itself, and we don't want that.

It turns out that pre-multiplied alpha can fix this. We set our blending equation to (1.0, 1.0-SA) and we pre-multiply our RGB. Our alpha will now be the old alpha (lightened by the amount the new alpha is "covering it") plus the new alpha, but not lightened.

To take the case of a 10% screen over an opaque scene, the alpha will be 0.1 * 1.0 + 1.0 * (1.0 - 0.1), which gives us...1.0, which is exactly right: blending over an opaque object doesn't make it translucent.

Front to Back

For the front to back case, we still want to use pre-multiplied alpha, but we set our blend factors to (1.0-DA, 1.0). With the back to front case in "pre-multiplied" form, this should look very symmetric. In fact, all we're doing is changing which one is the "master" (whose alpha cuts down the other" and which is not).

What effectively happens is:

- The less alpha is in the buffer already, the more you get to draw (ehnce 1.0-DA as a factor).
- The buffer is never reduced in color (which makes sense, since you can't darken something by drawing behind it).
- The amount of alpha opacity you leave behind/add-in is also reduced by what is already there (you matter less if you are behind something translucent).

## No comments:

## Post a Comment