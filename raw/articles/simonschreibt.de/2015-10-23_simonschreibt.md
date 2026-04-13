---
title: Simonschreibt.
url: https://simonschreibt.de/gat/xrebirth-geometric-lensflares/
author: Simon
published: '2015-10-23'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Lensflares are usually done by using textures (like the one below) which are oriented to the camera or may also be created via post effect.

For [X:Rebirth](http://www.egosoft.com/games/x_rebirth/info_en.php) we used textures at first but had some problems with compression artifacts especially when we had huge lensflares like the haze around the sun which dominates big parts of the screen.

I learned a really interesting trick from our Art-Director [Alex](http://www.abalakin.de/) which is to not use textures at all. Let’s recap: Normally you have a quad with a texture on it:

![](../../assets/df23c37107356746.png)


But if you invest a bit more geometry like here in this triangle-wheel, define the center-vertex as white, the outer ones black and then set its material to **additive** blending, you’ll end up with a very similar result:

![](../../assets/ff64775fd4abff6b.png)


In [X:Rebirth](http://www.egosoft.com/games/x_rebirth/info_en.php) we used this for all elements of our lensflares:

Here’s an example video showing the different elements in a “real-world”-example.**HIGH-RES** version: [mp4](https://data.simonschreibt.de/gat053/lensflare_wireframes_1280.mp4)/[webm](https://data.simonschreibt.de/gat053/lensflare_wireframes_1280.webm)

I’m not exactly sure if the extra geometry steals more performance than “real” textures would, but with this system we made sure that no compression artifacts appeared and if I look at the results I think this tech is quiet promising:

What do you think about this approach? Do you like it? Do you know similar stuff? Let me know in the comments or via [mail](mailto:simon@simonschreibt.de), [twitter](https://twitter.com/simonschreibt) or [facebook](https://www.facebook.com/simonschreibtblog)!

![](../../assets/ba0680151067ebbc.png)

[CeeJayDK](https://www.reddit.com/user/CeeJayDK)shared two great links related to

[Triangulation](http://www.humus.name/index.php?page=Comments&ID=228&start=0)and a

[Particle Trimming Tool](http://www.humus.name/index.php?ID=266)which explain why the geometric-lensflares might be a bit less performant than using textures. But like he sais: The only way to find out is testing. :)

![](../../assets/ba0680151067ebbc.png)

[Froyok](https://twitter.com/Froyok)created a HUGE post about lens flares:

[Custom Lens-Flare Post-Process in Unreal Engine](https://www.froyok.fr/blog/2021-09-ue4-custom-lens-flare/)! Don’t get discouraged about the title, it’s not “just” about Unreal, it contains a massive amount of information on how (and why) lens flares form with great examples from the real-world, film and games. Wow!

![](../../assets/4dc91c6272c65901.gif)


![](../../assets/4dc91c6272c65901.gif)

“I’m not exactly sure if the extra geometry steals more performance than “real” textures would”

It might even save performance. Less overdraw than a quad and less memory without the texture image files loaded.

Good points :) Sure the rasterizer might drop some pixels because of the thin trianges but it seems to be fine :)

Very interesting approach. And loved the results. Good work

Thank you :) There’s a really interesting discussion about this topic on reddit: https://www.reddit.com/r/gamedev/comments/3q9j8h/i_posted_a_new_game_art_trick_about_using/

This is always a nice trick to use vertex colors instead of real texture if you need scalability and as Justin is pointing, it even might save performances. :)

btw : This makes me thing about this trick : http://simonschreibt.de/gat/homeworld-2-backgrounds/

Well done !

Yeah, Vertex-Color for the win! :) I really like playing around with stuff like that. It gives so much interesting control :)

U mean anamorphic lens flare?

What exactly do you want to know? I’m not sure if I understood your question. :)