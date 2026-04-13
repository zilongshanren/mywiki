---
title: 'GM Shaders Guest: Radiance Cascades 2'
url: https://mini.gmshaders.com/p/radiance-cascades2
author: Alex; Xor
published: '2024-07-13'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

Hello! This is Yaazarai (Alex) again, and thank you for reading part one, an Introduction to Radiance Cascades! As a recap Radiance Cascades is a method of global illumination (GI) created by Alexander Sannikov that takes advantage of the unique properties of the penumbra hypothesis, which states: that the penumbra of a shadow requires a higher “linear resolution” (more probes) closer to a light source and a higher angular resolution” (more rays) further from a light source. This is done by casting short rays from many probes within the scene at the lowest cascade, and as you move up through the cascade hierarchy, cast more longer rays from further away from fewer probes (4x more rays from 4x longer away at 4x length, but from 1/4x as many probe positions per cascade). Then merge all of the cascades to reconstruct all of the rays into the full and final radiance field. The physics behind radiance/lights fields are linear in nature. However, due to limited GPU processing power, we’re limited in how much we can render. This is why we scale by a factor of 2 or 4 between cascades and interpolate between them as it gives us linear scaling at a lower cost.

Disclaimer: The implementation and explanation provided only covers one narrow design domain of Radiance Cascades using screenspace raymarching.

GM Shaders is a reader-supported publication. To receive new posts and support my work, consider becoming a free or paid subscriber.

Overview (Fixes & Optimizations)

The demo implementation provided in part one had several problems: overly complicated, no dynamic resolution, poor performance, more memory than necessary.

Complicated: The shaders for calculating rays and merging were split in two, causing me to double my shader pipeline setup. I also wanted to visualize each cascade separately and render each to their own surfaces. In reality, neither of these were necessary after rewriting the shaders to work together in one pass: raymarch + merge with the previous cascade (N+1).

Not Dynamic: All of the math I’d figured in the original shader was all in respect to square resolutions—even the SDF generation for raymarching—so changing the resolution to anything other than square caused everything to break. This was unfortunately due to focusing on customizing parameters rather than consistency. With the new implementation, I’ve enforced strict, less-customizable requirements to ensure proper scaling for the cascades themselves and the distance fields (SDF). The demo managed a smooth 1024 x 1024 render, but that may not be good enough for higher resolution games, not to mention the performance loss of clipping a square render to fit your game’s resolution!

Performance: Also missing is one key simple optimization: texture cache. Since shaders operate spatially, GPUs load and store texture data spatially via space filling curves to optimize texture memory reads/writes. I’m no expert, so my entire understanding boils down to: texture reads/write closer together both in space and memory go fast. We can take advantage of this by re-ordering our ray/probe storage pattern within our cascades to match. Merging Optimization: While not a major performance impact, we can reorder how rays are packed into the texture such that all rays pointing in the same direction are together in memory to take advantage of hardware interpolation for merging to reduce texture samples from merged rays by 1/4th (1 interpolated sample from each cN+1 probe).

UPDATE: If you’ve read this previously, the direction-first layout is NOT actually faster. There was an issue in the version of GameMaker at the time affecting performance. However this alternative layout is still easier for debugging!

Memory: Let’s say you want a higher quality render, you can increase the number of rays per-probe or decrease spacing between probes to fit more probes within the scene. At even 4 rays per probe at 1024 x 1024 that’s a 4K texture when using one pixel per ray. If you double probe density that’s quickly an 8K texture (2048 x 2048 x 4). There’s a simple optimization we can make to cut memory by 75% simply by casting 4x as many rays per cascade pixel.

Despite all of these problems, they can all be fixed trivially with the following two memory optimization patterns: Pre-Averaging and Direction-FirstProbes. These optimizations are provided curtesy of the Graphics Programming Discord community for Radiance Cascades.

Optimization #1: Pre-Averaging

Pre-Averaging, or Pre-Merge Ray Averaging takes advantage of cascade merging: where we lookup the four nearest probes of cascade N+1 and the four rays of each probe pointing in the same direction. We average each group of four rays, then interpolate by relative probe position to each N+1 probe.

Fig 1. Example of merging cascade N (red probe) with cascade N+1 (yellow probes). Probe N’s interpolation “weight” is its relative position between N+1 probes.

If we’re just going to average the results anyways, why even bother storing all four rays individually? In basic cases, this is unnecessary.

Instead, we can cast four rays into the scene, then store as one averaged result. This reduces the number of texture lookups during merging from sixteen (one per ray, four rays per probe) down to four texture lookups and reduces memory requirements from one pixel per ray to one pixel per four rays—a whopping 75% reduction in both samples and memory storage!

Optimization #2: Hardware Interpolation

With Radiance Cascades the memory layout provided by the original paper uses “position first probes,” where each block of memory represents one probe (video #1 below), and each pixel within that probe is a ray at a direction emitted from that probe.

One alternative is to reorganize our rays by “direction first” and position second; where one block of memory represents a group of rays each cast from their respective probes all pointing in the same direction (video #2 below).

You’ll notice that there are 4 yellow rays highlighted, this shows the pre-averaging component combined with direction-first probes, where we cast 4 rays at once and average their result (for merging) to avoid storing 75% more data—note the much higher probe/ray density here at the same resolution.

Hardware interpolation: reiterating on merging we lookup the four nearest probes of cascade N+1 and interpolate their rays. Now that all of the rays are grouped together spatially in memory we can enable hardware interpolation to automatically interpolate the rays in a single texture sample. This is done by calling gpu_set_texfilter(true) before we run our shader. Once hardware interpolation is enabled, we can sample in-between each of the four probes within a direction-first probe block to get the interpolated sample. Combine this with pre-averaging to reduce merge overhead from 16 texture samples down to 1.

While not a major optimization, the reduction in overall texture samples may provide extra headroom with higher resolutions.

The added bonus is mainly for debugging; since all rays pointing in the same direction are packed together its easier to verify that each ray direction or position within the scene is acting as expected.

You can play with the visualization demo by cloning or downloading from the provided Github repository.

Implementation: Code Deep Dive

The Radiance Cascades implementation is almost entirely a single shader excluding distance field generation.

Shader Inputs

For this implementation of Radiance Cascades we have an extensive list of inputs:

// Standard fragment texel position:
varying vec2 in_TexelCoord;
// Radiance Cascades Inputs:
// Gameplay lights/occluders scene.
uniform sampler2D in_RenderScene;
// Distance Field surface to sample from.
uniform sampler2D in_DistanceField;
// Surface size of the screen/gameplay area.
uniform vec2 in_RenderExtent;
// Surface size of the cascade being rendered.
uniform vec2 in_CascadeExtent;
// Total number of cascades used.
uniform float in_CascadeCount;
// Current cascade index to render.
uniform float in_CascadeIndex;
// Probe density/spacing of cascade0.
uniform float in_CascadeLinear;
// Ray interval length of cascade0.
uniform float in_CascadeInterval;

The first two inputs in_RenderScene and in_DistanceField are surface textures containing the game lights/shadow casters (render scene) and the distance field that represents that scene. The distance field is generated via an JFA/SDF shader which you can read about here.

The in_RenderExtent is two values (vec2) width and height of the scene and in_CascadeExtent is the size of the cascade surface we’re rendering to. The size of the cascade depends on resolution settings:

// Sets the cascade surface width,height relative to probe density.
cascade_width = render_width / cascade0_linear;
cascade_height = render_height / cascade0_linear;

As the paper outlines (fig 8), when using 4x ray and 1/4x probe scaling the cascade size is constant across all cascades. The cascade0_linear specifies the density and spacing of probes as powers of two (e.g. 1, 2, 4, 8px etc. apart) a higher value results in lower probe density as spacing between probes becomes larger. Values can be less than zero for even higher fidelity as you get multiple probes per-pixel at 0.5 (2 probes per pixel) and 0.25 (4 probes per pixel) and 0.125 (8 probes per pixel) at a much rendering higher cost.

The in_CascadeCount and in_CascadeIndex are pretty self-explanatory. We pass the cascade index 0…N to tell us which cascade pass we’re rendering and how many total passes are being used.

The in_CascadeLinear (probe spacing/density) and in_CascadeInterval (ray interval lengths) are the initial cascade0 settings which get scaled 4x for each successive cascade. Cascade0 (c0) has a linear scaling of N, c1 has a scaling of N*4, c2 has a scaling of N*16, c3 has a scaling of N*64, etc.

Raymarching

We’ve previously visited raymarching in other posts here and here. The idea is the same, choose a point within the scene and direction which to cast a ray and read out samples from the distance field at each point along the ray telling us how far we are away from the nearest surface—stop on surface hit.

vec4 raymarch(vec2 point, float theta, probe_info info) {
// Scalar for converting pixel-coordinates back to screen-space UV.
vec2 texel = 1.0 / in_RenderExtent;
// Ray component to move in the direction of theta.
vec2 delta = vec2(cos(theta), -sin(theta));
// Ray origin at interval offset starting point.
vec2 ray = (point + (delta * info.offset)) * texel;
// Loop for max length of interval (in event that ray SDF is near 0 for entire length of ray).
for(float i = 0.0, df = 0.0, rd = 0.0; i < info.range; i++) {
// Distance sample of scene converted from 2-byte encoded distance field scene texture.
df = V2F16(texture2D(in_DistanceField, ray).rg);
// Sum up total ray distance traveled (scale from distance UV to pixel-coordinates).
rd += df * info.scale;
// Move ray along its direction by SDF distance sample.
ray += (delta * df * info.scale * texel);
// If ray has reached range or out-of-bounds, return no-hit.
if (rd >= info.range || floor(ray) != vec2(0.0)) break;
// 2D light only cast light at their surfaces, not their volume.
if (df < EPS && rd < EPS && in_CascadeIndex != 0.0) return vec4(0.0);
// On-hit return radiance from scene (with visibility term of 0--e.g. no visibility to merge with higher cascades).
if (df < EPS) return vec4(texture2D(in_RenderScene, ray).rgb, 0.0);
}
// If no-hit return no radiance (with visibility term of 1--visibility to merge with higher cascades).
return vec4(0.0, 0.0, 0.0, 1.0);
}

This may be atypical, however I am performing raymarching in pixel space rather than UV space as it saved a lot of headache when dealing with non-square distance fields. To fix this when texture sampling we get the texel size (texture size of 1 pixel) to multiply back to UV space.

The largest change here from typical raymarching is the range and offset parameters specified for the ray. Each cascade represents a different part of the radiance field and as we move up the cascade chain rays get 4x longer and 4x further away. To fix this we first offset the ray as point + (delta * offset) and then only raymarch for a fixed distance. If the ray goes offscreen or total sampled ray distance rd reaches/exceeds the ray’s interval range we terminate the ray.

The second change is that in 2D light volumes only emit light from their surface edge, not from within (this otherwise causes artifacts). If the ray distance rd is zero AND the ray starts with a distance field sample df of zero the ray starts within a ray volume and must terminate.

The final change is that all distance field samples get scaled by the diagonal of the render width and height: length(in_RenderExtent). The distance field shader calculates all of its distances in pixel coordinates and then scales them back down by this diagonal scale back to UV space to fit within the 2-byte float precision when storing them in the texture. This avoids scaling issues by NOT calculating distance in UV space which become skewed. In UV space the upper/lower bounds of UVs are 0.0 and 1.0 for both x and y axis. This becomes a problem when calculating distances because the x and y axis have different widths and heights.

Probe/Ray Memory Layout & Abstraction

The parameters that define the probe and ray information for each pixel within the cascade are re-used everywhere. To make this easy I’ve abstracted out only the necessary parameters. The angular/linear resolution of the cascade, size of each direction-first probe, the ray’s probe position corresponding to its respective spatial-probe within each direction-first probe, index of the ray to calculate theta or the actual direction the ray is pointing, starting offset away from probe center and range or length of the ray cast into the scene, and the SDF scale factor.

For set up we need to define an abstract function (to make life easier) which defines our parameters for the direction-first memory layout. In this implementation angular resolution scales 4x, but is fixed to 4 rays in cascade0 and 4x for every cascade. This isn’t necessary, but makes managing cascades easier. In fact each function within the shader is an abstraction to perform its very specific task.

probe_info cascadeTexelInfo(vec2 coord) {
// Ray Count.
float angular = pow(2.0, in_CascadeIndex);
// Cascade Probe Spacing.
vec2 linear = vec2(in_CascadeLinear * pow(2.0, in_CascadeIndex));
// Size of Probe-Group.
vec2 size = in_CascadeExtent / angular;
// Probe-Group Index.
vec2 probe = mod(floor(coord), size);
// * spatial-xy ray-index position.
vec2 raypos = floor(in_TexelCoord * angular);
// PreAvg Index (actual = index * 4).
float index = raypos.x + (angular * raypos.y);
// Offset of Ray Interval (geometric sum).
float offset = (in_CascadeInterval * (1.0 - pow(4.0, in_CascadeIndex))) / (1.0 - 4.0);
// Length of Ray Interval (geometric sum).
float range = in_CascadeInterval * pow(4.0, in_CascadeIndex);
// * light Leak Fix (minimal overlap with higher cascade).
range += length(vec2(in_CascadeLinear * pow(2.0, in_CascadeIndex+1.0)));
// Diagonal of Render Extent (for SDF scaling).
float scale = length(in_RenderExtent);
// Output probe information struct.
return probe_info(angular * angular, linear, size, probe, index, offset, range, scale);
}

The first two parameters angular and linear set number of rays (angular resolution) and spacing (linear resolution) and by extension the number of probes within the cascade. Remember though that we’re pre-averaging, so the angular resolution here is actually 1/4x the actual number of rays cast into the scene per cascade. Both angular and linear scale 4x—powers of 4—except that linear resolution is two-dimensional so each x,y dimension scales by 2x for a total scaling factor of 4x.

The size parameter gets the number of rays—each corresponding to their respective probe—within each direction-first probe. The probe parameter then determines the actual probe-position of the ray. The index parameter converts our two-dimensional texel coordinate into 1-dimensional array index via the row-major-order curve or raster-scanline order which is just simple to use—there shouldn’t be any real benefit to storing via z-order curve as lookups for merging are GPU inexpensive and not worth the added complexity.

The offset and range parameters are per specification where rays within each cascade gets 4x offset further away and get 4xs larger using geometric sequences. However we also need to add a final minor overlap to the cascade interval to bright the slight gap between cascades to fix light leak. This overlap is spacing between probes of cascade N+1 due to the spatial transition between cascades N and N+1.

Finally we set the SDF’s scaling parameter for reading out pixel-space distances from our distance field shader. The SDF scales itself by the diagonal of the screen resolution to convert pixel-space distances to UV space while fitting in the 2-byte precision of the Distance field texture. This is done by calculating length of the vector formed by the width and height of the screen.

Merging with Cascade N+1

The final puzzle piece is merging the current cascade with the next highest cascade. Direction-First ordering to enable hardware interpolation and Pre-Averaging make this trivial, cutting down our merge samples from 16 (4 per probe) down to 1 single texture sample. Nice!

vec4 merge(vec4 rinfo, float index, probe_info pinfo) {
// For any radiance with zero-alpha do not merge (highest cascade also cannot merge).
if (rinfo.a == 0.0 || in_CascadeIndex >= in_CascadeCount - 1.0)
// Return non-merged radiance (invert alpha to correct alpha from raymarch ray-visibility term).
return vec4(rinfo.rgb, 1.0 - rinfo.a);
// Angular resolution of cascade N+1 for probe lookups.
float angularN1 = pow(2.0, in_CascadeIndex + 1.0);
// Size of probe group of cascade N+1 (N+1 has 1/4 total probe count or 1/2 each x,y axis).
vec2 sizeN1 = pinfo.size * 0.5;
// Get the probe group correlated to the ray index passed of the current cascade ray we're merging with.
vec2 probeN1 = vec2(mod(index, angularN1), floor(index / angularN1)) * sizeN1;
// Interpolated probe position in cascade N+1 (layouts match but with 1/2 count, probe falls into its interpolated position by default).
vec2 interpUVN1 = pinfo.probe * 0.5;
// Clamp interpolated probe position away from edge to avoid hardware inteprolation affecting merge lookups from adjacet probe groups.
vec2 clampedUVN1 = max(vec2(1.0), min(interpUVN1, sizeN1 - 1.0));
// Final lookup cascade position of the interpolated merge lookup.
vec2 probeUVN1 = probeN1 + clampedUVN1 + 0.25;
// Interpolated texture lookup of the merge sample.
vec4 interpolated = texture2D(gm_BaseTexture, probeUVN1 * (1.0 / in_CascadeExtent));
// Return original radiance input and merge with lookup sample.
return rinfo + interpolated;
}

The first if-statement check here is crucial. We want to avoid merging rays in two separate cases:

If the current ray already has radiance by hitting a surface—only terminated rays with no-hit need to merge because they found no scene radiance. Also any ray in cascade0 with a hit must have its alpha component inverted as the ray-visibility term is stored in the alpha component as 1 for no-hit and 0 for hit. If you don’t invert the alpha all light volumes within the scene will be black.

We never merge rays if we’re in the highest cascade. If there is no higher cascade, there is no cascade N+1 to merge with.

When merging for each ray we merge with 16 rays of cascade N+1, lookup each N+1 probe and the 4 corresponding rays in this direction, average, then interpolate. The averaging is done and hardware interpolation is setup, so all we have to do is find the closest top-left N+1 probe and add an offset between the 4 probes for our weight to get the interpolated sample.

If you look back at figure 1 for merging you can see that the interpolation weight is relative to the current probe’s position between all N+1 probes, which is 0.25, 0.25 (closest to top-left), 0.75, 0.25 (closest to top-right), 0.25, 0.75 (closest to bottom-left) and finally 0.75, 0.75 (closest to bottom-right). These weights are set because of the spatial density and positioning of this cascades probes are evenly distributed between probes of cascade N+1.

Now we need to get a little bit of information about cascade N+1, the angular resolution or angularN1 and size of each directional probe or sizeN1 and the direction-first probe or probeN1 corresponding to the index (direction/theta index) of the ray we’re merging. This is done by converting our row-major-order curve ray-index back to spatial index and then multiplying by the direction-first probe size to get the top-left probe position in the cascade.

NOTE: that with pre-averaged rays if we multiply our ray-index by 4 to get the actual index, this gives us the same resolution as the pre-averaged rays of cascade N+1. See figure below for an illustration of how index blocks of varying resolutions line up.

Fig 4. Showing how index blocks line up when multiplied up to match a higher resolution.

Next we take our current probe position and divide it in half to get the same position at 1/2 the spatial resolution to match that of cascade N+1, this is interpUVN1. This sets our probe position to the same relative position between the interpolated probes of cascade N+1, however if the probe position is even, e.g. 2,2 and we divide it we get 1,1 and the probe lies exactly on one of the N+1 probes. If the index is odd say 3,3 and divide it we get 1.5,1.5 and our probe lies in the center of all four N+1 probes. This is perfect because now we can just add 0.25 and now the interpolated probe position is properly weighted (2,2 becomes 2.25,2.25 and 1.5,1.5 becomes 1.75, 1.75).

Then clamp interpUVN1 to the boundary of the directional-first probe minus a 1-probe border to avoid interpolation leaks between direction-first probes at their borders. See figure 2 and 3 below for the difference.

Finally we add the interpolated probe position to the direction-first probe position within the cascade and voila, merged lookup.

Fig 2. Merged cascade with border clamping.

Fig 3. Merged cascade without border clamping.

Wrapping Up with Main()

The main function is the easiest, simply call each of our abstraction functions for each of the 4 pre-averaged rays we’re casting for the current texel. Lookup our ray/probe information with a call to cascadeTexelInfo(), calculate the probe’s origin point corresponding to this texel’s ray and calculate our pre-averaged ray-index or preavg_index, loop 4 iterations (one per ray), cast the ray into the scene and merge with cascade N+1. Nice!

void main() {
// Get info about the current probe on screen (position, angular index, etc.).
probe_info pinfo = cascadeTexelInfo(floor(in_TexelCoord * in_CascadeExtent));
// Get this probes position in screen space.
vec2 origin = (pinfo.probe + 0.5) * pinfo.linear;
// Convert this probe's pre-averaged index to its actual angular index (casting 4x rays, but storing 1x averaged).
float preavg_index = pinfo.index * 4.0;
// Get the scalar for converting our angular index to radians (0 to 2pi).
float theta_scalar = TAU / (pinfo.angular * 4.0);
// Cast 4 rays, one for each angular index for this pre-averaged ray.
for(float i = 0.0; i < 4.0; i++) {
// Get the actual index for this pre-averaged ray.
float index = preavg_index + float(i);
// Get the actual angle (theta) for this pre-averaged ray.
float theta = (index + 0.5) * theta_scalar;
// Raymarch the current ray at the desired angle (raymarch function handles interval offsets).
vec4 rinfo = raymarch(origin, theta, pinfo);
// Lookup the 4 rays of cascade N+1 in the same direction as this ray, merge and average results.
gl_FragColor += merge(rinfo, index, pinfo) * 0.25;
}
}

With pre-averaging ray indices are all compressed to 1/4th, so we need to undo that and multiply up our ray-index by 4 before calculating the theta for each ray. This is that index correction mentioned in the previous section. Once we know the ray index we can normalize the index and convert to radians and finally raymarch and merge. As mentioned prior the actual ray-index of the pre-averaged ray block is the same as the pre-averaged ray-index of the rays we want to merge with in cascade N+1, this is why we pass this scaled up ray-index into the merging function.

Conclusion

This new memory layout using pre-averaging and direction-first probes provides an elegantly simple implementation with nearly the entirety of Radiance Cascades being implemented in one short shader with less than 100 lines of code. The goal here was to increase performance and fix scaling bugs from the original implementation as we’ve exceeded that greatly! With a simple frame-time stress test (running on an RTX 3080) with similar settings we’ve got the following performance delta:

A) Position-First:
- Resolution: 1024 x 1024
- Probe Density 0.25 (4 probes per pixel)
- Ray Density: 4 (4 rays per probe c0)
= 29.91 / 8.33ms (120 FPS)
B) Direction-First:
- Resolution: 1920 x 1080
- Probe Density 0.25 (4 probes per pixel)
- Ray Density: 4 (4 rays per probe c0)
= 25.95 / 8.33ms (120 FPS)

The position-first implementation with the same settings at a lower resolution produced a higher frame-time delta per-frame at 120 FPS! While direction-first over doubled performance producing a lower frame-time delta at double the screen space.

This should at least get anyone and everyone understanding Radiance Cascades! No extras this time around, but go and take a look at Mytino’s work again with his voxel game implementing his own derivation of Radiance Cascades with realistic physics!

The visualization demos, original implementation and new direction-first implementation are all provided at the github repo (unlicensed).

I've noticed that nearly all 2D radiance cascade implementations I could find seem to have overlaid wave like patterns (I think someone referred to this as interference patterns in the first post). I was curious about why this is happening and if there is any way to reduce the effect.

Also I am a little puzzled on performance compared to sampling N random rays per pixel like in the first tutorial of this series (https://mini.gmshaders.com/p/yaazarai-gi).

For example if you have 6 cascades with 4 rays per pixel, isn't that about the same as sampling random 24 rays per pixel in one pass? From my tests sometimes RC runs slower than random sampling when the total ray operations match. (Big emphasis on sometimes because for some magical reason it depends on the device. On my desktop RC for the same scene runs with 40% GPU load (6 cascades) while naive rm runs 70% GPU load (24 rays) while on my laptop the same scene runs slower in RC compared to naive rm)

I agree that RC looks way better as its noiseless, but 24 random rays + blue noise + bilateral filtering (reducing noise) produces comparable results and sometimes its even better aesthetically as there are no ringing artifacts. If both implementations call the raymarch function 24 times per pixel then where is the performance difference coming from?

This might be an implementation issue on my side so I am not jumping to any conclusions but is RC supposed to be way faster?

I've noticed that nearly all 2D radiance cascade implementations I could find seem to have overlaid wave like patterns (I think someone referred to this as interference patterns in the first post). I was curious about why this is happening and if there is any way to reduce the effect.

Also I am a little puzzled on performance compared to sampling N random rays per pixel like in the first tutorial of this series (https://mini.gmshaders.com/p/yaazarai-gi).

For example if you have 6 cascades with 4 rays per pixel, isn't that about the same as sampling random 24 rays per pixel in one pass? From my tests sometimes RC runs slower than random sampling when the total ray operations match. (Big emphasis on sometimes because for some magical reason it depends on the device. On my desktop RC for the same scene runs with 40% GPU load (6 cascades) while naive rm runs 70% GPU load (24 rays) while on my laptop the same scene runs slower in RC compared to naive rm)

I agree that RC looks way better as its noiseless, but 24 random rays + blue noise + bilateral filtering (reducing noise) produces comparable results and sometimes its even better aesthetically as there are no ringing artifacts. If both implementations call the raymarch function 24 times per pixel then where is the performance difference coming from?

This might be an implementation issue on my side so I am not jumping to any conclusions but is RC supposed to be way faster?