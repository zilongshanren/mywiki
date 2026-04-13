---
title: Sampling projected spherical caps with multiple importance sampling
url: http://momentsingraphics.de/SphericalCapMIS.html
published: '2019-06-10'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Sampling projected spherical caps with multiple importance sampling

This blog post answers a question that [Tomáš Davidovič](http://www.davidovic.cz/) from [Weta Digital](https://www.wetafx.co.nz/) had about the recently published [projected solid angle sampling for spherical caps](http://momentsingraphics.de/I3D2019.html). In Monte Carlo rendering, it is very common to combine several sampling techniques through multiple importance sampling. In this case, any of the sampling techniques may produce a sample and then you need to compute the probability density for producing this sample with each of the other techniques.

The current implementation of projected solid angle sampling can only give you the probability density for a sample that it produced on its own. Adding the functionality for multiple importance sampling requires a little bit of thought. Below we make the necessary derivations. This post is not self-contained, so you should read the [paper](http://momentsingraphics.de/I3D2019.html) first. Source code is available for download below.

## Computing the density

The good news first: If the center of the spherical light source is above the horizon, the procedure is simple. The projected spherical cap is sampled uniformly, so the density is constant. The code to compute it is readily available.

The solution is a bit more complicated if the center of the light source is below the horizon. Using notations from the paper, the density for this case is given by:

\[ p(\xi_0,\xi_1):=-\frac{t_y^2}{(c_z+r_z)^2A_D}\frac{\omega_{i,x}}{d_xs_y} \]In this formula, \(\xi_0,\xi_1\in[0,1]\) are the random numbers used to produce a sample through projected solid angle sampling. In the context of multiple importance sampling, we do not know them. The quantities \(t_y,c_z,r_z,A_D\in\mathbb{R}\) all characterize the geometry of the projected spherical cap and are known. However, \(\omega_{i,x},d_x,s_y\in\mathbb{R}\) depend on the unknown \(\xi_0,\xi_1\).

We have to work our way through the algorithm backwards to recover them from the given normalized direction \(\mathbf{\omega}_i\in\mathbb{R}^3\). For \(\omega_{i,x}\), a mere change of coordinates gives us the desired result:

\[ \omega_{i,x}=\mathbf{x}^\mathsf{T}\mathbf{\omega}_i \]\(s_y\) is the scaling along the y-axis that we apply to our original sample. It is defined as

\[ s_y:=r_y\sqrt{\frac{r_z^2-(\omega_{i,z}-c_z)^2}{r_z^2(t_y^2-d_z^2)}}. \]The only unknown quantities on the right-hand side are \(\omega_{i,z}\) and \(d_z\) but both are easily computed:

\begin{align} \omega_{i,z}&=\mathbf{z}^\mathsf{T}\mathbf{\omega}_i \\ d_z&=\frac{c_z+r_z}{t_y}\omega_{i,z} \end{align}Now the only missing quantity is \(d_x\), which is the x-coordinate of the sample on the unit sphere that we had before the warping. We have already undone the scaling along the z-axis. If we also undo the scaling along the y-axis, we know enough to compute \(d_x\):

\begin{align} \omega_{i,y}&=\mathbf{y}^\mathsf{T}\mathbf{\omega}_i \\ d_y&=\frac{\omega_{i,y}}{s_y} \\ d_x&=\sqrt{1-d_y^2-d_z^2} \end{align}And with that, we have all the quantities that we need to compute the density.

## Checking for a hit

If we sample the projected spherical cap, we know that our density is non-zero. However, other sampling techniques may produce any direction. We do not know whether this direction hits the spherical light source at all. Thus, we have to check whether the sampled direction is inside the spherical cap and above the horizon. If either of these tests fails, we do an early out returning zero. In the notation from the paper, that means \(\omega_{i,z}<0\) or \(\mathbf{\omega}_d^{\mathsf{T}}\mathbf{\omega}_i< v\). All required quantities are computed anyway, we just have to keep them around a little bit longer.

## Putting the pieces together

To implement all of this, we add two new members to `struct ProjectedSphericalCap`

:

```
float3 normalizedCenter;
float planeOriginDistance;
```


Both of these bear the name of existing local variables in `prepareProjectedSphericalCapSampling()`

, so we modify this function to use the members of `ProjectedSphericalCap`

instead. We could also make a whole new variant of this function to only compute the parts that are needed for density computation but there is not much to be gained there. To compute the density, we at least need to compute the projected solid angle and most computations serve this goal. The following lines are the only exceptions:

```
cap.cutEllipseAreaRatio=cutEllipseArea*cap.densityFactor;
cap.randomToCutEllipseAreaFactor=normalizedEllipseArea/cap.cutEllipseAreaRatio;
cap.randomToCutDiskAreaFactor=cutDiskArea/(1.0f-cap.cutEllipseAreaRatio);
```


Rather than introducing a whole new variant of the function, I prefer to trust the compiler to eliminate these unused variables. On CPU, you should use inlining to give your compiler the opportunity to do so.

Finally, we add a new function `computeProjectedSphericalCapSampleDensity()`

that determines whether the given direction is in the projected spherical cap and computes the appropriate density. Please note that this density is given with respect to the projected solid angle measure. If you want a density with respect to solid angle, you need to multiply by the cosine term \(\omega_{i,z}\). The implementation of the new function is part of the code download below.

## Downloads

The following two headers make the modifications listed above for the code in the Falcor demo: