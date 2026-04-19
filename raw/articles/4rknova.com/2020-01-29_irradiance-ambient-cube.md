---
title: Irradiance, Ambient Cube
url: https://www.4rknova.com/blog/2020/01/29/ambient-cubes
author: Nikolaos Papadopoulos
published: '2020-01-29'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Radiosity Normal Mapping

Traditional light mapping involves baking a fixed irradiance value based on static geometry and lighting. This fixed value cannot be combined with directional data stored in surface textures such as normal maps. This limitation creates a flat appearance in shadowed areas and visible discontinuities when transitioning between lit and shaded surfaces.

To enable the use of normal maps with light maps in Half Life 2, Valve enhanced their lightmap baking tool (vrad) [5]. Their approach calculates three lightmap values, each corresponding to one of the orthonormal basis vectors that represent the hemisphere above the surface. During runtime, the irradiance value is determined by the cosine of the angle between the normal map direction and the three basis vectors

. While this technique is effective for static geometry, it does not scale well for dynamic objects

[[4]](https://www.4rknova.com#REF-4)

[[1]](https://www.4rknova.com#REF-1)

[[2]](https://www.4rknova.com#REF-2).

[[4]](https://www.4rknova.com#REF-4)# The Ambient Cube

Taking it a step further, they extended their hemispherical lightmap basis into a full spherical basis formed by 6 orthogonal basis vectors that coincide with the 6 face directions of a unit cube. This basis is called an “Ambient Cube”.

![01](../../assets/c23a590ee163c9f7.png)


Source engine calculates a sparse irradiance volume[REF:3] encapsulating a set of lighting probes placed across the environments. Those probes provide directional ambient illumination in addition to a small number of local analytical lights for characters [REF:2].

## Calculating the Ambient Cube Values

In my Shadertoy implementation I use a very simple approach that samples the highest cubemap LOD per basis axis, essentially averaging the values for the corresponding cube face.

```
vec3 cAmbientCube[6] = vec3[](
textureLod(iChannel0, vec3( 1, 0, 0), 1e10).xyz
, textureLod(iChannel0, vec3(-1, 0, 0), 1e10).xyz
, textureLod(iChannel0, vec3( 0, 1, 0), 1e10).xyz
, textureLod(iChannel0, vec3( 0,-1, 0), 1e10).xyz
, textureLod(iChannel0, vec3( 0, 0, 1), 1e10).xyz
, textureLod(iChannel0, vec3( 0, 0,-1), 1e10).xyz
};
```


## Evaluation

The ambient cube evaluation is distilled to a simple weighted blending of six RGB values, based on a world space normal of the surface receiving the light.

```
float3 AmbientLight( const float3 worldNormal )
{
float3 nSquared = worldNormal * worldNormal;
int3 isNegative = ( worldNormal < 0.0 );
return nSquared.x * cAmbientCube[isNegative.x ]
+ nSquared.y * cAmbientCube[isNegative.y+2]
+ nSquared.z * cAmbientCube[isNegative.z+4];
}
```


# Demo

This is what it looks like when we put it all together:

# Considerations

Encoding irradiance using ambient cubes results in a very crude approximation of the original signal, however the computational cost of evaluation is exceptionally low.