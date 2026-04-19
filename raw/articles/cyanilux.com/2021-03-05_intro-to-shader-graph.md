---
title: Intro to Shader Graph
url: https://www.cyanilux.com/tutorials/intro-to-shader-graph/
author: Cyanilux
published: '2021-03-05'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Intro to Shader Graph

Hey! This post is a detailed introduction to using **Shader Graph** - a node based shader editor for Unity that is provided for the **Scriptable Render Pipelines** (SRPs), including the **Universal Render Pipeline** (URP) and **High Definition Render Pipeline** (HDRP). The post goes over how to use the tool and it’s features, not necessarily how to create shaders using it - I have other [tutorial breakdowns](https://www.cyanilux.com/contents/#tutorial-breakdowns) that go over creating specific shader effects if you’re interested in that.

Shader Graph is also now supported in the **Built-in Pipeline as of Unity 2021.2+**, though may be limited in some features. It is not supported for previous versions.

Also note, you may also see the “Lightweight Render Pipeline (LWRP)” mentioned online, which was renamed to Universal RP during development. You may still find LWRP listed in the package manager but the newer versions (e.g. v7 onwards) should be identical to URP. If you are installing the package manually, I’d suggest just using the Universal RP one instead.

If you aren’t familiar with what **shaders** and **materials** are, I’d recommend looking at my [Intro to the Shader Pipeline](https://www.cyanilux.com/tutorials/intro-to-the-shader-pipeline) post before reading this one.

(Also note, any keyboard shortcuts will be based on Windows)

### Sections :


[Installing Shader Graph / URP / HDRP](https://www.cyanilux.com#install)[Graph Types](https://www.cyanilux.com#graph-types)[Graph Inspector](https://www.cyanilux.com#graph-inspector)[Master Stack](https://www.cyanilux.com#master-stack)[Save Graph](https://www.cyanilux.com#save-graph)[Nodes](https://www.cyanilux.com#nodes)[Data Types](https://www.cyanilux.com#data-types)[Coordinate Spaces](https://www.cyanilux.com#coordinate-spaces)[Understanding Previews](https://www.cyanilux.com#understanding-previews)[Main Preview](https://www.cyanilux.com#main-preview)[Blackboard](https://www.cyanilux.com#blackboard)[Grouping Nodes](https://www.cyanilux.com#groups)[Sticky Notes](https://www.cyanilux.com#sticky-notes)[Shortcut Keys](https://www.cyanilux.com#shortcuts)[Sub Graphs](https://www.cyanilux.com#sub-graphs)[Fragment-Only Nodes](https://www.cyanilux.com#fragment-only-nodes)[Advanced](https://www.cyanilux.com#advanced)


## Installing Shader Graph

Shader Graph is a node based shader editor that is mostly intended for the Scriptable Render Pipelines. But it does also have some Built-in RP support now for Unity 2021.2+. If in that version or higher, you can install the Shader Graph package via the **Package Manager** (accessed via **Window** on the top menu).

For the Universal RP and High Definition RP, Shader Graph is already included in their packages so **will automatically be installed alongside them**. Select one of the URP/HDRP **templates when starting a new project** or install the URP/HDRP package manually via the **Package Manager**.

If installed manually, this will also require following some additional setup - such as creating and assigning a Pipeline Asset under the **Project Settings → Graphics** tab. The asset can also be overriden per Quality setting. You’ll also need to convert materials to use the shaders from the appropiate pipeline, this can be done automatically from the **Edit → Render Pipeline** menu but will only work for the Standard built-in shaders. Any custom shaders cannot be upgraded automatically and will require rewriting. For additional setup instructions see the “Getting Started” tabs in the documentation :

I would mainly recommend that beginners start with URP as it is much simpler than HDRP (and most of my tutorials are written for URP). Some tutorials may also work in HDRP but may require some additional tweaks (due to differences like [Camera-Relative rendering](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@10.2/manual/Camera-Relative-Rendering.html) and different master nodes/stack).

There is also documentation for Shader Graph. The **Node Library** in particular can be very useful for learning what each node does, but it can also be accessed in Shader Graph by right-clicking a node and selecting “Open Documentation”.

Also be aware you can view your current **Shader Graph version** in the **Package Manager** window (accessed via **Window** on the top menu). You might also be able to update the version here though some aren’t available unless you also update Unity itself. (e.g. v10 is only available for 2020.2 onwards)

## Graph Types

To create a Shader Graph Asset, right-click somewhere in your **Assets** in the **Project** window then select **Create → Shader Graph**.

Older versions may have them listed under **Shader** heading but that also includes writing shaders using code (CG/HLSL) such as the Surface Shader and Unlit Shader options. Those templates are intended for the Built-in Render Pipeline and may not function in other pipelines.

In v10+ (Unity 2020.2+) there is three graphs listed :

**Blank Shader Graph**: A shader graph with no predefined settings. All other graphs (except for Sub Graphs) are a version of this graph with settings already adjusted. It’s possible to switch between them at any time through the use of the**Graph Settings**as discussed in the next section. While a Material can be created using a Blank Shader Graph, the resulting shader will be the magenta error shader unless configured into one of the other types. Using one of the other templates can provide quicker setup.**Sub Graph**: A special type of graph that can be used as a node in other graphs. Useful for creating functions that you will want to reuse many times and for organising large graphs. Sub Graphs can also be nested in other Sub Graphs. A later section will go into these in more detail.**VFX Shader Graph**: For creating a shader that is compatible with the[Visual Effect Graph](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest), used for creating particle effects. It cannot be applied to regular GameObjects/Renderers, only in the VFX Graph Output Particle blocks. (This graph type is deprecated in newer versions, in favour of checkboxes under the Graph Settings of other graph types to make them support VFX Graph without needing the VFX Graph “target”)

If URP is installed, a “Universal Render Pipeline” heading is shown with the following :

**Lit Shader Graph**: Known as the “PBR Graph” prior to v10. Used for creating a graph that handles lighting for 3D mesh objects, using a**Physically Based Rendering**lighting model, similar to the URP/Lit Shader (or the built-in RP’s Standard shader / surface shaders)**Unlit Shader Graph**: Always fully lit, is not affected by lights & shadows. Intended for use on 3D objects.**Sprite Lit Shader Graph**: For use with Sprites with[URP’s 2D Renderer & 2D lighting system](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@11.0/manual/2d-index.html)**Sprite Unlit Shader Graph**: For use with Sprites. Always fully lit, is not affected by lights & shadows.**Fullscreen Shader Graph**(Unity 2022.2+) : For use with the Fullscreen Pass Renderer Feature, for creating custom post-processing effects - see[docs example](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/post-processing/post-processing-custom-effect-low-code.html)(Unity 2023.2+ & 6000+) : For use with UI (e.g. Image, Raw Image components)**Canvas Graph**

For HDRP graph types, [see docs](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/shader-graph-materials-reference.html).

## Graph Inspector

In v10+, the **Graph Inspector** window was added, which can be toggled using the button in the top right of the graph. It has two tabs, **Node Settings** and **Graph Settings**.

The **Graph Settings** tab is important to set up the graph correctly if you’ve selected the **Blank Shader Graph** or want to switch to a different graph type. We need to select an **Active Target** (Universal, HDRP or Visual Effect, depending on which is installed in the project). It’s also possible to add multiple active targets to the list, if you need it to be compiled for more than one that is.

Once a target is selected, more settings are added below the list. I’ll be going through the **Universal** ones below but HDRP has some similar ones too (listed on their graph type / master node pages, as linked in the docs above).

Prior to v10, these settings can instead be found on the **Master** node. While hovering over it, a small cog/gear icon appears in the top right of the node which shows the settings when clicked.

Common settings for URP include :

**Material**: Selects the graph type. Can be**Unlit**,**Lit**, or**Sprite Unlit/Lit**.- As an example, if
**Lit**is selected Shader Graph will automatically handle lighting calculations based on**Physically Based Rendering**(PBR) lighting models and add more inputs to the**Master Stack**such as**Metallic**,**Smoothness**and Tangent space**Normal**. This will be explained in more detail in the section below.

- As an example, if
**Surface**: Can be**Opaque**or**Transparent****Blend**: If**Transparent**is selected, a**Blend**type option will appear which determines how the transparency is handled.## Details about each Blend option

The options here are :

**Alpha**: Regular alpha blending. Is equivalent to`Blend SrcAlpha OneMinusSrcAlpha, One OneMinusSrcAlpha`

in ShaderLab (Shader code), where the first term (`SrcAlpha`

, referring to the**Alpha**port of the**Master Stack**) is multiplied by the**Base Color**output and the second term (`OneMinusSrcAlpha`

) is multiplied by the colour already on screen. These two are added together which is then written to the screen. (The other two terms after the comma are used for the alpha channel only)- In this case, the calculation is identical to what a
**Lerp**(linear interpolation) does, with the alpha as the mask/T input. - If the
**Alpha**is 0, the colour on screen is not changed. While a value of 1 might appear opaque due to using the full**Base Color**, there can still be issues with sorting**Transparent**objects as they do not write to the**Depth Buffer**. Can find more information[here](https://www.cyanilux.com/tutorials/depth/#depth-buffer). - In terms of fixing this, there isn’t really a perfect way. Separate opaque and transparent parts of a model. Transparent objects are also sorted by the origins, so if you’re mesh contains multiple transparent parts it’ll sort better if you split them into separate parts. You can also force the Render Queue on the Material if you always want one transparent object to appear in-front of another. Dithering & alpha clip/cutout in an opaque shader can also be used as an alternative to transparency.

- In this case, the calculation is identical to what a
**Premultiply**: Is equivalent to`Blend One OneMinusSrcAlpha, One OneMinusSrcAlpha`

. When used in**Unlit**, it produces the same result as**Alpha**. In a**Lit**graph however, the alpha is multipled with the colour before other calculations are combined, so the other ports like**Smoothness**,**Metallic**,**Ambient Occlusion**, etc. will affect the result. Even at 0 alpha, you may still see something due to these settings.**Additive**: Is equivalent to`Blend One One`

. In other words, the colour on the screen is added with the colour output from the shader. e.g. Red and Green produces Yellow, because that’s how[RGB colours](https://en.wikipedia.org/wiki/RGB_color_model)add together. Outputting a**Base Color**of**Black**(0,0,0) means no change / invisible. The**Alpha**port is not used.**Multiply**: Is equivalent to`Blend DstColor Zero`

. In other words, the colour on the screen is multiplied with the colour output from the shader. Outputting**White**(1,1,1) means no change / invisible. The**Alpha**port is not used.

**Alpha Clip**: Toggles alpha clipping. If enabled, an**Alpha Clip Threshold**port will be added to the Master Stack. For each fragment/pixel, if the**Alpha**value is lower than the threshold the fragment is discarded, meaning it isn’t rendered. This can be done with both surface modes. Using**Opaque**&**Alpha Clip**is common for foliage effects to make sure they are sorted correctly.**Render Face**: Controls whether Front, Back or Both sides are rendered. In older versions, the option was only Front faces or**Two Sided**.- Be aware that for URP you may need to flip the Tangent space Normal for these faces in order to get the correct lighting/shading. You can do this with the
**Is Front Face**node and a**Branch**like so : - Rendering back or both faces in a Lit Graph might also cause issues with shadows if the
**Normal Bias**is used on the URP Asset, as this pushes the vertices in the normal direction which might lead to self-shadowing for back faces.

- Be aware that for URP you may need to flip the Tangent space Normal for these faces in order to get the correct lighting/shading. You can do this with the
**Allow Material Override**also gives you the option to expose these settings to the Material

## Master Stack

Prior to v10, You could switch between graph types by creating a new **Master Node** (e.g. **Unlit**, **PBR**), right-clicking it and setting it as the **Active** one.

In v10 and newer you can still switch types via the Material in the Graph Settings as explained in the previous section. But “Master nodes” were removed and replaced by the **Master Stack**.

Unlike Master nodes, there can only be one Master Stack in the graph. Each port in the stack is attached to a **Block**.

The blocks required by the graph type will automatically change when switching the type (explained in the section above), assuming the “Automatically Add or Remove Blocks” option is enabled in **Edit → Preferences → Shader Graph**.

Any blocks that the previous type had (which are connected to or the default value edited), will remain in the stack but may become greyed out if the new graph type doesn’t make use of them. For example, a **Lit** graph has a **Smoothness** block/port. If something is connected and the graph type changes to **Unlit**, the port will remain but become greyed out as it is no longer used.

Blocks in the stack can be removed by right-clicking them and selecting “Delete” from the dropdown.

Blocks can also be added manually by hovering over gaps between two blocks, or at the end of the last block. Right-click and select **Create Node**, or press **Space**. While you can add blocks, they’ll still be greyed out if the graph type doesn’t use them.

### Vertex vs Fragment

The stack also provides a clearer distinction between the **Vertex** and **Fragment** stages of the shader, and different blocks are available for each.

If you are unfamiliar, the Vertex stage runs for each vertex in the mesh being rendered, transforming the vertex positions onto the screen. Then rasterisation occurs, which produces fragments (basically pixels) from the triangles in the mesh. The Fragment stage then runs for each fragment/pixel created and outputs the colour to the screen. This is discussed in slightly more detail in my [Intro to the Shader Pipeline](https://www.cyanilux.com/tutorials/intro-to-the-shader-pipeline) post.

The Vertex stage is also responsible for passing through any data (e.g. from the mesh) that may be needed in Fragment stage calculations. This is known as **interpolators** (as this data for each vertex is interpolated across the triangle). It is mostly handled automatically by Shader Graph - e.g. For nodes requiring UVs, the **Position** node, **Normal Vector** and other nodes in the **Input → Geometry** heading under the Create Node menu.

But in some cases (discussed later), we may also want to pass our own custom data between the two stages. In Shader Graph **v12** (Unity **2021.2+**), we can do this by adding **Custom Interpolator** blocks to the **Vertex** stage. I’ll discuss this in more detail [near the end of the article](https://www.cyanilux.com#custom-interpolators).

## Save Graph

While I haven’t explained the other parts of a graph yet, this is something that is a common problem for beginners so I’m mentioning it early. Remember to save your graph or changes won’t appear in **Scene/Game View**!

In newer versions using Ctrl+S might now save the graph. You can tell if it works if the `*`

on the window/tab disappears.

Older versions did not have a shortcut and you had to use the **Save Asset** button in the top left corner of the graph.

When attempting to close the graph, it will also prompt you to save if unsaved changes have been made.

## Nodes

To add a node to the graph, right-click and choose **Create Node** from the dropdown, or press the **Spacebar**. A box will open at the mouse position allowing you to search and/or choose a node from the list. As the list is quite extensive, I recommend typing the name of a node once you learn them.

### Ports & Connections

Nodes have **inputs** and **outputs** shown as small circles, known as **ports**. Inputs are always on the **left** side of the node while outputs are on the **right**.

You can create connections between nodes by clicking on the port. While still holding the mouse button, drag over to another port and a connection will be made. You can only connect an output to an input. It’s not possible to connect an input to another input, or output to another output. Output ports can also have multiple connections to other nodes, but input ports must only have a single connection.

(The documentation refers to these connections as “Edges” but I’ve *never* heard anyone actually call them that, except for Unity that is. I’m just going to refer to them as connections)

While dragging a connection from a port, If you release the mouse while **not** hovering over another node port, it will open the **Create Node** menu – filtered to only show nodes where a connection is allowed. Selecting a node from there will then automatically connect it up too. This is very useful for quickly creating graphs.

Existing connections can be changed by clicking and dragging on the connection wire near to the port. In v10+ it’s also possible to drag a selection box over multiple connections coming out of a single output port, and move them all at once to another output.

It’s also possible to collapse unused ports to make the node smaller. This can be toggled with the small arrow in the top right of the node (that appears when hovering over it). You can also right-click the node and use **View → Collapse Ports** and **Expand Ports** to show all ports again.

### Redirect / Elbow

In v10+ you can add a redirect/elbow node by **double-clicking along the connection wire**, (or right-clicking the connection and selecting it from the dropdown). This will create a tiny node with a single input and output port that allows you to better organise connections (example shown below).

To help keep a graph readable, you should avoid having connections pass over other nodes. I’d also recommend keeping connections going horizontally or vertically, rather than diagonally, but this is more of a personal preference.



![(Image)](../../assets/4da7d5e360f72229.png)

An example using (probably way to many unncessary) redirect nodes, (but hopefully you get the point).

Versions prior to v10 did not have this feature, but the **Preview** node could be used instead, with the preview collapsed to make the node smaller to work with.

### Selecting Nodes

Nodes can be selected by clicking on them using the left mouse button, or by clicking in an empty space and dragging a selection box over multiple nodes to select them all at once.

While holding **Ctrl**, you can toggle the selection of nodes rather than unselecting everything else.

### Previews

Most nodes will have a **Preview**, shown on the bottom of the node. They allow you to preview what the shader is doing at that particular stage, but the result might look different in the scene depending on the mesh used. You can also use the **Preview** node to preview a particular port if it doesn’t already have a preview.

Because the **Preview** can take up a lot of space, you can collapse it by clicking the upwards-pointing arrow that appears on the preview while hovering over it. The preview can then be shown again by clicking the downwards-pointing arrow on the bottom of the node. Alternatively, right-click the node and use **View → Collapse Preview** and **Expand Preview**.

Nodes like **Position** and **Normal Vector** use a **3D/Sphere** version of the Preview rather than the **2D/Quad** one, as they are meant to show 3D positions/vectors. All nodes in the chain after it will also switch to using the 3D one when connected.

In Shader Graph **v11+** (Unity **2021.1+**) it is also now possible to choose between the 2D and 3D versions of the preview on a per-node basis. Can do this in the **Node Settings** tab of the **Graph Inspector** window. (This was something I suggested, though some others may have too. Still, I’m very happy to see it included). For Sub Graphs you can also find a setting in the **Graph Settings** to select it’s default preview state.

Before we can go into exactly what these previews are showing, we need to understand the different data types included in Shader Graph :

## Data Types

The **colours** of each port and connection will also change based on the **port data type**, which is also shown in brackets after the input/output name. Usually, different data types cannot be connected, though the Float/Vector types are an exception to this.

The data types are as follows :

- Float (1), light blue (referred to as Vector1 prior to v10).
- Vector2 (2), green
- Vector3 (3), yellow
- Vector4 (4), pink
- Color (Property only. Converts to Vector4 in graph, with colour space converted if using the
[Linear workflow](https://docs.unity3d.com/Manual/LinearRendering-LinearOrGammaWorkflow.html)) - Matrix (2x2, 3x3 or 4x4), blue
- Boolean (B), purple
- Texture2D (T2), red
- Texture2DArray (T2A), red
- Texture3D (T3), red
- Cubemap (C), red
- Virtual Texture (VT), grey : see
[docs](https://docs.unity3d.com/2020.1/Documentation/Manual/svt-use-in-shader-graph.html) - SamplerState (SS), grey
- Gradient (G), grey

### Float & Vector

A **Float** is a scalar (meaning single component) floating point value. While it’s called float, it’s precision can be changed between **Single** (32-bit) and **Half** (16-bit) on a per-node basis (under the **Node Settings** tab of the **Graph Inspector** in v10. Prior to v10, there was a **cog/gear** on the node itself to change this). Usually nodes will Inherit the precision of the previous one. Changing the precision can help with optimisation, mainly for mobile platforms. More information about the precision modes can be found in the [docs](https://docs.unity3d.com/Packages/com.unity.shadergraph@11.0/manual/Precision-Modes.html).

A **Vector** contains multiple components of these floating point values. This could be interpreted as a position or direction, but can also contain any arbitary numbers. The Vector4 contains four floating point values, Vector3 contains three, and Vector2 contains two. The precision again can be varied.

When put into a **Split** node, we can obtain each **Float** the vector contains. These components are usually labelled as **R, G, B, A** as shaders deal with colours a lot, but Shader Graph also uses **X, Y, Z, W** in the case of the **Vector2** / **Vector3** and **Vector4** nodes.

(The labels themselves aren’t too important, they are the same. R=X, G=Y, B=Z and A=W)

#### Truncate

Unlike other data types, different size vectors can be connected to other sized vector ports. For example, A **Vector3** or **Vector4** can be connected to a **Vector2** port (e.g. the **UV** input on a **Sample Texture 2D** node, some more examples are shown below).

This will cause the vector to be **truncated**. In the case of the **Float input** port, only the **R/X** component is used while GBA/YZW is truncated. For a **Vector2**, the **RG/XY** components are used and BA/ZW is truncated, and **Vector3**, **RGB/XYZ** with A/W truncated.

A **Float** output can’t be truncated as it’s already the smallest possible size with only a single component.

#### Promote

Similarly, a smaller sized vector put into a larger sized port will be **promoted**. For example, a **Vector2** put into a **Vector3**. The third component will be filled with a default value of **0**.

If put into a **Vector4** port, the fourth component has a default value of **1** (as it typically corresponds to an **alpha** value, and it defaults to full opaque, rather than invisible. Also useful for matrix multiplciation where the fourth component should be 1 to allow for translation. Don’t worry about that for now though, we’ll be going into matrices in a bit).



![(Image)](../../assets/c2cd0512bb6af2b6.png)

On the left, the Float is promoted to the Vector3 size, (0.5, 0.5, 0.5). After the add, resulting in (0.5, 0.5, 1). On the right, the Vector3 is truncated to the Vector2 size, (0, 0). After the add, resulting in (0.5, 0).

If a **Float** is connected to a **Vector** port, it is promoted where **all components are filled with the float value**. e.g. 0.5 would become (0.5,0.5,0.5,0.5) if connected to a Vector4 port. The alpha value would not default to 1 in this case too, which is something to be aware of.

If you wanted more control over promotion, you could handle it manually, using the Vector node that corresponds to the size you want. e.g. **Vector2**, **Vector3** or **Vector4**. Or use the **Combine** node which gives you an output for all sizes.

These have **Float** input ports for each component. If you are starting with a Vector type, you can use a **Split** node to obtain each component. Of course, you would only connect the components you want to keep and override the others. Note that when a **Split** is used, promotion does not take place and outputs that aren’t used by the input Float/Vector size will be 0.

You can use a **Split** and **Vector4** or **Combine** node to set each component to a specific **Float** if you want better control over how a vector is promoted. (**Split** would not be needed if you start with a Float though since it’s already a single component).

### Dynamic Ports

While not really a data type, Some nodes also have **Dynamic Vector** ports. This means it can change between **Float/Vector1**, **Vector2**, **Vector3** and **Vector4** depending on the inputs.

Examples of these include many of the **Math** based nodes, e.g. **Add**, **Subtract**, **Divide**, **Power**, **Fraction**, **Normalize**, etc.

In most cases, these dynamic vector ports **truncate both to the same size**, based on the **lowest size passed in** (so if a **Vector3** and **Vector2** is passed in to each port, both ports will be a **Vector2**). However a **Float/Vector1** will always be **promoted to the same size as the other input**.

The **Multiply** node ports are also dynamic, but also has a special case where a **Matrix** (will be explained below) can also be connected. Similar to the Vectors, the Dynamic ports are **truncated to the smallest of the two matrix sizes** (the output also changes to a matrix type of the same size). If a matrix and vector is connected, the size of the matrix is used and the Vector will be promoted or truncated to match.

### Matrix

A matrix has up to 16 components, defined in rows and columns. Shaders written in code can define matrices with different row/column sizes, and even different data types, however Shader Graph can only handle **square** ones consisting of floating point values (floats or halfs depending on precision).

A **Matrix4x4** means it has 4 rows and 4 columns, so 16 components in total. Similarly, a **Matrix3x3** has 9 components, and **Matrix2x2** has 4 components.

Matrices are used for applying transformations which consists of translation (adjusting position), rotation, and scaling. Shader Graph has a few useful spaces built-in to nodes though, such as **Object**, **World**, **View** and **Tangent**, so usually you don’t need to deal with matrices. I’ll be going over these spaces in more detail later. There’s also a **Transform** node to transform between these spaces.

It is possible that you may want to handle your own transformations to a custom space too though. The **Multiply** node can be used to achieve **matrix multiplciation** if a **Matrix** is connected. It’s unlikely that you’ll need to deal with matrix multiplication unless you’re doing some very custom stuff, but if you aren’t familiar with it I’d recommend looking it up. This [CatlikeCoding tutorial](https://catlikecoding.com/unity/tutorials/rendering/part-1/) goes over them.

Something to be aware of is when dealing with matrix multiplciation, the **order is important**. Usually the matrix will be in the first input and the vector in the second. A Vector in the second input is treated like a Matrix consisting of up to 4 rows (depending on the size of the vector), and a single column. A Vector in the first input is instead treated as a Matrix consisting of 1 row and up to 4 columns.

Due to the Vector promotion (explained a few sections above), if a **Vector3** is multiplied with a **Matrix4x4**, it’ll promote the vector to a **Vector4** with the alpha component defaulting to 1, which allows the translation part of the matrix to work. If this isn’t what you want, you can **Split** and use **Combine** or **Vector4** to set the alpha component yourself.

### Boolean

A type with two possible values, **True** or **False**. It is used in **Logic** based nodes, for example the **Comparsion** node outputs a Boolean based on comparing two Floats. The Boolean is mainly used in the **Predicate** input of the **Branch** node, which is used to select between two Floats or Vectors based on if the Boolean is True or False. For Example :



![(Image)](../../assets/ac62d3a92d200a6b.png)

Example showing a Branch based on a Boolean Property. Allows switching between two different UV types. Planar projected / regular model UVs.

Internally the type is actually treated as a Float with a value of 0 or 1, so can be set from C# using `material.SetFloat`

(or `SetInteger`

).

Don’t confuse the **Boolean** type/property with a **Boolean Keyword** - these are not the same! I’ll be explaining keywords in a later section.

### Textures

**Textures** store a colour for each **texel** - which is basically the same as a “pixel”, but as that is used to refer to the screen (or current render target) we instead use the term “texels” when referring to textures. They also aren’t limited to just two dimensions.

The fragment shader stage runs on a per-pixel basis, where we can access the colour of a texel with a given coordinate. Textures can have different sizes (widths/heights/depth), but the coordinate used to sample the texture is normalised to a **0-1 range**. These are known as **Texture Coordinates** or **UVs** - **U** corrosponding to the horizontal axis of the texture, while **V** is the vertical.

(Though I mentioned texels have colours, the data doesn’t necessary have to be output as a colour. It’s a **Vector4** which could represent any arbitary data and used for any calculations. Depending on the texture’s [format](https://docs.unity3d.com/ScriptReference/Experimental.Rendering.GraphicsFormat.html) it might also result in values outside a 0-1 range)

#### Filter Modes

To access a colour of a texel, we **sample** it with **filtering** applied. There are 3 different **Filter Modes** :

**Point**(or Nearest-Point) : The colour is taken from the nearest texel. The result is blocky/pixellated, but that if you’re sampling pixel art you’ll likely want to use this.**Linear / Bilinear**: The colour is taken as a weighted average of close texels, based on the distance to them.**Trilinear**: The same as Linear/Bilinear, but it is also blends between mipmap levels.

#### Mip Maps

**Mipmaps** are versions of a texture which are smaller than the original, with each mip map level being half the size of the previous. This produces downsampled/blurry versions of the texture which is useful for lowering detail at a distance, to avoid artifacts like [moiré patterns](https://en.wikipedia.org/wiki/Moir%C3%A9_pattern).

The original texture is known as mipmap level 0. If it’s size was 512x512, then level 1 would have a size of 256x256, level 2 would be 128x128, level 3 would be 64x64, and so on until it reaches 1x1 (level 9 in this case), or a maximum mip map chain count set in the case of textures created through C# code. You can visualise what these mipmaps look like by using the slider on the Texture Preview in Unity’s Inspector :

#### Wrap Modes

This filtering method is stored in the sampler (**SamplerState**), along with a **Wrap Mode** :

**Repeat**: UV values outside of 0-1 will cause the texture to tile/repeat.**Clamp**: UV values outside of 0-1 are clamped, causing the edges of the texture to stretch out.**Mirror**: The texture tiles/repeats while also mirroring at each integer boundary.**Mirror Once**: The texture is mirrored once, then clamps UV values lower than -1 and higher than 2.

#### SamplerState

Every Texture object also defines it’s own [SamplerState](https://docs.unity3d.com/Manual/SL-SamplerStates.html) (in DX10/11 at least, DX9 has them combined into a single “sampler” object but DX9 is deprecated as of Unity 2017.3 anyway. I believe OpenGL also doesn’t support separate textures and samplers, but Shader Graph takes care of this).

DX11 allows you to have up to **128** textures in a single shader but it’s important to be aware that there is a maximum of **16** samplers per shader. If you use more than 16, an error similar to `maximum ps_5_0 sampler register index (16) exceeded`

will be shown. While every texture object in Shader Graph will define a sampler, if left unused the compiler will ignore them.

This means, in order to have more than 16 **Sample Texture 2D** nodes sampling different textures, you will need to connect a **SamplerState** node - Which is the equivalent of HLSL’s [inline sampler states](https://docs.unity3d.com/Manual/SL-SamplerStates.html).

A **SamplerState** property could also be connected, it acts the same way. It cannot be exposed.

#### Texture2D

There a few different texture types as I listed earlier.

Texture2D is the more common one you’ll be familiar with and is sampled with a 2D coordinate (UV). If the UV input on the **Sample Texture 2D** is left blank, it automatically uses the UV0 channel from the mesh. If the **SamplerState** input is left blank, it’ll automatically use the one from the texture.

#### Texel Size & Texture Size

The **Texture Size** node allows us access to the **Width** and **Height** of a 2D texture (in texels), as well as the size of one texel (in terms of the normalised UV coords - so equal to the reciprocal of the texture’s width and height). In older versions of Shader Graph, the node was named **Texel Size** despite only outputting the texture’s size - hence it was renamed. You would have to use **Reciprocal** to calculate the texel sizes. Later, ports for texel size was added.

Specifically the node obtains components of a special Vector4 property that Unity passes into the shader alongside a Texture2D, which matches the texture’s name with `_TexelSize`

appended. The `.xy`

components of that are the Width & Height, while `.zw`

is the Texel Width & Texel Height.

While the node is limited to Texture2D only, you could always set up your own Vector property and pass the size of a different texture type manually or through C# if required. More information about setting up properties will be discussed in a later section.

#### Texture3D

**Texture3D** is similar, but three dimensional, so has a **depth** to it as well as the width and height. It defines a volume of texels so must be sampled with a 3D coordinate in order to select which pixel is output. Shader Graph still labels this as a UV, though it’s common to refer to this as a **UVW** coordinate too, where **W** refers to this depth-based axis similar to the **Z** axis in regular 3D space.

#### Texture2DArray

**Texture2DArray** is very similar to a Texture3D, it is a collection of multiple 2D textures. It is also sampled with a 3D coordinate, though the URP Shader Library functions split these into two variables - a 2D UV coordinate and an index. The same occurs on the **Sample Texture 2D Array** node, with **Vector2** “**UV**” and **Float** “**Index**” ports.

#### Cubemap

A **Cubemap** (also referred to as a TextureCube in HLSL) is another type of 2D texture array that contains 6 slices, one for each side of a cube. It is sampled with a 3D vector that points out from the center of the texture cube. The returned colour is the result of where that vector intersects it.

### Gradient

The gradient type is a bit of an odd one. The type does not exist in regular shaders, It is something specific to shader graph and is actually defined as a struct containing an array of up to 8 colour and alpha values.

|
|

The values are currently something that gets **hardcoded into the generated shader code**, so the Gradient type (created from the Blackboard at least) **cannot be exposed** or set by C# scripts.

If you need to expose something similar to a gradient, the foldout below has a few alternatives :

## Alternatives

#### Color properties & Lerp

If you only need two colours, you can create a gradient quite easily from two **Color properties** and a **Lerp** node. Same with three, perhaps four, but you’ll need to link together multiple lerps and remap the **T** inputs. The below image provides an example for a 3-colour gradient.

While this can work for even more colours, adding that many properties can be tedious.

#### Texture

Another option (especially when lots of colours are required) is to use a **Texture2D** instead. We sample it with the **Sample Texture 2D** with the **UV** coordinate as the same “**Time**” value that would have been used in the **Sample Gradient** node.

This gives us the flexibity of more colours, and can be swapped out more easily, but a texture sample might end up being be more expensive than a math-based method, and potentially suffer from colour banding issues.

For creating the gradient texture, it can either be done manually in your preferred image manipulation software (e.g. Photoshop, GIMP, etc), or baked from a C# Gradient object. For example, using a function like :

|
|

#### Custom Function

It is also technically possible to create a Gradient object in a **Custom Function** and pass it out. This is a node that allows us to write HLSL code, which is useful for accessing things that Shader Graph can’t handle, like arrays and loops. This method still cannot be exposed to the material inspector, but can be set through C# - but only globally.

|
|

The problem here is that these aren’t defined as properties (and arrays can’t be) so should be set through the **Shader.SetGlobalX** functions, not as per-material ones to avoid batching-related issues.

While it might be possible to work around this using multiple **Vector4** properties… It would be annoying to set these up in every graph you need an exposed Gradient for. You’d need 12 Vector4s to support all 8 colour/alpha options, (and another Vector4 / 3 Float properties for the ints), and then you have to deal with setting them through C#.

Using **Matrix4x4** instead *might* work, that would only require 3 which is a lot better than 12. But matrices can’t be serialised so would need to be set through C# at runtime.

I’d personally recommend the **Lerp** or **Sample Texture 2D** approaches instead, but thought I should still mention this too… Maybe it’ll give someone else a better idea for another workaround.

## Coordinate Spaces

Some nodes that obtain positions/directions will have the option to switch between different **Spaces**, including :

**Object**: Coordinates local to the**mesh**. (0,0,0) is the origin/pivot of the mesh. Axis follows the “Local” gizmo.**Absolute World**: Coordinates based on the**scene**. (0,0,0) is the origin of the scene. Axis follows the “Global” gizmo. Similar values used to position GameObjects/Transforms while they have no parent.**World**:- In URP, same as
**Absolute World**currently. - In HDRP, while
[Camera-Relative Rendering](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@10.3/manual/Camera-Relative-Rendering.html)is enabled (which it is by default. It helps combat[z-fighting](https://en.wikipedia.org/wiki/Z-fighting)by keeping values closer to 0), the space is**offset by camera’s position**(but not rotation/scale).`World Pos = Absolute World Pos - Camera World Pos`

.

- In URP, same as
**View**: Space is relative to the camera. (0,0,0) is at the camera’s position. The camera forward axis looks down the**Negative Z axis**. If Z is positive, the vertex/fragment is behind the camera. The Z axis put through a**Negate**node this gives you the[Eye Depth](https://www.cyanilux.com/tutorials/depth/#eye-depth).**Tangent**: Space is relative to the surface of the mesh.- The space is constructed from the mesh
**Tangent**and**Normal**vectors, and a Bitangent/Binormal vector is created based on a[Cross Product](https://en.wikipedia.org/wiki/Cross_product)between the two. - The X axis is the Tangent vector, the Y axis is the Bitangent vector, and Z axis it the Normal vector. The tangent vector also follows the horizontal axis of the UVs, while bitangent follows the vertical axis.
- Tangent space is commonly used for
[Normal/Bump Mapping](https://docs.unity3d.com/Manual/StandardShaderMaterialParameterNormalMap.html). These maps define vectors in tangent space, and it is then converted into World space for lighting/shading calculations.

- The space is constructed from the mesh

While not a space that is included on nodes, it may still be useful to be aware that **Clip space** exists. Behind the scenes the Vertex stage converts the **Object** space **Vertex Position** (port on Master Stack) to **Clip** space, which is important for clipping triangles to what is visible by the camera - so we don’t waste time trying to render fragments/pixels outside the screen. It’s a Vector4, where the XY components range from [-W, W], where W is the fourth component of that Vector4.

With a bit of remapping and dividing by W, clip space is converted to **Screen** space, aka **Screen Position** node (also known as “Normalised Device Coordinates” in SRP shader code). That node also has a few modes, including :

**Default**: (0,0) in the bottom left corner of the screen and (1,1) in the top right. Z/B and W/A components are 0.**Raw**: (0,0) in the bottom left corner, (W, W) in the top right. This is the position before the**Perspective Divide**step. For a Perspective Camera the W/A component gives you the[Eye Depth](https://www.cyanilux.com/tutorials/depth/#eye-depth). For Orthographic is always 1.`Default = Raw.xy / Raw.w`


**Center**: Offset so (0,0) is in the center of the screen. (-1, -1) in bottom left, (1, 1) in top right.**Tiled**: Tiled using**Fraction**and adjusted with screen ratio to produce squares.`Tiled = frac(Center * (ScreenWidth/ScreenHeight, 1))`


- newer versions also have
**Pixel**: (0,0) in the bottom left corner of the screen. Other corner values depend on screen resolution. Z/B and W/A components are 0.

## Understanding Previews

### Float/Vector1

For **Float** types, previews are always **greyscale**. **Black** means the value is **0**, or **negative**, and **White** means a value of **1** or **higher**. Values in-between 0 and 1 show as different greyscale shades.

The exact shade isn’t too important as it can vary depending on whether the project is using [Gamma or Linear colour space](https://docs.unity3d.com/Manual/LinearRendering-LinearOrGammaWorkflow.html) (setting under Project Settings → Player). If you’re using Gamma space, your previews might show more darker areas as the converison to linear isn’t handled. Projects should use Linear as it’s more realistic but Gamma can be more performant, especially for mobile devices.

Visualising values outside of a 0-1 range can be difficult, but nodes like these can help :

**Negate**: Same as multiplying by -1, positive values become negative, negative become positive**Absolute**: Negative values become positive, positive stays the same**Fraction**: Returns the fractional/decimal part of the value. The value will repeat between 0 and 1. Useful for visualising values higher than 1.**Step**: Can compare two values. If the**In**input is greater than or equal to the**Edge**input it returns 1, otherwise returns 0.

### Vector

For **Vector** types, the same applies but previews show up to **three** components in their respective colours (**red, green, blue**). The alpha channel is always ignored. Red corresponds to the first component, green the second, and blue the third.

As well as for colours, vectors are commonly used for **positions** and other coordinates. Some examples are below.

### UV

The **UV** node for example shows a **2D/Quad** preview. It’s output is a **Vector4**, but typically UVs (aka Texture Coordinates) are Vector2. As mentioned the 4th alpha component (which is 1 here) is ignored for previews and the 3rd component is 0 so we don’t see any Blue, only see **Red** and **Green**. From the colours shown, we can see that the red values start in the bottom left corner at 0 as they are darker, then increase to 1 horizontally across the quad, while green starts at 0 increasing to 1 vertically.

- Bottom Left Vertex = 0, 0
- Top Left Vertex = 0, 1
- Bottom Right Vertex = 1, 0
- Top Right Vertex = 1, 1

Where values of red and green are both larger than 0, we start getting shades of yellow due to the additive nature of the [RGB colour model](https://en.wikipedia.org/wiki/RGB_color_model).

It’s important to note that these UVs are for the **Quad mesh** that’s used in previews. Meshes in the scene might have their own UVs (assuming they were UV mapped when created in a 3D modelling program, e.g. Blender) and might even make use of the Blue or Alpha channels too. e.g. For the Skybox, the UVs are actually filled with a 3D position, equal to the **Position** node.

When we use the **Sample Texture 2D** node, these **UVs** are used as an input, where they correspond to the part of the texture to sample. In the case of the default quad UVs this just shows the texture (though since alpha is ignored it can show either black areas, or colour bleeding as some programs/formats won’t store RGB values in areas with 0 alpha).

It’s possible to offset or adjust the tiling of the UVs through **Add** and **Multiply** nodes, or by using the **Tiling And Offset** node. We can even offset each part of the UVs by different amounts, e.g. using **Simple Noise** or **Gradient Noise** nodes (or noise sampled from another texture). This distorts the UV coordinates, and so the resulting texture sample is also distorted.

The noise has values in a range from 0 to 1 (though this may vary depending on the noise used), so we **Subtract** **0.5** to center the distortion. We also **Multiply** by a small value to lower the strength of the distortion, as values of -0.5 and 0.5 would offset a coordinate by half of the texture.

Something to also note is the noise output is a **Float**, but the **Offset** is a **Vector2**, so it is being promoted. The distortion is using the same value in both axis of the texture so it will only ever offset in a diagonal direction towards the bottom left or top right. There is other methods that allow the distortion to be in any direction, for example using a flow map (which are very similar to Bump/Normal maps). This [CatlikeCoding](https://catlikecoding.com/unity/tutorials/flow/texture-distortion/) article is a good example of those, also offset by repeating time to create flowing water materials.

### Position

The **Position** node shows similar colours, but shows a **3D/Sphere** and the output is **Vector3**. Again no blue shades are shown, but this time it’s because the side of the sphere facing us is the negative Z axis. The blue parts of the sphere are hidden on the other side. We can **Negate** the result to flip everything and blue will be shown. We can also use an **Absolute** node to bring negative values back into a positive range.

In the preview, the center is the point (0,0,0), with the X axis (red) increasing to the right, and decreasing to the left. The Y axis (green) increasing upwards and decreasing downwards. The values range from -0.6 to 0.6 in each axis but this isn’t important as it will vary depending on the mesh and space used.

Visualising some positions in the **Scene View** can be difficult. e.g. For **World** space, **(0,0,0)** (visualised as black) would be near the scene’s origin, but the object the shader is applied to could be much further away. I find it useful to put the position through a **Fraction** node to see each unit square, especially when trying to debug something like [Reconstructing a position from Depth](https://www.cyanilux.com/tutorials/depth/#reconstruct-world-pos).

## Main Preview

You can also use the **Main Preview** window to view the final shader result based on what is connected to the **Master Stack** (or active **Master Node**), though personally I prefer to view the shader applied to an object in the **Scene View** instead.

Use the button in the top right of the graph to toggle the **Main Preview** window. The window can be resized by dragging the bottom right corner of it (same goes for the other windows). Unlike node previews, this will show alpha/transparency.

Dragging will rotate the model. It doesn’t move the camera or light direction though so this isn’t always useful.

Right-clicking anywhere inside the window will also allow you to change the **mesh** being used. It defaults to a sphere mesh, but strangely it’s not the same as the “Sphere” on the dropdown. The default (which is the same sphere used for node previews) has UVs that wrap around it **twice**, while the one on the dropdown is the same as Unity’s default sphere mesh which has UVs that wrap around **once**. This isn’t too important since it’s just a preview, but it might be something to be aware of still.

## Blackboard Window

Shaders can expose some of these data types as **Properties**, which are created from the **Blackboard** window. The visibility of the window can be toggled using the button in the top right of the graph.

### Path

The **Blackboard** window also allows you to adjust the **path** of the shader when it appears in the **Shader dropdown menu** on the Material. This is the grey text under the graph name at the top.

By default it shows under the “Shader Graphs” heading but this can be changed. It *really* doesn’t look like an editable field - but you can **double-click** it and it will change into a editable field.

You can also use slashes to create sub-headings to organise your shaders better.

### Properties

To create a **Property**, use the “+” button in the **Blackboard**, a menu will be shown with the different data types as listed earlier. Once created we can name the property. Right-clicking the property will give us options like **Rename**, **Delete** and in v10+ **Duplicate** was also added.

If we have a data type node in the graph, (e.g. Nodes like **Float**, **Vector2**, **Color**, etc), we can also right-click them and choose **Convert To → Property** from the dropdown to create the property automatically, with the default value set from the value it had before converting. It’s also possible to convert a property back using **Convert To → Inline Node** if required. These can be done to multiple nodes/properties at once if multiple are selected.

Each property in the **Blackboard** can be dragged into the graph to add it as a node. You can also use the **Create Node** menu by typing it’s name, or “Property” to see all of them.

Prior to v10, an arrow was on the left of each property to expand extra settings for it. In v10+ these settings were moved to the **Graph Inspector** window in the **Node Settings** tab. While a property is selected in the **Blackboard** or in the graph, the settings will appear there. (I’m personally not a fan of this change as it makes creating properties a bit awkward when having to go back and forth between two separate windows, so I’m very much hoping it’s reverted).

The settings available for each property can vary slightly but most types will have **Reference**, **Exposed**, **Default** and **Precision** options. Some also have additional **Modes**. I’ll discuss these in the sections below.

Some may also include a “**Override Property Declaration**” (or “Hybrid Instanced” prior to v10). The **Hybrid Per-Instance** option on this is related to the [DOTS Hybrid Renderer](https://docs.unity3d.com/Packages/com.unity.rendering.hybrid@latest). I’m not very familiar with DOTS, so if you want more information about it, see [here](https://learn.unity.com/tutorial/what-is-dots-and-why-is-it-important) and [here](https://unity.com/dots). There’s also **Global** and **Per-Material** options but I would avoid overriding the property declaration unless you are using the Hybrid Renderer as it can break the [SRP Batcher](https://www.cyanilux.com/tutorials/intro-to-the-shader-pipeline/#srp-batcher) compatibility.

#### Reference

The settings for each property can vary slightly, but all will have a **Reference** field.

Prior to v12 (Unity 2021.2) this defaults to an auto-generated string, while v12+ attempts to use the same as the name, but with “_” appended to the front (and in place of any spaces/hyphens/other symbols). This reference field is important for setting the property from a C# script, which will be discussed in a later section.

You can edit this reference if you’d like. I’d recommend making it begin with an underscore ("_") as this helps avoid issues with certain words - specifically words that are used as important keywords in HLSL or the Shaderlab section of the generated shader code.

For example, “Cull”, “Offset”, “float”, “void” will cause the graph to break. Might show a similar error to `syntax error: unexpected TOK_CULL, expecting TVAL_ID or TVAL_VARREF`

. But “_Cull”, “_Offset”, etc would work fine (though have nothing to do with the actual Cull/Offset functions, it’s just a string/name used to identify the property). Note that in v12+ Shader Graph automatically attempts fix references like this in order to prevent errors.

Note that the SamplerState node generates it’s reference based on the other settings so it cannot be edited. That data type also cannot be set through C# though.

#### Exposed / Scope

Most properties will also have an **Exposed** tickbox, or **Scope** dropdown in newer versions (with Local or Global options).

If exposed/local, these properties will appear in the **Inspector** window when viewing a **Material** (Unity’s regular Inspector that is, not the Graph Inspector). Materials allow you to have separate textures/values for each instance, while still sharing the same shader. These properties can also be set through C# as I’ll explain later.

If un-exposed/global, the properties will not appear on the Material, but can still be set from C# as a **Global Shader Property** - by using the static methods in the [Shader](https://docs.unity3d.com/ScriptReference/Shader.html) class. This means all instances of the material, and even materials sharing the same reference will use that value. This can be very useful for easily sending data into all shaders/materials that shouldn’t change per-object.

Not all properties in the Blackboard can be exposed however. e.g. **Matrices**, **SamplerState** and **Gradient** objects. (Though matrices *can* actually be set locally (on material) through C#)

#### Default Value / Preview Value

The **Default** field is the value the property will default to when a **Material** is first created.

If a **Material** is already created, changing the **Default** values for an exposed property won’t affect them. You would have to adjust the value on the material manually through Unity’s **Inspector**. Be aware of this as it’s a common issue that you might encounter when trying to debug your shader. If your shader is producing different results in-graph than in-scene, the values on the **Material** would be the first place to check. (If the problem isn’t there, it could also be related to the mesh, e.g. UV Mapping related, if your shader is using the UV channels that is).

It is also the value that will be used in the node **Previews** so it can be important to set this field.

#### Modes

Some properties will have different “**Modes**”, with options shown in these foldouts :

## Float

**Default**: Shows a regular float field in the Material Inspector.**Slider**: Equivalent of the “Range” property in shader code. Can set a**Minimum**and**Maximum**value. The property will appear with a slider in the inspector. Setting from C# can still cause the value to go outside the slider’s range. If this isn’t intended you’ll need to clamp the value manually. In 2019.3+ you can obtain the min/max from the property, see an example[here](https://twitter.com/Cyanilux/status/1337181494729699328).**Integer**: Shows a field that can only be set to integer values. Still acts as a float behind the scenes though. If setting from C#, Unity provides a SetInteger / SetGlobalInteger method.**Enum**: This should show as a dropdown of values, based on a C# enum or string of values (like “A, 1, B, 2”). But while this option is included there doesn’t seem to be a way to set that C# enum or string… so it doesn’t work.

## Color

**Default**: A regular colour. From the Material Inspector it can only be set to values between 0 and 1. From C# it can be set outside that range, though be aware that the final shader won’t be able to output values outside the range unless HDR is enabled on the URP Asset.**HDR**(High Dynamic Range) : A colour where values can be outside the 0-1 range. The inspector shows this by having an**Intensity**slider added to the Colour Picker UI. In terms of setting this from C#, you can multiply the Color with a float if you want a brighter result e.g.`material.SetColor("_Color", Color.red * 5f);`

. If you care about keeping it using the same result as the UI, multiply by`2^Intensity`

(aka`color * Mathf.Pow(2, intensity`

) instead.

As a note, prior to v10 Unity didn’t correct HDR colours to the correct colorspace for the project. Graphs imported into v10+ will show the property as “Deprecated” but it can be upgraded in the **Node Settings** tab of the **Graph Inspector**, assuming you want the proper behaviour. If you’re in v10+ and want the old behaviour, You can also use a **Colorspace Conversion** node to convert from **RGB** to **Linear** to mimic it.

## Texture2D

**White**: Defaults to white (1,1,1,1) when a texture isn’t assigned.**Black**: Defaults to black (0,0,0,0) when a texture isn’t assigned.**Grey**: Defaults to grey (0.5,0.5,0.5) in**Gamma**colour space only, when a texture isn’t assigned. Alpha of 0.5 in both colour spaces.**Bump**(renamed to**Normal Map**in v12+) : Defaults to (0.5,0.5,1,0.5) when a texture isn’t assigned. This should always be used for tangent space bump/normals maps. The colour converts to a normal direction of (0,0,1).**Linear Grey (v12+)**: Defaults to (0.5,0.5,0.5,0.5) in both**Linear**and**Gamma**colour spaces, when a texture isn’t assigned. See the [LinearOrGammaWorkflow docs page] for more information on color spaces.

Note that other texture types (Texture3D, Texture2DArray, Cubemap, etc) default to the **Grey** mode when a texture (despite the generated code trying to use `"white"`

, which isn’t a valid mode for those types)

#### Precision

All properties will also have a **Precision** option, which can be changed between **Inherit**, **Single** (32-bit) and **Half** (16-bit). If set to **Inherit** the properties will default to the **Precision** in the **Graph Settings** tab of the **Graph Inspector**.

I usually don’t worry to much about the precision, but it may be important if you’re targetting mobile platforms. It can help to make the shader more performant. You can learn more about precision in the [shadergraph docs](https://docs.unity3d.com/Packages/com.unity.shadergraph@11.0/manual/Precision-Modes.html).

#### Setting Properties from C#

Properties can also be set from a **C# script** through the [Material](https://docs.unity3d.com/ScriptReference/Material.html) class (only if exposed), or set globally through the static methods in the [Shader](https://docs.unity3d.com/ScriptReference/Shader.html) class. Follow those links to see a list of these methods. When setting a property using them, it’s important to use the [Reference](https://www.cyanilux.com#property-reference) of the property, and not it’s name in the **Blackboard**.

Note, since a **Matrix** cannot be exposed, by default they are declared in the **UnityPerMaterial** cbuffer which allows the SRP Batcher to function and the matrix can be different for each material. This however leads to garbage results when setting the matrix globally. If you want a global matrix, you should use the **Override Property Declaration** in the Node Settings to force it to **Global**. Don’t override it for other property types (unless you know what you are doing) as it can break SRP Batcher compatibility.

For more information and example code on setting properties from C#, see the section in my [Intro to the Shader Pipeline post](https://www.cyanilux.com/tutorials/intro-to-the-shader-pipeline/#properties). It’s also important to understand the difference between using `Renderer.material`

and `Renderer.sharedMaterial`

, so see the section [here](https://www.cyanilux.com/tutorials/intro-to-the-shader-pipeline/#material-instances) too.

### Keywords & Shader Variants

As well as Properties, the **Blackboard** also allows us to add **Keywords**. In the “+” menu, under the Keywords heading there is the following options :

**Boolean Keyword**: Keyword consisting of two states, labelled as**On**and**Off**.**Enum Keyword**: Keyword consisting of multiple states (up to a maximum of 8). You can select the display text used for each entry, but note that the Material Inspector may not update unless Unity is reloaded.- Built-in Keywords, currently consisting of only :
**Material Quality**: Same as Enum but predefined by Unity. I believe**HDRP**has a**Material Quality Level**somewhere in it’s Quality settings (under Project Settings → HDRP). However, URP does not seem to have this so I’m unsure if it can be set, without perhaps using C#, e.g.`Shader.EnableKeyword("MATERIAL_QUALITY_HIGH")`

though I haven’t tested that. I’d recommend using a custom Enum instead as you’d have better control over it.


Keywords allow you to create **multiple versions of the shader**, with and without calculations included. These are known as [Shader Variants](https://docs.unity3d.com/Manual/SL-MultipleProgramVariants.html). Each **Material** uses the given shader but can enable/disable keywords to select which variant is used.

Shader Graph has a set maximum number of **Shader Variants** that can be generated, which defaults to **128**. A warning should show if your shader generates more than the maximum (though that seems to be bugged in v10.2.2 due to a NullReferenceException). Only variants produced from Keywords created in the **Blackboard** counts for the maximum, keywords used interally won’t affect it.

The maximum can be edited in **Edit → Preferences → Shader Graph**, however it is important to realise that with each keyword added it **exponentially creates more variants**. And more variants will also slow down build times. With 7 Boolean Keywords (2 states, On and Off), the shader produces 2^7 or 128 variants, so hits the limit exactly. I recommend to be careful with keywords as you don’t want to over-use them for everything. They should be used in a situation where you need to toggle an effect because it would greatly affect performance if a **Branch** was used instead (which would still calculate both sides and discard one).

Each keyword can be dragged into the graph to add it as a node. You can also use the **Create Node** menu by typing it’s name, or “Keyword” to see all of them. The created node will resemble other nodes and have input ports (either On/Off for the **Boolean Keyword**, or the Entries for the **Enum Keyword**). Only **Floats** and **Vector** types can be connected.

Similar to Properties, you can find settings for each keyword under the **Graph Inspector** window in the **Node Settings** tab. While a keyword is selected in the **Blackboard**, the settings will appear there. (Prior to v10, an arrow was on the left of each keyword to expand extra settings for it).

Strangely, selecting the keyword node in the graph does not show the settings. I assume this wasn’t intended and might be fixed in the future.

#### Scope

Each keyword has a **Scope** setting, which can be set to **Local** or **Global**. This can affect how the keyword is set from C#, as explained in the next section. It does not affect how the keyword is exposed in the **Material Inspector** however. The inspector will always toggle the keyword locally.

There is a maximum of **256 Global** keywords that can be used **per-project**. Unity uses some of these interally, (apparently around 60 but that was referring to the Built-in RP). **Local** keywords have a maximum of **64 per-shader**.

These limits cannot be changed, so it is recommended to always use **Local** keywords (unless you need to set it globally through C# that is).

#### Exposed

To expose a **Boolean Keyword** in the **Material Inspector** it’s **Reference** must end in “_ON”.

For versions prior to v10, keywords had the **Exposed** tickbox but this still required the “_ON” suffix. The tickbox could only be used to *un-expose* the keyword if it had the suffix. This was removed in v10+, but you can always use a reference without the suffix if you don’t want it exposed.

**Enum Keywords** are always exposed by default and there doesn’t appear to be a way to set it as unexposed since the tickbox was removed. This shouldn’t be that important though as the keyword can still be accessed from C# regardless of whether it is exposed or not.

#### Definition

Each keyword has a definition field which has the following options :

**Shader Feature**: Unity will strip unused shader variants at build time.**Multi Compile**: Unity does not strip any shader variants.**Predefined**: Unity or the Render Pipeline has already defined the keyword so it should not be redefined. This is used only to create an “`#ifdef REF`

” (aka`#if defined(REF)`

) check on the given reference.- Prior to v10 it was possible to use this to output different values based on the shader pass. However due to changes it can only be done through a Custom Function now. More information and examples can be found in the
[Shader Pass Defines](https://www.cyanilux.com#shader-pass-defines)section (under the Advanced heading at the end of the post).

- Prior to v10 it was possible to use this to output different values based on the shader pass. However due to changes it can only be done through a Custom Function now. More information and examples can be found in the

It’s important to be aware that since **Shader Feature** strips unused variants from the build, it is not recommended to set the keywords at runtime from C#, since the required variant might not be included and result in a magenta error shader. If you plan on adjusting keywords at runtime, you should use **Multi Compile** instead.

#### Setting Keywords from C#

To adjust keywords in C#, we can use **EnableKeyword** and **DisableKeyword** methods in the [Material](https://docs.unity3d.com/ScriptReference/Material.html) class to toggle a keyword per-material, or the [Shader](https://docs.unity3d.com/ScriptReference/Shader.html) class to toggle a keyword globally, for all materials. Like properties, the string used to toggle a keyword in C# is it’s **Reference** field in the **Blackboard**.

Keywords using the **Global** scope can be set through either class. Note that if a keyword is enabled globally through `Shader.EnableKeyword`

it cannot be disabled or overriden using `Material.DisableKeyword`

(or the inspector toggle).

Keywords using the **Local** scope can only be set through methods in the [Material](https://docs.unity3d.com/ScriptReference/Material.html) class.

It is also recommended to only adjust **Multi Compile** keywords at runtime, see [Definition](https://www.cyanilux.com#keyword-definition) section below for more information.

For example, for **Boolean Keywords** :

|
|

For an **Enum Keyword** you need to append the **Entry’s Reference** to the **Keyword Reference**, separated with “_” to obtain the full string to use in the C# methods. The references for each entry is shown in the table in the **Node Settings** tab.

As an example, a **Keyword** with a **Reference** of “ENUM” and the entry “A”, can be toggled using “ENUM_A”. You also shouldn’t enable multiple entries at the same time. To switch between entires, you should always disable the others or the variant used might not change properly. e.g.

|
|

### Categories

In v12+ it is also now possible to create **Categories**, to better organise the properties in the **Blackboard** (and in the Inspector when viewing the material).

Can create them from the **+** button (same that you would use to add a property/keyword), then rename by double-clicking the Grey “Category” text.

They are also collapsable (by pressing the triangle to the left) which is useful if the graph has a large amount of properties.

## Grouping Nodes

To help with organising your graphs, you can group sections of nodes together. Drag a selection box over multiple nodes, right-click on one of those selected nodes, then choose **Group Selection**. Or use the **Ctrl+G** shortcut.



![(Image)](../../assets/a78ef52efe0d82da.png)

Example section of a graph containing a couple grouped nodes. Helps to understand what the nodes are doing at a quick glance.

Once a group is created you can give it a name which appears at the top in a large text size. The group can also be renamed at any time by double-clicking the name. The name will always be on a single line and affect the width of the group so it’s a good idea to keep it short.

A group can be moved around (along with it’s contents) by dragging the group’s name.

If you want to remove nodes from the group, select them and use **Ungroup Selection** or **Ctrl+U** to separate them from the group.

To delete a group entirely without affecting it’s contents, select the group by clicking it’s name, then use the **Delete** key on your keyword. To delete a group with it’s contents, right-click the group and use the option from that dropdown.

## Sticky Notes

You can also add **Sticky Notes** to a graph (Added in v7.4-ish?), by right-clicking an empty space in the graph and selecting **Create Sticky Note** from the dropdown.

These are for adding comments to your graph. They have a text field at the top for a title, and a larger box for the text body. The text can be edited by double-clicking one of the fields. They can also be resized by dragging the edges.

Right-clicking the Sticky Note will give you some additional options including :

- Toggle Light/Dark Theme : Switch between the Light and Dark themes. Currently it’s not possible to change the colour further than this.
- Small, Medium, Large or Huge Text Size : Adjusts the text size. This changes for both the title and body at the same time. The title will always have larger text size than the body.
- Fit To Text : Resizes the Sticky Note so that it precisely fits it’s contents. It will resize horizontally to fit the title on a single line.
- Delete : Deletes the Sticky Note

In **v11+** (Unity **2021.1+**) it should also now be possible to use [Rich Text](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/StyledText.html) to add additional formatting like bold (using `<b>example</b>`

), italics `<i>example</i>`

, colors (`<color=red>example</color>`

), etc.

## Shortcut Keys

There are a few keyboard shortcuts available to speed up working with Shader Graph. Some of these might have been mentioned in other sections. These shortcuts include:

**Space**: Access the**Create Node**menu**A**: Fits the graph to the viewport. Useful if you want to quickly zoom out to see the entire graph.**F**: Focuses on a selected node (/group of nodes). If nothing is selected, it does the same as the above.**O**: Moves the viewport to the origin of the graph. This might not really be useful though.**Ctrl**: While held, clicking nodes/properties will toggle selection of them**Ctrl+X**: Cut a selection of nodes**Ctrl+C**: Copy a selection of nodes**Ctrl+V**: Paste a selection of nodes**Ctrl+D**: Duplicate a selection of nodes**F1**: Open the Documentation for a specific node (Note, some pages might not exist / be missing). See the full[Node Library here](https://docs.unity3d.com/Packages/com.unity.shadergraph@11.0/manual/Node-Library.html).**Ctrl+G**: Group a selection of nodes. If nodes were already in a group, they will be removed from the previous one and added to the new group.**Ctrl+U**: Remove a selection of nodes from a group**Delete**: Deletes selected connections and nodes. If a group is selected, the group is deleted without affecting it’s contents (unless they are selected too). Some nodes, like a Sub Graph’s**Output**node cannot be deleted.**Shift + Space**: Toggles Maximize on the Unity window the mouse is currently hovering over. This is one of Unity’s shortcuts for all windows, not just Shader Graph. The shortcut can be edited via Edit → Shortcuts… → Window.

Shader Graph currently does not have any shortcuts for easily placing/creating nodes.

## Sub Graphs

As briefly mentioned earlier in the post, a **Sub Graph** is special type of graph that can be used as a **node** in other graphs, which is useful for functions you’d like to reuse. They can even be nested in other Sub Graphs (though it’ll prevent you creating a recursive loop where Sub Graphs try to call themselves).

Similar to other graphs, the **path** can be adjusted in the **Blackboard**, which determines how it appears in the **Create Node** menu. Use slashes to create sub-headings. See the [Path](https://www.cyanilux.com#path) section above for more information.

There is two ways to create a **Sub Graph** :

**Create → Shader**menu. This creates a blank Sub Graph with defaults to a single**Vector4**output, but this can be changed. See next section.**Convert To Sub Graph**: In any graph, you can drag a selection over some nodes, right-click one of the selected nodes, and convert to a**Sub Graph**(**Convert To → Sub-graph**). This will put the selected content into a new Sub Graph and should automatically create inputs/outputs and retain their connections. Note it only creates inputs if a connection from a non-selected node is going into one of the selected nodes.

### Outputs

In v10+ we can adjust the number of outputs and change their data types by selecting the **Output** node (left-click on it). A list will appear in the **Node Settings** tab of the **Graph Inspector** window, (It’s incorrectly labelled as “Inputs”, in v12 at least, but this might be fixed in the future).

Prior to v10 a cog/gear could be found on the **Output** node to adjust these instead.

The first output is used to create the node’s Preview. It must be a **Float**, **Vector**, **Matrix**, or **Boolean** type or the **Sub Graph** will error. Other outputs can be any type from the dropdown (though Virtual Texture appears to not be supported and is greyed out).

(You may also see some other “Bare” texture types if in v10.3+ but they’ll be greyed out. They are only used if a **Sub Graph** was using those texture types prior to updating. See the [Better Texture Data Types](https://www.cyanilux.com#better-texture-data-types) section for more information on why this change was made).

### Inputs

It’s also possible to create **Inputs** for the **Sub Graph**, which uses **Properties** that can be created from the **Blackboard**. See the [Properties](https://www.cyanilux.com#properties) section above for more information. Note however that some settings (like modes) will be hidden.

These inputs will always show as ports when the **Sub Graph** is added to another graph as a **node** and cannot be exposed to the **Material Inspector**.

### Branch On Input Connection

A pretty neat feature added in **v12+** (Unity **2021.2+**) is the **Branch On Input Connection** node, which is available for Sub Graphs. It’s purpose is to allow you to create a Branch (graph selects between two options) based on whether a node is connected to the Input port when the subgraph is used.

To use this, we first need to enable the **Use Custom Binding** option on the Input, which is found in the **Node Settings** tab of the **Graph Inspector** window when the Input is selected.

When ticked, a text field for a **Label** appears. This will be the text that appears next to the port when nothing is connected to the **Sub Graph** node (Similar to how “AbsoluteWorld Space” and “World Space” appear on the **Position** and **Normal** ports on the **Triplanar** node).

In the Sub Graph, we can then add the **Branch On Input Connection** node and connect our Input to the **Input** port, as well as the **Connected** port as we want to use it’s value.

In this example I’m using the **Normal Vector** node (mesh normal) for a custom lighting calculation. By using the **Branch On Input Connection** it allows us to optionally connect a Vector3, allowing for this custom lighting to support normal maps.

Having this in our Sub Graph is much better than not providing support for normal maps, or having to expose a regular Vector3 port and making the user connect a **Normal Vector** node (or normal map transformed into World space) for it to function correctly.

In this case I haven’t got a proper normal map so instead of using a **Sample Texture 2D** node with **Normal** mode, I’m using the **Normal From Texture** node which converts a height map into a normal map by using 3 texture samples (though may be less accurate). See [Normal From Texture docs page](https://docs.unity3d.com/Packages/com.unity.shadergraph@12.1/manual/Normal-From-Texture-Node.html) for more info.

## Fragment-Only Nodes

Some features of shaders are limited to the **Fragment** shader stage :

- Screen-space Partial Derivatives (
**DDX**,**DDY**,**DDXY**) : What these do is a bit complicated so not going into a lot of detail. In short, GPUs run the fragment shader in 2x2 pixel blocks, so can compare values with neighbouring pixels horizontally (ddx) and vertically (ddy). The values are subtracted giving what is apparently called a partial derivative.- DDXY, also known as
`fwidth`

in shader code, is equal to`abs(ddx) + abs(ddy)`

- Some uses of these are mentioned below (mipmaps, local anti-aliasing)

- DDXY, also known as
**Is Front Face**: Is true if the fragment is on the front side of the face. False if on the back side of the face. Only important if**Two Sided**is enabled.

Connecting these to the **Vertex** stage is not possible. Quite a few nodes also make use of these partial derivatives so also can only be used in the **Fragment** stage. For example :

**Sample Texture 2D**: Uses partial derivatives in order to calculate which mipmap level should be used.- If you need to sample a texture in the
**Vertex**stage, you should use a**Sample Texture 2D LOD**instead so you can specify which mipmap is used yourself, usually level 0. - In code, this would be SAMPLE_TEXTURE_2D(texture, sampler, uv, lod)`

- If you need to sample a texture in the
**Sample Texture 2D Array**: Same as the above, However a LOD verison of the node isn’t provided. Instead use a**Custom Function**with :`SAMPLE_TEXTURE2D_ARRAY_LOD(texture, sampler, uv, index, lod)`


**Sample Texture 3D**: Use a**Custom Function**with :`SAMPLE_TEXTURE3D_LOD(texture, sampler, uvw, lod)`


**Normal From Height**: Calculates a normal based on a Float input. Can only be used in the Fragment**Normal**input (Tangent or World space), as it makes use of ddx/ddy.- Procedural Shapes (e.g.
**Ellipse**,**Rectangle**,**Polygon**,**Rounded Rectangle**,**Rounded Polgyon**) : All make use of`fwidth`

(aka**DDXY**) for local anti-aliasing. See their documentation pages to see the code used. Using a**Custom Function**with the`fwidth`

removed would allow it to function in the vertex stage. Use a**Step**(or**Smoothstep**) node to convert the distance field to the shape itself. **Checkerboard**: Has local anti-aliasing applied using ddx/ddy. Not sure why you’d need this in vertex stage anyway though.

The following nodes also use 2D texture samples. It may be possible to create alternatives to these that use the Sample 2D LOD version instead.

-
**Triplanar**: Typically isn’t used per-vertex, but if needed, you would have to create your own Triplanar setup, with**Sample Texture 2D LOD**nodes instead. -
**Normal From Texture**: Calculates a normal based on a greyscale texture. Can find the code used for the node[here](https://docs.unity3d.com/Packages/com.unity.shadergraph@10.3/manual/Normal-From-Texture-Node.html).- Note : Not to be confused with sampling a bump/normal texture, which can be done using the
**Sample Texture 2D**node with the**Normal mode**. You wouldn’t usually sample a normal texture per-vertex, but that could be done with the LOD version of the node too.

- Note : Not to be confused with sampling a bump/normal texture, which can be done using the
-
**Scene Color** -
**Scene Depth**- For URP, see
[here](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl). It uses regular texture sampling while vertex stage would need to use a LOD version :

## Scene Depth LOD Custom Function (URP)

- Inputs :
- “ScreenPosition” (Vector2)

- Outputs
- “Out” (Float)

- Type : File
- Function Name : “SceneDepthLOD”

`1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20`

`#ifndef SCENEDEPTH_LOD #define SCENEDEPTH_LOD #ifndef SHADERGRAPH_PREVIEW #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl" #endif void SceneDepthLOD_float(float2 ScreenPosition, out float LinearDepth) { #ifdef SHADERGRAPH_PREVIEW = 0; //EyeDepth = 0; #else float RawDepth = SAMPLE_TEXTURE2D_X_LOD(_CameraDepthTexture, sampler_CameraDepthTexture, UnityStereoTransformScreenSpaceTex(ScreenPosition), 0).r; LinearDepth = Linear01Depth(RawDepth, _ZBufferParams); //EyeDepth = LinearEyeDepth(RawDepth, _ZBufferParams); #endif #endif // SCENEDEPTH_LOD`

- Untested but for Built-in RP, I’d maybe try the same as the above function but without the
`#include`

and define the texture yourself (i.e.`TEXTURE2D_X_FLOAT(_CameraDepthTexture); SAMPLER(sampler_CameraDepthTexture);`

) or via the Blackboard as Texture2D property with Exposed unticked / Global scope. - For HDRP,
`SampleCameraDepth(float2 uv)`

in[ShaderVariables.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.high-definition/Runtime/ShaderLibrary/ShaderVariables.hlsl)actually already uses an LOD version, you may still need to handle it in a**Custom Function**though.

- For URP, see
-
**Parallax Mapping**(v10.1+) : Uses texture sample, but would only ever be used in the fragment stage. -
**Parallax Occlusion Mapping**(v10.1+) : Technically I don’t think this node uses anything that would prevent it working in the vertex stage, but it would only ever be used in the fragment stage so is still limited to fragment-only.

Note, that when working with **Sub Graphs**, if one of these Fragment-only nodes is used, **all it’s outputs cannot be connected to the Vertex stage**. The shader won’t break if connections were made previously to converting it to a Sub Graph, but if un-connected, it won’t be possible to reconnect them without editing the Sub Graph. I recommend keeping all Vertex vs Fragment parts in completely separate Sub Graphs to avoid these issues.

If somehow you manage to create a connection to a Vertex port including a Fragment-only node, it will result in a shader error similar to `cannot map expression to vs_5_0 instruction set`

.

## Advanced

This final section includes some additional features of Shader Graph that I’d consider to be more advanced.

(I would have put some of the content in the [Gradient](https://www.cyanilux.com#gradient) & [Array](https://www.cyanilux.com#array) sections here instead, as that was also more advanced than I wanted the post to be, but felt it fits better to keep that under the [Data Types](https://www.cyanilux.com#data-types) section/heading)

Learning stuff below might not be necessary to get started, but may be useful to come back to! If you stop reading here, thanks for reading! Please consider sharing a link to others if you found this useful! <3

### Custom Interpolators

The Vertex stage is responsible for passing through any data (e.g. from the mesh) that may be needed in Fragment stage calculations. This is known as **interpolators** (as this data for each vertex is interpolated across the triangle). It is mostly handled automatically by Shader Graph - e.g. For nodes requiring UVs, the **Position** node, **Normal Vector** and other nodes in the **Input → Geometry** heading under the Create Node menu.

But in some cases we may also want to pass our own custom data between the two stages. In Shader Graph **v12** (Unity **2021.2+**), we can do this by adding **Custom Interpolator** blocks to the **Vertex** stage (by right-clicking, then selecting **Add Block Node**). There is a [docs page here](https://docs.unity3d.com/Packages/com.unity.shadergraph@14.0/manual/Custom-Interpolators.html) for this, but below also explains how to use it and some usage examples.

We can then change the name and type in the **Node Settings** tab of the **Graph Inspector** window while the block is selected.

You can have multiple interpolators. The maximum is 32, though the actual amount you can use will depend on the target platform (I believe gles platforms may be limited to 8, as they use the SubShader with target 2.0, even though gles3 can actually support more). The [Shader Compile Targets](https://docs.unity3d.com/Manual/SL-ShaderCompileTargets.html) docs page has some related info.

Also note that :

- As mentioned above, some interpolators will be taken up when using nodes that require the data in the fragment stage (nodes under
**Input → Geometry**in Create Node menu) - Interpolators can be up to
`float4`

, and in the actual generated shader code it will try to pack multiple together to fit that (e.g. a Vector3 and Float, or two Vector2s), so counting the blocks won’t necessarily be accurate to the interpolator count used. It is better to check the`PackedVaryings`

struct in the[generated code](https://www.cyanilux.com#generated-shader-code).

Some uses of Custom Interpolators :

- Meshes tend to have less vertices than fragments produced, so doing calculations in the vertex shader can be much cheaper, (but may not look as accurate).
[Gouraud shading](https://en.wikipedia.org/wiki/Gouraud_shading)for example, is when lighting models (e.g. Phong) are calculated per-vertex but this can result in geometry being fairly obvious (especially when low-poly).

- Obtaining the interpolated vertex position (
**Position**node), or**Screen Position**, before vertex displacement (see below for examples) - To pass something based on
**Vertex ID**node to the fragment (e.g. see`SV_VertexID`

example on the[SL-ShaderSemantics docs page](https://docs.unity3d.com/Manual/SL-ShaderSemantics.html).

#### Custom Interpolators Example 1 - Undisplaced Position

When using the **Position** node in the **Fragment** stage, it will always have any vertex displacement applied (from calculation passed into the **Position** port on the **Vertex** stage). As an example, here we can use a **Custom Interpolator** block to pass the un-displaced position through.

In the fragment we can create the interpolator node (found under **Create Node → Custom Interpolator**)

Now compare our interpolator with the regular **Position** node in the **Fragment** stage (can use the **Main Preview** for this. Can right-click in that window to swap the mesh for a **Plane**). The **Y** axis of the interpolator produces a completely black result (as the vertex positions are at **Y=0**). But with the **Position** node version, we can see a gradient (specifically from **-1 to 1**, though the negative values also show as black here).

Of course, you’d only do this if the black result is what you required. I used this recently, [to colour an fried egg shader](https://twitter.com/Cyanilux/status/1546404927978741760). As the egg yolk has higher vertices and I *(somewhat lazily)* used a **Step** node (then into a **Lerp**) rather than applying a texture or vertex colors. But this required the undisplaced position otherwise other parts of the egg would appear yellow too as it displaces upwards.

#### Custom Interpolators Example 2 - Vertex Based Distortion

Perhaps you’d also use this if you are applying a texture by using a projection via **Position** node (usually known as worldspace planar mapping, somewhat of a precursor to triplanar mapping). If we want the texture to distort as the vertices move rather than stay static, then we need to handle the mapping with the position prior to the distortion. Here’s an example using **Gradient Noise** for displacement (on all XYZ axis) :

And then **Fragment**, comparing the result with the **Main Preview** (with **Plane** mesh) :

We could also do the same thing but with the **Screen Position** node instead for a screenspace mapping.

As mentioned previously, this is likely cheaper than a per-pixel approach to distortion (which is essentially the same calculation but all in the Fragment stage), but it definitely doesn’t look as accurate and would likely only fit in a old-PS1 style (or similar platforms around that time) or low-poly style (though this plane may need to be fairly high-poly still).

### Custom Functions

Shader Graph is a powerful tool, but the nodes can’t do everything. Some things might require *code snippets* to be used instead, which is where the **Custom Function** node would be used. For example for creating **loops**, **dynamic branching**, or complex math calculations (which may be possible through nodes, but can be easier/shorter in code form)

Back in Unity 2018.1, there was a method of creating custom nodes using the `CodeFunctionNode`

class in the `UnityEditor.ShaderGraph`

namespace. This method is **no longer accessible** and will error if you attempt to use CodeFunctionNode in Shader Graph/URP/HDRP versions for Unity 2019.1+. The replacement was the in-graph node.

The **Custom Function** node can be added to a graph, and then configured under the **Node Settings** tab of the **Graph Inspector** window, while the node is selected in the graph. (Prior to v10 the settings could be accessed by the small cog/gear icon on the node itself)

We can set the **Inputs** and **Outputs** for the function by using the “+” icon to add to the list. For each item, a dropdown is shown to change it’s data type. This affects the ports on the node.

There is two **Types** for the node :

**String**: We can write HLSL code directly in the**Body**field that appears. For example, with two inputs A and B :

|
|

The **Name** of the function isn’t too important if using the **String** mode but they must be unique or the function may override another.

**File**: We can use an external .hlsl (or .cginc) file and set the node to use it with the**Source**field that appears. The file should use a specific template as explained in the[shader graph docs](https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/Custom-Function-Node.html)and example below.

Typically the whole file contents are inside an `#ifndef KEYWORD`

`#define KEYWORD`

… `#endif`

block, which ensures the functions are only defined **once** - even if the file is included multiple times, which may occur if two **Custom Function** nodes reference the same HLSL File. The keyword used should be *unique* to that file. If two files have the same keyword, the contents of one won’t be included (likely causing an undefined error)

|
|

As shown above, the **Name** field must match the name of the function you want to use without the precision prefix (`MyFunction`

in this case). A file can contain multiple functions - the **Custom Function** node will only use the one with the name you set.

#### Calling ShaderLibrary Functions in a Custom Function

There may be cases where you need to access functions from the URP/HDRP ShaderLibrary in your code. Some common macros may be defined for pipelines. For example, sampling a texture :

|
|

But other more pipeline-specific macros/functions require special care. Previews within shader graph need to render in any render pipeline, so they use their own separate ShaderLibrary which won’t have access to URP/HDRP specific functions.

It’s typical to use the `SHADERGRAPH_PREVIEW`

keyword to output something different for previews, especially when they wouldn’t be useful anyway. For example this function from my [Custom Lighting Package](https://github.com/Cyanilux/URP_ShaderGraphCustomLighting), obtains Directional Light info in URP :

|
|

`GetMainLight()`

here is a function that exists only in the URP ShaderLibrary. That is fine for the final generated shader, but as explained above, previews do not have access to it. You might think of adding `#include`

lines for Lighting.hlsl or RealtimeLights.hlsl so the function can be used, but those files contain other includes such as URP’s [UnityInput.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/UnityInput.hlsl) which defines variables like `_Time`

. That already exists under the ShaderGraphLibrary used by previews, hence redefiniton errors are caused and the `SHADERGRAPH_PREVIEW`

block must be used instead.

#### Sampling Textures in a Custom Function

In shader code online you might typically see `sampler2D`

and `tex2D()`

functions being used. This is the older DX9 syntax, but with Shader Graph we mostly use the newer DX11+ syntax which has [separate objects for the texture and sampler](https://docs.unity3d.com/Manual/SL-SamplerStates.html). This isn’t supported in all platforms though (GLES2), so Unity provides a bunch of **macros** which can generate different code. These macros are defined in files found under [render-pipelines.core/ShaderLibrary/API](https://github.com/Unity-Technologies/Graphics/tree/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/API). The foldout below also lists some.

## Texture Sampling Macros

Common macros for sampling textures :

-
Sample : Can be used in Fragment stage only

`SAMPLE_TEXTURE2D(textureName, samplerName, coord2)`

`SAMPLE_TEXTURECUBE(textureName, samplerName, coord3)`

`SAMPLE_TEXTURE3D(textureName, samplerName, coord3)`

`SAMPLE_TEXTURE2D_ARRAY(textureName, samplerName, coord2, index)`

`SAMPLE_TEXTURECUBE_ARRAY(textureName, samplerName, coord3, index)`

- These macros would end up using
[tex.Sample(…)](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-sample)(on DX11+ type platforms)

-
Sample Level (of Detail) : Provides lod input to specify the mip map level sampled. Can be used in both Vertex & Fragment stages

`SAMPLE_TEXTURE2D_LOD(textureName, samplerName, coord2, lod)`

`SAMPLE_TEXTURECUBE_LOD(textureName, samplerName, coord3, lod)`

`SAMPLE_TEXTURE3D_LOD(textureName, samplerName, coord3, lod)`

`SAMPLE_TEXTURE2D_ARRAY_LOD(textureName, samplerName, coord2, index, lod)`

`SAMPLE_TEXTURECUBE_ARRAY_LOD(textureName, samplerName, coord3, index, lod)`

- These macros would end up using
[tex.SampleLevel(…)](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-samplelevel)(on DX11+ type platforms)

-
Sample Bias : Provides a bias to adjust the mip map level. Can be used in Fragment stage only.

`SAMPLE_TEXTURE2D_BIAS(textureName, samplerName, coord2, bias)`

`SAMPLE_TEXTURECUBE_BIAS(textureName, samplerName, coord3, bias)`

`SAMPLE_TEXTURE2D_ARRAY_BIAS(textureName, samplerName, coord2, index, bias)`

`SAMPLE_TEXTURECUBE_ARRAY_BIAS(textureName, samplerName, coord3, index, bias)`

- Doesn’t seem to be BIAS macros for Texture3D. May be able to use
[tex.SampleBias(…)](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-samplebias)function still (or[tex3Dbias](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-tex3dbias)for GLES2) ?

-
Sample Gradient : Provides inputs for partial derivatives. Can be used in both Vertex & Fragment stages. (Unless you use

`ddx()`

/`ddy()`

functions to calculate those derivatives - as those are Fragment only). These are useful when the UV coords used for sampling aren’t continuous, see[Pixellation along seams question above](https://www.cyanilux.com#sg-pixellated-seams).`SAMPLE_TEXTURE2D_GRAD(textureName, samplerName, coord2, dpdx, dpdy)`

`SAMPLE_TEXTURE2D_ARRAY_GRAD(textureName, samplerName, coord2, index, dpdx, dpdy)`

- Doesn’t seem there is GRAD macros for other texture types. May be able to use
[tex.SampleGrad(…)](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-samplegrad)function still (or[texCUBEgrad](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-texcubegrad)/[tex3Dgrad](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-tex3dgrad)for GLES2) ?


In Shader Graph v10.3+ the following structs were added, mirroring the HLSL types :

**UnityTexture2D****UnityTexture2DArray****UnityTexture3D****UnityTextureCube****UnitySamplerState**

These structs (defined in [pipelines.core/ShaderLibrary/Texture.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/Texture.hlsl)) wrap the HLSL texture objects (`Texture2D, Texture2DArray, Texture3D, TextureCube`

) and their associated samplers (`SamplerState`

) together, allowing them to both be passed into a **Custom Function** node in a single parameter.

Some examples :

|
|

Thanks to these types, it’s possible to access the **SamplerState** used by the texture through `.samplerstate`

(as shown above), as well as the **TexelSize** through `.texelSize`

(That one is UnityTexture2D only though). The actual texture object is accessed via `.tex`

but sampling macros can be used with new struct types too.

Custom Function nodes created prior to this change will set their inputs/outputs as the “Bare” types when updated. This allows the function to still work as it was originally intended, but switching them to “non-Bare” allows you to use the new samplerstate/texelsize access.

## Pre-v10 examples

In case you are still on older versions or using Bare types, the above functions would instead typically look like this. Where a **Sampler State** node would have to be used.

|
|

#### Arrays & Loops

While not a type exposed in Shader Graph, shaders also have array types and it is possible to define them in a **Custom Function**

Defining arrays can only be done with the **File** mode, as it needs to be outside the scope of the function itself. Arrays can also only be set from C# and won’t appear in the material inspector.

For example :

|
|

In the above example, a loop has been used to sum the values. Typically you’ll need a loop inside the function in order to handle the array (unless you just need a single value at a given index). Another example can be found in my [Forcefield Shader Breakdown](https://www.cyanilux.com/tutorials/forcefield-shader-breakdown/) that uses an array to produce ripples on the forcefield surface.

## What is `[unroll]`

?

`[unroll]`

is specified in the above code before the loop, which tells the compiler that we’ve written the loop more out of *convienience* and it shouldn’t actually be handled on the gpu as an actual loop. It would be equivalent to writing :

|
|

Generally unrolling is faster, though you might instead use an actual `[loop]`

if the body is expensive and exiting early may be more performant than the overhead of the loop itself. Perhaps when dealing with raymarching for example.

For more info see [this forum answer](https://discussions.unity.com/t/what-are-unroll-and-loop-when-to-use-them/881945/3).

It’s technically also possible to have other types of arrays, however Unity can only set **Vector** (float4) and **Float** arrays from a C# script.

I also recommend to **always set arrays globally**, using `Shader.SetGlobalVectorArray`

and/or `Shader.SetGlobalFloatArray`

rather than using the `material.SetVectorArray / SetFloatArray`

versions as that can lead to glitchy behaviour due to SRP Batching.

Note that arrays are limited to a maximum array size of **1023**. If you need larger you might need to try alternative solutions instead, e.g. Compute Buffers (StructuredBuffer), though that is more something you’d index rather than loop over.

#### Shader Pass Defines

In URP, Prior to v10 it was possible to use a **Predefined Boolean Keyword** to switch between using code for different shader passes as a define would be added in each pass. These defines are still available in v10+ but how they were defined was changed which broke the ability to use a Keyword. It is still possible to handle it through a **Custom Function** node however.

These defines for URP are :

`SHADERPASS_FORWARD`

`SHADERPASS_GBUFFER`

`SHADERPASS_DEPTHONLY`

`SHADERPASS_SHADOWCASTER`

`SHADERPASS_META`

`SHADERPASS_2D`

`SHADERPASS_UNLIT`

`SHADERPASS_SPRITELIT`

`SHADERPASS_SPRITENORMAL`

`SHADERPASS_SPRITEFORWARD`

`SHADERPASS_SPRITEUNLIT`

`SHADERPASS_DEPTHNORMALSONLY`


For HDRP a similar list can be found [here](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.high-definition/Runtime/RenderPipeline/ShaderPass/ShaderPass.cs.hlsl).

Shader Graph also uses `SHADERPASS_PREVIEW`

for it’s previews. Though you can also check for this using :

|
|

This can be important for some code that isn’t available in the preview stage.

To use one of the pass defines in v10+ to output different values for a specific pass, the following **Custom Function** could be used :

|
|

Here I’m using the **String** mode, but you could also use the **File** mode and the `#include`

could then be moved outside the function too. The `ShaderPass.hlsl`

file is only important for defining values to each of the `SHADERPASS`

defines I listed before. I find it a bit strange that Shader Graph isn’t generating the include for this file automatically (in URP v10.2.2 at least). It is using the defines from that file so really should be including it. I would assume this is a bug.

(Thanks to ElliotB who shared their findings on the changes to this in v10+ on the Unity discord & [forums](https://forum.unity.com/threads/shaderpass_shadowcaster-and-testing-for-the-shadowcaster-pass.1033108/)).

As for HDRP, they correctly include their `ShaderPass.cs.hlsl`

file. Note that their shadow pass is `SHADERPASS_SHADOWS`

instead.

While I’ve used the `SHADERPASS_SHADOWCASTER`

as an example, if you actually wanted to have an object cast shadows without rendering normally, or only remove shadows, you can easily do this by changing the **Cast Shadows** option on the **Mesh Renderer** component, to **Shadows Only** or **Off**. The function here is just an example. The 0 and 1 used as the output could be replaced with two inputs for more control over which values are used, and would allow them to be different per fragment/pixel (e.g. based on **Simple Noise** or the result of a **Sample Texture 2D**).

### Viewing/Editing Generated Shader Code

Behind the scenes, Shader Graph generates shader code specific to the render pipeline you’re working in (URP/HDRP). In v10+ it’s possible to view this code using the **View Generated Shader** button in Unity’s **Inspector** window when the **Shader Graph Asset** is selected in the **Project** window. Prior to v10 you could instead right-click the **Master** node to find this option.

This will generate the code into a temporary file, allowing you to view it.

If you plan to edit the code, you must first save the shader file somewhere in your **Assets** folder. It can then be treated similarly to any other code-written shader (but still requires the Shader Graph package to be installed to function). It is separate from the graph asset now though, so you’ll need to switch the shader on materials to use the code version. Changes to the code will also not update the graph, and vice versa.

Sometimes Shader Graph can be a bit limited, so it can be useful to edit the generated code to extend what it is possible in graph form. For example, adding [Stencil](https://docs.unity3d.com/Manual/SL-Stencil.html) operations. (It’s also possible to override this on the **RenderObjects** feature for the URP Forward Renderer. That is outside of the scope of this tutorial though, it’s long enough already!)

Be aware that the code might include multiple SubShaders depending on the targets under the Graph Settings. I’ve also seen URP ones convert to two SubShaders, one intended for gles platforms (& using shader model 2) and another for other platforms (using shader model 4.5). If you’re editing the code make sure you edit the one being used by your target (or both)

## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)