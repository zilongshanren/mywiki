---
title: Animating Water Using Flow Maps
url: http://graphicsrunner.blogspot.com/2010/08/water-using-flow-maps.html
author: Kyle Hayward
published: '2010-08-03'
source_blog: Graphics Runner
source_site: http://graphicsrunner.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![flow flow](../../assets/757ff68fa0ba2da5.img)


Last week I attended SIGGRAPH 2010, and among the many good presentations, Valve game a talk on the simple water shader they implemented for Left For Dead 2 and Portal 2. So on the plane ride back from LA, I whipped up this little sample from what I could remember of the talk. Edit: You can find the talk here:

[http://advances.realtimerendering.com/s2010/index.html](http://advances.realtimerendering.com/s2010/index.html)

The standard technique for animated water is scrolling normal maps, as I’ve previously written about. The problem with this is that it looks unnatural as water does not uniformly move in one direction. So Valve came up with the idea of using flow maps ( based on a flow viz paper from the mid 90s ). The basic idea of flow maps is that you create a 2D texture that you will map to your water. And this map will contain the flow directions that you want the water to flow, with each pixel in the flow map representing a flow vector. This allows you to have varying velocity ( based on length of the flow vector ), and varying flow directions ( based on the color of the flow vector ). You then use this flow map to alter the texture coordinates of the normal maps instead of scrolling them. Lets get to work :)

**The Flow Map**

First we need to create a flow map. Here’s what I came up with in a couple of minutes in Photoshop. This flow map was designed around the column with dragon scene as with the previous scene. Note, this flow map is greatly exaggerated to demonstrate the effect.

![flowmap flowmap](../../assets/60c37ddf2b314cac.img)


**Using The Flow Map**

Now we need to use the flow map to alter the water normal maps. We do this by taking the texture coordinate of the current water pixel and offset it using the flow vector from the flow map based on a time offset. We then render the water as we did in the previous water sample. But there’s a problem with this, after awhile the texture coordinates will become so distorted that the normal maps will be stretched and will have nasty filtering artifacts. So to solve this we limit the amount of distortion of the texture coordinates by resetting the time offset. This solves the over-distortion, but now the water will reset every X seconds. So we introduce another layer, that is offset from the first by half a time cycle. This will ensure that while one layer is fading out and beginning to reset, the next layer is fading to where the last layer was. Here’s a diagram to visualize this phase-in phase-out of the 2 layers.

![graph graph](../../assets/fbcf7451e1ed9f99.img)


The graph illustrates that during a cycle time from 0 to 1, we want the layer to be fully interpolated at the mid-point in the cycle, and fully un-interpolated at 0 and 1. Lets see the code:

//get and uncompress the flow vector for this pixel float2 flowmap = tex2D( FlowMapS, tex0 ).rg * 2.0f - 1.0f; float phase0 = FlowMapOffset0; float phase1 = FlowMapOffset1; // Sample normal map. float3 normalT0 = tex2D(WaveMapS0, ( tex0 * TexScale ) + flowmap * phase0 ); float3 normalT1 = tex2D(WaveMapS1, ( tex0 * TexScale ) + flowmap * phase1 ); float flowLerp = ( abs( HalfCycle - FlowMapOffset0 ) / HalfCycle ); float3 offset = lerp( normalT0, normalT1, flowLerp );In the code above, HalfCycle would be .5 if our cycle was from 0 to 1. We can see here that we unwrap the flow vector (as it is stored in [0,1] and we need it in [-1,1]), fetch the normals using the flow vector and then lerp between the two normals based on the cycle time. This however will lead to a subtle pulsing affect, which I couldn’t really notice when the water was rendered, but I included the fix for completeness. To fix this pulsing effect, we perturb the flow cycle at each pixel using a noise map.

//get and uncompress the flow vector for this pixel float2 flowmap = tex2D( FlowMapS, tex0 ).rg * 2.0f - 1.0f; float cycleOffset = tex2D( NoiseMapS, tex0 ).r; float phase0 = cycleOffset * .5f + FlowMapOffset0; float phase1 = cycleOffset * .5f + FlowMapOffset1; // Sample normal map. float3 normalT0 = tex2D(WaveMapS0, ( tex0 * TexScale ) + flowmap * phase0 ); float3 normalT1 = tex2D(WaveMapS1, ( tex0 * TexScale ) + flowmap * phase1 ); float flowLerp = ( abs( HalfCycle - FlowMapOffset0 ) / HalfCycle ); float3 offset = lerp( normalT0, normalT1, flowLerp );And that’s pretty much it. I’ll update the post/source when the slides are posted from SIGGRAPH in case I left anything out. Video time!

Source/Demo:

[WaterFlow Demo](https://onedrive.live.com/download?cid=B80A3031B5BFA52B&resid=B80A3031B5BFA52B%21246&authkey=AOZzjISSdDuad44)

## 48 comments:

Awesome! Wanted to implement that algorithm myself after the presentation :)

It's such a neat (and somehow simple but amazing) technique, so that I assume we will get to see it more often in future games.

As ever awesome stuff, downloading it now to have a play :D


Thanks.

Looks great!

Looks nice. Did the Valve talk cover any other topics?

Hi Kyle,



This article looks awesome, I can't wait to get home and try it out.

thanks a lot for posting.

-John

Woh, glad to see people still read this thing :)



Hope you guys still liked after downloading it...

@dlai - Valve didn't talk about any other effects, but they did talk about why they implemented this. Apparently people were getting lost in swamp levels of LFD2, so they added this flow to guide the player. They said they saw an 18% decrease in players getting lost, and that they also finished the map faster.

The scary thing is I coded something very similar to this three months back for water intense game for a now defunct studio.


Woot ten points for being on the same wavelength as Valve... this makes me happy.

Looks cool, man thank!

yep, the technique to be seen everywhere for the end of 2010, takes less than an hour if you already have some nice water assets lying around. :)

BTW if you get the NVIDIA SHader Library "Paint Brush" sample for FXComposer, replace the bruch color with this:





QUAD_REAL3 dir_color(uniform float3 MousePos, uniform float4 MouseL)

{

QUAD_REAL2 dirVec = MousePos.xy - MouseL.xy;

dirVec = normalize(dirVec);

dirVec = 0.5 + (0.5*dirVec);

return QUAD_REAL3(dirVec.xy,0.5);

}

instant directional-paint tool

ooooohh nice :) I was hoping photoshop would have something like that built in. Valve used houdini to import their level, create flow vectors, and comb them in the direction they wanted.

Nice implementation! :)

I wanted to implement this method also!

Interestingly the guy from Valve did not correctly attributed the flow idea. It was developed in Naughty Dog by another person and used in the Uncharted games.

Thanks Sebastien :)


@Anonymous: Hmm I'll have to go back and look at Uncharted's water.

Anonymous, the idea of "flow maps" goes back well before that, they've been used for particle effects and hair grooming for quite a while.

Yep Anonymous(A) is correct. This idea maybe old and used on Particles and Hair Grooming previously.



However, to my knowledge this was not correctly credited. Naughty Dogs Uncharted games were indeed the first to use Flow in this way.

Credit where credit is due!

Cool web site, I had not noticed graphicsrunner.blogspot.com previously during my searches!

Carry on the good work!

Nice,

but I don't understand how the noisemap is supposed to prevent the pulsing behavior. If you want to make sure you see the pulsing, use to artificial normal maps, say one with a circular pattern and one with a rectangular. With those patterns you will see the the wave pulsing over the whole image. The noisemap seems only to shift the waves slightly in position.

Is it right that you use two diffrent normal maps?


(WaveMapS0 / WaveMapS1)

And thanks for sharing!

@Anonymous1


Yes the noise map does not completely prevent the pulsing, but it does a fairly good job of hiding it, by having each pixel start at a different time in the phase. The pulsing was still noticeable in Valve's presentation too after applying the noise map.

@Anonymous2

I don't think it's correct or incorrect since this is not physically based. Valve used 1, but I decided to use 2 to have more variety.

Hi Kyle,


I think the idea was to indeed shift the phase, which will help in reducing the pulsing as different parts reset their animation cycle at different times. However I think that in your implementation it just shifts the texture lookup in position, not in time.

Ahhh yep. You're correct. The original code made sense on my red eye flight :P. I'll update the post soon.

Hi Kyle,



I'm trying to add some directional waves in, so I made my normal textures with long waves (long in one direction, short in the perpendicular direction). It's a good start, but if the flow is not in the direction of the waves, I want to rotate the waves. I cannot get that to work. I almost gave up, but now I'm thinking of the same trick with mixing two textures in time but in addition mix it in position, so I could locally rotate the waves in a particular direction. I guess it could also be used for waves with different frequencies.

If someone has good ideas for this...

Based on the idea of this blog entry, somebody wrote a test and demo application with the Ogre engine.

It simulates flowing water of rivers:

http://www.ogre3d.org/forums/viewtopic.php?f=11&t=60363

Pretty cool. Thanks for the link :)

I feel like swimming now, good looking demo! Nice and simple technique. It always looks stupid when a quick moving water plane intercepts the land, but with this you can reduce the flow at the shallows. One thing though, how to maintain a certain resolution for bigger scenes? Multiple textures?

This is all well and good, but what about realtime ripple interaction with the player?


MM

Any chance you can post a video where you aren't moving the camera around at all (e.g. no fly-by's) It is kind of a pain to look at the effect and see how it works when the camera is moving so fast.

Now look at this... a totally different approach. http://goo.gl/gcXQ

I will put up a description soon.

Cool stuff :) Do you have a write-up?

no, no write up. I just finished the first implementation. I'll put up the sourcecode very soon.

new video at:

http://www.youtube.com/watch?v=TeSuNYvXAiA

source code (not packed together yet) at

http://www.ogre3d.org/forums/viewtopic.php?f=11&t=60363&start=25

Cool! Thanks for the link :)

Finally, code ready for download, complete with images, from http://www.rug.nl/cit/hpcv/publications/watershader

Very nice!

Hey,


I've ported most of this to XNA 4, but the shader .fx is failing to compile when trying to add the refl and refr matricies to the watercolor and sun fields (right before the return)

Any idea what's going on? It's failed to compile from the get go, but I've nailed it down to that line.

What's the error that fxc is reporting?

Error 1 Errors compiling C:\[...]\WaterFlowDemo\WaterFlowDemo\Content\Shaders\Water.fx:


C:\[...]\WaterFlowDemo\WaterFlowDemo\Content\Shaders\Water.fx(261,24): ID3DXEffectCompiler::CompileEffect: There was an error compiling expression

ID3DXEffectCompiler: Compilation failed C:\[...]\WaterFlowDemo\WaterFlowDemo\Content\Shaders\Water.fx 261 24 WaterFlowDemo

Is the error, but it compiles if I change

finalColor.rgb = WaterColor * lerp( refr, refl, f) + sunlight;

to

finalColor.rgb = WaterColor + sunlight;

Also, you wouldn't know how to convert the clipplanes into an oblique frustum clip would you?

Ah that's right xna 4 doesn't have clip planes.







There's a simpler solution than oblique frustum clipping. Just use the 'clip' semantic in the pixel shader.

This is how I clipped geometry with the O3D version of the water game component.

Putting this at the top of the phong shader should do it:

clip(ClipHeight - height);

Where ClipHeight is the position.Y of the water plane, and height is the position.Y of the current pixel being rendered.

Have a look at the WaterScene.html from the sample code in the Water in your Browser for more info.

I was told about this technique by a coder at work.. now I'm trying out a method for creating the flowmap texture using particle simulations in Softimage. Check it out: http://vimeo.com/29728577

Very cool! I need to try that and Houdini( the tool that Valve used to author flow maps ).

For smaller values of flowSpeed everything is fine, but for larger values the water surface is getting extremely distorted. Is there any solution to this problem?



Here's how do the FlowMapOffset calculation:

flowMapOffset0 += flowSpeed * Time.deltaTime;flowMapOffset1 += flowSpeed * Time.deltaTime;

if ( flowMapOffset0 >= cycle )

flowMapOffset0 = .0f;

It's been awhile since I've looked at this, but I believe it's a fundamental problem with the approach.

Hi.



I'm trying to create this feature, and, there is one moment...

if I use noise map for texture offset, I get this

http://img826.imageshack.us/img826/1615/offset.gif

so, I think, that noise map must be used not for texture offset, but for phase offset.

if phase changes 0...1...0

with noise map it will look like 0 -> some white spots expands -> 1 -> some black spots expands -> 0

but I can't figure out that formula

:)

finished!

https://www.dropbox.com/s/ii2x077vj64lyhl/Water%20Flow%20For%20UDK.pdf

Post a Comment