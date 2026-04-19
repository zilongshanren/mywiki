---
title: Small BRDF visualizer
url: https://c0de517e.blogspot.com/2010/02/small-brdf-visualizer.html
published: '2010-02-28'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Update: There are now at least two tools that do this properly and seriously. This was never a serious BRDF tool, but if you landed here you're probably interested in one.


I've just learned from the

[BRDFLab](http://brdflab.sourceforge.net/)and Disney's[BRDF visualizer](http://www.disneyanimation.com/technology/brdf.html).I've just learned from the

[Real-Time Rendering](http://www.realtimerendering.com/blog/)blog, that Torrance[died](http://www.realtimerendering.com/blog/ken-torrances-accomplishments/)a couple of weeks ago. Can't be a better time to write a BRDF visualizer, that is something that I always wanted to have handy in order to really understand what's going on with different shading models, and approximations.
So today I tried to write a simple vertex shader to visualize and compare shading models. I thought that visualizing them in the BRDF form would be nice (something like

[this](http://graphics.stanford.edu/~smr/brdf/bv/)). Also, I wanted to write this not using Nvidia FXComposer ([shit](http://c0de517e.blogspot.com/2009/09/fix-for-fxcomposer-25-clear-bug.html)).
So I went on a quest to find an FXComposer replacement. It's not the first time I try and fail at that. This is what I found this time:



[Media Player Classic](http://mpc-hc.sourceforge.net/media-player-features.html): Off-topic, but it was surprising for me to find out that the latest version does support HLSL shaders, and you can even edit them while the movie is playing. It's cool and I think I'll put this to a good use to prototype post effects and colour correction.[QShaderEdit](http://code.google.com/p/qshaderedit/): looks nice, it's inspired by the Apple OpenGL Shader Builder, with CG support added to it (GLSL is really ugly). I didn't try it as it's source only, and something tells me that it won't compile so easily with Visual Studio. Also it looks like it does not support scripting.

[glslDevil](http://www.vis.uni-stuttgart.de/glsldevil/): it's not an IDE, only a debugger, and only GLSL. So overall it's useless for my purposes but as a debugger it really looks nice. There is a windows port, so I'll try it some day.

[Lumina](http://lumina.sourceforge.net/): GLSL only, but supports scripting. There is a windows port but the whole project looks discontinued. It's a shame as it seems to be very decent. Maybe someone should pick this up.

[PyOpenGL_Lab](http://www.geeks3d.com/20091008/pyopengl_lab-a-small-lab-for-opengl-tests-without-compilation/): hooks OpenGl to python, plus it provides some utility functions like camera management. It's the slimmed-down version of

[GeeXLab](http://www.geeks3d.com/geexlab/), that I tried and found to be really messy. Overall it looks decent, but no CGFX support and as is, it's not so much better/faster than writing your own testbench in C#/SlimDX. Python seems to be the scripting language with the most wrapper libraries. I even found a

[Cuda](http://mathema.tician.de/software/pycuda)and an

[OpenCL](http://mathema.tician.de/software/pyopencl)binding for it.

In the end I went back, frustrated, to FXComposer (1.8, I use 2.5 only where 1.8 crashes). This is the result, just attach it to a tessellated sphere and bind the LightPos parameter to a point light.




float4x4 ViewProj : ViewProjection;

float4 LightPos : Position

float4 OutColor = {0.3,0,0,1};

#define BRDF_Normal (float4(-1,0,0,0))

void VShader(in float4 inNormal : NORMAL,out float4 outPos : POSITION,out float4 outCol : COLOR)

{

float4 BRDF_OutDir = inNormal;

float4 BRDF_InDir = normalize(LightPos);

float Phong = pow(max(dot(reflect(BRDF_Normal, BRDF_InDir), BRDF_OutDir),0), 10);

float Blinn = pow(max(dot(normalize(BRDF_InDir + BRDF_OutDir), BRDF_Normal),0), 10);

float Lambert = dot(BRDF_InDir, BRDF_Normal);

float BRDF = (Lambert + Phong) / max(dot(BRDF_InDir, BRDF_Normal), 0.01);

BRDF = max(0,BRDF); float OutDirCond = dot(BRDF_Normal, BRDF_OutDir)>0;

outPos = mul(float4((inNormal * BRDF * OutDirCond).xyz, 1), ViewProj);

outCol = OutColor * BRDF;

}

float4 PShader(in float4 inCol : COLOR) : COLOR { return inCol; }

technique t0 { pass p0 {

VertexShader = compile vs_3_0 VShader();

PixelShader = compile ps_3_0 PShader();

}}

## No comments:

Post a Comment