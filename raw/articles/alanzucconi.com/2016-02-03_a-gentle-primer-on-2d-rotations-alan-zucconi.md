---
title: A Gentle Primer on 2D Rotations - Alan Zucconi
url: https://www.alanzucconi.com/2016/02/03/2d-rotations/
author: Alan Zucconi
published: '2016-02-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will introduce rotations, translations and other affine transformations. This knowledge is essential not just for 2D games, but also to understand Quaternions and transformations in 3D games. This first post of the series is a gentle primer on 2D rotations.

A point in a 2D space can be represented in a series of ways. Despite being all equivalent, each one finds its own applications. The Cartesian (left) and Polar (right) representations are the two most common ways to define 2D points.

![2d transform_01](../../assets/37edf31743d1120b.png)

While the former ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)

![Rendered by QuickLaTeX.com \left\langle R,\theta\right\rangle](../../assets/f22ae51b1138eca5.png)


![2d transform_02](../../assets/00fcc097a160dd8f.png)

These two representations are deeply connected by trigonometry, since:

![Rendered by QuickLaTeX.com \[x=R \, \cos\left(\theta\right ) \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e8b2e786f6267b518d76c162e95cad2a_l3.png)


![Rendered by QuickLaTeX.com \[y=R \, \sin\left(\theta\right ) \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6aefa2309257048436b8d20d744271fe_l3.png)


At this stage it doesn’t matter if you have never heard of the trigonometric functions *cosine *and *sine. *The only thing you should know to understand the rest of this post is that given a vector, cosine and sine are used to calculate the length of its projections onto the X and Y axes (in blue and red, respectively). Trigonometry is, in a nutshell, the glue that connects Cartesian and Polar representations of points.

Using trigonometry might seem an overkill, but there are many instances in which talking about angles is convenient. Rotations, for instance, are trivial to represent with angles.

![2d transform_03](../../assets/2ba9452f326ca88f.png)

In this image, the point ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)

![Rendered by QuickLaTeX.com \phi](../../assets/5894f23fcbaa6c26.png)

![Rendered by QuickLaTeX.com \left({x}',{y}'\right)](../../assets/aa0eef36fe72c922.png)


![Rendered by QuickLaTeX.com \[{x}' = R \, \cos\left(\theta + \phi\right )\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6d791e22cf095a00ebaf05ada70f6743_l3.png)


![Rendered by QuickLaTeX.com \[{y}' = R \, \sin\left(\theta + \phi\right )\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8cdd2fe63aa6ef9eefdf66bdf085f3de_l3.png)


Knowing the polar coordinates of ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)

![Rendered by QuickLaTeX.com \left({x}',{y}'\right)](../../assets/aa0eef36fe72c922.png)


Before doing this, we need a little refresher on trigonometry.

We can now use these identities to expand the sum of angles into:

![Rendered by QuickLaTeX.com \[{x}' = R \, \cos\left(\theta\right) \cos\left(\phi\right)- R \, sin\left(\theta\right) \sin\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-4bc2944b22dda1211dfaa0975fd464da_l3.png)


![Rendered by QuickLaTeX.com \[{y}' = R \, \sin\left(\theta\right) \cos\left(\phi\right)+ R \, \cos\left(\theta\right) \sin\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-3ca148b777b7fe88f1029e493cbdde30_l3.png)


From the initial definition of ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com y](../../assets/6cc181d8f36d0fd4.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


![Rendered by QuickLaTeX.com \[R=\frac{x}{\cos\left(\theta\right)}=\frac{y}{\sin\left(\theta\right)}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5e28253d9c3cf0323441fa015eb39582_l3.png)


Substituting:

![Rendered by QuickLaTeX.com \[{x}' = \boxed{\frac{x}{\cos\left(\theta\right)}} \, \cos\left(\theta\right) \cos\left(\phi\right)- \boxed{\frac{y}{\sin\left(\theta\right)}} \, \sin\left(\theta\right)\sin\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ce45595826e4ffc31722f8b07be11df0_l3.png)


![Rendered by QuickLaTeX.com \[{y}' = \boxed{\frac{y}{\sin\left(\theta\right)}} \, \sin\left(\theta\right) \cos\left(\phi\right)+ \boxed{\frac{x}{\cos\left(\theta\right)}} \, \cos\left(\theta\right)\sin\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-cbad7b5f2cfd1f04d996c9f98956e133_l3.png)


Simplifying:

![Rendered by QuickLaTeX.com \[{x}' = x \, \cos\left(\phi\right)- y\, \sin\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c06eac1eb2b8967e4a72d06516252f29_l3.png)


![Rendered by QuickLaTeX.com \[{y}' = x\, \sin\left(\phi\right) + y \, \cos\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0d42f021df2e967e57b470834362b330_l3.png)


Using trigonometry, we can now rotate points in 2D, even when they are not expressed in polar coordinates.

### 📚 Recommended Books

This post has introduced two ways of representing points in a 2D, and how they are connected by trigonometry. We have also shown how to rotate points in 2D in both representations.

Polar coordinates ![Rendered by QuickLaTeX.com \left\langle R,\theta\right\rangle](../../assets/f22ae51b1138eca5.png)


![Rendered by QuickLaTeX.com \[\left\langle R,\theta+\phi\right\rangle\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6b9a5a5d03f0e1e6bd2ee9d836c73b06_l3.png)


Cartesian coordinates ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)


![Rendered by QuickLaTeX.com \[{x}' = x \, \cos\left(\phi\right)- y\, \sin\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c06eac1eb2b8967e4a72d06516252f29_l3.png)


![Rendered by QuickLaTeX.com \[{y}' = x\, \sin\left(\phi\right) + y \, \cos\left(\phi\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0d42f021df2e967e57b470834362b330_l3.png)


The next post in this series will focus on how rotations can be expressed in matrix form. This is the next step to understand how quaternion works.

#### Other resources

- Part 1.
**A Gentle Primer on 2D Rotations** - Part 2.
[The Transformation Matrix](https://www.alanzucconi.com/2016/02/10/tranfsormation-matrix/) - Part 3. Rotations in the Complex Plane
- Part 4. Understanding Rotations in 3D
- Part 5. Understanding Quaternions

## Leave a Reply Cancel reply