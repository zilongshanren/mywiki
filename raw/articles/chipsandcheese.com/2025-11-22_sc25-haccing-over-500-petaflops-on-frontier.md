---
title: 'SC25: HACCing over 500 Petaflops on Frontier'
url: https://chipsandcheese.com/p/sc25-haccing-over-500-petaflops-on
author: George Cozma
published: '2025-11-22'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Here at Supercomputing the Gordon Bell Prize is announced every year. The Gordon Bell Prize is awarded every year to recognize outstanding achievement in high-performance computing applications.

This simulation of the observable universe tracked over 4 trillion particles across 15 billion light years of space. The prior state of the art observable universe simulations only went up to about 250 billion particles which is a fifteenth the number of particles of this new simulation.

This HACC simulation shows the universe about 10 billion years after the Big Bang.

But, not only was this the largest universe simulation ever, the ORNL team managed to get over 500 Petaflops on nearly 9,000 nodes of Frontier’s 9,402 nodes. As a reminder, Frontier manages to get approximately 1,353 Petaflops on High Performance Linpack (HPL). This means that for this simulation the ORNL team managed to get about 37% of the Rmax HPL performance out of Frontier which is very impressive for a non-synthetic workload.

It is awesome to see the Department of Energy’s (DOE) supercomputers being used for amazing science like this! With the announcement of the Discovery Supercomputer that is due in 2028/2029, I can’t wait to see the science that comes out of that system when it is turned over to the scientific community!

If you like the content then consider heading over to the Patreon or PayPal if you want to toss a few bucks to Chips and Cheese. Also consider joining the Discord.

Thanks for reporting in this. Upon looking at the poster, when not running on GPUs it appears they use something called recursive coordinate bisection to improve efficiency. This leaves me wondering what kind of performance is possible using RCB on a system like Fugaku which has GPU-like FLOPS on HBM equipped CPUs.

Thanks for reporting in this. Upon looking at the poster, when not running on GPUs it appears they use something called recursive coordinate bisection to improve efficiency. This leaves me wondering what kind of performance is possible using RCB on a system like Fugaku which has GPU-like FLOPS on HBM equipped CPUs.