---
title: Z-order in top-down 2d games
url: https://eliasdaler.wordpress.com/2013/11/20/z-order-in-top-down-2d-games/
published: '2013-11-20'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

*This tutorial is language agnostic. It doesn’t contain implementation, because it may differ a lot between different languages or frameworks. Ideas themselves are what’s the most important, I think.
*

# Basics

So, what is **z-order**?

Z-order is an ordering of overlapping 2d objects. Look at the picture:

![1](../../assets/b955e860ef6c0ec4.png)


**Rectangle B** is drawn after **rectangle A**. The result is **rectB** is drawn “above” **rectA**. **R****ectB** is said to have higher z-order than **rectA**. Really simple.


# Z-order in games

You can tell that Link is behind that tree. But this is actually an illusion of depth achieved by using clever z-ordering. The tree is drawn after Link, so it has higher z-order.

![3](../../assets/8b5695a6a3731993.png)


And now Link is drawn after the tree. He has higher z-order and it looks like he’s standing closer to the camera. And here’s how you can achieve the same effect.

# First approach: layers

This is actually how** A Link to the Past** does it(I don’t know about moving objects, but it surely uses layers for static objects. You can see it yourself if you swing your sword at different positions near houses, walls etc.)

One sprite can be divided in two parts(as shown in the picture) which have different constant z-order. You draw all objects with **z = 0**, then with **z = 1**, etc.

This method works good and it’s easy to implement, but after a while it becomes hard to maintain, because every time you add a new sprite you have to divide it by parts and calculate areas which must be drawn before of after player and other objects.

And this can get quite complicated with lots of objects. And what about moving objects? If some enemy is circling around you, how can you find out who must have higher z-order?

# Second approach: dynamic z-order

This is where it gets smarter. First, let’s look at collision bounding boxes:

Look at the Link’s bounding box. Its lowest Y coordinate is higher than tree’s and that’s why Link is drawn after the tree. And look at another situation. Now lowest Y coordinate of tree is higher, so you draw it after Link.

So, that’s what you do:

**Sort all objects(or sprites) visible on the screen and sort this list by (boundingBox.top + boundingBox.height) value from lowest to highest and then draw objects in this order.**

If some object doesn’t have boundingBox, you can think like its **boundingBox.top + boundingBox.width equals 0. **

# Complex objects

Drawing something like arcs is trickier. It requires you to use two bounding boxes for each column. And how do you deal with the part which is above player?

You need to use z axis for this. “Z” has nothing to do with z-order in the context. It tells you how far from the ground is **boundingBox** of an object(**z = 0** is ground level). Here’s how the arc can be separated:

The algorithm is the same, but now you can sort by lowest Y coordinate for each Z and then combine them in one list sorted by Z. You’ll get something like this:

*objects = {*

*link, (z = 0, lowY = 64)*

*column_a, (z = 0, lowY = 100)*

*column_b, (z = 0, lowY = 100)*

*topPart (z = 1, lowY = 80)*

*}*

So arc will consist from three parts and each will be drawn in needed order.

Separating by z axis is actually very useful, because, for example, objects with higher z value don’t have to be checked when you check collision with objects but that’s another thing to talk about. ;)

# Final words

And that’s all I have to say about z-order. I hope it’s not very confusing. :)

Your feedback is welcome at **eliasdaler@yandex.ru**

So, if i got it right, the z-axis is a sort of gitan layer right ? It’s a sort of array of plan (ground, aboveGround etc …) ? Thanks for your tutorial, it was interesting ! :)

*giant layer, sorry for the mistake !

There’s no z-axis really. There’s just an order in which you draw objects. You can implement “height” by making use of layers and applying the algorithm for each z-layer, this is the closest thing to z-axis :)

Very useful – thank you!

You’re welcome! :)

Wonderful tutorial, very useful for the game I’m developing!

Hello, thanks for the tutorial c: But I was wondering… isn’t sorting too slow/consuming? I mean, if I have a 200×200 tilemap with several objects each tile, it would propably lag a little bit, wouldn’t it? Do you know any other method that is more eficient than sorting a whole list of sprites?

You can sort static object only one time and form sorted list of them. Then you can sort only moving objects using the algorithm and merge it with static objects list.

This will reduce the sorting a lot.

that is a great technique, I’ll have to implement that.