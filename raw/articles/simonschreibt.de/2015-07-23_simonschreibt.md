---
title: Simonschreibt.
url: https://simonschreibt.de/gat/sacred-2-fake-mirror/
author: Simon
published: '2015-07-23'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This is a really spontaneous post and it was initiated by [this observation about Fallout 3](http://kotaku.com/turns-out-fallout-3s-trains-were-actually-equipped-to-1719572837):

It made me remember a small trick one of our level designers told me when we were working on [Sacred 2](http://www.sacred2.com/). It’s not as crazy cool as the Train-Hat, but I liked it a lot.

Here you see a dungeon entrance and the level designers made it so that the bright white area “bleeds” into the level like sunshine flooding through the entrance (I’m **not** talking about the rays, only about the overglow):

That’s not really special. But would you expect such a wireframe in this scene?

Yes, there’s a giant mirror sticking in the wall and you’ll find this mirror at almost all dungeon entrances.

So why is that? It’s simple: Level Designers were able to scale objects and the normals of these objects where scaled too. We **didn’t** normalize them after scaling which means in our engine: Up-Scaled objects got brighter, Down-Scaled objects got darker. The mirror was made for hanging in a living-room, but they scaled it up and got a bright glowing surface out of it.

I mean, in general I don’t like that an engine has such a flaw (if this behavior is normal, just tell me, but in the eyes of an artist, this is a bit weird :) ), but on the other hand, I really like how the level designers used the “bug” and at the end it was better that it never got fixed – dark entrances or a lot re-working would have been the result. :D

I hope you liked this small and light article. If you know cool hacks in your game, feel free to tell me. :) Thanks for reading!

Hi!

I wanted to say thanks for your blog, great stuff! I love to reverse engineer technical side of the art myself. Hope you’ll keep posting!

Great to hear! Did you write your technical investigations down somewhere? Nice Art-Station-Portfolio ;)

Yay, thanks! No, not yet. I’m, sort of, working on buiding my online presence, and I’ll try to post some thoughts about gamedev, in general, and certain aspects in detail. Maybe blogspot, maybe facebook, probably alltogether.

Looking forward reading what you write. Maybe tumblr would also be an interesting place for you, because there it’s really easy to follow blogs and keep updated.

I use tumblr, just not that often, usually just spamming with some art nonsense ) http://seraphfawkes.tumblr.com/

Nice! I follow you know :) That’s what I like about Tumblr. <3

BTW – Not a bit art trick, but anyway. In Mafia 1 they’ve used typical 12 sided toruses for wheel, but to make them look better from the sideview, they’ve added alpha tested texture of the wheel with rim. Cheers!

Yeah i really like this trick. I think several racing-games did that too back then. Thanks for your comment :)

Hey just wanted to say that the scaling of the normals will always happen except it is taken care of by code.(normal vectors should only ever be normalized)- if they are scaled the shading gets over interpolated between the vertices and this leads to so called shading overflow ;). This is just the nature a matrices and vectors, anyhow there have to be even more things done to the normals of an object, if the scaling of the object is not uniform.- then even the orientation not only the length of the normal vector has to be recalculated.

Good points :) I don’t remember if our level designers were able to scale the objects non-uniform…and it’s good that this never got fixed :D Else the dungeon entrances would have been very dark suddenly. :D Thank you for your comment!