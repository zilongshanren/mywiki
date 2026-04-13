---
title: 'Spherical Harmonic Lighting: The Gritty Details'
url: https://basesandframes.wordpress.com/2016/05/11/spherical-harmonic-lighting-the-gritty-details/
author: Robingreen
published: '2016-05-11'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

I wrote the paper *Spherical Harmonic Lighting: The Gritty Details* before the more general terminology *Precalculated Radiance Transfer* (PRT) was coined, which explains the slightly strange title. In 2002 I was working for Sony Computer Entertainment America in Foster City, CA in the R&D group under Dominic Mallinson. I received a preprint from Peter-Pike Sloan of his Siggraph paper * Fast, Arbitrary BRDF Shading for Low-Frequency Lighting Using Spherical Harmonics* and made a bet with my manager that I could implement SH Lighting on PS2 before Siggraph came around that year. I started by verifying that we could do SH projection and demonstrate successive approximation by coding it up in Maple:

And once the SH projection code was verified I went into coding up an app to demo it on Win32 and PS2. The math was straightforward enough but getting hold of watertight manifold models proved to be more of a challenge than I imagined. Most of the diagrams in the paper came from the realtime ray tracing engine that [Gabor Nagy](https://www.linkedin.com/in/gabor-nagy-443890) had built for his 3D editor [Equinox 3D](http://www.equinox3d.com/) and the models were provided through endless patience of our in-house technical artist [Care Michaud-Wideman](https://www.linkedin.com/in/caremichaud) who provided an initial model of a Sofa with cushions, as well as later on a Tree (with double-sided leaves) and chop-top convertible Audi models. The torus scene was knocked up in just a few minutes by Gabor in Equinox 3D.

The sofa was the first object successfully lit using SH. You can see artifacts on the first two images where the regular grid in my simple ray tracer had rejected hits outside of the current voxel leading to checkerboard shadows under the sofa and strangeness on vertices close to voxel boundaries. The SH vs. Point Lighting diagram was after fixing this and was used to demonstrate progress and get the go ahead continue to write the GDC presentation.

We booked a proposal for a GDC talk, so we’d need a live demo, a presentation plus a paper to back up the slides. That year I had been invited back to present my *Faster Math Functions* tutorial for a second year, so it was an intense conference run-up. All I remember about the day was that the room at GDC was standing room only. Our time flew by in a blur as we had 60-minutes for 69 slides plus a live demo by Gabor, and at the end of it we received something like 4.8 out of 5 in the feedback reviews. Nothing tops good reviews from the grizzled, war-weary GDC attendees.

I also learned a lesson to never promise future work in a scientific paper as immediately afterwards the CELL project came round and the SCEA R&D group went into silent lockdown for the next three and a half years working on PSGL for the release of PS3. Including the infamous month where SCEA R&D was asked “What if we didn’t have a GPU in the next Playstation and instead gave you *two* CELL chips…”

**Additional:**

Forgot to add the numerous bugs in the paper, especially with the SH rotation equations that were imperfectly transcribed from some terrible photocopies of photocopies of Ivanic’s original paper. The task of discerning between subscripts and

or

and

, plus testing out whether the Ivanic method derived from real values or the Choi method derived from complex was faster fell to

[Don Williamson](https://twitter.com/Donzanoid), graphics lead at Lionhead. His code is still available online:

and contains validated implementations of both methods, Ivanic being the winner. Fast approximate rotations have been proposed, but the ZYZ rotation decomposition [still wins for low orders](http://www.ppsloan.org/publications/StupidSH36.pdf).


The code posted there still has a wrong sign in the routine that calculates V.

When m<0 it is 1-delta in the second term.