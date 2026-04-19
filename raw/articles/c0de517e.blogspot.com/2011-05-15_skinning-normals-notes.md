---
title: Skinning normals notes
url: https://c0de517e.blogspot.com/2011/05/skinning-normals-notes.html
published: '2011-05-15'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Ok, really this is a

[Penultimate](http://itunes.apple.com/us/app/penultimate/id354098826?mt=8)test :) but the defect is real, I think I've read of this the first time in an article about facial animation in Capcom's MT framework engine (that I can't find right now, I think it was related to Resident Evil 5). This is an example in FNC, see the weird lighting under the armpit, a complex area where many bones meet:

Normals in realtime rendering (or rendering in general) are the same as colors.

**We use them all the times but we seldom if ever really reason about them**until an article comes our and teaches the basics of gamma correction or normalmap blending and so on and everyone jump mindlessly on the new "cool" technique without really having any deeper understanding of the problem. I wonder how many renderers really went from the rendering equation to the sRGB colour space... We should do better.

Let's say we derive face normals by averaging the vertices of a face. And that we compute vertex normals by some form of averaging of the faces of a vertex (usually, weighted by the areas). Let's assume that the face areas do not change under skinning. In that case we can compute a set of bone weights and indices that is the average of the bone weights and indices that act upon the faces of a given vertex.



**Errata**: The weights in the note are wrong, for the second vertex they should be 0.75/0.25 as one segment is influenced by the bone 1 with weight 1 (as both their vertices are skinned by that bone) and the other segment of the vertex is influenced by 1,2 with 0.5,0.5, so the vertex should be skinned with bones 1 and 2 with weights 0.75,0.25 (and a similar reasoning applies to the third vertex).*P.S. I still prefer my pens and my notebooks over writing with an iPad with a capacitive pen :(*

**Update (2023):**Sergey Makeev smartly noted that there is even a bigger issue with normals if you allow for bone translation. Translation would not change normals at all, which is clearly wrong. In Fight Night the skeleton did only rotations, so it was not a problem, but in modern facial animation systems you might end up with bones that do a lot of translation instead!

## 3 comments:

"Let's assume that the face areas do not change under skinning."


Isn't this a flawed assumption?

Rim: not too much. Some even compute vertex normals without weighting the faces with areas. Vertex normals (Gouraud shading) are a "hack", the assumption is not too unreasonable.

"Some even compute vertex normals without weighting the faces with areas"


I just came across some code where I did this too, so I do see your point :)

Post a Comment