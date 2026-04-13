---
title: Speed of Light
url: https://outerra.blogspot.com/2010/10/speed-of-light.html
author: Outerra
published: '2010-10-31'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*actually*is by flying away from the planet in Outerra at that speed. Now I've made a short video showing exactly that - flying away from the surface to space, and then returning back (but overshooting past it).

And while the speed is indeed great, one can feel that's also terribly slow when considering the extents of space ..

## 6 comments:

Would it be possible to create a nuclear bomb, ICBMs and such? I want to play DEFCON with this engine

Destructing the terrain will be possible, even on such large scales. Though getting all the secondary effects worked out won't be trivial.

Great video Brano. Are you using your logarithmic depth buffer for this scene? When the viewer is very far from Earth, is there still enough precision in a single frustum? Are you dynamically pushing out the near plane as the distance increases?


Thanks!

Patrick

Yes, it's still the logarithmic one, I'm just setting the far plane adaptively, but even that is not necessary. Near plane is always at 0.001m, because in logarithmic buffer it doesn't affect the precision.



Still plenty of resolution - logarithmic depth is specific in that the resolution is proportional to the size of object on the screen at given distance. That practically means that rendered objects are always getting enough resolution while they are visible.

It truly feels "magic", mainly after being treated by the normal depth buffer all those years :)

I am a big fan of this approach. I also wanted to ask how it affects your content creation pipeline since every shader needs to be modified. Do artists author shaders without logarithm Z, then Outerra modifies the shader? Or does Outerra provide a GLSL function to call that is stubbed out in an authoring tool such as Maya, etc?

Well, we are making all our shaders ourselves, and putting requirements on the output from the modeling tools.

We will have our own material system, as is usual with game engines, so there's no need to handle this issue now. But since you are asking - it should be relatively easy, just few lines inserted into the shader code.

Post a Comment