---
title: Screen Space Ambient Occlusion
url: https://anki3d.org/screen-space-ambient-occlusion/
author: Panagiotis Christopoulos Charitos
published: '2011-04-18'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

“Ambient occlusion is a shading method used in 3D computer graphics which helps add realism to local reflection models by taking into account attenuation of light due to occlusion” [Wikipedia.org]

The proper way to do ambient occlusion is very expensive for today’s hardware and especially without the use of a ray-tracing renderer. For that reason a few new techniques developed that tried to produce the same result using simpler and faster algorithms. One of these approaches is the Screen Space Ambient Occlusion (aka SSAO) that makes the calculations of ambient occlusion in 2D space just like a normal 2D filter. This article will not go deep into what SSAO is, there are many great readings around the web that cover the theory behind SSAO, in this article we will jump into the implementation that AnKi uses.

There are quite a few techniques to produce SSAO, a top level way to group them is from the resources they need to produce the SSAO:

- Some use just the depth buffer (Amnesia, Aliens VS Predator)
- others use the depth buffer and the normal buffer (Crysis,
[gamerendering article](http://www.gamerendering.com/2009/01/14/ssao/)) - and others use the pixel position and the normal buffer (
[gamedev article](http://www.gamedev.net/page/resources/_/reference/programming/140/lighting-and-shading/a-simple-and-practical-approach-to-ssao-r2753))

AnKi used to implement the second technique for quite some time. The results were good but apparently not that good, so for the past couple of weeks I’ve tried to implement the third technique by reading [this](http://www.gamedev.net/page/resources/_/reference/programming/140/lighting-and-shading/a-simple-and-practical-approach-to-ssao-r2753) great article from gamedev. The present article extends the gamedev one by adding a few optimization tips and by presenting the code in GLSL.

Bellow you can see the old and the new SSAO, rendered at the half of the original rendering size with two blurring passes.

![ssao-old](https://anki3d.org/wp-content/uploads/2011/04/ssao-old-300x168.jpg)


![ssao-old](https://anki3d.org/wp-content/uploads/2011/04/ssao-old-300x168.jpg)

![ssao-new](https://anki3d.org/wp-content/uploads/2011/04/ssao-new-300x168.jpg)


![ssao-new](https://anki3d.org/wp-content/uploads/2011/04/ssao-new-300x168.jpg)

![anki-full](https://anki3d.org/wp-content/uploads/2011/04/screenshot-300x168.jpg)


![anki-full](https://anki3d.org/wp-content/uploads/2011/04/screenshot-300x168.jpg)


In order to produce the SSAO factor we need practically tree variables for every fragment, the first is the position of the fragment in view or world space (view space in our case), the normal of that fragment and a random vector that we obtain using a noise texture. The fact that AnKi uses a deferred shading renderer gives us the normals of the scene in a texture. The gamedev article suggests that we need to have the view space positions stored in a texture but in AnKi we don’t do that for any reason. Its very expensive to store the position in a texture and for that reason we use a few techniques to obtain the position from the depth buffer.

To obtain the fragment position in view space using the fragments depth we do:

vec3 getPosition(in vec2 uv) { float depth = texture2D(depthTexture, uv).r; vec3 fragPosVspace; fragPosVspace.z = -planes.y / (planes.x + depth); fragPosVspace.xy = (((uv) * 2.0) - 1.0) * limitsOfNearPlane; float sc = -fragPosVspace.z / zNear; fragPosVspace.xy *= sc; return fragPosVspace; }

The variables:

**uv**: The texture coordinates to read from

**depthTexture**: The texture that stores the depth

**zNear**: Camera’s near plane

**zFar**: Camera’s far plane

**planes**: This is an optimization that we use to calculate the fragment’s z. The original and unoptimized code that gives the z is given by:

fragPosVspace.z = -zNear / (zFar - (depth * (zFar - zNear))) * zFar;

if we do a few calculations we can isolate two expressions that can be pre-calculated in the CPU and then passed as uniforms in the shader. The planes 2D vector is (C++):

planes.x() = zFar / (zNear - zFar); planes.y() = (zFar * zNear) / (zNear -zFar);

**limitsOfNearPlane**: This is a 2D vector that keeps the limits of the right and top eye vector (C++):

limitsOfNearPlane.y() = zNear * tan(0.5 * fovY); limitsOfNearPlane.x() = limitsOfNearPlane.y() * (fovX / fovY);

fovX is the horizontal angle (imagine the cam positioned in the default OGL pos). Note that fovX > fovY in the classic resolutions where the width > height

As may have already noticed by now the getPosition is used to calculate the position using a perspective camera.

The SSAO vertex shader:

layout(location = 0) in vec2 position; out vec2 vTexCoords; layout(location = 0) in vec2 position; out vec2 vTexCoords; void main() { vec2 vertPos = position; vTexCoords = vertPos; vec2 vertPosNdc = vertPos * 2.0 - 1.0; gl_Position = vec4(vertPosNdc, 0.0, 1.0); }

The **position** is the vertex coordinates of the quad, the coordinates are: {1.0, 1.0}, {0.0, 1.0}, {0.0, 0.0}, {1.0, 0.0}. The values are pretty easy to digest and they help to calculate the texture coordinates. With this way we don’t pass a separate vertex attribute for the texture coordinates.

Fragment shader:

/// @name Uniforms /// @{ uniform vec2 planes; ///< for the calculation of frag pos in view space uniform vec2 limitsOfNearPlane; ///< for the calculation of frag pos in view space uniform float zNear; ///< for the calculation of frag pos in view space uniform sampler2D msDepthFai; ///< for the calculation of frag pos in view space uniform sampler2D noiseMap; /// Used in getRandom uniform float noiseMapSize = 100.0; /// Used in getRandom uniform vec2 screenSize; /// Used in getRandom uniform sampler2D msNormalFai; /// Used in getNormal /// @} /// @name Varyings /// @{ in vec2 vTexCoords; /// @} /// @name Output /// @{ layout(location = 0) out float fColor; /// @} /// @name Consts /// @{ uniform float SAMPLE_RAD = 0.1; /// Used in main uniform float SCALE = 1.0; /// Used in doAmbientOcclusion uniform float INTENSITY = 3.0; /// Used in doAmbientOcclusion uniform float BIAS = 0.00; /// Used in doAmbientOcclusion /// @} /// globals: msNormalFai vec3 getNormal(in vec2 uv) { return unpackNormal(texture2D(msNormalFai, uv).rg); } /// globals: noiseMap, screenSize, noiseMapSize vec2 getRandom(in vec2 uv) { return normalize(texture2D(noiseMap, screenSize * uv / noiseMapSize).xy * 2.0 - 1.0); } /// Get frag position in view space /// globals: msDepthFai, planes, zNear, limitsOfNearPlane vec3 getPosition(in vec2 uv) { float depth = texture2D(msDepthFai, uv).r; vec3 fragPosVspace; fragPosVspace.z = -planes.y / (planes.x + depth); fragPosVspace.xy = (((uv) * 2.0) - 1.0) * limitsOfNearPlane; float sc = -fragPosVspace.z / zNear; fragPosVspace.xy *= sc; return fragPosVspace; } /// Calculate the ambient occlusion factor float doAmbientOcclusion(in vec2 tcoord, in vec2 uv, in vec3 original, in vec3 cnorm) { vec3 newp = getPosition(tcoord + uv); vec3 diff = newp - original; vec3 v = normalize(diff); float d = length(diff) /* * SCALE*/; float ret = max(0.0, dot(cnorm, v) /* - BIAS*/) * (INTENSITY / (1.0 + d)); return ret; } void main(void) { const vec2 KERNEL[16] = vec2[](vec2(0.53812504, 0.18565957), vec2(0.13790712, 0.24864247), vec2(0.33715037, 0.56794053), vec2(-0.6999805, -0.04511441), vec2(0.06896307, -0.15983082), vec2(0.056099437, 0.006954967), vec2(-0.014653638, 0.14027752), vec2(0.010019933, -0.1924225), vec2(-0.35775623, -0.5301969), vec2(-0.3169221, 0.106360726), vec2(0.010350345, -0.58698344), vec2(-0.08972908, -0.49408212), vec2(0.7119986, -0.0154690035), vec2(-0.053382345, 0.059675813), vec2(0.035267662, -0.063188605), vec2(-0.47761092, 0.2847911)); vec3 p = getPosition(vTexCoords); vec3 n = getNormal(vTexCoords); vec2 rand = getRandom(vTexCoords); fColor = 0.0; const int ITERATIONS = 16; for(int j = 0; j < ITERATIONS; ++j) { vec2 coord = reflect(KERNEL[j], rand) * SAMPLE_RAD; fColor += doAmbientOcclusion(vTexCoords, coord, p, n); } fColor = 1.0 - fColor / ITERATIONS; }

- The
**noiseMapSize**is the size of the noise map. The width and height of the noise map is the same - The
**screenSize**is the width and height of the window. This value is not that relevant and it doesn’t affect the result that much - The
**KERNEL**is a number of 2D coordinates that form a circle around (0, 0) and we use them for sampling - The
**unpackNormal**is a function that unpacks the normal from two 16bit floats, dont be alerted by this function its internal