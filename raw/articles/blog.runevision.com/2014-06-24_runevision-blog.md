---
title: runevision blog
url: https://blog.runevision.com/2014/06/
published: '2014-06-24'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

For the past two weeks I've been trying out and evaluating Substance Designer in some of my spare time. Substance Designer is a tool for generating procedural materials. Really what this means is that it generates a set of procedural textures (such as diffuse map, normal map, specular map, and others) which many tools can then combine into a material.

![](../../assets/09f01b6f2a16855d.png)

Why is this useful? Substance Designer can export generated textures, but the more interesting part is that some other tools support the proprietary Substance format, which allows generating variations of procedural materials at runtime. So for example in Unity, which support Substances, a Unity game can include a Substance file for a stone wall, and then at runtime, while the game is running, an unlimited number of variations of it can be generated. This means you can have stone walls with different colors, different amount of dirt, different amounts of moss growing on them and whatever other variations this stone wall Substance exposes. Including all these variations (including all the possible combinations) in the game as regular textures would have taken up a ton of space, but instead a single Substance file can generate them all, and it usually takes up less space than even a single set of textures. That's a pretty cool way to get a lot of variety.

I'm working on and off on a procedural game in my spare time, and I would like to use procedural materials in it. I recently finally got around to evaluating if this would be feasible using Substance Designer. I know the runtime part in Unity works well, and since they added an Indie license, the price is feasible too, even for a game created on the side. Their Pro license is at the time of writing $449 while their Indie license (which has all the same features, just some restrictions on the license) is just $66. More details on the [Allegorithmic website](http://www.allegorithmic.com/). So the remaining questions was how easy or hard it would be to author the procedural materials in Substance Designer. Luckily they have a 30 day evaluation period that let me find out about that.

### The Test

I learned recently that Allegorithmic have begun downplaying the procedural aspect of Substance Designer and instead marketed it as an advanced compositing tool for textures (imported from e.g. Photoshop or similar) with emphasis on non-destructive workflows and on nodes being a superior alternative to layers. Nevertheless, my own interest in Substance Designer is for it's hardcore procedural features, and that's what I wanted to evaluate it based on.

I was pretty sure Substance Designer would make it easy to just combine various noise functions, but how did it fare with creating more structured man-made patterns such as a brick wall? To what degree would these things be hard-coded in the engine and to which degree would the design tool let me create something completely custom? I decided to use an existing material I had created before as reference and try to recreate a material in Substance Designer with a look as close as possible to this reference.

One of the best-looking materials I've created myself is a sort of ancient temple brick wall. It has rows of different heights, a different number of bricks per row, subtle variations of brick widths, and subtle random rotations of each brick. Furthermore it has erosion of the bricks as well as small cracks here and there.

![](../../assets/a2a87ee702237be6.png)

This material was created procedurally in the free raytracer 3D software [POV-Ray](http://povray.org/), so it's already procedurally created, but it can't be altered at runtime. In POV-Ray I created this brick wall by using a physical rounded box for each brick, and then the rest was done with procedural texturing of these bricks. In Substance Designer I would have to find a way to get the same end result purely with 2D texture tricks, without using any physical 3D objects.

### The Main Graph

Substance Designer is a graph based authoring tool. You author materials by visually creating and connecting various nodes that each manipulate a texture is various ways. For example, a blend node takes two textures as input and provide a new texture as output which is the blended result. The node has settings for which blend mode to use. Eventually, the graph feeds into the output textures, such as diffuse map, normal map etc. Here's my main graph from a point in time early into my attempt:

![](../../assets/c99702f8b91f7046.png)

In this graph I'm using some "Brick Pattern" nodes as input and some noise functions and then combining these in various ways. The brick pattern used here comes with the tool and does not support variable row height, variable number of bricks per row, etc.

In short, the main graph works well. It's fairly intuitive to work with and quick to make changes to. If you want a new node in between two other nodes, it takes about five seconds to create and reconnect. In fact, the tool tries to be smart about it and can do the reconnection automatically based on the currently selected node. Sometimes this can be a bit annoying when it's not what you want, but once you learn to take advantage of it, it's actually quite nice.

You can also easily see the intermediary results in each node since they show a small preview of the output texture they produce. If you want to see it larger, you can double-click on the node, which shows its output in a texture preview window. At the same time you can have the final output of the graph shown in a different 3D preview window at all times, so you easily keep track of how your changes affect the final result.

![](../../assets/843cf917adacba79.png)

In the depicted graph, I had just figured out how to obtain an effect of erosion of the bricks. The normal map is generated from a depth texture where darker shades are deeper depth. It would be easy to roughen up the surface by blending the depth texture with a noise texture, but this would make the surface rough everywhere. I wanted primarily the edges of bricks to be affected by this roughness.

The brick pattern I used for the bricks depth texture has a bevel size setting which is used to define the rounding size. I had used this pattern with a very small bevel for the depth texture itself, since the bricks should have fairly sharp edges. However, by using the same pattern with a much larger bevel, I got a texture which was darker near the edges of bricks and hence could be used as a mask for the noise texture. By subtracting the large-beveled brick pattern from the noise pattern, I got a texture that was only noisy at the edges of bricks. Well, it would have been noisy everywhere, but since all texture outputs have values clamped between zero and one, the negative values of the noise near the center of bricks becomes clamped to zero and thus not visible.

This kind of clever manipulation and combination of different patterns is what the main graph is all about. This is not specific to Substance Designer either - arguably this is how procedural textures are created regardless of the tool used. Through my previous work with POV-Ray, I already had extensive experience with thinking in this way, even though procedural materials in POV-Ray are defined in a text description language rather than a visual graph based tool. Compared to someone with no previous experience with creating procedural textures of any kind, this probably gave me an advantage in being able to figure out how to obtain the results I wanted.

There are some fundamental differences though. Some procedural material approaches are based on function evaluation. This includes the procedural materials in POV-Ray, or patterns defined in pixel shaders. These methods are not rasterized except at the very last stage. This means you can always easily scale a pattern up or down, even by factors of 1000 or more, without any loss of quality. They are perfect mathematical functions of infinite resolution. On the other hand, nodes in Substance Designer are rasterized textures. There are nodes that can be used to scale the input up or down, but up-scaling creates a blurry result as with any regular rasterized image. Some pattern nodes have a setting that can be used to scale the pattern up or down without loss of quality, but many other patterns have a hard-coded scale that you're basically stuck with. The rasterized approach has the advantage though that blurring operations can be done much cheaper than with a function evaluation based approach.

### Function Graphs

As mentioned earlier, each node in the main graph have various settings. Each of these settings can either be set to a fixed value in the user interface, or they can be setup to be driven by a function. Editing this function is done in a new window where you build up the function as a function graph.

![](../../assets/dee06eb5d5c6dfc0.png)

The function graphs look very similar to the main graph but the node types and connection types are different. Where the connections in the main graph are always either a color image or a gray-scale image, the connections in the function graphs are things such as floating point numbers, integers, and vectors.

In this case we're looking at a function driving the "Level In Mid" setting of a Levels node in the main graph. The very simple function graph I created looks like this:

![](../../assets/4427811e1e5f533b.png)

If you look at this simple graph, you might not know what it's doing despite the simplicity. It's subtracting some float from some float and using the result as the value for this setting. But which floats? The nodes show no preview information at a glance like the nodes in the main graph. Instead you have to click on a node to see in the settings view what it does.

In this graph the Float node contains a value of 1. And the Get Float node gets the value of the variable called ColorVariation. The code equivalent of the graph would be *outputValue = 1 - ColorVariation*. It's unfortunate that the content of the nodes, such as constant values and variable names, is not shown in a more immediate way, because this makes it pretty hard to get any kind of overview, especially with larger graphs.

That said, the ability to use a graph to drive any node settings you can think of is really powerful.

### Discovering FX-Maps

I mentioned earlier that I was most curious about the extend of the ability to define structured man-made patterns. It took me a while to figure out how to even access the part of the software needed to do that.

First of all, the software contains a "Generator" library with a collection of pre-built noise and pattern nodes. At one point I found out that these are all "main graphs" themselves and that the nodes can be double-clicked to inspect the main graph that makes up the generator for that node. The graph can't be edited right away, but if it's copied, the copy can be edited.

The next thing I found out - and this took a bit longer - was that the meat of all patterns eventually came from a node type called FX-Map. The FX-Map looks like it's a hard-coded node and it's functionality is impossible to understand based on looking at its settings. Eventually I found out that you have to right-click on an FX-Map node and choose "Edit Fx-Map". This opens a new window with a new graph. This is a new graph type different from the main graphs and the function graphs.

The FX-Map graph is the strangest thing in Substance Designer. It has three node types - Quadrant, Switch, and Iterate. The connections represent parts of a texture being drawn I think.

![](../../assets/e03e30854712053d.png)

Everything in FX-Maps boils down to drawing patterns repeatedly. A pattern is drawn inside a rectangle and can be either one of a set of hard-coded patterns (like solid colors, linear gradients, radial fills, etc.), or a specified input image.

Confusingly, drawing this pattern is done with a node called Quadrant. The Quadrant node can itself draw one pattern and it has four input slots that can be connected to other quadrants which will each draw in one quadrant of the main image. This is useful if you want a pattern that's recursively composed of quadrants of smaller patterns, but for everything else, having to draw patterns with a node called Quadrant even when no quadrant-related functionality is used is somewhat weird.

Anyway, if you want a pattern that's composed of patterns in a non-quadrant way, you'll need an Iterator node that takes a Quadrant node as input. The Iterator will then invoke the Quadrant repeatedly. The Quadrant node has settings for the pattern drawing and for the placement of the rectangle the pattern is drawn inside. By varying these settings (using function graphs) based on a hard-coded variable called "$number", the patterns can be drawn next to each other in various ways.

So far so good. But how would I create a nested loop in order to draw my brick wall with multiple bricks in each of the multiple rows? When programming a nested loop in a programming language, I'll normally have the outer iterator called *i* and the inner called *j* or something like that. But here, since the Iterator node is hard-coded to write the index value into a variable called "$number", the inner loop index overwrites the outer loop index. I looked at the FX-Map for the Brick pattern in the library, but it used a single iterator only. This can be done when all the rows have the same number of bricks by using division and modulus on the iteration value, but when each row have a random number of bricks, this trick doesn't work and a proper nested loop is needed.

### Getting Stuck With Advanced Stuff

Google was not of much help finding information on nested iteration. Searching for variations of "substance designer" together with "nested loop", "nested iterator" or similar would at best point to arbitrary release notes for Substance Designer, and at worst to pages not related to Substance Designer at all.

This is a general trend by the way. More often than not, when I needed details about something in Substance Designer, they were nowhere to be found whether looking in the documentation or using Google. Take the Blend node in the main graph for example. It has different blend modes such as "copy", "add", "subtract", "add sub", "switch", and more. I didn't quite understand all of those just from the names. The [manual page about nodes](http://support.allegorithmic.com/documentation/display/SD43/Nodes) only describe the blend node with two sentences and doesn't cover the various blend modes. If there's one thing Substance Designer really needs, it's to make sure all features and settings are documented.

In the end I had to write a mail to Allegorithmic support and ask them how I could do a nested loop. The first answer didn't contain concrete help with my problem, but there was an interesting snippet I found illuminating:

Before going into details, I think you experienced Substance Designer in the hardest possible way, trying to use FXMaps and functions for procedural textures. Although that was the case 3 years ago, and although you can still make procedural textures, Substance Designer is now more a kind of "compositing" tool for your texturing work. I would say that the procedural part of Substance Designer barely didn't evolve since that time, on the contrary to all the rest.

This is where I realized they're focusing on compositing over procedural, and upon reinspecting their website, it's hard to find any use of the word "procedural" at all today. I wrote a reply back explaining that my interest is in the procedural aspects regardless, and my aim to recreate my reference brick material as a procedural material in Substance Designer.

The second answer was a bit more helpful. It pointed to a [forum post](http://forum.allegorithmic.com/index.php/topic,1084.msg5777.html#msg5777) where community members had made experiments with advanced FX-Maps that contained nested loops among other things. But they were very complex and I had a very hard time understanding those without any kind of proper introductory explanation of the basics.

![](../../assets/507f05db5b81944c.png)

At this point Eric Batut, Development Director at Allegorithmic, came to my help. He had been reading my support email as well, and he replied with detailed explanations including an attachment with a basic example graph. The graph contained an FX-Map with nested Iteration nodes, all well commented using comments embedded in the graph.

I should say that I know Eric and other guys from Allegorithmic. We worked together in the past on implementing support for Substances in Unity (I worked on the UI for it). They might very well provide the same level of support for everyone though; I really can't say.

Part of my confusion had also been about a node type in the function graphs called Sequence, and this was explained as well. With my new found insight, I was ready to tackle implementing my own custom brick pattern with random widths and heights, and random number of bricks per row.

### Working With FX-Maps

FX-Maps get gradually easier to work with as you get used to them, but they're still a bit strange. Most of the strangeness is related to the way of controlling which order things are executed in.

If we look at the Quadrant node again, which is used for drawing patterns inside rectangles, there's a number of settings in it.

![](../../assets/e59f9472b8798553.png)

The thing to learn about these settings is that a function graph for a given property often doesn't just contain logic needed for that setting itself, but also logic needed for settings below it. You see, the graphs for the settings are evaluated in order, and whenever a node in one of those graphs is used to write a value to a variable, that value can then be read in graphs of the subsequent settings too, because all variables are global - at least in the scope of the main graph.

So in the example graph I was given, the Color / Luminosity setting's function graph doesn't just have logic for determining the color of the pattern being drawn; it also has logic that read the "$number" variable and saves it into a variable called "y". And the Pattern Offset setting's function graph calculates and saves a vector values called "BoxSize" which is then used both by the graph of the Pattern Offset setting itself as well as by the graph of the Pattern Size setting.

The execution order of nodes within the function graphs themselves are controlled using Sequence nodes.

![](../../assets/80c2c56f12d2405b.png)

Sequence nodes have two input slots that are executed in order - first the sub-graph feeding into the first slot is evaluated, then the sub-graph feeding into the second slot. The sequence node itself returns the value from the second slot, while the value of the first slot is simply discarded.

Again, the approach works once you get used to it, but it's still somewhat strange. It means function graphs are even harder to get an overview of, because you can't assume that the nodes in it are related to the settings this graph is for. Some or all nodes might be just some general-purpose calculations that needed to be put into this graph for timing purposes. Nevertheless, it can get the job done.

One last strange thing about FX-Maps. Like I mentioned earlier, what an FX-Map node does can't be gathered from its settings at all. I learned that the FX-Map instead has direct access to the variables defined in the main graph - basically there's zero encapsulation. This makes FX-Maps very tied to the main graph they're inside. Normally this would be very bad, but it does seem like FX-Maps are not designed for reuse at all anyway. An FX-Map is always embedded inside a main graph, even if the FX-Map is the only thing in it.

### Reuse of Graphs

Now for some good news. Like mentioned earlier, all the noise and pattern nodes in the built-in library are their own main graphs, and it's very easy to make new custom nodes as well. In fact, nothing needs to be done at all. Any main graph can be dragged into another main graph and then appears as a node. The output maps of that graph automatically appear as output slots on the node, and the settings of the graph automatically appear as setting of the node. Though I haven't used the feature myself yet, graphs can also define input images, and these, I'm sure, will appear as input slots on the node.

Function graphs can also be reused. FX-Maps can't, but this is probably ultimately a good thing, since it's easier to make everything be able to connect together when there is only two types of graph assets that can be referenced.

In my own material I ended up with a design with three different main graphs

**VariableRowTileGenerator**

An FX-Map that draws patterns in a brick formation. The patterns can be set to be gradients (in 90 degree intervals) or solid color. Randomness can be applied to the luminosity of each pattern.

![](../../assets/d99eb0e3c1766505.png)

**VariableRowBrickGenerator**

More high level processing built on top of the VariableRowTileGenerator. This includes bevels and slopes (gradients at random angles not constrained to 90 degree intervals).

![](../../assets/17859a55fa4a09fa.png)

**VariableRowBricks**

The is the final material. It references nodes both of type VariableRowTileGenerator and VariableRowBrickGenerator as well as some noise nodes. Lots of custom processing on top.

![](../../assets/e6c9804e6f431161.png)

Actually I used a few more main graphs. I ended up copying and customizing some noise graphs from the library because I wanted them to behave slightly differently.

The ability to super easily reuse graphs inside other graphs is very powerful and definitely a strong point of Substance Designer, both usability wise and in terms of raw functionality.

### Limitations

I'm almost towards the end of my impressions, but they wouldn't be complete without some thoughts about what it is possible to achieve and what simply isn't possible, since that's what I set out to find out about.

Basically, Substance Designer is not Turing complete, and as such you can't just implement any pattern you can think of an algorithm for. Specifically the lack of being able to work with arrays means that some common patterns are out of reach. Sometimes there will exist some workaround that produces a very similar result though.

One example is Perlin noise. The library in Substance Designer contains patterns called Perlin noise but they're not really Perlin noise. Nobody would ever care that it doesn't use the correct algorithm though - it easily looks close enough.

Another example is a pattern often called crackle or voronoi crackle. It's a very versatile and useful pattern that is defined as the difference between the closest and second closest point out of a set of randomly distributed points. It's great for cracks, angular bumps, and many other things, and I happened to need this pattern for the cracks in my brick wall.

![](../../assets/b6e336327c150801.png)

I don't think it's possible to generate a crackle pattern in Substance Designer. There's a pattern in the library called Crystals which seems to be very inspired by it both in looks and implementation. I tweaked it a bit to be even closer to crackle, but it still doesn't quite have the same properties. In the original crackle pattern, each cell is convex and has only a single peak. In the Substance Designer substitute some cells are partially merged together which gives a non-convex shape with multiple peaks. The workaround just about worked all right in my use case, but it's enough visibly different that it might not work out for all use cases.

### Results

All right, let's have a look at how close I got to the reference material I was trying to recreate in Substance Designer.

![](../../assets/c59515300bfb2d03.png)

I think it got very close! Don't pay attention to specific rows having different heights or number of bricks than in the original, or other specific differences like that. I designed that to be determined by the random seed, so I have no direct control over that. The important part was that it should look like it could have been a part of the same brick wall, just somewhere else. It's close enough that I'll happily use this substance instead of the original material.

![](../../assets/a2069872d07748cd.gif)

![](../../assets/02887e93466df0f1.gif)

The substance material of course has the advantage of being able to recreate randomized variations of itself on the fly where the random widths and heights and locations of cracks are different. This on its own is already pretty nice, but with some additional work I can implement support for qualitative variations too. I could add sliders for varying the bricks between shiny new and old and crumbled. I could add fields for specifying the main color, and a slider for the amount of color variation of the bricks (right now there's always just a tiny bit). I have some other ideas as well, but I'm sure your imagination is as good as mine.

I hope you found these impressions useful or interesting, and that you may have learned something new about Substance Designer, whether you knew nothing about it before or was already using it. Are you considering using Substance Designer for your game, or are you already using it? I'd like to hear about your impressions as well!