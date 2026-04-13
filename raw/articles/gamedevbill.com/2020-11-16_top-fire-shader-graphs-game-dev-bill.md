---
title: Top Fire Shader Graphs - Game Dev Bill
url: https://gamedevbill.com/top-fire-shader-graphs/
author: Bill
published: '2020-11-16'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![Top fire shader graphs title image](../../assets/ea7d42c3ff40c259.png)

There are a lot of ways to make a fire shader graph (and a lot of ways to make fire outside a shader graph). Today I’ll cover three main ways to pull off the effect, all in 2D: A sprite based approach, procedural cartoon fire, and procedural realistic fire. Then at the end I’ll discuss how to use the 2D shader graphs in 3D scenes.

This post is paired with a video, available [here](https://youtu.be/8sJQvFA6GEI), and includes [a github project with the final graphs](https://github.com/gamedevbill/Tutorials/tree/master/2D_Fire/). In this case, most of the content fit best in video format, so the written version here is quite brief. For all the meaty details, please see the video. This write up is here to just give an overview, and provide high-res screenshots.

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

The video is especially important if you wish to match my node input-values. Throughout development I tweak the constant values in the shader a lot, and the best place to see where they change, and why, is in the video.

Assets used in the creation of this tutorial: [Dragon from Infinity PBR](https://assetstore.unity.com/packages/3d/characters/creatures/dragons-45330?aid=1011l3QFn), [Low Poly Ultimate Pack](https://assetstore.unity.com/packages/3d/props/low-poly-ultimate-pack-54733?aid=1011l3QFn), and [Gaia 2](https://assetstore.unity.com/packages/tools/terrain/gaia-2-terrain-scene-generator-42618?aid=1011l3QFn). Hosting by [BlueHost](https://www.bluehost.com/track/gamedevbill/AboutMe).

With all three of these graphs, I’m showing most of the constants I used. In many cases, however, those should be tweaked and adjusted based on the scene you are using them in. Perhaps you need a chill fire to calmly wriggle nearby. Or maybe you need something more intense (like camping, [in-tents](https://amzn.to/3pzhEvm)).

## Sprite Based Fire Shader Graph

The first approach I’ll take is to make a static sprite animate in a fiery way. In this case, I’ll be using a four frame sprite. This is just a simple sprite I threw together that is not intended to look amazing, but is set up so the four frames can layer relatively well.

Make sure your sprite importer setting of “Mesh Type” is set to “Full Rect” and not “Tight”. Without that, the shader won’t look at all correct.

![](../../assets/351e84ea6029661d.png)


![](../../assets/351e84ea6029661d.png)

To start make an Unlit shader graph, or “Unlit Graph” as it’s called in the Create menu. I don’t want it to be lit because it shouldn’t be affected by shadows. Set the master node to be in “Transparent” mode (though you can get around this if you wish to use clipping instead).

Make an input called “MainTex” and set the Reference to “_MainTex”. Feed this into a sampler node. Then drive the UV’s of that node with a “Tiling and Offset” node with the Tiling set to (0.5, 0.5).

![](../../assets/49593be0afdef024.png)


![](../../assets/49593be0afdef024.png)

To animate, I’m going to use the [heat haze shader from my previous tutorial](https://gamedevbill.com/heat-haze-shader-graph/). We need to alter the haze core subgraph from that tutorial, so make a copy of it.

### Subgraph Alteration

The haze core subgraph uses two important nodes internally. UV and Time. In both cases we need this to be driven from the top level, so edit the graph to us a UV and Time input instead of node. In the spot where TimeSine was used, simply feed Time input to a newly created Sine node.

![](../../assets/26c7d1d18c2eaaf0.png)


![](../../assets/26c7d1d18c2eaaf0.png)

Next, go over to the section of the subgraph that does the blur. Being a hand-drawn kind of effect, we don’t want the blur. Simply remove all the nodes except the main sampler.

![](../../assets/8c42ffc38306e923.png)


![](../../assets/8c42ffc38306e923.png)

### Layering Flames

This subgraph has many inputs, most of which are covered in the previous tutorial, so I’ll skip to them being in place, while feeding the two new inputs by Tiling and Time nodes.

![](../../assets/32927628c97c96af.png)


![](../../assets/32927628c97c96af.png)

Now, copy the above three more times (four total) and edit the Offset input of each Tiling node such that the each haze core subgraph is sampling a different portion of the sprite.

To layer these on top of each other, there is one more convenience thing to do. Editing the subgraph, change the output to be pre-multipled by it’s own alpha, and also feed the inverted alpha out as a new output.

![](../../assets/98b27a917d61ee07.png)


![](../../assets/98b27a917d61ee07.png)

With these new outputs, we can more easily layer each of them together. For clarity, I’ll call the layers A, B, C, and D. Combine A & B by adding Color_A with Color_B * AlphaInv_A. Then do the same to combine C & D. To combine these two intermediate steps, do the same logic, but with a multiplied AB alpha. Like so: Color_AB + Color_CD * AlphaInv_A * AlphaInv_B.

![](../../assets/2acb9ed634a1684e.png)


![](../../assets/2acb9ed634a1684e.png)

### Activation

The one subgraph input still left unwired is the Activation input. Currently set to 1, the full flame animates. We’d prefer if the bottom were locked in place, so feed a UV node into a split, and feed the Y into a smoothstep. I set my inputs to (0.1, 0.3).

![](../../assets/6d07080d6b7d1c16.png)


![](../../assets/6d07080d6b7d1c16.png)

### Time Stepping

The last piece to work on is Time. Currently the simple Time node is driving the Time input of all the subgraphs. Instead, we want a more stepped time to give this a cartoony effect. Essentially, we want to lower the framerate of the effect.

To do that, feed time into a Multiply, then a Floor, and then a Divide. Have both the Multiply and the Divide be driven by a Vector1. Setting this to a high number will keep time fairly smooth, setting it to something low will make it very choppy.

Next, feed the output of that Divide into four Add nodes (or three adds and a preview). Give each add a different value, and that will make all our flame pieces be offset in their animation cycle.

![](../../assets/35760d71966d0c3c.png)


![](../../assets/35760d71966d0c3c.png)

### Full Sprite Fire Shader Graph

![](../../assets/1b413214b63ce9e2.png)


![](../../assets/1b413214b63ce9e2.png)

## Procedural Cartoon Fire Shader Graph

The target here is to create something that looks somewhat hand drawn and cartoony. The basis was a fire shader graph I made [in response to a tech-art challenge](https://twitter.com/GameDevBill/status/1318185394358407169?s=20). I also made a [time-lapse recording of that graph’s creation](https://youtu.be/R7niMLnQ3Ow). Today’s video ends up with almost the exact same graph, but with a lot more detail and explanation.

Again start with an unlit shader graph, that can sample a MainTex. In this case I’m using a texture just to define the sprite size & shape in-scene in Unity, and to define the shape of my fire. I used this sprite:

![](../../assets/67cefe525701185e.png)

I recommend setting this texture as the default input to the shader graph. That helps visualize things properly in the shader graph.

### Fire Noise

Feed the sampled texture into a smoothstep, and multiply that by the output of a Voronoi node.

![](../../assets/14feeebedd4b6755.png)


![](../../assets/14feeebedd4b6755.png)

To make the fire animate upwards, create a UV node and feed that into a split. Leave the X (R) unchanged, but feed the Y (G) into a subtract node that is fed by Time.

![](../../assets/e30af3651e0e12bd.png)


![](../../assets/e30af3651e0e12bd.png)

### Color Layers

Feed the output of the shaped noise (noise multiplied by the texture) into two Smoothstep nodes. One set to (0.3, 0.35) the other to (0.05, 0.1). Multiply each of these Smoothstep outputs by a color. I choose colors #FEC905 and #FF8E07.

Multiply the second noise output by one-minus the first noise output. Then add them together.

![](../../assets/0fcb2036d8dda015.png)


![](../../assets/0fcb2036d8dda015.png)

Feed the output of that Add into the color of the master node. To get alpha working right, also feed it into a split, and use the R channel to drive a smoothstep set to (0, 0.1). AlphaClipping on the master node needs to be 0.01.

![](../../assets/2a3cc6182a22b24c.png)


![](../../assets/2a3cc6182a22b24c.png)

### Fixing the shape

First step in fixing our shape is to add the shaping texture in just before we multiply by it. The multiply serves the purpose of forcing outside areas to 0, while the add will force central areas to 1.

Take the sampler output, feed it into a Multiply and an Add. I currently have these as 0.5 and -0.1 respectively, but this will be tweaked as needed. Add that result with the noise coming out of the Voronoi node.

![](../../assets/e67e509da2175f27.png)


![](../../assets/e67e509da2175f27.png)

Next, we’re going to make the noise less circle-y. To do this, make a second Voronoi node, and multiply it’s output in with our first Voronoi node. Give the new node some different input values from the first, and feed in a slightly altered time input.

This will make the “floating circles” look much more like chaotic noisy fire.

![](../../assets/37c6478b96c0cd3c.png)


![](../../assets/37c6478b96c0cd3c.png)

### Time Stepping

Just like the sprite shader, here we need to make the time movement more choppy to simulate a lower framerate. I’ll do the exact same thing I had done above.

![](../../assets/11cc1e76b6e0efd8.png)


![](../../assets/11cc1e76b6e0efd8.png)

At this point, we have a pretty good cartoon fire. In the video, I go into how to split the movement so it not only moves up, but also moves outward (to the sides). This is a lot harder to cover in text form, so if you are interested in that, please watch the video.

### Full Cartoon Fire Shader Graph

Graph as described above:

![](../../assets/80017e9646dd69c0.png)


![](../../assets/80017e9646dd69c0.png)

Graph with the outward movement covered in the video:

![](../../assets/486df132bdac382a.png)


![](../../assets/486df132bdac382a.png)

## Realistic Fire Shader Graph

The third and last of the 2D fire shader graphs I’ll cover today is realistic fire shader. For this, we start with the graph described above for cartoon fire (the final product of the written tutorial, not the final product of the video).

### Color Changes

First remove the secondary color & smoothstep such that there is only one color layer to the graph. Then change the mode of that color from “Default” to “HDR”. This makes it so the color can be brighter than 1, and will make it glow when your camera has bloom on.

In addition, feed the smoothstep output (before multiplying by color) directly into the Alpha input of the master mode. Set the master node to Transparent.

![](../../assets/ad30cc271c93054a.png)


![](../../assets/ad30cc271c93054a.png)

### Noise Shape

Take the output of the stepped time group, feed it into a multiply, then an add. Feed this into the Angle Offset inputs of the Voronoi nodes. I set the multiply and add to 5 and 50 respectively.

This makes the dots in the Voronoi node not only move upwards, but wiggle and dance as they do so. It would have been a good idea to also do this back in the cartoony effect.

![](../../assets/678be6996e7afc90.png)


![](../../assets/678be6996e7afc90.png)

To further mess with the noise shape, replace one Voronoi node with a Gradient Noise. Not that one of these is better than the other, but it’s worth trying different noise nodes as you work towards a shape you want. I also multiply the output here by 2 to more easily emphasize the bright points.

![](../../assets/03ef7537ebdb0dbb.png)


![](../../assets/03ef7537ebdb0dbb.png)

### Shape Changes

Since the realistic version of this graph has softer edges than the cartoony one, getting the gradients right is key. I recommend adjusting the texture smoothstep to be (0,0.5) and the texture multiply to either be 1 or 0.5 depending on if you are going for a more candle-y look, or camp-fire-y look. I also adjust the final smoothstep to (0.4, 1).

![](../../assets/e139fe2345ee5671.png)


![](../../assets/e139fe2345ee5671.png)

### Full Realistic Fire Shader Graph

![](../../assets/91ab9865158ccd4b.png)


![](../../assets/91ab9865158ccd4b.png)

## Working in 3D

The last thing to cover is how to add 2D fire to a 3D scene. It can be a very cheap (performance-wise) way to get fire into your levels.

For this, put a handful of fire layers into an empty 3d game object. Stagger their positions front to back and side to side. You’ll also want to vary the look of each layer. In the video I did this by creating copies of the material, and exposing a TimeOffset and Color property. Another way to do it is to create logic inside the shader that makes them look different based on things like world position.

Then attach a look-towards-camera script to the empty game object.

public class CameraLook : MonoBehaviour { public Camera Cam; // Update is called once per frame void Update() { var f = Cam.transform.forward; this.transform.forward = new Vector3(f.x, 0, f.z); } }

Note that I’m using he Camera’s forward, and I’m excluding y. I use the forward rather than the position so that if two fires are next to each other, they’ll appear to be on the same plane, rather than pointed inwards. I exclude the y because it looks weird when fire leans back if you are above it.

![](../../assets/c7f9508415f9dd20.png)

## All done

Again, this is covered in far more detail in [the video](https://youtu.be/8sJQvFA6GEI). This is written as an accompanying guide, not as a stand alone piece.

References

[Infinity PBR Dragon](https://assetstore.unity.com/packages/3d/characters/creatures/dragons-45330?aid=1011l3QFn)(only on youtube video)[Low Poly Ultimate Pack](https://assetstore.unity.com/packages/3d/props/low-poly-ultimate-pack-54733?aid=1011l3QFn)– Tons of low-poly assets from all sorts of era’s and regions.[Gaia 2](https://assetstore.unity.com/packages/tools/terrain/gaia-2-terrain-scene-generator-42618?aid=1011l3QFn)– procedural terrain creation (only on youtube video)- Hosting by
[BlueHost](https://www.bluehost.com/track/gamedevbill/AboutMe).

*Do something. Make progress. Have fun*.