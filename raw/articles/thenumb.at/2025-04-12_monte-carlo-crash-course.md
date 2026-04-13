---
title: Monte Carlo Crash Course
url: https://thenumb.at/Sampling/
published: '2025-04-12'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Monte Carlo Crash Course

[Continuous Probability](https://thenumb.at/Probability)[Exponentially Better Integration](https://thenumb.at/Monte-Carlo)[Sampling](https://thenumb.at/Sampling)[Case Study: Rendering](https://thenumb.at/Rendering)[Quasi-Monte Carlo](https://thenumb.at/QMC)*Coming Soon…*

# Sampling

In the previous chapter, we assumed that we can uniformly randomly sample our domain.
However, it’s not obvious how to actually do so—in fact, how can a deterministic computer even generate random numbers?[1](https://thenumb.at#fn:1)

[Pseudo-Random Numbers](https://thenumb.at#pseudo-random-numbers)[Uniform Rejection Sampling](https://thenumb.at#uniform-rejection-sampling)[Non-Uniform Rejection Sampling](https://thenumb.at#non-uniform-rejection-sampling)[Inversion Sampling](https://thenumb.at#inversion-sampling)[Changes of Coordinates](https://thenumb.at#changes-of-coordinates)

## Pseudo-Random Numbers

Fortunately, Monte Carlo methods don’t need truly random numbers.
Instead, we can use a *pseudo-random number generator*, or PRNG.
Given a random initial state (the *seed*), a PRNG produces a deterministic stream of numbers that look uniformly random:[2](https://thenumb.at#fn:2)

By “look uniformly random,” we mean the sequence exhibits certain statistical properties:

- Uniformity: samples are evenly distributed.
- Independence: previous samples cannot be used to predict future samples.
[3](https://thenumb.at#fn:3) - Aperiodicity: the sequence of samples does not repeat.

Deterministic generators cannot fully achieve these properties, but can get pretty close, in a precise sense. 4
Here, we will use the

[PCG](https://www.pcg-random.org/)family of generators, which are performant, small, and statistically robust.

PRNGs give us uniformly random scalars, but we ultimately want to sample complex, high-dimensional domains. Fortunately, we can build up samplers for interesting distributions using a few simple algorithms.

## Uniform Rejection Sampling

*Rejection sampling* transforms a sampler for a simple domain $$D$$ into a sampler for a complex domain $$\Omega$$, where $$\Omega \subseteq D$$.
All we need is a function $$\text{accept}$$ that indicates whether a point $$\mathbf{x} \in D$$ is also contained in $$\Omega$$.

Let’s build a rejection sampler for the two-dimensional unit disk. First, we’ll choose $$D = [-1,1]\times[-1,1]$$, which clearly encloses $$\Omega$$. We may use a PRNG to produce a sequence of uniform samples of $$[-1,1]$$, denoted as $$\xi_i$$. Taking each pair $$D_i = (\xi_{2i},\xi_{2i+1})$$ then provides samples of $$D$$.

Second, we’ll define $$\text{accept}(\mathbf{x})$$—for the unit disk, we may check that $$||\mathbf{x}|| \le 1$$. Now, the rejection sampler:

```
def Ω():
x = D()
if accept(x):
return x
return Ω()
```


In other words, sample $$D$$, and if the result is not in $$\Omega$$, just try again!

Intuitively, rejection sampling filters out samples that aren’t in $$\Omega$$. If we start with uniform samples of $$D$$, we should be left with uniform samples of $$\Omega$$.

To formalize our reasoning, let’s derive our sampler’s PDF, denoted $$f_\text{rej}$$. To produce a sample $$\mathbf{x}$$, we must first sample it from $$f_D$$, then accept it. Therefore $$f_\text{rej}(\mathbf{x})$$ is equivalent to $$f_D(\mathbf{x})$$ condition on $$\mathbf{x}$$ being accepted.

Note $$|D|$$ and $$|\Omega|$$ indicate the volume of the respective domain.
Hence $$f_\text{rej}$$ is indeed uniform on $$\Omega$$.[5](https://thenumb.at#fn:5)

## Non-Uniform Rejection Sampling

Like we saw with [Monte Carlo integration](https://thenumb.at/Monte-Carlo/#non-uniform-sampling), rejection sampling can be straightforwardly extended to work with non-uniform distributions.

Let’s say the PDF of our distribution on $$D$$ is $$f_D(\mathbf{x})$$, and we want to use it to sample from $$\Omega$$ with PDF $$f_\Omega(\mathbf{x})$$.
We already know that $$\Omega \subseteq D$$, but we’ll also need to check a slightly stricter condition—that the ratio between our PDFs has a finite upper bound, denoted $$c$$.[6](https://thenumb.at#fn:6)

Above, we required $$\Omega \subseteq D$$ because it would otherwise be impossible to sample all parts of $$\Omega$$. Here, we need a finite $$c$$ for essentially the same reason—we’re checking that there is no part of $$\Omega$$ that we sample infinitely infrequently.

Once we have $$c$$, we just need to update $$\text{accept}$$. Now, we will accept a sample $$\mathbf{x}$$ with probability $$\frac{f_\Omega(\mathbf{x})}{cf_D(\mathbf{x})}$$, which is always at most $$1$$.

```
def accept(x):
return random(0, 1) < f_Ω(x) / (c * f_D(x))
```


Intuitively, we’re transforming the probability density at $$\mathbf{x}$$ from $$f_D(\mathbf{x})$$ to $$f_\Omega(\mathbf{x})$$ by accepting $$\mathbf{x}$$ with probability proportional to $$\frac{f_\Omega(\mathbf{x})}{f_D(\mathbf{x})}$$. Note that if $$f_D$$ is uniform, we directly accept $$\mathbf{x}$$ with probability proportional to $$f_\Omega(\mathbf{x})$$.

For example, given uniform $$f_D$$ and $$f_\Omega(\mathbf{x}) \propto \frac{1}{1+||\mathbf{x}||^2}$$:

As you’d expect, we see a greater proportion of accepted samples towards the center, where $$f_\Omega(\mathbf{x})$$ is largest.

Finally, let’s check that our sampler’s PDF is actually $$f_\Omega(\mathbf{x})$$. Like above, the PDF is equivalent to $$f_D(\mathbf{x})$$ condition on $$\mathbf{x}$$ being accepted.

In the second step, we obtain the probability of accepting an arbitrary sample by computing the expected probability of accepting $$\mathbf{x}$$ over all $$\mathbf{x} \in D$$. In the fourth, note that we define $$f_\Omega = 0$$ outside of $$\Omega$$.

### Sample Efficiency

Many practical problems can be solved using only rejection sampling and uniform Monte Carlo integration.
Choosing $$D$$ to be a box enclosing $$\Omega$$ works in any number of dimensions—boxes are always easy to sample, as every dimension is independent.[7](https://thenumb.at#fn:7)

However, rejection sampling is only efficient when $$f_\Omega$$ can make use of a significant proportion of the probability density in $$f_D$$. Each sample of $$f_\Omega$$ requires a geometric number of samples of $$f_D$$, distributed according to $$\mathbb{P}\{\text{accept}\}$$:

Since we have $$\frac{1}{c}$$ chance of accepting each sample, we should expect to generate $$c$$ samples of $$f_D$$ for each sample of $$f_\Omega$$. Intuitively, when $$c$$ is large, it means $$f_D$$ rarely samples regions that $$f_\Omega$$ samples frequently.

For example, you may not want to use rejection sampling when $$\Omega$$ doesn’t cover much of $$D$$:

So, we’ll need to devise a more efficient sampling algorithm.

## Inversion Sampling

Inversion sampling is a method for sampling any one-dimensional distribution with an invertible cumulative distribution function ([CDF](https://thenumb.at/Probability/#cumulative-distributions)).
The CDF of a random variable $$X$$, denoted as $$F_X(x)$$, measures the probability that a sample is less than $$x$$.

Intuitively, the CDF maps $$x$$ to the percentage of probability mass lying below $$x$$:

Hence, the *inverse* CDF $$F^{-1}_X(p)$$ maps a percentage of probability mass to the corresponding $$x$$.[8](https://thenumb.at#fn:8)

We may define an inversion sampler $$\text{Inv}$$ by uniformly sampling $$p$$ from $$[0,1]$$ and computing $$F_X^{-1}(p)$$. To characterize our sampler’s behavior, we can find its PDF. The probability that $$\text{Inv} = F_X^{-1}(p)$$ falls within a range of outcomes $$dx$$ is equivalent to the probability that $$p$$ falls within the corresponding range $$dp$$:

We sampled $$p$$ uniformly, so the probability that $$p$$ falls in $$dp$$ is the length of $$dp$$. The average probability density on $$dx$$ is then $$\frac{dp}{dx}$$. In the limit, the length of $$dp$$ is proportional to slope of $$F_X$$—this ratio is its derivative!

Therefore, we have $$f_\text{Inv} = f_X$$. 9
That implies inversion sampling works, but more rigorously, we can check that the CDF of our sampler matches $$F_X$$.

Since their CDFs are equivalent, we indeed have $$\text{Inv} \sim X$$.

### Marginal Inversion Sampling

As stated, inversion sampling only applies to one-dimensional distributions.
Fortunately, we can extend inversion to higher dimensions by iteratively sampling each dimension’s [ marginal distribution](https://thenumb.at/Probability/#joint-distributions).

Let’s derive an inversion sampler for the two-dimensional distribution $$f_{XY}(x,y)$$. First, we’ll define the marginal distribution $$f_X(x)$$, which computes the total probability density at $$x$$ across all choices for $$y$$.

This distribution is one-dimensional, so we can use inversion sampling to choose a sample $$X$$. Second, we’ll compute the marginal distribution $$f_Y(y)$$ condition on $$X$$, which must be proportional to $$f_{XY}(X,y)$$.

Finally, we can apply inversion again to sample $$Y$$. Intuitively, $$f_{Y\ |\ X}$$ selects the correct distribution for $$y$$ given our choice of $$X$$. We will more rigorously explore why inversion sampling works in the next section.

## Changes of Coordinates

While marginal inversion sampling can build up arbitrarily high-dimensional distributions, it’s often not necessary in practice. That’s because inversion sampling is a special case of a more general technique for transforming random variables.

To illustrate, let’s attempt to define a uniform sampler for the unit disk.
Unlike rejection sampling, we first need to choose a *parameterization* of our domain.
A natural choice is polar coordinates, where $$\theta$$ is angle with respect to the the x-axis and $$r$$ is distance from the origin.

The unit disk is hence described by $$\mathcal{S} = \Phi(\mathcal{R})$$, where $$\mathcal{R} = [0,1]\times[0,2\pi]$$. To produce a sampler for $$\mathcal{S}$$, we could try mapping uniform samples of $$\mathcal{R}$$ onto $$\mathcal{S}$$:

But uniform samples of $$\mathcal{R}$$ don’t become uniform samples of $$\mathcal{S}$$. That’s because transforming from polar to rectangular coordinates didn’t preserve area—smaller radii contain less area, yet we weighted all $$r$$ equally.

To determine what went wrong, let’s find the PDF of this sampler.
The key observation is that a sample $$\mathbf{s}$$ falls within a circular patch $$d\mathcal{S}$$ if and only if $$\mathbf{r} = \Phi^{-1}(\mathbf{s})$$ falls within the corresponding rectangle $$d\mathcal{R}$$.[10](https://thenumb.at#fn:10)

Hence, the probabilities of sampling either region must be equivalent.

In the limit, these integrals reduce to the respective PDF times the area of the patch.

Intuitively, the ratio of areas $$\frac{|d\mathcal{R}|}{|d\mathcal{S}|}$$ tells us how much $$d\mathcal{S}$$ is squashed or stretched when mapped onto $$d\mathcal{R}$$. For example, if $$d\mathcal{S}$$ is scaled down by a factor of two, $$d\mathcal{R}$$ must contain twice the probability density.

Finally, since $$\Phi^{-1}$$ maps $$\mathcal{S}$$ to $$\mathcal{R}$$, the area scaling factor is given by its derivative:[11](https://thenumb.at#fn:11)

Where $$|D\Phi^{-1}|$$ denotes the [determinant of the Jacobian](https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant#Jacobian_determinant) of $$\Phi^{-1}$$.[12](https://thenumb.at#fn:12)

### Sampling via Change of Coordinates

Now that we know the relationship between $$f_\mathcal{S}$$ and $$f_\mathcal{R}$$, we can choose a different, non-uniform $$f_\mathcal{R}$$ that will produce a uniform $$f_\mathcal{S}$$. Our new PDF will need to cancel out the factor of $$|D\Phi^{-1}|$$:

Proportionality with $$\frac{1}{r}$$ makes sense—our misbehaving sampler produced too many samples near the origin.
If we instead sample $$\mathcal{R}$$ according to $$f_\mathcal{R}(r,\theta) = \frac{r}{2\pi}$$, we’ll end up with a uniform $$f_\mathcal{S}$$.[13](https://thenumb.at#fn:13)

In the previous section, we applied a change of coordinates in one dimension. That is, by taking $$\Phi = F_X^{-1}$$, we transformed the uniform unit distribution to have our desired PDF.

In practice, many useful distributions can be efficiently sampled via the proper change of coordinates.
However, doing so requires a parameterization of the domain, which is sometimes infeasible to construct.
In such cases, we may turn to methods like *Markov Chain Monte Carlo*, to be discussed in a future chapter.

# Footnotes

Can you, personally,

[generate random numbers](https://calmcode.io/blog/inverse-turing-test)? It can be[hard to tell](https://thenumb.at/random.jpg).[↩︎](https://thenumb.at#fnref:1)But how do we generate a random seed? In practice, programs use an external source of randomness like the current time or transient hardware state. For secure applications, there are devices that provide random bits based on physical sensor noise or even quantum processes.

[↩︎](https://thenumb.at#fnref:2)Although we assumed independent samples in

[chapter two](https://thenumb.at/Monte-Carlo/#escaping-the-curse), this is*not*required for Monte Carlo to work! We will explore uses of correlated random numbers in a future chapter.[↩︎](https://thenumb.at#fnref:3)For example, if the PRNG has a finite number of internal states, the sequence necessarily repeats after they are exhausted. Similarly, the existence of an algorithm to compute the next sample from the current state implies that previous samples provide

*some*information about future samples. A good PRNG ensures that it is computationally difficult to take advantage of that information. Refer to the[PCG paper](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf)for further analysis.[↩︎](https://thenumb.at#fnref:4)Note the non-standard use of Bayes’ rule to compute a probability density conditioned on a discrete event. This step should be read as follows: the density at $$\mathbf{x}$$, condition on $$\mathbf{x}$$ being accepted, is equivalent to the probability of accepting $$\mathbf{x}$$ (i.e. one), times the density at $$\mathbf{x}$$, divided by the probability we accept an arbitrary sample (i.e. the ratio of volumes).

[↩︎](https://thenumb.at#fnref:5)Note $$\frac{\omega(\mathbf{x})}{d(\mathbf{x})}$$ may not have a maximum; we really use the supremum on $$\Omega$$.

[↩︎](https://thenumb.at#fnref:6)That said, in higher dimensions, spheres—and most other domains you’d want to sample—contain exponentially less volume than cubes! The curse of dimensionality returns.

[↩︎](https://thenumb.at#fnref:7)Assuming the CDF is injective. Some distributions (e.g. whenever $$f_X = 0$$ on some interval) do not have injective CDFs, which are not invertible in the usual sense. Fortunately, we can still apply inversion sampling to their generalized inverse, defined as $$F_X^{-1}(p) = \inf_x\{F_X(x) \ge p\}$$. Intuitively, the generalized inverse skips over regions where $$f_X = 0$$.

[↩︎](https://thenumb.at#fnref:8)Assuming the CDF is differentiable. As mentioned in

[chapter 1](https://thenumb.at/Probability/#dirac-delta-distributions), distributions involving Dirac deltas may have discontinuous (and so non-differentiable) CDFs. Fortunately, inversion sampling still works: the generalized inverse is simply constant on the interval corresponding to the discontinuity. Using[non-standard analysis](https://alok.github.io/2024/09/28/discontinuous-derivative/), we could also rigorously define a derivative for the CDF that contains a Dirac delta, matching the PDF.[↩︎](https://thenumb.at#fnref:9)Note that $$\Phi^{-1}$$ is not defined at $$(0,0)$$, so we’re technically working with the unit disk minus the origin.

[↩︎](https://thenumb.at#fnref:10)This proof is quite stylized, but can be expressed more rigorously in the language of

[exterior calculus](https://en.wikipedia.org/wiki/Exterior_derivative).[↩︎](https://thenumb.at#fnref:11)When $$\Phi$$ is

[sufficiently nice](https://en.wikipedia.org/wiki/Diffeomorphism), we also have $$|D\Phi^{-1}| = \frac{1}{|D\Phi|}$$, which may be easier to compute. However, this is not true when $$\Phi$$ is not injective, as seen in[footnote 8](https://thenumb.at#fn:8).[↩︎](https://thenumb.at#fnref:12)Deriving an inversion sampler for $$f_\mathcal{R}(r,\theta) = \frac{r}{2\pi}$$ is left as an exercise to the reader.

[↩︎](https://thenumb.at#fnref:13)