---
title: Full Screen Pass Without Explicit Geometry
url: https://www.4rknova.com/blog/2019/03/21/full-screen-pass-without-explicit-geometry
author: Nikolaos Papadopoulos
published: '2019-03-21'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

Drawing geometry using modern graphics APIs typically involves generating a set of data buffers to define a shape in terms of a collection of 3D point coordinates and the corresponding set of connections between those points.

This is true for even the most trivial of shapes, including the humble screen aligned quad which consist of 2 triangles.

Thankfully, both OpenGL and DirectX allow drawing simple geometry without the need to create any vertex attribute buffers, using a simple trick.

Instead of explicitely defining the vertex attributes, the shader uses the built-in vertex ID value to derive the position and uv coordinates for each vertex and produce the following geometry:

| Vertex ID | Position | UV Coordinates |
|---|---|---|
| 0 | (-1,-1) | (0,0) |
| 1 | (+3,-1) | (2,0) |
| 2 | (-1,-3) | (0,2) |

In practice, a screen filling triangle can be more efficient than a quadrilateral. For example, image processing proceeds almost 10% faster on the AMD GCN architectures when a single triangle is used instead of a quadrilateral formed from two triangles [3], due to better cache coherency

.

[[4]](https://www.4rknova.com#REF-4)It’s important to note that OpenGL uses a right-handed coordinate system while DirectX uses a left-handed one. This essentially means that the vertexID transform used for DirectX won’t work in OpenGL and vice versa. The vertices must be ordered accordingly so that they are traversed correctly.

# Implementation

## OpenGL / GLSL

### App

```
[...]
glDrawArrays( GL_TRIANGLES, 0, 3 );
[...]
```


### Shader

```
out vec2 texCoord;
void main()
{
float x = -1.0 + float((gl_VertexID & 1) << 2);
float y = -1.0 + float((gl_VertexID & 2) << 1);
texCoord = (vec2(x,y) + 1.0) *0.5;
gl_Position = vec4(x, y, 0, 1);
}
```


## DirectX / HLSL

### App

```
[...]
ID3D11DeviceContext* pCtx = nullptr;
m_pDevice->GetImmediateContext(&pCtx);
[...]
pCtx->VSSetShader(shader, ..., ...);
pCtx->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
pCtx->Draw(3, 0);
[...]
```


### Shader

```
struct VS_Output
{
float4 Pos : SV_POSITION;
float2 Tex : TEXCOORD0;
};
VS_Output VS(uint id : SV_VertexID)
{
VS_Output Output;
Output.Tex = float2((id << 1) & 2, id & 2);
Output.Pos = float4(Output.Tex * float2(2,-2) + float2(-1,1), 0, 1);
return Output;
}
```


# References / Further Reading

Tomas Akenine-Mller, Eric Haines, and Naty Hoffman. 2018. Real-Time Rendering, Fourth Edition (4th ed.). A. K. Peters, Ltd., Natick, MA, USA. Chapter 12, Image-Space Effects