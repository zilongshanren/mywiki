---
title: Simonschreibt.
url: https://simonschreibt.de/gat/deus-ex-scanlines/
author: Simon
published: '2013-01-23'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

In Deus Ex you can see screens hanging at the walls. Or let’s say they’re electrical boards. If you get near to them, you can see weird artifacts. It’s like in [Matrix](http://en.wikipedia.org/wiki/The_Matrix) where Neo gets questioned by the police, sitting in a small room. First you see that through a monitor but the viewers “eye” (camera) gets closer and closer until we “enter” the screen and are in the room with Neo. Shortly before this you can see very similar artifacts there also. Now we know how this lady from [The Ring](http://en.wikipedia.org/wiki/The_Ring_%282002_film%29) feels.

That reminds me of user-created spray paints in Team Fortress 2. Some of them would use mipmaps for trickery.

For example, a “spray paint” of the “Sandvich” item on a plate. However when you walk closer (highest mipmap level), the Sandvich disappears, leaving an empty plate, and the text “How could this happen?” appears instead!

Awesome trick! I love when people play around with MipMaps. Back in the days i saw a nVidia presentation where they added more color layers the more mip maps they generated and got a cheap fog effect (textures more far away would be tinted more).

Where is this? I don’t recall seeing this issue in the game.

And yes, I personally consider it an issue :P

It might just be moiré due to lack of mipmapping or a negative lod bias. Try having a grid texture without mipmapping in a 3D scene. You will see the same thing.

Remember that your monitor is a grid of pixels, when a grid pattern interlaces with that grid you can get moire. This is a big problem for photographers and filmmakers as well. You might recall seeing a person on TV which has a suit of small checkered fabric, and you will get the same issue. If the contrast on the pattern is high enough you will even get different colors due to the relative offset of the RGB elements!

http://en.wikipedia.org/wiki/Moir%C3%A9_pattern

It’s in the head quarter right at the start of the game. You have to do the first mission in the statue of liberty and then you are free to go to the head quarter and there you can see it. :)

Yeah normally moire effect isn’t cool but i like it in this special case :)

I made a similar scanline shader for my own game. I can only assume that the weird UV trickery is one of two things:

1. Scanline UV scale from screen view (based on camera distance)

2. Mipmap switching (maybe)

It’s really strange that the lines seem to be distorted to the left, specifically, but that may have been because you were standing more to the left of the screen.

Great to hear that someone read this small article. :) I really like the effect but I guess most people are more interested in the bigger stuff. Is there somewhere an example of your game where this effect is shown? Would love to add it as an update to the DeusEx-Article!

Hey,

I made a pretty similar effect once by erasing scan lines from a simple multiplicative sphere map (white in the center, gray at the edges), which I was doing to simulate anti-glare coating on a laptop screen. Before editing, it was about as dramatic as that, but I blended the scanlines to be more subtle.

Sounds nice, do you have some example-GIF or something like that? :)

I’m sorry, I don’t, and I don’t think I have the model put together any more. But I’ll certainly be happy to share one if I make something similar again in the future! I’ve been trying to learn modelling and HLSL simultaneously, and I love tricks like this– if you want to see more, maybe check out http://vasilnatalie.deviantart.com/art/Gems-647134374, which is me messing with internal meshes to create specular, then scroll around a bit. I’m a lousy artist, I’m not a good coder, but I try to be creative. Maybe because I need to be to make up for the absence of talent :)

Wow, that’s great! It would be awesome to see the 2nd render-target and maybe a wire-frame view in the same animated gif. This would explain it basically without words :D Really cool idea! Let me know if you plan to update the GIF – if not, I would love to take it as it is and make a tweet. :)

Well, it’s still something I’m working on. Not really happy with the output yet, even if I think that the idea has some merit. But I can’t predict that it’ll ever be good, and especially not when. I pursue ideas based on my ability and interest, return to old projects when I get a new idea. Next time I open this file, I’ll probably examine what happens to the specular when I remap a normal map so that 0.75 blue is actually zero instead of 0.5 blue, see what happens when I get some specular on a backwards normal that’s still continuous with the other normals.

I’m glad you like it, and feel free to tweet! I’ll certainly consider building in some wireframe and alternate RT shaders to show the principle better in any future gifs I make.

hey, really nice website 👍

there are some shader examples for moire patterns at shadertoy.com

1- https://www.shadertoy.com/view/4sjXzm

2- https://www.shadertoy.com/view/DlfSz8 //this one is not moire but looks awesome, very cheap also

Those are really cool! Thanks for sharing :)