---
title: Mikkelsen and 3D Graphics
url: http://mmikkelsen3d.blogspot.com/2013/10/volume-height-maps-and-triplanar-bump.html
author: Morten S Mikkelsen
published: '2013-10-06'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Volume Height Maps and Triplanar Bump Mapping**

**Since I wrote this post I've written a new technical paper called "Surface Gradient Based Bump Mapping Framework" which does a better and more complete job describing the following.**

**All my papers can be found at**

[https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html](https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html)I know it has been a while but I thought I would like to emphasize an easily missed contribution in my paper

[Bump Mapping Unparametrized Surfaces on the GPU](https://www.dropbox.com/s/l1yl164jb3rhomq/mm_sfgrad_bump.pdf?dl=0). The new surface gradient based formulation (eq. 4) of Jim Blinn's perturbed normal unifies conventional bump mapping and bump mapping from height maps defined on a volume. In other words you do not have to bake such heights to a 2D texture first to generate

Jim Blinn's perturbed normal. The formula also suggests that a well known

[method](http://web.cse.ohio-state.edu/~shen.94/681/Site/Slides_files/p287-perlin.pdf)proposed by Ken Perlin is wrong. For a more direct visual confirmation a difference is shown in figure 2. The black spots on the left are caused by subtracting the volume gradient which causes the normal to implode. The result on the right is when using the new surface gradient based formulation and as you see the errors are gone.

To give an example of how the theoretical math might apply to a real world practical case

let us take a look at triplanar projection. In this case we have a parallel projection

along each axis and we use a derivative/normal map for each projection.

Let's imagine we have three 2D height maps.

H_x: (s,t) --> R

H_y: (s,t) --> R

H_z: (s,t) --> R

The corresponding two channel derivative maps are represented as (dH_x/ds, dH_x/dt) and similar for the other two height maps. Using the blend weights described on page 64 in the

[presentation](http://www.slideshare.net/icastano/cascades-demo-secrets)by Nvidia on triplanar projections, let us call them w0-w2, the mixed height function defined on a volume can now be given as

H(x,y,z) = H_z(x,y)*w0 + H_x(z,y)*w1 + H_y(z,x)*w2

The goal is to use equations 2 and 4 on it to get the perturbed normal.

However, notice the blend weights w0, w1 and w2. These are not really constant.

They depend on the initial surface normal. In my paper I mention that the height map

defined on a volume does not have to be global. It can be a local extension on an open

subset of R^3. What that means (roughly) is at every given point we just need to know some local height map function defined on an arbitrarily small volume which contains the point.

At every given point we can assume the initial normal is nearly constant within some small neighborhood. This is the already applied approximation by Jim Blinn himself.

Constant "enough" at least that its contributions, as a varying function, to the gradient

of H will be negligible. In other words in the local height map we treat w0, w1 and w2 as constants.

Now to evaluate equation 2 using H as input function we need to find the regular gradient of H

Grad(H) = w0 * Grad(H_z) + w1 * Grad(H_x) + w2 * Grad(H_y)

= w0*[ dH_z/ds dH_z/dt 0 ]^T +

w1*[ 0 dH_x/dt dH_x/ds ]^T +

w2*[ dH_y/dt 0 dH_y/ds ]^T

[w0*dH_z/ds + w2*dH_y/dt]

= [w0*dH_z/dt + w1*dH_x/dt]

[w1*dH_x/ds + w2*dH_y/ds]

Now that we have the gradient this can be used in equation 2 and subsequently equation 4. Another way to describe it is to use this gradient with Listing 3 in the paper.

The derivation in this post is according to OpenGL conventions. In other words assuming a right hand coordinate system and Y is up. Furthermore, using lower left corner as texture space origin. Let me know if you need help reordering things to D3D.

This comment has been removed by a blog administrator.

ReplyDeleteThis comment has been removed by a blog administrator.

ReplyDelete