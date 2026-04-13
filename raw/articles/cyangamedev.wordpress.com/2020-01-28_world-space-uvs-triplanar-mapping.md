---
title: World space UVs & Triplanar Mapping
url: https://cyangamedev.wordpress.com/2020/01/28/worldspace-uvs-triplanar-mapping/
author: Cyan
published: '2020-01-28'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This post includes an introduction to using the **Position** node to sample textures rather than using mesh **UV** channels, which is also the basis of **Triplanar** mapping. It won’t be super in-depth but will provide some example graphs to (hopefully) help beginners understand how this could be used!

### World space UVs

We use UVs to tell the shader what parts of a texture to render to a model. While we usually use the ones stored in the mesh **UV** channels it can also be useful to use the **World** **space** **Position** of the fragment/pixel instead, especially if there aren’t any **UV** coordinates available. I tend to refer to this as World space UVs, but I’ve also seen this referred to as World space “**projected**” (or aligned) UVs and **planar** texture mapping.

The **Position** node gives us a **3D vector** however, and the **UV** coordinates required to sample a **Texture2D** are two dimensional. Therefore, we can only use **two** components from the position vector. For example, we could use the **X** and **Z** components (labelled as **R** and **B** in the **Split** node) to sample a texture. Since the **Y** axis isn’t included in the sample, this has the result of “**projecting**” the texture from above/below.

An implementation of this in shadergraph would be :

![](../../assets/5c782c91817474d4.png)


![](../../assets/5c782c91817474d4.png)

Side note, the

**Position**node’s

**World**and

**Absolute World**spaces are identical for the Universal Render Pipeline (

**URP**). However in the High Definition Render Pipeline (

**HDRP**), the

**World**positions are

[Camera Relative](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@6.7/manual/Camera-Relative-Rendering.html), therefore use

**Absolute World**if you don’t want the positions moving with the camera!

![](../../assets/7d35125403e598a3.png)

Since the coordinates are in **world space**, the **position**, **rotation** and **scale** of the **object** in the scene does not affect the coordinates. This has the advantage of being able to use multiple planes, even at different sizes, and the texture will connect **seamlessly**. In the example image, I’ve left some small gaps between the water planes to show they are separate, however their texture does clearly tile correctly.

We can adjust the **scaling** via a **Multiply** (or use the **Tiling and Offset** node), as well as change **rotation** via the **Rotate** node. As long as the scaling, offset and rotation values stay consistent between objects we’ll get that seamless connection. If for some reason you want the texture to move with the object, you can offset the world space UVs with the **object’s world space** **Position** from the **Object** node. However doing this may break the seamless connections between multiple objects as the offset will be different per object.

While this is great for flat planes, what about **3D** objects? The textures here on the left look very stretched as the texture is only projected in the Y axis. This is where **triplanar mapping** comes in useful! (The result shown on the right)

![](../../assets/960ed9a487963436.png)

### Triplanar Mapping

![](../../assets/adaf9b0b1b9f8780.png)

**Triplanar** mapping uses the World space UVs (or planar mapping), but three times, for each axis direction. It blends between the three textures based on the mesh world space **Normal Vector**. This can be useful if UVs would stretch textures too much or aren’t available for the mesh (e.g. Procedurally generated content where you aren’t generating UVs).

Triplanar mapping can be considered a fairly advanced topic, but luckily shadergraph does have a built-in node for it. It does only have a single texture input though, (but the code the node uses could easily work with multiple textures if it had more inputs).

![](../../assets/d8b878d946244510.png)

If we wanted the **upwards Y** axis to have a different texture than the other sides (including the negative Y axis), we could use the **Triplanar** node with an additional **Texture Sample 2D** and mask based on the **Normal Vector**.

Something like the following would work. Our shader does now have 4 texture samples though, which isn’t too bad, but this is currently only sampling the albedo/colour. If we also wanted to apply metallic/specular maps and/or normal maps while also using triplanar mapping, this could become quite expensive.

(To be clear, if our mesh has UVs we don’t need to use triplanar mapping to obtain this blend between textures. We can also use the **Normal Vector** and **Lerp** node like this to blend between two **Sample Texture 2D** node outputs (sampled using the default **UV** input).

If for some reason we want to use a different texture for each axis of the triplanar mapping, we would have to recreate what the **Triplanar** node does as it doesn’t have multiple texture inputs. This can also be useful to help see how the node works.

This can be done either as **graph nodes** or via a **Custom Function** node. It’s probably easier to use a custom function, as we could copy the node’s generated code from the docs page, but I’ve also included a node version below. Since this is mostly an introduction post, I won’t be going over the implementation in detail – but I have included some resources at the end of the post if you want more in-depth explanations. (Note the graph/code below doesn’t include triplanar mapping for **Normal map** textures – Check the [Triplanar node docs page](https://docs.unity3d.com/Packages/com.unity.shadergraph@7.1/manual/Triplanar-Node.html) for generated code to see how that is implemented).

### Multi-texture Triplanar (Albedo/Colour, using Nodes)

Below is the graph which replicates what the **Triplanar** node does (with the **Default Type** setting). As we have access to each **Sample Texture 2D** we can connect different textures to each node. The blending function is based on the **Normal Vector**, which we take the **Absolute** of to flip negative values into the positive, as we want both sides of each axis to blend. The **Power** controls the amount of blending, where a higher **Blend Vector1 property** value will cause a sharper/smaller blend between the textures. The **Dot Product** and **Divide** part is to retain the correct brightness for the texture, as without it the result looks darker. If you want to control the tiling of each texture separately, add **Tiling and Offset** nodes between the **Vector2** and **Sample Texture 2D** nodes.

![](../../assets/e46d0a938a2ae44a.png)

### Multi-texture Triplanar (Albedo/Colour, using Custom Function)

```
void MultitextureTriplanar_float(Texture2D TextureA, Texture2D TextureB, Texture2D TextureC, SamplerState Sampler,
float3 Position, float3 Normal, float Tile, float Blend, out float4 Out){
float3 Node_UV = Position * Tile;
float3 Node_Blend = pow(abs(Normal), Blend);
Node_Blend /= dot(Node_Blend, 1.0);
float4 Node_X = SAMPLE_TEXTURE2D(TextureA, Sampler, Node_UV.zy);
float4 Node_Y = SAMPLE_TEXTURE2D(TextureB, Sampler, Node_UV.xz);
float4 Node_Z = SAMPLE_TEXTURE2D(TextureC, Sampler, Node_UV.xy);
Out = Node_X * Node_Blend.x + Node_Y * Node_Blend.y + Node_Z * Node_Blend.z;
}
```

Note that there is a slight downside to using a **Custom Function** node – Shadergraph doesn’t seem to have a way to use the **Sampler** associated with the texture input passed in (which contains the texture **Filter **and **Wrap **modes). It seems only the **Sample Texture 2D** node can automatically use the sampler for the given texture. For our **Custom Function**, we need to pass in a **Sampler** instead, and leaving the input blank will use the default values of **Linear** filtering and **Repeat** wrap mode.

Sources & Other Resources :

[https://docs.unity3d.com/Packages/com.unity.shadergraph@7.1/manual/Triplanar-Node.html](https://docs.unity3d.com/Packages/com.unity.shadergraph@7.1/manual/Triplanar-Node.html)[https://www.patreon.com/posts/quick-game-art-16714688](https://www.patreon.com/posts/quick-game-art-16714688) [https://catlikecoding.com/unity/tutorials/advanced-rendering/triplanar-mapping/](https://catlikecoding.com/unity/tutorials/advanced-rendering/triplanar-mapping/) [http://www.martinpalko.com/triplanar-mapping/](http://www.martinpalko.com/triplanar-mapping/)[https://medium.com/@bgolus/normal-mapping-for-a-triplanar-shader-10bf39dca05a](https://medium.com/@bgolus/normal-mapping-for-a-triplanar-shader-10bf39dca05a)