---
title: Different coordinate spaces and how they relate to the shader pipeline stages
url: https://apoorvaj.io/ndc-clip
published: '2025-01-09'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

Graphics programming relies on transforming position coordinates between different spaces—from 3D mesh vertex positions all the way to the final screen pixels. In this post, we’ll examine how these spaces relate to the graphics pipeline, and develop some intuition about the mathematics behind perspective projection.

```
| |
| | Input assembler
v |
Object-space coords (3D) - - - - - - - +
| |
| Append 1 as W coord, |
| multiply by 4x4 matrix | Vertex shader
v |
Clip-space coords (4D) - - - - - - - - +
| |
| Divide X, Y, and Z by W |
v |
Normalized-device coords (3D) | Fixed-function hardware
| |
| Viewport transform |
v |
Screen-space coords & depth (3D) - - - +
| |
| | Pixel shader
| |
```


To summarize the diagram above, the vertex shader usually gets object-space position coordinates from the input assembler stage of the graphics pipeline. The vertex shader then applies arbitrary logic (usually a object -> world -> view -> projection transformation) to output 4D clip-space coordinates. Sometimes, e.g. in full-screen shaders, the vertex shader can directly output clip-space coordinates, without receiving any object-space coordinates from the input assembler.

Then fixed function hardware takes these 4D clip-space coordinates through Normalized Device Coordinates (NDC) to Screen-space coordinates. In these black-boxed non-programmable steps, GPU hardware performs triangle clipping and rasterization. It bundles up the rasterized pixels along with their helper lanes into work packets, that are then scheduled to run on the GPUs shader execution units. Then the screen-space coordinates and depth are passed to the pixel shader, where as a graphics programmer, you get to use them.

Now let’s look at something a bit different that comes up when you’re in the weeds trying to figure out some depth logic. Let’s build some intuition about perspective projection.

Clip-space conventions are a little different between DirectX and OpenGL, so perspective projection math is a bit different as well. I’ll stick to DirectX style.

Since view-space (VS) to clip-space (CS) transformation is a matrix multiply, it is by definition a linear transformation. When CS.x, CS.y and CS.z are divided by CS.w to get NDC, that is when the non-linearity occurs.

A perspective projection matrix looks like this:

\begin{pmatrix} \frac{1}{\tan(\frac{FOV}{2})\cdot\text{aspect}} & 0 & 0 & 0 \\ 0 & \frac{1}{\tan(\frac{FOV}{2})} & 0 & 0 \\ 0 & 0 & \frac{\text{far}}{\text{far-near}} & 1 \\ 0 & 0 & -\frac{\text{near}\cdot\text{far}}{\text{far-near}} & 0 \end{pmatrix}

From this, let’s look at what happens to view-space points on the near and far plane in clip space. We’re going to focus in on depth, so we’ll ignore the X and Y coordinates and the first two columns of the matrix.

// VS = View-Space, CS = Clip-Space
// Substituting for `VS.w == 1`, we get:
CS.z = (VS.z * far / (far - near)) + ((-near * far) / (far - near));
CS.w = VS.z;
// For a view-space point on the near-plane, where VS.z = near:
CS.z = (near * far / (far - near)) + ((-near * far) / (far - near));
= ((near * far) - (near * far)) / (far - near);
= 0
CS.w = near;
// For a view-space point on the far-plane, where VS.z = far:
CS.z = (far * far / (far - near)) + ((-near * far) / (far - near));
= ((far * far) - (near * far)) / (far - near);
= (far * (far - near)) / (far - near);
= far;
CS.w = far;


So we can see that:

| View-space Z | Clip-space Z | Clip-space W |
|---|---|---|
| near | 0 | near |
| far | far | far |

This is just to give some intuition of what clip-space looks like after perspective projection.

This post started as a personal note that I often returned to. I originally drafted the note after a conversation with my colleague and friend Mikkel Simonsen.