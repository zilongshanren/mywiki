---
title: Even Faster Math Functions
url: https://basesandframes.wordpress.com/2020/04/04/even-faster-math-functions/
author: Robingreen
published: '2020-04-04'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

![fmf_title_page](../../assets/4be8acb16640e0db.png)


GDC 2020 was cancelled, but I was lucky enough to be selected to present as part of the “Math for Game Programmers” summit. Slotted in last thing in the day from 5:30pm to 6:30pm my job was to be interesting (and quite possibly loud) enough to keep people awake.

The goal was to update the GDC 2002 talk on “[Faster Math Functions](https://basesandframes.wordpress.com/2016/05/17/faster-math-functions/)” as the state of the art in numerical computing has moved on since then. The projects attempting to standardize math libraries so that they all produce the same values for the same inputs is gaining pace. Setting the goal of “last bit accurate” makes correctness an attainable goal for all math libraries.

My focus was to draw inspiration from innovation happening in the fixed-point and FPGA worlds and provide some updates. Specifically an update on converting minimax polynomials for use in programs, using [Sollya](http://sollya.gforge.inria.fr/) we can do far better than truncating carefully balanced coefficients to our machine word size, we can optimize the whole solution. Using [FloPoCo](http://flopoco.gforge.inria.fr/) we can generate optimized fixed and floating point math functions in VHDL. We can do more with less storage using bipartite tables. Generating sines and cosines on a grid has been fully described with an [underlying theory for Discrete Digital Oscillators](http://www.claysturner.com/dsp/digital_resonators.pdf). We can even find a use for Taylor series in generating bit-twiddling functions for reciprocal, sqrt and inverse-sqrt.

When the conference was cancelled, the slide set lost the need to be constrained to one hour and expanded somewhat. Enjoy.