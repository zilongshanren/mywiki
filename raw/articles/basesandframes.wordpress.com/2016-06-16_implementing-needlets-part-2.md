---
title: Implementing Needlets, Part 2
url: https://basesandframes.wordpress.com/2016/06/16/implementing-needlets-part-2/
author: Robingreen
published: '2016-06-16'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

In [Implementing Needlets](https://basesandframes.wordpress.com/2016/05/22/implementing-needlets/) we got as far as defining the family of Needlet basis functions, showing what they look like and providing some code for evaluating them. The questions remains, how do I use these to represent a signal on the sphere? Reading the GDC presentation you might get that you need to point Needlets in a bunch of directions and product-integrate them against the signal you want to represent, but which directions and how many points before you get a smooth result?

It’s perfectly possible to take any set of equally spaced directions and use these to approximate the sphere. Take for instance the vertices of tetrahedron.

{{0., 0., 1.}, {-0.471405, -0.816497, -0.333333}, {-0.471405, 0.816497, -0.333333}, {0.942809, 0., -0.333333}}

![tetra-points](../../assets/3230a7ab2eba0fac.png)


If we point the Needlet along each of these directions and sum the result we get this:


![tetra-result](../../assets/3673582e86b9f23e.png)


It’s… something, but it doesn’t look like a sphere, not enough points to provide sufficient coverage. If we then take the vertices of an icosahedron normalized onto the unit sphere:

{{0., 0., -1.}, {0., 0., 1.}, {-0.894427, 0., -0.447214}, {0.894427, 0., 0.447214}, {0.723607, -0.525731, -0.447214}, {0.723607, 0.525731, -0.447214}, {-0.723607, -0.525731, 0.447214}, {-0.723607, 0.525731, 0.447214}, {-0.276393, -0.850651, -0.447214}, {-0.276393, 0.850651, -0.447214}, {0.276393, -0.850651, 0.447214}, {0.276393, 0.850651, 0.447214}}

![icosa-points](../../assets/324540b9e0858989.png)


and do the same operation, something strange happens.

![icosa-result001](../../assets/e90b8f72e9ef897e.png)


An empty box? Zooming in we find a tiny residual function no larger than , the result of summing the floating point values of each basis:


![icosa-result002](../../assets/2c2a74fcb79648e1.png)


So given enough density Needlets cancel each other out and sum to zero. What’s going on here?

In general wavelets are designed to represent *zero mean* functions, i.e. functions that are distributed equally on either side of zero – this is one of the issues with using SH to represent lighting signals where the light probe, visibility and BRDF functions are all positive functions yet we’re using a zero mean system to represent them so we have to carefully avoid reconstruction returning values .


We have successfully projected the unit sphere onto a zero-mean basis and it correctly reconstructs to zero. So somewhere between 4 and 20 points there is a set of points that will accurately reconstruct a band-limited version of our spherical signal using this particular Needlet.

### Quadrature and Spherical Designs

*Gauss Quadrature* is the low cost way to calculate the integral of a function with a known polynomial order and like almost every cool trick in mathematics was invented by [Carl Friedrich Gauss](https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss) [1814]. The idea is that to integrate a function over the range , all you need do is sample the polynomial at specific points and make a weighted sum of those samples:


More than this, for any -point Gauss quadrature the samples will correctly integrate any polynomial function

. To integrate across any other range you just scale into the

domain, calculate the integral and scale the result accordingly. Proofs of this are basic to

[most undergrad math courses](http://www2.math.umd.edu/~mariakc/teaching/gaussian.pdf) as it’s one of the fundamental relations between Orthogonal bases and function approximation. Gauss quadratures are generated from the zeros of Legendre polynomials, solutions using zeros from Chebychev polynomials are * Clenshaw-Curtis quadratures* and those using equally-spaced points are

*(which include the Trapezium and Simpson’s Rules).*

[Newton-Cotes quadratures](http://www4.ncsu.edu/~mtchu/Teaching/Lectures/MA427/By_subjects/16_newton_cotes_quadrature.pdf)Spherical quadrature, [sometimes referred to as cubature](http://web.maths.unsw.edu.au/~rsw/Sphere/), has recently gained some interest through it’s use in analyzing directional data and

[faster integration for Global Illumination](http://www.morganclaypool.com/doi/abs/10.2200/S00649ED1V01Y201505CGR019). A weighted quadrature on the

*spherical design*and designs with equal weight on each sample are

*spherical t-designs*. While

[generating and proving new designs can get involved](http://web.maths.unsw.edu.au/~rsw/Sphere/EffSphDes/RSW_Shanghai15.pdf), using a set of these quadrature points is pretty simple. Lists of designs are available online:

- Hardin & Sloane’s page on
[Spherical t-designs](http://neilsloane.com/sphdesigns/index.html). - Rob Womersley’s page on
[Cubature on the sphere](http://web.maths.unsw.edu.au/~rsw/Sphere/).

Downloading the data gets you a list of either pairs of weights and points or, for a t-designs,

points that should be equally weighted

. Each design is notated with the number of points and the

*degree* or *order* of spherical polynomial it will approximate (remembering that a quadrature can accurately integrate degree and below). Plotting the set of t-designs from Hardin & Sloane’s page we get 112 sets of points here sorted by number of points and colored by the polynomial degree of each set:


![t-designs](../../assets/5eedac1a44114c6e.png)


You can see that we have runs of designs with the same degree and we’re looking for the minimum number of points that will “cover” the sphere with our Needlet, so which design works the best? Without giving too much away, we can show that is an order-3 function so let’s project it against each of the order-3 designs. Notice how not every set is symmetrical so it’s not just bases opposite each other cancelling out – this cancellation is happening in polynomial frequency space.


![order-3](../../assets/ab104cd6e1d6b478.png)


The result is that each design can resolve the sphere to within :


![order-3-result](../../assets/3b99d0bc436ba290.png)


So for our purposes we only need to consider the designs with the smallest number of points for each order, lets call it the set of *minimum t-designs (*shown here for the first 22 orders). There are a few non-intuitive moments in there where order-6 uses less samples than order-5, same with order-8 vs. order-7, so we can pare down the list even further at the low end.

![minimum-t-designs2](../../assets/28970da57e4e3707.png)


Note that this is a quick result using only the set of t-designs, the designs with uniformly weighted samples. I don’t have any results yet for weighted designs so there could well be point sets out that do the same job for less samples (if you find any tell me and I’ll keep a list updated).

### Fractional Needlets

So now we have a way to uncover how many samples each Needlet requires. By matching the Needlet against the list of minimum t-designs we can find the threshold. For the family we find the thresholds are


For fine control Needlets can also be generated with fractional powers, and the function that maps the related bandwidth to polynomial order still needs further investigation (my bet is that it’s related to the highest SH function in the non-zero weights). Here’s an animation from

to

in steps of +0.05.


### Needlets as Frames

So we have Needlet families, we know the sample counts needed to correctly reconstruct a spherical signal, how do we project a spherical function onto Needlets? It works much the same way as SH projection but without the benefits of *successive approximation*. The level index in each Needlet family

specifies the frequency range that each Needlet is covering and they do so orthogonally like any other wavelet family.


![discrete-levels](../../assets/c15cc4677ba5d39c.png)


The only difference is that each level requires a different number of points to reliably project the signal. [Math libraries that provide Needlet projections](https://astro-informatics.github.io/s2let/) are mostly designed to support high-frequency signals and just pick the highest spherical design and project all levels of the Needlet family against that, but for real-time applications we’re looking for the minimal design for each level. Summing the reconstructed signal against successive indices that were projected using different designs for each level, we can add detail to the approximation in the correct wavelet-like behavior.



I hope you will entertain a newb question.

N(1,2) is order 3 and can cover the sphere with 6 points, and N(0,2) is constant and covers the sphere with 1 point.

If I understand this all correctly, and I probably don’t, that means these 7 basis functions can be used to encode arbitrary spherical functions (appropriately band-limited).

So that’s 7 coefficients for an order-3 scheme, whereas SH requires 16 coefficients for same…

What I want to know is, would a light probe expressed in this basis with just 7 coefficients be as faithful as the 16-coefficient SH representation, or necessarily blurrier?

Quick answer: Blurrier, but not in the way you might think.

Needlets, and Wavelets in general, are ways of representing signals that bias the information content in different ways than the SH method. Classical SH is the smoothest possible solution to representing signals on the sphere and are generated to represent low frequency data first and subsequently higher and higher frequencies afterwards. Wavelets can be generated to represent low-and-mid signals first and clean up the rest of the information content later, partially sharing frequency ranges across bands. It’s a different way of representing signals that allows you to concentrate on squeezing out the information you are interested in the first few coefficients and move the non-interesting data into later coefficients. Wavelets have other rules (self similar scaling and translation) that make them easier to generate, but these rules are arbitrary “rules of the game” that are not fundamental to the problem of signal representation.

We will never be using all the coefficients of a signal (and SH requires many, many levels to converge, ringing all the way down) so front-loading the information into the first few coefficients will give us fast convergence. Fast convergence is something SH does not have and would be useful, but none of the signal processing literature talks about speed of convergence. They do however talk about sparsity of a representation which is approximately the same thing. So that’s the route I have been looking in. The goal is to make a system for spherical signal representation that can be computed fast (polynomial or table based), converges fast (for the kinds of information I am interested in) and is efficiently directable (this requires rotational symmetry).

So to directly answer your question, by ignoring some of the symmetry in the spherical signal we get a low frequency signal using less coefficients with less ringing that’s not as smooth as SH but converges faster when you add higher frequency bands. Some win, some loss, net advantage.

Very good. Thank you!

Thanks for this, this is a fantastic write up. I’ve gone through both of these articles and the PDF and I think I’ve understood most of it, but I’m struggling to understand the process of projecting a function into the needlet basis. I’d really appreciate if you’re willing to expand a little.

As I understand things currently, we choose a particular value for j and B, find the appropriate spherical T-design, point needlets along each of those T-design directions, and product integrate the function against them to get the coefficients.

I’m having a little trouble understanding how that product integration step works. It seems that just directly monte carlo sampling uniformly on the surface of the sphere doesn’t work. Perhaps I’m being a dummy, but I think that conclusion is backed up by both reasoning and my practical experiments. Your GDC presentation says “Sampling Needlets correctly requires non-uniform sampling” which is presumably referring to this, but I don’t think it elaborates. I’m working my way through a number of papers that seem to touch on this topic, but my formal maths education isn’t quite up to this level and it’s slow going.

I’d really appreciate it if you could point me in the right direction to get the projection step working.

Thanks again for putting these articles together, they’re by far the most approachable needlet resource I’ve been able to find.