---
title: Subpixel Reconstruction Antialiasing
url: https://anteru.net/research/subpixel-reconstruction-antialiasing
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Subpixel Reconstruction Antialiasing (SRAA) combines singlepixel (1x) shading with subpixel visibility to create antialiased images without increasing the shading cost. SRAA targets deferred shading renderers, which cannot use multisample antialiasing. SRAA operates as a post-process on a rendered image with super-resolution depth and normal buffers, so it can be incorporated into an existing renderer without modifying the shaders. In this way SRAA resembles Morphological Antialiasing (MLAA), but the new algorithm can better respect geometric boundaries and has fixed runtime independent of scene and image complexity. SRAA benefits shading-bound applications. For example, our implementation evaluates SRAA in 1.8 ms (1280x720) to yield antialiasing quality comparable to 4-16x shading. Thus SRAA would produce a net speedup over supersampling for applications that spend 1 ms or more on shading; for comparison, most modern games spend 5-10 ms shading. We also describe simplifications that increase performance by reducing quality.

@InProceedings{CML11,author="Chajdas, Matth{\"a}us G. and Mc{G}uire, Morgan and Luebke, David",title="Subpixel Reconstruction Antialiasing",booktitle="Proceedings of the ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games",year="2011",publisher="ACM Press"}

Kernel source

float3normal(intx,inty){returnnormalBuffer.Get(x,y)*2.0-make_float3(1,1,1);}floatdepth(intx,inty){returndepthBuffer.Get(x,y);}floatbilateral(float3centerN,floatcenterZ,float3tapN,floattapZ){returnexp(-scale*max((1.0-dot(centerN,tapN)),depthScale*abs(centerZ-tapZ)));}// Iterate the "center" (cx, cy) of the filter// over the samples in the pixel at (x, y)floatweights[9]={0};for(intcy=y;cy<(y+2);++cy){for(intcx=x;cx<(x+2);++cx){float3N=normal(cx,cy);floatZ=depth(cx,cy);floattmpWeights[9]={0};floatsum=0.0f;// Iterate over the neighboring samplesfor(intj=0;j<3;++j){for(inti=0;i<3;++i){// If inside filter supportif((abs(i-1-cx)<=1)&&(abs(j-1-cy)<=1)){inttapX=x+i-1;inttapY=y+j-1;// Compute the filter weightfloatw=bilateral(N,Z,normal(tapX,tapY),depth(tapX,tapY));tmpWeights[i+j*3]=w;sum+=w;}}}for(intt=0;t<9;++t){weights[t]+=tmpWeights[t]/sum;}}}// Apply the filterfloat3result=make_float3(0,0,0);for(intj=0;j<3;++j){for(inti=0;i<3;++i){result+=weights[i+j*3]*0.25*colorBuffer.Get(x+i-1,y+j-1);}}