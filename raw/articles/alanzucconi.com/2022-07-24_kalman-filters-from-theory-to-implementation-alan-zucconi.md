---
title: 'Kalman Filters: From Theory to Implementation - Alan Zucconi'
url: https://www.alanzucconi.com/2022/07/24/kalman-filter-1/
author: Alan Zucconi
published: '2022-07-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This series of articles will introduce the **Kalman filter**, a powerful technique that is used to reduce the impact of noise in sensors. If you are working with Arduino, this tutorial will teach you how to reliably read data from your sensors. This is a tutorial that will be very helpful even if you are not working with hardware: game developers are often challenged by noise, especially when it comes to integrating data collected from gyroscopes and accelerometers. And even if you are not building a mobile game, you can use Kalman filters to increase the precision of your controllers.

This first post will focus on a brief introduction to the problem, while the other tutorials in this online will focus on the derivation and implementation of a Kalman filter.

You can read all the tutorials in this online course here:

**Part 1.**[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795)- Part 2.
[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain - Part 3.
[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models - Part 4:
[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models - Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

## Introduction

It is often said that no two snowflakes are alike. Whether this is really true or not, they all share a similar structure. Even though each one is unique, you can always tell you are looking at a snowflake. This means that snowflakes have an **inherent** **variability**, which makes them diverging from the “ideal” shape we have in mind. The same argument holds for most, if not all, natural objects. All leaves look similar, although each one is unique.

![](../../assets/d3d0582f41492f1a.jpg)

A similar concept can be extended—beyond objects—to *processes*. Measuring your weight, for instance, is one of such processes. Every time you weigh yourself, your mass has changed, so you should expect to read a different value on the scale. This type of variability is akin to the one exhibited by snowflakes and leaves, although it occurs over a temporal axis, as your weight changes over time. And on top of that, the scale you are using is not perfect, but its reading will likely be subjected to some flucuations.

Statistics tries to account for such variability, introducing the concept of **random process**. Both the processes that generates leaves and the one that determines your weight are indeed random processes. This happens because the actions of taking a new leaf and weighing yourself produce different results each time they are performed. If you repeat them over and over again, you will have a rough estimate of what the “average” leaf looks like, and how much you weight.

In the past examples, the term “random” might be slightly misleading. There is not necessarily any *randomness* involved; at least not in the traditional sense. Your weight, for instance, fluctuates because matter is constantly added and removed in a rather determinist fashion. The problem is that we don’t know at which point in time you will be weighing yourself: this is where the randomness comes in. The queue in a supermarket behaves in a deterministic and easy to predict way. But if you can arrive at potentially *any *time, you cannot possibly tell how many people will be in the queue. The original process is deterministic, but the process of measuring occurs at an arbitrary time. It is indeed this **uncertainty** that causes the process to be random.

This is why virtually every measuring process comes with a certain degree of **statistical uncertainty**, which is commonly referred to as **noise**, event though there might not be any actual randomness in the process.

### Noise in Software Development

If you are not an engineer, it might be hard to imagine ways in which noise can directly affect you. Most of the randomness that software developers encounter come from users’ inputs. The most simple example you can think of is touch input. When you tap on a screen with your finger, you cannot physically hit just a single pixel. Your finger covers a much larger area, which does not necessarily matches with what you want to touch. And since each successive tap touches a slightly different part of the screen, tapping itself can be seen as a random process, both *spatially* and *temporally*.

Here it is an interesting experiment that you can try on your phone. Open your contact list; any list that you can scroll will work. Try scrolling the list slower and slower. You will reach a point where your finger barely moves. If your phone is a few years old, you will see that the list starts jerking up and down. This is because the inputs from your finger are noisy; the position oscillates by a few pixels (even if you are doing your best to stand still) and the phone cannot tell if you want to go up or down. Most modern phones have a threshold that prevents this from happening, but it is something you can still perceive on older models. It is also worth noticing that the same jittering effect does not occur when you are scrolling. Your finger is still noisy, but the distance your finger covers is greater than its uncertainty.

![](../../assets/b9a5cb03123abe9f.jpg)

In reality, noise is everywhere. Every time you are reading data from a sensor, you will incur in some kind of noise. Whether this is embedded in the system, or added by the measuring process, the result is essentially the same. All sensor data, from GPS to gyroscopes, is noisy and needs to be processed. This topic has been explored in another online course on this blog, [An Introduction to Signal Smoothing](https://www.alanzucconi.com/?p=5010). This new series of tutorials, however, will take on a more probabilistic approach to the problem of **data de-noising**.

If you are working with Arduino, most of your sensors might benefit from using a Kalman filter. If you are a game developer, you can use one to filter users’ input on mobile devices.

## The Kalman Filter

![](../../assets/d52223e8c36d15f0.jpg)

Obtaining reliable readings from sensors is one of the main challenges that engineers face every day. Creating more accurate sensors is very expensive, and does not solve the problem. If a process is inherently random, even the most precise sensor will still be subjected to random fluctuations.

A better approach is to embrace the probabilistic nature of random processes, relying on more clever software, rather than more expensive hardware. This is precisely what Rudolf E. Kálmán and his collaborators discussed in “[A New Approach to Linear Filtering and Prediction Problems](http://www.cs.unc.edu/~welch/kalman/media/pdf/Kalman1960.pdf)“, published in 1960. Kálmán proposed a powerful, yet simple technique to obtain reliable readings from noisy sensors, which is now referred to as the **Kalman filter**.

2008 Draper Prize, Awards Committee

«The Kalman filter revolutionized the field of control theory and has become pervasive in engineering systems.»

National Academy of Engineering

Thanks to their outstanding results, Kalman filters ended up being used even in the Apollo program. The Apollo 11 Guidance Computer (below) used a Kalman filter to calculate the position of the spacecraft integrating information from the internal sensors and the radio measurements back from Earth.

![](../../assets/68c2dad4fa0fd3e2.jpg)

Despite over sixty years have passed, Kalman filters are still being used today. You can read more about its development in the article “[Applications of Kalman Filtering in Aerospace 1960 to the Present](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5466132)“.

The Kalman filter works in two steps: **prediction** and **correction**. Each filter is built with a model that tells how the system in which is used should behave. For instance, if a Kalman filter is used to measure the position of a moving train, the filter will be “shipped” with a basic understanding of how velocity and acceleration change an object’s position. This model is used in the prediction step to *guess* how the train should move, in an ideal scenario. Such a guess tends to be quite inaccurate, and is prone to *drifting*, since the errors inherited from all previous prediction steps add up over time. This is why the Kalman filter needs to correct its guess using the data from a noisy sensor. In the case of a train, it could be a GPS. What Kalman filter does is blending these two pieces of information (its *guess* and the *sensor measurements*) to find the most likely position of the train.

What makes the Kalman filter so special is that, under certain circumstances, it has been proved to be *optimal*. This means that is able to minimise the error between its updated guess and the actual position.

## What’s Next…

This first post introduced the concept of **random process**, and how Kalman filtering can be used to minimise the impact of noise in sensors. The rest of this tutorial will show the derivation of the equations involved in a Kalman filter, and how to implement it in C# for Unity and C++ for Arduino.

You can read all the tutorials in this online course here:

**Part 1.**[A Gentle Introduction to the Kalman Filter](https://www.alanzucconi.com/?p=8795)- Part 2.
[The Mathematics of the Kalman Filter](https://www.alanzucconi.com/?p=8799): The Kalman Gain - Part 3.
[Modelling Kalman Filters](https://www.alanzucconi.com/?p=8963): Liner Models - Part 4:
[The Extended Kalman Filter](https://www.alanzucconi.com/?p=14146): Non-Linear Models - Part 5.
[Implementing the Kalman Filter](https://www.alanzucconi.com/?p=9124)🚧

### Further Readings

- “
[How a Kalman filter works, in pictures](http://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/)” by Tim Babb - “
[Kalman Filter For Dummies](http://bilgin.esme.org/BitsAndBytes/KalmanFilterforDummies)” by[Bilgin Esme](https://twitter.com/RubberBoom) - “
[Kalman](http://greg.czerniak.info/guides/kalman1/)” by Greg Czerniak - “
[Understanding the Basis of the Kalman Filter Via a Simple and Intuitive Derivation](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf)” by[Ramsey Faragher](https://twitter.com/RamseyFaragher) - “
[Kalman filter](http://david.wf/kalmanfilter/)” by[David Khudaverdyan](https://twitter.com/khdavid) - “
[Kalman Filter Interview](https://towardsdatascience.com/kalman-filter-interview-bdc39f3e6cf3)” by[Harveen Singh](https://twitter.com/harveenj) - “
[Kalman Filter Simulation](https://www.cs.utexas.edu/~teammco/misc/kalman_filter/)” by Richard Teammco - “
[A New Approach to Linear Filtering and Prediction Problems](http://www.cs.unc.edu/~welch/kalman/media/pdf/Kalman1960.pdf)” by Rudolf E. Kálmán

## Leave a Reply Cancel reply