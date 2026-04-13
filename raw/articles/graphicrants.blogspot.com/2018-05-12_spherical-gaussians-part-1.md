---
title: Spherical Gaussians (part 1)
url: http://graphicrants.blogspot.com/2018/05/spherical-gaussians-part-1.html
author: Brian Karis
published: '2018-05-12'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The formula can be read as evaluating a SG in the direction of $\vv$ where the SG has the parameters of $\muv,\lambda, a$. An abbreviated notation $G(\vv)$ can be used instead when the parameters can be assumed. Often the more verbose notation is used to assign values to the parameters.

SGs have a number of nice properties including simple equations for a number of common operations.

### Product of Two SGs

The product of two SG's can be represented exactly as another SG. This product is sometimes referred to as the vector product. This formula was first properly given in [1] (it was shown earlier but in an non-normalized form).Let $\lambda_m = \lambda_1 + \lambda_2$ and let $\muv_m = \frac{\lambda_1\muv_1 + \lambda_2\muv_2}{\lambda_1 + \lambda_2}$, then \begin{equation} \begin{split} G_1(\vv)G_2(\vv) = G\left(\vv; \frac{\muv_m}{\|\muv_m\|}, \lambda_m\|\muv_m\|, a_1 a_2 e^{\lambda_m\left(\|\muv_m\| - 1\right)}\right) \end{split} \label{eq:sg_product} \end{equation}

### Raising to a power

Given that the product of two SGs is another SG it shouldn't be much of a surprise that a SG raised to a power can be expressed exactly as another SG: \begin{equation} \begin{aligned} G(\vv)^n &= G(\vv; \muv,n\lambda, a^n) \end{aligned} \label{eq:sg_power} \end{equation}### Integration Over The Sphere

The integral of a SG over the sphere has a closed form solution.[2] showed that the integral was: \begin{equation} \int_{S^2}G(\vv) d\vv = 2 \pi \frac{a}{\lambda} \left( 1 - e^{-2\lambda} \right) \label{eq:sg_integral} \end{equation}

### Inner product

The inner product is defined as the integral over the sphere of the product of two SGs. We can already find the product of two SGs and integrate over a sphere. Putting those together we have: \begin{equation} \int_{S^2}G_1(\vv) G_2(\vv) d\vv = \frac{4 \pi a_0 a_1}{e^{\lambda_m}} \frac{ \sinh\left(\|\muv_m\| \right) }{ \|\muv_m\| } \label{eq:sg_inner_product_sinh} \end{equation} This equation has numerical precision issues when evaluated with floating point arithmetic. An alternative form which is more stable is the following: \begin{equation} \int_{S^2}G_1(\textbf{v}) G_2(\textbf{v}) d\textbf{v} = 2 \pi a_0 a_1 \frac{ e^{ \|\boldsymbol\mu_m\| - \lambda_m } - e^{ -\|\boldsymbol\mu_m\| - \lambda_m } }{ \|\boldsymbol\mu_m\| } \label{eq:sg_inner_product_exp} \end{equation}### Normalization

Although there are other definitions for normalization I use the term to mean having an integral over the sphere equal to 1. Normalizing a SG is a simple matter of dividing it by its integral over the sphere. \begin{equation} \begin{aligned} \frac{ G(\vv) }{ \int_{S^2}G(\vv) d\vv } = G\left( \vv; \muv, \lambda, \frac{\lambda}{ 2\pi \left( 1 - e^{-2 \lambda} \right) } \right) \end{aligned} \label{eq:sg_normalized} \end{equation} Notice that the original $a$ parameter canceled out. Instead lobe amplitude is derived purely from the lobe sharpness $\lambda$.These are all the common operations that have closed form solutions. So far nothing new here but hopefully it is helpful to have all these equations in a centralized place for reference. I didn't include derivations for any of these formulas. If readers think that would be useful to see maybe those could be added at a later date.

Special thanks to David Neubelt. Although this has been heavily modified from what we previously had I'm sure his touch is still present.

Now on to some less well covered concepts.

[von Mises-Fisher (part 2)](https://graphicrants.blogspot.com/2018/05/von-mises-fisher-part-2.html)

### References

[1][Wang et al. 2007, "All-Frequency Rendering of Dynamic, Spatially-Varying Reflectance"](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/12/sg.pdf)

[2]

[Tsai et al. 2006, "All-Frequency Precomputed Radiance Transfer using Spherical Radial Basis Functions and Clustered Tensor Approximation"](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.102.1493&rep=rep1&type=pdf)

## No comments:

Post a Comment