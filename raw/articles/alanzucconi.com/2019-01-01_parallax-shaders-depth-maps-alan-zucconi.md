---
title: Parallax Shaders & Depth Maps - Alan Zucconi
url: https://www.alanzucconi.com/2019/01/01/parallax-shader/
author: Alan Zucconi
published: '2019-01-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In the previous part of this series, [Inside Facebook 3D Photos](https://www.alanzucconi.com/?p=9493), we have explained how modern mobile phones are able to infer depth from pictures. Such a piece of information is stored in a **depth map**, which is used for a variety of effects. From blurring the background to three-dimensional reconstruction, this type of technology will become more and more present in our daily lives.

![](../../assets/9f5519082519a5fe.gif)

This is a two-part series. You can read all the posts here:

- Part 1.
[Inside Facebook 3D Photos](https://www.alanzucconi.com/?p=9493) - Part 2.
[Parallax Shaders & Depth Maps](https://www.alanzucconi.com/?p=10453)

A link to the complete Unity package is available at the end of the tutorial.

## The Shader Template

If we want to recreate Facebook 3D photos using a shader, we first need to establish what exactly we are going to do. Since this effect works best on 2D images, it makes sense to implement a solution that is compatible with Unity **Sprites**. This will be achieved by creating a shader that can be used on **Sprite Renderers**.

While it is possible to create such a shader from scratch, it is often preferable to start from an existing template. The best way forward is to make a copy of the existing sprite diffuse shader that Unity is using by default for all sprites. Unfortunately, the engine is not shipped with a *shader* file that we can edit ourselves.

To retrieve it, we need to visit the [Unity download archive](https://unity3d.com/get-unity/download/archive), and download the Built in* shaders* package (below) for the version we are currently using.

![](../../assets/9f94bd0c81731d8a.png)

Once the package is extracted, we can browse the source code for all the shaders that are shipped in Unity. The one we are interested in is *Sprites-Diffuse.shader*, which is the one used by default for all the newly created sprites.

## The Images

The second aspect that we need to formalise is what data we have. Let’s imagine we have both the image that we want to animate, and its depth map. The latter will be a black and white image where black and white indicates that pixels are, respectively, very far or very close to the camera.

The images used for this tutorial come from [Dennis Hotson](https://twitter.com/dennishotson)‘s [Pickle cat](https://dn.ht/picklecat/) project (🥒🐱) which is, undoubtedly, the best thing you will see today.

![](../../assets/6d287300068d8577.png)

The depth map associated with the image above has been designed to reproduce the distance of the cat’s face from the camera.

![](../../assets/7d6ef5c54c4e0b28.jpg)

It’s easy to see how relatively good results can be achieved with such a simple depth map. This means that is not hard to create your own depth maps for images that already exist.

## The Properties

Now that we have all the resources, we have everything we need to start coding our parallax shader. If we import the main image as a sprite, then Unity will pass it to the shader automatically via the `_MainTex`

property. What we need to add, however, is a way to make the depth map accessible to the shader. We can do this by adding a new **shader property** called `_HeightTex`

. I have intentionally decided not to call this `_DepthTex`

to avoid confusion with the **depth texture** (a similar concept in Unity that is used to render depth maps from a scene).

To modulate the strength of the effect, we also add a property called `_Scale`

.

Properties { ... _HeightTex ("Heightmap (R)", 2D) = "gray" {} _Scale ("Scale", Vector) = (0,0,0,0) }

These two newly created properties also have to be matched by two variables with the same name, to be included in the `CGPROGRAM`

/`ENDCG`

section:

sampler2D _HeightTex; fixed2 _Scale;

Now that we have everything, we are ready to write the code that actually makes the displacement happen.

The first step is to sample the value of the depth map, which is possible thanks to the `tex2D`

function. Since `_HeightTex`

is a black and white texture, we can simply take its red channel discarding all the others. The value that we now have measures, on some arbitrary units, the distance of the current pixel from the camera.

The depth value ranges from ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com -1](../../assets/5209a4a606950b66.png)

![Rendered by QuickLaTeX.com +1](../../assets/07166c3ac7d7ae94.png)


### ⭐ Recommended Unity Assets

## The Theory

To simulate the parallax effect, what we need to do at this point is to use the depth information to shift the pixels of an image. The closer a pixel is, the more we need to shift it. This process is explained in the diagram below. The red pixel from the *original image* should be shifted by two pixels on the left, according to the information from its depth map. Likewise, the blue pixel is supposed to be shifted two pixels on the right.

![](../../assets/fea1f80c59e53bd9.png)

While this works *theoretically*, there is no easy way to achieve it in a shader. This is because a shader, by design, can only change the colour of the *current* pixel. When the shader code is executed, it is to draw a specific pixel on the screen; we cannot simply shift that pixel to another location, or changing the colour of a nearby one. This *constraint of locality* allows shaders to be run in parallel very efficiently, but also prevents us from achieving all sorts of effects that would be trivial if we had *random write access* to every pixel in an image.

If we really wanted to be precise, we would need to sample the depth map of all nearby pixels to find out which one (if any) is supposed to move to our position. If multiple pixels lands on our very position, we can average their contribution accordingly. While this works and gives the best possible result, it is also exceptionally inefficient and potentially hundreds of times slower than the original diffuse shader we started from.

The next best thing that we can do, is another one. We retrieve the depth of the current pixel from the depth map; then, if we were supposed to shift on the *right*, we replace the current colour with the pixel on the *left* (below). The assumption here is that if we are supposed to move to the right, perhaps the nearby pixels on the left is supposed to move in a similar way as well.

![](../../assets/2958dee7c12fc939.png)

It should be easy to see that this is only a cheap approximation of what we really want to achieve. Nonetheless, it turns out to be very effective. This is because depth maps are generally smooth.

## The Code

Following the algorithm described in the previous section, we can implement a parallax shader using a simple **UV displacement **approach.

This leads to the following code:

void surf (Input IN, inout SurfaceOutput o) { // Displacement fixed height = tex2D(_HeightTex, IN.uv_MainTex).r; fixed2 displacement = _Scale * ((height - 0.5) * 2); fixed4 c = SampleSpriteTexture (IN.uv_MainTex - displacement) * IN.color; ... }

The technique works well with mostly flats objects, as it can be seen in the animation below.

![](../../assets/ce41d9c1925d3953.gif)

This technique really shines on 3D models. This is because is very easy to render depth textures for 3D scenes. Below, you can see an image that has been rendered in 3D next to its depth map.

![](../../assets/2d40efa231d5566c.jpg)

The final results can be seen here:

![](../../assets/f3cd2bf9304a49bd.gif)

## Conclusion

This online course introduced the concept of 3D photos, and how they can be reimplemented in Unity.

This is a two-part series. You can read all the posts here:

- Part 1.
[Inside Facebook 3D Photos](https://www.alanzucconi.com/?p=9493) - Part 2.
[Parallax Shaders & Depth Maps](https://www.alanzucconi.com/?p=10453)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)You can download the full Unity Project for this download on [Patreon](https://www.patreon.com/posts/23680800).

Credits for the picture of the cat and its depth map goes to [Dennis Hotson](https://twitter.com/dennishotson)‘s [Pickle cat](https://dn.ht/picklecat/) project.

## Leave a Reply Cancel reply