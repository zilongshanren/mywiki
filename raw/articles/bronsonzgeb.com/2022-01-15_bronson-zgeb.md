---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2022/01/15/drawing-with-sdfs-in-unity/
author: Bronson
published: '2022-01-15'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# Drawing with SDFs in Unity

![](../../assets/75ddb1c1b6e82eeb.png)

This post will explore 2D SDFs in Unity. We’ll learn what SDFs are and see one way to draw them in Unity.

## What are SDFs?

SDFs (or *signed distance functions*) are functions that describe primitive shapes. We use them to make shapes using pure math. Given a point, each function indicates whether that point lies within the shape, on its boundary or outside. It does so by returning a signed value, where the sign suggests if the point is inside the shape. In my experience, negative values are inside the shape, zero is the boundary, and positive values are outside. However, sometimes this convention is reversed. So, if you haven’t guessed it, they’re called signed distance functions because they return a signed value representing the distance from a given point to the shape’s boundary.

They’re similar to metaballs but more flexible. Metaballs are generally spherical and goopy, whereas SDFs can be many shapes and blend in multiple ways, goopy or otherwise.

## How do we draw SDFs?

There are several ways to approach the problem of drawing SDFs, so my final solution is less important than the theory behind it. If you want to use SDFs in your project, you may need to adapt the approach to your use case. Additionally, I made a WebGL demo of the application, which means we’re limited by what’s available in WebGL 1.0, which roughly translates to OpenGL ES 2 in terms of functionality.

We’ll use a custom shader on a fullscreen quad. Typically I would store the data in a compute buffer and bind that to a material on the quad, but unfortunately, compute buffers aren’t available to us. So instead, we’ll set a bunch of arrays on the material.

Using a fullscreen quad, we can go pixel-by-pixel through the final buffer displayed on the screen. We’ll check each pixel to determine if any of our SDFs contain it. This approach allows us to blend our SDFs as we go because every pixel is aware of every SDF.

We’ll draw the quad the lazy way by dropping it in front of the camera in the scene. Initially, I generated the quad procedurally and drew it with the `DrawProceduralNow`

method, but I decided to simplify everything while porting the project to WebGL. WebGL is more limited than the standard desktop platform, and frankly, I’m not certain where the limits are, so I chose to simplify everything aggressively until it worked.

## SDF Manager

Let’s get into `SdfManager.cs`

.

```
using UnityEngine;
public class SdfManager : MonoBehaviour
{
const int MaxShapes = 64;
int _numShapes;
[SerializeField] Material _materialPrototype;
Material _material;
[SerializeField, Range(0, MaxShapes)] int _numStartingShapes;
Vector4[] _sdfPositions;
float[] _sdfSizes;
Vector4[] _sdfDirections;
float[] _sdfStartTimes;
void OnEnable()
{
var meshRenderer = FindObjectOfType<MeshRenderer>();
_material = new Material(_materialPrototype);
_material.name = "Instance";
meshRenderer.material = _material;
_numShapes = _numStartingShapes;
_sdfPositions = new Vector4[MaxShapes];
_sdfSizes = new float[MaxShapes];
_sdfDirections = new Vector4[MaxShapes];
_sdfStartTimes = new float[MaxShapes];
for (int i = 0; i < MaxShapes; ++i)
{
_sdfStartTimes[i] = -1;
}
for (int i = 0; i < _numShapes; ++i)
{
Vector4 position = new Vector4(Random.Range(-1, 1), Random.Range(-1, 1), 0.0f, 1.0f);
_sdfPositions[i] = position;
_sdfSizes[i] = Random.Range(0.1f, 0.5f);
_sdfDirections[i] =
new Vector4(Random.Range(-1, 1), Random.Range(-1, 1) * Random.Range(2f, 5f), 0.0f, 0.0f);
_sdfStartTimes[i] = Time.time;
}
_material.SetVectorArray("_SdfPositions", _sdfPositions);
_material.SetFloatArray("_SdfSizes", _sdfSizes);
_material.SetFloatArray("_SdfStartTimes", _sdfStartTimes);
_material.SetVectorArray("_SdfDirections", _sdfDirections);
}
}
```


The code is straightforward. First, we create an instance of the material attached to the quad. There’s only a single `MeshRenderer`

in the scene in my prototype, so I fetch it with `FindObjectOfType`

. Then we create arrays to hold our SDF data and bind them to the material. I use statically-sized arrays everywhere to be compliant with WebGL 1.0. Every SDF has a position, a size, a start time and a direction. The positions range from `-1`

to `1`

, where `(-1, -1)`

corresponds to the bottom left of the quad and `(1, 1)`

is the top right. Then, we’ll use the start time and direction to animate the SDFs. We also use a start time of `-1`

to indicate when we haven’t initialized the SDF.

## SDF Shader

Next, we’ll explore the SDF shader. Let’s start with the simple vertex shader.

```
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2f
{
float4 vertex : SV_POSITION;
float2 uv : TEXCOORD0;
};
v2f vert(appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = (v.uv * 2.0f) - 1.0f;
return o;
}
```


We’re doing the usual vertex shader stuff here, moving the quad from object space to clip space. In addition to that, we remap the UV coordinates from the 0 to 1 range into the -1 to 1 range. This change moves (0,0) to the center of the quad and corresponds with the position range of our SDFs.

And finally, the fragment shader, where the magic happens.

```
fixed4 frag(v2f i) : COLOR
{
float2 p = i.uv;
float d = 10000000;
for (int c = 0; c < MAX_SHAPES; ++c)
{
if (_SdfStartTimes[c] == -1)
continue;
const float size = _SdfSizes[c];
const float3 position = _SdfPositions[c].xyz;
float startTime = _SdfStartTimes[c];
float2 direction = _SdfDirections[c].xy;
float aliveTime = (startTime - _Time[1]) / 20.0;
float2 movement = (aliveTime * direction * _EnableMovement);
float2 pos = (p - position) + movement;
pos.x = ((pos.x + 1.0) % 2) - 1.0;
pos.y = ((pos.y + 1.0) % 2) - 1.0;
d = smin(d, sdCircle(pos, size), 0.1);
}
d = smoothstep(0.02, 0.03, d);
d = saturate(1 - d);
return d * _Color;
}
```


Let’s walk through this. First, `float2 p = i.uv;`

is the position within the quad, which roughly corresponds to our position on the screen. In other words, we can use this as a pixel coordinate. Next is `float d = 10000000;`

where we set the current distance to a very high number. If you recall, in our SDF, a negative distance means we’re inside the shape. As a result, we initialize d to be high. Now, we loop over all the shapes, checking the current pixel against every SDF. If we forget about animating the SDFs and simplify the loop to the bare minimum, this is what we get:

```
for (int c = 0; c < MAX_SHAPES; ++c)
{
if (_SdfStartTimes[c] == -1)
continue;
const float size = _SdfSizes[c];
const float3 position = _SdfPositions[c].xyz;
float2 pos = (p - position);
d = smin(d, sdCircle(pos, size), 0.1);
}
```


This loop is surprisingly straightforward, but, you’re probably wondering about the functions `smin`

and `sdCircle`

.

The `smin`

function is a fancy blend function from Inigo Quilez’s website. It gives us a goopy blend between SDFs that’s reminiscent of metaballs. You could replace `smin`

with `min`

, `max`

or any other function that could take two values and return one. I recommend you experiment and see. By the way, if you aren’t familiar with Inigo Quilez, I recommend you look him up. He’s the creator of Shadertoy and an avid proponent of SDFs. I linked his website at the bottom of this article.

```
//source: https://iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm
float smin(float a, float b, float k)
{
float h = max(k - abs(a - b), 0.0) / k;
return min(a, b) - h * h * k * (1.0 / 4.0);
}
```


The `sdCircle` function is *the *SDF. That’s right, the thing I’ve been talking about for the past 1000 words is finally here. This function takes a position and a radius and returns a value indicating whether we’re inside the circle or not. Like the `smin` function, I pulled this one from Mr Quilez’s website as well. If circles aren’t interesting to you, dozens of other shapes are available. Feel free to replace `sdCircle` with any other SDF. Experiment and have fun!

```
//source: https://iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm
float sdCircle(float2 p, float r)
{
return length(p) - r;
}
```


Finally, we’re out of the loop. Once we’ve found the distance value of our current pixel, we can colour it in.

```
d = smoothstep(0.02, 0.03, d);
d = saturate(1 - d);
return d * _Color;
```


In this block, we smooth the distance value to soften the edges of our shapes. Then, remap the value between `0`

and `1`

, where `1`

is inside a shape. Multiply that by the chosen colour and return.

## Interactivity

The final version of this little application is interactive. You can create new SDFs at runtime, and they’ll animate across the screen like a lava lamp simulator. What’s more, you can even play it in the browser [here](https://bzgeb.github.io/SdfDraw/). I constrained myself to WebGL 1.0 to reach as many platforms as possible, but it still doesn’t work well on mobile or Safari. So, I recommend trying it on a desktop in Firefox or Chrome. To try it out, click and hold to create a new goop and watch it go. Also, hit spacebar to toggle the animation.

I want to cover how I added interactive elements, but this post is getting a little long already. So if you’re curious, I linked the Github project at the bottom of this post. I believe that an ambitious reader could expand on this idea to create a goopy character who moves across a goopy world. Additionally, I’ll post the entire `SdfManager.cs`

and `SdfShape.shader`

files here:

```
//SdfManager.cs
using UnityEngine;
public class SdfManager : MonoBehaviour
{
const int MaxShapes = 64;
int _numShapes;
[SerializeField] Material _materialPrototype;
Material _material;
[SerializeField] float _growSpeed = 100f;
[SerializeField, Range(0, MaxShapes)] int _numStartingShapes;
Vector4[] _sdfPositions;
float[] _sdfSizes;
Vector4[] _sdfDirections;
float[] _sdfStartTimes;
Camera _camera;
void OnEnable()
{
var meshRenderer = FindObjectOfType<MeshRenderer>();
_material = new Material(_materialPrototype);
_material.name = "Instance";
meshRenderer.material = _material;
_camera = FindObjectOfType<Camera>();
_numShapes = _numStartingShapes;
_sdfPositions = new Vector4[MaxShapes];
_sdfSizes = new float[MaxShapes];
_sdfDirections = new Vector4[MaxShapes];
_sdfStartTimes = new float[MaxShapes];
for (int i = 0; i < MaxShapes; ++i)
{
_sdfStartTimes[i] = -1;
}
for (int i = 0; i < _numShapes; ++i)
{
Vector4 position = new Vector4(Random.Range(-1, 1), Random.Range(-1, 1), 0.0f, 1.0f);
_sdfPositions[i] = position;
_sdfSizes[i] = Random.Range(0.1f, 0.5f);
_sdfDirections[i] =
new Vector4(Random.Range(-1, 1), Random.Range(-1, 1) * Random.Range(2f, 5f), 0.0f, 0.0f);
_sdfStartTimes[i] = Time.time;
}
_material.SetVectorArray("_SdfPositions", _sdfPositions);
_material.SetFloatArray("_SdfSizes", _sdfSizes);
_material.SetFloatArray("_SdfStartTimes", _sdfStartTimes);
_material.SetVectorArray("_SdfDirections", _sdfDirections);
}
void Update()
{
if (Input.GetMouseButtonDown(0))
{
if (Physics.Raycast(_camera.ScreenPointToRay(Input.mousePosition), out var hit))
{
var position = hit.textureCoord * 2.0f - Vector2.one;
AddCircle(position);
}
}
else if (Input.GetMouseButton(0))
{
int index = _numShapes - 1;
ResizeCircle(index, _sdfSizes[index] + (Time.deltaTime * _growSpeed));
}
if (Input.GetKeyDown(KeyCode.Space))
{
for (int i = 0; i < _numShapes; ++i)
{
_sdfStartTimes[i] = Time.time;
}
_material.SetFloatArray("_SdfStartTimes", _sdfStartTimes);
var isMovementEnabled = _material.GetFloat("_EnableMovement");
_material.SetFloat("_EnableMovement", 1 - isMovementEnabled);
}
}
void AddCircle(Vector3 position)
{
if (_numShapes < MaxShapes)
{
_sdfPositions[_numShapes] = position;
_sdfDirections[_numShapes] =
new Vector4(Random.Range(-1, 1), Random.Range(-1, 1) * Random.Range(2f, 5f), 0.0f, 0.0f);
_sdfSizes[_numShapes] = 0.01f;
_sdfStartTimes[_numShapes] = Time.time;
++_numShapes;
_material.SetVectorArray("_SdfPositions", _sdfPositions);
_material.SetFloatArray("_SdfSizes", _sdfSizes);
_material.SetFloatArray("_SdfStartTimes", _sdfStartTimes);
_material.SetVectorArray("_SdfDirections", _sdfDirections);
}
}
void ResizeCircle(int index, float size)
{
_sdfSizes[index] = size;
_sdfStartTimes[index] = Time.time;
_material.SetFloatArray("_SdfSizes", _sdfSizes);
_material.SetFloatArray("_SdfStartTimes", _sdfStartTimes);
}
}
```


```
//SdfShape.shader
Shader "SdfShape"
{
Properties
{
_Color ("Color", Color) = (0.8,0.2,0.2,1)
[Toggle] _EnableMovement("Enable movement", float) = 0
}
SubShader
{
Tags
{
"RenderType"="Transparent"
}
Pass
{
Blend SrcAlpha OneMinusSrcAlpha
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
//source: https://iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm
float smin(float a, float b, float k)
{
float h = max(k - abs(a - b), 0.0) / k;
return min(a, b) - h * h * k * (1.0 / 4.0);
}
//source: https://iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm
float sdCircle(float2 p, float r)
{
return length(p) - r;
}
#define MAX_SHAPES 64
fixed4 _Color;
float _EnableMovement;
float _SdfSizes[MAX_SHAPES];
float _SdfStartTimes[MAX_SHAPES];
float4 _SdfPositions[MAX_SHAPES];
float4 _SdfDirections[MAX_SHAPES];
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2f
{
float4 vertex : SV_POSITION;
float2 uv : TEXCOORD0;
};
v2f vert(appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = (v.uv * 2.0f) - 1.0f;
return o;
}
fixed4 frag(v2f i) : COLOR
{
float2 p = i.uv;
float d = 10000000;
for (int c = 0; c < MAX_SHAPES; ++c)
{
if (_SdfStartTimes[c] == -1)
continue;
const float size = _SdfSizes[c];
const float3 position = _SdfPositions[c].xyz;
float startTime = _SdfStartTimes[c];
float2 direction = _SdfDirections[c].xy;
float aliveTime = (startTime - _Time[1]) / 20.0;
float2 movement = (aliveTime * direction * _EnableMovement);
float2 pos = (p - position) + movement;
pos.x = ((pos.x + 1.0) % 2) - 1.0;
pos.y = ((pos.y + 1.0) % 2) - 1.0;
d = smin(d, sdCircle(pos, size), 0.1);
}
d = smoothstep(0.02, 0.03, d);
d = saturate(1 - d);
return d * _Color;
}
ENDCG
}
}
}
```


**Check out the project ****on GitHub**** or play it in your browser ****here****. Learn more about SDFs from ****Inigo Quilez’s website****. If you’d like to support my work, join**** my mailing list****. If you do, I’ll notify you whenever I write a new post.**