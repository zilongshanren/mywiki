---
title: 'Camera mapping a comic: the Ward trailer'
url: http://joostdevblog.blogspot.com/2013/12/camera-mapping-comic-ward-trailer.html
author: Joost van Dongen
published: '2013-12-19'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Marissa Delbressine](http://ocreana.tumblr.com/)was working on a trailer for her comic and she thought having a camera mapping of Ward's cover would be an awesome addition. Marissa threw me a pretty smile to which I couldn't say 'no', so I went to work on it. (Marissa happens to be my girlfriend, so I guess without the pretty smile I couldn't have said 'no' either... ;) )

Here is a compilation of the shots I made of the cover of Ward, plus shots of the meshes used to make this scene:

Marissa used a couple of these shots in the complete Ward trailer, which you can see below. Note that most of this trailer is

*not*camera mapped: I was personally only involved in the shots at 0:43 and 1:12. All the 2D art and the rest of this trailer were made by Marissa and co. I think the result is great: making a trailer for something as static as a comic is difficult and I think Marissa did a great job of bringing it to life. It helps if you know Dutch and can read the text, though... Anyway, here is the complete trailer:

It has been several years since I last wrote about camera mapping on this blog, so let's do a quick recap of what this technique is. The idea is to project a 2D image onto a 3D model, so that you can do 3D camera movements through this 2D image. To do so, you have to first split the image into layers, and then create simple, rough 3D models to represent the objects in the image. Here is how this was done for Ward:

![](../../assets/c3b853b2e9a78fce.jpg)

*The process of creating the camera mapping of Ward. I only did the 3D parts: colours were done by Shanna Paulissen and splitting into layers and extending them by Iris Adriaansz.*

Those who make 2D animations will likely recognise most of this: camera mapping is a more advanced version of a technique that is often used by 2D animators; they also split the scene in layers to create a 3D effect. The difference between this simple layers approach and full camera mapping is that with camera mapping the 3D models aren't just planes: they are real 3D objects that roughly mimick the shape of the 2D objects. This makes the 3D camera movements much more convincing, since the scene is not just a collection of cardboard planes anymore.

The main reason I think camera mapping is such an exciting technique, is that it allows for 3D graphics to achieve unique 2D looks. 3D graphics can look like many things, but there are very few 2D styles that normal 3D graphics can do well. The roughness of a brush or a pencil stroke is something that only really works in 2D, and camera mapping makes it possible to get that look in 3D.

Another benefit of camera mapping is that it only requires very simple 3D models. The details are all in the drawing, so you don't need to model everything and can get away with crude approximations of the real 3D models. Most work in camera mapping is in dividing the scene into proper layers in Photoshop. If the artist already works in layers, this can be a relatively simple thing to do.

The big downside of camera mapping is that objects have no backside, so the camera cannot rotate all around them. In the case of games this makes camera mapping mostly useful for games with limited camera movement, like 2.5D platformers, or games with a perspective like Diablo. In fact, the awesome Diablo III uses quite a bit of camera mapping, but disappointingly refuses to use the technique to create a truly unique art style.

![](../../assets/ecd36d64ffdf5927.jpg)

Since it has been so long since I wrote about camera mapping, here are the camera mappings I did a couple of years ago:

I hope to come back to camera mapping some day to create some real-time game environments with it. I already have one quite far finished, but instead of finishing it I always end up spending my spare time on

[Cello Fortress](http://www.cellofortress.com)and writing blogposts, so I don't know when I will actually get to that.

Let's end this blogpost with some blatant marketing for Ward, which is an awesome comic and it currently available in stores in the Netherlands. Marissa drew some amazingly detailed and beautiful art for it, so check it out! Ward is only available in Dutch, and is sold in specialised comic stores and at

[Bol.com](http://www.bol.com/nl/p/gestrand/9200000019244989/)and in the

[Eppo Webstore](http://www.eppostripblad.nl/eppo_shop.php?artsid=138).

Have a look at the trailers that Wizards of the Coast do for the release of new Magic sets, for example the latest one: https://www.youtube.com/watch?v=oNewZZPKH-U (Don't mind the voice-over: it's ridiculously bad.)

ReplyDeleteA lot of these shots are very close to the art on actual magic cards (painted by freelance artists), so my expectation is there is a lot of camera-mapping-like stuff going on in these trailers. (Along with particle effects and stuff.) There's actually an impressive amount of animation in these newer ones; the older ones were more restrained, for example http://www.youtube.com/watch?v=B6eUQ5DTqtU

Yeah, I had already seen those, really cool stuff! :)

Delete