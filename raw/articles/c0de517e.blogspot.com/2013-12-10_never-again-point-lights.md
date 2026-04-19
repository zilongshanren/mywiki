---
title: 'Never again: point lights'
url: https://c0de517e.blogspot.com/2013/12/never-again-point-lights.html
published: '2013-12-10'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Distant, point, spotlight, am I right? Or maybe you can merge point and spot into an uberlight. No.


Have you ever actually seen a point-light in the real world? It's very rare, isn't it? Even bare-bulbs don't exactly project uniformly in the hemisphere...


If you're working with a baked-GI solution that might not affect you much, in the end you can start with a point, construct a light fixture around it and have GI take care of that. But even in the baked world you'll have analytic lights most often. In deferred, it's even worse. How many games show "blobs" of light due to points being placed around? Too many!


With directional and spots we can circumvent the issue somehow by adding "cookies", 2d projected textures. With points we could use cube textures, but in practice I've seen too many games not doing it (authoring also could be simpler than hand-painting cubes...)


During


[Fight Night](http://www.ea.com/fight-night)(boxing game) one little feature we had was light from camera flashes, which was interesting as you could clearly see (for a fraction of a second) the pattern they made on the canvas (journalists are all around the ring) and there it was the first time I noticed how much point lights suck.
The solution was easy, really, I created a mix of a point and distant light, which gave a nice directional gradient to the flash without a cone shape of spots. You could think of the light as being a point and the "directional" part being a function that made the emission non constant on the hemisphere.




**It's a multiply-add. Do it. Now!**

| Minimum-effort "directional" point |

Another little trick that I employed (which is quite different) is to "mix" point and directional in terms of the incoming light normal on the shaded point (biasing point normals towards a direction), at the time an attempt to create lights that were "area" somehow, softer than pure points. But that was really a hack...

Nowadays you might have heard of IES lights (see

[this](http://www.photometricviewer.com/)and[this](http://www.visual-3d.com/Tools/PhotometricViewer/)for example), which are light emission profiles often measured by light manufacturers (which can be converted to cubemaps, by the way).
I would argue -against- them. I mean sure, if you're going towards a cubemap based solution sure, have that as an option, but IES are really meaningful if you have to go out in the real world and buy a light to match a rendering you did of an architectural piece, if you are modeling fantasy worlds there is no reason to make your artists go through a catalog of light fixtures just to find something that looks interesting. What is the right IES for a pointlight inside a barrel set on fire?



|

A good authoring tool would be imho just a freehand curve, that gets baked into a simple 1d texture (in realtime, please, let your artists experiment interactively), mapped with light direction dot (light position-shaded point).

If you want to be adventurous, you can take a tangent vector for the light and add a second dot product and lookup. And add the ability of coloring the light as well, a lot of lights have non-constant colors as well, go around and have a look (i.e. direct light vs light reflected out of the fixture or passing through semi-transparent material...).


1d lookups are actually -better- than a cubemap cookies, because if you see in real world example many fixtures generate very sharp discontinuities in the light output, which are harder (require much more resolution) to capture in a cubemap...

If you want to be adventurous, you can take a tangent vector for the light and add a second dot product and lookup. And add the ability of coloring the light as well, a lot of lights have non-constant colors as well, go around and have a look (i.e. direct light vs light reflected out of the fixture or passing through semi-transparent material...).

1d lookups are actually -better- than a cubemap cookies, because if you see in real world example many fixtures generate very sharp discontinuities in the light output, which are harder (require much more resolution) to capture in a cubemap...

Exercise left for the reader: bake the light profile approximating a GI solution, automatically adapting it to the enviroment the light was "dropped" in...




## 5 comments:

I'm trying to get cookies working on my lights, and I really liked this article. I'm confused about the part where you use a tangent vector to do a lookup. Do you mean the tangent to the surface you are shading a the tangent to the direction-to-light-vector>

Of the light. An "up" vector if you want.

Oh, I see so you would have a 3D pattern. I have been trying to model my lights after Blender Internal (they let you hand-draw the intensity curve, like you suggest) but for 3D intensity pattern wouldn't it be more expressive to let the artist shape a polyhedron?

You can use a cubemap, which is not uncommon as a real-time implementation of IES lights. Really at the time I wrote this it was mostly a suggestion to do -something- (even cheap) and not keep "bare" lights which are fairly uncommon in most real world scenarios.


From there you can go as complex as you like. The crazies thing I can think of would be to do raytracing of light within its surroundings (fixture, wall) to get a small local light field that would include the nearby occlusion and bounces, and encode it in a cubemap or a volumetric texture of SH (to be more accurate) or something like that... Recently this was published (for offline rendering, just tangentially related) http://flycooler.com/download/luminaire_tog2015_preprint.pdf

Ugh, that is so cool.

Post a Comment