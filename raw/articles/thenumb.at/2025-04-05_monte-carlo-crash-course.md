---
title: Monte Carlo Crash Course
url: https://thenumb.at/Monte-Carlo/
published: '2025-04-05'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Monte Carlo Crash Course

[Continuous Probability](https://thenumb.at/Probability)[Exponentially Better Integration](https://thenumb.at/Monte-Carlo)[Sampling](https://thenumb.at/Sampling)[Case Study: Rendering](https://thenumb.at/Rendering)[Quasi-Monte Carlo](https://thenumb.at/QMC)*Coming Soon…*

# Exponentially Better Integration

By introducing randomness, Monte Carlo methods let us integrate high-dimensional functions *exponentially faster* than traditional algorithms.

[Integration](https://thenumb.at#integration)[Quadrature](https://thenumb.at#quadrature)[The Curse of Dimensionality](https://thenumb.at#the-curse-of-dimensionality)[Monte Carlo Integration](https://thenumb.at#monte-carlo-integration)[Why Monte Carlo?](https://thenumb.at#why-monte-carlo)[Bias and Consistency](https://thenumb.at#bias-and-consistency)[Non-Uniform Sampling](https://thenumb.at#non-uniform-sampling)

## Integration

Many interesting quantities can be computed by evaluating an integral. For example:

- In computer graphics, the
[rendering equation](https://en.wikipedia.org/wiki/Rendering_equation)equates the light leaving a point along a particular direction with an integral over all incoming directions.

- In finance, one form of the
[Black-Scholes model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)computes the value of an option by integrating over potential prices.

In fact, applied mathematics is full of differential equations, many of which have equivalent [integral forms](https://en.wikipedia.org/wiki/Integral_equation).
Hence, similar formulas show up in physics, engineering, and even machine learning.

However, there’s a catch: analytically solving these sorts of integrals is often infeasible.
Instead, we must turn to *numerical integration*—using computers to approximate the true result.

## Quadrature

Let’s start simple: how might we numerically integrate $$\sqrt{x}$$?
One strategy is to partition the domain into intervals of length $$\frac{1}{N}$$, then sum the areas of corresponding rectangles with height $$f$$.[1](https://thenumb.at#fn:1)

By increasing $$N$$, we can compute a close approximation of the exact answer, $$\frac{2}{3}$$.
Given a sufficiently large $$N$$, our approximation’s *error*, or distance from the true value, will be proportional to $$\frac{1}{N}$$.

Therefore, if we want to cut our error in half, we simply need to use twice as many rectangles.

Choosing a more complex discretization of our domain can decrease error without increasing $$N$$.
For example, we could partition the area into [trapezoids](https://en.wikipedia.org/wiki/Trapezoidal_rule), or perhaps [choose rectangle widths](https://en.wikipedia.org/wiki/Multigrid_method) based on how quickly $$f$$ changes.
This broader class of techniques is often referred to as [quadrature](https://en.wikipedia.org/wiki/Numerical_integration).[2](https://thenumb.at#fn:2)

## The Curse of Dimensionality

For functions like $$\sqrt{x}$$—well-behaved and one-dimensional—quadrature can be accurate and efficient. However, we’re interested in integrating much higher-dimensional functions.

Let’s consider using quadrature to compute the volume of the unit cylinder, which is $$\pi$$. The unit cylinder can be described as a function $$f(\omega)$$, where $$f = 1$$ if $$\omega$$ is inside the unit circle and $$f = 0$$ otherwise. We will then integrate $$f$$ over the two-dimensional domain $$\Omega = [-1,1]\times[-1,1]$$.

Similarly to the one-dimensional case, we can break up $$\Omega$$ into squares of side length $$\frac{2}{N}$$ and sum the volumes of corresponding rectangular prisms with height $$f$$. *(Top view:)*

We can compute a fairly accurate answer, 3 as our error still scales with $$\frac{1}{N}$$—but we had to use $$N^2$$ squares!
If $$M$$ is our sample count, or the number of locations at which we evaluated $$f$$, our error only scales with $$\frac{1}{\sqrt{M}}$$.
That means cutting our error in half requires four times as many samples.

If $$f$$ was three-dimensional, we would have to break up the domain into $$N^3$$ cubes, and so on: in $$d$$ dimensions, we need $$N^d$$ samples.
This combinatorial explosion makes (naive) quadrature untenable for integrals like the rendering equation.[4](https://thenumb.at#fn:4)

## Monte Carlo Integration

Computing the volume under $$f$$ is equivalent to finding the average value of $$f$$ on $$\Omega$$, then multiplying by the area of $$\Omega$$.

Above, partitioning $$\Omega$$ into uniform squares led us to average $$f$$ over a deterministic grid of samples.
You might wonder if we can use uniformly *random* samples instead. *(Top view:)*

Clearly, we can: averaging $$f$$ over $$M$$ uniform samples of $$\Omega$$ results in error proportional to $$\frac{1}{\sqrt{M}}$$.

We can model this sampling procedure as a [random variable](https://thenumb.at/Probability#random-variables) $$U$$ that outputs points uniformly distributed in $$\Omega$$. For $$U$$ to be uniform, its [PDF](https://thenumb.at/Probability#probability-mass-vs-probability-density) must be constant. The PDF must also integrate to one over $$\Omega$$, which has area $$4$$.

$$U$$ samples all parts of $$\Omega$$ with equal probability, so the average value of $$f$$ is the [expected value](https://thenumb.at/Probability#expectation) of $$f(U)$$.

That’s why we got an accurate answer: our sample average approximates $$\mathbb{E}[f(U)]$$. We can precisely define this integration strategy using the following formula:

Where $$U_i$$ is a sequence of [independent](https://thenumb.at/Probability#dependence), identically distributed (i.i.d.) copies of $$U$$ and $$|\Omega| = 4$$ is the area of our domain.
$$F_M$$ is known as a uniform Monte Carlo estimator for $$f$$.

## Why Monte Carlo?

First of all, why does our Monte Carlo estimator even work?
Using [linearity of expectation](https://thenumb.at/Probability#linearity), we can show that the expected value of our estimator is equal to the desired integral:

Hence, our estimator will produce the correct result on average.
Additionally, increasing $$M$$ should give us a more accurate result.
For any variable $$X$$ with a finite expected value, the [strong law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers) states:

That is, our estimator indeed [almost surely](https://en.wikipedia.org/wiki/Almost_surely) converges to the correct answer as we increase $$M$$.

### Escaping the Curse

Second, even if Monte Carlo works, why should we use it over quadrature?
To justify the introduction of randomness, we must show that the *expected error* of our estimator decreases at an accelerated rate.

One way of quantifying expected error is to compute the [standard deviation](https://thenumb.at/Probability#variance) of our estimator.
Given that $$U_i$$ are i.i.d. and $$f(U)$$ has finite variance, we can assume variance is [additive](https://thenumb.at/Probability#covariance):[5](https://thenumb.at#fn:5)

The variance of $$F_M$$ is proportional to $$\frac{1}{M}$$, so its standard deviation (and hence error) is proportional to $$\frac{1}{\sqrt{M}}$$.
This relationship matches our empirical result—but we didn’t assume anything about the dimensionality of $$f$$.
Therefore, our error now scales with $$\frac{1}{\sqrt{M}}$$ in *arbitrarily high dimensions*.

For example, if we integrate $$f$$ over a three-dimensional domain…

Our error indeed still scales with $$\frac{1}{\sqrt{M}}$$.

As we increase dimensionality, Monte Carlo integration becomes *exponentially faster* than uniform quadrature!

## Bias and Consistency

The *bias* of an estimator is the difference between its expected value and the desired integral:

We say that $$F$$ is *unbiased* if $$\beta_F = 0$$, i.e. its expected value is exactly the correct answer.
Above, we proved that our uniform Monte Carlo estimator is unbiased.

Given an unbiased $$F$$, we can assume that averaging $$F$$ over many trials converges to the proper result.[6](https://thenumb.at#fn:6)

Biased estimators are, in some sense, incorrect, but it can be worthwhile to trade bias for lower variance. 7
For example, we could consider quadrature (for a fixed $$N$$) to be an estimator with zero variance—it always returns the same result.
Of course, that result is biased: additional trials won’t converge to the correct answer.

Fortunately, quadrature exposes an additional parameter—$$N$$, the resolution—which decreases its bias.
Quadrature is therefore *consistent*: given more computation, though not in the form of additional trials, it still converges to the exact result.

Concretely, we say that $$F$$ is consistent if $$\beta_F$$ goes to zero with increasing computation.

So far, we’ve only encountered a purely random estimator, uniform Monte Carlo, and a purely deterministic estimator, uniform quadrature.
A practical class of algorithms known as *Quasi-Monte Carlo* methods combines both approaches, as we will see in a future chapter.[8](https://thenumb.at#fn:8)

## Non-Uniform Sampling

Above, we defined the uniform Monte Carlo estimator as follows:

Where $$U_i$$ are random variables representing uniform samples of $$\Omega$$. This formula was actually a special case of a more fundamental method. The factor of $$|\Omega|$$ provides a hint—it’s equivalent to dividing by the PDF of $$U$$:

We can generalize this definition to *non-uniform* random variables $$X_i$$.
Intuitively, if $$X$$ over-represents some portion of the domain, $$f_X$$ will be proportionally larger in that region, so the overall effect cancels out.

For example, let’s revisit our two-dimensional cylindrical integral, but take $$X$$ to sample the right half of the domain three times as often. *(Top view:)*

We’ll find that error still scales with $$\frac{1}{\sqrt{M}}$$, yet is overall higher than the uniform case. That’s because using $$X$$ increased the single-sample variance of our estimator, slowing convergence by a constant factor.

Nonetheless, we may check that our estimator is unbiased, regardless of the distribution of $$X$$:

Note that the final step is valid only if $$f_X(x) > 0$$ whenever $$f(x) \neq 0$$. That is, we can’t use $$X$$ to integrate $$f$$ if $$X$$ never actually samples some part of the domain where $$F$$ is non-zero.

In this example, non-uniform sampling increased variance.
That’s because the variance of our estimator depends on how well our sample distribution matches $$f$$.
We will explore techniques for approximating $$f$$, known as *importance sampling*, in a future chapter.

# Footnotes

[Riemann integration](https://en.wikipedia.org/wiki/Riemann_integral)may be defined as the limit of this process for large $$N$$.[↩︎](https://thenumb.at#fnref:1)Monte Carlo integration can also be considered a form of quadrature, but we will treat it as separate.

[↩︎](https://thenumb.at#fnref:2)Fun fact:

[$$\pi = 4$$](https://math.stackexchange.com/questions/12906/the-staircase-paradox-or-why-pi-ne4)[↩︎](https://thenumb.at#fnref:3)It’s not obvious why the rendering equation (as stated in the introduction) is high-dimensional: it’s

*recursive*. Evaluating $$\mathcal{L}_i$$ requires a nested integral over another $$\mathcal{L}_i$$, ad infinitum. We will discuss a non-recursive,[infinite-dimensional](https://thenumb.at/Functions-are-Vectors), formulation in a future chapter.[↩︎](https://thenumb.at#fnref:4)Even if $$f(U)$$ has infinite variance, the strong law of large numbers implies that our estimator will still converge—but potentially asymptotically slower than $$\frac{1}{\sqrt{M}}$$.

[↩︎](https://thenumb.at#fnref:5)In

[statistics](https://stats.stackexchange.com/questions/31036/what-is-the-difference-between-a-consistent-estimator-and-an-unbiased-estimator), bias and consistency are defined a bit differently (and more rigorously): a particular random variable doesn’t have “trials,” and estimators are only parameterized by sample count. Bias is still the difference between the expected value and the estimated quantity, but consistency implies that bias goes to zero with increasing sample count. Hence, it’s possible to have an unbiased yet inconsistent estimator: consider Monte Carlo with a fixed number of samples. We will ignore this case, since any unbiased estimation algorithm can be made consistent by running it multiple times. The more hand-wavey notion of consistency used here is often seen in graphics and simulation.[↩︎](https://thenumb.at#fnref:6)Another example is

[firefly suppression](https://en.wikipedia.org/wiki/Fireflies_(computer_graphics)), which reduces variance at the expense of bias (energy loss).[↩︎](https://thenumb.at#fnref:7)Another example is

[photon mapping](https://en.wikipedia.org/wiki/Photon_mapping), which is actually possible to[unbias](https://cs.dartmouth.edu/~wjarosz/publications/misso22unbiased.html)![↩︎](../../assets/b0e2093c5008201f.img)