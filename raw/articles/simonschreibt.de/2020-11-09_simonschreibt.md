---
title: Simonschreibt.
url: https://simonschreibt.de/gat/mafia-ii-hat-vs-hair/
author: Simon
published: '2020-11-09'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1).

![](../../assets/474d258b7d1c8291.png)


![](../../assets/474d258b7d1c8291.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

I stumbled across this funny video and after a short period of lolling I was thinking… maybe this isn’t a bug at all!

What we see here is **either** the result of a little torture fun of an opposing Mafia family or it’s a neat little trick to avoid **clipping** between hat and hair (only that the guy in the video has no hat – which is the **actual** bug).

Here is how it looks when you just put a hat on a Mafia II guy:

What can we do about the clipping? We already saw the solution in the first video. They just compress the upper head a bit:

But how did they do it? At first I thought it’s a vertex shader pushing the vertices a bit but I couldn’t find proof by studying the draw calls.

So I got some mod tools ([M2Toolkit](https://mafiamods.com/mods/mafia-2-toolkit/) and [M2CharMC](https://cgig.ru/en/2011/01/converting-3d-model-from-mafia-2-en/comment-page-1/)), extracted the meshes and found something! There is a bone called “**HairScale**” in the rig and this is how it looks when scaling it up and down:

Voilà! With that, we can put the hat on, scale the hair bone down and schwups, our little Mafia men is happy!

I hope you liked the article! Feel free to follow me on [Twitter](https://twitter.com/simonschreibt), check out my [Artstation](https://www.artstation.com/simont) and/or leave me a comment.

![](../../assets/ba0680151067ebbc.png)

Found this video [Inside Disco Elysium – graphics studies](https://youtu.be/vp5mtj2tJMQ?si=i4x4_9XnK4oHi3F3&t=188) which reveals a similar technique in Disco Elysium: Here, parts of the body are scaled depending on the cloth.

Putting pants on makes the legs thinner (orange outline):

Adding a shirt scales torso (orange outline):

Interesting: Putting a jacket **on top of the shirt**, makes the shirt scale as well (blue outline). Also look how the feet deforms when a show is put on it (orange outline, in the shot only 1 shoe is worn):

There is one open question, though: How exactly does the scaling work? In the Mafia game, a bone was scaled.

For Disco Elysium, we either have several additional bones as well, or it’s done via vertex shader (pushing the vertices inward along their normal orientation). If so, I guess the body is painted with different vertex color masks to allow for scaling different parts (e.g. legs) and leaving others untouched (e.g. torso).

Or could there be another solution? What do you think?

Simon, I just wanted to thank you for this great blog. I have sent it to my students over many years so they can see the innovative way artists in industry solve problems. It is such a great resource, I hope you keep it up!

Thank you for the kind words! <3

I guess it’s blendshapes in Elysium :)