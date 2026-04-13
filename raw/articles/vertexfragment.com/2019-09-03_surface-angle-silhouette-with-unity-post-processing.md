---
title: Surface Angle Silhouette with Unity Post-Processing
url: https://www.vertexfragment.com/ramblings/unity-deferred-post-processing/
author: Steven Sell
published: '2019-09-03'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![Silhouette Outlining on a Dragon and Bunny Model Silhouette Outlining on a Dragon and Bunny Model](../../assets/43d32443ffcbf601.png)


In this ramble I will demonstrate how to use post-processing within Unity’s deferred rendering pipeline by writing a basic surface angle silhouette shader. It is assumed that the reader has some familiarity with Unity and it’s deferred rendering functionality.

We will see how to set up post-processing within a Unity scene, using both a Post-Processing Layer and Volume, as well as how to access the GBuffer textures and calculating basic scene values such as camera direction and pixel world position. While we will work within the deferred pipeline, it is possible to apply post-processing effects in a purely forward rendered scene though additional steps are necessary to capture the data that is freely available within the deferred GBuffers.

*Note: This section assumes you are not using the High Definition Render Pipeline (HDRP) which includes it’s own post-processing implementation.*

To begin, we must first install the Post Processing package as it does not come in the default Unity project setup. This can be retrieved through the **Window > Package Manager** window and searching for the [Post Processing package](https://docs.unity3d.com/Packages/com.unity.postprocessing@2.1/manual/index.html) (v2.1.7 at the time of writing).

With the package installed you will have access to the `UnityEngine.PostProcessing.Runtime`

assembly. It should be noted that if you have defined your own `.asmdef`

for your project that you will need to add a reference to this assembly. If you do not you will receive numerous errors in later steps such as:

```
error CS0234: The type or namespace name 'PostProcessing' does not exist in the namespace 'UnityEngine.Rendering' (are you missing an assembly reference?)
```


Before we write our own post-processing effect, we will try to use one of the post-processing effects that come with the package.

First, select your main camera and add a `Post Process Layer`

component to it. For right now the only field we care about is the `Layer`

which we want to set to `Everything`

. This sets up our camera so that it will render the effect that we are about to add. Additionally, the Post Process Layer also gives us access to multiple AA implementations including FXAA, SMAA, and TAA.

![](../../assets/bb7e5463e73de780.png)


With our camera setup to view post-processing effects we will now add one to the scene. This is done by creating a new object in the scene and adding a `Post Process Volume`

component to it. For this example we want to make sure that the `Is Global`

box is checked which will apply the effect to the entire scene.

To add the effect itself, click `New`

in the `Profile`

row to create a new effect profile. These profiles store information such as what effect to apply and the values of their customization parameters, if they have any. With the profile created, you should see an `Add effect...`

button appear at the bottom of the component properties. When this is clicked you will be presented with a list of built-in effects that you may apply, such as Ambient Occlusion (SSAO) and Bloom.

For demonstration purposes, choose the `Grain`

effect. To enable the effect, check the `Intensity`

box and slide the value to 1.0. You should now see a grainy film effect applied to your camera in both Scene and Game mode.

![](../../assets/5728a6ca4a26cb4b.png)


At this point you can play around with the other settings for the effect and for the volume as well, such as `Weight`

, to gain an understanding of what they do. You can also try creating a new GameObject layer to store your effect in, which can then be referenced by the Post Process Layer component that is attached to the main camera. This will allow you to selectively render global effects without having to toggle the effect itself on/off.

It is time to create our own post-processing effect now that we know how to add them to the scene.

The effect we will be creating is called a Surface Angle Silhouette. This is a relatively simple effect which operates on the dot product between an object’s normal and the camera view direction to produce a silhouette or outline on the object. We will expose properties within the effect to control the width, density, and color which will give us enough control to produce results ranging from subtle highlights to thick toon-esque edges.

The effect is split into two different parts: the Unity component and the screen-space shader. Though either one could be done first, it is generally better to write the component before the shader so that we can see our incremental progress in the shader and tweak it as we go.

Each post-processing component is comprised of two classes:

`PostProcessEffectSettings`

which defines the parameters that controls the effect, such as outline thickness and color.`PostProcessEffectRenderer`

which is responsible for drawing the screen-space triangle on which our effect shader is applied.

To start we will define our effect settings class. We want to expose three parameters for controlling the effect: thickness, density, and color.

|
|

In the first two lines we create our effects class and provide metadata about it. The metadata specifies which renderer will be used (which we have not yet defined, causing a chicken-or-the-egg situation), when the effect should be rendered, and the name of the effect shown within the Unity Editor when selecting it from the effect list.

`PostProcessEvent`

enumeration value that is specified in the settings class decorator, and are as follows:
`BeforeTransparent`

the effect is applied only to opaque objects, before the transparent pass.`BeforeStack`

the effect is applied before the built-in effects, such as AA and depth-of-field.`AfterStack`

the effect is applied after the built-in effects.

In the body of the class we then define our three control parameters as we detailed before: two clamped floats and a color value. With our settings complete we can move on to the renderer class.

In the renderer we will retrieve our custom shader (that has yet to be created), apply our settings control parameters, and then blit a fullscreen pass to a destination buffer using the current render buffer as input.

|
|

With both the settings and renderer defined, let’s modify our scene to add it. Select the GameObject which we previously added a `PostProcessVolume`

to and remove or disable the Grain effect. Then click `Add effect...`

and select our new `SurfaceAngleSilhouetting`

.

And voilà! Our screen has turned black and the Unity Editor console is displaying an error message informing us that it can not find our custom shader.

Now for the fun part, create a new shader in the editor and set it’s contents to the following:

|
|

`VaryingsDefault`

structure.
Our once black screen should now be green as the post-processing renderer component has found our new shader. It should be noted that while we are writing our shader using HLSL, it will be cross-compiled to GLSL when we are not using a Direct3D-based renderer.

We will now start incrementally building up our shader. Future code snippets will show only the modified or added portions, but the complete shader is available at the end.

![From left to right: the scene render target, depth buffer, and surface normals. From left to right: the scene render target, depth buffer, and surface normals.](../../assets/0719685e3113aa03.png)


Our first step in creating the actual effect is to recreate the scene by extracting three components: the current render target, depth buffer, and the scene normals.

We require the current render target as we will be applying our effect on top of the previously rendered image, the depth to exclude the skybox from our effect, and the normals for each fragment as the surface angle silhouette is calculated as:

Where,

`V`

is the normalized camera view vector.`S`

is the surface normal for the current fragment.

Fortunately for us, all three of these components are provided as inputs to our shader as we are using the deferred pipeline. They can be retrieved by adding definitions for the relevant textures and then sampling them within our fragment shader.

|
|

Where `_MainTex`

is the current render target, [ _CameraDepthTexture](https://docs.unity3d.com/Manual/SL-CameraDepthTexture.html) is the main camera’s depth texture, and

`_CameraGBufferTexture2`

is our GBuffer texture containing the scene normals. Notice that we have to undo the transformation applied to our normal which fits it to the range of `[0, 1]`

. The other sampled values are usable without any further modifications.[Deferred Shading Rendering Path](https://docs.unity3d.com/Manual/RenderTech-DeferredShading.html), but can vary if using a custom deferred shader. By default, they are:

`_CameraGBufferTexture0`

which is`{diffuse.rgb, occlusion}`

.`_CameraGBufferTexture1`

which is`{specular.rgb, roughness}`

.`_CameraGBufferTexture2`

which is`{normal.rgb, unused}`

.`_CameraGBufferTexture3`

which is the cumulative lighting. (HDR or LDR)

Now that we have the surface normal we will need the camera view vector. Once that is retrieved we can finalize our effect.

It is important for us to keep in mind that there is not a single uniform value for the camera direction as we are using a perspective projection. So the direction vector at UV coordinate `(0, 0)`

will be different from the vector at `(1, 1)`

.

In order to interpolate the view vector over the screen we will calculate it in our Vertex shader. However we are currently using the `VertDefault`

program provided by our inclusion of `StdLib.hlsl`

so we will first create our own Vertex program. Additionally we will use a new structure for Vertex output/Fragment input so that we can interpolate our camera view vector.

|
|

And in our shader pass we set our new `VertMain`

program as the Vertex shader:

`#pragma vertex VertMain`


Now we will calculate three vectors: the camera forward vector, the local direction vector, and finally our vector pointing to the camera.

To calculate the first of these vectors, the uniform camera forward vector, we simply unproject the NDC-space coordinate `(0.0, 0.0, 0.5)`

back to world-space. The returned vector is constant regardless of which vertex or fragment is being rendered. Note that the calculation makes use of `_ViewProjectInverse`

which we provided as input from our renderer component and `_WorldSpaceCameraPos`

is provided by Unity.

```
float4 cameraForwardDir = mul(_ViewProjectInverse, float4(0.0, 0.0, 0.5, 1.0));
cameraForwardDir.xyz /= cameraForwardDir.w;
cameraForwardDir.xyz -= _WorldSpaceCameraPos;
```


We want the non-normalized direction vector as we will use it’s length in an upcoming step. If all we wanted was the camera direction we could instead unproject `(0.0, 0.0, 1.0)`

and perform normalization after converting to world-space. However, what we are actually interested in is what we will be referring to as the “local” camera direction.

As we are using a perspective projection, the uniform view direction calculated earlier is only valid for the UV coordinate `(0.5, 0.5)`

. As we move away from this position the angle will vary across the image as we approach the edges of our view frustum. To calculate this “local” direction, we perform the following:

```
float4 cameraLocalDir = mul(_ViewProjectInverse, float4(o.texcoord.x * 2.0 - 1.0, o.texcoord.y * 2.0 - 1.0, 0.5, 1.0));
cameraLocalDir.xyz /= cameraLocalDir.w;
cameraLocalDir.xyz -= _WorldSpaceCameraPos;
```


Breaking this down, we first convert from our UV screen-space coordinates to NDC-space remembering that the NDC unit cube ranges from `[-1, -1, 0]`

to `[1, 1, 1]`

.

`float4(o.texcoord.x * 2.0 - 1.0, o.texcoord.y * 2.0 - 1.0, 0.5, 1.0)`


Next we take our NDC-space position and unproject it back to projection-space:

`mul(_ViewProjectInverse, float4(o.texcoord.x * 2.0 - 1.0, o.texcoord.y * 2.0 - 1.0, 0.5, 1.0));`


Then we perform perspective division to return to view-space:

`cameraForwardDir.xyz /= cameraForwardDir.w;`


And finally from view-space to world-space:

`cameraForwardDir.xyz -= _WorldSpaceCameraPos;`


Whew. One step left and then we will have our “local” view direction vector:

`o.cameraDir = cameraLocalDir.xyz / length(cameraForwardDir.xyz);`


|
|

Between the inputs to our shader program and the output of our Vertex shader, we now have everything we need to apply the silhouette edges to our image in the Fragment shader. Let’s start by visualizing our dot product:

|
|

![](../../assets/ca8bd9a8831cb732.png)


Next we use our remaining input values from our renderer component to transform our raw dot product values into a proper silhouette/outline:

|
|

![](../../assets/097f08d670474d5e.png)


And that is it! From the Unity Editor we can now modify our post-processing effect control parameters to make a wide range of silhouettes and outlines, from thick black comic book style lines to smoothly interpolated colored highlights.

Along the way we have also learned how to use the Unity Post Processing package, create our own HLSL-based shader, and calculate various commonly-used values such as the camera direction and transforming from screen-space back to world-space.

As a final bonus calculation, we can easily calculate the world position of our current fragment with:

```
float linearDepth = LinearEyeDepth(sceneDepth);
float3 worldPosition = (i.cameraDir * linearDepth) + _WorldSpaceCameraPos;
```


![The absolute world position set as the scene color. The absolute world position set as the scene color.](../../assets/22b9183844a1167b.png)


|
|

|
|

|
|

[Unity Post Processing Package Documentation](https://docs.unity3d.com/Packages/com.unity.postprocessing@2.1/manual/index.html)*Dragon*model is sourced from:[http://graphics.stanford.edu/data/3Dscanrep/](http://graphics.stanford.edu/data/3Dscanrep/)*UV-Unwrappd Stanford Bunny*model is sourced from:[https://blenderartists.org/t/uv-unwrapped-stanford-bunny-happy-spring-equinox/1101297](https://blenderartists.org/t/uv-unwrapped-stanford-bunny-happy-spring-equinox/1101297)