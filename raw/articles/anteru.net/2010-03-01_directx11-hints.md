---
title: DirectX11 hints ...
url: https://anteru.net/blog/2010/directx11-hints
published: '2010-03-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Some stuff that might be useful if you’re getting started with DX11:

-
Tesselation:

- If you get
`error X4577: Not all elements of SV_Position were written`

, make sure to write 4 elements positions in your domain shader. `error X3502: tessfactor inputs missing`

: For triangles and quads, you have to write both`SV_TessFactor`

and`SV_InsideTessFactor`

. The first determines the number of subdivisions for each edge, the second the internal subdivision. You should try to keep them somehow together, as widely varying values will result in totally broken polygons along the edge (basically, you’ll get vertices with a very high valence).- Freeze when rendering: Make sure to change your topology to
`D3D11_PRIMITIVE_TOPOLOGY_<N>_CONTROL_POINT_PATCHLIST`

, withbeing equal to the number of control points expected by your hull shader. Rendering using for instance `D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST`

freezes my machine until Windows 7 resets the driver

- If you get
-
Compute shader:

`D3D11: WARNING: ID3D11DeviceContext::OMSetRenderTargets: Resource being set to OM RenderTarget slot 1 is still bound on input! [ STATE_SETTING WARNING #9: DEVICE_OMSETRENDERTARGETS_HAZARD ]````D3D11: WARNING: ID3D11DeviceContext::OMSetRenderTargets[AndUnorderedAccessViews]: Forcing CS shader resource slot 1 to NULL. [ STATE_SETTING WARNING #2097317: DEVICE_CSSETSHADERRESOURCES_HAZARD ]`

Easy, just make sure you unbind all resources after calling`Dispatch`

by using`CSSetShaderResources`

and an array of`nullptr`

(or plain NULL, in pre-C++-0x days) resources.- In order to create a RW texture, use a
`D3D11_TEXTURE2D_DESC`

and specify`D3D11_BIND_SHADER_RESOURCE | D3D11_BIND_UNORDERED_ACCESS`

for binding. Then, just create an`UnorderedAccessView`

on it. - Parameter binding has to be done in order. Use
`register (tN)`

for textures and structured buffers.`uN`

is for unordered access views. I’ve put my constant buffers into`bN`

, just in case.

-
HLSL:

- If you need infinity, just use
`float i = 1.#INF`

.

- If you need infinity, just use

So much for starts, I really do hope Microsoft improves the documentation of these parts, as it’s mostly trial&error for many things, despite having a nice debug layer on the runtime. Ah and yes, if anyone at ATI reads this: Crashing the driver in case of user errors is not helpful ;) I’ve seen plenty of freezes while doing CS development which required me to reboot; it’s slightly better with tessellation as Windows seems to be able to restart the driver each time.