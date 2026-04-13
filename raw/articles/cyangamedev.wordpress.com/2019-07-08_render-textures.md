---
title: Render Textures
url: https://cyangamedev.wordpress.com/2019/07/08/render-textures/
author: Cyan
published: '2019-07-08'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Render Textures** are special textures which are updated at runtime. The **Camera** component has a **Target Texture** variable, which can be set to a Render Texture object to output the camera’s view to the texture rather than the screen. To create this object we can right-click somewhere in the Assets folder on the Project window, and select **Create** **→** **Render Texture**.

We can then click on the texture and look in the Inspector window to change its Size, Color Format, enable/disable Mip Maps, etc. Be aware that these options will affect how much memory the Render Texture requires, which is displayed on the Inspector at the bottom on the texture preview.

Since we use a Camera to render to the texture we can change the background to a solid black colour if we don’t want the skybox being rendered. It can also be useful to set the **Culling Mask** option on the Camera so we only render specific layers to the texture rather than all of them. Note that we should still have a **Main Camera** in our scene rendering normally, which might exclude these specific layers from it’s Culling Mask. This allows us to render objects, such as coloured particles, to a render texture without it affecting the normal view.

It is also possible to create a Render Texture at runtime in C# by using the [RenderTexture constructor](https://docs.unity3d.com/ScriptReference/RenderTexture-ctor.html). You should also Release render textures when they are no longer used, (including the one used by a camera previously if you are setting the targetTexture via code).

In order to reference a Render Texture from a shader, set up a texture [property](https://docs.unity3d.com/Manual/SL-Properties.html), the same as you would for a normal texture. e.g.

_name ("display name", 2D) = "defaulttexture" {}

In shadergraph, simply create a **Texture 2D property** from the blackboard, or create a **Texture 2D Asset** node, right-click and **Convert to Property**. You can rename the property and set the default texture in the blackboard.

Some examples of when Render Textures are used:

- Post processing effects. I believe old methods used
, but there is also the**Camera.OnRenderImage****Post Processing Stack v2**, which uses a**CommandBuffer**instead. Shaders should use the _MainTex property/reference as this will automatically be set when using a Blit. (See[here](https://docs.unity3d.com/Packages/com.unity.postprocessing@2.1/manual/Writing-Custom-Effects.html)for the manual page showing an example of writing custom effects for PPv2). The LWRP used to be compatible with this, but when it was renamed to URP it introduced it’s own post processing “v3” (Note : 2019.3+ / URP 7.2.0 versions should still support v2, but the plan is from 2020.1 only v3 will be supported). See[here](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@7.2/manual/integration-with-post-processing.html)for information on URP’s Post Procesing v3. It currently does not support custom effects though (URP 7.2.0), you currently need to use the URP Custom Renderer with a custom Blit pass[(see here)](https://github.com/Unity-Technologies/UniversalRenderingExamples/tree/master/Assets/Scripts/Runtime/RenderPasses). - View of a Security Camera being displayed on a Monitor.
- Mirrors or Portals (See
[here](https://www.youtube.com/watch?v=TkzASwVgnj8)for an example of Portals in the LWRP on Unity’s Youtube channel). - Rendering particles to a Render Texture for various interactive effects, such as leaving trails in snow or sand/mud, grass interaction, or adding ripple/ring effects to water. See the end of this post for a few tweets showing off some interesting effects!

### Color Formats

Render Textures have quite a few options for **Color Formats**, and some may not be supported by the target platform, which is where ‘Enable Compatible Color Format’ comes in useful. If a format is named **R8G8B8A8_UNORM**, this means the Render Texture will have channels for **Red**, **Green**, **Blue**, and **Alpha**, each having **8** bits (**1** byte) (**32** bits total). If you don’t need all those channels use a format which has less in order to save on memory. **R8_UNORM** for example only has the red channel. Using 8 bits per channel would also use less memory than **16** bits or **32** bits per channel, but will reduce the number of colours available.

As for the final part of the name :

**SRGB** = unsigned normalized format that uses sRGB nonlinear encoding. (Note, if an Alpha channel is also present it will be a linear unsigned normalized value).**UNORM** = unsigned normalized format. (Output will be between 0 and 1)**SNORM** = signed normalized format. (Output will be between -1 and 1)**UINT** = unsigned integer format. (Output will be between 0 and 2^(n-1), where n is how many bits the channel has)**SINT** = signed integer format. (Output will be between -2^(n-1) and 2^(n-1))**UFLOAT** = unsigned floating-point format.**SFLOAT** = signed floating-point format.**PACKn** = the format is packed into an underlying format with n bits.

See [here](https://docs.unity3d.com/ScriptReference/Experimental.Rendering.GraphicsFormat.html) for more info on these formats.

For HDR colour support I believe you should use a **16** bit or **32** bit **SFLOAT** format. Render Textures can also support negative values, use one of the signed formats. (Note : If you are using a Camera to render to a Render Texture in the HDRP, and you require negative values, you also need to disable the Postprocess option under the Rendering tab of the Custom Frame Settings overrides on the Camera. I’m not sure why, but it seems to remove negatives if that is enabled).

### Reading Render Textures on the CPU

Render Textures are stored and handled on the **GPU**, which means we can’t access the data from them in a C# script which runs on the CPU – and you shouldn’t really need to for most effects. However, I wanted my player to be able to interact with water which was based on a Render Texture and only spawn particles if the player was in the water, along with some other effects. In order to find where the water was, I needed a way of obtaining the render texture data on the CPU.

In order to do this we can create a **Texture2D**, and use the ** Texture2D.ReadPixels** function to copy the active render texture to the CPU. This is a very slow method though, and causes the CPU to stall until it’s finished obtaining the data, so should be used sparingly. A better approach is to use

**instead, which won’t stall the CPU for better performance, but can cause a few frames of latency. The script below shows an example of how to use this.**

[AsyncGPUReadback.Request](https://docs.unity3d.com/ScriptReference/Rendering.AsyncGPUReadback.Request.html)```
using System.Collections.Generic;
using UnityEngine.Rendering;
using Unity.Collections;
using UnityEngine;
public class RenderTextureGPURequest : MonoBehaviour {
public RenderTexture renderTexture;
private Queue<AsyncGPUReadbackRequest> requests
= new Queue<AsyncGPUReadbackRequest>();
private float t;
private float timeBetweenRequests = 0.2f;
void Update() {
// Handle Request Queue
while (requests.Count > 0) {
// Get the first Request in the Queue
AsyncGPUReadbackRequest request = requests.Peek();
if (request.hasError) {
// Error!
Debug.LogWarning("AsyncGPUReadbackRequest Error! :(");
requests.Dequeue(); // Remove from Queue
} else if (request.done) {
// Request is done, Obtain data!
NativeArray<Color32> data = request.GetData<Color32>();
// RGBA32 -> use Color32
// RGBAFloat -> use Color
// else, you may have to use the raw byte array:
// NativeArray<byte> data = request.GetData<byte>();
// Do something with the data
if (data.Length <= 0) {
// No data?
} else if (data.Length == 1) {
// Single Pixel
// Note, we don't know the coords of the pixel obtained
// If you want this information, consider wrapping the
// AsyncGPUReadbackRequest object in a custom class.
} else {
// Full Image
}
requests.Dequeue(); // Remove from Queue
} else {
// Request is still processing.
break;
}
// Note : We have to Dequeue items or break,
// or we'll be caught in an infinite loop!
}
// Handle Request Timer
t += Time.deltaTime;
if (t > timeBetweenRequests) {
t = 0;
RequestScreen();
//RequestPixel(0, 0);
// Note that 0,0 is in the bottom left corner
// of the Render Texture
}
}
private void RequestScreen() {
AsyncGPUReadbackRequest rq = AsyncGPUReadback.Request(
renderTexture
);
requests.Enqueue(rq);
}
private void RequestPixel(int x, int y) {
if (x < 0 || x >= renderTexture.width ||
y < 0 || y > renderTexture.height) {
// Pixel out of the render texture bounds!
return;
}
AsyncGPUReadbackRequest rq = AsyncGPUReadback.Request(
renderTexture, // Render Texture
0, // Mip Map level
Mathf.RoundToInt(x), // x
1, // Width (1 as we want a single pixel)
Mathf.RoundToInt(y), // y
1, // Height (1 as we want a single pixel)
0, // z
1, // Depth
TextureFormat.RGBA32); // Format
// I believe this should reflect the Color Format the render texture has,
// 8 bits per channel = RGBA32 (or R8, RG16, RGB24)
// 16 bits per channel = RGBAHalf (or RHalf, RGHalf, RGBHalf)
// 32 bits per channel = RGBAFloat (or RFloat, RGFloat, RGBFloat)
// Note that not all Color Formats are supported by AsyncGPUReadback
// Some will return errors/warnings.
// UNORM seems to be supported, but SNORM returns errors.
// If you need negative values, use a Half or Float format
// I recommend using RGBA32 or RGBAFloat, as you can retrieve
// the data as a NativeArray of Color32 or Color objects respectively.
requests.Enqueue(rq);
}
}
```

Update Note : It’s also possible to use the [AsyncGPUReadback.Request](https://docs.unity3d.com/ScriptReference/Rendering.AsyncGPUReadback.Request.html) with a callback parameter to trigger what happens when the request is done, rather than using the Queue and loop in the above example. [See here](https://github.com/keijiro/AsyncCaptureTest) for an example.

You could also request a specific rectangle from the screen by using a method similar to RequestPixel, but also setting the width and height. You can use request.width and request.height to get them back after the request is done, to split/handle the data correctly. (I don’t know however if requesting less pixels makes the operation any less expensive or quicker though).

Note that you don’t seem to be able to get the x and y coordinates of the request back, but you could probably wrap the request in a custom class to add some extra variables to hold data, and add that class to the Queue instead. For my purposes, I just needed the colour of the pixel at the player’s position, where the render texture is on a plane. Using the above, this is something like :

float scale = 512f / 10f;

Vector3 position = player.transform.position;

float x = position.x * scale + 512f / 2f;

float y = position.z * scale + 512f / 2f;

RequestPixel(x, y);

Assuming the render texture’s width and height are 512, and the plane it is rendered to spans 10 world space units, centred at the origin, hence the offset of 256 is required.

Sources : [https://docs.unity3d.com/Manual/class-RenderTexture.html](https://docs.unity3d.com/Manual/class-RenderTexture.html)[https://docs.unity3d.com/ScriptReference/Experimental.Rendering.GraphicsFormat.html](https://docs.unity3d.com/ScriptReference/Experimental.Rendering.GraphicsFormat.html)

Script based on an older version of [https://github.com/keijiro/AsyncCaptureTest](https://github.com/keijiro/AsyncCaptureTest)

Here’s something I’ve done with rendering particles to a Render Texture. I haven’t got a breakdown blog post of this yet, but check the twitter thread for more details!

I’ve also collected a few tweets showing off some Render Texture based stuff. (If anyone here doesn’t want their tweet here, let me know and I’ll remove it).