---
title: 'Minimal setup screen space quads: No buffers/layouts required'
url: https://anteru.net/blog/2012/minimal-setup-screen-space-quads-no-buffers-layouts-required
published: '2012-03-03'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

A neat trick that [Rory Driscoll](https://twitter.com/#!/rorydriscoll) mentioned on Twitter is to [use vertex IDs to generate screen space quads](https://twitter.com/#!/rorydriscoll/status/148212638566985730). I just recently came around to use that in my stuff, so here’s some ready-to-use code. The advantage of using the vertex id is that you don’t need a vertex layout, vertex buffer or index buffer.

Here’s the complete vertex shader:

```
float4 VS_main (uint id : SV_VertexID) : SV_Position
{
switch (id) {
case 0: return float4 (-1, 1, 0, 1);
case 1: return float4 (-1, -1, 0, 1);
case 2: return float4 (1, 1, 0, 1);
case 3: return float4 (1, -1, 0, 1);
default: return float4 (0, 0, 0, 0);
}
}
```


All you need for rendering now is to issue a single draw call which renders a triangle strip containing four vertices, and you’re done. Note: This quad is for RH rendering, if your culling order is reversed, you’ll need to swap the second and third vertex. In the pixel shader, you can now use `SV_Position`

, or alternatively, you can also generate UV coordinates in the vertex shader.

**Update**: As noted in the comments by Martins, there is also a way to do it with a single triangle that spans the whole screen. Here’s the code for that, again for a RH system:

```
// Without the explicit casts, this does not compile correctly using the
// D3D Compiler (June 2010 SDK)
float x = float ((id & 2) << 1) - 1.0;
float y = 1.0 - float ((id & 1) << 2);
return float4 (x, y, 0, 1);
```


There’s a weird compiler bug that requires the explicit `float`

cast, otherwise, the D3D compiler from the June 2010 SDK fails to compile this code.