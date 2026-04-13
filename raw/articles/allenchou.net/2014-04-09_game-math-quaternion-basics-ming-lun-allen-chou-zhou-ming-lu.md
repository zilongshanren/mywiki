---
title: 'Game Math: Quaternion Basics | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/04/game-math-quaternion-basics/
author: Allen Chou
published: '2014-04-09'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

A quaternion is a very useful mathematical object devised by [Sir William Rowan Hamilton](http://en.wikipedia.org/wiki/William_Rowan_Hamilton) as an extension to [complex numbers](http://en.wikipedia.org/wiki/Complex_number). It is often used to compactly represent 3D orientations with just four floating-point numbers, as opposed to using a 3-by-3 matrix that contains nine floating-point numbers, and it has other nice properties that I will talk about later.

As its name suggests, a quaternion is composed of four components, one in the **real part**, and the other three in the **imaginary part**. A quaternion is usually denoted as:

![Rendered by QuickLaTeX.com \[ q = w + xi + yj + zk, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-771ba63d1bec465b195003f07d06245a_l3.png)


where ![Rendered by QuickLaTeX.com w](../../assets/fdb8d80aa4044c76.png)

![Rendered by QuickLaTeX.com (i, j, k)](../../assets/38d20d92165fd5de.png)

![Rendered by QuickLaTeX.com (x, y, z)](../../assets/d07300f37c3ec746.png)


For brevity, I will use the notation below to represent a quaternion:

![Rendered by QuickLaTeX.com \[ q = [w, \overrightarrow{v}], where \overrightarrow{v} = (x, y, z). \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-01824fbcec87b23b4ac8fa721000ed93_l3.png)


### The Fundamental Formula for Quaternions

Below is the fundamental formula that governs the arithmetics of quaternions:

![Rendered by QuickLaTeX.com \[ i^2 = j^2 = k^2 = ijk = -1 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-cf2f03bdcffb9af04ea8cf48fc27c7a0_l3.png)


With this formula, we can derive the following identities:


![Rendered by QuickLaTeX.com \begin{flalign*} ij &= k \\ jk &= i \\ ki &= j \\ ji &= -k \\ kj &= -i \\ ik &= -j \\ \end{flalign*}](../../assets/e6e0b538c27a3166.png)


[ ]

Thus, if we expand the product of two quaternions, we will arrive at the **quaternion multiplication formula**:

![Rendered by QuickLaTeX.com \begin{flalign*} q_1 q_2 &= (w_1 + x_1 i + y_1 j + z_1 k) (w_2 + x_2 i + y_2 j + z_2 k) \\ &= [w_1, \overrightarrow{v_1}] [w_2, \overrightarrow{v_2}] \\ &= [(w_1 w_2 - \overrightarrow{v_1} \cdot \overrightarrow{v_2}), (w_1 \overrightarrow{v_2} + w_2 \overrightarrow{v_1} + \overrightarrow{v_1} \times \overrightarrow{v2})] \\ \end{flalign*}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4186e3ae2b4df12366b0c589c785d9bc_l3.png)


Note that quaternion multiplication is **associative**:

![Rendered by QuickLaTeX.com \[ q_1 q_2 q_3 = (q_1 q_2) q_3 = q_1 (q_2 q_3) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-32f5dc02470a9f526aeebf47c8f1b984_l3.png)


but generally **not commutative**:

![Rendered by QuickLaTeX.com \[ q_1 q_2 \neq q_2 q_1 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2e7695975827d8ba90fda8aa8f29c8f9_l3.png)


**Adding** and **subtracting** two quaternions are just like adding and subtracting two 4D vectors:

![Rendered by QuickLaTeX.com \[ q_1 \pm q_2 = [w_1 \pm w_2, \overrightarrow{v_1} \pm \overrightarrow{v_2}] \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-80b3b61a17487b357a3eb72cbd3d17f5_l3.png)


**Multiplying** a quaternion by a scalar is as simple as multiplying individual component by the scalar:

![Rendered by QuickLaTeX.com \[ c q = [ c w, c \overrightarrow{v}] \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2921c7440554232e2e29a6bac0beeefb_l3.png)


The **dot product** of two quaternions is the sum of products of corresponding components:

![Rendered by QuickLaTeX.com \[ q_1 \cdot q_2 = w_1 w_2 + x_1 x_2 + y_1 y_2 + z_1 z_2 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4a21736ff15faad64105dba0aedf4a3f_l3.png)


### Unit Quaternions

The **magnitude** of a quaternion is calculated as follows:

![Rendered by QuickLaTeX.com \[ || w, \overrightarrow{v} || = \sqrt{w^2 + x^2 + y^2 + z^2} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6004a73447b790161e658852e580aefa_l3.png)


A **unit quaternion** has a magnitude of one. The product of two unit quaternions is also a unit quaternion. To **normalize** a quaternion means dividing each quaternion component by the quaternion’s magnitude.

For convenience, game developers usually just work with unit quaternions. After many multiplications, a quaternion can become non-normalized, so we sometimes need to re-normalize a quaternion to make sure it stays normalized. The approximation technique described in [this post](http://allenchou.net/2014/02/game-math-fast-re-normalization-of-unit-vectors/) can be used to re-normalize an almost-normalized quaternion without using the square root function and floating-point division.

### Quaternion Inverses

For a quaternion ![Rendered by QuickLaTeX.com q](../../assets/6bacf3521f213f9b.png)

**multiplicative inverse** (or **inverse** for short) is denoted ![Rendered by QuickLaTeX.com q^{-1}](../../assets/7e73044e0716bd68.png)


![Rendered by QuickLaTeX.com \[ q q^{-1} = q^{-1} q = 1 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b05df5edaa22108d45f44592126c6847_l3.png)


If the quaternion ![Rendered by QuickLaTeX.com q = [w, \overrightarrow{v}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1e24a1f42426d368a1959790f617bcf1_l3.png)

**conjugate**:

![Rendered by QuickLaTeX.com \[ q^{-1} = \overline{q} = [w, -\overrightarrow{v}] \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-c537681c051b1781212b9d2f11a44d74_l3.png)


Just like that, as easy as negating the imaginary part. This is one of the many reasons why game developers prefer working with unit quaternions. Otherwise, the inversion process would involve a floating-point division by the magnitude of the quaternion.

Also, the inverse of a quaternion product of two quaternions would be equal the individual quaternion inverses multiplied in reverse order:

![Rendered by QuickLaTeX.com \[ (q_1 q_2)^{-1} = q_2^{-1} q_1^{-1} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3ab84ef85642d2adc14cd1e2bb30714d_l3.png)


Proof:

![Rendered by QuickLaTeX.com \begin{flalign*} (q_1 q_2)^{-1} (q_1 q_2) &= q_2^{-1} q_1^{-1} q_1 q_2 \\ &= q_2^{-1} (q_1^{-1} q_1) q_2 \\ &= q_2^{-1} q_2 = 1 \end{flalign*}](../../assets/b94f77305371789e.png)


### 3D Orientations

Every orientation in 3D can be represented using the [axis-angle representation](http://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation), and there is a mapping between an axis-angle pair and a unit quaternion.

For an orientation represented by an axis ![Rendered by QuickLaTeX.com \overrightarrow{n}](../../assets/58afda5173643155.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![Rendered by QuickLaTeX.com \[ q = [cos\frac{\theta}{2}, \overrightarrow{n} sin\frac{\theta}{2}] \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-073c21929ce71cdb3fe2892e4e59f843_l3.png)


When we have a 3D vector ![Rendered by QuickLaTeX.com \overrightarrow{r}](../../assets/665cf8264d118337.png)

![Rendered by QuickLaTeX.com q](../../assets/6bacf3521f213f9b.png)


![Rendered by QuickLaTeX.com \[ [0, \overrightarrow{r}'] = q [0, \overrightarrow{r}] q^{-1}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1cf25c6b12addf9d19eedc85f6f3cfa2_l3.png)


where ![Rendered by QuickLaTeX.com \overrightarrow{r}'](../../assets/6e290a96dabf0e24.png)


### Rotation Concatenation

Concatenation of two rotations represented by two quaternions, ![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)


So the formula below:

![Rendered by QuickLaTeX.com \[ [0, \overrightarrow{r}''] = (q_2 q_1) [0, \overrightarrow{r}] (q_2 q_1)^{-1} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-028818d3ce7a637dac54a111e7ff89bc_l3.png)


would give the resulting vector ![Rendered by QuickLaTeX.com \overrightarrow{r}''](../../assets/030bad7cc186862d.png)

![Rendered by QuickLaTeX.com \overrightarrow{r}](../../assets/665cf8264d118337.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)


![Rendered by QuickLaTeX.com \begin{flalign*} [0, \overrightarrow{r}''] &= (q_2 q_1) [0, \overrightarrow{r}] (q_2 q_1)^{-1} \\ &= q_2 q_1 [0, \overrightarrow{r}] q_1^{-1} q_2^{-1} \\ &= q_2 (q_1 [0, \overrightarrow{r}] q_1^{-1}) q_2^{-1} \\ &= q_2 [0, \overrightarrow{r}'] q_2^{-1} \end{flalign*}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-fd8e2b680b42f26e3bcbce8b082e5546_l3.png)


where ![Rendered by QuickLaTeX.com \overrightarrow{r}'](../../assets/6e290a96dabf0e24.png)

![Rendered by QuickLaTeX.com \overrightarrow{r}](../../assets/665cf8264d118337.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)


### Slerp

**Slerp** (spherical linear interpolation) is a very important quaternion operation. It allows you to interpolate between two orientations along the “shortest path” if the two quaternions used are of the same magnitude (another good reason to work with only unit quaternions). This is a non-trivial task if you represent 3D orientations using [rotation matrices](http://en.wikipedia.org/wiki/Rotation_matrix) or [Euler angles](http://en.wikipedia.org/wiki/Euler_angles). Below is the formula for slerping from a quaternion ![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)


![Rendered by QuickLaTeX.com \[ Slerp(q_1, q_2, t) = \frac{sin((1 - t)\Omega)}{sin\Omega}q_1 + \frac{sin(t\Omega)}{sin\Omega}q_2, \, 0 \le t \le 1, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4a231d4f391da718761095c7f71b3370_l3.png)


where ![Rendered by QuickLaTeX.com \Omega](../../assets/6ccca86ab1ee1829.png)


![Rendered by QuickLaTeX.com \[ \Omega = cos^{-1}(q_1 \cdot q_2) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-0d736046e38a8d9d6e2e7567a677eadf_l3.png)


One nice thing about slerp is the linearity of interpolation with respect to the parameter ![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com t = 0.5](../../assets/5fc33fb83a0da87b.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)


There is one caveat, though. Exactly two quaternions can map to the same orientation, namely ![Rendered by QuickLaTeX.com q = [w, \overrightarrow{v}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1e24a1f42426d368a1959790f617bcf1_l3.png)

![Rendered by QuickLaTeX.com -q = [-w, -\overrightarrow{v}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f93406ba0561ef681f133a1fd0bf382c_l3.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com -q_2](../../assets/db43df97001ac59c.png)

![Rendered by QuickLaTeX.com q_1 \cdot q_2 < 0](../../assets/1ea205001868d01a.png)


### End of Quaternion Basics

That’s it. I have covered the basic operations for quaternions, how to represent a 3D orientation using a quaternion, how to rotate a point using quaternions, and a nice tool called “slerp” to interpolate between two 3D orientations along the “shortest path”.

Nice blog as always, I feeling lost at quaternion multiplication formula dot and cross product, my math completely rusted. 🙂