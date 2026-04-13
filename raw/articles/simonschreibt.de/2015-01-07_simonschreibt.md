---
title: Simonschreibt.
url: https://simonschreibt.de/gat/rei-ayanami-inner-eyes/
author: Simon
published: '2015-01-07'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Did you like poetry interpretation during school? Me neither. But thanks to a nice [polycount](http://www.polycount.com/forum/showpost.php?p=2140701&postcount=380) member you’ll get one because [throttlekitty](http://www.polycount.com/forum/member.php?u=25486) mentioned this topic and it was too fascinating to not talk about it:

This model by [Muumin](http://www.3dcg-arts.net/art/polygon/1311/full) seems to orient its eyes always to the camera, right? To me it looks really convincing and I would have expected the use of bones for the eye-geometry and some constraints to focus them towards camera.

Not sure if you saw it instantly, but I noticed it only at second glance: There are **no** eye balls. No camera-oriented parts. Instead, the eyes only consist out of holes and the pupils are painted at the back of the eyehole. It gets clearer when you look at it from nearer distance:

And it works great too for camera positions above/below the character:

OK, I have to admit that this illusion only works for the very specific cases:

- The texture must be self-illuminated, so that no shadow reveals the secret.
- The character always looks at the camera which might not be too useful in a lot cases.

But anyway, I really like the basic idea! Below you’ll find a small example with Mr. GPU who wants to clear out this topic further, by comparing the shaded (left), illuminated (center) and a wireframed version (right).

Mr. GPU

Thanks for reading! Please tell me how you like the trick! Also I would be interested in your opinion about the article itself. It’s more “back to the roots” which means short and simple instead of the really big ones I release lastly. Which one do you like more?

[The model by Muumin we’re talking about](http://www.3dcg-arts.net/art/polygon/1311/full)

[l02]

[Who’s Rei Ayanami?](http://en.wikipedia.org/wiki/Rei_Ayanami)

[l03]

[Throttlekitty’s post in polycount forum](http://www.polycount.com/forum/showpost.php?p=2140701&postcount=380)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Zoltan](https://twitter.com/ZoltanErdokovy)mentioned

[this tweet](https://twitter.com/kohta0130/status/717555450799984640)with another great example for a “strange” trick when it comes to bringing anime into 3D:

It’s awesome how these people know exactly what they want and bend 3D if necessary to achieve the goal. If you like this I can strongly recommend [this awesome talk](http://gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The) where more stunning tricks are presented to create the style of Guilty Gear X.

This is super creepy o_o

(And also pretty clever, but once you’ve noticed it you can not unsee it!)

Right! but for me, it works very well even if i see how it’s done. Normally such effects lose “grip” but this one impressed me everytime i look at it :)

The T-Rexs completly bluffed me ! I was thinking it was 3D images incrusted on real-life video. Only the last part of the video makes it clear how it works… and only knowing the trick it still works for me. Great stuff !

Had exactly the same impression :D Looks so weird but cool :)

Whow! How cool that it works in the browser already so you can check out yourself.

Somehow I immediately feel how the poly mesh works in the background. But it doesn’t feel weird like I could imagine it should.

I know the dragon thing too :D but in the video its well lit on purpose so the side that actually faces to the bottom is not that dark. In reality the effect is pretty good but not THAT strong.

Yeah the dragon video seems to be under perfect conditions. But on the other side, there’s paper-craft for those models in the internet. Which means everyone can build it’s own dragon … we should try it out and see how it works with different light setup :D

Another great post! Lengthy or short–this stuff is always so interesting and enlightening. Thank you!

Thanks man! Personally i like the short ones sometimes even better because they’re faster to read and contain not less awesome tricks :D

Can you try the shaded Mr. GPU, but with eye normals being outward or all pointed in the same direction instead?

I’m not sure if I totally understand what you mean? :D

Here are some Paint mad skillz to illustrate :D http://i.imgur.com/Bp9mzZa.png

To make those concave “eyes” shaded like true spheres or at least like a flat polygon.

Good Idea :) Thanks for the image!

Having used some of these flat eyes, you generally want to avoid much in the way of diffuse lighting for them anyways. They should kind of glow with more ambient than is typical. Shadowing is best done with an explicit alpha-mapped shadow layer over the eye, which is just a black-to-alpha transparency. The best place to see these shadows in action is on DOA models.

The concave normals don’t end up meaning a lot to the broad specular I end up using for irises. What’s much more noticeable is the difference that occurs from Y-axis (up-down) differences in the eyes, which don’t mirror the way real life irises do. These differences can easily be corrected in the shader by rotating the normals to the center line. If you want to use specular on these kinds of eyes, you’ll probably be wanting to mask the specular for good, anime eye style effects, and that mask will end up making it even harder to notice any concavity in the iris.

However! The concavity is totally apparent if you try to use the iris to create environmental lighting lens effects, typically with a sphere map or cube map. These kinds of effects are both really important to anime eyes (huge highlights!) and look totally wrong with concave irises. Bending the normals would probably work, but what I’ve ended up doing is creating a transparent, convex lens to fit over the iris. I can then use environmental lighting, with NdotE fresnel, applied to that iris as an add or alpha layer over the iris. This has benefits for the side view. Bending the normals somehow (maybe a model space normal map?) would probably have almost the same effect, though. If performance is a consideration, the lens is an extra draw call.

There are limits to the tracking from concave eyes. The best solution is still a bone, with a transformation matrix generated by the CPU. It’s also possible to do these sort of transformations in the shader, provided you supply it with a center of rotation for the eye– just rotate the eye’s vector toward the camera and apply that rotation to the vertices of the relevant materials.

Cool stuff, Oskar Stalberg used this trick for the shrubs in Townscaper https://twitter.com/OskSta/status/1191990107785572352.