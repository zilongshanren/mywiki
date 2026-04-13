---
title: Graphics Programming weekly - Issue 13 — October 22, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-13/
author: Jendrik Illner
published: '2017-10-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[VK_KHR_dedicated_allocation unofficial manual](http://asawicki.info/articles/VK_KHR_dedicated_allocation.php5) [[wayback-archive]](https://web.archive.org/web/20171023035149/http://asawicki.info/articles/VK_KHR_dedicated_allocation.php5)

- extension allows the driver to inform application that separate allocations are preferred
- nvidia and intel need this extension to allow extra optimizations
- how to use the extension

[Material layering](https://dakrunch.blogspot.ca/2017/10/material-layering.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171023035231/https://dakrunch.blogspot.ca/2017/10/material-layering.html?m=1)

- overview of different techniques
- Color Layering
- shade each layer and blend the results

- Pattern Layering
- blending the inputs and shading once with that
- discussion of problems


[Perceptually uniform color spaces](https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/) [[wayback-archive]](https://web.archive.org/web/20211215204701/https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/)

- Why is sRGB not linear?
- and what problems this causes when working with sRGB colors
- HSLuv color space
- human-friendly HSL
- identical lightness = equally bright
- same saturation = same perceived color purity


[Master Thesis: Cross-Compiling Shading Languages](https://github.com/LukasBanana/XShaderCompiler/releases/tag/master-thesis) [[wayback-archive]](http://web.archive.org/web/20171020141723/https://github.com/LukasBanana/XShaderCompiler/releases/tag/master-thesis)

- using source-to-source compiler (HLSL to GLSL)
- overview of different models
- “translation” of concept differences between shading languages
- implementation overview
- source code

[A Temporal stable Distance to Edge Anti-Aliasing Technique for GCN architecture](http://www.diva-portal.org/smash/get/diva2:843104/FULLTEXT02) [[wayback-archive]](http://web.archive.org/web/20171016152004/http://www.diva-portal.org/smash/get/diva2:843104/FULLTEXT02)

- master thesis produced at EA DICE
- idea, store the distance from the nearest edge in all pixels + extra post-pass blurs neighbors with each other if an edge is shared by the pixel pair
- how to take advantage of GCN hardware for this

- what are deferred shading limitations
- how does tiled deferred improve and solve some of the limitations
- Forward+
- how does it work
- comparison to deferred and classical forward shading
- how to extend to Clustered


[Volume Tiled Forward Shading](https://www.3dgep.com/volume-tiled-forward-shading/) [[wayback-archive]](https://web.archive.org/web/20171023035332/https://www.3dgep.com/volume-tiled-forward-shading/)

- master thesis
- aims to improve upon Clustered forward shading
- optimizes mainly the light assignment phase
- done by using a BVH( Bounding Volume Hierarchy) for the lights


[Galaxy GameDev](http://developer.samsung.com/game) [[wayback-archive]](http://web.archive.org/web/20160116231623/http://developer.samsung.com:80/game)

- collection of resource to achieve best results on the mali GPUs in Galaxy phones
- especially interesting:
[Vulkan Usage Recommendations](http://developer.samsung.com/game/usage)[[wayback-archive]](https://web.archive.org/web/20171023035452/http://developer.samsung.com/game/usage)

- Vulkan layer to validate against the Mali Application Developer Best Practices
- example of the output:
[https://twitter.com/SaschaWillems2/status/921101878364196864?s=09](https://twitter.com/SaschaWillems2/status/921101878364196864?s=09) - can be run on any vulkan device

[Generating Blue Noise Sample Points With Mitchell’s Best Candidate Algorithm](https://blog.demofox.org/2017/10/20/generating-blue-noise-sample-points-with-mitchells-best-candidate-algorithm/amp/) [[wayback-archive]](https://web.archive.org/web/20171023035600/https://blog.demofox.org/2017/10/20/generating-blue-noise-sample-points-with-mitchells-best-candidate-algorithm/amp/)

- explanation of regular, white and blue noise sampling
- and algorithm overview to generate blue noise (with source code)

[Signed Octahedron Normal Encoding](http://johnwhite3d.blogspot.ca/2017/10/signed-octahedron-normal-encoding.html) [[wayback-archive]](http://web.archive.org/web/20171021042003/http://johnwhite3d.blogspot.ca/2017/10/signed-octahedron-normal-encoding.html)

- extending Octahedron encoding for normals with an extra sign bit
- better precision

[Games Look Bad, Part 1: HDR and Tone Mapping](https://ventspace.wordpress.com/2017/10/20/games-look-bad-part-1-hdr-and-tone-mapping/amp/) [[wayback-archive]](https://web.archive.org/web/20171023035657/https://ventspace.wordpress.com/2017/10/20/games-look-bad-part-1-hdr-and-tone-mapping/amp/)

- subjective discussion of the visual/art direction aspects of HDR and color mapping in games

- command line tool for converting 3D model assets from FBX to glTF 2.0

[Compilation Pipeline in the DirectX Compiler](https://blogs.msdn.microsoft.com/marcelolr/2017/10/13/compilation-pipeline-in-the-directx-compiler/) [[wayback-archive]](https://web.archive.org/web/20171023035756/https://blogs.msdn.microsoft.com/marcelolr/2017/10/13/compilation-pipeline-in-the-directx-compiler/)

- high level overview how the compiler flow is implemented

[Computing the Area of a Convex Polygon](https://erkaman.github.io/posts/area_convex_polygon.html) [[wayback-archive]](http://web.archive.org/web/20171015235638/https://erkaman.github.io/posts/area_convex_polygon.html)

- clear and good to follow derivation