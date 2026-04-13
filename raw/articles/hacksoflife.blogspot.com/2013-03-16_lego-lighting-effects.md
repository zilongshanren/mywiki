---
title: Lego Lighting Effects
url: http://hacksoflife.blogspot.com/2013/03/lego-lighting-effects.html
author: Benjamin Supnik
published: '2013-03-16'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I was flipping through MOC-train pictures and was struck by


(Compare the first image to


I was able to get smooth shading working (more or less) in BrickSmith, at least as a prototype, and that got me thinking: what are we going to


So I took the only lego set I actually own now (the


Putting this wish list together, I can imagine:[this](http://www.flickr.com/photos/savatheaggie/5474568321/)image. What got my attention is not only that it is a very well done model, but also that it is one of the few images in the photo stream that really pops despite being a computer-graphics render (as opposed to a photo of a real lego set); most of the renderings don't have the same "ooh" factor as real models.(Compare the first image to

[this](http://www.flickr.com/photos/savatheaggie/5454163393/)image from the same set, which appears to be more like a screen capture from a lego editing program - a very simple forward-shaded lighting environment. The first image works because the lighting environment does enough interesting things to make the model start to look like it exists in a real 3-d space.)I was able to get smooth shading working (more or less) in BrickSmith, at least as a prototype, and that got me thinking: what are we going to

*do*with the new rendering engine? Now that we have shaders and smooth normals, what lighting would actually look good? The existing lighting model makes models look like a bit like instructions; it's great for clarity and editing without eye strain, but no one is going to think you're looking at a photo.So I took the only lego set I actually own now (the

[Maersk train](http://shop.lego.com/en-US/Maersk-Train-10219)), and held it up to the window while turning it. I don't actually play with it - it just sits on my shelf, so the parts are still clean and relatively finger-print free. It looks to me like there are a few critical lighting effects that we'll need to capture to get a high quality render. The good news is that they are probably all doable in real time. Here is a brain dump:- Lego bricks have some kind of BDRF - they are highly reflective at some angles, and the reflection strength dies off with angle; the BDRF may be more complicated than a standard exponential specular hilite. Given the small number of part surfaces, it would not be insane to model each specific BDRF with a lookup table texture.
- Normal mapping: it turns out that a square brick doesn't actually have a flat side. There is a subtle bit of 'indent' in the center of the side relative to the corners. I don't know if this is intentional or a limit of the manufacturing process (I'll go with "intentional" since TLC is known for their insane levels of quality control) but there is no question that a flat surface is not actually flat. The amount of curvature depends on the part, and the shape of the curvature appears to have a pattern - the brick wall goes 'out' at the corner, creating tell-tale reflections just inside the bounds of the brick. This effect could potentially be created with texture-based normal mapping.
- The slope bricks have a 'grit' texture etched into the sloped sides; this effectively changes the BDRF. The question then is whether this should be done with a normal map or BDRF tweak. The answer might be to use something like
[LEAN mapping](http://www.csee.umbc.edu/~olano/papers/lean/), e.g. a normal map that produces a correct specularity change when mipmap-filtered. (Again, we could get away with a technique that is considered "expensive" for game content because legos have very few distinct materials and LDraw makes almost no use of textures; that texturing hardware is just sitting waiting for us.) - The brick edges present a difficult problem; they are represented as line segments in LDraw (to make it easy to provide a wire-frame around bricks for instruction-style drawing). In a real lego model, the edges of the bricks appear to be slightly faceted, which makes them feel less sharp. This leads to two effects: specular hilites off the edge of the brick, and 'dark cracks' between bricks, which I would say is essentially self-shadowing or ambient occlusion. My thought is to set up the lines with the average normal of the 'crease' it represents and then use them to overpaint some specularity, but I haven't tried this yet.
- There is slight variation in the direction of the bricks - a modeler can assemble bricks with varying degrees of tightness, and if desired, can leave the bricks a little bit loose to get some variation in their exact orientation. This leads to variations in normals (and thus lighting) as well as self shadowing and more/less visible cracks at their junctions. My thinking is that this could be simulated by applying some tiny offset to the transform of individual bricks.
- While some POV-Ray style renders use cast shadows (including the one I linked to) I think that ambient occlusion might provide better lighting cues. People usually play with and observe legos indoors, and the indoor environment often has heavily diffused lighting.

- Lighting via an environment map (to capture variable changes in diffuse lighting levels with multiple lighting reflection sources) and
- Rendering to a deferred surface, with lines blending changes into the normal vector plane. (Some normal-mapping schemes are reasonably amenable to hardware blending.)
- Lighting with screen space reflectance/ambient occlusion - that is, we walk the neighborhood around our pixel in screen space, capturing shadowing and local color bounce, and lookup the ray in the environment map for rays that escape.

Those questions may also be slightly moot; the LDraw data for parts does not contain normal maps or even surface roughness descriptions, so good input data on the lighting properties of the bricks might not even be available.

But this is all walking before we crawl; smooth normals are not fully coded or debugged, the new renderer hasn't shipped yet, and I still don't have an LOD scheme to cut

[vertex count](http://hacksoflife.blogspot.com/2013/01/instancing-for-bricksmith.html).

## No comments:

## Post a Comment