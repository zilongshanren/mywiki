---
title: Correctly interpolating view/light vectors on large triangles
url: https://interplayoflight.wordpress.com/2013/05/17/correctly-interpolating-viewlight-vectors-on-large-triangles/
author: Kostas Anagnostou
published: '2013-05-17'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A few days ago an artist came to me scratching his head about a weird distortion he was getting on the specular highlight of his point light with an FX composer generated blinn shader. His geometry was comprised of large polygons and the effect of applying the reflection model to the surface was something like that:

Upon inspection of the shader, I noticed that the view and light directions were being calculated in the vertex shader:

vertexOutput std_VS(appdata IN) { vertexOutput OUT = (vertexOutput)0; OUT.WorldNormal = mul(IN.Normal,WorldITXf).xyz; OUT.WorldTangent = mul(IN.Tangent,WorldITXf).xyz; OUT.WorldBinormal = mul(IN.Binormal,WorldITXf).xyz; float4 Po = float4(IN.Position.xyz,1); float3 Pw = mul(Po,WorldXf).xyz; OUT.LightVec = (Lamp0Pos - Pw); #ifdef FLIP_TEXTURE_Y OUT.UV = float2(IN.UV.x,(1.0-IN.UV.y)); #else /* !FLIP_TEXTURE_Y */ OUT.UV = IN.UV.xy; #endif /* !FLIP_TEXTURE_Y */ OUT.WorldView = normalize(ViewIXf[3].xyz - Pw); OUT.HPosition = mul(Po,WvpXf); return OUT; }

Now, there is nothing wrong with calculating those vectors in the vertex shader, if anything it saves some GPU cycles in the pixel shader. The problem was that the vectors were normalised before sent out to the rasteriser.

During rasterisation triangles are interpolated using a process called barycentric interpolation, which in short combines the vertex attributes from the three corners of a triangle to produce a new value on a triangle point. Barycentric interpolation works ok on the inside of the triangle but degrades to linear interpolation on the edges:

In the above example the opposite sides of the 2 triangle quad have the same colour. It is apparent that on the common triangle edge the red colour are interpolated linearly with no contribution of the blue colour.

Really, the only vertex attribute that interpolates correctly is the position since it inherently expresses spatiality. Other quantities that might change a lot over the surface of the triangle like colours, the view/light directions are affected most, especially for large triangles like in the above case. This is exactly what happens to the view and light vectors, something that affects the specular highlight on the triangle.

Since position interpolates correctly, an obvious solution to the above problem is to calculate the view and light vectors in the pixel shader. There is another solution though: calculate the view and light vectors in the vertex shader as previously but do not normalise them in the vertex shader only in the pixel shader. That way we can still calculate the view/light vector in the vertex shader (which is cheaper) and get correct specular reflections on large triagles.

Hi, nice catch.

In the code you only normalize the view vector. So only this has to be left unnormalized.

In essence the normalized vs unnormalozed view vector are the same vectors. so you say that because the unnormalized one has larger values the GPU barycentric algorithm does not feature artifacts?

Which means that depending on the implementation AMD/Nvidia/DirectX/OpenGL we might get different results?

The vertex shader, as produced by the fx composer template only normalizes one of the vectors, but either normalized will cause this artifact on large triangles. Both should be left unnormalised to get the correct results. My test was on NVidia/Direct3d 9 but it should be the same for other GPUs/Apis. It is not the same thing interpolating unnormalised vs normalized versions of the view/light vectors. Think of it as interpolating the adjacent sides of a triangle vs interpolating normalized vectors (or colors or any other attribute with no notion of location).