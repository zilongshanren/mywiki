---
title: Which algorithm is the best choice for real-time path tracing?
url: http://raytracey.blogspot.com/2011/01/which-algorithm-is-best-choice-for-real.html
author: Sam Lapere
published: '2011-01-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

instant radiosity

- fast

- only useful for diffuse and semi-glossy scenes

- performance deteriorates quickly in glossy scenes

- many artefacts due to light bleeding through, singularity effects, clamping, ...

unidirectional path tracing (PT)

- best for exteriors (mostly direct lighting)

- not so good for interiors with much indirect lighting and small light sources

- very slow for caustics

bidirectional path tracing (BDPT)

- best for interiors (indirect lighting, small light sources)

- fast caustics

- very slow for reflected caustics

Metropolis light transport (MLT) + BDPT

- best for interiors (indirect lighting, small light sources)

- especially useful for scenes with very difficult lighting (e.g. through a keyhole, light splitting through prism)

- faster for reflected caustics

energy redistribution path tracing

- mix of Monte Carlo PT and MLT

- best for interiors (indirect lighting, small light sources)

- much faster than PT for scenes with very difficult lighting (e.g. light coming through a small opening, lighting the scene indirectly)

- fast caustics

- not so fast for glossy materials

- problems with detailed geometry

photon mapping

- best for indoor scenes

- biased, artefacts, splotchy, low frequency noise

- fast, but not progressive

- large memory footprint

- very useful for caustics + reflected caustics

stochastic progressive photon mapping

- best for indoor

- fast and progressive

- very small memory footprint

- handles all kinds of caustics robustly

I also found this comment from vlado (V-Ray developer) on the V-Ray forums regarding Metropolis light transport:

BDPT with quasi Monte Carlo (QMC) for indoor and PT with QMC for outdoor scenes seem to be the best candidates for real-time pathtraced games."I came to the conclusion that MLT is way overrated. It can be very useful in some special situations, but for most everyday scenarios, it performs (much) worse than a well-implemented path tracer. This is because MLT cannot take advantage of any sort of sample ordering (e.g. quasi-Monte Carlo sampling, or the Schlick sequence that we use, or N-rooks sampling etc). A MLT renderer must fall back to pure random numbers which greatly increases the noise for many simple scenes (like an open skylight scene)."

[Two-way path tracing](http://www.sjbrown.co.uk/2011/01/03/two-way-path-tracing/)could be a very interesting alternative as well. Caustics are a nice effect for perfectly physically correct rendering, but are really not that important in most scenes and can generally be ignored for real-time purposes, where convergence speed is of uttermost importance.

## 4 comments:

Google "Noise Aware MLT"

It could help on those dark regions that are under sampled. The algorithm seems simple.

Very useful post, bookmarked!

I really liked this as a read and discussion with friends. Bring more of this pls!

Post a Comment