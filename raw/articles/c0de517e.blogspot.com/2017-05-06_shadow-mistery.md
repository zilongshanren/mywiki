---
title: Shadow mistery
url: http://c0de517e.blogspot.com/2017/05/shadow-mistery.html
published: '2017-05-06'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This was a bug assigned to one of our engineers. Puzzling. Instead of being really useful, I started to investigate with some offline rendering.

![]() |

Wow! Mental Ray is broken :)

So apparently yes, you can easily create this optical illusion. It's pretty easy to understand why, especially on a constant albedo the texture of the surface comes entirely from shading. If the light moves, so will the highlights traverse the surface, and that creates an illusion similar to a texture shift, of just a few pixels.

The effect is much stronger when the ambient light creates an highlight opposite to the main light, so when the main light is shadowed the ambient highlight dominates and the shift becomes apparent.

On a render where the ambient and highlight are on the same side, the effect is much less pronounced.

The nail on the coffin was though when I managed to reproduce the same effect in real-life, so, it's definitely an optical illusion that can happen, but it's probably made worse by realtime rendering unshadowed ambient/GI on normalmaps and by the fact that shadows abruptly cancel the sun/sky light, instead of gradually blocking only some rays and rolling out the highlight direction in the penumbra region.

## No comments:

Post a Comment