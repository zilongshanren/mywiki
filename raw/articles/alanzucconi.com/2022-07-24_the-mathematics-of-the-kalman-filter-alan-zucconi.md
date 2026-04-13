---
title: The Mathematics of the Kalman Filter - Alan Zucconi
url: https://www.alanzucconi.com/2022/07/24/kalman-gain/
author: Alan Zucconi
published: '2022-07-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the series dedicated to one of the most popular sensor de-noising technique: Kalman filters. This article will introduce the Mathematics of the Kalman Filter, with a special attention to a quantity that makes it all possible: the **Kalman gain**.

You can read all the articles in this online course here:

- Part 1.
[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795) **Part 2.**[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain- Part 3.
[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models - Part 4:
[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-linear Models - Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

## Introduction

**Kalman filtering** is a very powerful technique that finds application in a vast number of cases. One of its most popular use is** sensor de-noising**. Readings from sensors are typically affected by a certain degree of statistical uncertainty, which can lead to poor measurements. Under certain circumstances, Kalman filters have been proved to be *optimal*, meaning that no other algorithm will perform better.

This series of tutorials aims not just to explain the theory behind Kalman filters, but to create a fully functioning one! Many books present the equations in their “final” form; while that is a very time-efficient approach, it is not the one that we have chosen for this series.

If we want to understand not just *how* Kalman filters work, but *why* they work, it is important to do so step by step. And so, this series will build a Kalman filter “iteratively”, adding a new features at the end of every article.

By the end of this first article—which will focus on a quantity called **Kalman gain**—we will have a fully-functioning Kalman filter which is able to de-noise signals that are not expected to change very rapidly.

![](../../assets/35afbe4b6e820e61.png)


![](../../assets/35afbe4b6e820e61.png)

The following part will extend this limitation, but introducing a much more “complete” version of the Kalman filter which can handle signals that evolve linearly over time.

Finally, another article will introduce the so-called **Extended Kalman Filters**, which are designed to handle signals that can evolve in more complex ways.

## How it Works

When it comes to Kalman filters, most online tutorials start with the example of a moving train. The position of the train at a given time ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com x_n](../../assets/e37a9e1505935ab0.png)

*direct* access to the *true* position of the train, there would be no need for Kalman filters. The only way to access the position of the train is *indirectly*, by some sort of measurement; for instance, a GPS. If we had a truly perfect GPS, there would be no need for Kalman Filters. Unfortunately, no measurement apparatus is perfect, and no matter what we do, our measurement—let’s call it ![Rendered by QuickLaTeX.com z_n](../../assets/a2574dc1f31e9f42.png)


From a mathematical point of view, we can model this in the following diagram:

![](../../assets/39972d9f65e23a0f.png)


![](../../assets/39972d9f65e23a0f.png)

The train (generally referred to as the **process**) changes its position at every new time interval. This is often referred to as **process update**. In an ideal scenario, if a train travels at a constant speed of ![Rendered by QuickLaTeX.com v](../../assets/1bf6fd37becd9c3d.png)


(1) ![Rendered by QuickLaTeX.com \begin{equation*} x_{n+1} = x_{n} + v \, dn\end{equation*}](../../assets/d0a8f1c4e9af377c.png)


where ![Rendered by QuickLaTeX.com dn](../../assets/668cae056446532e.png)


Each measurement (![Rendered by QuickLaTeX.com z_n](../../assets/a2574dc1f31e9f42.png)

![Rendered by QuickLaTeX.com x_n](../../assets/e37a9e1505935ab0.png)

![Rendered by QuickLaTeX.com z_0](../../assets/abec12670a6297ad.png)

![Rendered by QuickLaTeX.com x_0](../../assets/0c97e55ba3e6a7a0.png)

**estimated position**, is indicated at ![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} \hat{x}_0 = z_0\end{equation*}](../../assets/7a1d56f006cefaff.png)


What a Kalman filter does, is updating and refining the estimated position (![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)

*fusing*) together the information about where the system believes the train should be (![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)

![Rendered by QuickLaTeX.com z_n](../../assets/a2574dc1f31e9f42.png)


![](../../assets/7e82ea4346c42475.png)


![](../../assets/7e82ea4346c42475.png)

Both quantities are inherently inaccurate, but combining them both can help refining the overall estimate. In this example we used two measures, but this can theoretically be expanded to include more readings from different sensors, all of which having different degrees of reliability. This is commonly known in the academic literature as [sensor fusion](https://en.wikipedia.org/wiki/Sensor_fusion).

The rest of this article will slowly expand on this simplistic interpretation of Kalman filtering, by progressively introducing more nuanced variants.

## Step 1: The Model

Each Kalman filter is tailored to the application it needs to be used for, and it does so by incorporating a **model** of the system. This model is a simplified mathematical description of how we expect the system to evolve. In the case of a train, the Kalman filter would need to integrate the *laws of motion* into its equations. This allows the filter to not just passively *reacts* to the train movement, but to *predict* its future position based on its current state. Equation ([1](https://www.alanzucconi.com#id3003347595)), for instance, is modelling the fact that the train position increases linearly with time.

It is important to understand two things about this:

- This is a
**belief**: all Kalman filters are built with some pre-existing knowledge of how the system should evolve. The idea that the train moves at a constant speed is a*belief*, which may or may not be entirely correct; - This is a
**model**: the Kalman filter does not expect (or require) ([1](https://www.alanzucconi.com#id3003347595)) to be valid at all times. That equation is a simplified*model*of how the system is expect to behave at a short time scale. As such, there is no requirement for this to be*exact*. The more precise the model can be, the better the system will react. But because Kalman filters are designed to be resilient to noise, errors or inaccuracies in the model are generally well tolerated, as their deviation from the “true” behaviour can simply be interpreted as an extra source of noise.

This leads to an algorithm that works in two separate steps:

**Time update**(or**prediction step**): based on the current state of the system, we predict its new state.

In the case of a train, this means predicting its*next position*based on its*previous position*and*previous velocity*.**Measurement update**(or**correction step**): the prediction generated in the step before is corrected using the data from a sensor.

In the case of a train, this means integrating the*predicted position*with the*measurement*from a GPS.

![](../../assets/49a5a7c7286d7dbd.png)


![](../../assets/49a5a7c7286d7dbd.png)

Under this framework, the expected position updated in the prediction step is called ** a priori state estimate** (

![Rendered by QuickLaTeX.com \hat{x}^{-}_n](../../assets/09ef714c07def65f.png)

*a priori*” means “

*before*“, as this is the predicted position where the train should

*before*the measurement is performed. Once a measure is available, the Kalman filter can integrate that information to refine its estimation, which gets called

**.**

*a posteriori*state estimate### A simpler toy example

Most online tutorials start with the example of a train moving forward along a track; and this tutorial was not an exception. Such a scenario is very easy to understand. However, when it comes to the actual Maths, following such a path actually leads to a more complex derivation. This is because each Kalman filter is tailored to the application it needs to be used for, and doing so requires to integrate the laws of motion into our equation. And doing so, “pollutes” the derivation of the Kalman filter by adding specific terms that are not part of the filter itself, but of the model the filter is trying to predict.

In this specific article, we will focus only on the correction step, which is the real heart of the Kalman filter; something that all filters belonging to Kalman family share. But for this to work, we need to pick a scenario in which the prediction step is virtually non-existent. This means measuring a quantity that is not expected to change over time. More realistically, a quantity that is not expected to change *too fast*. This leads us to consider a system which was already described in the second diagram of this article:

A good example is the temperature of a well-insulated room. Let’s assume that the *real* temperature at time ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com x_n](../../assets/e37a9e1505935ab0.png)

*believe* that the system evolves according to the following equation:

(3) ![Rendered by QuickLaTeX.com \begin{equation*} x_{n+1} = x_{n}\end{equation*}](../../assets/9cd3bb45550867b0.png)


This means that we expect the temperature of the room to remain constant, as the room itself is well insulated.

Also, to simplify the notation—yet without loss of generality—we will only consider the evolution of the Kalman filter from a generic time ![Rendered by QuickLaTeX.com n=0](../../assets/552a975d42f15a70.png)

![Rendered by QuickLaTeX.com n=1](../../assets/985496c603983de4.png)


![](../../assets/eed409e43a950037.png)


![](../../assets/eed409e43a950037.png)

This has no real implication, but it allows to simplify the notation getting rid of ![Rendered by QuickLaTeX.com n-1](../../assets/43204d5a42f66088.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n+1](../../assets/d60c306e19db7234.png)


## Step 2: The Measurement

If we could access the *real* temperature of the room (![Rendered by QuickLaTeX.com x_n](../../assets/e37a9e1505935ab0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

*directly* and with *absolute* precision. Instead, we are forced to rely on an *indirect*, *imprecise* measure, which introduces some uncertainty. What we read from a thermometer is not a value of the “real temperature”. It is (to make an old-fashioned example) how much mercury expands when subjected to a certain temperature. The expansion of mercury is a *proxy* for the temperature, which is the real quantity that we want to estimate.

Measuring the temperature of a room using a thermometer introduces a new type of uncertainty, as the sensor itself has a limited precision.

(4) ![Rendered by QuickLaTeX.com \begin{equation*} z_1 = x_1 + w_1\end{equation*}](../../assets/cd1713ff7118ec8e.png)


(5) ![Rendered by QuickLaTeX.com \begin{equation*}w_1 \sim \mathcal{N}(0,R)\end{equation*}](../../assets/3f15ce279808219d.png)


The quantity ![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com x_1](../../assets/b0ef10e062b6a0ae.png)

**Gaussian variable** ![Rendered by QuickLaTeX.com w_1](../../assets/2f34a509219963ab.png)

**measurement noise**.

![](../../assets/abd53923a9a3c00d.png)


![](../../assets/abd53923a9a3c00d.png)

The quantity ![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


### Visualising Noise and Uncertainty

Before we proceed, you should be familiar with the concept of Gaussian distribution. To get a better idea of the true meaning of ([4](https://www.alanzucconi.com#id979612561)) you can have a look at the interactive chart below. The blue curve shows the **probability density function** of ![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

**relative likelihood** of appearing.

If the sensor returns the value ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)


## Step 3. Estimated Position

The purpose of sensor de-noising is, at its core, finding a good guess for ![Rendered by QuickLaTeX.com x_1](../../assets/b0ef10e062b6a0ae.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

**estimated state** (or position, in our example) at time ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com \hat{x}_1=z_1](../../assets/89a1245fb4a2097f.png)

*raw* value means that you are comfortable integrating the maximum amount of noise possible into your application.

A more reasonable approach is to come up with a different equation for ![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)


There are infinitely many ways in which ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)


(6) ![Rendered by QuickLaTeX.com \begin{equation*} \hat{x}_1 \overset{\triangle}{=} \hat{x}_0 \left(1-k_1\right) + z_1 \, k_1\end{equation*}](../../assets/07af8c870970ba4b.png)


Equation ([6](https://www.alanzucconi.com#id2632081632)) interpolates between ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com k_1\in\left[0,1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-43f560705299e3cdde1c912f25f1aa68_l3.png)

![Rendered by QuickLaTeX.com k_1=1](../../assets/bdac54412c8e06cb.png)

![Rendered by QuickLaTeX.com \hat{x}_1=z_1](../../assets/89a1245fb4a2097f.png)

![Rendered by QuickLaTeX.com k_1=0.5](../../assets/75f779a9804f0017.png)

![Rendered by QuickLaTeX.com \hat{x}_1=\frac{\hat{x}_0+ z_1}{2}](../../assets/6837de4b51153c13.png)

![Rendered by QuickLaTeX.com k_1=0](../../assets/9e29eaeafc47f3cc.png)


What we have done here is called **linear interpolation**: a technique that all game developers should be very familiar with. In case you are interested to learn more about what it can do and how it can be used, [An Introduction to Linear Interpolation](https://www.alanzucconi.com/2021/01/24/linear-interpolation/) is a good starting point.

It is obvious at this point that, if we decide to mix ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

![Rendered by QuickLaTeX.com k](../../assets/1f6815ea9a6d4626.png)


You can obviously choose the value of ![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

*optimal* value. The term “optimal” means that, under the right conditions and providing certain assumptions are holding, it converges to the the value of ![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com x_1](../../assets/b0ef10e062b6a0ae.png)


## Step 4. Sensor Fusion

To understand how Kalman finds the optimal value for ![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

**probability density function** (or **pdf**), which indicates the values it can produce, and how likely they area.

In the case of the thermometer that is used in this example, we have assumed the pdf of its error to follows a Gaussian distribution. When the sensor reads a value of ![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

[4](https://www.alanzucconi.com#id979612561)). Incidentally, this means that if we assume the sensor noise to be normally distributed, we can also model the sensor reading itself (![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)


(11) ![Rendered by QuickLaTeX.com \begin{equation*} Z_1 \sim \mathcal{N}(z_1, R)\end{equation*}](../../assets/83aa0978626c2e50.png)


which means that the value returned by the sensor (![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)


What we are trying to do here is to model all parts of the system as normal distributions. This will allow us to borrow the much needed statistical tools which will help compensating for the presence of noise.

This was pretty much straightforward for (![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)

[6](https://www.alanzucconi.com#id2632081632)), ![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{x}_0=z_0](../../assets/37d0f14e93fb806a.png)

[2](https://www.alanzucconi.com#id1418879772)). In the following iteration, ![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{x}_0=z_0](../../assets/37d0f14e93fb806a.png)

![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)


Thanks to this inductive reasoning, even the estimated temperature (![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)


(12) ![Rendered by QuickLaTeX.com \begin{equation*} \hat{X}_0 \sim \mathcal{N}(\hat{x}_0, P_0)\end{equation*}](../../assets/4d0b61e74ec4f216.png)


Practically speaking, ![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)


### Joint Probability

We now have two different probability distributions, each one estimating the probability of finding how hot the room is. These distributions are not only associated with a **mean** (which is their best guess), but also with a variance that indicates how confident that guess is. Their **joint probability** is a new probability distribution which incorporates all of these pieces of information.

What Kalman does is finding the most likely estimation for the temperature of the room, calculating the joint probability of the two distributions, ![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)

![Rendered by QuickLaTeX.com \hat{X}_1](../../assets/cbf158ff6d792ab4.png)


If we assume ![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)


(13) ![Rendered by QuickLaTeX.com \begin{equation*}\hat{X}_1 \overset{\triangle}{=} \hat{X}_0 \times Z_1\end{equation*}](../../assets/b022c66cf1a3915c.png)


One of the things that make the derivation of the Kalman filter algorithm so clean and efficient is that the product of two Gaussian distributions is another Gaussian distribution:

(14) ![Rendered by QuickLaTeX.com \begin{equation*} \mathcal{N}\left(\mu_1, \sigma_1^2\right) \times\mathcal{N}\left(\mu_2, \sigma_2^2\right) =\mathcal{N}\left(\frac{\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2}{ \sigma_1^2+ \sigma_2^2},\frac{\sigma_1^2\sigma_2^2}{\sigma_1^2+\sigma_2^2}\right)\end{equation*}](../../assets/59c977b929fb22ac.png)


This means that the process can be repeated indefinitely, without increasing in complexity. And it is, ultimately, what allowed us to assume that even the estimated position (![Rendered by QuickLaTeX.com x_0](../../assets/0c97e55ba3e6a7a0.png)

[12](https://www.alanzucconi.com#id1376805543)).

We can use ([14](https://www.alanzucconi.com#id281287465)) to multiply together the probability distributions of ![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)


(15) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align}\hat{X}_1 & \overset{\triangle}{=} \hat{X}_0 \phantom{\left(\hat{x}_0, P_0\right)} \times Z_1 \phantom{\left(z_1, R\right)} &=\\&= \mathcal{N}\left(\hat{x}_0, P_0\right) \times\mathcal{N}\left(z_1, R\right) &=\\&=\mathcal{N}\Bigl(\underset{\hat{x}_1}{\underbrace{\frac{\hat{x}_0 R+ z_1 P_0}{P_0+R}}},\underset{P_1}{\underbrace{\frac{P_0 R}{P_0 + R}}}\Bigr) & \overset{\triangle}{=}\\&\overset{\triangle}{=}\mathcal{N}\left(\hat{x}_1, P_1\right)&\end{align}\end{equation*}](../../assets/ae5616d1fb7c86d4.png)


Before progressing, is important to understand what this means, in the context of our example. Both ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)

![Rendered by QuickLaTeX.com \hat{X}_1](../../assets/cbf158ff6d792ab4.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

[15](https://www.alanzucconi.com#id689576985)) also allows to derive the variance of ![Rendered by QuickLaTeX.com \hat{X}_1](../../assets/cbf158ff6d792ab4.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)


## Step 5. The Kalman Gain

If we look at the new definition that we have derived for ![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

[15](https://www.alanzucconi.com#id689576985)), it looks quite different from what originally proposed in ([6](https://www.alanzucconi.com#id2632081632)). In reality, they are indeed the same quantity, although just expressed in a different way. We can see this by rearranging ([15](https://www.alanzucconi.com#id689576985)) like this:

(16) ![Rendered by QuickLaTeX.com \begin{equation*}\hat{x}_1 = \frac{\hat{x}_0 R + z_1 P_0}{P_0+R} =\end{equation*}](../../assets/e407ac1fcc85c6ed.png)


![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}& = \phantom{\hat{x}_0}\frac{\hat{x}_0 R }{P_0+R} & + & \phantom{z_1} \frac{z_1 P_0}{P_0+R} =\\& = \hat{x}_0\underset{1-k_1}{\underbrace{\frac{ R}{P_0+R}}}& +& z_1\underset{k_1}{\underbrace{\frac{P_0}{P_0+R}}} = \\& = \hat{x}_0 \left(1-k_1 \right) & +& z_1 k_1\end{align}\end{equation}](../../assets/d3aac92cf06b9dc0.png)


There is a hidden beauty in this derivation, which arises from the fact that a probabilistic definition of the problem, based on two Gaussian distributions ![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

**Kalman gain**:

(17) ![Rendered by QuickLaTeX.com \begin{equation*}k_1 = \frac{P_0}{P_0+R}\end{equation*}](../../assets/09dcc83b17a56698.png)


Now we have all the pieces to calculate the temperature of the room ![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)


To recap:

(18) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}k_1 &= \frac{P_0}{P_0+R} & \textup{Kalman gain} \\\hat{x}_1 & = \hat{x}_0 \left(1-k_1\right) + z_1 \, k_1 & \textup{state update} \\P_1 &= \frac{P_0 R}{P_0 + R} & \textup{variance update}\end{align}\end{equation*}](../../assets/c9a8d7a4a0cbe122.png)


## Step 6. Iterate

This derivation for the Kalman filter has been shown between an initial time ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


Like any Mathematical model, the Kalman filter works under very strict assumptions. In this case, the evolution of the system has to be linear, the and measurement noise have to be Gaussian distributed. For this specific derivation, we have also assumed that the quantity we want to measure never changes.

### Visualising The Kalman Filter

Understanding what the Kalman filter *really* does can be quite challenging at first. The interactive chart below allows controlling the parameters of the random variables which represent the *sensor measurement* ![Rendered by QuickLaTeX.com Z_1](../../assets/cab10c383d4154aa.png)

*previous estimate* ![Rendered by QuickLaTeX.com \hat{X}_0](../../assets/47be08e274852060.png)

*updated estimate* ![Rendered by QuickLaTeX.com \hat{X}_1](../../assets/cbf158ff6d792ab4.png)


## Summary

This post introduced the mathematics of Kalman filter. This is a list of all the symbols and notations used:


: the *real temperature*of the room at time

;


: the *measured temperature*, which is the data collected from the sensor at time

;

This is a noisy estimate for the values of

;

: the measurement *noise*, which indicates how reliable the sensor is.

This is the variance of the sensor;


: the *estimated temperature*of the room at time

.

This is an inaccurate guess for

, and it is calculated by taking into account

and

;

: the *Kalman gain*, which represents the best coefficient to merge the estimated temperature and the sensor measurement;

: the confidence of the estimated position.

This is the variance of the estimated temperature.

To simplify the notations, we have focused on two generic time intervals referred to as ![Rendered by QuickLaTeX.com n=0](../../assets/552a975d42f15a70.png)

![Rendered by QuickLaTeX.com n=1](../../assets/985496c603983de4.png)


The next part of this series will extend the equations here presented, so that the filter can work even if the temperature changes.

### 📚 Recommended Books

## What’s Next…

You can read all the tutorials in this online course here:

- Part 1.
[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795) **Part 2.**[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain- Part 3.
[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models - Part 4:
[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models - Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

### Further Readings

- “
[Kalman Filter For Dummies](http://bilgin.esme.org/BitsAndBytes/KalmanFilterforDummies)” by[Bilgin Esme](https://twitter.com/RubberBoom) - “
[Kalman](http://greg.czerniak.info/guides/kalman1/)” by Greg Czerniak - “
[Understanding the Basis of the Kalman Filter Via a Simple and Intuitive Derivation](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf)” by[Ramsey Faragher](https://twitter.com/RamseyFaragher) - “
[Kalman filter](http://david.wf/kalmanfilter/)” by[David Khudaverdyan](https://twitter.com/khdavid) - “
[Kalman Filter Interview](https://towardsdatascience.com/kalman-filter-interview-bdc39f3e6cf3)” by[Harveen Singh](https://twitter.com/harveenj) - “
[Kalman Filter Simulation](https://www.cs.utexas.edu/~teammco/misc/kalman_filter/)” by Richard Teammco - “
[A New Approach to Linear Filtering and Prediction Problems](http://www.cs.unc.edu/~welch/kalman/media/pdf/Kalman1960.pdf)” by Rudolf E. Kálmán

## Leave a Reply Cancel reply