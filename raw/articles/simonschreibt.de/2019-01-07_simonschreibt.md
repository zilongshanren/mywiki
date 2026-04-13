---
title: Simonschreibt.
url: https://simonschreibt.de/gat/river/
author: Simon
published: '2019-01-07'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](https://data.simonschreibt.de/gat069/thumbnail_youtube_01_forward.png)


![](../../assets/4d91614db59804c6.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

# Preface

![](../../assets/cef2e62a8ddb42a9.gif)

This article was originally an [interview for 80lv](https://80.lv/articles/006sdf-river-simulation-with-simonschreibt/). For the 2k19 edition, I ditched the introduction but added **more content**:

- Advanced alignment & placement of particle systems around the obstacles (
[jump to section](https://simonschreibt.de#New-Flow-Detection)) - Automated Reflection-Probe placement (
[jump to section](https://simonschreibt.de#New-Reflection-Probes)) - New river-related tutorials in
[my Houdini Youtube Channel](https://www.youtube.com/channel/UCHKNOUwxyld0UVTIOk4E0zw/videos) - This article in form of a video for all who think reading is sooo 2018 :)

Further credit & information:

- You can download the
**Unreal and Houdini Assets**[here](https://data.simonschreibt.de/gat069/HoudiniRiver.zip). - For a major part of the project I followed tutorials by
[Ben Schrijvers](https://www.linkedin.com/in/bensch/?originalSubdomain=nl)and[Andreas Glad](http://partikel.co/). - Don’t be afraid of Nodes and Scripts. It’s not as hard as it may look.
- For the water I used a normal-map from the Unreal Starter content.

# What are you trying to build?

I wanted to learn how to make a procedural generated river for the [Realtime VFX River Challenge](https://realtimevfx.com/c/Events/17-river) but had no idea how to start. Accidentally I stumbled across this amazing [tutorial from Ben Schrijvers](https://www.sidefx.com/community/horizon-zero-dawn-guerrilla-games/) where he talks about the rivers in [Horizon Zero Dawn](https://www.guerrilla-games.com/play/horizon). I was hooked and had to try it out!

![](../../assets/516fdfedf754ac43.png)


![](../../assets/516fdfedf754ac43.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

By the way, there is another really cool [Houdini river tutorial](https://vimeo.com/243733565) by [Andreas Glad](https://twitter.com/PartikelVFX):

![](../../assets/caa784f81f61d53f.png)


![](../../assets/caa784f81f61d53f.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

These videos where my main foundation and helped a ton to get everything started.

# How did you build the landscape?

The terrain was super-complex. Let me illustrate the creation-process with a video to make sure everyone can follow along:

Just kidding. The shelf-tools make it very easy to create a terrain. I just set a smaller size and it was ready to go.

# What is the way you’re building the river itself?

The first steps are 100% copied from [Bens tutorial](https://www.sidefx.com/community/horizon-zero-dawn-guerrilla-games/) and they are fascinating. First, you create a spline and let it “fall down” on the terrain. This is done by reading the height of the terrain at the spline-point-positions and then moving the points to this height (in my case the points are moved upward to match the terrain-height because my spline was place below the terrain):

Next, you let the spline-points “roll” down the hill to integrate the river a bit better to the terrain:

Actually, they do not roll in a physical way. Instead, you use the underlying surface-normal and the normal of the point to calculate a local axis for each point (which points away from the spline and down the hill). Then, you move the points along the calculated axis a little bit (this process is documented very well in Ben’s video).

The next step is to make sure, that the river does not flow upstream in case the terrain directs it to (because there’s a little hill where the river goes along).

![](../../assets/e58263d5764b4a16.png)

A little Python script makes sure that a spline-point is never higher in 3D space than the point before on the spline:

Another nice trick for a more natural appearance is to avoid **continuous** slopes but instead let the river flow in steps (for better visualization I show the river-**geometry** here, but actually we’re still only working with a single spline for now).

Finally we reach a step where I contribute my own ideas: I add colors to the spline to mark where a slope is (green), where it starts (turquoise) and where it ends (red). This will help me later to blend different water-textures and place particle systems.

![](../../assets/2b0a21946c8e4382.png)

Let’s go a little bit faster over the river-geometry-creation since all of that is perfectly fine explained in Ben’s video. The most important point is, that only the **outer** edges of the river get aligned again with the terrain (like we did with the spline in the first place):

# How did you manage to achieve the deformation of the landscape where the river flows?

Again, it’s 100% Ben’s workflow but it starts by moving the terrain **below** the river geometry so that it does not intersect in any way:

Then, for every point in the terrain, you shoot a ray upward. If it hits the river geometry, this point will be moved upward to the hit-position:

Every point which didn’t hit anything, gets its **original** height assigned again:

Here you can see how everything behaves now, when you change your spline:

Then the terrain height-field gets converted into polygons and re-meshed. Now it’s ready for being used in Unreal:

Even if it’s not part of the question, I would like to add some details about UVs, Materials, Flow-Maps etc.:

## River Geometry

The river geometry you saw **before** was just used to carve the terrain. The **actual** river is a bit thinner, got UVs and was subdivided (note, that my slope-colors are still there):

![](../../assets/942a1d4eec9e0f66.png)

## UV Generation

Talking about UVs: Since the spline always varies in length, the UVs must adapt to that. Luckily this is very easy in Houdini. First you create your UVs in the 0-1-UV-Space and then you measure the spline-length. This value can be used to scale the UVs. Here you see me changing the spline and in the **lower** part you see how the UVs auto-adapt. Believe me, if you experienced this once, you never want to manually create UVs anymore :D

## Riverbed

Another detail: I wanted to make the river bed darker and wet. To do that, I shoot some rays from every terrain-polygon upward and if I hit the river, I assign a color to all **points** of that polygon. The created mask looks like this:

![](../../assets/2814597f4196ac86.png)

And here is an example how much difference it makes when using the mask in a material to assign different diffuse and roughness values:

## Flow-Map

Generating the flow-map for the river is super easy with Houdini. You just tell a special node “This is my river geometry and this is the spline which indicates the river-direction” and boom, your river geometry suddenly has vertex colors assigned representing the flow of the river:

Another node can be added which makes the flow-map react to obstacles. Now the water can flow around them:

And the best: You can trigger the baking of the flow-map in Unreal! No need to switch back and forth between Unreal and Houdini. Just expose the Houdini-“Render”-Button as Parameter. Here you see me changing the obstacles and then render a new flow-map (note: the baking takes a longer time than in the video):

### New: 3 Flow Map Errors to avoid

I made a [video about 3 mistakes](https://youtu.be/YpXczzOtsHc) I made while baking the flow map and hopefully it will help you to avoid those.

## Foam Mask

To get some foam on the water around obstacles, I use a so called “isoOffset”-node. It stores basically the distance to an object into the vertex color of the river. Then I spice it up with a little noise and the mask is good to go:

To make the foam-mask less static, I use a simple Photoshop cloud pattern which I move along the river and subtract it from the original mask. This adds a more interesting feel:

And since we’re talking about foam: The cascades get a simple foam texture too, which is only shown at the slope of the river (I masked this slope at the beginning with vertex colors when I was creating the spline). The foam structure is scrolling faster than the river water:

## Particle Systems

Because I stored where top and bottom of my cascade are, I can now filter those elements (these lines where used to generate the river-geometry), create a point in their center and copy a dummy-cube to this point which will exchanged against a particle system in Unreal later:

For the particles around the obstacles, I’m using a nice node called “Intersection Analysis” to get the intersection of obstacles and river. Those intersection-edges have points. To a random number of those I copy a dummy-box again (which is exchanged against an particle system in Unreal later):

### New: Flow Detection

I’ve extended this system by detecting if the particle system was placed in front of an obstacle (in comparison to the flow-direction of the river) or behind. With that, I can use different particle-effects depending on if the water “crashes” head-on into an obstacles or flows more relaxed around it:

The particle systems on the front are aligned by the normals of the obstacle:

Also, I detect the flow direction now (by reading out the v-Attribute from the river points in Houdini) and be able to align the particle systems according to that (I explain the procedure in detail in [this tutorial video](https://youtu.be/Xjmskl3hl1c)).

The particle systems “behind” the obstacles are aligned with the river flow:

Here I show how it looks when I assign two different particle systems:

## New: Reflection Probes

**Important**: I didn’t use this at the end since my Unreal-SkyLight was already capturing a nice cubemap. But maybe this workflow is useful for someone out there. :)

Reflection Probes are basically cameras and do capture the world from their point of view providing shiny surfaces with better reflections. I wanted to have them placed along the river in periodic intervals.

To be able to use a Reflection Actor here, you have to encapsulate it in a **Blueprint** (see below). I also made [a tutorial video about this](https://youtu.be/nz5_kJ3bskI).

![](../../assets/1bfa8cc3cace1914.png)

# How are you going to prepare and export this project into Unreal?

The so called [Houdini Engine](https://www.sidefx.com/products/houdini-engine/) is a plugin for Unity, Unreal, 3Ds Max, Maya and Cinema 4D and executes the node networks you create in Houdini directly in the mentioned programs. So what I have to do, to make the terrain and river show up is to save my Houdini-File as Digital Asset. This can be imported and used like any other asset in Unreal:

Now, I can change parameters (which I exposed in Houdini) or change the spline to make the river take a different road:

The materials are still created and assigned in Unreal **but** you can pre-assign materials ([you can find my tutorial about this here](https://youtu.be/U4uLy1P3X4g)).

Of course, it’s not perfect yet. Further improvements would for example be: avoid placing obstacle-particles “behind” objects (away from river flow direction), setting the orientation of the obstacle-particles along the flow-map so that particles move into the direction of the flow, accept Unreal-Terrain as Input, improve performance of the node-network so that changes on the spline get calculated faster, narrowing/extending the river-width depending on the area (like in Ben’s video), …

# Overall, how difficult is setting up this type of asset and using it in games?

Yes, Houdini has a steep learning curve. And since the game dev tools are brand-new, sometimes you will find bugs, anomalies in the documentation or you’ll struggle to get the output as you want it to be.

But that’s a common situation for game developers, isn’t it? We’re often working with cutting-edge technology which has to be tamed first. Most importantly: you’re not alone. The [Thinking Procedural Discord](https://discordapp.com/invite/b8U5Hdy) is full of very nice people which are eager to learn and help. You can even find Sidefx developers in those chats!

# The End.

Thanks to Damien, lKruel, mgw, Ambrosiussen, Glad and Julián (all from [“Thinking Procedural” Discord](https://discordapp.com/invite/b8U5Hdy)! Wouldn’t have been possible to finish the project without you.

# Links

- You can download the Unreal and Houdini Assets
[here](https://data.simonschreibt.de/gat069/HoudiniRiver.zip). Here is an[Installation video](https://youtu.be/9nFlCxEx4XI). - Discord:
[Houdini “Thinking Procedural”](https://discordapp.com/invite/b8U5Hdy) [Houdini river Tutorial by Ben Schrijvers](https://www.sidefx.com/community/horizon-zero-dawn-guerrilla-games/)[Houdini river tutorial by Andreas Glad](https://vimeo.com/243733565)- Simon’s
[River Challenge Thread](https://realtimevfx.com/c/Events/17-river)with more details - Simon’s
[Talk containing the Liquid Implementation](https://www.youtube.com/watch?v=aYZEmaQUrAo)in “The Invisible Hours” - Simon’s
[Unreal](https://www.youtube.com/channel/UC9go9jWq2w4iDdZ162ulmug/videos)and[Houdini](https://www.youtube.com/channel/UCHKNOUwxyld0UVTIOk4E0zw/videos)Youtube channel [Vertex-count-agnostic Morph Targets by Norman Schaar](http://norman3d.com/TextureMorphTargets/Vertex-count-agnostic_Morph_Targets.pdf)

I can totally recommend checking out the software. Every day new amazing tutorials appear and the game dev tools are a great way to use the software not “just” for baking out some simulations into flip books but improving the workflow in a way, that classic workflows feel like stone-age.

Reminds me a little of this: https://steamcdn-a.akamaihd.net/apps/valve/2010/siggraph2010_vlachos_waterflow.pdf

Yeah! I didn’t re-visit this PDF for the project but I know it and it’s fascinating that they did the same already ages ago. These Valve-Guys did a fantastic job … back then when they where still creating games :D

Awesome stuff you got! Got some great new ideas because of you and Ben. Thanks a lot!

Hi Simon, btw for some reason this hda crashes Houdini when I try to install the asset with “install asset library”, it cooks for a minute then crashes without an error. I’ve recreated most of the tool from the Guerilla Games video but still have some stuff unfinished, like coloring the curves, UVs and placing the rock and particle proxies.

Any idea why it’s crashing? I’m using Houdini 18.

I also have installed H18 and it crashed for me too UNTIL I installed the new Side FX Labs Tools (that’s how they called now, instead of “Game Dev Tools”) and now I can install the HDA. Here is a video how to install the SideFx Labs Tools: https://www.sidefx.com/tutorials/sidefx-labs-installation/

I hope this works for you too! :)

Yup that worked! Awesome, thank you!

Hi Simon, I’ll try that and report back, thanks for responding!