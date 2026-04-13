---
title: Major C#/.NET graphics framework update + volumetric fog code!
url: https://bartwronski.com/2014/08/20/major-c-net-graphics-framework-update-volumetric-fog-code/
published: '2014-08-20'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

As I already promised too many times, here comes major [CSharpRenderer framework](https://bartwronski.com/2014/04/10/c-net-graphics-framework/) update!

As always, [all code available on GitHub](https://github.com/bartwronski/CSharpRenderer).

Note that the goal is still the same – not to write most beautiful or fast code, but to provide a prototype playground / framework for hacking and having fun with iteration times approaching 0. 🙂 It still will undergo some major changes.

Apart from volumetric code as [example for my Siggraph talk](https://bartwronski.com/publications/) (which is not in perfect shape code quality wise – it is supposed to be a quickly written demo of this technique; note also that this is not the code that was used for shipping game, it is just a demo; original code had some NDAd and console specific optimizations), other major changes cover:

## “Global” shader defines visible from code

You can define some constant as “global” one in shader and immediately have it reflected in C# side after changing / reloading. This way I removed some data / code duplication and potential for mistakes.

Example:

// shader side #define GI_VOLUME_RESOLUTION_X 64.0 // GlobalDefine // C# side m_VolumeSizeX = (int)ShaderManager.GetUIntShaderDefine("GI_VOLUME_RESOLUTION_X");

## Derivative maps

Based on old but excellent [post by Rory Driscoll](http://www.rorydriscoll.com/2012/01/11/derivative-maps/). I didn’t see much sense in computing tangent frames in mesh preprocessing for needs of such simple framework. I used “hack” of using normal maps as derivative map approximation – doesn’t really care in such demo case.

## “Improved” Perlin noise textures + generation

Just some code based on state of the art [article from GPU Pro by Simon Green](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter26.html). Used in volumetric fog for some animated, procedural effect.

## Very basic implementation of BRDFs

GGX Specular based on a very good [post about optimizing it by John Hable](http://www.filmicworlds.com/2014/04/21/optimizing-ggx-shaders-with-dotlh/).

Note that lighting code is a bit messy now, its major clean-up is my next task.


Minor changes added are:

- UI code clean-up and dynamic UI reloading/recreating after constant buffer / shader reload.
- Major constants renaming clean-up.
- Actually fixing structured buffers.
- Some simple basic geometric algorithms I found useful.
- Adding shaders to project (actually I had it added, have no idea why it didn’t get in the first submit…).
- Some more easy-to-use operations on context (blend state, depth state etc.).
- Simple integers supported in constant buffer reflection.
- Other type of temporal AA – accumulation based, trails a bit – I will later try to apply some ideas from
[excellent Epic UE4 AA talk](https://www.unrealengine.com/resources). - Time-delta based camera movement (well, yeah…).
- Fixed FPS clamp – my GPU was getting hot loud. 🙂
- More use of LUA constant buffer scripting – it is very handy and serves purpose very well.
- Simple basis for “particle” rendering based on vertex shaders and GPU buffer objects.
- Some stupid animated point light.
- Simple environment BRDF approximation by
[Dimitar Lazarov from Black Ops 2](http://blog.selfshadow.com/publications/s2013-shading-course/lazarov/s2013_pbs_black_ops_2_notes.pdf)

## Future work

Within next few weeks I should update it with:

- Rewriting post-effects, tone-mapping etc.
- Adding GPU debugging
- Improving temporal techniques
- Adding naive screens-pace reflections and an env cube-map
- Adding proper area light support (should work super-cool with volumetric fog!)
- Adding local lights shadows

Reblogged this on Dinesh Ram Kali..

Is there anyway to only output the ambient occlusion output ?

(I tried disabling a few things in the C# code but it messes the rendering)

Hey, debug modes is a next coming big feature (ETA 1-3 weeks). Meanwhile it should be trivial in the C# code for debugging – do a temp copy pass to a temp target and then replace main framebuffer with it during final resolve. 🙂

Or just use EXCELLENT RenderDoc https://github.com/baldurk/renderdoc

Yea thanks, I got it to work by replacing the line :

source = currentFrameMainBuffer;

to :

source = ssaoRT;

A little bit of context, I’m trying to port Scalable Ambient Occlusion to DX9. Since I can’t even run the SAO reference implementation demo on my PC (it crashes no matter what I setup/install/try) I’m going to use your amazing framework to see how it looks and works 🙂

Oh by the way at this point I could use some help from a knownledgeable person like you if you still remember a bit about how SAO works because I’m having a really hard time getting it to work and… I don’t even know where to start :

My depth is properly retrieved and linearized (it’s okay when displayed on screen), my reconstructed normals somewhat look ok :

![](https://i0.wp.com/abload.de/img/screenshot_2014-09-07r9kbz.png)


Probably “a bit too blue” ? I was told blue wasn’t okay for normals as it could be a sign they’re not in the right space. But I could be wrong. Now the annoying thing is that I get a black screen (how incredibly informative) when trying to output the result of occlusion (i.e the variable ‘sum’ where occlusion is supposedly accumulated).

I should mention that I’m not working with a particular game engine but with an injector that hooks DX9 games and injects SSAO on top of them. The downside of that is that I don’t have access to the game original matrices (projection/world…) so I copied your g_ReprojectInfoFromInt routine and incorporated it into my code. I think it should be ok but obviously it’s not. There must be something missing I don’t know. The full shader can be found here :

http://pastebin.com/vqUQwKj2

I’m sorry this is a bit off topic I should have PM’ed that maybe. Let me know if this is a problem

Hi, no problem for the offtopic. 🙂 The normals would look “ok” if they were in for instance world-space. They definitely wouldn’t look like that in camera space the algorithm is using. All the edges should have some Z/blue components in them, not just some and only saturated… So I guess reconstruction (passed matrices) could be wrong indeed.

Thanks for the pointer !

Keep up the great work. Love your photos too btw

Hello, maybe I am blind but I cant see the perlin noise effect in the exe. Or does it need to be turned on/up?

Hello, yes it is pretty subtle and tweaked to look good (like fog, not clouds of smoke) – you can tweak and edit shader files – volumetric_fog.fx – manually and boost it as much as you want. 🙂

Just saw your latest debug visualizer update for your C# graphic framework, great job Bart

Can I ask you one last question ? Since you’re working in the game industry you should be able to spot the issues at once.

So I’ve been working some more on SAO and I seem to be getting somewhere, at least I hope so. Can you tell me if this is ok -just looking at it :

Game is Devil May Cry 4 (it could be any dx9 game really but I like seeing the SSAO output on architecture -and I like.. architecture). It probably needs toning down. I’m still tweaking it. But other than that if you can spot glaring issues feel free to tell me. Another shot with different nearZ/farZ settings (I have to tweak these manually in the shader file for each game since I can’t retrieve the exact original values from the game -unfortunately) :

This is my last semi off-topic post. Once again sorry. And thank you for being so accessible as a developper. Bonjour from France !

Hi Michel! Results you got look like plausible SSAO – but probably a bit too dark. I think you could be suffering from some self-occlusion artifacts. Usually in games we “bias” SSAO contribution and ignore small depth differences when computing the occlusion factors. Need to do so comes from the fact that a) depth reconstruction precision is limited b) geometry face normals don’t match normals authored by artists. In scalable AO code you can see “static const float bias = 0.02f;” value which is used exactly for this purpose. If you make SSAO less intensive and less self-occluding, it should look good! 🙂 Cheers!

Thanks a lot I had overlooked the use of the bias variable. It’s been working well to some extent now that I have incorporated it in my tweaking session but I still get a very “polygonal look” (even going as far as bias = 0.04f). But I’m afraid it’s bound to happen when working solely with face normals I guess (unblurred AO output) :

Another thing I’m concerned about is the little artefacts here and there -depending on the scene- like ghosting artefacts around the edges :

But I think it has to do with the fact that I have to “guess” the nearZ/farZ values from the game and manually input them in my shader (yeah I know). That is a real weakness in my setup but I’m afraid I won’t be able to do much about it.

I still haven’t implemented mipmapping like the original paper suggests. I wonder if it makes a big difference. I’ll try to do that. Temporal supersampling looks convincing as well from your blog post

(I wish I could PM you all this Bart instead of spamming your blog but you don’t seem to have a public email, do you ?)

The polygonal look will be there – as you said it is because of use of depth buffer and face normals. For the second kind of artifacts IMO they are simple ringing / undersampling and will be there… Z reconstruction can add to it as well. And for the mip maps – they will only increase problems / artifacts, not decrease them. They are “only” for performance. For the temporal supersampling I’m afraid that with only camera motion reconstruction (if you don’t have motion vectors buffer) it will produce hard to avoid ghosting.

Many thanks. Very helpful !

Hello!

Since I’m newbie in a game development, I have one question about your Volumetric fog – maybe you know, does anyone implemented it for UE4 in some way? (if no, probably, I will try to do it by myself, while it will take a lot of time 🙂 )

Hi Alexey! I have no idea about UE4, you’d need to ask Epic… But most recent game engines have this technique! 🙂 All Ubisoft Scimitar games, Far Cry: Primal, Frostbite (by Sebastien Hillaire), Unity3D (port by Robert Cupisz), latest Call of Duty game or Eidos Montreal titles. So I wouldn’t be surprised if UE also had it, but as I said – I have no idea… Cheers!

Hi Bart,

how i can change tonemapping shader in order to use 10bit render-target insted of 8bit classic one.

I make classic light calulation and bloom hdr on a 16bit rendertarget, at the end i would use a 10bit one. I want to test an hdr monitor tha have a 10bit display panel. I gooogled this but i didn’t found any sample about.

Thanks in advance,

cheers.

Hi Andrea! I have literally zero experience with it on Windows (only on PS4), so won’t be much help and sorry for that. 😦

As far as I know, so far HDR is supported only by nVidia and requires some extensions / nVidia SDK. You can find some information on their website together with a sample https://developer.nvidia.com/high-dynamic-range-display-development . I hope this helps you at least a bit…

Cheers,

Bart