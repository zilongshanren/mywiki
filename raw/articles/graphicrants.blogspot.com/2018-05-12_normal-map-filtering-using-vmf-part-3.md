---
title: Normal map filtering using vMF (part 3)
url: http://graphicrants.blogspot.com/2018/05/normal-map-filtering-using-vmf-part-3.html
author: Brian Karis
published: '2018-05-12'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This mapping for Beckmann is given by [1] as: \begin{equation} \lambda \approx \frac{2}{\alpha^2} \label{eq:roughness_to_lambda} \end{equation} and following my

[previous post about specular models](https://graphicrants.blogspot.com/2013/08/specular-brdf-reference.html)we can use the $\alpha$ from any of those distributions in this equation for a reasonable approximation.

Once you have vMFs we can sum or filter them in $\rv$ form. Then we can turn it back to normal and roughness by inverting the function: \begin{equation} \alpha \approx \sqrt{\frac{2}{\lambda}} \label{eq:lambda_to_roughness} \end{equation} We must be careful with floating point precision and divide by zero though. Instead of calculating $\lambda$ we can instead calculate its reciprocal which avoids multiple places where a divide by nearly zero can happen.

How does this compare to the common approaches? The first to do something like this was Toksvig [2] which follows similar logic with vector length corresponding with gloss and uses properties of Gaussian distributions but not SGs exactly. LEAN mapping [3] is based on Gaussians as well but planar distributions, not spherical. The approach I just explained should in theory work just as well with object space normals.

Even though it was part of the original approach the common way to use "Toksvig" filtering (including UE4's implementation) is to find the normal variance and increase the roughness by it. There is no influence from the roughness on the normals when doing that and there should be. The correct way will affect how the normals are filtered. A smooth normal should have more weight in the filter than a rough normal.

vMF has been used for this task before in [5] and later [6]. There is a major difference from our approach in that Frequency domain normal map filtering relies on convolving instead of averaging. It finds the vMF for the distribution of normals over the filter region. It then convolves the normal and roughness by that vMF. But what is a convolution?

### Convolution

Graphics programmers know of convolutions like blurring. It sort of spreads data out right? What does it mean mathematically though? A convolution of one function by another creates a new function that is equivalent to the integral of the function being convolved multiplied by a the convolving function translated to that point.Think of a blur kernel with weights per tap. That kernel center is translated to the pixel in the image that we write the blur result to. Each tap of the kernel is a value from the blur function. We multiply those kernel values by the image that is being convolved. All of those samples are then added together. Now usually a blur doesn't have infinite support or every pixel of the image would need to be sampled but the only reason that doesn't need to happen is because the convolving function, ie the blur kernel, is zero past a certain distance from the center of the function. Otherwise the integral needs to cover the entire domain. In the 1D case that means from negative to positive infinity. In the case of a sphere that means over the entire surface of the sphere.

This symbolically looks like this for 1D: \begin{equation} (f * g) (x) = \int_{-\infty}^\infty f(t) g(x-t)\,dt \end{equation} We now have the definition but why would we want to convolve a function besides image blurring? A convolution of one function by another creates a new function that when evaluated is equal to if the both functions were multiplied together and integrated at that translated point. Think of this like precalculating the multiplication and integration of those functions for any translated point. The integral of the product is done ahead of time and now we can evaluate it for any translation.

This is exactly the use case for preconvolving environment maps by the reflected GGX distribution. GGX is the convolving function, the environment map is the function being convolved, the reflection vector direction used to sample the preconvolved environment map is the "translation". SGs are very simple to multiply and integrate as we have already seen so precomputing it often doesn't save much. Convolving does have its uses though so let's see how to do it.

### Convolving SGs

The convolution of two SGs is not closed in the SG basis, meaning it does not result in exactly a SG. Fortunately it can be well approximated by one. [7] gave a simple approximation that is fairly accurate so long as the lobe sharpnesses aren't very low: \begin{equation} \begin{aligned} \left(G_1 * G_2\right) \left( \vv \right) &= \int_{S^2} G_1(\omegav) G_2\left( \omegav; \vv, \lambda_2, a_2 \right) \,d\omegav \\ &\approx G \left( \vv; \muv_1, \frac{\lambda_1 \lambda_2}{\lambda_1 + \lambda_2}, 2\pi\frac{a_1 a_2}{\lambda_1 + \lambda_2} \right) \end{aligned} \label{eq:convolve_sg} \end{equation} The first line of the equation above may shed more light on how we can use this if it isn't clear already. This is identical to the inner product but with $\muv_2$ replaced with a free parameter.For the case of normal map filtering we don't care about amplitude. We want a normalized SG. That means for this case the only part that matters is the convolved $\lambda'$: \begin{equation} \lambda' = \frac{\lambda_1 \lambda_2}{\lambda_1 + \lambda_2} \end{equation} We can ignore the rest of eq \eqref{eq:convolve_sg} for the moment. If we replace $\lambda$ everywhere with $\alpha$ using eq \eqref{eq:lambda_to_roughness} we get a nice simple equation: \begin{equation} \alpha' = \sqrt{ \alpha_1^2 + \alpha_2^2 } \end{equation} Leave $\lambda$ in for one of them and we get: \begin{equation} \alpha' = \sqrt{ \alpha^2 + \frac{2}{\lambda} } \label{eq:alpha_prime} \end{equation} which looks just like what [6] used except for the 2 factor. I believe this is a mistake in their course notes. In equation (37) of their notes they have it as 1/2 and in the code sample it is 1. I think the confusion comes from the Frequency Domain Normal Map Filtering paper working with Torrance Sparrow and not Cook Torrance, and $\sigma \neq \alpha$. Overall it means less roughness from normal variance. In my tests using eq \eqref{eq:alpha_prime} that we just derived looks closer to Toksvig results. Otherwise the range is off and less rough. MJP uses the same 2/a^2 for SG sharpness in his blog post so we don't disagree there.

As a gut check if $\alpha=0$ and all final roughness comes from normal variation then $\alpha'=\sqrt{\frac{2}{\lambda}}$ which is what we established in eq \eqref{eq:lambda_to_roughness}. If there is no normal variation then this equation explodes but if you calculate InvLambda like I did in the code snippet the second term becomes zero and $\alpha'=\alpha$ which is what we want.

Next up, converting from SH to SG (coming soon).

### References

[1][Wang et al. 2007, "All-Frequency Rendering of Dynamic, Spatially-Varying Reflectance"](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/12/sg.pdf)

[2]

[Toksvig 2004, "Mipmapping Normal Maps"](https://developer.download.nvidia.com/whitepapers/2006/Mipmapping_Normal_Maps.pdf)

[3]

[Olano et al. 2010, "LEAN Mapping"](https://www.csee.umbc.edu/~olano/papers/lean/)

[4]

[Hill 2011, "Specular Showdown in the Wild West"](http://blog.selfshadow.com/2011/07/22/specular-showdown/)

[5]

[Han et al. 2007, "Frequency Domain Normal Map Filtering"](http://www.cs.columbia.edu/cg/normalmap/)

[6]

[Neubelt et al. 2013, "Crafting a Next-Gen Material Pipeline for The Order: 1886"](http://blog.selfshadow.com/publications/s2013-shading-course/rad/s2013_pbs_rad_notes.pdf)

[7]

[Iwasaki 2012, "Interactive Bi-scale Editing of Highly Glossy Materials"](http://www.wakayama-u.ac.jp/~iwasaki/project/biscale/sa2012.pdf)

## No comments:

Post a Comment