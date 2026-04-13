---
title: Addendum to Mathematica and Skin Rendering
url: http://c0de517e.blogspot.com/2012/11/addendum-to-mathematica-and-skin.html
published: '2012-11-03'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Update: there was a typo in the shader code, I didn't update the screenshot...**

A shader code snippet following

[my work on Penner's scattering approximation](http://c0de517e.blogspot.ca/2011/09/mathematica-and-skin-rendering.html). I'm actually rather sure it can be done better and for cheaper, especially if you "clamp" the radius range to a narrower window, currently it goes too broad on one side while trying to go back to a standard, not wrapped N dot L for large radii, it's not really useful. But, I've already given the Mathematica code so you can do better...

float3 PSSFitFunction(float NdL, float r)

{

float3 a0 = {0.0605, 0.2076, 0.2243};

float3 a1 = {0.0903, 0.1687, 0.2436};

float3 a2 = {-0.0210, -0.0942, -0.1116};

float3 a3 = {0.6896, 0.6762, 0.6480};

float3 a4 = {-0.1110, -0.5023, -0.6703};

float3 a5 = {0.8177, 0.9119, 0.9209};

float3 t = NdL.xxx * (a0*r+a1) + (a2*r+a3);

float3 fade = saturate(a4*r+a5);

return t*t*t * fade + saturate(NdL) * (1-fade);

}
## No comments:

Post a Comment