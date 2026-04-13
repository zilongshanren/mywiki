---
title: 'CD-ROM Shader: Diffraction Grating - Part 2 - Alan Zucconi'
url: https://www.alanzucconi.com/2017/07/15/cd-rom-shader-2/
author: Alan Zucconi
published: '2017-07-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post completes the series on how to create a shader for CD-ROMs.

![](../../assets/2c71be173dfa1509.png)

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6703)(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
[Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651) - Part 5.
[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) - Part 6.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6767)(Part 1) - Part 7.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6791)(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

A link to **download** the **Unity project** used in this series is also provided at the end of the page.

#### Introduction

In the first part of this tutorial, we have created a first approximation for the iridescent reflections that CD-ROMs exhibit. It’s important to remember that this shader is physically based. To correctly simulate the reflection we want, we need to make sure that the tracks on our CD-ROM are arranged in a circular way. This will ensure a radial reflection.

#### Slit Orientation

The grating equation that we have derived in [The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) has a big limitation: it assumes that the slits are all aligned in the same direction. While this is often the case with insects’ exoskeletons, the bands on the surface of a CD-ROM are arranged in a circular pattern. If we naively implement the solution presented in the section above, we will obtain a rather disappointing reflection (below, right).

![](../../assets/45b778208e267679.png)

To correct this issue, we need to take into account the local orientation of the slits on a CD-ROM. Using the normal vector will not help here since all the slits share the same normal direction, which points away from the surface of the disk. What correctly captures the local orientation of a slit is its tangent vector (above, left).


![](../../assets/53aef8cd5bf70dea.png)

In the diagram above, the normal direction ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

![Rendered by QuickLaTeX.com \theta_V](../../assets/b093ae38d3530c80.png)

![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com \Theta_L](../../assets/355e5cde48abcb8f.png)

![Rendered by QuickLaTeX.com \Theta_V](../../assets/0003a156b85017de.png)

![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

![Rendered by QuickLaTeX.com \theta_V](../../assets/b093ae38d3530c80.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com \Theta_L](../../assets/355e5cde48abcb8f.png)

![Rendered by QuickLaTeX.com \Theta_V](../../assets/0003a156b85017de.png)


So far, we know that:

![Rendered by QuickLaTeX.com \[N \cdot L = \cos{\theta_L}\; \; \; N \cdot V = \cos{\theta_V}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0c0587329c71248c7e70e2a7ec255bd0_l3.png)


![Rendered by QuickLaTeX.com \[T \cdot L = \cos{\Theta_L}\; \; \; T \cdot V = \cos{\Theta_V}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b4fdab037e7b8a3df1025df4f244774b_l3.png)


Since ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)


![Rendered by QuickLaTeX.com \[T \cdot L = \cos{\Theta_L} = \sin{\theta_L}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b6b770c6e6d2f24a12c9f0637e5d076b_l3.png)


![Rendered by QuickLaTeX.com \[T \cdot V = \cos{\Theta_V} = \sin{\theta_V}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-329e23b82f1c6ab144b97724ea9fbe37_l3.png)


That is very convenient also because Cg offers a native implementation of the dot product. What’s left now is to calculate ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)


#### Calculating the Tangent Vector

To complete our shader, we need to calculate the tangent vector ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)


![](../../assets/6bab0879f35d4c48.png)

The diagram above shows how the tangent directions are calculated. The underlying assumption is that the surface of the disk is UV mapped like a quad, with coordinates ranging from (0,0) to (1,1). Once that is known, each point on the CD-ROM surface is remapped onto (-1,-1) to (+1,+1). With this change of the frame of reference, we have that the new coordinate of a point also corresponds with its direction away from the centre (green arrow). We can rotate that direction 90 degrees to find a vector that is tangent to concentric tracks of the CD-ROM (in red).

![](../../assets/46f8ba2701ababbb.png)

These operations need to be done in the `surf`

function of the shader since the UV coordinates are not available in the lighting function `LightingDiffraction`

.

// IN.uv_MainTex: [ 0, +1] // uv: [-1, +1] fixed2 uv = IN.uv_MainTex * 2 -1; fixed2 uv_orthogonal = normalize(uv); fixed3 uv_tangent = fixed3(-uv_orthogonal.y, 0, uv_orthogonal.x);

What’s left now is to convert the calculated tangent from **object space** to **world space**. The conversion will take into account the object translation, rotation and scale.

worldTangent = normalize( mul(unity_ObjectToWorld, float4(uv_tangent, 0)) );

### ⭐ Recommended Unity Assets

#### Putting All Together…

We now have all we need to calculate the colour contribution of the iridescence reflection:

inline fixed4 LightingDiffraction(SurfaceOutputStandard s, fixed3 viewDir, UnityGI gi) { // Original colour fixed4 pbr = LightingStandard(s, viewDir, gi); // --- Diffraction grating effect --- float3 L = gi.light.dir; float3 V = viewDir; float3 T = worldTangent; float d = _Distance; float cos_ThetaL = dot(L, T); float cos_ThetaV = dot(V, T); float u = abs(cos_ThetaL - cos_ThetaV); if (u == 0) return pbr; // Reflection colour fixed3 color = 0; for (int n = 1; n <= 8; n++) { float wavelength = u * d / n; color += spectral_zucconi6(wavelength); } color = saturate(color); // Adds the refelection to the material colour pbr.rgb += color; return pbr; }

#### Conclusion

![](../../assets/b09b8223f116f938.gif)

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6703)(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
[Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651) - Part 5.
[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) - Part 6.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6767)(Part 1) - Part 7.
**CD-ROM Shader: Diffraction Grating**(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for the CD-ROM Shader effect on [ Patreon](https://www.patreon.com/posts/13032957).

## Leave a Reply Cancel reply