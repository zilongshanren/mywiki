---
title: Raindrops on a puddle
url: https://www.4rknova.com/blog/2026/02/08/raindrops-on-puddle
author: Nikolaos Papadopoulos
published: '2026-02-08'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Rain has a mesmerizing quality when it hits water. Each droplet creates expanding ripples that interfere with one another, forming complex, organic patterns. In this post, I’ll walk through how to simulate this effect in real time using a two-pass shader technique that combines wave propagation physics with ray marching and realistic reflections.

The result is an interactive puddle where you can control the rain intensity, drop count, reflectivity, and other parameters to create different moods and effects.

# Overview

The simulation consists of two main components:

**Wave Propagation (Buffer A)**: A 2D wave equation simulates how ripples spread across the water surface. Multiple raindrops are procedurally generated at random positions and intervals, each creating a disturbance that propagates outward with damping over time.**Scene Rendering (Image Pass)**: The ripple data modulates the height of a 3D puddle surface. Ray marching renders the scene with proper normals calculated from the height field. Fresnel effects make the water more reflective at grazing angles, and an environment cubemap provides realistic reflections of the surrounding sky.

The key insight is that we don’t need to simulate 3D fluid dynamics. A 2D wave equation running on the GPU provides convincing results at 60fps, and the ray marched rendering adds the 3D perspective and lighting that makes it feel like a real puddle.

# Buffer A: Wave Propagation

The first pass simulates water ripples using a discrete approximation of the 2D wave equation. This is stored in a texture that feeds back into itself each frame, creating a continuous simulation.

## The Wave Equation

The wave equation describes how disturbances propagate through a medium. In 2D, it looks like this:

\[\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)\]Where \(u(x,y,t)\) is the height of the water surface at position \((x,y)\) and time \(t\), and \(c\) is the wave propagation speed.

For real-time simulation, we use a discrete approximation. By sampling the neighboring pixels and applying finite differences, we can compute how the current pixel should change:

```
// Macro to sample neighbor pixels from the wave buffer
#define S(e) (texture(iChannel0, p+e).x)
// Convert pixel coordinates to normalized UV [0,1]
vec2 p = gl_FragCoord.xy / iResolution.xy;
// Read current state: red=current height, green=previous height
vec4 c = texture(iChannel0, p);
// Calculate offset for neighbor sampling in UV space
vec3 e = vec3(vec2(STEP)/iResolution.xy, 0.);
// Sample center and 4 neighbors (forms a + pattern)
float s0 = c.y; // Previous state (center)
float s1 = S(-e.zy); // Left neighbor
float s2 = S(-e.xz); // Down neighbor
float s3 = S(e.xz); // Right neighbor
float s4 = S(e.zy); // Up neighbor
// Discrete wave equation: velocity term + Laplacian
// -(s0 - 0.5) * 2.0 = negative of previous velocity
// (s1 + s2 + s3 + s4 - 2.0) = discrete Laplacian
float d = -(s0 - 0.5) * 2.0 + (s1 + s2 + s3 + s4 - 2.0);
```


This calculates the Laplacian (second spatial derivative) by summing the four neighboring values and subtracting the center value. The previous state `s0`

provides the time derivative needed for wave propagation.

## Damping

Real water ripples don’t propagate forever. Energy dissipates due to viscosity, surface tension, and other effects. We model this with a simple damping factor:

```
// Apply damping to gradually reduce wave amplitude
// Values like 0.99 cause slow fadeout, 0.95 causes faster fadeout
d *= uDamping;
```


A value slightly less than 1.0 causes ripples to gradually fade away, preventing the simulation from becoming chaotic over time.

## Generating Raindrops

Multiple raindrops are generated procedurally using hash functions for pseudo-random positions. Each raindrop appears at a different time offset to create a continuous rainfall effect:

```
// Hash function: generates pseudo-random 2D vector from 2D input
// Uses fractional sine/dot products for randomness
vec2 hash22(vec2 p)
{
// Expand to 3D and take fractional part (creates distribution)
vec3 p3 = fract(vec3(p.xyx) * vec3(.1031, .1030, .0973));
// Mix components using dot product (increases randomness)
p3 += dot(p3, p3.yzx + 33.33);
// Return fractional part of product (final randomization)
return fract((p3.xx + p3.yz) * p3.zy);
}
void getRaindrops(out vec3 drops[MAX_DROPS], int count)
{
// Scale time by rain speed
float t = iTime * uRainSpeed;
// Floor creates discrete time intervals (drops regenerate here)
float baseTime = floor(t);
for (int i = 0; i < MAX_DROPS; i++) {
// Deactivate drops beyond the requested count
if (i >= count) {
drops[i] = vec3(0.0, 0.0, 0.0);
continue;
}
// Unique time offset for each drop (prevents synchronization)
float offset = float(i) * 0.3711;
// Create seed from time + drop index
vec2 seed = vec2(baseTime + offset, float(i) * 17.3);
// Hash seed to get random screen position
vec2 pos = hash22(seed) * iResolution.xy;
// Randomize drop strength (0.5 to 1.0 range)
float strength = uDropIntensity * (0.5 + 0.5 * hash12(seed + 1.0));
// Create smooth pulse: ramps up, stays active, ramps down
float pulse = fract(t + offset * 0.7);
// Combine two smoothsteps to create bell curve activation
float activation = smoothstep(0.0, 0.15, pulse) *
smoothstep(0.35, 0.2, pulse);
// Store position (xy) and activated strength (z)
drops[i] = vec3(pos, strength * activation);
}
}
```


The hash functions ensure each raindrop appears at a unique, random location within each time interval. The `activation`

term creates a smooth pulse that makes drops appear and disappear naturally. Each drop adds a disturbance to the wave field at its location:

```
// Apply each active raindrop as a localized disturbance
for (int i = 0; i < MAX_DROPS; i++) {
if (i >= uDropCount) break;
// Only process drops with meaningful activation
if (drops[i].z > 0.01) {
// Calculate distance from this pixel to drop center
float dist = length(drops[i].xy - gl_FragCoord.xy);
// Add circular disturbance with smooth falloff
// Full strength at dist=0.5, fades to zero at dist=4.0
d += drops[i].z * smoothstep(4.0, 0.5, dist);
}
}
```


The `smoothstep`

creates a localized impact zone. Drops don’t affect the entire surface instantaneously but rather create a small initial disturbance that then propagates outward via the wave equation.

## State Storage

The shader stores both the current and previous state in the texture’s red and green channels:

```
// Remap wave value from [-0.5, 0.5] to [0, 1] for texture storage
d = d * 0.5 + 0.5;
// Store in buffer: red=new state, green=old state (double buffering)
// Next frame: red becomes current, green becomes previous
fragColor = vec4(d, c.x, 0, 0);
```


This double-buffering technique is essential for the wave equation, which needs to know both the current value and the previous value to compute the next timestep.

# Image Pass: Scene Rendering

The second pass renders the actual 3D puddle using the ripple data from Buffer A. This is where ray marching, lighting, and reflections come together.

## Ray Marching Setup

Ray marching is a rendering technique where we step along a ray from the camera until we hit a surface. For each pixel, we generate a ray and march it through the scene.

The scene is set up with the camera positioned at (20, 18, 14), elevated and offset from the puddle center. It looks toward a target point at (-6, -4, 10), which is slightly below the horizon and offset from the puddle origin. This angled view creates a natural perspective where we can see both the water surface and its reflections. The puddle itself is modeled as a box with dimensions 84x10x84 units, centered at the world origin. The top surface of this box is displaced vertically by the wave height data from Buffer A, creating the ripple geometry. This setup gives us an oblique view of the puddle that emphasizes the ripple patterns and their reflections.

```
// Camera: position, target, up vector
struct Camera { vec3 p, t, u; };
// Ray: origin, direction
struct Ray { vec3 o, d; };
// Set up camera for puddle scene
Camera c;
c.p = vec3(20, 18, 14); // Position: elevated and to the side
c.t = vec3(-6, -4, 10); // Target: puddle center, below horizon
c.u = vec3(0, 1, 0); // Up: positive Y axis
// Generate ray for this pixel through the camera
Ray r;
generate_ray(uv, c, r);
```


The `generate_ray`

function computes a ray direction based on the pixel coordinates and camera parameters, taking into account the field of view.

## Distance Function

The core of ray marching is the signed distance function (SDF), which tells us how far we are from the nearest surface. For the puddle, we sample the ripple texture and use it to modulate the height of a box:

```
// Signed distance to puddle surface (displaced box)
float scene_distance(vec3 p)
{
// Convert world XZ position to texture UV [0,1]
vec2 uv = 0.5 * (p.xz / SIZE + 1.);
// Sample wave height from Buffer A
vec3 res = texture(iChannel0, uv).xyz;
// Extract height from green channel
float d = dot(res, vec3(0, 1, 0));
// Return distance to box displaced by wave height
// The wave height modulates the top surface
return deu_box(p + vec3(0, d, 0), vec3(SIZE, 5, SIZE));
}
```


The height value from the ripple buffer displaces the surface vertically, creating the ripple geometry. The ray marcher steps along each ray until it finds a point where the distance is below a threshold:

```
// Ray marching: steps along ray until hitting surface
// Returns true if surface found, outputs hit position, normal, iterations
bool rmarch(Ray r, out vec3 p, out vec3 n, out int iter)
{
// Start at ray origin
p = r.o;
vec3 pos = p;
// Initialize distance to something > 0
float d = 1.;
// March up to MAX_STEPS times
for (int i = 0; i < RMARCH_MAX_STEPS; i++) {
// Track iteration count for debugging/optimization
iter = i;
// Query distance to nearest surface at current position
d = scene_distance(pos);
// Surface hit: distance below threshold
if (d < EPSILON) {
p = pos; // Store final hit position
break; // Early exit on hit
}
// Safe to step forward by distance d (sphere tracing)
// Won't overshoot because d tells us the closest surface
pos += d * r.d;
}
// Calculate surface normal at hit point
n = scene_normal(p, d);
// Return true if we actually hit something
return d < EPSILON;
}
```


## Normal Calculation

To properly light the surface, we need accurate normals. These are calculated by sampling the height field in four directions and computing the gradient:

```
// Calculate surface normal from height field gradient
vec3 scene_normal(vec3 pos, float d)
{
// Convert world position to texture UV
vec2 uv = 0.5 * (pos.xz / SIZE + 1.);
// Size of one texel in UV space
vec2 texelSize = 1.0 / iResolution.xy;
// Sample wave heights at 4 neighbors (left, right, down, up)
// Green channel contains current wave height
float hL = texture(iChannel0, uv - vec2(texelSize.x, 0)).y;
float hR = texture(iChannel0, uv + vec2(texelSize.x, 0)).y;
float hD = texture(iChannel0, uv - vec2(0, texelSize.y)).y;
float hU = texture(iChannel0, uv + vec2(0, texelSize.y)).y;
// Compute gradient using central differences
// Gradient = (dh/dx, 1, dh/dz) gives surface slope
vec3 n;
n.x = (hL - hR) * 2.5; // X slope (amplified for visibility)
n.z = (hD - hU) * 2.5; // Z slope (amplified for visibility)
n.y = 1.0; // Base upward component
// Normalize to unit length
return normalize(n);
}
```


The gradient gives us the slope of the surface, which when normalized becomes the surface normal. This is critical for accurate lighting and reflections.

## Fresnel Effect

Water exhibits strong Fresnel effects: it’s more reflective when viewed at grazing angles and more transparent when viewed from directly above. The Fresnel-Schlick approximation provides an efficient way to model this:

```
// Fresnel-Schlick approximation for reflectance
// Returns how much light reflects vs refracts at the surface
float fresnel(vec3 view, vec3 normal, float ior)
{
// f0 = reflectance at normal incidence (head-on viewing)
// For water (ior=1.333), f0 is about 0.02 (2% reflectance)
float f0 = pow((1.0 - ior) / (1.0 + ior), 2.0);
// Angle between view direction and surface normal
float cosTheta = abs(dot(view, normal));
// Schlick approximation: reflectance increases at grazing angles
// At normal: returns f0, at grazing: returns 1.0
return f0 + (1.0 - f0) * pow(1.0 - cosTheta, 5.0);
}
```


Where `ior`

is the index of refraction for water (1.333). The formula computes \(F_0\), the reflectance at normal incidence, then blends toward full reflectance at grazing angles using the \((1 - \cos\theta)^5\) term.

## Refraction and Ground Rendering

To see the ground through the water, we need to simulate refraction. When light passes from air into water, Snell’s law dictates that the ray bends according to the ratio of refractive indices:

\[n_1 \sin\theta_1 = n_2 \sin\theta_2\]GLSL provides the `refract()`

function which handles this calculation. We cast a refracted ray from the water surface and intersect it with the ground plane below the water:

```
// Cast refracted ray to find ground intersection
vec3 refrDir = refract(v, n, 1.0 / WATER_IOR); // Air to water
// Negative because ground is below water surface (y < 0)
float groundDist = intersectPlane(p, refrDir, -uPuddleDepth);
// Compute ground color at intersection point
vec3 groundPos = p + refrDir * groundDist;
groundColor = shadeGround(groundPos);
```


The `intersectPlane()`

function solves the ray-plane intersection:

```
// Find where ray hits horizontal plane at height planeY
float intersectPlane(vec3 rayOrigin, vec3 rayDir, float planeY)
{
// Ray: p = rayOrigin + t * rayDir
// Plane: y = planeY
// Solve: rayOrigin.y + t * rayDir.y = planeY
if (abs(rayDir.y) < 0.0001) return -1.0; // Parallel to plane
float t = (planeY - rayOrigin.y) / rayDir.y;
return t > 0.0 ? t : -1.0; // Only forward intersections
}
```


The ground can be rendered in two ways: a procedural checkerboard pattern or by sampling a pavement texture. This is controlled by the `uUseCheckerboard`

uniform:

```
// Shade ground with either checkerboard or texture
vec3 shadeGround(vec3 pos)
{
if (uUseCheckerboard)
{
// Procedural checkerboard pattern with user-controlled tiling
vec2 checker = floor(pos.xz * uGroundScale);
float pattern = mod(checker.x + checker.y, 2.0);
vec3 darkTile = vec3(0.15, 0.12, 0.10);
vec3 lightTile = vec3(0.25, 0.22, 0.20);
vec3 baseColor = mix(darkTile, lightTile, pattern);
// Add subtle noise for variation
float noise = fract(sin(dot(pos.xz, vec2(12.9898, 78.233))) * 43758.5453);
baseColor += (noise - 0.5) * 0.05;
return baseColor;
}
else
{
// Sample pavement texture
// Map ground XZ position to UV coordinates with tiling
vec2 uv = pos.xz * uGroundScale; // User-controlled tiling
// Sample pavement texture and convert from sRGB to linear
vec3 pavementColor = pow(texture(iChannel2, uv).xyz, vec3(2.2));
// Darken to simulate ground in shadow/water
return pavementColor * 0.6;
}
}
```


The `uGroundScale`

parameter controls the tiling for both ground modes. When using the texture mode, we sample a pavement texture (iChannel2) mapped onto the ground plane. The ground position’s XZ coordinates are used as UV coordinates, scaled by `uGroundScale`

. In checkerboard mode, the same scale parameter controls the size of the checkerboard tiles. This provides a realistic ground appearance that can be customized by replacing the pavement texture with any desired ground material (cobblestones, asphalt, dirt, etc.).

This gives us physically plausible underwater visibility, with the ground appearing distorted through the rippling water surface.

### Water Turbidity

Real water is rarely perfectly clear. Suspended particles, dissolved organic matter, and other impurities cause light to scatter and absorb as it travels through water. This is modeled using Beer’s law, which describes exponential attenuation:

\[I(d) = I_0 \cdot e^{-\alpha d}\]Where \(I_0\) is the initial light intensity, \(d\) is the distance traveled through the medium, and \(\alpha\) is the attenuation coefficient (turbidity). We apply this to the ground color:

```
// Calculate distance refracted ray travels through water
float waterDepth = groundDist;
// Apply Beer's law: exponential attenuation
// Higher turbidity = murkier water = ground fades faster
float visibility = exp(-waterDepth * uWaterTurbidity);
// Blend ground color toward water body color based on visibility
vec3 waterBodyColor = uTint;
groundColor = mix(waterBodyColor, groundColor, visibility);
```


With low turbidity (clear water), `visibility`

stays close to 1.0 and the ground remains visible. With high turbidity (murky water), `visibility`

drops quickly and the ground fades to the water’s body color. This creates a physically accurate depth-dependent fadeout where distant parts of the ground disappear into murky darkness.

### Puddle Depth

The depth of the puddle (distance from the water surface to the ground plane) is controlled by the `uPuddleDepth`

uniform. This parameter works in tandem with turbidity to control how the puddle feels:

**Shallow puddles**(2-3 units): Ground is clearly visible with minimal light attenuation, creating the appearance of a thin layer of water. Even with some turbidity, details remain sharp.**Medium puddles**(5-8 units): Offers a good balance between seeing the ground and maintaining a sense of depth. Turbidity has noticeable effects at this depth.**Deep puddles**(10-20 units): Combined with turbidity, these create the appearance of deep water where the ground fades into darkness. High turbidity at these depths can make the ground completely invisible, like looking into murky pond water.

The ground plane position is passed to `intersectPlane()`

as `-uPuddleDepth`

(negative because the ground is below the water surface at y < 0). Changing this value effectively moves the ground plane up or down, controlling how far refracted light rays must travel through the water before hitting the bottom.

## Shading

The final shading combines ground color with environment reflections, modulated by the Fresnel term:

```
// Shade water surface with reflections
vec3 scene_shade(vec3 v, vec3 p, vec3 n)
{
// Calculate Fresnel: water reflects more at grazing angles
float F = fresnel(v, n, WATER_IOR);
// Sample environment reflection
vec3 reflDir = reflect(v, n); // Mirror view around normal
// Rotate environment and convert from sRGB to linear color space
vec3 rotatedReflDir = rotateY(reflDir, uEnvRotation);
vec3 reflColor = pow(texture(iChannel1, rotatedReflDir).xyz, vec3(2.2));
// Compute refracted ray and trace to ground
vec3 refrDir = refract(v, n, 1.0 / WATER_IOR);
// Ground plane depth is user-controllable
float groundDist = intersectPlane(p, refrDir, -uPuddleDepth);
vec3 groundColor;
if (groundDist > 0.0) {
// Ray hits ground - shade at intersection point
vec3 groundPos = p + refrDir * groundDist;
groundColor = shadeGround(groundPos);
// Apply water turbidity (Beer's law - exponential attenuation)
float waterDepth = groundDist;
float visibility = exp(-waterDepth * uWaterTurbidity);
vec3 waterBodyColor = uTint;
groundColor = mix(waterBodyColor, groundColor, visibility);
// Filter ground color through water tint (colored water effect)
groundColor *= 0.7 * (vec3(1.0) - uTint * 0.5);
} else {
// Fallback (rare): use dark tint
groundColor = uTint * 0.3;
}
// Blend ground and reflection based on Fresnel + user control
// Higher uReflectivity = more mirror-like water
float reflMix = mix(0.3, 0.8, uReflectivity);
vec3 col = mix(groundColor, reflColor, F * (reflMix - 0.3) + 0.3);
// Add water body color (intrinsic tint of the water itself)
col += uTint * 0.15 * (1.0 - F);
return col;
}
```


The shading combines both reflection and refraction. The `reflect()`

function computes the mirrored view direction for sampling the environment cubemap (rotated by `uEnvRotation`

for artistic control), while the `refract()`

function bends the ray through the water to show the ground underneath. The Fresnel term controls the balance: at grazing angles we see mostly reflection (sky), while looking straight down shows mostly refraction (ground).

The `uTint`

parameter provides water coloration in two ways: it acts as a color filter for light passing through the water (affecting the ground visibility), and adds an intrinsic body color to the water itself. This allows us to simulate anything from clear water (black tint) to murky green or brown puddles.

## Atmospheric Effects

To add depth and atmosphere, the shader applies fog and vignette:

```
// Apply exponential depth fog for atmospheric perspective
float depth = length(sp - c.p); // Distance from camera to surface
float fog = exp(-depth * uFogDepth); // Exponential falloff
col = mix(col * 0.7, col, fog); // Blend to darkened color
// Apply vignette (darken edges of screen)
vec2 vigUV = fragCoord.xy / iResolution.xy; // Normalized coords
float vig = 1.0 - uVignette * length(vigUV - 0.5); // Radial falloff
col *= vig; // Darken by vignette factor
```


The exponential fog darkens distant parts of the scene, while the vignette darkens the edges of the screen, drawing focus to the center.

## Gamma Correction

Finally, the output is gamma corrected for proper display:

```
// Gamma correction: convert linear to sRGB for display
// 0.4545 ≈ 1/2.2 (inverse of standard monitor gamma)
col = pow(col, vec3(0.4545));
```


Most displays expect gamma-encoded colors. Without this correction, the image would appear washed out.

# Parameter Controls

The demo exposes several uniforms that allow to customize the effect:

| Parameter | Effect |
|---|---|
`uDropCount` | Number of simultaneous raindrops (1-10) |
`uDropIntensity` | Strength of each raindrop impact |
`uRainSpeed` | How quickly new drops appear |
`uDamping` | How fast ripples fade (0.95-0.999) |
`uReflectivity` | How much the water reflects vs shows ground color |
`uVignette` | Edge darkening strength |
`uFogDepth` | Distance fog intensity |
`uEnvRotation` | Rotate environment cubemap (0-2π radians) |
`uUseCheckerboard` | Toggle between checkerboard and pavement texture |
`uGroundScale` | Ground texture tiling (lower = more zoomed out) |
`uWaterTurbidity` | Water murkiness (0=clear, higher=murky) |
`uPuddleDepth` | Distance to ground plane (2=shallow, 20=deep) |
`uTint` | Base color of the puddle water |

These parameters give artistic control over the mood and appearance of the scene. High reflectivity and low damping create energetic, mirror-like water, while lower values give a calmer, muddier puddle.

# Performance Considerations

This technique should run at 60fps on modern GPUs due to:

**Efficient wave equation**: The 2D discrete approximation requires only 5 texture reads per pixel in Buffer A.**Texture feedback**: Using the GPU’s texture units for reading the previous state is typically faster than computing it in the shader.**Limited ray marching**: The distance function is simple (a displaced box), so rays converge quickly, typically in 10-15 steps.

The main bottleneck is fill rate: every pixel in Buffer A reads 5 samples, and every pixel in the Image pass does ray marching. On lower- end hardware, reducing the resolution of Buffer A or limiting the maximum ray marching steps can improve performance.

# Conclusion

This raindrops on puddle effect demonstrates how combining relatively simple techniques can create convincing simulation of natural phenomena. The wave equation handles the physics of ripple propagation, ray marching renders the 3D geometry, and Fresnel reflections add realism to the water surface.

The key to making it work is careful attention to the details: proper damping prevents chaos, smooth raindrop pulses look more natural than sudden impacts, and combining multiple lighting terms creates a rich, layered look.

Feel free to experiment with the live demo above and adjust the parameters to gain further insight how each one affects the rendered image.

# Asset Attribution

This demo uses the following third-party assets:

**City Night HDRI Cubemap**: Downloaded from[HDRI Hub](https://www.hdri-hub.com/free-hdr-city-night-lights). Used for environment reflections and sky background.**Pavement Texture**: “Crazy Stone Pavement Texture” from[Texturelib](https://texturelib.com/texture/?path=/Textures/brick/pavement/brick_pavement_0080). Copyright © 2019 Dmitriy Chugai. Used for ground rendering.

Both assets are used in accordance with their respective terms. If you plan to reuse this demo, please verify the current licensing terms with the original sources.