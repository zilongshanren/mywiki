---
title: The Extended Kalman Filter - Alan Zucconi
url: https://www.alanzucconi.com/2022/07/24/extended-kalman-filter/
author: Alan Zucconi
published: '2022-07-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the third part of the series dedicated to one of the most popular sensor de-noising technique: Kalman filters. This article will explain how to model non-linear processes to improve the filter performance, something known as the **Extended Kalman Filter**.

You can read all the tutorials in this online course here:

- Part 1.
[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795) - Part 2.
[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain - Part 3.
[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models **Part 4:**[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models- Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

## Introduction

At the end of the previous article, we derived the equations for a Kalman filter able to work with linear models. In a nutshell, this means that we could use such a filter for any signal or quantity which changes over time in a linear fashion. If the assumption that both the measurement and process noises follow a normal distribution, Kalman filters are proven to be *optimal*.

Let’s recall the current structure of the Kalman filter:

![](../../assets/6e7082cc02b7d663.png)


![](../../assets/6e7082cc02b7d663.png)

And all of the equations that have been derived so far:

**Initialisation**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_0 & & \textup{initial state} \\P_0 &= 1& \textup{initial variance} \\Q & & \textup{process noise variance} \\R & & \textup{measurement noise variance} \\A & & \textup{model coefficient} \\B & & \textup{model offset}\end{align}\end{equation}](../../assets/9b57dc8fea68ec60.png)


**Prediction step**How we think the system should evolve, solely based on its model.

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_1^{-} & = A~\hat{x}_0 + B & \textup{state prediction} \\P_1^{-} & = A^2 ~ P_0 +Q & \textup{variance prediction} \\\end{align}\end{equation}](../../assets/51830ca4ab45a707.png)


**Correction step**The most likely estimation of the system state, integrating the sensor data.

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}k_1 & = \frac{P_1^{-}}{P_0+R} & \textup{Kalman gain} \\\hat{x}_1 &= \hat{x}_1^{-} \left(1-k_1\right) + z_1 \, k_1 & \textup{state update} \\P_1 & = \left(1-k_1\right) P_1^{-} & \textup{variance update}\end{align}\end{equation}](../../assets/daa81b3ac01e3b2a.png)


**Iteration**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_0 & \leftarrow \hat{x}_1 \\P_0 & \leftarrow P_1\end{align}\end{equation}](../../assets/c0ddcb7c6ac37df3.png)


You can get a feeling for how the system behaves using the interactive chart below, which gives you the ability to control the amount of noise in the process (![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


The rest of this article will focus on dismantling one of the strongest limitation of the current derivation: linear models.

![](../../assets/35afbe4b6e820e61.png)


![](../../assets/35afbe4b6e820e61.png)

We are now ready to fix this introducing the so-called **Extended Kalman Filter**.

## Non-Linear Models

The “magic” of the Kalman lies in a simple idea: both the sensor measurements (![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)


This means that in the next time frame the process can be repeated, since the new best estimated is once again a normal distribution.

However, updating the model alters its probability distribution. Allowing any function can break the assumption of its normal distribution. And if that fails, the guarantee of optimality fails as well.

The reason why this does not happen when using a linear model is that a linear combination of two normal distribution is a normal distribution itself. Under those assumptions, the equation for the state prediction respects the constraints that ultimately yields a good result:

(1) ![Rendered by QuickLaTeX.com \begin{equation*} x_1 = A~x_0 + B + v\end{equation*}](../../assets/e1d52a4221ddd10b.png)


What this means is that the “vanilla” implementation of the Kalman filter is guaranteed to be optimal only for processes which evolution can be modelled as a line. This is a very strong constraint, as many real-life processes tend to be non-linear.

In reality, what would really make a difference is the ability to use any generic function ![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} x_1 = f\left({x_0} \right)+ v\end{equation*}](../../assets/e1f2b22ef350943e.png)


While this is not always possible using Kalman filters, there is a variant that can handle non-linear functions, as long as they are **differentiable**: [Extended Kalman filters](https://en.wikipedia.org/wiki/Extended_Kalman_filter). Intuitively speaking, a function is differentiable if it can be drawn as a continuous, smooth line.

What an EFK does is finding a linear approximation of the function around its current estimate. So, in a way, even EKFs are still relying on a linear model. The interactive chart below show a sinusoid function; while non-linear, it can be approximated at any given point with a tangent line.

Such approximation can be very accurate if we stay around the tangent point. Translated to a signal, this means that approximating differentiable functions with a tangent line to their current state estimate is a good solution for short time intervals.

### Model Linearisation

To do so, the first step is to find a way to “linearise” a model around the current estimate. This means replace the non-linear model ![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)


One way way to approach this is to recall the equation of a line in its **point-slope form**:

(3) ![Rendered by QuickLaTeX.com \begin{equation*} y = y_p + m \left(x - x_p\right)\end{equation*}](../../assets/38e7ea138f004cc7.png)


Such an equation defines a line which passes through the point ![Rendered by QuickLaTeX.com \left(x_p, y_p\right)](../../assets/0289afb1b79b1c99.png)

![Rendered by QuickLaTeX.com m](../../assets/ae1726b8a02e3872.png)

![Rendered by QuickLaTeX.com \left(\hat{x}_0, f\left({\hat{x}_0}\right)\right)](../../assets/a618aaf278c8ab38.png)

![Rendered by QuickLaTeX.com f'\left({\hat{x}_0}\right)](../../assets/4139a1f7cc4f8f3c.png)


In order for this to work, it is necessary for the function that models the evolution of the system to be **differentiable**. This means that its first derivative can be calculated; a property that not all functions have. However, most well-behaved functions are differentiable in the majority of their domain.

Thanks to this linearisation trick, we can now approximate the function ![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)


(7) ![Rendered by QuickLaTeX.com \begin{equation*} f\left(x\right) \approx f\left(\hat{x}_0\right) + f'\left(\hat{x}_0\right) \left( x - \hat{x}_0 \right)\end{equation*}](../../assets/1a910539f4579e85.png)


It should be noticed that both ![Rendered by QuickLaTeX.com f\left(\hat{x}_0\right)](../../assets/ce16e66068188dce.png)

![Rendered by QuickLaTeX.com f'\left(\hat{x}_0\right)](../../assets/9fc8b9ef101ff6f0.png)

*numbers*, and they correspond to the value of the model at ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)


We can now rearrange the terms in ([7](https://www.alanzucconi.com#id3122654239)) to better reveal its linear nature, in a form that we have already encountered:

(8) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align}f\left(x\right) \approx & f\left(\hat{x}_0\right) + f'\left(\hat{x}_0\right) \left( x - \hat{x}_0 \right) = \\& \underset{A}{\underbrace{ f'\left(\hat{x}_0\right) }}\, x + \underset{B}{\underbrace{ f\left(\hat{x}_0\right) - f'\left(\hat{x}_0\right) \, \hat{x}_0}}\end{align}\end{equation*}](../../assets/c94cbc63f20cd76b.png)


We can now replace ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)


(9) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align}\hat{x}_1^{-} = & \boxed{A} &\hat{x}_0 &+& \boxed{B} &= \\& \boxed{f'\left(\hat{x}_0\right)} &\hat{x}_0 &+& \boxed{f\left(\hat{x}_0\right) - f'\left(\hat{x}_0\right) \, \hat{x}_0}&\end{align}\end{equation*}](../../assets/7a3ac155ff9bf5cf.png)


and:

(10) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align}P_1^{-}= & \boxed{A^2} &P_0 &+Q &= \\& \boxed{f'\left(\hat{x}_0\right)^2} & P_0 &+Q &\end{align}\end{equation*}](../../assets/f142c2b8b8d1c624.png)


It is to be noted that in many derivations of the Extended Kalman Filter, you may find ![Rendered by QuickLaTeX.com \hat{x}_1^{-}](../../assets/2ba86f2f15608f42.png)

![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)


This derivation is really needed in the calculation of ![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)


When the function is highly non-linear, even EFK can have issues adapting to its temperamental behaviour. In that case, another variant called the [Unscented Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter#Unscented_Kalman_filter) (UKF) finds ample application.

## Numerical Estimation

The Extended Kalman Filters relies on the strong assumption that we can model the evolution of the system as a differentiable function. While a system might be evolving in such a way, it does not mean we are immediately able to derive the necessary equations.

This is why Extended Kalman Filters often rely on numerical estimation of the first derivative, rather than using its actual mathematical formulation. This makes such filters able to better handle rapid changes in behaviours, at the cost of a less precise measure overall.

The only thing needed in this case is to simply use the previous two best estimates (![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{x}_{-1}](../../assets/ea2686c2971c5a00.png)

[5](https://www.alanzucconi.com#id4249984988)).

The interactive chart below shows the evolution of two Extended Kalman Filters. The one on top uses the actual first derivative, while the one on the bottom approximates it numerically.

## Further Extensions…

### Feedback Loop

The current derivation is for a Kalman filter that is “passive”, in the sense that it does not interact with the system it measures. This is often not the case: in the example of a thermostat, for instance, the observations might be used to determine whether or not to turn heating on or off.

More advanced versions of the Kalman filter also include a **control factor** (![Rendered by QuickLaTeX.com u_n](../../assets/353a62ecf6b249ba.png)


(11) ![Rendered by QuickLaTeX.com \begin{equation*} x_1 = A~x_0 + B + C ~ u_1 + v\end{equation*}](../../assets/238504955c610035.png)


In the equation above, ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

**control-input model**, and modulates the contribution of the control factor (![Rendered by QuickLaTeX.com u_1](../../assets/ba92b276b258a109.png)


For instance, if the Kalman filter detects that temperature is too low, it could trigger a thermostat to turn the heating on. In that case, we could set ![Rendered by QuickLaTeX.com u_1=1](../../assets/660f191ebc97fd0b.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)


This allows for a more complex, yet accurate prediction of the system. As seen before, the control-input model is expected to be linear, or at least differentiable if we are using an Extended Kalman Filter.

### Observation Model

For the entire duration of this series we have simply assumed that the sensor would return readings in the same scale of the original process. This is not necessarily the case, especially for electronics sensors which might register a temperature as a current drop across a resistor, rather than degrees.

Traditionally, the “complete” formulation of the Kalman filter includes a factor ![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)

**observation model**. In a nutshell, it allows to remap values sampled from the sensor in the same scale and unit of the process property under examination:

(12) ![Rendered by QuickLaTeX.com \begin{equation*} z_1 = H ~ x_1 + w_1\end{equation*}](../../assets/00e0370edd99dcb2.png)


### Extending Into Multiple Dimensions

Right now we have presented a derivation of the Kalman filter that works on *scalar* quantities, meaning that only works on a single numbers. In reality, however, there might be properties that we want to estimate that are multi-dimensional. In one of its more general formulations, Kalman filters are actually presented in matrix form. Under this new framework, the positions (![Rendered by QuickLaTeX.com x_n](../../assets/e37a9e1505935ab0.png)

![Rendered by QuickLaTeX.com z_n](../../assets/a2574dc1f31e9f42.png)

![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)


The position of a building, for instance, is likely going to include at least two independent variables: latitude and longitude. One could easily use two separate Kalman filter for both properties, but that is very wasteful because it completely ignores how the two coordinates are connected.

#### State Prediction

Let’s see a concrete example, imaging a multi-dimensional filter which measures two quantities at the same time, such as *latitude* and *longitude*:

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\boldsymbol{x_n} & = \begin{bmatrix} x_n^1 \\ x_n^2 \end{bmatrix} \\\boldsymbol{z_n} & = \begin{bmatrix} z_n^1 \\ z_n^2 \end{bmatrix} \\\boldsymbol{\hat{x}_n} & = \begin{bmatrix} \hat{x}_n^1 \\ \hat{x}_n^2 \end{bmatrix}\end{align}\end{equation}](../../assets/e4588096b4761933.png)


To avoid confusion, the matrix (or vector) version of a variable is indicated in ** bold italic** (in accordance with the ISO standard).

During the past few articles we have seen how the process evolves over time ([1](https://www.alanzucconi.com#id1832530401)) as a linear combination of the previous state (or as its function, in the case of the Extended Kalman Filter):

(13) ![Rendered by QuickLaTeX.com \begin{equation*}x_1 = A~x_0 + B + v\end{equation*}](../../assets/20b0f0012abe20c4.png)


This can be rethought in terms of matrices as:

(14) ![Rendered by QuickLaTeX.com \begin{equation*} \boldsymbol{x_1} = \boldsymbol{A}~\boldsymbol{x_0} + \boldsymbol{B} + \boldsymbol{v}\end{equation*}](../../assets/281ec0b0a62fee8f.png)


The two expressions seem pretty much the same, but they are fundamentally different. Under this new framework, ![Rendered by QuickLaTeX.com \boldsymbol{A}](../../assets/01dfe87088ad74c4.png)

![Rendered by QuickLaTeX.com \boldsymbol{B}](../../assets/afd645b368a15159.png)

![Rendered by QuickLaTeX.com \boldsymbol{x_1}](../../assets/a4cdff9304913870.png)


In the case of a static object which is not expected to move, ![Rendered by QuickLaTeX.com \boldsymbol{A}](../../assets/01dfe87088ad74c4.png)

![Rendered by QuickLaTeX.com \mathbb{I}](../../assets/879c66bc1c522fb3.png)

![Rendered by QuickLaTeX.com \boldsymbol{B}](../../assets/afd645b368a15159.png)


(15) ![Rendered by QuickLaTeX.com \begin{equation*} \boldsymbol{x_1} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} ~\boldsymbol{x_0} + \begin{bmatrix} 0 \\ 0 \end{bmatrix} + \boldsymbol{v} \end{equation*}](../../assets/8c723589441b1f5d.png)


#### Extended Kalman Filter

Equation ([15](https://www.alanzucconi.com#id605668997)) expresses the state prediction step in its matrix form. However we have seen how the Extended Kalman Filter supports not just linear combinations, but any differentiable function.

Things get a bit more complex when we have to calculate the first derivative of such function ![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)

**Jacobian**. This is a matrix which elements are the partial derivative of a given function, calculated with respect to each dimension of the system:

(18) ![Rendered by QuickLaTeX.com \begin{equation*} \boldsymbol{F}\overset{\triangle}{=}\frac{\partial f }{\partial x}\end{equation*}](../../assets/fe4016ada94afcb0.png)


For instance:

(19) ![Rendered by QuickLaTeX.com \begin{equation*} \boldsymbol{F} = \begin{bmatrix} \frac{\partial f }{\partial x_n^1} \\ \frac{\partial f }{\partial x_n^2} \end{bmatrix} \end{equation*}](../../assets/c495b1238f2d2880.png)


#### State Update

Due to the fact that matrix multiplication is non-commutative, we should be very careful in how terms are rearranged. For instance:

(20) ![Rendered by QuickLaTeX.com \begin{equation*} \boldsymbol{\hat{x}_1} = \left(\mathbb{I}-\boldsymbol{k_1}\right) \, \boldsymbol{\hat{x}_1^{-}} + \boldsymbol{k_1} \, \boldsymbol{z_1}\end{equation*}](../../assets/e6f084c63d11a8f4.png)


has to be expressed in this way to ensure that the matrix multiplication yields the correct result:

(21) ![Rendered by QuickLaTeX.com \begin{equation*} \underset{2 \times 1}{\boxed{\boldsymbol{\hat{x}_1} }} =\underset{2 \times 1}{\boxed{\underset{2 \times 1}{\boxed{\underset{2 \times 2}{\boxed{ \left(\underset{2 \times 2}{\boxed{\mathbb{I}}}-\underset{2 \times 2}{\boxed{\boldsymbol{k_1}}}\right) }} \,\underset{2 \times 1}{\boxed{\boldsymbol{\hat{x}_1^{-}}}}}}+\underset{2 \times 1}{\boxed{\underset{2 \times 2}{\boxed{\boldsymbol{k_1}}} \,\underset{2 \times 1}{\boxed{\boldsymbol{z_1}}}}}}}\end{equation*}](../../assets/ded54e13d33721e3.png)


#### Kalman Gain

Even the expression for Kalman gain requires some attention. In fact, scalar division needs to be replace with its matrix counterpart: multiplication by the inverse.

(22) ![Rendered by QuickLaTeX.com \begin{equation*} \boldsymbol{k_1} = \boldsymbol{P_1^{-}} {\left( {\boldsymbol{P_0}+\boldsymbol{R}} \right)}^{-1}\end{equation*}](../../assets/c55cf21be315a364.png)


Another tricky aspect is that other scalar properties, such as the variance ![Rendered by QuickLaTeX.com P_n](../../assets/d5c9c88137f65500.png)

**covariance matrices**.

## Conclusion

We have finally concluded the theoretical overview of the Kalman Filter, along with some of its many variants and evolutions.

**Initialisation**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_0 & & \textup{initial state} && \underset{d \times 1}{\boldsymbol{\hat{x}_0}} \\P_0 &= 1& \textup{initial variance} && \underset{d \times d}{\boldsymbol{P_0}} =\mathbb{I} \\Q & & \textup{process noise variance} && \underset{d \times d}{\boldsymbol{Q}} \\R & & \textup{measurement noise variance} && \underset{d \times d}{\boldsymbol{R}} \\f & & \textup{function} && f \\f' & & \textup{first derivative} && \underset{d \times 1}{\boldsymbol{F}}=\frac{\partial f }{\partial x}\end{align}\end{equation}](../../assets/066120b2f95b9b38.png)


**Prediction step**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}& \textup{Scalar} & & & & \textup{Matrix} \\\hat{x}_1^{-} & = f\left(\hat{x}_0\right) & \textup{state prediction} & & \boldsymbol{\hat{x}_1^{-}} & = f\left(\boldsymbol{\hat{x}_0} \right) \\P_1^{-} & = f'\left(P_0\right)^2 +Q & \textup{variance prediction} & & \boldsymbol{P_1^{-}} & = \boldsymbol{F} ~ \boldsymbol{P_0} ~ \boldsymbol{F^T} + \boldsymbol{Q} \\\end{align}\end{equation}](../../assets/329991705df262b3.png)


**Correction step**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}& \textup{Scalar} & & & & \textup{Matrix} \\k_1 & = \frac{P_1^{-}}{P_0+R} & \textup{Kalman gain} & & \boldsymbol{k_1} & = \boldsymbol{P_1^{-}} {\left( {\boldsymbol{P_0}+\boldsymbol{R}} \right)}^{-1}\\\hat{x}_1 &= \hat{x}_1^{-} \left(1-k_1\right) + z_1 \, k_1 & \textup{state update} & & \boldsymbol{\hat{x}_1} &= \left(\mathbb{I}-\boldsymbol{k_1}\right) \, \boldsymbol{\hat{x}_1^{-}} + \boldsymbol{k_1} \, \boldsymbol{z_1} \\P_1 & = \left(1-k_1\right) P_1^{-} & \textup{variance update} & & \boldsymbol{P_1} & = \left(\mathbb{I}-\boldsymbol{k_1}\right) \boldsymbol{P_1^{-}}\end{align}\end{equation}](../../assets/b0825cf5a80b4c29.png)


## What’s Next…

You can read all the tutorials in this online course here:

- Part 1.
[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795) - Part 2.
[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain - Part 3.
[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models **Part 4:**[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models- Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

The next and final part of this series will focus on a simple, efficient and effective implementation of the Kalman filter in C#.

### Further Readings

- “
[Kalman Filter For Dummies](http://bilgin.esme.org/BitsAndBytes/KalmanFilterforDummies)” by[Bilgin Esme](https://twitter.com/RubberBoom) - “
[Kalman](http://greg.czerniak.info/guides/kalman1/)” by Greg Czerniak - “
[Understanding the Basis of the Kalman Filter Via a Simple and Intuitive Derivation](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf)” by[Ramsey Faragher](https://twitter.com/RamseyFaragher) - “
[Extended Kalman Filter](https://zlthinker.github.io/extended_kalman_filter)” by Lei Zhou - “
[Kalman filter](http://david.wf/kalmanfilter/)” by[David Khudaverdyan](https://twitter.com/khdavid) - “
[Kalman Filter Interview](https://towardsdatascience.com/kalman-filter-interview-bdc39f3e6cf3)” by[Harveen Singh](https://twitter.com/harveenj) - “
[Kalman Filter Simulation](https://www.cs.utexas.edu/~teammco/misc/kalman_filter/)” by Richard Teammco - “
[Extended Kalman Filter: Why do we need an Extended Version?](https://towardsdatascience.com/extended-kalman-filter-43e52b16757d)” by[Harveen Singh Chadha](https://medium.com/@harveenchadha) - “
[The Unscented Kalman Filter: Anything EKF can do I can do it better!](https://towardsdatascience.com/the-unscented-kalman-filter-anything-ekf-can-do-i-can-do-it-better-ce7c773cf88d)” by[Harveen Singh Chadha](https://medium.com/@harveenchadha) - “
[A New Approach to Linear Filtering and Prediction Problems](http://www.cs.unc.edu/~welch/kalman/media/pdf/Kalman1960.pdf)” by Rudolf E. Kálmán

## Leave a Reply Cancel reply