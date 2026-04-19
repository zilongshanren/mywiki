---
title: Draw Anti-aliased Lines with Geometry Shader
url: https://atyuwen.github.io/posts/antialiased-line/
published: '2020-01-01'
source_blog: C++ Minor
source_site: https://atyuwen.github.io/
category: graphics
fetched: '2026-04-19'
---

For engine programmers, there are many cases you have to draw lines on screen, e.g. rendering a grid on the ground, drawing bounding boxes and other helper objects. Usually it’s not a problem if you are very used to the jaggies, but recently I can’t stand it anymore, my eyes complain to me that they want anti-aliased lines. After a quick search on google, it surprises me that there is no existing handy code piece can meet my needs. So, it’s time to do research!

The first thing comes to my eye is an old article “Fast Prefiltered Lines” 1. It describes a method that can draw pretty high quality anti-aliased lines with fixed cost, since the filter is pre-calculated. It’s a great article but I can’t use it directly for several reasons:

- It’s mainly about drawing 2D lines, so perspective projection is not considered.
- It uses CPU to calculate edge equations, but I want to keep changes to a minimum in my cpp code.
- It uses shader uniforms to pass the edge equations to pixel shader, which means you can only draw a single line in one DP.

Fortunately now the programmable pipeline is way more flexible than in 2005. With **geometry shader**, we can do it much easier. Following shows the final rendered image, and I’ll describe the details in below.

![](../../assets/958c2db9d56e7716.png)

First, draw lines as usual: there is no change needed for host code and vertex shader. Then, add following geometry shader to expand 1-pixel-width lines to 3-pixel-width quads in screen space, and store *distance to line center* in `TexCoord.x`

:

```
struct GeometryOutput
{
float4 HPosition : SV_Position;
noperspective float2 TexCoord : TEXCOORDN; // section 2
};
[maxvertexcount(4)]
void AALineGS(line VertexOutput IN[2], inout TriangleStream<GeometryOutput> OUT)
{
VertexOutput P0 = IN[0];
VertexOutput P1 = IN[1];
if (P0.HPosition.w > P1.HPosition.w)
{
VertexOutput temp = P0;
P0 = P1;
P1 = temp;
}
if (P0.HPosition.w < NearPlane) // section 1
{
float ratio = (NearPlane - P0.HPosition.w) / (P1.HPosition.w - P0.HPosition.w);
P0.HPosition = lerp(P0.HPosition, P1.HPosition, ratio);
}
float2 a = P0.HPosition.xy / P0.HPosition.w;
float2 b = P1.HPosition.xy / P1.HPosition.w;
float2 c = normalize(float2(a.y - b.y, b.x - a.x)) / ScreenSize * 3;
GeometryOutput g0;
g0.HPosition = float4(P0.HPosition.xy + c * P0.HPosition.w, P0.HPosition.zw);
g0.TexCoord = float2( 1.5, 0.0);
GeometryOutput g1;
g1.HPosition = float4(P0.HPosition.xy - c * P0.HPosition.w, P0.HPosition.zw);
g1.TexCoord = float2(-1.5, 0.0);
GeometryOutput g2;
g2.HPosition = float4(P1.HPosition.xy + c * P1.HPosition.w, P1.HPosition.zw);
g2.TexCoord = float2( 1.5, 0.0);
GeometryOutput g3;
g3.HPosition = float4(P1.HPosition.xy - c * P1.HPosition.w, P1.HPosition.zw);
g3.TexCoord = float2(-1.5, 0.0);
OUT.Append(g0);
OUT.Append(g1);
OUT.Append(g2);
OUT.Append(g3);
OUT.RestartStrip();
}
```


The above code is pretty straightforward, except two places I would like to explain further:

- The highlighted
*section 1*does a manual near-plane clipping to ensure all lines passed out are**internal lines**. This is necessary because it’s meaningless to calculate screen position for points behind the camera, which will mess things up. - The keyword
**noperspective**in*section 2*is to tell the rasterizer to interpolate`TexCoord`

in screen space rather than in world space, which is exactly what we want, since we are drawing lines with constant width in pixels.

Finally the pixel shader. Since we already have `TexCoord.x`

represents the distance field, it’s not difficult to fade the pixel base on that to get anti-aliased lines. However, in order to get better AA quality, we have to choose the filter very carefully. It turns out $2^{-2.7 \cdot d \cdot d}$ can fit the **cone filter kernel** 2 very well.

![](../../assets/0a5bdc091a5857d7.png)

Now here is the full PS code, and we are done!

```
float4 AALinePS(in GeometryOutput IN) : SV_Target
{
float a = exp2(-2.7 * IN.TexCoord.x * IN.TexCoord.x);
return float4(LineColor, a);
}
```


-
Eric Chan and Frédo Durand. “Fast Prefiltered Lines”. In GPU Gems 2, Addison-Wesley, 2005, pp. 345–359.

[↩︎](https://atyuwen.github.io#fnref:1) -
McNamara, Robert, Joel McCormack, and Norman P. Jouppi. 2000. “Prefiltered Antialiased Lines Using Half-Plane Distance Functions.” In Proceedings of the ACM SIGGRAPH/Eurographics Workshop on Graphics Hardware, pp. 77–85.

[↩︎](https://atyuwen.github.io#fnref:2)