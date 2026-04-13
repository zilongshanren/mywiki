---
title: Tiled Light Culling
url: http://graphicrants.blogspot.com/2012/04/tiled-light-culling.html
author: Brian Karis
published: '2012-04-29'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[GDC talk](http://schedule.gdconf.com/session/6704/Rendering_Technology_of_Prey_2)but that was cancelled due to forces outside my control. If you follow me on twitter (

[@BrianKaris](https://twitter.com/#!/BrianKaris/)) you probably heard all about it. My comments were picked up by the press and quoted in every story about Prey 2 since. That was not my intention but oh, well. So, I will go back to what I was doing which is to talk here about things I am not directly working on.

### Tiled lighting

There has been a lot of talk and excitement recently concerning tiled deferred [1][2] and tiled forward [3] rendering.I’d like to talk about an idea I’ve had on how to do tile culled lighting a little differently.

The core behind either tiled forward or tiled deferred is to cull lights per tile. In other words for each tile, calculate which of the lights on screen affect it. The base level of culling is done by calculating a min and max depth for the tile and using this to construct a frustum. This frustum is intersected with a sphere from the light to determine which lights hit solid geometry in that tile. More complex culling can be done in addition to this such as back faced culling using a normal cone.

This very basic level of culling, sphere vs frustum, only works with the addition of an artificial construct which is the radius of the light. Physically correct light falloff is inverse squared.

### Light falloff

Small tangent I've been meaning to talk about for a while. To calculate the correct falloff from a sphere or disk light you should use these two equations [4]:


Falloff:

$$Sphere = \frac{r^2}{d^2}$$

$$Disk = \frac{r^2}{r^2+d^2}$$


If you are dealing with light values in lumens you can replace the r^2 factor with 1. For a sphere light this gives you 1/d^2 which is what you expected. The reason I bring this up is I found it very helpful in understanding why the radiance appears to approach infinity when the distance to the light approaches zero. Put a light bulb on the ground and this obviously isn’t true. The truth from the above equation is the falloff approaches 1 when the distance to the sphere approaches zero. This gets hidden when the units change from lux to lumens and the surface area gets factored out. The moral of the story is don’t allow surfaces to penetrate the shape of a light because the math will not be correct anymore.



Falloff:

$$Sphere = \frac{r^2}{d^2}$$

$$Disk = \frac{r^2}{r^2+d^2}$$

If you are dealing with light values in lumens you can replace the r^2 factor with 1. For a sphere light this gives you 1/d^2 which is what you expected. The reason I bring this up is I found it very helpful in understanding why the radiance appears to approach infinity when the distance to the light approaches zero. Put a light bulb on the ground and this obviously isn’t true. The truth from the above equation is the falloff approaches 1 when the distance to the sphere approaches zero. This gets hidden when the units change from lux to lumens and the surface area gets factored out. The moral of the story is don’t allow surfaces to penetrate the shape of a light because the math will not be correct anymore.

### Culling inverse squared falloff

Back to tiled culling. Inverse squared falloff means there is no distance in which the light contributes zero illumination. This is very inconvenient for a game world filled with lights. Two possibilities, first is to subtract a constant term from the falloff but max with 0. The second is windowing the falloff with something like (1-d^2/a^2)^2. The first loses energy over the entire influence of the light. The second loses energy only away from the source. I should note the tolerance should be proportional to the lights intensity. For simplicity I will use the following for this post:

$$Falloff = max( 0, \frac{1}{d^2}-tolerance)$$


The distance cutoff can be thought of as an error tolerance per light. Unfortunately glossy specular doesn’t work well in this framework at all. The intensity of a glossy, energy conserving specular highlight, even for a dielectric, will be WAY higher than the lambert diffuse. This spoils that idea of the distance falloff working as an error tolerance for both diffuse and specular because they are at completely different scales. In other words, for glossy specular, the distance will have to be very large for even a moderate tolerance, compared to diffuse.


This points to there being two different tolerances, one for diffuse the other for specular. If these both just affect the radius of influence we might as well just set the radius of both as the maximum because diffuse doesn’t take anything more to calculate than specular. Fortunately, maximum intensity of the specular inversely scales with the size of the highlight. This of course is the entire point of energy conservation but energy conservation helps us in culling. The higher the gloss, the larger the radius of influence the tighter the cone of influencing normals.


If it isn’t clear what I mean, think of a chrome ball. With a mirror finish, a light source, even as dim as a candle, is visible at really large distances. The important area on the ball is very small, just the size of the candle flame’s reflection. The less glossy the ball, the less distance the light source is visible but the more area on the ball the specular highlight covers.


Before we can cull using this information we need specular to go to zero past a tolerance just like distance falloff. The easiest is to subtract the tolerance from the specular distribution and max it with zero. For simplicity I will use phong for this post:

$$Phong = max( 0, \frac{n+2}{2}dot(L,R)^n-tolerance)$$



$$Falloff = max( 0, \frac{1}{d^2}-tolerance)$$

The distance cutoff can be thought of as an error tolerance per light. Unfortunately glossy specular doesn’t work well in this framework at all. The intensity of a glossy, energy conserving specular highlight, even for a dielectric, will be WAY higher than the lambert diffuse. This spoils that idea of the distance falloff working as an error tolerance for both diffuse and specular because they are at completely different scales. In other words, for glossy specular, the distance will have to be very large for even a moderate tolerance, compared to diffuse.

This points to there being two different tolerances, one for diffuse the other for specular. If these both just affect the radius of influence we might as well just set the radius of both as the maximum because diffuse doesn’t take anything more to calculate than specular. Fortunately, maximum intensity of the specular inversely scales with the size of the highlight. This of course is the entire point of energy conservation but energy conservation helps us in culling. The higher the gloss, the larger the radius of influence the tighter the cone of influencing normals.

If it isn’t clear what I mean, think of a chrome ball. With a mirror finish, a light source, even as dim as a candle, is visible at really large distances. The important area on the ball is very small, just the size of the candle flame’s reflection. The less glossy the ball, the less distance the light source is visible but the more area on the ball the specular highlight covers.

Before we can cull using this information we need specular to go to zero past a tolerance just like distance falloff. The easiest is to subtract the tolerance from the specular distribution and max it with zero. For simplicity I will use phong for this post:

$$Phong = max( 0, \frac{n+2}{2}dot(L,R)^n-tolerance)$$

### Specular cone culling

This nicely maps to a cone of L vectors per pixel that will give a non-zero specular highlight.


Cone axis:

$$R = 2 N dot( N, V ) - V$$


Cone angle:

$$Angle = acos \left( \sqrt[n]{\frac{2 tolerance}{n+2}} \right)$$


Just like how a normal cone can be generated for the means of back face culling, these specular cones can be unioned for the tile and used to cull. We can now cull specular on a per tile basis which is what is exciting about tiled light culling.


I should mention the two culling factors need to actually be combined for specular. The sphere for falloff culling needs to expand based on gloss. The (n+2)/2 should be rolled into the distance falloff which leaves angle as just acos(tolerance^(1/n)). I’ve leave these details as an exercise for the reader. Now, to be clear I'm not advocating having diffuse and specular light lists. I'm suggesting culling the light if diffuse is below tolerance AND spec is below tolerance.

Cone axis:

$$R = 2 N dot( N, V ) - V$$

Cone angle:

$$Angle = acos \left( \sqrt[n]{\frac{2 tolerance}{n+2}} \right)$$

Just like how a normal cone can be generated for the means of back face culling, these specular cones can be unioned for the tile and used to cull. We can now cull specular on a per tile basis which is what is exciting about tiled light culling.

I should mention the two culling factors need to actually be combined for specular. The sphere for falloff culling needs to expand based on gloss. The (n+2)/2 should be rolled into the distance falloff which leaves angle as just acos(tolerance^(1/n)). I’ve leave these details as an exercise for the reader. Now, to be clear I'm not advocating having diffuse and specular light lists. I'm suggesting culling the light if diffuse is below tolerance AND spec is below tolerance.

This leaves us with a scheme much like biased importance sampling. I haven’t tried this so I can’t comment on how practical it is but it has the potential to produce much more lively reflective surfaces due to having more specular highlights for minimal increase in cost. It also is nice to know your image is off by a known error tolerance from ground truth (per light in respect to shading).

The way I handle this light falloff business for current gen in P2 is by having all lighting beyond the artist set bounds of the deferred light get precalculated. For diffuse falloff I take what was truncated from the deferred light and add it to the lightmap (and SH probes). For specular I add it to the environment map. This means I can maintain the inverse squared light falloff and not lose any energy. I just split it into runtime and precalculated portions. Probably most important, light sources that are distant still show up in glossy reflections. This new culling idea may get that without the slop that comes from baking it into fixed representations.

I intended to also talk about how to add shadows but this is getting long. I'll save it for the next post.

References:

[1]

[http://visual-computing.intel-research.net/art/publications/deferred_rendering/](http://visual-computing.intel-research.net/art/publications/deferred_rendering/)

[2]

[http://www.slideshare.net/DICEStudio/spubased-deferred-shading-in-battlefield-3-for-playstation-3](http://www.slideshare.net/DICEStudio/spubased-deferred-shading-in-battlefield-3-for-playstation-3)

[3]

[http://aras-p.info/blog/2012/03/27/tiled-forward-shading-links/](http://aras-p.info/blog/2012/03/27/tiled-forward-shading-links/)

[4]

[http://www.iquilezles.org/www/articles/sphereao/sphereao.htm](http://www.iquilezles.org/www/articles/sphereao/sphereao.htm)

## 2 comments:

Hi, i dont get the statement " you are dealing with light values in lumens you can replace the r^2 factor with 1". Is it possible that you explain it more ? Thank you

A lumen (lm) is a unit of the amount of light emitted in any direction from a light source. It is independent from surface area or distance. The r^2/d^2 formula makes sense if the units of the light source were in lux, which is lm/m^2. Perhaps a more accurate thing to say is replace the r^2 with a constant but unless you have a camera model that you are trying to exactly match to the settings of a real world camera there will always be an exposure fudge factor which can nicely eat up any arbitrary constants. Maybe I should write a post about this concept as it simplifies so many physically based rendering formulas for us game guys that the FX guys can't necessarily take advantage of.

Post a Comment