---
title: 'ShaderQuest Part 4: Shader Environment Architecture'
url: https://halisavakis.com/shaderquest-part-4-shader-environment-architecture/
published: '2021-03-06'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

The 4th part of ShaderQuest post is brought to you by these awesome Patrons:

- Not Invader Zim
- Tiph’ (DN)
- orels1
- raingame

## Introduction

I know you’re probably eager to get into the nitty gritty of shader creation, but once again I’m about to disappoint you. This is the last introductory ShaderQuest post that doesn’t go through actual shader making. I promise you that starting with the next post we’ll start seeing some shader magic happening, but first I wanted to give some more context and terminology around the way shaders are built in different environments.

One of the most intimidating things for me when I started with shaders was opening up a newly created shader file and see all the different syntaxes, tags, capitalized terms etc. Node-based shader authoring tools probably aren’t as intimidating, but you still might not know exactly what you’re looking at when you’re using them.

The purpose of this ShaderQuest part is to familiarize you with the architecture of coded shaders in Unity as well as with the visual shader creation environments found in both Unity and UE4.

Let’s get started!

## Unity

Not sure if I mentioned that in previous ShaderQuest parts, but the system Unity uses for hand-coded shaders is called **ShaderLab** (even though you can’t really see that name inside Unity). Therefore, when I’m talking about coded shaders in Unity, instead of flipping back and forth with terms like “hand-coded shaders”, “hand-written shaders”, “coded shaders” etc, I’ll just be using “**ShaderLab shaders**“. Cool? Cool.

### ShaderLab

As mentioned in the [previous ShaderQuest](https://halisavakis.com/shaderquest-part-3-shaders-and-materials/), we’ll mostly be dealing with two types of shaders: **Vertex/Fragment shaders** and **Surface shaders** (we mentioned **image effect shaders** too, but they’re essentially the same as vertex/fragment shaders). They both use the ShaderLab system and have a lot of similarities in their architecture, but there are some key differences as well.

#### Vert/Frag Shaders

Let’s start with Vertex/Fragment shaders, as they’re the most explicit. By the way, keep in mind that I might be referring to Vertex/Fragment shaders as **Vert/Frag** **shaders** as well, for brevity. Here’s what you see when you open up that newly created Vert/Frag shader file:

```
Shader "Unlit/NewUnlitShader"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
}
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
// make fog work
#pragma multi_compile_fog
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2f
{
float2 uv : TEXCOORD0;
UNITY_FOG_COORDS(1)
float4 vertex : SV_POSITION;
};
sampler2D _MainTex;
float4 _MainTex_ST;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = TRANSFORM_TEX(v.uv, _MainTex);
UNITY_TRANSFER_FOG(o,o.vertex);
return o;
}
fixed4 frag (v2f i) : SV_Target
{
// sample the texture
fixed4 col = tex2D(_MainTex, i.uv);
// apply fog
UNITY_APPLY_FOG(i.fogCoord, col);
return col;
}
ENDCG
}
}
}
```

Let’s start by identifying the main blocks of this shader file:

![](../../assets/4f001345d342c763.png)

Ok that looks like a lot, but we’ll go step by step, from the outmost top block to the inmost bottom block.

##### ShaderLab Shader

This is the main block that makes up a Unity ShaderLab shader. In most cases it contains a **Properties block** and one or more **SubShaders**. In our examples though, we won’t be using more than one SubShader.

This whole Shader block is initialized by this line of code:

```
Shader "Unlit/NewUnlitShader"
```

“Shader” is the keyword that lets Unity know that this is, well, a shader, and the string following it is the path by which the shader can be found when choosing a shader for a material. If you remember from the [previous ShaderQuest](https://halisavakis.com/shaderquest-part-3-shaders-and-materials/), I mentioned that built-in unlit (or vert/frag) shaders can be found in the “Unlit” category when choosing a shader from the dropdown menu at the top of the material inspector. This is defined by this first line of the shader.

**The name of the shader is arbitrary and doesn’t have to match the name of the shader file.**

Same goes for the category it’s under. You can create a custom category for your shaders, by saying, for example:

```
Shader "MyFancyShaders/MyFancyShadersFancyName"
```

But wait; we can go deeper! You can create subcategories in your categories for better organization, so, if you really hate your artists, you can even say something like:

```
Shader "Unlit/Very Unlit/The Most Unlit/NewUnlitShader"
```

That will make users go through this menu to select your shader:

![](../../assets/206e8265c4ccb19e.gif)

**NOTE:** Since this is gamedev, there is a hardcoded exception with the categories that you should keep in mind: If your top-level category is set to “Hidden”, it won’t appear in the Shader dropdown menu. This is usually used for image effects or shaders that aren’t meant to be directly assigned to materials but are instead used to create materials dynamically via code.

##### Properties block

Unity’s editor can’t really know by reading your shader which properties to expose to the material inspector, so we have to be explicit about that. **In the properties block we declare what properties we want to use in the shader that are also exposed in the material inspector**. The syntax for the properties is **unique** for the material block (because why not?) and it follows this convention:

```
[REFERENCE] (["DISPLAY_NAME"], [TYPE]) = [DEFAULT_VALUE]
```

**Reference**: The reference for this property that will be used later in the main body of our shader.**Display name**: The name of the property that will be displayed in the material inspector.**Type**: The type of the property.**Default value**: The default value that the property will have, if left unassigned/unmodified.

In our unlit shader example we have just the one property:

![](../../assets/719707451df3ab20.png)

**Do notice the lack of semicolons at the end of the lines.**

In general, the most common types we will see in a shader are:

**2D Textures**- Their type is
**2D** - They can be initialized with a texture that has a solid color with this syntax: “[COLOR]” {}
- The colors available for 2D initialization are:
- white -> “white” {}
- black -> “black” {}
- bump (used for neutral normal maps) -> “bump” {}
- gray/grey -> “gray” {} / “grey” {}
- red -> “red” {}

- Example: _Texture (“My Texture”, 2D) = “black” {}
**TIP:**If you want to have a property for a normal map, besides setting its default value to “bump” you can also add**[Normal]**before the property declaration. That way, if you assign a texture to this property that hasn’t been imported as a normal map, Unity will show a message notifying you of this and will add a button on the inspector that fixes that on the spot:

- Their type is

![](../../assets/8633f7a2a2417fb3.png)

**Floats**- Their type is
**float** - They can be initialized with a single value
- If you want the float property to be serialized as a slider you can use
**Range([X],[Y])**as the type, where X and Y are the minimum and maximum value the property can take respectively. - Float example: _FloatValue (“My Float”, float) = 0
- Range example: _RangeValue (“My Range”, Range(0.0, 1.0)) = 0.5

- Their type is
**Colors**- Their type is
**Color** - They can be initialized with a 4-dimensional vector that represents the value of the color for each one of its four channels (red, green, blue and alpha). More on how colors work in shaders in a future ShaderQuest post.
- This property will expose a color picker in the material inspector.
- Example: _Color (“My Color”, Color) = (1,1,1,1)
**TIP**: If you want an HDR color picker exposed (for emission effects for example) you can add**[HDR]**before the property declaration like so: [HDR] _HDRColor (“My HDR Color”, Color) = (1,1,1,1)

- Their type is
**Vectors**- Their type is
**Vector** - They can be initialized exactly like colors, using a 4-dimensional vector.
- Example: _Vector (“My Vector”, Vector) = (1,1,1,1)

- Their type is

Here’s what a properties block with a bunch of different properties can look like:

![](../../assets/5b4e681366d6dfb8.png)

The inspector for a material with this shader will look like this:

![](../../assets/104867598bbce111.png)

##### SubShader

As mentioned, a ShaderLab shader can have one ore multiple subshaders. When running the game, Unity will pick the first subshader that can run on the user’s GPU. The actual shader stuff are stored in the subshader.

More information on subshaders can be found in [Unity’s official manual](https://docs.unity3d.com/Manual/SL-SubShader.html).

##### SubShader tags

In our example there are some weirdly written tags and directives in the block I’ve marked as “SubShader tags”. These are some information relative to our shader that Unity needs to know. There are some specific tags that we can use outside the pass block, but there are some other tags that we can use in each pass block, which convey different information, mainly related to lighting.

You can read more about subshader tags and pass tags in Unity’s official manual: [subshader tags](https://docs.unity3d.com/Manual/SL-SubShaderTags.html), [pass tags](https://docs.unity3d.com/Manual/SL-PassTags.html).

There is a bunch of different information we can convey to Unity with these tags, including information about which faces to cull, if our shader is opaque or transparent, its rendering queue etc. In our example we have

```
Tags { "RenderType"="Opaque" }
```

which lets Unity know that the objects that have materials that use this shader will be rendered as opaque.

Below that, the

```
LOD 100
```

assigns a LOD (**Level Of Detail**) value to the shader, so that Unity can adjust what shaders its using dynamically as a way to increase quality or performance. More on that in [Unity’s official manual](https://docs.unity3d.com/Manual/SL-ShaderLOD.html).

Any other tags we can add in this section will be examined in future ShaderQuest posts.

##### Pass

A subshader consists of multiple passes, each of which causes the geometry of a game object to be rendered once. Since rendering an object is an expensive operation, we usually want to use as few passes as possible (ideally just one), and in most of our shaders we won’t be using more than one passes. There are cases, however, were one might need to use multiple passes, either for specific effects (like inverted hull outlines) or for effects that involve lighting and shadow casting.

Some more information on shader passes and the set-up commands than can be used in passes can be found in, you guessed it, [Unity’s official manual](https://docs.unity3d.com/Manual/SL-Pass.html).

##### CGPROGRAM block

This is the block that holds our **actual** shader code. Anything in this block is actual CG code and there’s no more of that injected, weirdly-syntaxed code that communicates directly with Unity.

If our shader was written in HLSL this block would instead start with

```
HLSLPROGRAM
```

and it would end with

```
ENDHLSL
```

Similarly, if you want, you could write Unity shaders in GLSL, in which case your block would start with GLSLPROGRAM and end with ENDGLSL, though there’s not a whole lot of documentation on GLSL shaders in Unity, so for the built-in pipeline we’re sticking to CG.

It’s important to note that any hand-written shaders in URP and HDRP are using HLSL.

##### Pragmas & includes

Much like in a C# script or in a C/C++ program, at the start of our shader program we have some preprocessor commands that are actually pretty important to our shader.

One of the things that confused me the most when I first opened up a shader file was how Unity knew that the “frag” method corresponded to the fragment shader and the “vert” method corresponded to the vertex shader.

You, however, are probably more observant than me and you probably noticed these two commands in this block:

```
#pragma vertex vert
#pragma fragment frag
```

This is where Unity matches the methods to their actual functionality. That being said, the method for the fragment shader doesn’t really need to be called “frag”, neither does the vertex shader method have to be called “vert”. **You can name these methods however you want, but you’ll have to make sure the corresponding pragmas match.**

Below these pragmas you can find an #include command that includes the built-in “UnityCG.cginc” file that’s full of helpful macros and methods. You can check out some of the included methods in [Unity’s official manual](https://docs.unity3d.com/Manual/SL-BuiltinFunctions.html), however I also highly suggest downloading Unity’s built-in shaders from the [Unity download archive](https://unity3d.com/get-unity/download/archive) to access the UnityCG.cginc yourself, along with other built-in shaders.

##### Data structs

This is where the structs we’re using in our shader are declared and defined.

The first struct is the struct that defines the objects that serve as inputs to our vertex shader. This is where we get access to all the cool data from 3D models that we mentioned in the [first ShaderQuest part](https://halisavakis.com/shaderquest-part-1-graphics-concepts/), including object-space vertex position, UV coordinates, vertex colors etc.

Here’s where you might notice some more weird syntax; specifically a colon after each struct member, followed by a capitalized term.

**The members of the struct are defined almost arbitrarily, but if we want to assign specific data to them we have to use specific keywords.**

For example, the member of the “appdata” struct

```
float4 vertex : POSITION
```

adds a 4-dimensional vector to the struct that’s called “vertex” to which the object-space position of a vertex is stored. The member could be called anything we want, but because we’re adding ” : POSITION” at the end, it means that the object-space position of the vertex will be stored in it regardless of the name.

Similarly, the member

```
float2 uv : TEXCOORD0
```

stores the UVs on the first UV channel of the mesh. Just in case you don’t know, 3D modelling applications give you the option to store more sets of UV coordinates. The second set of UVs would then be stored to TEXCOORD1, the third one to TEXCOORD2 and so on.

Bellow the “appdata” struct we have the “v2f” struct. “v2f” stands for “vertex to fragment” and it’s an **interpolator struct** used to pass data down from the vertex shader to the fragment shader.

Because this shader samples a texture to determine the final color, it needs the UVs to be passed down to the fragment shader, so we find another “float2 uv” member in there that’s written exactly like the on in the appdata struct. The interpolator structs use the TEXCOORD data streams to move information around, so if we wanted to move more data from the vertex to the fragment shader we’d just use TEXCOORD1, TEXCOORD2 and so on.

Something that stands out in the “v2f” struct is the

```
UNITY_FOG_COORDS(1)
```

line, which is just a Unity macro to get some fog-related data, as well as the use of “SV_POSITION” instead of “POSITION”, which is attributed to a compatibility workaround for some platforms.

##### Property declarations

Here are the property declarations for any properties that we’re going to be using in our shaders. In this case, we only have a **sampler2D** called “_MainTex” and a **float4** (a 4-dimensional vector) called “_MainTex_ST”. Ignoring the second one for the time being, you might be wondering:

**Why do we declare _MainTex again in there? Isn’t it already declared in the properties block?**

Well, no. In the properties block we just created a field for Unity’s material inspector to display, and we assigned the “_MainTex” reference ID to it. That means, that **if in the actual shader there’s a property with the exact**

**same name as the property reference ID, the values assigned to the property in the material inspector will be reflected on the shader property.**So, basically, in order to pair our material inspector properties with our shader properties, we just need to use the same name-reference ID.

##### Vertex shader

Next up is the “vert” method which, as we already mentioned, operates as our vertex shader. Won’t go into details about what it’s doing, but do notice that the method takes an **appdata** object as an input and returns a **v2f** object, after it operates on the individual members of the **v2f** object.

Again, keep in mind that it’s basically taking the mesh data, it’s doing some modifications on them and then passes the new data over to the fragment shader.

##### Fragment shader

Finally, we have what usually serves as the star of the show, the method that operates as our fragment shader. Here you can see that the input is a **v2f** object and that the method actually returns a **fixed4** (a 4-dimensional vector with lower precision). That’s basically the color of the pixel the fragment shader is outputting! Each component of the vector corresponds to the value of the color in each channel (Red, Green, Blue and Alpha respectively). It’s cool to keep that in mind because, at the end of the day, shaders are usually responsible for outputting a color on our screen, and even if the whole process for that seems a bit convoluted with all the data streams and weird syntaxes, we still end up with just color.

**NOTE: **As you can probably imagine, the blocks inside the CGPROGRAM block and under the pragmas/includes can be placed in a somewhat arbitrary order; as long as there is some top-down sequential logic, meaning that you can’t, for example, define “v2f” under the vert method, since it’s being referenced in the method. Same goes for property declarations as well.

#### Surface Shaders

Surface shaders offer a very useful layer of abstraction but they’re shaped in a very similar way to vert/frag shaders.

Surface shaders work by offering an interface to modify a set of data before they’re sent to a background process for lighting and shading. By default, they’re using the same PBR lighting as Unity’s standard shader. Therefore, materials using a surface shader like the default one, will react to all lighting as if they were using the Standard shader.

We’ll take a look at surface shaders later as well, but if you’re eager to find out more about them, you can take a look at [this tutorial](https://halisavakis.com/my-take-on-shaders-whats-the-deal-with-surface-shaders/).

Let’s take a look at how a surface shader looks:

```
Shader "Custom/NewSurfaceShader"
{
Properties
{
_Color ("Color", Color) = (1,1,1,1)
_MainTex ("Albedo (RGB)", 2D) = "white" {}
_Glossiness ("Smoothness", Range(0,1)) = 0.5
_Metallic ("Metallic", Range(0,1)) = 0.0
}
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 200
CGPROGRAM
// Physically based Standard lighting model, and enable shadows on all light types
#pragma surface surf Standard fullforwardshadows
// Use shader model 3.0 target, to get nicer looking lighting
#pragma target 3.0
sampler2D _MainTex;
struct Input
{
float2 uv_MainTex;
};
half _Glossiness;
half _Metallic;
fixed4 _Color;
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputStandard o)
{
// Albedo comes from a texture tinted by color
fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;
o.Albedo = c.rgb;
// Metallic and smoothness come from slider variables
o.Metallic = _Metallic;
o.Smoothness = _Glossiness;
o.Alpha = c.a;
}
ENDCG
}
FallBack "Diffuse"
}
```

You might be seeing a very similar structure to vert/frag shaders already. Let’s break this down to blocks as well:

![](../../assets/c59dab5be890390c.png)

The core blocks are pretty much the same, even if what’s inside them might be a bit different. You might notice that some blocks are missing, like the pass block or the vertex shader block. Surface shaders abstract a lot of shader ugliness and perform most of the tedious work behind the scenes automagically.

Two different blocks you might have notices are the “Instancing info” block and the “Surf method” block.

##### Instancing info

This blocks handles per-instance data if we are using GPU instancing on our materials. We probably won’t be using this block a lot.

##### Surf method

You can kind of think this method as your fragment shader; here’s where you can modify the data that’s being sent to the lighting function. Again, not going into any details on how this all works, I’ll just link [my surface shader tutorial again](https://halisavakis.com/my-take-on-shaders-whats-the-deal-with-surface-shaders/).

### Shader Graph (SG)

In URP and HDRP, shader creation involves the use of Shader Graph. You can create shaders starting from different presets (lit, unlit, sprite lit etc) but the overall setup is the same:

![](../../assets/8a52284986534d39.png)

![](../../assets/db8e59102568e6ec.png)

There’s far fewer things to go through here, that mostly involve the UI:

![](../../assets/26a25133e0c88567.png)

#### Blackboard

This is similar to the “Properties” block in hand-written shaders; it holds all the properties that are exposed to the material inspector and that are used in our shader. Hitting the top right “+” button will give you a list of different properties to create, like floats, vectors, textures etc.

Here’s what a populated Blackboard can look like:

![](../../assets/4e008d08e3cdc182.png)

The green dot next to each property lets us know that this property is exposed to the material inspector.

#### Graph Inspector

This window holds details both for the entire graph and for individual nodes and properties.

On the “Graph Settings” tab you can see information about our graph, like what sort of workflow it uses, if the shader is opaque or transparent etc.

![](../../assets/b5431c5be87c5ca7.png)

Switching to the “Node Settings” tab gives us a context-aware inspector of the selected node. If we select the “Albedo” property, for example, we get this view:

![](../../assets/1ecb07ec444b8d8b.png)

From here we can tweak information about our property, like its default texture, its name, or its reference ID.

#### Master stack

The master stack holds the outputs of our shader, split into information related to the vertex shader (like vertex position and normal vector) and information related to the fragment shader (like color and smoothness).

![](../../assets/76d7a5709d97859d.png)

You can add or remove nodes from the stack, based on your shader’s needs.

#### Main preview

This just gives you a preview of what a material with this shader will look like. There’s nothing fancy about it reallly.

![](../../assets/206c9c35a12d67ed.png)

### Amplify Shader Editor (ASE)

Node-based shader authoring systems are pretty similar in their architecture, and ASE is no exception:

![](../../assets/4d9659e98f16652f.png)

The main elements of the ASE environment of which you need to be aware initially are:

- Inspector: Similar to SG graph inspector – it displays contextual information about the selected node. If no node is selected, the inspector displays information about the shader.
- Output node: Similar to SG’s master stack; it contains all the outputs of the shader, like the color and smoothness.
- Compile shader button: The button you need to press to apply your changes to the shader and all the materials that use that shader.

## UE4

There’s not a whole lot to say about the environment of the UE4 material editor either. It’s quite similar to that of SG and ASE:

![](../../assets/3183564b4624f799.png)

### Details

The “Details” tab works like the inspector of the two previous visual shader creation environments; it displays the information and properties of the selected node or, if no node is selected, it displays data about the whole shader (its type, blending etc).

### Output node

The master node that contains all the outputs of the material, very much like the output node of ASE or the master stack of SG. You can even notice very similar outputs between the three systems (like Base Color/Albedo, Smoothness/Roughness, Metallic etc).

### Palette

This is a pretty useful tab that contains a library of all the available nodes you can add to your material. It’s not really necessary as you can search all these nodes by right-clicking on the graph, but it’s nice to have.

### Material preview

A live preview of the material which should give you a good idea of how your material will end up looking.

## Conclusion

Oof this was a big one. It’s obvious that much more attention was given to ShaderLab shaders since visual shader creation environments were created with the users in mind. I strongly feel, however, that it’s more important to get what’s happening in coded shaders since, after all, whether it’s SG or ASE, the end result will end up looking very much like a ShaderLab shader. And even if we won’t be examining a similar hand-coded shader system in UE4, know that under the hood things look very similar, especially in terms of what goes into your vertex/fragment shaders.

Familiarizing yourself with the shader creation environment you’ll be using, whether that’s code or a graph, is certainly valuable to start creating your own shaders.

Which, by the way, is what we’ll finally start doing with the next ShaderQuest part!

See you in the [next part of ShaderQuest](https://halisavakis.com/shaderquest-part-5-shader-code-syntax-colors/)❗