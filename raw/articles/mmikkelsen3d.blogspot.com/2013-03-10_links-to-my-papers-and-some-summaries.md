---
title: Links to my papers and some Summaries
url: http://mmikkelsen3d.blogspot.com/2013/03/the-jbit.html
author: Morten S Mikkelsen
published: '2013-03-10'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

So the short answer is yes it will work but in equation 7 you need to use det(A_33) and det(B_33) instead of det(A_34) and det(B_34).

This way will also work for point lights but for directionals it's a requirement since det(A_34) is in this case zero. Since det(A_34) is zero equation 4 is already simplified without using substitution.

Let me know if you have more questions I'd be happy to answer them. That paper is a blast from the past :)

Looks like the dropbox link to "Bump Mapping Unparametrized Surfaces on the GPU" is dead. I'd love to take a look at that paper.

I managed to find a summary online which was enough to implement it, and it works great. Humourously enough, I'm coming at it from the opposite angle, of wanting lower accuracy. Often in Renderman, you would just compute a displaced position and then recompute the normal from the new surface derivatives, which is theoretically maximally accurate. In practice though, the main place where you see a difference between that and your bump mapping is when the displacement is so extreme that things start self intersecting or otherwise screwing up. It looks like it will be very handy to have a simple convenient approach that seems quite robust.

So thanks a lot for coming up with a nice way of looking at this and doing the derivation, and hopefully I can actually see it sometime!

Hi, I read your thread on gamedevnet, and found this blog. http://www.gamedev.net/topic/594687-finally-nailing-the-torrance-sparrow-shader-once-and-for-all/

I am interested in looking at the illum.h file written on that thread, since the link is broken. Is it still possible to get access to it ?

Hi, will Separate Perspective Shadow Mapping work for directional lights?



ReplyDeleteI saw, that in the paper there lz which is supposed to be finite?

Regards

So the short answer is yes it will work but in equation 7




ReplyDeleteyou need to use det(A_33) and det(B_33) instead of

det(A_34) and det(B_34).

This way will also work for point lights but for directionals it's a requirement since det(A_34) is in this case zero. Since det(A_34) is zero equation 4 is already simplified without using substitution.

Let me know if you have more questions I'd be happy to answer them. That paper is a blast from the past :)

Looks like the dropbox link to "Bump Mapping Unparametrized Surfaces on the GPU" is dead. I'd love to take a look at that paper.



ReplyDeleteI managed to find a summary online which was enough to implement it, and it works great. Humourously enough, I'm coming at it from the opposite angle, of wanting lower accuracy. Often in Renderman, you would just compute a displaced position and then recompute the normal from the new surface derivatives, which is theoretically maximally accurate. In practice though, the main place where you see a difference between that and your bump mapping is when the displacement is so extreme that things start self intersecting or otherwise screwing up. It looks like it will be very handy to have a simple convenient approach that seems quite robust.

So thanks a lot for coming up with a nice way of looking at this and doing the derivation, and hopefully I can actually see it sometime!

Hmmm...could you try the link again? It should work.

DeleteOh sorry, I just realized I'm an idiot - my office blocks Dropbox.


ReplyDeleteI'll check it out at home - thanks!

This comment has been removed by a blog administrator.

ReplyDeleteHi, I read your thread on gamedevnet, and found this blog.


ReplyDeletehttp://www.gamedev.net/topic/594687-finally-nailing-the-torrance-sparrow-shader-once-and-for-all/

I am interested in looking at the illum.h file written on that thread, since the link is broken. Is it still possible to get access to it ?

There's a bump demo available in this post:



Deletewww.mmikkelsen3d.blogspot.com/2011/12/so-finally-no-tangents-bump-demo-is-up.html

You can get either binary or source. Both contain the file you're looking for.

Awesome, thanks a lot !

DeleteThis comment has been removed by the author.

ReplyDeleteThis comment has been removed by a blog administrator.

ReplyDeleteThis comment has been removed by a blog administrator.

ReplyDelete