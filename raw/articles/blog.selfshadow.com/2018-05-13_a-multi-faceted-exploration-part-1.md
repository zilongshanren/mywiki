---
title: A Multi-Faceted Exploration (Part 1)
url: https://blog.selfshadow.com/2018/05/13/multi-faceted-part-1/
author: Stephen Hill
published: '2018-05-13'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/ab0ab40021abaa53.jpg)

## Introduction

As part of the [Physically Based Shading Course](https://blog.selfshadow.com/publications/s2017-shading-course/) at SIGGRAPH last year, Christopher Kulla and Alejandro Conty presented the latest iteration of Sony Pictures Imageworks’ core production shading models. One area of focus for them was to improve the energy conservation of their materials; in particular they wanted to compensate for the inherent lack of multiple scattering in common analytic BSDFs, which can be a major source of energy loss. (More on this later.)

A year prior, [Heitz et al. [2016]](https://eheitzresearch.wordpress.com/240-2/) had addressed this very issue with an accurate model 1 for microfacet multiple scattering. Unfortunately, since it uses a stochastic process, it wasn’t a good fit for Imageworks’ renderer. Instead, Kulla and Conty adapted ideas from earlier work [

[Kelemen and Szirmay-Kalos 2001](http://sirkan.iit.bme.hu/~szirmay/scook_link.htm);

[Jakob et al. 2014](http://rgl.epfl.ch/publications/Jakob2014Comprehensive)] in order to develop practical solutions for conductors and dielectrics.

While the multiple-scattering term that Imageworks uses is energy conserving by design, it doesn’t actually simulate how light scatters between the facets of a given microsurface (in their case modelled by GGX) in the way that the Heitz model does. Still, in spite of this theoretical shortcoming, it is undoubtedly an improvement over doing nothing at all.

I remember being quite excited when I first saw Imageworks’ results, particularly because their approach appeared to be suitable for real-time use. At the same time, I was curious to see exactly how well it compared to the Heitz model as the gold standard. And beyond that, I was eager to explore the general topic of real-time-friendly approximations to microfacet multiple scattering. In the next few posts, I will share my findings, but first let’s start with a quick recap of the problem…

## Scratching the Microsurface

The most popular microfacet-based BSDFs in use today have a common limitation: they only model *single scattering*. This means that any incoming light that doesn’t immediately leave the microsurface through a single reflection or refraction event is ignored by these models. For instance, light that hits one facet and is reflected onto another (and so on) is treated as though it has been completely absorbed.

It’s this restriction on single scattering that made the derivation of compact, analytic models possible in the first place. However, the lack of *multiple* scattering can lead to significant energy loss with rougher surfaces, which makes sense since there’s a higher probability of light bouncing several times within the microsurface before escaping.

To give a concrete example of this problem, let’s start with a very simple material model: a GGX-based conductor with a constant reflectance of 1. Here is a render of a set of spheres made of this material, with roughness 2 varying from 0.125 to 1 (left to right):

![](../../assets/fdb9b7136431e5e4.png)

At a first glance this result might seem reasonable, but the problem of energy loss becomes readily apparent when the same spheres are placed in a uniform lighting environment (a.k.a. a *furnace* test):

![](../../assets/5d65a99aed8a8370.png)

As we can see, though our material is supposed to be completely reflective, more and more energy is lost as roughness increases. In fact, at the very right, close to 60% of the light has vanished due to the absence of microfacet multiple scattering. Up until recently, we had largely been sweeping this problem under the rug, but it’s hard to argue with concrete numbers like that.

A practical consequence of this behaviour is that it makes life harder for artists doing texture painting and look development, and while it might be possible to manually compensate for the darkening effect in simple cases such as above, it soon becomes an impossible task with textured reflectance and roughness.

It’s clear that we are falling a little short on the physically based shading front and the promise of intuitive material parameters. Fortunately, our collective feeling of shame will be momentary, since help is at hand.

[Next](https://blog.selfshadow.com/2018/06/04/multi-faceted-part-2/) we’ll take an initial look at Imageworks’ approach and see how it measures up against the Heitz model.