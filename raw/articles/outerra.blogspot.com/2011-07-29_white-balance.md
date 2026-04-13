---
title: White balance
url: https://outerra.blogspot.com/2011/07/white-balance.html
author: Outerra
published: '2011-07-29'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous post](http://outerra.blogspot.com/2011/07/fog-and-dust.html), I observed a weird thing happening: the fog wasn't white, as I expected, but it had a dirty Beige tint making it look a bit like a smog or something. But since the implementation didn't use different absorption and scattering coefficients for RGB components, and thus the color of the sun light shouldn't have been modified, I thought it was a bug, and neglected it until most of other issues were solved.

But then, after inspecting all the code paths, I came to the only conclusion that the computation is right and the problem must be in the interpretation. So I tried to convince myself that the fog must be white, and the tint actually isn't there. Almost made it, too.

But the machine coldly asserted that the color wasn't white as well. Didn't bother with any hinting as to why, though.

Apparently the incoming light that was scattering on fog particles was already this color, even though the sun color was not modified in any way, unlike in the previous

[experiments](http://outerra.blogspot.com/2011/07/alien-planet-earth.html).

**Interpretation?**

The thing is that sunlight really gets modified a bit until it arrives to the planet surface. The same thing that is responsible for blue sky causes this: a small part of the blue light (and a smaller part of the green light too) gets scattered away from the sun ray. What comes down here has a slightly shifted spectrum.

But how come we see the fog white in real life?

Turns out, everything is fake.

The way we perceive colors is purely subjective interpretation of a part of the electromagnetic spectrum.

And as it is easier for the brain to orient in the environment when the

[sensors don't move](http://www.youtube.com/watch?v=KEyvvAiIwYc), it is also simpler to stick with constant properties on objects. Our brain "knows" that a sheet of paper is white, and so it will make it appear white in wildly varying lighting conditions. This becomes apparent when you use a digital camera without adjusting for the white color - the results will be ugly.

So basically that's why we have to implement an automatic white balancing, at least until we all have full surround displays and our brains magically adapt by themselves. By the way, playing in fullscreen in the dark room with uncorrected colors slowly makes it adapt too.

**Implementation**

Our implementation tries to mimic what the perception actually does. By definition, a white sheet appears to be white under a wide range of lighting conditions. So we are running a quick computation that uses the existing atmospheric code on GPU, that computes what light reflects off a white horizontal surface. The light has two components - sun light that reflects at an angle and its illuminative power diminishes as the sun recedes from zenith, and the second one is the aggregated light from the sky. Once this compound color is known, we could perform the color correction as a post-process, but there's another way - adjusting the color of sun so that the resulting surface color is white. This has an advantage of not affecting the performance at all, since the sun color is already taken into equation.

While this algorithm doesn't mimic the human perception precisely, i.e. the actual process is more complex and depends on other things, it seems to be pretty satisfactory, though I expect further tuning.

Some of the properties: it extends the period of day that seems to have a "normal" lighting, and removes the unnatural greenish tint on the sky:

![]() |

![](../../assets/f93514cdef84b636.jpg)

![](../../assets/f93514cdef84b636.jpg)

During the day it compensates for the brownish light color by making the blue things bluer. Can't say the old colors were entirely bad though.

![]() |

![](../../assets/3278e4b2d8b98968.jpg)

![](../../assets/3278e4b2d8b98968.jpg)

![]() |

![](../../assets/e94ba8cafda32810.jpg)

![](../../assets/e94ba8cafda32810.jpg)

![]() |

## No comments:

Post a Comment