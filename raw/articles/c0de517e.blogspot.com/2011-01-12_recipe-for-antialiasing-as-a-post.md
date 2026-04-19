---
title: Recipe for antialiasing as a post
url: https://c0de517e.blogspot.com/2011/01/recipe-for-antialiasing-as-post.html
published: '2011-01-12'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I thought that I did post already this little experiment, but I didn't find it on the blog and I had to dig into my old sources...

*1) Identify edges.*(From color? From normals and depth? In practice I've found the latter to be better)



*2) Fit a primitive to edges, find parameters.*A line? A line centered on the pixel? A curve? Most algorithms fit one of the first two.

MLAA for example finds lines from the discrete edge detection, and the key of the algorithm is that is able to find lines even if they are nearly vertical (or horizontal). These lines have long steps when rasterized, and are hard to detect because you have to "look" way far from the pixel you're considering. MLAA uses pattern matching to achieve that, and that's also why it does not fit the GPU too well (at least DX9ish ones)

Simple edge detection is too local, won't know if a horizontal discontinuity is an horizontal line or part of a line at a nearly horizontal angle. Also it won't know how long that line is, so it won't know for how long the line approximation holds, in practice it will work decently only on curves, organic surfaces. This can be remedied by searching in a larger neighborhood, but it's not too simple and of course it costs performance...

*3) Blend along the primitive.*Either identify a "foreground" and "background" color and blend between the two using the coverage of the primitive on the pixel considered, or smooth by integrating (sampling) along the primitive. MLAA does the former, many post-filters do the latter (or a generic isotropic blur) to avoid computing the exact integral of the fitted line through the pixel.

Now how you do that defines your post-aa filter.

[MLAA](http://visual-computing.intel-research.net/publications/papers/2009/mlaa/mlaa.pdf)is currently the most popular algorithm (especially on ps3, where you can use all these SPUs... there is a[GPU version](http://igm.univ-mlv.fr/%7Ebiri/mlaa-gpu/index.php?idmenu=0)but it doesn't seem suited to run on the 360 GPU) and it seems to be almost the "only" choice nowadays but it's quite possible to do something decente even with more "conventional" filters.I started experimenting with this a while ago, to improve the PS3 2x quincunx filter resolve (that is commonly used "against" a 4x MSAA on 360 as PS3 is way slower to do MSAA).

This idea of mixing MSAA and edge filtering is not new,

[this paper](http://developer.amd.com/gpu_assets/AA-HPG09.pdf)from ATI explores it and it's a very interesting read (also its citations, like[this one](http://www.cs.cityu.edu.hk/%7Erynson/papers/tcsvt03.pdf), are a good inspiration)It's important to be able to do this on the samples before the MSAA downscale because otherwise you'll loose information and it's harder to identify geometric discontinuities while preserving detail in the already antialiased (hopefully) interior shaded regions.

Also, as you're running your post effect on the full HD framebuffer, it's fundamental to be as fast as possible. With that in mind I started experimenting with the goal of doing the simplest filter that still looked good. This is what I've ended up with (beware, it's not shader code but Adobe Pixel Bender stuff):

void evaluatePixel() {

float3 orig = sampleLinear(src, outCoord()).rgb;

float3 vb = sampleLinear(src, outCoord() + float2(1,0) ).rgb - sampleLinear(src, outCoord() + float2(-1,0) ).rgb;

float3 hb = sampleLinear(src, outCoord() + float2(0,1) ).rgb - sampleLinear(src, outCoord() + float2(0,-1) ).rgb;

float vg = dot(vb, float3(0.2126, 0.7152, 0.0722));

float hg = dot(hb, float3(0.2126, 0.7152, 0.0722));

float3 col = orig.rgb;

float2 off = float2(hg, -vg); float offl = length(off);

off/=offl;

col += sampleLinear(src, outCoord() + off).rgb + sampleLinear(src, outCoord() - off).rgb;

col/=float3(3,3,3);

float threshold = 0.25;

float blend = offl/threshold; if(blend>1.0) blend = 1.0;

dst.rgb = orig.rgb * (1.0 - blend) + col.rgb * blend; dst.a = 1.0;

}

The results are not too bad... As you can see MLAA is vastly better on straight, clean lines (see the bench) but it's actually a fair bit worse on curves/complex surfaces (see the leaves) and tends to mess/blur things that change often direction (see the metal rods on the left, above the zombie head). Maybe it's a matter of tuning, I used the original MLAA sourcecode from Intel.

![]() |

Original image: Dead Rising 2 without MSAA

## 5 comments:

Thanks for sharing.




Tried it, works somewhat better on our scenes than my attempts - but only really works on almost-diagonal, well defined edges, while MLAA really shines on almost horizontal/vertical edges.

Still can't decide if it's better than nothing; characters are pretty well rounded in their details, so it seems to be a win for them.

Have you seen LucasArts' Force Unleashed II?

Mhm no I didn't know that Force Unleashed 2 did AA tricks, I'll look at it.



I'm actually quite confident I can raise the quality of the post-AA to something closer to MLAA.

We'll see, stay tuned.

Judging from what I see here:


http://www.eurogamer.net/articles/digitalfoundry-lucasarts-on-tfu2-tech-blog-entry

it looks very similar to what I posted (note: you should tune it...)

Force Unleashed's thing works very well on long almost-horizontal or almost-vertical edges, like MLAA.

Post a Comment