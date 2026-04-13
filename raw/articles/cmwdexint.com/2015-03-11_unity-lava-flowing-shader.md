---
title: '[Unity] Lava Flowing Shader'
url: https://cmwdexint.com/2015/03/11/unity-lava-flowing-shader/
author: Ming Wai Chan
published: '2015-03-11'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Done with blending 3 textures:

1. Rock with some outline glow, transparent background (RGBA)

2. Distortion map made with the above texture, but blurred (A)

3. Lava, where the scrolling UV takes place (RGB)

The shader is just 1 draw call [~~that little poor man doesn’t count xD its just for fun~~] so I can’t add more texcoords to it to create more layers with different scrolling speeds

The distortion effect is just what so called “water refraction” shader, which is modified from the code: [http://unitycoder.com/blog/2012/02/26/water-splash-screen-effect-shader/](http://unitycoder.com/blog/2012/02/26/water-splash-screen-effect-shader/)

The scene works in my i9000 phone with 4x-5x fps but the scrolling stops working after one UV cycle. Newer devices runs smoothly without any problem.


//*******************************//

I further added vertex displacement animation to the lava by using the script in : [https://stevencraeynest.wordpress.com/2013/03/29/easy-volumetric-explosion-in-unity3d/](https://stevencraeynest.wordpress.com/2013/03/29/easy-volumetric-explosion-in-unity3d/)

Also tested in my i9000 phone, the scrolling problem still exists, but the displacement animation works fine.

Cool! Looks terrific.

I always love lava in games. The most brilliant game with lava in it I think is From Dust. I thought that was a very inspiring game. Also the water in that game really formed sand delta’s as it flowed down mountains.

LikeLike

Thanks!

Just watched some videos of Dust. The lava really looks great with particles. It makes the scene very energetic.

LikeLiked by 1 person

No thanks! Yeah also the sounds of the volcano are real sounds recorded from a real volcano. It really sounded impressive. I’m still waiting for more From Dust kinda games:( Btw the much older game black & white 2 also has great volcano,lava effects.

LikeLike

good reference also!

I didn’t play lots of games….I really should see more >0< so anyway, thx again xD

this lava shader idea actually came from the guild wars2 mega destroyer scene. I saw the lava flows with some distortion between layers

LikeLiked by 1 person

That’s ok:) I should play more games myself but i don’t have the money for it nowadays. Being an artist made me a poor bastard:/. Good luck with the lava Dexint. I’ll keep an eye on your blog and I will upload some of my programming work in the coming days. Cheers!

LikeLike

Terrific! Is it possible to make the rocks and the lava go in different direction, up and down. Been trying this but I can’t find the solution. Cheers!

LikeLike

Hello, thanks for this lava, it works great. I’m wondering how would I be able to make lava shader be fadeable (fade from texture color to completely transparent). Any thoughts would be appreciated!

LikeLike

Hey try to download this which has the transparent lava shader: https://drive.google.com/file/d/0B5VH9PozUxl-TGozWjd6eng1OFk/view?usp=drivesdk

LikeLiked by 1 person

Thanks for replying! To clarify, what I’m looking for is a scrolling material/shader that I can also fade out in runtime. I know very little about writing shaders but took a look at the docs and I shyly added back in the color to your Diffuse/Distort shader and added an alpha:fade property to #pragma. That didn’t seem to work and I don’t have any other ideas. Any other hints would be appreciated. Thanks again, Ming.

LikeLike

Also change these:

Tags {“Queue”=”Transparent” “RenderType”=”Transparent” }

ZWrite Off Blend SrcAlpha OneMinusSrcAlpha

Also, make sure the render queue on your material is 3000(transparent) (you should see the render queue field on the material)

LikeLiked by 1 person

I got a more experienced coworker to help me with this. Thanks for the help!

LikeLike

Hey i applied the material to a plane and it doesn’t move like in the video! what am i doing wrong? (i know little to nothing about shaders so, sorry for the newbie question)

LikeLike

i guess you hav’nt add the scrolling UV script

LikeLike

How to fix this error?

Material ‘mtl_lava_diffuse’ with Shader ‘Lava Flowing Shader/Unlit/Distort’ doesn’t have a texture property ‘__LavaTex’

LikeLike

Did you edited the shader? ‘__LavaTex’ has an extra underscore. It should be ‘_LavaTex’

LikeLike