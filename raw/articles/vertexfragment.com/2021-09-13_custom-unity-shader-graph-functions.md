---
title: Custom Unity Shader Graph Functions
url: https://www.vertexfragment.com/ramblings/unity-custom-shader-graph/
author: Steven Sell
published: '2021-09-13'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

The Unity Shader Graph is a powerful tool that provides the ability to design custom shaders and effects without having to write any code. It comes with a well-rounded suite of existing nodes and utilities, however there are still times when the packaged nodes are not quite up to the challenge and a custom node is needed to either make life easier or even just possible.

One common effect that is surprisingly difficult to implement using the stock nodes is a radial reveal on a GUI element. This is seen in almost any game that uses the concept of skill cooldown. By using a custom node we can achieve the cooldown effect very easily, but it can take a bit of digging to figure out just how to create one.

In this ramble we will use a custom Shader Graph node to implement a cooldown effect as shown below.

![](../../assets/814010142bfd1d71.gif)


Shader Graph allows for the definition of nodes which have their implementations in a CG (`.cginc`

) or HLSL (`.hlsl`

) file within your project. For our effect we will be using CG.

To begin, create the file that will house the implementation. For example:

`Assets/Resources/Shaders/ShaderGraph/CustomFunctions.cginc`


And start the file with a standard inclusion guard:

```
#ifndef VF_CUSTOM_SHADERGRAPH_FUNCTIONS
#define VF_CUSTOM_SHADERGRAPH_FUNCTIONS
// ...
#endif
```


Our function will have the following input:

- UV Coordinates
- Cooldown Progress
- Source Color
- Tint Modifier Color

And output the adjusted color. The function signature will be:

```
void TintBasedOnClockProgress_float(
float2 uv,
float progress,
float3 sourceColor,
float3 tintModifier,
out float3 color)
{
// ...
```


Note that there is no return value, and instead Shader Graph expects output to be provided via an `out`

parameter. It is also required that the function name end with `_float`

, though when we specify our custom function later within Shader Graph it will be excluded.

First we need to define `PI`

and `ONE_OVER_PI`

,

```
#ifndef PI
#define PI 3.141592f
#endif
#ifndef ONE_OVER_PI
#define ONE_OVER_PI 0.318309f
#endif
```


The tint function itself is fairly simple: calculate the “clock angle” of the current fragment UV, and if the angle is less than our current remaining progress value then the fragment is tinted.

```
void TintBasedOnClockProgress_float(
float2 uv,
float progress,
float3 sourceColor,
float3 tintModifier,
out float3 color)
{
float angle;
CalculateClockAngle_float(uv, angle);
color = (angle > progress) ? sourceColor : sourceColor * tintModifier;
}
```


So as the time remaining decreases (as a normalized float on the range `[0.0, 1.0]`

), the less the image is tinted with it being “revealed” in a clockwise rotation.

Next we have to actually calculate the clock angle, which we do in `CalculateClockAngle_float`

. For utility purposes, we write the function signature so that our clock angle function can be used in an independent node in the future.

```
void CalculateClockAngle_float(float2 uv, out float frac)
{
float2 a = float2(0.0, 1.0);
float2 b = normalize(uv - float2(0.5, 0.5));
float dot = (a.x * b.x) + (a.y * b.y);
float det = (a.x * b.y) - (a.y * b.x);
float angle = atan2(-det, -dot);
frac = ((angle + PI) * 0.5f) * ONE_OVER_PI;
}
```


With our function in place we are now ready to use it from within Shader Graph.

Lets start with creating a new Shader Graph:

```
Assets → Create → Shader → Universal Render Pipeline → Unlit Shader Graph
```


Within your new graph,

```
Right-click → Create Node → Utility → Custom Function
```


When you select your new node, the Graph Inspector / Node Settings dialog will display the following:

![](../../assets/b80ef71809a106d2.png)


We can configure this node to use the Clockwise Tint function that we made earlier. All we have to do is set the expected input, output, and where our function exists. For this we have the following inputs:

| Graph Input Name | Graph Input Type | CG Input Name | CG Input Type |
|---|---|---|---|
| UV | `Vector 2` |
uv | `float2` |
| Progress | `Float` |
progress | `float` |
| SourceColor | `Vector 4` |
sourceColor | `float3` |
| TintModifier | `Vector 4` |
tintModifier | `float3` |

And then our output:

| Graph Output Name | Graph Output Type | CG Output Name | CG Output Type |
|---|---|---|---|
| TintedColor | `Vector4` |
color | `out float3` |

Finally we point to where our code lives:

**Type:**File**Name:**TintBasedOnClockProgress**Source:**CustomFunctions

All set up, it should look like this:

![](../../assets/bc859badccf09e22.png)


With our node created, we can now make use of it in our graph.

The demo graph below simply provides the required input to our node and then outputs it to the fragment.

![](../../assets/26acd1b0098634bc.png)


By default we have the tint modifier set to `(0.2, 0.2, 0.2, 1.0)`

and the progress as `0.6`

. The next step would be to create a material using our new shader. Once that is done we can setup a simple script to update the progress of our cooldown to see the final effect. This will target an Unity UI `RawImage`

.

```
using UnityEngine;
using UnityEngine.UI;
namespace VertexFragment
{
/// <summary>
/// Demonstrates setting the "progress" of the CooldownDemo material.
/// </summary>
public sealed class CooldownDemo : MonoBehaviour
{
/// <summary>
/// The raw image with our CooldownDemo material applied.
/// </summary>
public RawImage TargetImage;
/// <summary>
/// The duration of the cooldown effect.
/// </summary>
public float Duration = 2.0f;
/// <summary>
/// How long is remaining in the current cooldown cycle.
/// </summary>
private float CooldownRemaining = 0.0f;
private void Update()
{
if (TargetImage?.material == null)
{
return;
}
float progress = Mathf.Clamp01(CooldownRemaining / Duration);
TargetImage.material.SetFloat("Progress", progress);
CooldownRemaining -= Time.deltaTime;
CooldownRemaining = (CooldownRemaining < 0.0f ? Duration : CooldownRemaining);
}
}
}
```


With our final result:

![](../../assets/814010142bfd1d71.gif)


[Unity Shader Graph Manual](https://docs.unity3d.com/Packages/com.unity.shadergraph@12.0/)- Icon is from
*4000 Fantasy Icons*