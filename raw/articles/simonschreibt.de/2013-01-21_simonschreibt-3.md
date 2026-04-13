---
title: Simonschreibt.
url: https://simonschreibt.de/gat/diablo-3-trees/
author: Simon
published: '2013-01-21'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Since i saw the Diablo 3 trees the first time on a screenshot, i noticed that there is something special. Their silhouettes were really detailed and i didn’t saw aliased edges during other objects HAD aliased ones.

I couldn’t believe it, when i saw how they did the trees. They painted them (alpha8) on slightly bent planes. That makes them only usable from one perspective, but therefore they look unbelievable detailed. And because of the fact, that camera rotation isn’t necessary in ARPGs, Blizzard shows that they’re masters in combining graphic and gameplay.

Robert asked in the comments about more details and to be honest i never was satisfied with the resolution of the GIF you can see above. Thanks to [Roger](http://boerdijk.org/) and his great APP->OBJ converter (.APP is the filetype of Diablo3-models in the MPQ archives) i was able to create a version with better quality:

Robert mentioned, why it wouldn’t be possible to get the same result with “real” geometry and my answer would be: Of course it would be possible, but you would have to spend *a lot* more polygons to get the same great detailed silhouette. Here’s a single banch as example:

They used two triangles for this beautiful branch instead of x-thousand for a “real” model. And by the way: never forget that even the biggest mega-super-highpoly-model is just rendered to a flat surface (the frame buffer or let’s say: your monitor). So if we don’t talk about [Occulus Rift](http://www.oculusvr.com/) (or other techniques which give a “real” 3D impression) and there’s no big change in the perspective (camera rotation, zooming, etc.) it might be enough to use 2D elements instead of going crazy with polygons. Just my personal opinion, correct me if I’m wrong. :)

By the way, if you’re interested here is the tree-texture (left: diffuse, right: alpha). It’s hard to look at them without getting jealous…they’re sooo beautiful! :,)

The question is, why not doing it more often like this? I think it’s because of the weight of this decision. Looking at computer graphics from an traditional art perspective isn’t easy all the time. Especially when you have people which only want awesome new tech features. “If we have a 3D engine, we have to be able to rotate the camera!”. If the person who screams like that is in a higher position than you are, your arguments that the camera rotation *isn’t* necessary (either for gameplay nor for art), can be overheard quickly.

Oh and i really recommend to watch the whole [presentation](http://gdcvault.com/play/1015306/The-Art-of-Diablo). To see how Blizzard approaches to the field of computer graphic is just awesome and very helpful when all people around you are just shouting for the next DX99 features to place them on the game package – ignoring what the game really needs.

![](../../assets/ba0680151067ebbc.png)

[Roger](http://boerdijk.org/)gifted us with a new

[Diablo 3D Model converter](http://www.kalmiya.com/index.php/coding/diablo3)! Since Blizzard released

[Reaper of Souls](http://eu.battle.net/d3/en/reaper-of-souls/)and changed the format of the .APP files (Diablo 3 models), the old converter tools weren’t working. Eventually you’ll need the vcredist_x86.exe (containing a msvcrt*.dll) – you can download it

[via Microsoft here](http://www.microsoft.com/en-us/download/details.aspx?id=40784)(i had to download the German version, be sure to set the correct language). Thx Roger!

I don’t really understand how this makes the silhoutte awesome. Wouldn’t a normal constructed tree have the same silhoutte? I kind of get that the painted leaves will look better, but the trunk surely will have the same edgy look as any other 3d mesh?

Sorry for the late answer! Here’s an image of a great tree trunk: http://thumbs.dreamstime.com/z/tree-trunk-2862486.jpg

You would need a lot geometry detail to re-create the beautiful silhouette (or decrease the detail to not make the programmers scream because of your “highpoly”-mesh). But if you would just take this picture (with an fitting alpha channel of course to separate the background from trunk), map it on a slightly bent plane, you would keep all the great detail without using too much polygons.

Was this explanation better, or do you have any more questions?

Yes I understand it better now. I’m curious as how these textures look though, would they just be normal textures with a faded alpha around the edges? or more like a hard line will differentiate between the trunk and the see-through part?

Hi Robert, i updated the article with better images. I hope it’s even more clear now :) And i hope it’s OK, that in mentioned you there? :)

It is MUCH more clear now. This is a beauty. Nice work! (Yeah, no problem mentioning me :P)

Good to hear :) Have a nice day!

I don`t get it. They didn`t use any special technique, we see this technique in every game. If you see better at tree screenshot you will notice the aliased edges on the trunk. And I guess they just deleted back side of all ingame models for better performance.

You’re might be right. My articles don’t always explain unique tech or the first appearance of a technique. Instead, they’re my subjective view on games and when i see something i like, i write about it. To be honest, i didn’t see many games using “style” but if you’ve more examples, i would love to see them. :)

Would this become a big problem if you had dynamic lights in the scene? I feel like they would work together. Also just cast shadows from the tree would not be correct from most angles. Am I wrong, or how do they work around the lighting situation?

I’ll definately watch the whole presentation. Maybe they’ll talk about it..

That’s a very good question. It works of course only with static lighting where you can define where the light comes from and in best case it shouldn’t come from the side :) If it would, you would need some additional shadow geometry I would say. Maybe it could even be the same tree-geometry but (internally) rotated towards the light source.

hi, i know its a bit late but how did they do those tree? did they generate a 3D and paint over it or they just make the whole 3D trees high geometry setup a isometric camera assign lighting then render with no background and use that image to make this 2D texture/alpha?

I don’t know for sure but it’s NOT just a texture on 1 plane so the “high poly bake to plane” would not be an option. I guess they started with the trunk, build a base geometry, painted on it and extended it more and more and re-used parts of the texture like the leafes again and again. It’s only my idea, maybe the workflow was very different. :D