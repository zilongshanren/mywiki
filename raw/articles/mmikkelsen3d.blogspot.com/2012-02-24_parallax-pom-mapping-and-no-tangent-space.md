---
title: Parallax/POM mapping and no tangent space.
url: http://mmikkelsen3d.blogspot.com/2012/02/parallaxpoc-mapping-and-no-tangent.html
author: Morten S Mikkelsen
published: '2012-02-24'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Since I wrote this post I've written a new technical paper called "Surface Gradient Based Bump Mapping Framework" which does a better and more complete job describing the following.**

**All my papers can be found at**

[https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html](https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html)I thought I would do yet another follow up post regarding thoughts on

[Parallax](https://www8.cs.umu.se/kurser/5DV051/VT09/lab/parallax_mapping.pdf)/POM mapping

[without the use of conventional tangent space](http://mmikkelsen3d.blogspot.com/2011/07/derivative-maps.html). A lot of the terms involved are terms we already have when doing bump mapping using either derivative or height maps.

// terms shared between bump and pom

float2 TexDx = ddx(In.texST);

float2 TexDy = ddy(In.texST);

float3 vSigmaX = ddx(surf_pos);

float3 vSigmaY = ddy(surf_pos);

float3 vN = surf_norm; // normalized

float3 vR1 = cross(vSigmaY, vN);

float3 vR2 = cross(vN, vSigmaX);

float fDet = dot(vSigmaX, vR1);

// specific to Parallax/POM

float3 vV = vView; // normalized view vector in same space as surf_pos and vN

float2 vProjVscr = (1/fDet) * float2( dot(vR1, vV), dot(vR2, vV) );

float2 vProjVtex = TexDx*vProjVscr.x + TexDy*vProjVscr.y;

The resulting 2D vector vProjVtex is the offset vector in normalized texture space which corresponds to moving along the surface of the object by the plane projected view vector which is exactly what we want for POM. The remaining work is done the usual way.


The magnitude of vProjVtex (in normalized texture space) will correspond to the magnitude of the projected view vector at the surface. To obtain the third component of the transformed view vector the applied bump_scale must be taken into account. This is done using the following line of code:


float vProjVtexZ = dot(vN, vV) / bump_scale;


If we consider T the texture coordinate and the surface gradient of T a 2x3 matrix then an alternative way to think of how we obtain vProjVtex is through the use of surface gradients. One per component of the texture coordinate since each of these represent a scalar field.


float2 vProjVtex = mul(SurfGrad(T), vView)



The first row of SurfGrad(T) is equal to (1/fDet)*(TexDx.x*vR1 + TexDy.x*vR2) and similar for the second row but using the .y components of TexDx and TexDy. In practice it doesn't really simplify the code much unless we need to transform multiple vectors but it's a fun fact :)


Note that one of the observations made in the



The magnitude of vProjVtex (in normalized texture space) will correspond to the magnitude of the projected view vector at the surface. To obtain the third component of the transformed view vector the applied bump_scale must be taken into account. This is done using the following line of code:

float vProjVtexZ = dot(vN, vV) / bump_scale;

If we consider T the texture coordinate and the surface gradient of T a 2x3 matrix then an alternative way to think of how we obtain vProjVtex is through the use of surface gradients. One per component of the texture coordinate since each of these represent a scalar field.

float2 vProjVtex = mul(SurfGrad(T), vView)

The first row of SurfGrad(T) is equal to (1/fDet)*(TexDx.x*vR1 + TexDy.x*vR2) and similar for the second row but using the .y components of TexDx and TexDy. In practice it doesn't really simplify the code much unless we need to transform multiple vectors but it's a fun fact :)

Note that one of the observations made in the

[paper](https://www.dropbox.com/s/l1yl164jb3rhomq/mm_sfgrad_bump.pdf?dl=0)is that the surface gradient of a given scalar field can be obtained using any parametrization of the surface and the field (**eq. 3**). For a scalar field defined on a volume we can (though not required) use**eq. 2**instead to obtain the surface gradient.
This comment has been removed by a blog administrator.

ReplyDelete