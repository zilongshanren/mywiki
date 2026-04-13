---
title: The Transformation Matrix
url: https://www.alanzucconi.com/2016/02/10/tranfsormation-matrix/
author: Alan Zucconi
published: '2016-02-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will introduce the Transformation Matrix, one of the standard technique to translate, rotate and scale 2D graphics. The first part of this series, [A Gentle Primer on 2D Rotations](https://www.alanzucconi.com/2016/02/03/2d-rotations/), explaines some of the Maths that is be used here.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Matrix notation](https://www.alanzucconi.com#part1) - Part 2.
[Adding translations](https://www.alanzucconi.com#part2) - Part 3.
[Composition](https://www.alanzucconi.com#part3) - Part 4.
[Inversion](https://www.alanzucconi.com#part4) - Part 5.
[Rotation around a point](https://www.alanzucconi.com#part5) [Conclusion](https://www.alanzucconi.com#conclusion)

In the previous post we have seen how a 2D point ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)


![2d transform 2](../../assets/428e7d26b1ef82b4.png)

In a nutshell:

![Rendered by QuickLaTeX.com \[x=R \, \cos\left(\theta\right ) \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e8b2e786f6267b518d76c162e95cad2a_l3.png)


![Rendered by QuickLaTeX.com \[y=R \, \sin\left(\theta\right ) \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6aefa2309257048436b8d20d744271fe_l3.png)


The second important result is that any given point ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![Rendered by QuickLaTeX.com \[{x}' = x \, \cos\left(\theta\right)- y\, \sin\left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fade6d9535a96a1ce3e8729b8019470_l3.png)


![Rendered by QuickLaTeX.com \[{y}' = x\, \sin\left(\theta\right) + y \, \cos\left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b674791ad82cae94818ac9e2ff6c17b7_l3.png)


These are the only two notions you need to understand this tutorial.

When it comes to 3D graphics, there’s an alternative representation that is often encountered. A rotation can, in fact, be expressed as a matrix multiplication. To do this, let’s express ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)

![Rendered by QuickLaTeX.com \begin{bmatrix}x & y\end{bmatrix}](../../assets/f22cec691d026533.png)

![Rendered by QuickLaTeX.com T\left(\theta\right)](../../assets/f0de7f20bda5f123.png)


![Rendered by QuickLaTeX.com \[T\left(\theta\right)\cdot\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}x\,\cos\left(\theta\right) -y\,\sin\left(\theta\right) \\x\,\sin\left(\theta\right) + y\,\cos\left(\theta\right)\end{bmatrix}=\begin{bmatrix}{x}' \\ {y}'\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c25c5e3d4576756c172e415c20e9f5cc_l3.png)


The matrix ![Rendered by QuickLaTeX.com T\left(\theta\right)](../../assets/f0de7f20bda5f123.png)


![Rendered by QuickLaTeX.com \[\underbrace{\begin{bmatrix}\cos\left(\theta\right) & -\sin\left(\theta\right) \\\sin\left(\theta\right) & \cos\left(\theta\right)\end{bmatrix}}_{T\left(\theta\right)}\cdot\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}x\,\cos\left(\theta\right) -y\,\sin\left(\theta\right) \\x\,\sin\left(\theta\right) + y\,\cos\left(\theta\right)\end{bmatrix}=\begin{bmatrix}{x}' \\ {y}'\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-daad9536a552b3e92cbf54b3e7643e4b_l3.png)


Every rotation of ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com T\left(\theta\right)](../../assets/f0de7f20bda5f123.png)


There are other operations which, unfortunately, cannot be achieved with this matrix. Translations is one of them. What we want is a new matrix ![Rendered by QuickLaTeX.com T\left(t_x, t_y\right)](../../assets/7b39ae4e24b1a73f.png)


![Rendered by QuickLaTeX.com \[T\left(t_x, t_y\right)\cdot\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}x+ t_x \\y+ t_y\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-295f027d1d1a5b65d3cd31b1f04f3ebd_l3.png)


This is not possible with the current setting. In order to obtain this result, we need to modify the way ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)


![Rendered by QuickLaTeX.com \[\underbrace{\begin{bmatrix}1&0 & t_x \\0 & 1 & t_y \\0 & 0 & 1 \\\end{bmatrix}}_{T\left(t_x, t_y\right)}\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}=\begin{bmatrix}x+t_x\\y +t_y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7ebc1704849fd24e68971e0d2fdd3e5e_l3.png)


The point ![Rendered by QuickLaTeX.com \left(x,y\right)](../../assets/b55fb2e0fe05e831.png)

![Rendered by QuickLaTeX.com \begin{bmatrix}x & y & 1\end{bmatrix}](../../assets/fd6dffc69f19d172.png)

![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)


Using matrices to perform transformation has an incredible advantage: they can be multiplied together to perform multiple transformation. A single matrix can hold as many transformation as you like. In a nutshell:

![Rendered by QuickLaTeX.com \[T_2 \cdot\left (T_1 \cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\right)=\left (T_2 \cdot T_1\right)\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f9f0ad177726e4b8c5b6cb48948eb005_l3.png)


This is true because matrix multiplication is an associative operator. It is important to remember, however, that these transformations are not commutative. This means that ![Rendered by QuickLaTeX.com T_2 \cdot T_1](../../assets/333d93e2ddc43a50.png)

![Rendered by QuickLaTeX.com T_1 \cdot T_2](../../assets/fe51a6f1aa1adf61.png)


Transformations can be undone. For every transformation matrix ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com T^{-1}](../../assets/a308f872a5499002.png)

![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com T^{-1}](../../assets/a308f872a5499002.png)


![Rendered by QuickLaTeX.com \[T^{-1} \cdot\left (T \cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\right)=\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-1b8866aa3b95df8de74fb5da6bd3c5af_l3.png)


By using the associative property, we can get a glimpse of what this matrix is:

![Rendered by QuickLaTeX.com \[\left (T^{-1} \cdotT\right)\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}=\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-080c2c62e1f111700d2469a447aaf2c0_l3.png)


![Rendered by QuickLaTeX.com \[\left (T^{-1} \cdotT\right)\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}=\mathbb{I}\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c7a6c2e50f9fda2cbdd4c85d73afb12e_l3.png)


![Rendered by QuickLaTeX.com \[T^{-1} \cdot T = \mathbb{I}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-28b14aa4d31bf91da69d005631a27883_l3.png)


If you have a basic knowledge of matrix algebra, you should recognise this: ![Rendered by QuickLaTeX.com T^{-1}](../../assets/a308f872a5499002.png)

[inverse matrix](https://en.wikipedia.org/wiki/Invertible_matrix) of ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)


![Rendered by QuickLaTeX.com \[T\left(-\theta\right) \cdot\left (T\left(+\theta\right)\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\right)=\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-43e83b62c926b22b7707692d7ed598e9_l3.png)


![Rendered by QuickLaTeX.com \[T\left(-x,-y\right) \cdot\left (T\left(+x,+y\right)\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\right)=\begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8f55f4d1dea4abbe44c26ad1fddc7fe4_l3.png)


The meaning of these two equations should be intuitive to grasp: if you rotate a point of ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com -\theta](../../assets/02ea7b02e2a19f1b.png)


![Rendered by QuickLaTeX.com \[T\left(+\theta\right)^{-1} = T\left(-\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-64c3702fea6368556b3dde40e33a92a3_l3.png)


![Rendered by QuickLaTeX.com \[T\left(+x,+y\right)^{-1} = T\left(-x,-y\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-665ce71150113626c48c3eec715836f0_l3.png)


From this, it follows that if you have a series of elementary rotations and translations, the inverse of their composition is the composition of their inverses, in reversed order:

![Rendered by QuickLaTeX.com \[\left( T_n \cdot T_{n-1}\cdot \dots \cdot T_2\cdot T_1 \right)^{-1}= T_1^{-1} \cdot T_2^{-1} \cdot T_{n-1}^{-1}\cdot \dots \cdot T_n^{-1}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a08b3e2e3d088596030e6f8ffd2a67d6_l3.png)


As seen in the previous part of this tutorial ([A Gentle Primer on 2D Rotations](https://www.alanzucconi.com/2016/02/03/2d-rotations/)), to rotate around an arbitrary point, we need to first make that our new origin of the Cartesian plane. Then we rotate the point, and finally we restore the origin of the plane. This can be expressed a composition of three transformations:

![Rendered by QuickLaTeX.com \[T\left(P_x,P_y\right) \cdot T\left(\theta\right) \cdot T\left(-P_x,-P_y\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7af36dbba5425d88a4adb8b144d89b0b_l3.png)


It’s important to remember that, despite the order in which they are written, the first transformation is the one on right.

### 📚 Recommended Books

This post has introduced the transformation matrix, which is one of the standard ways in which transformations are stored and performed in computer graphics. We have explored the following transformations:

- Translation by

:

![Rendered by QuickLaTeX.com \[\underbrace{\begin{bmatrix}1 & 0 & t_x\\0 & 1 & t_y \\0 & 0 & 1\end{bmatrix}}_{T\left(t_x, t_y\right)}\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}=\begin{bmatrix}x + t_x \\x + t_y \\1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f05823bee9681077444892673444dcca_l3.png)


- Rotation by

around the origin:

![Rendered by QuickLaTeX.com \[\underbrace{\begin{bmatrix}\cos\left(\theta\right) & -\sin\left(\theta\right) & 0\\\sin\left(\theta\right) & \cos\left(\theta\right) & 0 \\0 & 0 & 1\end{bmatrix}}_{T\left(\theta\right)}\cdot\begin{bmatrix}x \\ y \\ 1\end{bmatrix}=\begin{bmatrix}x\,\cos\left(\theta\right) -y\,\sin\left(\theta\right) \\x\,\sin\left(\theta\right) + y\,\cos\left(\theta\right) \\1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f473fc2c6b313c6644a3c16575d39704_l3.png)


- Rotation by

around the point

:

![Rendered by QuickLaTeX.com \[T\left(P_x,P_y\right) \cdot T\left(\theta\right) \cdot T\left(-P_x,-P_y\right) \cdot \begin{bmatrix}x \\ y \\ 1\end{bmatrix}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-69f6f1bc3421fea2eb2a2f42084dc94f_l3.png)


The main advantage of the matrix notation is that transformations can be composed by multiplying their respective transformation matrices. This also allows to “undo” transformation by calculating the inverse of its matrix.

The next post in this series will focus on the geometrical consequences of the equations we have derived. This will help to demystify one of the most misunderstood concept of Maths: complex numbers. Their understanding is essential for quaternions.

#### Other resources

- Part 1.
[A Gentle Primer on 2D Rotations](https://www.alanzucconi.com/2016/02/03/2d-rotations/) - Part 2.
**The Transformation Matrix** - Part 3. Rotations in the Complex Plane
- Part 4. Understanding Rotations in 3D
- Part 5. Understanding Quaternions
[Matrices aren’t scary. They’re essential.](http://catlikecoding.com/unity/tutorials/rendering/part-1/)

## Leave a Reply Cancel reply