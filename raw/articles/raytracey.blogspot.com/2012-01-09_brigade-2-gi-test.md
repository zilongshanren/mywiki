---
title: Brigade 2 GI test
url: http://raytracey.blogspot.com/2012/01/brigade-2-gi-test.html
author: Sam Lapere
published: '2012-01-09'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just a small test with a Cornell box scene to test diffuse color bleeding with Brigade 2, rendered on my faithful 8600M GT (the female character is a high poly version of Alyx from Half-Life 2 (character model from

[here](http://www.gfx-3d-model.com/category/3d-characters/page/7/)), containing almost 40k triangles and can be moved around the scene in real-time, the spheres are made of triangles):
Some more tests with an area light that show indirect lighting and subtle brownish/greenish color bleeding on the left side of the character:

These scenes use Brigade's multiple importance sampling kernel which drastically reduces the noise in interior scenes compared to the kernel used in previous test scenes (which converged fast because those were open outdoor scenes lit by an HDR skydome).
Brigade's MIS algorithm allows this kind of interior scenes to converge extremely fast as can be seen in

## 3 comments:

I see the color bleeding between the diffuse surfaces, very nice indeed.

if you could make a binary of that, it would be great!

No more binaries for a while, I'm saving them to create a much larger release in a few months :)

Post a Comment