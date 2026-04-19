---
title: Optimizing AMD FSR for Mobiles
url: https://atyuwen.github.io/posts/optimizing-fsr/
published: '2021-08-25'
source_blog: C++ Minor
source_site: https://atyuwen.github.io/
category: graphics
fetched: '2026-04-19'
---

Recently AMD released its super resolution algorithm named [FidelityFX Super Resolution (FSR)](https://gpuopen.com/fidelityfx-superresolution/). Compare to its competitor [DLSS](https://www.nvidia.com/en-us/geforce/technologies/dlss/) that can only be enabled on RTX capable cards, FSR doesn’t require any particular hardware support, which makes it very attractive for cross-platform games. However, although FSR is highly optimized and runs efficiently on PCs, it is overweight on Mobiles. This article describes how we optimize FSR greatly on an iPhone 12 without sacrificing too much image quality.

*Here is a very brief introduction to the FSR algorithm. You can find more details from this Siggraph talk.*

FSR is a two-pass algorithm. The first pass, EASU (Edge Adaptive Spatial Upsamling), is for upscaling. EASU uses a 12-tap pattern as following:

```
b c
e f g h
i j k l
n o
```


These 12 taps are convoluted using a stretched lanczos(2) kernel. The stretch factor is determined from the gradients of nearby pixels. In a nutshell, the final shaped filter is an elliptical kernel whose major axis is perpendicular to the gradient of the current pixel.

The second pass is called RCAS (Robust Contract Adaptive Sharpening), which is used for enhancing the image details. RCAS uses a 5 tap sharpening operator in a cross pattern:

```
w
w 1 w
w
```


The negative weight ‘w’ is carefully chosen per pixel to avoid clipping (exceeds the [0, 1] range).

We integrated AMD FSR into our engine, and it worked great on PCs. Good performance and nice image quality, AMD YES!!!. Then we tested it on an iPhone 12 1 with great expectations, but the result frustrated us a lot. The EASU pass takes about 5.4 ms, and RCAS takes about 0.9 ms

. A 6.3 ms cost in total is absolutely unacceptable.

[2](https://atyuwen.github.io#fn:2)Ok, can we optimize it? Because the cost of the RCAS is reasonable to some extent, our attention is focused on the EASU pass. After several attempts, we managed to reduce the EASU cost from 5.4 ms to 1.8 ms, which is apparently a big win. The following describes how we do that.

At first we used the fp32 version of EASU for simplicity, but on mobile devices fp16 operations are basically twice the throughput of fp32 operations. Since our shader system doesn’t support uint16/int16, we have to tweak the original `FsrEasuH`

code a little bit to make it compiles. Simple modification but high profit, the fp16 version only takes 4.7 ms.

Since EASU uses a lanczos kernel which has negative lobes, ringing artifacts may appear along the strong edges. To eliminate ringing, EASU clips the filtered result against the min-max value from the nearest 2x2 quad. This deringing process spawns a lot of arithmetic instructions. I tried to remove the clipping code completely, then the cost of EASU was reduced to 4.3 ms, another 0.4 ms saved! But how is the ringing? It surprised me that the artifacts are barely noticeable except in some rare cases, I’m comfortable with that.

The EASU pass has an analysis phase to determine the stretch and rotation of the lanczos kernel. In this phase, the analysis routine `FsrEasuSetH`

is called 4 times and the outputs are bilinearly interpolated. Instead of computing 4 times and interpolating the outputs，can we interpolate the inputs and call `FsrEasuSetH`

once? In theory it won’t give you the correct result for any non-linear functions, but let’s try it. I modified the analysis process like this:

```
// Compute bilinear weight.
// x y
// z w
AH4 ww = AH4_(0.0);
ww.x =(AH1_(1.0)-ppp.x)*(AH1_(1.0)-ppp.y);
ww.y = ppp.x *(AH1_(1.0)-ppp.y);
ww.z =(AF1_(1.0)-ppp.x)* ppp.y ;
ww.w = ppp.x * ppp.y ;
// Direction is the '+' diff.
// A
// B C D
// E
AH1 lA = dot(ww, AH4(bL, cL, fL, gL));
AH1 lB = dot(ww, AH4(eL, fL, iL, jL));
AH1 lC = dot(ww, AH4(fL, gL, jL, kL));
AH1 lD = dot(ww, AH4(gL, hL, kL, lL));
AH1 lE = dot(ww, AH4(jL, kL, nL, oL));
// Here FsrEasuSetH is inlined as following:
AH1 dc=lD-lC;
AH1 cb=lC-lB;
AH1 lenX=max(abs(dc),abs(cb));
lenX=ARcpH1(lenX);
AH1 dirX=lD-lB;
lenX=ASatH1(abs(dirX)*lenX);
lenX*=lenX;
// Repeat for the y axis.
AH1 ec=lE-lC;
AH1 ca=lC-lA;
AH1 lenY=max(abs(ec),abs(ca));
lenY=ARcpH1(lenY);
AH1 dirY=lE-lA;
lenY=ASatH1(abs(dirY)*lenY);
AH1 len = lenY * lenY + lenX;
AH2 dir = AH2(dirX, dirY);
```


It’s such a rude simplification, with which the EASU cost comes to 3.8 ms. But does this decrease the upscaling quality? Not very much! The edge features are still preserved very well, I can hardly tell the difference between before and after.

For non-edge pixels, the original EASU still accumulates all the 12 taps. An intuitive idea for optimizing this case is to use a simple bilinear interpolation instead:

```
AH2 dir2=dir*dir;
AH1 dirR=dir2.x+dir2.y;
if (dirR<AH1_(1.0/64.0)) {
// Early quit for non-edge pixels
pix.r = dot(ww, AH4(fR, gR, jR, kR));
pix.g = dot(ww, AH4(fG, gG, jG, kG));
pix.b = dot(ww, AH4(fB, gB, jB, kB));
return;
}
```


Since most threadgroups go into this early-quit branch, the cost should be reduced a lot. But after profiling we only see a 0.2 ms improvement. Although the ALU pressure reduced rapidly, the GPU counters show that now the shader is completely texture bound.

So we have to optimize the TEX ops. Let’s focus on the early-quit code path: In this path, we only need 5 bilinearly interpolated lumas to ensure this pixel falls into the non-edge case. How about we sample these 5 taps directly using a bilinear sampler, and defer other taps until we really need them? Not only can it save texture fetches for the early-quit path, but it also saves some ALUs that do the bilinear interpolation manually.

```
AF2 pp=(ip)*(con0.xy)+(con0.zw);
AF2 tc=(pp+AF2_(0.5))*con1.xy;
AH3 sA=FsrEasuSampleH(tc-AF2(0, con1.y));
AH3 sB=FsrEasuSampleH(tc-AF2(con1.x, 0));
AH3 sC=FsrEasuSampleH(tc);
AH3 sD=FsrEasuSampleH(tc+AF2(con1.x, 0));
AH3 sE=FsrEasuSampleH(tc+AF2(0, con1.y));
AH1 lA=sA.r*AH1_(0.5)+sA.g;
AH1 lB=sB.r*AH1_(0.5)+sB.g;
AH1 lC=sC.r*AH1_(0.5)+sC.g;
AH1 lD=sD.r*AH1_(0.5)+sD.g;
AH1 lE=sE.r*AH1_(0.5)+sE.g;
```


This change improves the performance dramatically, the EASU cost goes from 3.6 ms to 1.8 ms. Now the total cost of FSR is 1.8 ms (EASU) + 0.9 ms (RCAS) = 2.7 ms. Don’t forget without FSR we still need a pass to copy the offscreen target to back buffer, which takes about 0.7 ms. So the net cost of our optimized FSR is 2.7 ms - 0.7 ms = 2.0 ms. Not extremely efficient but we are satisfied.

OK, that’s it. The full source code is listed below ([Gist link](https://gist.github.com/atyuwen/78d6e810e6d0f7fd4aa6207d416f2eeb)), hope you find it useful. We also made a [sample based on the official FSR demo](https://github.com/atyuwen/FidelityFX-FSR), you can play with it and compare the quality of our optimized version with the original. If you have any questions or have other ideas to optimize it further, please don’t hesitate to leave a comment.