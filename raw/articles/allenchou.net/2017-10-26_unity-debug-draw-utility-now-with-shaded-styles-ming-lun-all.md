---
title: Unity Debug Draw Utility – Now with Shaded Styles | Ming-Lun "Allen" Chou |
  周明倫
url: https://allenchou.net/2017/10/unity-debug-draw-utility-now-with-shaded-styles/
author: Allen Chou
published: '2017-10-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

Complete source code for the debug draw utility and Unity scene for generating the demo animation above can be found on [GitHub](https://github.com/TheAllenChou/unity-cj-lib). Here is a [shortcut](https://github.com/TheAllenChou/unity-cj-lib/blob/master/src/Assets/CjLib/DebugUtil.cs) to the debug draw utility class. And here is a [shortcut](https://github.com/TheAllenChou/unity-cj-lib/tree/master/src/Assets/CjLib/Shader) to the shaders.

### Debug Draw Upgraded

A couple weeks ago, I [documented](http://allenchou.net/2017/09/debug-draw-with-cached-meshes-vertex-shaders-in-unity/) how I implemented a wireframe Unity debug draw utility using cached mesh pools and vertex shaders.

Recently, I have upgraded the utility to now support various shaded styles, including solid color, flat-shaded, and smooth-shaded. This post is a documentation of my development process and how I solved some of the challenges on the way.


### Extending The Mesh Factory

For each mesh rendered in wireframe style, the original [mesh factory](https://github.com/TheAllenChou/unity-cj-lib/blob/master/src/Assets/CjLib/PrimitiveMeshFactory.cs) only needed to generate an array of unique vertices, along with an index array containing the vertex indices in either lines or line strip topology.

To generate a mesh to be rendered in solid color style, I reused the same unique vertex arrays, but the index arrays hadto be changed to contain vertex indices in triangle topology, three indices per triangle.

Once the generation of meshes for solid color style was done, I decided counter-intuitively to first implement the “fancier” smooth-shaded style before the flat-shaded style, because the former was actually an easier incremental change from the solid color style. Taking spheres for example, the vertex array actually still didn’t need to be changed; I just had to create an array of normals that is the exact copy of the vertices. Recall from the [previous post](http://allenchou.net/2017/09/debug-draw-with-cached-meshes-vertex-shaders-in-unity/) that in order to reduce numbers of cached meshes, I offloaded scaling to the vertex shaders and just generated meshes that are unit primitives. The normal of a vertex of a smooth-shaded unit sphere is just conveniently identical to the vertex positional vector.

Figuring out the index arrays for other smooth-shaded primitive meshes wasn’t as straightforward as spheres, but it wasn’t too hard either. I still didn’t need to change most of the vertex arrays and just had to figure out the proper accompanying normal array and index array. Cones were a notable exception, because even with smooth-shaded style, they still have some normal discontinuity along the base edges, which required duplicates of the base edge vertices with different normals.

Finally moving onto the flat-shaded style, most primitives required me to modify the generation of vertex arrays, normal arrays, and index arrays. Arrays of unique vertices no longer worked, because a vertex shared by multiple faces (triangles, quads, circles, etc.) would have a different normal on each face. For each face, a new set of vertices had to be put into the vertex array. Different primitives required slightly different techniques to generate the vertices for each face. Taking spheres for example again, for each longitudinal strip, two triangles connecting to the poles plus two triangles per quad along the strip were needed. The normals were simply computed with cross products of any two non-parallel vectors connecting vertices in each face.

I generally followed this pattern for triangles:

Vector3[] aVert = new Vector3[numVerts]; Vector3[] aNormal = new Vector3[numNormals]; int[] aIndex = new int[numIndices]; int iVert = 0; int iNormal = 0; int iIndex = 0; for (int i = 0; i < numIterations; ++i) { int iTriStart = iVert; aVert[iVert++] = ComputeTriVert0(i); aVert[iVert++] = ComputeTriVert1(i); aVert[iVert++] = ComputeTriVert2(i); Vector3 tri01 = aVert[iTriStart + 1] - aVert[iTriStart]; Vector3 tri02 = aVert[iTriStart + 2] - aVert[iTriStart]; Vector3 triNormal = Vector3.Cross(tri01, tri02).normalized; aNormal[iNormal++] = triNormal; aNormal[iNormal++] = triNormal; aNormal[iNormal++] = triNormal; aIndex[iIndex++] = iTriStart; aIndex[iIndex++] = iTriStart + 1; aIndex[iIndex++] = iTriStart + 2; }

And this pattern for quads:

Vector3[] aVert = new Vector3[numVerts]; Vector3[] aNormal = new Vector3[numNormals]; int[] aIndex = new int[numIndices]; int iVert = 0; int iNormal = 0; int iIndex = 0; for (int i = 0; i < numIterations; ++i) { int iQuadStart = iVert; aVert[iVert++] = ComputeQuadVert0(i); aVert[iVert++] = ComputeQuadVert1(i); aVert[iVert++] = ComputeQuadVert2(i); aVert[iVert++] = ComputeQuadVert3(i); Vector3 quad01 = aVert[iQuadStart + 1] - aVert[iQuadStart]; Vector3 quad02 = aVert[iQuadStart + 2] - aVert[iQuadStart]; Vector3 quadNormal = Vector3.Cross(quad01, quad02).normalized; aNormal[iNormal++] = quadNormal; aNormal[iNormal++] = quadNormal; aNormal[iNormal++] = quadNormal; aNormal[iNormal++] = quadNormal; aIndex[iIndex++] = iQuadStart; aIndex[iIndex++] = iQuadStart + 1; aIndex[iIndex++] = iQuadStart + 2; aIndex[iIndex++] = iQuadStart; aIndex[iIndex++] = iQuadStart + 2; aIndex[iIndex++] = iQuadStart + 3; }

### The Shaders

The positional portion of the vertex shader for all styles is actually identical, so I wanted to find a way to avoid creating an extra set of vertex and fragment shaders just in order to add the logic for normals. Then I found out about Unity’s [shader variant](https://docs.unity3d.com/Manual/SL-MultipleProgramVariants.html) feature. By using the `shader_feature`

keyword and `#ifdef`

‘s in the shaders, combined with the `Material.EnableKeyword`

method, I was able to choose from a collection of variants generated from a single [master shader](https://github.com/TheAllenChou/unity-cj-lib/blob/master/src/Assets/CjLib/Shader/PrimitiveCore.cginc) at run time for each primitive mesh type. I used the `NORMAL_ON`

keyword for the normal feature.

As shown below, only when the `NORMAL_ON`

keyword is enabled are normals included in the vertex structs.

#pragma shader_feature NORMAL_ON struct appdata { float4 vertex : POSITION; #ifdef NORMAL_ON float3 normal : NORMAL; #endif }; struct v2f { float4 vertex : SV_POSITION; #ifdef NORMAL_ON float3 normal : NORMAL; #endif };

The model-view matrix is used to transform vertex positions from object space into view space, but normals need to be transformed using the [inverse transpose of the model-view matrix](https://paroj.github.io/gltut/Illumination/Tut09%20Normal%20Transformation.html). Since the scaling is offloaded to the shader, I needed to fold in the scaling portion of the inverse transpose of the model-view matrix myself.

v2f vert (appdata v) { v2f o; // ... #ifdef NORMAL_ON float4x4 scaleInverseTranspose = float4x4 ( 1.0f / _Dimensions.x, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f / _Dimensions.y, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f / _Dimensions.z, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f ); float4x4 m = mul(UNITY_MATRIX_IT_MV, scaleInverseTranspose); o.normal = mul(m, float4(v.normal, 0.0f)).xyz; #endif return o; }

I also used the `shader_feature`

keyword to optionally activate the “cap shift/scaling” logic for cylinders and capsules. Recall from the [previous post](http://allenchou.net/2017/09/debug-draw-with-cached-meshes-vertex-shaders-in-unity/) that in order not to generate a mesh for each possible height, only unit-height cylinder and capsule meshes are generated, and the caps are shifted towards the X-Z plane, scaled, and then shifted back to the final height. I used the `CAP_SHIFT_SCALE`

keyword for this feature.

#pragma shader_feature CAP_SHIFT_SCALE // (x, y, z) == (dimensionX, dimensionY, dimensionZ) // w == capShiftScale // shifts 0.5 towards X-Z plane, scale by dimensions, // and then shoft back 0.5 * capShiftScale) float4 _Dimensions; v2f vert (appdata v) { v2f o; #ifdef CAP_SHIFT_SCALE const float ySign = sign(v.vertex.y); v.vertex.y -= ySign * 0.5f; #endif v.vertex.xyz *= _Dimensions.xyz; #ifdef CAP_SHIFT_SCALE v.vertex.y += ySign * 0.5f * _Dimensions.w; #endif o.vertex = UnityObjectToClipPos(v.vertex); // ... return o; }

I noticed some Z-fighting between the two styles when I drew the same meshes twice, once in wireframe style and once in shaded style. It was actually an easy fix. I just added a small Z-bias to make sure the wireframe lines are always drawn in front of the shaded pixels.

float _ZBias; v2f vert (appdata v) { v2f o; // ... o.vertex = UnityObjectToClipPos(v.vertex); o.vertex.z += _ZBias; // ... return 0; }

And finally here’s the fragment shader. It really doesn’t contain anything out of the ordinary, except that it remaps the vertex brightness from (0.0, 1.0) to (0.3, 1.0), because I really don’t like completely black pixels.

fixed4 frag (v2f i) : SV_Target { fixed4 color = _Color; #ifdef NORMAL_ON i.normal = normalize(i.normal); color.rgb *= 0.7f * i.normal.z + 0.3f; // darkest at 0.3f #endif return color; }

### Conclusion

That’s it! I am pretty satisfied with the current Unity debug draw utility. It’s also easy to combine primitives to make more interesting shapes, such as the arrows shown in the demo animation above.

Potentially, the meshes for flat-shaded and smooth-shaded styles, generated from the mesh factory, can be used to implement a [gizmo](https://docs.unity3d.com/ScriptReference/Gizmos.html) utility. But I’ll probably only do it when I really need it.

Stay tuned for more documentation of my future venture into Unity land.

Until next time!