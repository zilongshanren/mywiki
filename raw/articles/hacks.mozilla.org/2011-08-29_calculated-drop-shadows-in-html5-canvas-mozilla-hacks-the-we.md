---
title: Calculated drop shadows in HTML5 canvas – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/08/calculated-drop-shadows-in-html5-canvas/
author: Chris Heilmann
published: '2011-08-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of the best new features of HTML5 when it comes to visual effects is the canvas element and its API. On the surface, it doesn’t look like much – just a rectangle in the page you can paint on and wipe. Much like an etch-a-sketch. However, the ability to transform, rotate and scale its coordinate system is very powerful indeed once you master it.

Today I want to quickly show how you can do (well simulate) something rather complex with it, like a calculated drop shadow on an element. To see what I mean with this, check out the following demo which is [also available on the Demo Studio](https://developer.mozilla.org/en-US/demos/detail/calculated-shadow/launch):

(This is using JSFiddle to show you the demos, so you can click the different tabs to see the JavaScript and CSS needed for the effects. All of the demos are also [available on GitHub](https://github.com/codepo8/calculated-shadow).)

As you can see, the shadow becomes more blurred and less pronounced the further away the “sun” is from it. You can use the mouse to see the effect in the following demo:

Let’s take a look how that is done. The first step is to have a canvas we can paint on – you do this simply by having a mouse detection script (which we used for years and years) and a canvas with access to its API:

Click the play button of the above example and you see that you can paint on the canvas. However, the issue is that you keep painting on the canvas instead of only having the orb follow the cursor. To do this, we need to wipe the canvas every time the mouse moves. You do this with `clearRect()`


Running the above example now shows that the orb moves with the mouse. Cool, so this is going to be our “sun”. Now we need to place an object on the canvas to cast a shadow. We could just plot it somewhere, but what we really want is it to be in the middle of the canvas and the shadow to go left and right from that. You can move the origin of the canvas’ coordinate system using `translate()`

. Which means though that our orb is now offset from the mouse:

If you check the “fix mouse position” checkbox you see that this is fixed. As we move the coordinate system to the half of the width of the canvas and half of its height, we also need to substract these values from the mouse x and y position.

Now we can draw a line from the centre of the canvas to the mouse position to see the distance using `c.moveTo( 0, 0 );c.lineTo( distx, disty );`

where `distx`

and `disty`

are the mouse position values after the shifting:

In order to find out the distance of the shadow, all we need to do is multiply the mouse coordinates with -1 – in this demo shown as a red line:

This gives us a shadow distance from the centre opposite of the mouse position, but we don’t want the full length. Therefore we can apply a factor to the length, in our case 0.6 or 60%:

Now we are ready for some drop shadow action. You can apply shadows to canvas objects using `shadowColor`

and its distance is `shadowOffsetX`

and `shadowOffsetY`

. In our case, this is the end of the red line, the inversed and factored distance from the mouse position to the centre of the canvas:

Now, let’s blur the shadow. Blurring is done using the `shadowBlur`

property and it is a number starting from 0 to the strength of the blur. We now need to find a way to calculate the blur strength from the distance of the mouse to the centre of the canvas. Luckily enough, [Pythagoras](http://en.wikipedia.org/wiki/Pythagorean_theorem) found out for us years ago how to do it. As the x and y coordinate of the mouse are the catheti of a right-angled triangle, we can [calculate the length of the hypothenuse](http://en.wikipedia.org/wiki/Hypotenuse) (the distance of the point from the centre of the canvas) using the Square root of the squares of the coordinates or `Math.sqrt( ( distx * distx ) + ( disty * disty ) )`

.

This gives us the distance in pixels, but what the really want is a number much lower. Therefore we can again calculate a factor for the blur strength – here we use an array for the weakest and strongest blur `blur = [ 2, 9 ]`

. As the canvas itself also has a right-angled triangle from the centre to the top edge points we can calculate the longest possible distance from the center using `longest = Math.sqrt( ( hw * hw ) + ( hh * hh ) )`

where `hw`

is half the width of the canvas and `hh`

half the height. Now all we need to do is to calculate the factor to multiply the distance with as `blurfactor = blur[1] / longest`

. The blur during the drawing of the canvas is the distance of the mouse position multiplied with the factor or `currentblur = parseInt( blurfactor * realdistance, 10 );`

. We disregard blur values below the range we defined earlier and we have our blurred shadow:

In order to make the shadow weaker the further away the mouse is we can use the alpha value of its `rgba()`

colour. The same principle applies as with the blur, we set our edge values as `shadowalpha = [ 3, 8 ]`

and after calculating them from the distance we apply their inverse as the alpha value with `c.shadowColor = 'rgba(0,0,0,' + (1 - currentalpha / 10) + ')';`

. This blurs and weakens the shadow:

You can do a lot more with this, for example we could also [scale the sun orb](http://jsfiddle.net/codepo8/eUYKu/26/) the further out it gets or use a [second shape to resize and blur it](http://jsfiddle.net/PHbgN/32/). You can also go [completely overboard](http://jsfiddle.net/codepo8/mTaug/17/).

Found a way to optimise this? Tell us about it!

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 5 comments

basicAugust 29th, 2011 at 06:23ybochatayAugust 29th, 2011 at 21:55Chris HeilmannAugust 30th, 2011 at 04:43Style ThingAugust 30th, 2011 at 17:06ybochatayAugust 31st, 2011 at 07:19