---
title: Screenshot Saturday 167
url: https://etodd.io/2014/04/19/screenshot-saturday-167/
published: '2014-04-19'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 167

With the Kickstarter finished, it's back to our regularly scheduled programming!

I am in the middle of a major graphics engine upgrade. This whole time I've been using fake HDR. Basically I divide every color by 2 when storing it in a texture, then multiply it by 2 whenever I read it from the texture. It works but you end up with lower color fidelity.

Now everything is done in full 64-bit floating point textures. Here's an exaggerated before/after shot so you can see the difference. Notice the color banding on the left.


I was also skipping a few major steps of the usual recipe for bloom, namely downsampling and later resampling with a linear filter. The new bloom effect is much prettier. Here it is in action, along with some crazy geometry bugs I encountered while optimizing the vertex buffer code:


Lastly, I'm experimenting with a new effect for the slow-motion predictive block system:


That's it for this week. Thanks for reading!