---
title: Fresnel Effect
url: https://cyangamedev.wordpress.com/2019/09/04/fresnel-effect/
author: Cyan
published: '2019-09-04'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

![](../../assets/5908a1c04815dfcf.png)

The shadergraph documentation defines this node as :

“*Fresnel Effect is the effect of differing reflectance on a surface depending on viewing angle, where as you approach the grazing angle more light is reflected. The Fresnel Effect node approximates this by calculating the angle between the surface normal and the view direction.”*

In other words, the node will output a value based on the mesh’s **normal** (a vector pointing out from each vertex) and the **view direction** (a vector from the camera to the fragment/pixel position). The bigger the **angle** between them, the larger the value returned. At an angle difference of **90 degrees** this is exactly **1**. While normals that face the camera return smaller values or **0** if they exactly align, and we can specify a **Power** value to adjust this. It is sometimes also referred to as ‘rim lighting’.

Shadergraph has a built-in node for this which is very useful, the generated code looks as follows :

```
void Unity_FresnelEffect_float(float3 Normal, float3 ViewDir,
float Power, out float Out) {
Out = pow((1.0 - saturate(dot(normalize(Normal),
normalize(ViewDir)))), Power);
}
```

Note that if a shader is **Transparent** and using **Two Sided**, since the mesh’s normals usually point away from the view direction they will return **1**. If this isn’t the intended result, you can make use of a **Branch** with the **Is Front Face** node to prevent this by only using the **Fresnel Effect** output for the front faces, or to invert the **Normal Vector** input like so:

![](../../assets/0126f3937dd49187.png)