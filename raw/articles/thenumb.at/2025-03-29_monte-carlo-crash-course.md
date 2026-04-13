---
title: Monte Carlo Crash Course
url: https://thenumb.at/Probability/
published: '2025-03-29'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Monte Carlo Crash Course

[Continuous Probability](https://thenumb.at/Probability)[Exponentially Better Integration](https://thenumb.at/Monte-Carlo)[Sampling](https://thenumb.at/Sampling)[Case Study: Rendering](https://thenumb.at/Rendering)[Quasi-Monte Carlo](https://thenumb.at/QMC)*Coming Soon…*

# Continuous Probability

*Prerequisites: Discrete Probability, Multivariable Calculus*

This chapter is a condensed review of continuous probability. If you’re comfortable working with continuous random variables, you may want to skip it.

[Random Variables](https://thenumb.at#random-variables)[Probability Mass vs. Probability Density](https://thenumb.at#probability-mass-vs-probability-density)[Cumulative Distributions](https://thenumb.at#cumulative-distributions)[Joint Distributions](https://thenumb.at#joint-distributions)[Dependence](https://thenumb.at#dependence)[Expectation](https://thenumb.at#expectation)[Probability Bounds](https://thenumb.at#probability-bounds)[Variance](https://thenumb.at#variance)[Covariance](https://thenumb.at#covariance)[Dirac Delta Distributions](https://thenumb.at#dirac-delta-distributions)

## Random Variables

In the discrete world, a *random variable* represents a random process with [countably many](https://en.wikipedia.org/wiki/Countable_set) outcomes.
The classic example is flipping a fair coin: let’s say $$X$$ evaluates to $$1$$ if our coin comes up heads, otherwise $$0$$.
Because there are only two possibilities, $$X$$ is a *discrete* random variable.

Discrete does not necessarily imply finite—there may be infinite possible outcomes. For example, if $$Y$$ encodes the number of coins we flip before seeing heads, then $$Y$$ is discrete, yet may be arbitrarily large.

On the other hand, a continuous random variable represents a process with [uncountably many](https://en.wikipedia.org/wiki/Uncountable_set) outcomes.
This is the case whenever we measure a continuous quantity.
For example, if $$Z$$ returns the position of a particle in a box, then $$Z$$ is continuous.

This distinction might seem subtle, but it fundamentally changes how we reason about probability.

## Probability Mass vs. Probability Density

Discrete random variables are described by *probability mass functions* (PMFs), which record the chance of seeing each outcome.
For example, the PMFs of $$X$$ and $$Y$$:

| \[ x \sim X \] | \[ f_X(x) \] |
|---|---|
| \[ 0 \] | \[ 0.5 \] |
| \[ 1 \] | \[ 0.5 \] |

| \[ y \sim Y \] | \[ f_Y(y) \] |
|---|---|
| \[ 1 \] | \[ 0.5 \] |
| \[ 2 \] | \[ 0.25 \] |
| \[ 3 \] | \[ 0.125 \] |
| \[ \vdots \] | \[ \vdots \] |

The notation $$x \sim X$$ indicates that the specific outcome $$x$$ was sampled from the random variable $$X$$.

Intuitively, summing the PMF over all possible outcomes must result in a probability of $$1$$.
That’s why we call it a *mass* function: it measures how we’ve partitioned the total mass across the possible outcomes.

However, this intuition doesn’t apply to the continuous world, where we can’t sum over uncountably many possibilities.
Naively, if we assigned any non-zero probability to each outcome, the total mass would be infinite!
Therefore, the probability of drawing any particular outcome must be *zero*.[1](https://thenumb.at#fn:1)

Consider a continuous random variable $$Z$$ that produces a random point in the interval $$[0,1]$$. For any particular outcome $$z$$:

Yet sampling $$Z$$ still produces *some* result.
To make sense of this conflict, we must shift our perspective from *mass* to *density*.
In physics, density is mass per unit volume—here, density is probability per “unit outcome.”
Just like you wouldn’t expect a single point to contain mass, a single outcome does not contain probability.

Instead, we can consider the probability of $$Z$$ falling within a small interval $$[z, z + h)$$. Let’s say $$Z$$ is uniformly distributed, so the answer is simply the length of the interval:

Dividing the probability by $$h$$ gives us the average probability density over the interval.
Taking the limit as $$h$$ goes to zero produces the *probability density function* (PDF) of $$Z$$ at $$z$$.

In physics, mass may be computed by integrating density over volume. The same applies here: to recover the probability of $$Z$$ falling within an interval $$[a, b)$$, we integrate the PDF over that interval.

Just like the discrete case, integrating a PDF over its domain must yield a probability of $$1$$.

## Cumulative Distributions

The above limit looks suspiciously like a derivative—but what are we differentiating?

Another way to express the probability that $$Z$$ falls within $$[z,z+h)$$ is by taking the probability that $$Z$$ is less than $$z+h$$ and subtracting out the probability that $$Z$$ is less than $$z$$.

We call the function $$F_Z(z) = \mathbb{P}\{Z < z\}$$ the *cumulative distribution function* (CDF) of $$Z$$.
We can see that the PDF is the derivative of the CDF:[2](https://thenumb.at#fn:2)

Therefore, we can compute the CDF by integrating the PDF:

This result again echoes the [discrete case](https://www.youtube.com/watch?v=D0EUFP7-P1M), where the CDF is the sum of the PMF up to a given point.

## Joint Distributions

So far, all of our PDFs have been one-dimensional, using a single input to describe the outcome of a single random process. How can extend this perspective to more complex outcomes?

Let’s consider jointly sampling $$x \sim X$$ and $$y \sim Y$$. Flip one coin to get $$x$$, then flip additional coins to get $$y$$.

The outcome is described by two variables, so the resulting *joint PMF* must be two-dimensional.
We can write down a table of probabilities for $$f_{X,Y}(x,y)$$:

| \[ x \sim X \] | \[ y \sim Y \] | \[ f_{X,Y}(x,y) \] |
|---|---|---|
| \[ 0 \] | \[ 1 \] | \[ 0.25 \] |
| \[ 1 \] | \[ 1 \] | \[ 0.25 \] |
| \[ 0 \] | \[ 2 \] | \[ 0.125 \] |
| \[ 1 \] | \[ 2 \] | \[ 0.125 \] |
| \[ \vdots \] | \[ \vdots \] | \[ \vdots \] |

Just like a one-dimensional PMF, summing $$f_{X,Y}$$ over all outcomes must result in a probability of one.

We can recover the PMF of $$X$$ by summing over all possible outcomes for $$Y$$.
The result is known as the *marginal PMF* of $$X$$, and the same applies to $$Y$$.

In the continuous world, a *joint PDF* is defined similarly, except that summation is replaced by integration.

The *marginal PDF* as well:

## Dependence

In the above example, we found that $$f_{X,Y}(x,y) = f_X(x)f_Y(y)$$.
This relationship holds if and only if we sampled $$X$$ and $$Y$$ *independently*, denoted as $$X \perp Y$$.

Intuitively, $$X$$ and $$Y$$ are independent if our choice of $$y$$ was not influenced by $$x$$, and vice versa.

However, random variables are not, in general, independent. For example, let’s instead sample a sequence of flips to determine $$y$$, then take the first coin flip to be $$x$$.

Given this sampling procedure, we’ll still find that $$x \sim X$$ and $$y \sim Y$$. However, knowing $$x$$ tells us something about $$y$$: if $$x = 1$$, clearly $$y = 1$$ as well. Therefore, these $$X$$ and $$Y$$ are not independent.

| \[ x \sim X \] | \[ y \sim Y \] | \[ f_{X,Y}(x,y) \] |
|---|---|---|
| \[ 1 \] | \[ 1 \] | \[ 0.5 \] |
| \[ 0 \] | \[ 2 \] | \[ 0.25 \] |
| \[ 0 \] | \[ 3 \] | \[ 0.125 \] |
| \[ \vdots \] | \[ \vdots \] | \[ \vdots \] |

Hence, we cannot assume that the joint PMF is the product of the marginal PMFs. Fortunately, we can still recover $$f_X$$ and $$f_Y$$ by marginalizing $$f_{X,Y}$$.

When dealing with dependent variables, it’s often useful to consider the *conditional distribution* of each variable.
For example, the distribution of $$Y$$ given a particular $$x$$ is denoted as $$f_{Y\vert X=x}(y)$$, and vice versa.

| \[ y \sim Y \] | \[ f_{Y\vert X=0}(y) \] | \[ f_{Y\vert X=1}(y) \] |
|---|---|---|
| \[ 1 \] | \[ 0 \] | \[ 1 \] |
| \[ 2 \] | \[ 0.5 \] | \[ 0 \] |
| \[ 3 \] | \[ 0.25 \] | \[ 0 \] |
| \[ \vdots \] | \[ \vdots \] | \[ \vdots \] |

When $$X$$ and $$Y$$ are independent, their conditional distributions are always equal to their respective PMFs. The same logic applies to the continuous case.

## Expectation

The “typical” result of sampling $$X$$ is known as the *expected value* or *mean* of $$X$$, denoted as $$\mathbb{E}[X]$$.[3](https://thenumb.at#fn:3)

In the discrete world, $$\mathbb{E}[X]$$ is computed by summing the outcomes of $$X$$ weighted by their probability.
For example, let’s compute $$\mathbb{E}[Y]$$ analytically, then check our result by averaging many samples:[4](https://thenumb.at#fn:4)

When sampling $$Y$$, we have a 50% chance to only need one coin flip, 25% to need two, and so on. Hence, we should expect to flip the coin twice before coming up with heads.

In the continuous world, we’ll replace the sum with an integral. Given $$Z$$ from above:

Unsurprisingly, the expected outcome of uniformly sampling $$[0,1]$$ is $$0.5$$.

More generally, we can define a notion of expected value for *functions* of random variables, such as $$g(X)$$:

Intuitively, this integral sums $$g(x)$$ for every $$x$$, weighted by the probability (density) of drawing that $$x$$. The plain expected value $$\mathbb{E}[X]$$ may be considered a special case, i.e. when $$g(x) = x$$.

### Linearity

Expectation is linear, even for dependent random variables. That is, the expected value of $$X + Y$$ is the sum of the expected values of $$X$$ and $$Y$$, and the expected value of $$\alpha X$$ is $$\alpha$$ times the expected value of $$X$$.

We can prove this fact by marginalizing the joint PDF:[5](https://thenumb.at#fn:5)

## Probability Bounds

Expected value tells us the mean of a random variable, but it does not indicate the average distance a sample will fall from that mean.
This property is known as *dispersion*.
The following distributions have the same expected value, but different dispersions.

Given high dispersion, we should expect to find more samples far away from the expected value. However, there’s a limit: we can bound the probability that any one sample is particularly distant from the mean.

One way to do so is using *Markov’s inequality*, which states that for any non-negative $$X$$, the probability of drawing $$X \ge a$$ is at most $$\frac{\mathbb{E}[X]}{a}$$.

This inequality follows directly from the definition of expected value. If we could sample $$a$$ with probability greater than $$\frac{\mathbb{E}[X]}{a}$$, the expected value itself must be greater than $$a\frac{\mathbb{E}[X]}{a} = \mathbb{E}[X]$$—a contradiction.

Above, we computed $$\mathbb{E}[Y] = 2$$. Therefore, the probability of drawing $$Y \ge 4$$ must be at most $$0.5$$:

Markov’s inequality is often loose: for random variables like $$Y$$, the true probability is far lower than $$\frac{\mathbb{E}[X]}{a}$$.
As we will see in the following section, it’s possible to enforce stricter bounds by comparing functions of the random variable.[6](https://thenumb.at#fn:6)

## Variance

The *variance* of a random variable is a quantitative measure of its dispersion.
Denoted as $$\mathrm{Var}[X]$$, the variance of $$X$$ is defined as the expected squared distance between $$X$$ and $$\mathbb{E}[X]$$.[7](https://thenumb.at#fn:7)

Conveniently, $$\mathrm{Var}[X]$$ is equivalent to expected value of $$X^2$$ minus the expected value of $$X$$, squared.

Let’s compute $$\mathrm{Var}[Y]$$ analytically and check our answer. Unlike our estimates of expectation, the empirical result may differ substantially from the true value. This is because the random variable $$Y^2-4$$ has higher variance than $$Y$$ itself.

The same procedure may be applied to continuous random variables:

The square root of variance, known as the *standard deviation* or $$\sigma$$, is often reported as a more intuitive measure of dispersion.
The standard deviation is particularly relevant to the [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution)—but it also lets us bound any random variable via *Chebyshev’s inequality:*

That is, the probability $$X$$ falls at least $$k$$ standard distributions away from the mean is at most $$\frac{1}{k^2}$$. To prove Chebyshev’s inequality, we may apply Markov’s inequality to the random variable $$(X - \mathbb{E}[X])^2$$.

## Covariance

Unlike expectation, variance is only additive for independent random variables.

Here, $$\mathrm{Cov}[X,Y] = \mathbb{E}[XY] - \mathbb{E}[X]\mathbb{E}[Y]$$ denotes the *covariance* of $$X$$ and $$Y$$.
Intuitively, covariance measures how strongly two variables are correlated.

Let’s compute covariance for the *dependent* $$X$$ and $$Y$$ we defined above:

| \[ x \sim X \] | \[ y \sim Y \] | \[ f_{X,Y}(x,y) \] |
|---|---|---|
| \[ 1 \] | \[ 1 \] | \[ 0.5 \] |
| \[ 0 \] | \[ 2 \] | \[ 0.25 \] |
| \[ 0 \] | \[ 3 \] | \[ 0.125 \] |
| \[ \vdots \] | \[ \vdots \] | \[ \vdots \] |

The negative covariance makes sense: when $$X$$ is large ($$1$$), $$Y$$ must be small (also $$1$$), and vice versa.

When $$X$$ and $$Y$$ are independent, their covariance is zero, and therefore their variance is additive.

While independent random variables have zero covariance, zero covariance does **not** imply independence.

## Dirac Delta Distributions

The Dirac delta distribution (often seen in signal processing and computer graphics) gives us a way to define PDFs for discrete random variables. Denoted as $$\delta(x)$$, the Dirac delta is defined to be zero whenever $$x \neq 0$$, and to satisfy the following property:

The Dirac delta is not a function in the usual sense.
If you had to give it a piecewise definition, you might say $$\delta(0) = \infty$$, but this description would violate other assumptions.[8](https://thenumb.at#fn:8)

Fortunately, integrating to one is exactly what we need to describe a “discrete” PDF.
The plain Dirac delta describes a continuous random variable that always returns zero.[9](https://thenumb.at#fn:9)

We can then define PDFs for discrete variables like $$X$$ using linear combinations of deltas:

This PDF concentrates half of its mass at $$x = 0$$ and half at $$x = 1$$. We can check that it still integrates to one:

So, to sample from $$f_X$$, you would return either 0 or 1 with equal probability.

Additionally, we can use deltas to mix discrete and continuous distributions. For example, consider a random variable $$W$$ that returns 0 with 50% probability, otherwise a uniform sample of $$[0,1]$$.

Technically, we should state $$f_W(w) = 0$$ for any $$w \notin [0,1]$$, but a PDF’s [support](https://en.wikipedia.org/wiki/Support_(mathematics)) is often left implicit in practice.
When integrating, we’ll remember to restrict the constant portion to the unit interval.

# Footnotes

More precisely, the set of outcomes with non-zero probabilities must have

[measure zero](https://en.wikipedia.org/wiki/Null_set).[↩︎](https://thenumb.at#fnref:1)Assuming the CDF is differentiable. Note that the CDF is always the (

[Lebesgue–Stieltjes](https://en.wikipedia.org/wiki/Lebesgue%E2%80%93Stieltjes_integration)) integral of the PDF, which must have[bounded variation](https://en.wikipedia.org/wiki/Bounded_variation).[↩︎](https://thenumb.at#fnref:2)Assuming the expected value is finite.

[↩︎](https://thenumb.at#fnref:3)On its own, the definition of expected value does not imply that averaging samples of $$X$$ will approximate $$\mathbb{E}[X]$$. This property relies on the

[law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers).[↩︎](https://thenumb.at#fnref:4)Assuming it is valid to swap the integration order of $$f_{X,Y}$$.

[↩︎](https://thenumb.at#fnref:5)In randomized algorithms,

[Chernoff bounds](https://en.wikipedia.org/wiki/Chernoff_bound), which bound $$e^X$$, are often used to prove results with high probability.[↩︎](https://thenumb.at#fnref:6)Assuming the expected

*squared*value is finite.[Heavy-tailed distributions](https://en.wikipedia.org/wiki/Heavy-tailed_distribution)can have finite expected value, yet infinite variance![↩︎](../../assets/1d06d8407d8bfcad.img)For example, it would not be a real-valued function, and it clearly wouldn’t have

[bounded variation](https://en.wikipedia.org/wiki/Bounded_variation).[↩︎](https://thenumb.at#fnref:8)Earlier, we said $$\mathbb{P}\{X = x\} = 0$$ for all continuous random variables, but that’s no longer the case.

[↩︎](https://thenumb.at#fnref:9)