---
title: von Mises-Fisher (part 2)
url: http://graphicrants.blogspot.com/2018/05/von-mises-fisher-part-2.html
author: Brian Karis
published: '2018-05-12'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Compare the equation for a vMF to the equation for a SG and it is easy to see that: \begin{equation} \begin{aligned} V(\vv;\muv,\lambda) = G\left( \vv; \muv, \lambda, \frac{\lambda}{ 2\pi \left( 1 - e^{-2 \lambda} \right) } \right) \end{aligned} \label{eq:vmf_to_sg} \end{equation} That means a vMF is equivalent to a normalized SG and by moving terms from one side to the other we can show that a SG is equivalent to a scaled vMF. \begin{equation} \begin{aligned} G\left( \vv; \muv, \lambda, a \right) = \frac{2\pi a}{\lambda} \left( 1 - e^{-2 \lambda} \right) V(\vv;\muv,\lambda) \end{aligned} \label{eq:sg_to_vmf} \end{equation}

### Fitting a vMF distribution to data

Fitting a vMF distribution to directions or points on a sphere is a very similar process as fitting a normal distribution to points on a line. In the case of a normal distribution, one calculates the mean and variance of the data set and then chooses a normal distribution with the same mean and variance as the best fit to the data.For the vMF distribution the mean direction and spherical variance are used. Calculating these properties for a set of directions is simple. \begin{equation} \begin{aligned} \rv = \frac{1}{n}\sum_{i=1}^{n} \textbf{x}_i \end{aligned} \label{eq:r_average} \end{equation} where $\textbf{x}_1, \textbf{x}_2, ..., \textbf{x}_n$ are a set of unit vectors.

Often values are associated with these directions. So instead taking a simple average we can take a weighted average. \begin{equation} \begin{aligned} \rv = \frac{\sum_{i=1}^{n} \textbf{x}_i w_i}{\sum_{i=1}^{n} w_i} \end{aligned} \label{eq:r_weighted_average} \end{equation} We have the two properties, the mean direction $\muv = \frac{\rv}{\|\rv\|}$ and the spherical variance $\sigma^2 = 1 - \|\rv\|$. To fit a vMF distribution to the data we need to know what these properties are for the vMF distribution. Since the vMF distribution is convex, circularly symmetric about its axis, and is max in the direction of $\muv$, it is fairly obvious that the mean direction will be $\muv$ so I won't derive that here.

The spherical variance $\sigma^2$ on the other hand is a bit more involved. Because we already know the direction of $\rv$ is $\muv$ we can simplify this calculation to the integral of the projection of the function onto $\muv$. \begin{equation} \begin{split} \|\rv\| &= \int_{S^2} V(\vv;\muv,\lambda) (\mudotv) d\vv \\ &= \frac{\lambda}{ 4\pi \sinh(\lambda) } \int_{S^2} e^{\lambda(\mudotv)} (\mudotv) d\vv \\ \end{split} \end{equation} Because the integral over the sphere is rotation-invariant we will replace $\muv$ with the x-axis. \begin{equation} \begin{split} &= \frac{\lambda}{ 4\pi \sinh(\lambda) } \int_{0}^{2 \pi} \int_{0}^{\pi} e^{\lambda\cos\theta} \cos\theta\sin\theta d\theta d\phi \\ &= \frac{\lambda}{ 4\pi \sinh(\lambda) } 2 \pi \int_{0}^{\pi} e^{\lambda\cos\theta} \cos\theta\sin\theta d\theta \\ \end{split} \end{equation} Substituting $t=-\cos\theta$ and $dt=\sin\theta d\theta$ \begin{equation} \begin{split} &= \frac{\lambda}{ 2 \sinh(\lambda) } \int_{-1}^{1} -t e^{-\lambda t} dt \\ &= \frac{\lambda}{ 2 \sinh(\lambda) } \left( \frac{ 2 \lambda \cosh(\lambda) - 2 \sinh(\lambda) }{ \lambda^2 } \right) \\ &= \frac{\cosh(\lambda)}{ \sinh(\lambda) } - \frac{\sinh(\lambda)}{ \lambda \sinh(\lambda) } \\ \end{split} \end{equation} Arriving in its final form \begin{equation} \|\rv\| = \coth(\lambda)-\frac{1}{\lambda} \label{eq:r_length} \end{equation} Although simple in form, this function unfortunately isn't invertible. [1] provides an approximation which is close enough for our purposes. \begin{equation} \begin{aligned} \lambda &= \|\rv\| \frac{ 3 - \|\rv\|^2}{1 - \|\rv\|^2} \end{aligned} \end{equation} Now that we have a way to calculate the mean and spherical variance for a data set and we know the corresponding vMF mean and spherical variance, we can fit a vMF to the data set.

Using eq \eqref{eq:r_weighted_average} to calculate $\rv$, the vMF fit to that data is \begin{equation} V\left( \vv; \frac{\rv}{\|\rv\|},\|\rv\| \frac{ 3 - \|\rv\|^2}{1 - \|\rv\|^2} \right) \label{eq:r_to_vmf} \end{equation}

Going the other direction from $V(\vv;\muv,\lambda)$ form to $\rv$ form using eq \eqref{eq:r_length} is this: \begin{equation} \rv = \left( \coth(\lambda)-\frac{1}{\lambda} \right) \muv \label{eq:vmf_to_r} \end{equation}

### Addition of SGs

We now have a way to convert to and from $\rv$ form. $\rv$ is linearly filterable as shown in how it was originally defined in eq \eqref{eq:r_weighted_average}. This means if our vMF functions are representing a spherical distribution of something then a weighted sum of those distributions can be approximately fit by another vMF. In other words we can approximate the resulting distribution by converting to $\rv$ form, filtering, and then converting back to traditional $V(\vv;\muv,\lambda)$ form.By using the weighted average eq \eqref{eq:r_weighted_average} we can apply this concept to non normalized SGs too. This allows us to not just filter (ie sum with a total weight of 1) but add as well. A non-normalized SG as shown in eq \eqref{eq:sg_to_vmf} is a scaled vMF. We can use this scale as the weight when summing and use the total weight as the final scale for the summed SG.

This is the $\rv$ form for $G(\vv;\muv,\lambda, a)$. It includes an additional weight value you can think of like the energy this SG is adding to the sum: \begin{equation} \begin{aligned} \rv_i &= \left( \coth(\lambda_i)-\frac{1}{\lambda_i} \right) \muv_i \\ w_i &= \frac{2\pi a_i}{\lambda_i} \left( 1 - e^{-2 \lambda_i} \right) \\ \end{aligned} \end{equation} This weight is of course used in the weighted sum \begin{equation} \begin{aligned} \rv &= \frac{\sum_{i=1}^{n} \rv_i w_i}{\sum_{i=1}^{n} w_i} \\ w &= \sum_{i=1}^{n} w_i \\ \end{aligned} \end{equation} Using eq \eqref{eq:r_to_vmf} and eq \eqref{eq:vmf_to_sg} we can convert back to a scaled vMF and finally to a SG in $G(\vv;\muv,\lambda, a)$ form: \begin{equation} \begin{aligned} G\left( \vv; \muv, \lambda, a \right) &= w V(\vv;\muv,\lambda) \\ &= G\left( \vv; \muv, \lambda, w \frac{\lambda}{ 2\pi \left( 1 - e^{-2 \lambda} \right) } \right) \end{aligned} \end{equation} While addition and filtering are approximate they can be useful. The accuracy of the result is very dependent on the angle between the $\mu$ vectors or lobe axii. Adding sharp lobes pointed in different directions will result in a single wide lobe.

Next, what we can use this for:

[Normal map filtering using vMF](https://graphicrants.blogspot.com/2018/05/normal-map-filtering-using-vmf-part-3.html)

### References

[1][Banerjee et al. 2005, "Clustering on the Unit Hypersphere using von Mises-Fisher Distributions"](http://jmlr.org/papers/volume6/banerjee05a/banerjee05a.pdf)

[2]

[Jakob 2012, Numerically stable sampling of the von Mises Fisher distribution on S2 (and other tricks)"](http://www.mitsuba-renderer.org/~wenzel/files/vmf.pdf)

## No comments:

Post a Comment