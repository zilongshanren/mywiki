---
title: Plasma Effect
url: https://www.4rknova.com/blog/2016/11/01/plasma
author: Nikolaos Papadopoulos
published: '2016-11-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

The plasma effect is one of the most iconic visual effects from the demoscene era of the 1980s and 1990s. Named for its resemblance to flowing plasma or aurora-like patterns, this effect creates organic, continuously moving patterns using surprisingly simple mathematics. Despite its simplicity, the visual result is captivating and has remained a favorite demonstration of procedural graphics techniques.

The effect relies on combining multiple sinusoidal wave patterns to create complex interference patterns. By animating these patterns over time and mapping them to color gradients, we achieve the characteristic flowing, pulsing appearance.

On early hardware like the Commodore 64 and Amiga, plasma effects often used pre-calculated lookup tables to avoid expensive real-time sine calculations. Modern GPUs can compute these effects in real-time with minimal performance impact, allowing for more complex variations and higher resolutions.

Here’s what the effect looks like:

# Core Mathematics

At its heart, the plasma effect combines multiple sine and cosine functions with different frequencies and phases. The basic approach involves:

**Generating wave patterns**: Create 2D wave patterns using sine and cosine functions based on screen coordinates.**Combining waves**: Add or multiply multiple wave patterns to create interference effects.**Time animation**: Offset the wave patterns over time to create motion.**Color mapping**: Map the resulting values to a color gradient.

The typical formula structure looks like:

```
value = sin(x + time) + cos(y + time) + sin(distance + time)
```


Where different combinations of `x`

, `y`

, `distance`

, and `time`

create different visual patterns.

# Wave Interference

The beauty of the plasma effect comes from wave interference. When multiple sinusoidal patterns overlap, they create complex patterns through constructive and destructive interference:

**Constructive interference**: Waves align and amplify each other**Destructive interference**: Waves cancel each other out

This creates the characteristic peaks and valleys that define the plasma’s flowing appearance.

# Color Gradients

The numerical output of the combined sine waves is then mapped to colors. A common approach uses the cosine color palette technique, which provides smooth, continuous color gradients by treating the wave output as input to RGB color channels with different phase offsets.

# Specular Enhancement

Modern implementations can add specular highlights by analyzing the gradient of the color field. This creates the illusion of a reflective surface and adds depth to the otherwise flat 2D pattern.

The specular component is typically implemented using derivatives (dFdx and dFdy in GLSL) to detect rapid color changes, treating these as “surface normals” for lighting calculations.

# Implementation Walkthrough

The sections above describe the general principles behind the plasma effect. In this section we will walk through the actual implementation step by step.

```
// by Nikos Papadopoulos, 4rknova / 2016
// Specular highlights contributed by Shane
// Enable specular highlight pass for added depth and shine
#define SPECULAR
// Controls the overall zoom level of the plasma pattern
#define SCALE 1.0
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
float time = iTime;
// Compute the aspect ratio correction vector so the pattern
// isn't stretched on non-square viewports
vec2 aspectRatio = vec2(iResolution.x / iResolution.y, 1.0);
// Map fragment coordinates to a scaled, aspect-corrected UV space
// and scroll the pattern over time to create movement
vec2 uv = SCALE * fragCoord.xy / iResolution.xy * aspectRatio * 4.0 + time * 0.3;
// Generate two oscillating phase values that evolve over time.
// These drive the plasma's swirling motion by combining the
// x and y axes with sin/cos pairs at different rates.
float phaseVertical = 0.1 + cos(uv.y + sin(0.148 - time)) + 2.4 * time;
float phaseHorizontal = 0.9 + sin(uv.x + cos(0.628 + time)) - 0.7 * time;
// Radial distance from the origin. Adds circular symmetry
// to the interference pattern
float radialDist = length(uv);
// Combine the radial distance with both phase terms to produce
// the final plasma interference value. The product of cos and sin
// creates the characteristic banded, swirling look.
float plasma = 7.0 * cos(radialDist + phaseHorizontal)
* sin(phaseVertical + phaseHorizontal);
// Map the scalar plasma value to RGB using cosine-based palette.
// The offset vector (.2, .5, .9) shifts each channel's phase,
// producing smooth color gradients across the pattern.
fragColor = vec4(0.5 + 0.5 * cos(plasma + vec3(0.2, 0.5, 0.9)), 1.0);
#ifdef SPECULAR
// Approximate a specular lighting pass using screen-space derivatives.
// dFdx/dFdy estimate the color gradient between neighbouring fragments,
// which serves as a proxy for surface normals on the plasma "surface".
// A simple Phong-style specular term is then applied with a warm tint
// to give the plasma a glossy, liquid appearance.
vec3 surfaceNormal = normalize(vec3(
length(dFdx(fragColor)),
length(dFdy(fragColor)),
0.5 / iResolution.y
));
float specularIntensity = pow(max(surfaceNormal.z, 0.0), 2.0);
vec4 warmTint = vec4(1.0, 0.7, 0.4, 1.0);
fragColor *= warmTint * specularIntensity + 0.75;
#endif
}
```


## Setting Up the Coordinate Space

The first thing the shader does is map each pixel to a usable coordinate. Raw pixel positions `fragCoord`

are divided by the viewport resolution to produce normalized coordinates in the 0 to 1 range. These are then scaled by 4.0 and corrected for aspect ratio so the pattern does not appear stretched on non-square viewports. Finally, a time-dependent offset `time * 0.3`

is added to both axes, which causes the entire pattern to scroll slowly across the screen.

```
vec2 aspectRatio = vec2(iResolution.x / iResolution.y, 1.0);
vec2 uv = SCALE * fragCoord.xy / iResolution.xy * aspectRatio * 4.0 + time * 0.3;
```


The `SCALE`

define at the top of the shader lets you adjust the zoom level without touching the body of the code.

## Phase Oscillators

The core motion of the plasma is driven by two phase values, one for the vertical axis and one for the horizontal axis. Each one feeds the current coordinate through a nested sin/cos pair whose argument also includes time, producing smooth oscillation that drifts at a different rate along each axis.

```
float phaseVertical = 0.1 + cos(uv.y + sin(0.148 - time)) + 2.4 * time;
float phaseHorizontal = 0.9 + sin(uv.x + cos(0.628 + time)) - 0.7 * time;
```


The magic numbers `0.148`

and `0.628`

are arbitrary seed offsets that were chosen experimentally to produce a pleasing visual rhythm. Changing them will alter the shape and speed of the swirls without breaking the effect. The linear time terms `2.4 * time`

and `-0.7 * time`

add a constant drift on top of the oscillation, preventing the pattern from looking static.

Because the two phases evolve at different speeds and in opposite directions, the resulting pattern never settles into a repeating loop, which is what gives the plasma its organic, unpredictable feel.

## Radial Distance

The `radialDist`

variable is simply the Euclidean distance from the UV-space origin to the current fragment position. When this value is fed into the interference equation it adds concentric, ring-like structure to the pattern, complementing the linear waves produced by the phase oscillators.

```
float radialDist = length(uv);
```


## Interference Combination

The final plasma value is produced by multiplying a cosine wave (driven by radial distance plus the horizontal phase) with a sine wave (driven by the sum of both phases). Multiplying rather than adding the two waves produces sharper bands and more contrast, because the product is zero whenever either wave crosses zero. The factor of 7.0 amplifies the combined value, which increases the number of visible color bands.

```
float plasma = 7.0 * cos(radialDist + phaseHorizontal)
* sin(phaseVertical + phaseHorizontal);
```


This single line is what generates the characteristic swirling, banded look of the effect. The interplay between linear phases and radial distance creates a pattern that is neither purely circular nor purely linear, but a fluid mixture of both.

## Cosine Color Palette

Rather than using a lookup table, the shader maps the scalar `plasma`

value to an RGB color using the cosine palette technique popularized by [Inigo Quilez](https://iquilezles.org/articles/palettes/). The idea is simple: pass the plasma value through `cos()`

for each color channel, but with a different phase offset per channel. The offsets `(0.2, 0.5, 0.9)`

stagger the red, green and blue channels so they peak at different plasma values, producing smooth rainbow-like gradients.

```
fragColor = vec4(0.5 + 0.5 * cos(plasma + vec3(0.2, 0.5, 0.9)), 1.0);
```


The `0.5 + 0.5 * cos(...)`

expression remaps the cosine output from the -1 to 1 range into the 0 to 1 range, which is what the GPU expects for color values. Changing the offset vector shifts which hues appear in the palette. For example, using `vec3(0.0, 2.1, 4.2)`

would produce a completely different color scheme while keeping the same underlying pattern.

## Specular Highlights

The optional specular pass treats the flat 2D color field as if it were a 3D surface and applies a simple lighting model to add a glossy sheen. It works by estimating a surface normal at each pixel using `dFdx`

and `dFdy`

, which are built-in GLSL functions that return the rate of change of a value between neighbouring fragments. Large changes suggest a steep slope, while small changes suggest a flat area.

```
vec3 surfaceNormal = normalize(vec3(
length(dFdx(fragColor)),
length(dFdy(fragColor)),
0.5 / iResolution.y
));
```


The x and y components of the constructed normal come from the magnitudes of the horizontal and vertical color gradients. The z component is a small constant that controls how “tall” the surface appears. Normalizing this vector gives a unit normal that can be used in standard lighting math.

The specular intensity is then computed using the z component of the normal, which represents how directly the surface faces the viewer. Flat areas (large z) get a strong highlight, while steep edges (small z) stay dark. The `pow(..., 2.0)`

sharpens the falloff to concentrate the highlights.

```
float specularIntensity = pow(max(surfaceNormal.z, 0.0), 2.0);
vec4 warmTint = vec4(1.0, 0.7, 0.4, 1.0);
fragColor *= warmTint * specularIntensity + 0.75;
```


Finally, the result is tinted with a warm orange-gold color and blended with the base plasma color. The `+ 0.75`

ensures that even areas without specular highlights retain most of their original brightness, so the effect enhances the image rather than darkening it.