---
title: Modelling Kalman Filters - Alan Zucconi
url: https://www.alanzucconi.com/2022/07/24/kalman-filter-3/
author: Alan Zucconi
published: '2022-07-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the third part of the series dedicated to one of the most popular sensor de-noising technique: Kalman filters. This article will explain how to model processes to improve the filter performance.

You can read all the tutorials in this online course here:

- Part 1.
[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795) - Part 2.
[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain **Part 3.**[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models- Part 4:
[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models - Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

## Introduction

Before we can extend the Kalman filter towards its full potential, it is important to do a quick recap of what was explored in the previous two articles of this series.

Kalman filters are a family of statistical techniques which find ample application in engineering to solve the problem of **sensor de-noising** and **sensor fusion**. All sensors, in fact, are affected by errors, delays and inaccuracies which can have a significant impact on the system in which they are integrated.

Typical examples of system in which Kalman filters find ample applications are refining the location of an object (such as a train using GPS data) or controlling a thermostat (using readings from a thermometer). In the field of games, they are really useful when it comes to read input data from controllers, accelerometers, gyroscope and webcams.

The theory of a Kalman filters sees the world through three different lenses:

- The
**process**: represents the system that we are trying to measure. The*exact*value of the system at time

is

. This value is never directly accessible, hence it must be sampled using a sensor; - The
**measures**: they represents the raw data coming from a sensor. The reading of the system at time

in

. This reading is assumed to be affected by an additive noise factor,

, which follows a normal distribution with variance

; - The
**estimates**: they represents the guesses of the Kalman filter. The “best guess” for the value of the system (

) at time

is

. As a consequence of assuming that the various measurements are following a normal distribution, even the various

are normally distributed.

The diagram below summarises all of those elements. For simplicity, we will mostly refer to two generic time instances ![Rendered by QuickLaTeX.com n=0](../../assets/552a975d42f15a70.png)

![Rendered by QuickLaTeX.com n=1](../../assets/985496c603983de4.png)


![](../../assets/abd53923a9a3c00d.png)


![](../../assets/abd53923a9a3c00d.png)

The Kalman filters estimates the “true” value of the system by combining (*fusing*) together the best estimate of its previous value (![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

**state estimate** (sometimes also referred to as the **estimated position**, when the filter is used for locations).

In one of its more vanilla implementations, this fusion is done by linearly interpolating ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

**Kalman gain**.

(1) ![Rendered by QuickLaTeX.com \begin{equation*}\hat{x}_1 = \hat{x}_0 \left(1-k_1\right) + z_1 \, k_1\end{equation*}](../../assets/586538ddcfbc5ca0.png)


What the Kalman filter does is converging towards the *optimal* gain value: the value which results in the combination of the previous state estimate (![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com x_1](../../assets/b0ef10e062b6a0ae.png)


And it does so through a statistical approach. Because both quantities can be represented as being sampled from two normal distributions (![Rendered by QuickLaTeX.com \hat{X}_0 \sim \mathcal{N}(\hat{x}_0, P_0)](../../assets/a2f545f6c116aad9.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com Z_1 \sim \mathcal{N}(z_1, R)](../../assets/66bf99c2508a07b3.png)

![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} \mathcal{N}(\hat{x}_1, P_1)=\mathcal{N}(\hat{x}_0, P_0) \times \mathcal{N}(z_1, R)\end{equation*}](../../assets/f3f8d742c0ad70a8.png)


In the previous article we made the example of a Kalman filter applied to a thermometer. In that scenario, we encountered the following quantities:


: the *real temperature*of the room at time

;


: the *measured temperature*, which is the data collected from the sensor at time

;

This is a noisy estimate for the values of

;

: the measurement *noise*, which indicates how reliable the sensor is;

(3) ![Rendered by QuickLaTeX.com \begin{equation*} z_1 = x_1 + w_1\end{equation*}](../../assets/cd1713ff7118ec8e.png)


(4) ![Rendered by QuickLaTeX.com \begin{equation*}w_1 \sim \mathcal{N}(0,R)\end{equation*}](../../assets/3f15ce279808219d.png)



: the *estimated temperature*of the room at time

.

This is an inaccurate guess for

, and it is calculated by taking into account

and

;

: the *Kalman gain*, which represents the best coefficient to merge the estimated temperature and the sensor measurement;

(5) ![Rendered by QuickLaTeX.com \begin{equation*} \hat{x}_1 = \hat{x}_0 \left(1-k_1\right) + z_1 \, k_1\end{equation*}](../../assets/acaa7989f6abaa9b.png)


(6) ![Rendered by QuickLaTeX.com \begin{equation*} k_1 = \frac{P_0}{P_0+R} \end{equation*}](../../assets/f47fcbc7ffbac039.png)



: the confidence of the estimated position

.

(7) ![Rendered by QuickLaTeX.com \begin{equation*} P_1 &= \left(1-k_1\right) P_0\end{equation*}](../../assets/fef8f17c520a834e.png)


### Limitations

At this stage is important to remember that this series of tutorial is building a “fully functional” Kalman filter *incrementally*. The version presented in the diagram above works, but is still fairly simple compared to the more general versions that one would typically find in the scientific literature.

And yet, this is already enough to implement a fully working Kalman filter. The char below shows how the filter (![Rendered by QuickLaTeX.com \hat{x}_n](../../assets/07245b120be7d7e9.png)

![Rendered by QuickLaTeX.com x_n](../../assets/e37a9e1505935ab0.png)


The yellow line indicates the noisy measurements (![Rendered by QuickLaTeX.com z_n](../../assets/a2574dc1f31e9f42.png)

![Rendered by QuickLaTeX.com P_n](../../assets/d5c9c88137f65500.png)

![Rendered by QuickLaTeX.com \sqrt{P}](../../assets/853971bf771ee3b5.png)


It is easy to see, however, that the filter’s performance is not that great. This is the results of an over-simplistic approach in its current derivation. In fact, there are two important aspects that so far have been ignored:

**The process is believed to be static.**The current iteration of the Kalman filter presented assumes that the true state of the system is typically not subjected to any change over time. For instance, the location of a building is not supposed to change over time. While this is true in certain applications, it not true in general;**The process update is assumed to be noiseless.**The Kalman filters believes that the original process itself is perfectly noiseless and fully deterministic. Hence, it’s evolution could be technically derived just from its original state. In the current derivation, in fact, the only source or noise the Kalman filter acknowledges is the one coming from the sensor.

The performance of the filters gets progressively worse the more the signal diverges from the initial “belief” of how it should evolve. The chart below shows the same filter responding to an even changing signal:

There are two important problems that can be observed:

**The delayed response.**The real temperature changes too fast for the filter to react in a reasonable time frame. This is a consequence of assuming a static model: the filter sees a change, but it attributes it to noise, since it believes the temperature should not change. It takes several consistent measurements to steer the prediction onto a new value; this is a known as**transient lag**;**The filter over-confidence.**The second issue is that the response of the filter gets progressively smaller. This is an interesting issue that arises from the fact that our model was assumed*perfect.*The filter is unaware of its underperformance, which can also be seen by how the variance

gets smaller.

All of these points will be addressed in the rest of this article, integrating a probabilistic model of the system inside the Kalman filter.

## Improving the Kalman Filter

The previous article in this series focused on the derivation of the Kalman gain, and for the sake of simplicity it completely ignore one very important aspect: the model. Every modern Kalman filter, in fact, also comes with an internal model of how the system is expected to evolve. The reason why this step was simply ignored in the previous section is simple: adding a specific model “pollutes” the equations of the Kalman filter with terms that belongs to the system, not to the filter itself.

However, creating a Kalman filter without an explicit model does not make it agnostic to the system. Quite the opposite, not including a mathematical model has the implicit effect of assuming that the system is not subjected to any change; which is a model in itself! There are many scenarios in which this is actually desirable: the position of a building, for instance, is not expected to change over time. In the toy example previously used (a sensor measuring the temperature of a room), this was encoded in the following equation:

(8) ![Rendered by QuickLaTeX.com \begin{equation*} x_{1} = x_{0}\end{equation*}](../../assets/1edd1976a526d02b.png)


which indeed indicates that there is no expected change from one time frame to the next.

#### Process Noise

The filter derived in the previous part of this course suffered from a severe issue. Not only it believes the temperature is static: it also believes the system is unaffected by noise or uncertainty of any kind. From an engineering perspective, this is simply impossible as any process is likely poised by errors. We can take this into account by modelling even the evolution of the room temperature as a **random process**. This means introducing an error term ![Rendered by QuickLaTeX.com v](../../assets/1bf6fd37becd9c3d.png)

**process noise**) which, in the case of a Kalman filter, is expected to follow a **Gaussian distribution**:

(9) ![Rendered by QuickLaTeX.com \begin{equation*} x_1 = x_0 + v\end{equation*}](../../assets/a868fd6207991048.png)


(10) ![Rendered by QuickLaTeX.com \begin{equation*}v \sim \mathcal{N}(0,Q)\end{equation*}](../../assets/db5533e469a4ffab.png)


The Kalman filter works under the assumption that ![Rendered by QuickLaTeX.com v](../../assets/1bf6fd37becd9c3d.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

**variance** of the process noise. In the original toy example of a train moving along a track, the process noise would loosely relate to how reliably the train can move.

![](../../assets/5e370c739de45e8b.png)


![](../../assets/5e370c739de45e8b.png)

Equation ([9](https://www.alanzucconi.com#id3154604484)) has an intuitive explanation. If the temperature is ![Rendered by QuickLaTeX.com x_0](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e6e1c3611728e9db0e52bb6485e06068_l3.png)

![Rendered by QuickLaTeX.com x_0](../../assets/0c97e55ba3e6a7a0.png)

![Rendered by QuickLaTeX.com x_1](../../assets/b0ef10e062b6a0ae.png)

![Rendered by QuickLaTeX.com \mathcal{N}(x_0,Q)](../../assets/88a8f23dcec4c363.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)


#### Prediction Step

To better understand how to fix our filter, we first need to understand what’s wrong. Let’s recall the definition of ![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)


(11) ![Rendered by QuickLaTeX.com \begin{equation*}P_1 &= \left(1-k_1\right) P_0\end{equation*}](../../assets/a8d8654e7ae59f14.png)


Since ![Rendered by QuickLaTeX.com k_1](../../assets/d46968d98f9dd5b5.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)


This breaks when the temperature is subjected to variations. An increase in the error of the filter should increase the value of ![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)


As anticipated in the previous part of this tutorial, the Kalman filter works in two steps: **prediction** and **correction**. The prediction step answers this question: given our current understand of the world (represented by ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

[9](https://www.alanzucconi.com#id3154604484)), we still expect no changes (on average) from ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)


(12) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}P_1^{-} & \overset{\triangle}{=} P_0 +Q & &\\k_1 & = \frac{P_0 +Q}{P_0+R} & =& \frac{P_1^{-}}{P_0+R} \\P_1 & = \left(1-k_1\right) \left(P_0 +Q\right) &= &\left(1-k_1\right) P_1^{-}\end{align}\end{equation*}](../../assets/de585ce6962986fd.png)


The quantity ![Rendered by QuickLaTeX.com P_0 + Q](../../assets/a5171ce58e749303.png)

![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

**a priori variance**. The term *a priori* indicates that ![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

*before* taking into consideration any sensor data. Once the measurement ![Rendered by QuickLaTeX.com z_1](../../assets/45bf12742d523c83.png)

![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

**a posteriori variance** ![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)


This change alone is not fixing all of our issues. But the resulting filter, above, is now responding correctly and its variance doesn’t vanish, as seen in the chart above.

Unfortunately, there is a trade-off between *responsiveness* and *noise reduction*. A filter that is very responsive will also be more susceptible to noise; a filter that can reduce most of the noise will take longer to respond to changes.

#### Model Prediction

Despite the introduction of the a priori variance ![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)


If you do not know anything about the dynamic of the system, this is your best guess and the only thing you can do is tweaking the values of ![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

[9](https://www.alanzucconi.com#id3154604484)) can be rewritten to include an arbitrary function ![Rendered by QuickLaTeX.com f\left(\cdot\right)](../../assets/8f0185935e4d91de.png)

![Rendered by QuickLaTeX.com x_0](../../assets/0c97e55ba3e6a7a0.png)

![Rendered by QuickLaTeX.com x_1](../../assets/b0ef10e062b6a0ae.png)


(13) ![Rendered by QuickLaTeX.com \begin{equation*} x_1 = f\left(x_0\right) + v\end{equation*}](../../assets/77419d1f74a4e6db.png)


The equations that are derived from this formulation lead to the so-called [extended Kalman filter](https://en.wikipedia.org/wiki/Extended_Kalman_filter) (or EKF), which works for functions that are not necessarily *linear*. We will explore how it works in the fourth instalment of this tutorial: [The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146).

In order to simplify our derivation, we need to restrict our problem by imposing a constraint of linearity on ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)


(14) ![Rendered by QuickLaTeX.com \begin{equation*} x_1 = A~x_0 + B + v\end{equation*}](../../assets/e1d52a4221ddd10b.png)


One can be tempted to simply state that:

(15) ![Rendered by QuickLaTeX.com \begin{equation*} \hat{x}_1 = A~\hat{x}_0 + B + v\end{equation*}](../../assets/ddb19c24888b2458.png)


but that would not be entirely correct. This is because what we have here is a probabilistic model. And so, the best way to extend the prediction step to include the *a priori* prediction for the evolution of ![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

**expected value**:

(16) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}\hat{x}_1^{-} &\overset{\triangle}{=} \mathrm{E} \left[\hat{x}_1\right] &=\\& = \mathrm{E} \left[A~\hat{x}_0 + B + v\right] &=\\& = \mathrm{E} \left[A~\hat{x}_0\right] + \mathrm{E} \left[B\right] + \mathrm{E} \left[v\right] &=\\& = A ~\mathrm{E} \left[\hat{x}_0\right] + B + 0 &=\\& = A ~\hat{x}_0 + B\end{align}\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b0c51e98e8e0bf128e63e264d8bf84e5_l3.png)


This new quantity, ![Rendered by QuickLaTeX.com \hat{x}_1^{-}](../../assets/2ba86f2f15608f42.png)

![Rendered by QuickLaTeX.com \hat{x}_0](../../assets/c8d46a0477b832ee.png)

** a priori state estimate**, as it happens before (

*a priori*) the measurement.

![](../../assets/6e7082cc02b7d663.png)


![](../../assets/6e7082cc02b7d663.png)

To complete the derivation, we also need to update our a priori prediction for ![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

![Rendered by QuickLaTeX.com \hat{x}_1](../../assets/e64a7b3302cfed69.png)


(17) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}P_1^{-} &\overset{\triangle}{=} \mathrm{Var} \left[ \hat{x}_1^{-}\right] &=\\& = \mathrm{Var} \left[ A~\hat{x}_0 + B + v \right] &= \\& = \mathrm{Var} \left[ A~\hat{x}_0\right] + \mathrm{Var} \left[B\right] + \mathrm{Var} \left[v \right] &= \\& = \mathrm{Var} \left[ A~\hat{x}_0 \right] + 0 + Q&= \\& = A^2 ~ \mathrm{Var} \left[\hat{x}_0 \right] + Q&= \\& = A^2 ~ P_0 + Q\end{align}\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-421ee1eca0e74f972b6a94b305663bde_l3.png)


Adding a constant to a random variable does not change its variance, so ![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)


(18) ![Rendered by QuickLaTeX.com \begin{equation*}$\mathrm{Var} \left[ A~X \right] = A^2 ~ \mathrm{Var} \left[X\right]$\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-21eb2d3207b2c0805c4f4c361012387c_l3.png)


In the scientific literature, ![Rendered by QuickLaTeX.com P_1^{-}](../../assets/30598acd47a4de6c.png)

![Rendered by QuickLaTeX.com A~ P_0 ~ A + Q](../../assets/99568e2a7853a8a6.png)

![Rendered by QuickLaTeX.com A^2 ~ P_0 + Q](../../assets/547303229c949423.png)


So, to recap:

(19) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}\hat{x}_1^{-} & = A~\hat{x}_0 + B \\P_1^{-} & = A^2~P_0 +Q\end{align}\end{equation*}](../../assets/6b209b58e345be1f.png)


This leads to a more precise version of the Kalman filter that is able to take into account the evolution of the system. You can try this yourself using the interactive chart below:

Compared to the original one, this time the filter is able to correctly re-adjust to the signal change. Setting ![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)


It is important to remember that the version of the Kalman filter that has been derived so far is only able to integrate linear models. In a nutshell, this means that our filters are optimised to work with signals that are essentially straight lines. This is a strong limitations which will be revised in the following article.

## Conclusion

In this article we completed the derivation of the Kalman filter, a popular statistical technique used for sensor de-noising and sensor fusion. Below you can see a diagram showing the most complex model build:

![](../../assets/6e7082cc02b7d663.png)


![](../../assets/6e7082cc02b7d663.png)

This includes a prediction of how the system is going to evolve over time, as long as a correction step which integrates readings from a sensor to reach to a better estimate.

You can play with a Kalman filter yourself using the interactive chart below:

hghghg

**Initialisation**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_0 & & \textup{initial state} \\P_0 &= 1& \textup{initial variance} \\Q & & \textup{process noise variance} \\R & & \textup{measurement noise variance} \\A & & \textup{model coefficient} \\B & & \textup{model offset}\end{align}\end{equation}](../../assets/9b57dc8fea68ec60.png)


**Prediction step**How we think the system should evolve, solely based on its model.

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_1^{-} & = A~\hat{x}_0 + B & \textup{state prediction} \\P_1^{-} & = A^2 ~ P_0 +Q & \textup{variance prediction} \\\end{align}\end{equation}](../../assets/51830ca4ab45a707.png)


**Correction step**The most likely estimation of the system state, integrating the sensor data.

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}k_1 & = \frac{P_1^{-}}{P_0+R} & \textup{Kalman gain} \\\hat{x}_1 &= \hat{x}_1^{-} \left(1-k_1\right) + z_1 \, k_1 & \textup{state update} \\P_1 & = \left(1-k_1\right) P_1^{-} & \textup{variance update}\end{align}\end{equation}](../../assets/daa81b3ac01e3b2a.png)


**Iteration**

![Rendered by QuickLaTeX.com \begin{equation*}\begin{align*}\hat{x}_0 & \leftarrow \hat{x}_1 \\P_0 & \leftarrow P_1\end{align}\end{equation}](../../assets/c0ddcb7c6ac37df3.png)


## What’s Next…

You can read all the tutorials in this online course here:

- Part 1.
[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795) - Part 2.
[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain **Part 3.**[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models- Part 4:
[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models - Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

The next part of this series will extend the current derivation of the Kalman filter to include non-linear models.

### Further Readings

- “
[Kalman Filter For Dummies](http://bilgin.esme.org/BitsAndBytes/KalmanFilterforDummies)” by[Bilgin Esme](https://twitter.com/RubberBoom) - “
[Kalman](http://greg.czerniak.info/guides/kalman1/)” by Greg Czerniak - “
[Understanding the Basis of the Kalman Filter Via a Simple and Intuitive Derivation](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf)” by[Ramsey Faragher](https://twitter.com/RamseyFaragher) - “
[Kalman filter](http://david.wf/kalmanfilter/)” by[David Khudaverdyan](https://twitter.com/khdavid) - “
[Kalman Filter Interview](https://towardsdatascience.com/kalman-filter-interview-bdc39f3e6cf3)” by[Harveen Singh](https://twitter.com/harveenj) - “
[Kalman Filter Simulation](https://www.cs.utexas.edu/~teammco/misc/kalman_filter/)” by Richard Teammco - “
[Extended Kalman Filter: Why do we need an Extended Version?](https://towardsdatascience.com/extended-kalman-filter-43e52b16757d)” by[Harveen Singh Chadha](https://medium.com/@harveenchadha) - “
[The Unscented Kalman Filter: Anything EKF can do I can do it better!](https://towardsdatascience.com/the-unscented-kalman-filter-anything-ekf-can-do-i-can-do-it-better-ce7c773cf88d)” by[Harveen Singh Chadha](https://medium.com/@harveenchadha) - “
[A New Approach to Linear Filtering and Prediction Problems](http://www.cs.unc.edu/~welch/kalman/media/pdf/Kalman1960.pdf)” by Rudolf E. Kálmán

## Leave a Reply Cancel reply