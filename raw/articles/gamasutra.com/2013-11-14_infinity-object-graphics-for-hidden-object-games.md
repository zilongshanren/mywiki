---
title: Infinity object graphics for hidden object games
url: https://www.gamedeveloper.com/art/infinity-object-graphics-for-hidden-object-games
author: Junxue Li
published: '2013-11-14'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

If you play hidden object games very much, you will encounter the same objects all the time. Across many games from many developers, the objects seem to come from a same collection of photos.

This problem due to so limited is the source of royalty free photos, and too many hidden object games.

This is also a great woe of we art production houses. The clients often complain that we used the same piece of photo of a hat, and rubber duckling over and over again.

Today I come up with a solution, which enables us to tap into an infinity source of object graphics. And for a single object, we can enjoy all the camera angles, which saves us from the trouble that we have a single graphic to use.

The idea is to download free 3D objects, then render turntable animation to get a sequence of images. Then from the sequence, we have all the angles to choose from, that in putting hidden objects in a scene, you can always find graphic of a fitting angle.

Ok, let’s see how it works.

There’re many websites offer free downloading 3D objects. Like this one:

It offers a full spectrum of objects. We can find the categories which are most commonly used in hidden object games, like kitchen wares, clothes, home appliances. There seems to be infinity objects we can use from this site.

![](../../assets/60288483b7b0058d.img)


![](../../assets/9f59a9ce20ba84ce.img)


We download this coffee grinder from this link:

![](../../assets/f181396933561bcf.img)


Import it to Maya, make a turn round animation of it. Here we turn 180 degrees about Y axis, from frame 1 to 10. That is, we get a graphic every 18 degrees, 10 graphics in all.

![](../../assets/236c9647225df28f.img)


We put 4 cameras, which can catch 4 different angles.

![](../../assets/315e13d8a79cdf58.img)


![](../../assets/bdf6b234d77a628e.img)


Give a simple lighting to the coffee grinder.

Then render frame 1~10 from all the 4 cameras, we get 40 graphics in all. I think for a hidden object scene, for any certain spot in it, you can always find a fitting graphic to fit the perspective.

![](../../assets/ebc16dec40883a28.img)