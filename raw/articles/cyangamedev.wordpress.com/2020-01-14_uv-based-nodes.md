---
title: UV-Based Nodes
url: https://cyangamedev.wordpress.com/2020/01/14/uv-based-nodes/
author: Cyan
published: '2020-01-14'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This post includes an introduction to using the **Sample Texture 2D** node and UV-based nodes such as **Tiling And Offset**, **Rotate**, **Flipbook** and **Polar Coordinates**.

Note that I’m not going over warping effects such as the **Radial Shear**, **Spherize** and **Twirl **nodes. This post is already quite long and I think what those effects do should be fairly self-explanatory from looking at the preview’s they produce.

For information on the **Triplanar **node, see the [World space UVs & Triplanar Mapping](https://cyangamedev.wordpress.com/2020/01/28/worldspace-uvs-triplanar-mapping/) post.

### UVs

When creating a model in a 3D modelling programs (e.g. Blender, Maya), an artist will usually go through a process known as **UV-mapping**. This is where the 3D geometry is unwrapped into a 2D “net”, assigning a UV value (the XY coordinates on that net, usually between **0** and **1**) to each vertex. These UVs can be used for various effects, most commonly for applying a texture to the model.

In a shader, we can obtain these UV coordinates from the model. In code this is done by using one of the **TEXCOORD(0, 1, etc)** semantics in the “appdata” struct (usually instead named as “Attributes” in the **URP**). In shadergraph, we can use the **UV** node.

For complicated models with many pieces, they would usually have a complicated UV map where manipulating the UVs, such as offsetting or tiling, for the purpose of sampling a texture would likely cause very strange results. A lot of the nodes mentioned below will be more useful for manipulating the UVs to render something interesting to a simple quad.

![](../../assets/5526db9fbb02d074.png)

For a simple quad, it contains 4 vertices where the UVs (channel 0) typically are:

**Bottom Left Vertex = 0, 0****Top Left Vertex = 0, 1****Bottom Right Vertex = 1, 0****Top Right Vertex = 1, 1**

This also happens to be what the preview of the UV node uses. The X coordinate of the UVs is shown in **red**, and the Y coordinate shows in **green**. If both values are **0**, it shows as **black** and if both values are **1** it shows as **yellow** due to the additive nature of the [RGB colour model](https://en.wikipedia.org/wiki/RGB_color_model), but it might be a lot easier if you see “yellow” as “red and green” rather than a separate colour.

While UVs are assigned per **vertex**, when the UV values are sent from the shader’s **Vertex stage** to the **Fragment (pixel) stage**, it interpolates between the values, hence why the blending occurs in the **UV** node preview.

There are multiple UV channels that can be used. Usually only the **UV0** channel is used, but an artist might use other channels to provide extra information to the shader. The default Unity sphere actually has two sets of UVs, the UV0 channel will stretch a the texture around the sphere while UV1 has 6 squares located in the bottom two-thirds of the UVs where each one is projected onto the sphere from a different axis.

Also when using **Custom Vertex Streams** on a **Particle System** object (under the Particle System Renderer tab), it might use these extra channels (as well as the **Z/B** or **W/A** values in the UV0 channel) to pass in information such as particle lifetime.

### Sample Texture 2D

![](../../assets/e7d024b9f74a59e9.png)

When sampling a texture, we pass in the UV coordinates and it obtains the Vector4 colour on the texture at each coordinate.

The **Type** and **Space** should only be changed when sampling **normal** maps (textures containing information about normals, which are used in lighting calculations).

Also notice how the UV input has “UV0” next to it. This means that it will automatically use the UV Node input (using the UV0 Channel) if nothing is connected.

It will also automatically use the **Sampler State** based on the Texture if the **Sampler(SS)** input is left blank, however it can also be useful to connect one if you want to override the texture’s default settings. This includes information like switching between different **Filter** and **Wrap** modes, which I’ve listed below.

An important note is that this node can only be used in the **Fragment stage** (colour/alpha) of the shader. It won’t allow you to connect nodes that use this to the **Vertex Position** input, use the **Sample Texture 2D LOD** node instead if you need to sample a texture in the **Vertex stage**. It will allow you to specify which mipmap level to use.

##### Sampler Filter Modes

**Point**(no filter) : The Texture appears blocky up close. (Useful for sampling pixel art)**Linear**(aka**Bilinear**in the texture inspector) : The Texture appears blurry up close.**Trilinear**: The Texture appears blurry, also blurring between the different mipmap levels.

Note : There can be some confusion between “**Linear/Bilinear**” and “**Trilinear**” filtering modes. In shaders the Bilinear setting is referred to as Linear, which is a better name for it as even when using 3D textures this mode will linearly interpolate/blend all 3 axes. The term Trilinear does not mean the same thing – It blends between each axis in the texture **plus an additional mipmapping axis**. Since textures are usually 2D, this results in 3 axes, hence the slightly confusing term, Trilinear – which has nothing to do with linear filtering in 3D textures.

##### Sampler Wrap Modes

**Repeat**: Repeats the Texture in tiles.**Clamp**: Clamps the UVs to the Texture’s edges, creating a stretching effect if the UVs are below 0 or above 1.**Mirror**: Mirrors the Texture at every integer boundary to create a repeating pattern.**Mirror Once**: Mirrors The texture once, then clamps it to edge pixels

### Tiling And Offset

![](../../assets/30850e2c32838010.png)

This node allows us to scale and offset the UV coordinate. The code generated by the node is actually very simple. It would be equal to doing a **Multiply** node and then an **Add** node :

Out = UV * Tiling + Offset

You might have noticed that I said the node allows us to “**scale**” the UVs and not “**tile**“. It actually only creates a tiling effect when sampling textures with the **Sampler State** set to **Repeat **wrap mode. I’ve seen others get confused at this and unsure about how to tile their effect when not sampling textures.

In order to create tiling UVs, we can use the **Fraction** node after the **Tiling And Offset **as shown in the example below. I’m using the **Rectangle** node to produce repeating squares, which could be put into a **One Minus** to produce a grid pattern. We could also use other shapes such as the **Ellipse** node to produce a repeating set of circles. We won’t want to do this if sampling a texture though as if mipmaps are enabled it can cause visible seams where the UVs jump from **0** to **1**.

![](../../assets/192a49d92d7e68c8.png)

### Scale Centered at Offset

This isn’t a node, but it’s something I put together that might be useful. This allows us to sample a texture, but have it always be **scaled from the point it’s offset to**, and from the **center** of the texture rather than the bottom left corner. Note that the offset is done **before** scaling, rather than **after** like the **Tiling And Offset** node does. Copy the graph and play around with the **Offset** (**Vector2**) and **Scale** (**Vector1**) **property** inputs and see what happens to the texture preview!

### Rotate

As the name suggests, this node allows us to rotate the UVs around a point (not to be confused with **Rotate About Axis** which is for rotations in **3D**). The given rotation can be **Degrees** or **Radians** based on the **Unit** setting on the node. As an example, we can have the UVs **rotate over time** around the center of the UVs by using a center point of **(0.5, 0.5)** and use the **Time** node like so :

### Flipbook

The **Flipbook** node is useful if you want to sample a **rectangular section** of a texture (based on a regular **grid**), with the **Tile** input to determine which section to output. The node only manipulates the UVs so it can then be put into a **Sample Texture 2D** node to handle the texture sampling. e.g. It could be used to obtain a **single sprite** from a **sprite sheet texture**. You can also base the **Tile** input over **Time** (put into a **Floor** node so that it jumps between each integer) to animate the sprite over time.

The **Sample Texture 2D** on the left is only there to show what the original texture looks like. The **Width** and **Height** inputs are both **3**, as the texture is made up from a **3×3** set of tiles. The **Tile** input should be an integer from **0** **to 8** since it’s **3×3**, meaning a total of **9** tiles. I’ve numbered the texture to help show which part of the texture is what **Tile** index. Note that I’ve enabled the **Invert Y** on the **Flipbook** node, as UVs start at **(0,0)** in the bottom left corner, while I have put tile **0** is in the **top left** on the texture. If **Tile** is outside the range of **0 to 8**, it will wrap back around (regardless of Sampler State wrap mode). e.g. **-1** will select tile **8**, **9** will select tile **0**, **10** will select tile **1**, etc.

### Polar Coordinates

The **Polar Coordinates** node is a useful node that converts between Cartesian and polar coordinate spaces. In short, the **R/X** component of the output **Vector2** contains the **distance** from the center point, while the **G/Y** component contains the **angle** the point is at, with a range of **Length Scale** * (**-0.5 to 0.5** (straight down going clockwise) and **0** straight up). It can be used to sample a texture to create portal/wormhole/whirlpool effects, and when put through a **Fraction** and **Step **node, we can create tiling sets of circles or outward rays (usually referred to as a sunburst). By using additional maths more interesting flower-like shapes can also be produced.

For more information, I have a separate post explaining it in more detail : [Polar Coordinates Post](https://cyangamedev.wordpress.com/2019/05/13/polar-coordinates/)