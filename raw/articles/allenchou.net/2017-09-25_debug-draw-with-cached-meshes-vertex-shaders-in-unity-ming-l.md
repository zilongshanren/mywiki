---
title: Debug Draw with Cached Meshes & Vertex Shaders in Unity | Ming-Lun "Allen"
  Chou | 周明倫
url: https://allenchou.net/2017/09/debug-draw-with-cached-meshes-vertex-shaders-in-unity/
author: Allen Chou
published: '2017-09-25'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

![](../../assets/7fc5683bf408e260.gif)


This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

Complete source code for the debug draw utility and Unity scene for generating the demo animation above can be found on [GitHub](https://github.com/TheAllenChou/unity-cj-lib). Here is a [shortcut](https://github.com/TheAllenChou/unity-cj-lib/blob/master/src/Assets/CjLib/DebugUtil.cs) to the debug draw utility class. And here is a [shortcut](https://github.com/TheAllenChou/unity-cj-lib/tree/master/src/Assets/CjLib/Shader) to the shaders.

### Motivation

I’ve recently started picking up [Unity](https://unity3d.com/), and quickly found out that the only easily accessible debug draw function is

, unless I was mistaken (in which case please do let me know).[Debug.DrawLine](https://docs.unity3d.com/ScriptReference/Debug.DrawLine.html)

So I thought it was a good opportunity to familiarize myself with Unity’s environment and a great exercise to implement a debug draw utility that draws various primitives, including rectangles, boxes, spheres, cylinders, and capsules. This post is essentially a quick documentation of what I have done and problems I’ve encountered.


### First Attempt with Line Drawing

As my first iteration, I took the naive approach and just wrote functions that internally make a bunch of calls to `Debug.DrawLine`

. You can see such first attempt [here](https://github.com/TheAllenChou/unity-cj-lib/blob/b65818af9a178f1e97fe2ca0f0cbd359024ccb28/src/Assets/CjLib/DebugUtil.cs) in the history.

The majority of the time spent was pretty much figuring out the right math, so nothing special. I guess the only thing worth pointing out is how I arranged the loops in the functions for spheres and capsules. My first instinct was to draw “from top to bottom”, looping from one pole to the other and constructing rings of line segments along the way, with special cases at the poles handled outside the loop. However, I didn’t like the idea of part of the math outside the loop, as it didn’t feel elegant enough (note: this is just my personal preference). So I came up with a different way of doing it, where I “assemble identical longitudinal pieces” around the central axis that connects the poles. In this case, there are no special cases outside the loop body.

### Second Attempt with Cached Meshes & Vertex Shaders

After my first attempt, I got curious as to how other people debug draw spheres in Unity, and I came across this [gist](https://gist.github.com/speps/3701541). This is when it occurred to me that I can get better performance by caching the mathematical results into meshes, and then simply draw the cached meshes, as well as offloading some of the work onto the GPU with vertex shaders.

There are a bunch of primitives in my debug draw utility, so I won’t enumerate every single one of them. I’ll just use the capsule as an example.

I didn’t want to create a new mesh for every single combination of height, radius, latitudinal segments, and longitudinal segments, because you can have so many different combinations of floats that it’s impractical. Instead, I used just the latitudinal and longitudinal segments to generate a key for each cached mesh, and modify the vertices in the vertex shader with height and radius as shader input.

private static Dictionary<int, Mesh> s_meshPool; private static Material s_material; private static MaterialPropertyBlock s_matProperties; public static void DrawCapsule(...) { if (latSegments <= 0 || longSegments <= 1) return; if (s_meshPool == null) s_meshPool = new Dictionary<int, Mesh>(); int meshKey = (latSegments << 16 ^ longSegments); Mesh mesh; if (!s_meshPool.TryGetValue(meshKey, out mesh)) { mesh = new Mesh(); // ... s_meshPool.Add(meshKey, mesh); } if (s_material == null) { s_material = new Material(Shader.Find("CjLib/CapsuleWireframe")); } if (s_matProperties == null) s_matProperties = new MaterialPropertyBlock(); s_matProperties.SetColor("_Color", color); s_matProperties.SetVector("_Dimensions", new Vector4(height, radius)); Graphics.DrawMesh(mesh, center, rotation, s_material, 0, null, 0, s_matProperties); }

And below is the vertex shader. I basically shift each cap towards the center, scale the vertices using the radius, and push them back out using the height. I used the `sign`

function to effectively branch on which side of the XZ plane the vertices are on, without actually introducing a code branch in the shader.

float4 _Dimensions; // (height, radius, *, *) v2f vert (appdata v) { v2f o; float ySign = sign(v.vertex.y); v.vertex.y -= ySign * 0.5f; v.vertex.xyz *= _Dimensions.y; v.vertex.y += ySign * 0.5f * _Dimensions.x; o.vertex = UnityObjectToClipPos(v.vertex); return o; }

However, I spent 2 hours past midnight just scratching my head, trying to figure out why some of my debug draw meshes pop around as I shift and rotate the camera. It was as if the positional pops are dependent on the camera position and orientation, which was quite bizarre. It finally occurred to me that I might not have been consistently getting vertex positions in object space in the vertex shader, and based on that assumption I found this [post](http://answers.unity3d.com/questions/819002/getting-the-local-vertex-positions-in-vertex-shade.html) that confirmed my suspicion.

Basically, Unity has draw call batching turned on by default, so it inconsistently passed in vertex positions to vertex shaders in either object space or world space. It’s actually stated in Unity’s documentation [here](https://docs.unity3d.com/Manual/SL-SubShaderTags.html) under the not-so-obvious `DisableBatching`

tag section, that vertex shaders operating in object space won’t work reliably if draw call batching is on.

Although the process of figuring out what went wrong was annoying, the fix was luckily quite simple: just disable draw call batching in the vertex shaders.

Tags { "DisableBatching" = "true" }

That’s it! I hope you find this post interesting. I will likely continue to document my ventures into the Unity world.