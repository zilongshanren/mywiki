---
title: Simonschreibt.
url: https://simonschreibt.de/gat/homeworld-2-hyperspace/
author: Simon
published: '2013-04-14'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Do you remember the days where i just mentioned *what* impressed me instead of *how* it was made? Today it’s like that. But i hope you’ll enjoy the article anyway. Oh and by the way: feel free to suggest games or tricks you think this blog should cover.

When ships jump around in Homeworld, there’s a neat **Hyperspace Effect**:

I would state 3 points why this is technical kind of complicated:

- You have to “cut” the ship and render only a part of it
- You have to “fill” the cut surface
- You
*can*create a white “outer glow” around the cut

Feel free to put your Sherlock hat on and guess how [Relic](http://relic.com/) did this effect. If you need some clues, here’s what i got:

**Clue I**

I thought, maybe the ship geometry is completely there but drawn transparent behind the plane. But the wireframe tells a different story:

![](../../assets/643b88169706bac9.gif)

**Clue II**

The ship *doesn’t* move through the plane. *The plane* moves through the ship. And it uses the ship coordinate system – or it’s just “linked” to the ship (because it moves with the ship):

![](../../assets/ff32f7ab46d17cab.gif)


[Kurt Russell Fan Club](http://mikeblackney.com/)mentioned, that it’s maybe done via

[this technique](http://github.prideout.net/clip-planes/). But until a Homeworld Dev gets in contact with us, we won’t know.

I’m sorry about the missing background information but i can talk about one interesting thing i learned during the investigation:

None of the tools i usually use to have a deeper look were working with Homeworld. Maybe it doesn’t use DirectX? But how can i find out, which mode my graphic card is running?

I asked the [Internet](http://www.polycount.com/forum/showthread.php?t=119327) and some coders but it seems that there’s no tool for it. But you can check which .DLLs are laying in the game directory and/or check which file are loaded with [Process Monitor](http://technet.microsoft.com/en-us/sysinternals/bb896645.aspx).

I found out that Homeworld uses OpenGL and thanks to the great [GLIntercept](http://code.google.com/p/glintercept/) i was able to force a wireframe mode.

![](../../assets/ba0680151067ebbc.png)

[Lino](http://linolafett.deviantart.com)just showed me a video how

[Elite: Dangerous](https://www.elitedangerous.com/)does a very similar effect but covering the “cut” with a cloud (at 00:09):

![](../../assets/f0b0c8a815f9481d.png)


![](../../assets/f0b0c8a815f9481d.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

And here are other really nice looking “jump-in” effects:

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

This video by [Chris Murph](https://twitter.com/highlyspammable?lang=es) has a part at the beginning where he shows how to create an effect very similar to the homeworld-hyperspace-effect! Not saying it’s done like this in Homeworld, but it’s a very cool solution! :)

This is the full video:

![](../../assets/ba0680151067ebbc.png)

gDebugger is a great free tool to see what’s going on in openGL: http://www.gremedy.com/

Thx! I’ll have to try it out! I guess it’s time for a small collection of debugging tools…could be a small list i do in form of an article. I’ll see. Thanks for mentioning!

You can achieve a similar effect on Unity 3D.

1- Use 2 cameras.

2- Camera A renders everything, except for the ship.

3- Camera B renders ONLY the ship.

4- Since they are at the same position, the image merges smoothly (think it like 2 Photoshop layers).

5- All you have to do now is to increase the Clipping Plane of Camera B.

6- ?????

7- Profit

Good idea. But wouldn’t the clipping plane cut the ship in a screen-oriented plane instead of a plane perpendicular to the ship?

p.s. And how would you “fill” the geometry hole of the cut ship?

Hmmm, you’re right. I guess it’s a little more complicated then. Maybe a dinamic Clipping Plane would work?

I have no idea how to do this on Unity :)

I don’t know. Let’s make a fire, sit there and wait for someone come by which can explain it :)

Damn…

If not with hardware clipping planes (problem I see with this is too many drawcalls, for each ship the hardware clipping planes would not be the same)

I think I would do it like this, at least for the first screenshot:

Let’s call the hyperspace planes ‘clip planes’ (not related custom clipping planes function of the graphics cards)

1. – Render everything EXCEPT ships and ‘clip planes’: this is still done in the original rendering order. Opaque objects, then background then all transparent/alpha-blended objects.

2.- ‘Clip Planes’ Draw: Now time to render the ‘clipping planes’ -> these won’t write to the color buffer, only write to the depth mask.

3.- Ships Draw: As opaque objects, DepthRead and DepthWrite enabled. What will happen is since the clip plane wrote to the depth buffer on the previous draw calls, the ships won’t be visible until the planes start ‘swiping’ and ‘clipping’ over the ship geometry. DepthRead test would be LESSEQUAL, if you want to see the ships in front of the ‘Clip Plane’ or GREATEREQUAL if you want to see it behind the ‘Clip Plane’

4.- Re-Draw ‘Clip Planes’: This time as a normal alpha blended object, probably with a bit of a depth bias to not fight for the depth written by itself the previous time. This will allow the planes to blend and be over the ships in case it is the case shown in the second gif.

If you somehow can pause the game and move the camera while the ‘hyperspace effect’ is in mid-sequence, maybe you should be able to see the ship already there.

In the second gif, we see that they actually leave some engine trails at the very beginning. Wireframe wouldn’t help because for wireframe to be drawn for those objects it would actually need to pass the depth tests the same way as when not-wireframe mode. Maybe disabling/overriding every type of depth testing will show better (if possible, the same you are forcing the wireframe mode).

Caveats:

– These ‘clip planes’ have to be big enough as to cover the whole ship from the point of view of the camera then.

Filling geometry idea:

For filling the geometry it could be an exact second pass but with the planes animation offset and the ship completely white and a bit inflated. Or the first plane pass, ship pass, and second plane pass and the extra offset plane pass increment the stencil buffer, so, somehow it is known between which stencils value to let it pass.

Would be interesting to try nevertheless.

Hi Alejandro! Muchas gracias for your very long comment and your deep thoughts! I have no idea what GREATEREQUAL/LESSEQUAL means but the rest of your argumentation sound good to me. Maybe a dev from Relic read this and tells us the thruth :)

Have a great day!

First of all, the theories of using the depth buffer are quite possible, and easy to do.

(But NOT what I think! Explanation why and how I think later.)

HOWEVER I doubt they’d hassle with clip planes… Much easier to draw a box, (using vertex colors to only show the rectangular “portal” area, to avoid extra draw calls). As more of the ship warps in, the box is scaled down. With the “pivot” being behind the ship being warped in.

The downsides of this is that the Order of the ships being rendered is VERY important, as the box can hide things behind the ship. This can be solved as mentioned before using a second camera, drawing one ship at a time…

Once again, that seems like far to much of a hassle! Yes, absolutely doable, even performance wise, especially if they are doing some good z-sorting already.

My guess:

They are simply using a smart Vertex Shader!

Combined with a trick on the plane, to create the white cuts.

Vertex shader:

Remember that the ships Front is always warped in first, right? And it warps Along the ship.

Assumption: The ships are modeled with the front facing +z. (Not important if it’s true or not, but helps make the example more understandable, as long as the model’s front is pointing along one axis!)

The vertex shader will also get a parameter every frame that tells it how much of the ship to show.

As the ship is aligned in the z axis, (in OBJECT space), the vertex shader can at that point already discard any and all pixels that in object space have a lower z value then where the portal is!

Due to max nr of characters continuing in a second post.

Continuation:

As for the white areas, I’m a good bit less sure about those, would be relatively easy if I could look at the depth buffer at different frames.

Looking at the gifs frame by frame gives Alot of clues:

The white is shown where the ship WILL NOT BE! (Frame 113 in the first gif, lower left part of the ship).

However, I’m not 100% sure this applies when seeing them from the front! (Need more angles/ships/pictures to check better).

Looking at the wireframe gif gives me the impression that it’s vertexes being thrown away, not pixels.

Without drawing each ship twice the view from the front can relatively easily be created:

Turn off backface culling, and in exchange, color all vertexes with vertex normals away from the camera, (those that would normally not be rendered, due to backface culling), and put them to a different vertex color. These veretexes can then be identified in the pixel shader, and simply return white.

However, when the warp portal is moving away from us, and the white area is obviously outside the shown vertexes, I can see NO way of getting it without extra draw calls! (Not necessarily the ship again). One way is to use the depth buffer, and when drawing the plane, (as it’s transparent it will most likely not write to it anyways!), and let the planes pixel shader sample the depth buffer (offset inwards as to make it appear as an outline), and if the value is close enough to the plane’s depth, color that pixel white. Another option is to draw the ship to a separate buffer, and when drawing the plane, it samples from that buffer

The thing I’d guess’ed most likely, drawing the ship twice, the first time using a scaled up version, (only in object space x+y, as else it might show white over something already warped in), still with the same vertex position limit, and second pass as described above.

Odd but maybe useful note: Vertexes seem to “move”, due to clipping? (They always as far as I can tell keep connections to other vertexes).

Guess:

The white is drawn as part of the plane, as I see no other vertexes that could have drawn it!

(When looking at the plane going away from us).

I hope others will come with theories as to how the white is done. However as explained in my first comment, doing the cutting off is very easy! (With the assumption they can actually code a vertex shader in that old shader variations…)

First of all: Thank you so much for taking the time to write these long comments! :)

I can try to create more footage from different angles. But i’m not sure if i understood the vertex-shader idea: As far as i know, vertex shader handle only vertices and pixel shader handle only pixels. How would a vertex shader be used to throw away all pixels behind the warp-“wall”?

A Dissolve Shader can be used, with World-Oriented UV , or Object Oriented UV, forcing the ship to have 0 Alpha and go up to 255 procedural manner.

The ”white” is drawn with Edge. On Unity’s Asset Store there are a number of Dissolve Shaders granting you the option for ‘colored edge’ where the object is dissolving in/out.

Personally I’d reconstruct this using ShaderForge in 10min (its node-based, so quite simple really. ) From there, have the Rate (speed) be a constant, that way the Plane follows along.

Recap :

Dissolve shader, uses Alpha.

World-Oriented (not Texture based, that would use local uv).

Edge Color + Edge width.

Constant Rate, so as to sync moving plane’s speed.

Few bucks on Asset Store, or DYI with ShaderForge or UDK’s built-in shader editor.

https://www.assetstore.unity3d.com/#/content/2903 Procedural Dissolve with Edge Color (Edge width too!) option.

https://www.assetstore.unity3d.com/#/content/883 yet another!

This same method of dissolving was used in Fallout 3 and Fallout New Vegas, both of which were on the Gamebryo engine, and both of which can be edited via GECK tool for a very very quick remake of the effect.

It was an Effect Shader used for their special Laser and Plasma deaths, complete with Edge Color & Edge With (bless you Bethesda, but only for this…)

(‘Dissolve In’ simply goes backward from full alpha 255, to full opaque 0, GECK even lets you set the Rate/Time d’awww)

Source = done it myself ages ago when modding Fallout and Torchlight. Doing it on UDK engine for a survival horror indie game with super-human powers, and have done it on Unity3D for an indie RTS game involving magic spells.

Many answers already, my turn :

Let say, for convenience that the ship are of length 1 and facing +x (the rear is at x=0 and the front at x=1)

Vertex shader :

position.x = max(position.x, animationState);

// with animationState ggoing from 0 to 1

// squash the front of the ship to match the portal. this will deform the ship and create holes if there are long polygons, this can be fixed with a geometry shader.

Pixel shader:

if( position >= n.xanimationState – epsilon) color = white; // the bloom will take care of the glow.

In 1999 there was none of this shader non since, so how did they do?

1) draw a translucent box (alpha = 0) covering the front of the ship. this will fill the depth buffer, it with a value close than the ship itself without altering the background.

2) draw the ship as usual, it will be cut by the depth test.

3) draw the ship in white (and without shading) with reversed normals, to fill the gap with white.

If you draw your ships back to front the there should be on flase occlusion problems.

You could also use the clip-plane thingy instead of using the depth buffer which might be faster on old hardware, but I wanted to share the depth hack anyway.

Thanks for your comment and the explanation! I have to checkout the new version of Homeworld (Remastered). Maybe there we can find more clues :)

Given the graphics for homeworld is not all that superior it’s possible they are doing a rasterization fill in the fragment shader, similar to how voxilization on the GPU is done.

When you do the rasterization, you typically create a grid of x size. If the ships never go past that one size, you can get a set of cubes that acts as a pixel representation till the next block in a sequence of time. You wouldn’t need to anti-alias, but you could blur the final result.

as for the appearance of the ship. Maybe it’s something similar to what portal has done. The object exists outside of the sphere, and as the plane moves the object appears on the other end?

Thank you for your suggestion! I’m not sure what you mean with the grid of x size. Do you mean a 2D “array” where all the fragment data is stored to? Or do you think of a 3D data type to store the depth too?

I guess we need some developer of the game or some programmer who recreates the effect to know it for sure.

I think I found something that might help with this question.

http://www.tomlooman.com/the-many-uses-of-custom-depth-in-unreal-4/

thanks for the link! it’s a great idea and i think for just one ship this might work. there you could write the ship in the depth buffer and cut the values dependant on their depth value but i guessit would be hard to do this with multiple ships which are at different locations in the universe … wouldn’t it?

Probably not if each ship is processed independently.

Algorithimically, the way I see this is that ships are not batched together. Each ship are seperate draw calls. Treat each ship independently to a clipping plane in the shader to cut off portions of the ship as the plane moves.

The plane will be calculated in a seperate draw call, and will be using Z-tests to create it’s image. If not Z-tests, then maybe just a polygonal intersection test.

This might cause some overhead, but honestly Home-world is a fairly graphically simple game. It can afford to take the hit.

Nice thought, having the ships calculated independently could work I’d guess. :)

Run into an nice asset on unity asset store.

I think it reproduces such effect.

Share it with you => http://u3d.as/hgX

I have a solution although it may not be the solution used in homeworld.

What if there is no plane doing the culling? (The plane is just a z-depth effect but the culling effect is separate).

The material can be two passes on a ship. One pass into the stencil buffer of the part of the ship to be shown, and the second pass to draw the ship only where the stencil buffer had written the pixels prior (pixels discarded otherwise).

To decide which pixels to be written to the stencil buffer you can threshold an alpha value (alpha cutout) decided by object position (pass a varying value from the vertex shader to the fragment shader that is interpolated based on vertex X position for instance). The threshold would just be a uniform that increases over time to “reveal” it. This first pass should not write into the depth buffer.

The second pass just draws the ship normally where the stencil value is written to (and sets the value back to zero for other ships).

Unlike other examples people mentioned, this would work with multiple ships overlapping each other as there is no real clipping “volume” or camera trickery. Ideally after the effect is done the ships should swap materials to a shader that doesn’t do this effect for performance.

I made a comment before about how 2 passes could be done using the stencil buffer but looking back on it, the solution is much easier (and actually correct unlike my other solution which has problems).

Just alpha-cutout in the fragment shader the parts of the ship with an X position value greater than whatever your “plane” is at (shader uniform). The X position just comes from a varying value set in the vertex shader of the vert position.

The plane itself is only a quad with a z-depth effect done after and is unrelated.

thanks for your thoughts :) i wonder if this would also “close” the cut so that you can’t look “into” the ships belly.

This effect is trivial with modern shaders, but these games predate shaders as we know them today and would have been running OpenGL 1.1 or 1.2. Homeworld was originally announced in 1997 just months after the first release of OpenGL!

Stencils would have been plausible with OpenGL 1.1, but unlikely. Especially since the effect still “works” when wireframe is enabled. That also rules out clipping planes since the entire ship is still being drawn.

That leads me to think this was done with a panning UV and alpha test. The interior is probably rendering the ship a second time, inverted, and with a solid white color.

Hi Simon,

Long ago Relic Developers Network (RDN) released the Homeworld source code (if my memory serves me right sometime around 2003?)

There are a pair of files called hs.h and hs.c that spell out how the hyperspace effect is done. It uses glClipPlane along with disabling backface culling. The rectangle that is drawn is just for visual effect:

https://github.com/aheadley/homeworld/blob/master/src/Game/hs.h

https://github.com/aheadley/homeworld/blob/master/src/Game/hs.c

HW1: Remastered and HW2 use a slightly nicer-looking method because it shows a glowing outline of the ship on the rectangle – I don’t remember the original HW1 having this, and I didn’t find any references to this effect in the file.

Ohhhh that’s interesting! Thank you!!!

I didn’t know you could pass arbitrary clipping planes to OpenGL, that’s nice! And probably much more efficient than any other solution given here!