---
title: Spherical Integration
url: https://thenumb.at/Spherical-Integration/
published: '2023-01-08'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Spherical Integration

*Or, where does that $$\sin\theta$$ come from?*

Integrating functions over spheres is a ubiquitous task in graphics—and a common source of confusion for beginners. In particular, understanding why integration in spherical coordinates requires multiplying by $$\sin\theta$$ takes some thought.

# The Confusion

So, we want to integrate a function $$f$$ over the unit sphere. For simplicity, let’s assume $$f = 1$$. Integrating $$1$$ over any surface computes the area of that surface: for a unit sphere, we should end up with $$4\pi$$.

Integrating over spheres is much easier in spherical coordinates, so let’s define $$f$$ in terms of $$\theta, \phi$$:

$$\theta$$ ranges from $$0$$ to $$\pi$$, representing latitude, and $$\phi$$ ranges from $$0$$ to $$2\pi$$, representing longitude. Naively, we might try to integrate $$f$$ by ranging over the two parameters:

That’s not $$4\pi$$—we didn’t integrate over the sphere! All we did was integrate over a flat rectangle of height $$\pi$$ and width $$2\pi$$. One way to conceptualize this integral is by adding up the differential area $$dA$$ of many small rectangular patches of the domain.

Each patch has area $$dA = d\theta d\phi$$, so adding them up results in the area of the rectangle. What we actually want is to add up the areas of patches *on the sphere*, where they are smaller.

In the limit (small $$d\theta,d\phi$$), the spherical patch $$d\mathcal{S}$$ is a factor of $$\sin\theta$$ smaller than the rectangular patch $$dA$$. 1 Intuitively, the closer to the poles the patch is, the smaller its area.

When integrating over the sphere $$\mathcal{S}$$, we call the area differential $$d\mathcal{S} = \sin\theta\, d\theta d\phi$$.[2](https://thenumb.at#fn:2)

Let’s try using it:

It works! If you just wanted the intuition, you can stop reading here.

# But why $$\sin\theta$$?

It’s illustrative to analyze how $$\sin\theta$$ arises from parameterizing the cartesian ($$x,y,z$$) sphere using spherical coordinates.

In cartesian coordinates, a unit sphere is defined by $$x^2 + y^2 + z^2 = 1$$. It’s possible to formulate a cartesian surface integral based on this definition, but it would be ugly.

Instead, we can perform a *change of coordinates* from cartesian to spherical coordinates. To do so, we will define $$\Phi : \theta,\phi \mapsto x,y,z$$:

\[ \begin{align*} \Phi(\theta,\phi) = \begin{bmatrix}\sin\theta\cos\phi\\ \sin\theta\sin\phi\\ \cos\theta\end{bmatrix} \end{align*} \] |

The function $$\Phi$$ is a *parameterization* of the unit sphere $$\mathcal{S}$$. We can check that it satisfies $$x^2+y^2+z^2=1$$ regardless of $$\theta$$ and $$\phi$$:

Applying $$\Phi$$ to the rectangular domain $$\theta\in[0,\pi],\phi\in[0,2\pi]$$ in fact describes all of $$\mathcal{S}$$, giving us a much simpler parameterization of the integral.

To integrate over $$d\theta$$ and $$d\phi$$, we also need to compute how they relate to $$d\mathcal{S}$$. Luckily, there’s a formula that holds for **any** parametric surface $$\mathbf{r}(u,v)$$ describing a three-dimensional domain $$\mathcal{R}$$:[3](https://thenumb.at#fn:3)

The two partial derivatives represent tangent vectors on $$\mathcal{R}$$ along the $$u$$ and $$v$$ axes, respectively. Intuitively, each tangent vector describes how a $$u,v$$ patch is stretched along the corresponding axis when mapped onto $$\mathcal{R}$$. The magnitude of their cross product then computes the area of the resulting parallelogram.

Finally, we can actually apply the change of coordinates:

We just need to compute the area term:

Since $$ \theta\in[0,\pi] $$, we can say $$ \lvert\sin\theta\rvert = \sin\theta $$. That means $$d\mathcal{S} = \sin\theta\, d\theta d\phi$$! Our final result is the familiar spherical integral:

## Footnotes

Interestingly, if we knew the formula for the area of a spherical patch, we could do some slightly illegal math to derive the area form:

\[\begin{align*} dA &= (\phi_1-\phi_0)(\cos\theta_0-\cos\theta_1)\\ &= ((\phi + d\phi) - \phi)(\cos(\theta)-\cos(\theta+d\theta))\\ &= d\phi d\theta \frac{(\cos(\theta)-\cos(\theta+d\theta))}{d\theta}\\ &= d\phi d\theta \sin\theta \tag{Def. derivative} \end{align*}\][↩︎](https://thenumb.at#fnref:1)In graphics, also known as

*differential solid angle*, $$d\mathbf{\omega} = \sin\theta\, d\theta d\phi$$.[↩︎](https://thenumb.at#fnref:2)Even more generally, the scale is related to the inner product on the tangent space of the surface. This inner product is defined by the

[first fundamental form](https://en.wikipedia.org/wiki/First_fundamental_form)$$\mathrm{I}$$ of the surface, and the scale factor is $$\sqrt{\det\mathrm{I}}$$, regardless of dimension. For surfaces immersed in 3D, this simplifies to the cross product mentioned above. Changes of coordinates that don’t change dimensionality have a more straightforward scale factor: it’s the determinant of their Jacobian.[4](https://thenumb.at#fn:4)[↩︎](https://thenumb.at#fnref:3)These topics are often more easily understood using the language of exterior calculus, where integrals can be uniformly expressed regardless of dimension. I will write about it at some point.

[↩︎](https://thenumb.at#fnref:4)