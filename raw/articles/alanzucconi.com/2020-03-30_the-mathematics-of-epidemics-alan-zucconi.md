---
title: The Mathematics of Epidemics - Alan Zucconi
url: https://www.alanzucconi.com/2020/03/30/mathematics-epidemics/
author: Alan Zucconi
published: '2020-03-30'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This online course introduces the topic of modelling and simulating epidemics. If you are interested in understanding how Mathematicians, Programmers and Data Scientists are studying and fighting the spread of diseases, this series of posts is what you are looking for.

**Part 1.**[The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838)- Part 2.
[Simulating Epidemics](https://www.alanzucconi.com/?p=11840) - Part 3.
[From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842)

This online course is inspired by the recent COVID-19 pandemic. Now more than ever we need skilled and passionate people to focus on the complex subject of Epidemiology. I hope these articles will help some of you to get started.

### Introduction

It is impossible to deny that the recent pandemics of COVID-19 has changed the world we live in. With a significant part of the world population under lockdown, most people living in Western countries have been—one way or another—affected by the novel coronavirus (below, an artistic rendering by [David S. Goodsell](https://twitter.com/dsgoodsell)). Now more than ever, we are bombarded with a constant stream of contradicting news and inconsistent policies. Technical terms such as *exponential growth*, *social distancing* and *logarithmic plots* are now commonly used on both TV and social media. And without the right background, it might be very difficult to make sense of the numbers that are constantly been updated every hour. When colleagues, friends and relatives are getting ill, it is only natural wanting to do everything in our power to help them. And, paradoxically, we are being told to stay home and *do nothing*. It is hard to understand how any good could actually come out of inaction.

![](../../assets/d3b3dbaf26e73d48.png)

As a Science Communicator—one which family has been affected—I feel is important I take this opportunity to add my contribution to the current discourse. Not the one surrounding COVID-19 (for which I am not really qualified to talk about), but the study and simulation of epidemics. Since 2015, I have talked extensively about the power of simulations, and how they could be used to solve a variety of different problem. From simulating the process of *evolution by natural selection* ([Evolutionary Computation](https://www.alanzucconi.com/2016/04/06/evolutionary-coputation-1/)) to harnessing the power of modern GPUs ([How to Use Shaders for Simulations](https://www.alanzucconi.com/2016/03/02/shaders-for-simulations/)), up to the creating photorealistic rendering of a planet’s sky ([Volumetric Atmospheric Scattering](https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/)).

If you want to understand how scientists model and simulate the evolution of epidemics and the spread of diseases on large populations, this is the right place. I sincerely hope this series of articles will not only give you the tools to better understand the terminology and numbers surrounding the current pandemics. I ultimately hope it will inspire more passionate developers to proactive study and research the fascinating fields of epidemiology. Just a few days ago, the Royal Society started coordinating the [Rapid Assistance in Modelling the Pandemic](https://epcced.github.io/ramp/) (RAMP): an urgent *call to action* addressed to the scientific modelling community, recruiting developers, programmers and data scientists all over the UK to study and predict the evolution of the current COVID-19 pandemic. While hundreds of thousands nurses and doctors are saving lives every day, there are probably as many researchers and developers who are working around the clock to end the current pandemic. Those are hidden heroes which might end up saving your life, even though you never met them.

There are probably many researchers and developers who are working around the clock to end the current pandemic. Those are hidden heroes which might end up saving your life, even though you never met them.


## Modelling Epidemics

Epidemics are very complex social phenomena that involve millions of people, over hundreds of countries. They are undeniably driven by the individual choices of each person involved, although they ultimately follow very recognisable patterns.

At first glance, this might seem counterintuitive. If the decisions of each person are arbitrary and unpredictable, how could an overall population made out of millions of them become suddenly predictable?

Let’s try to answer this question with a simple example. Let’s imagine a population of arrows, each one pointing in a different direction (below). What is the “overall” direction they point at? If we assume there is a sufficiently large number of them, it is also reasonable to assume that for each arrow pointing in a certain direction, there is another one pointing in the opposite one. The more arrows we have, the more confident we can be about the fact that their sum cancels out.

![](../../assets/ecbcfff562085e71.png)

This concept is related to the [Law of Large Numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers), which describes the overall behaviour of large numbers of random phenomena. Even if we assumed human behaviour to be completely random (which is not), we would still be able to model the overall behaviour of a sufficiently large population. So, we do not need to take into account the behaviour of each individual person to draw meaningful conclusions on the overall population.

### Exponential Growth

One of the most simple ways to model the evolution of an epidemic is to only focus on the number of infected people, ![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com r](../../assets/0f11bfbe35b9451a.png)

![Rendered by QuickLaTeX.com r=2](../../assets/c8c68f058ded4ba1.png)


(1) ![Rendered by QuickLaTeX.com \begin{equation*}X\left(t+1\right)=r X\left(t\right)\end{equation*}](../../assets/80fcc669f50d1642.png)


In the expression above, ![Rendered by QuickLaTeX.com X\left(t\right)](../../assets/6c8b191e5574dcbd.png)

![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

![Rendered by QuickLaTeX.com X\left(t+1\right)](../../assets/5639db2c5d404864.png)

**recurrence relationship**, as the value for ![Rendered by QuickLaTeX.com t+1](../../assets/c98aef5936371823.png)

![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

**recursive functions**.

We can expand the equation by noticing that it follows a simple pattern:

(2) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}X\left(0\right)&=& 1 & & &=&{r}^0\\X\left(1\right)&=& r X\left(0\right) &=& r &=&{r}^1\\X\left(2\right)&=& r X\left(1\right) &=& r r &=&{r}^2\\X\left(3\right)&=& r X\left(2\right) &=& r {r}^2 &=&{r}^3\end{align}\end{equation*}](../../assets/2ba33761f6befc53.png)


It is easy to see that we can generalise this with a traditional **closed-form expression**:

(3) ![Rendered by QuickLaTeX.com \begin{equation*} X\left(t\right)={r}^t\end{equation*}](../../assets/f869b2c9c8ca9cdb.png)


which is an **exponential curve**. This means that if every infected person always infects ![Rendered by QuickLaTeX.com r](../../assets/0f11bfbe35b9451a.png)


### Logistic Growth

The model presented in the section above works very well during the early stages of an epidemic. However, it is clear that such growth cannot be sustained because we will reach the point where all people are infected. After an initial *explosion*, the number of infected people will start growing slower because the more people are infected, the harder it is to find someone new who can be infected.

The idea is to change ([3](https://www.alanzucconi.com#id51418722)) by adding a factor that can slow down the exponential growth. We can think about ![Rendered by QuickLaTeX.com r](../../assets/0f11bfbe35b9451a.png)

![Rendered by QuickLaTeX.com X\left(t\right)](../../assets/6c8b191e5574dcbd.png)


When the model starts, ![Rendered by QuickLaTeX.com r](../../assets/0f11bfbe35b9451a.png)

![Rendered by QuickLaTeX.com r_0](../../assets/6c2220d02ffe1f67.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com r\left(X\left(t \right)\right)](../../assets/757ce6abac184744.png)


What we want, in a nutshell, is to enforce the following properties:

(5) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}X\left(t\right) = 0 &\rightarrow & r =r_0 \\X\left(t\right) = C &\rightarrow & r = 0\end{align}\end{equation*}](../../assets/aea316e7561c4130.png)


The simplest way to model this new function is with a linear mapping:

(6) ![Rendered by QuickLaTeX.com \begin{equation*}r = r_0\left(1 - \frac{X\left(t \right)}{C}\right)\end{equation*}](../../assets/c491757923817d52.png)


We can now update ([1](https://www.alanzucconi.com#id3713768402)), replacing ![Rendered by QuickLaTeX.com r](../../assets/0f11bfbe35b9451a.png)

[6](https://www.alanzucconi.com#id1529150060)):

(7) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}X\left(t+1\right)&=&\boxed{r} X\left(t\right) \\X\left(t+1\right)&=&\boxed{r_0\left(1 - \frac{X\left(t \right)}{C}\right)}X\left(t \right)\end{align}\end{equation*}](../../assets/a7ff5bdda324a83a.png)


The new equation results in the so-called **logistic growth**, which approximately very well the growth of populations and the spread of diseases.

Converting the recurring expression for ![Rendered by QuickLaTeX.com X\left(t\right)](../../assets/6c8b191e5574dcbd.png)

**ordinary differential equation**. For this reason, I will omit the full derivation; its solution take the form of the well-known **logistic function**:

(8) ![Rendered by QuickLaTeX.com \begin{equation*}X\left(t\right) = \frac{C}{1+\left(\frac{C-X\left(0\right)}{X\left(0\right)}\right) \exp\left\{-r_0 t\right\} }\end{equation*}](../../assets/cf844ecb1f609612.png)


where:


: the **time**after the first infection (for instance, the number of days);

: the **infected population**at time

;

: the number of infected people at time

;

: the number of infected people after which no new infections are possible (known as the **carrying capacity**);

: how many other people, on average, each infected person infects (known as the **basic reproduction number**).

### Compartmental Models

Both the exponential and logistic growth can be applied to a variety of different scenarios, some of which are not related to the study of epidemics. In fact, they were originally designed to model the growth of a generic population.

In the scientific literature, there are several mathematical models that have been created specifically for the study of how diseases spread in a given population. A branch of them models are called **compartmental models**, as they divide the general population into different groups called or compartments (and assuming no new people are born or can enter into the system).

One of the most simple compartmental models is called **SIR**, from the initials of the three groups it models: **susceptible**, **infected** and **recovered **people. The idea is that, at time ![Rendered by QuickLaTeX.com t=0](../../assets/6c6cee41bddf42e5.png)

*removed*: because they do not play a role anymore to the spread of the disease. *Resistant* is another term that is often seen in the literature. The model was originally developed by William Ogilvy Kermack and Anderson Gray McKendrick in 1927, but gained popularity only in 1979.

The SIR model is often indicated using the following notation, which explains the journey of a person from the different compartments:

(11) ![Rendered by QuickLaTeX.com \begin{equation*}\mathcal{S} \rightarrow \mathcal{I} \rightarrow \mathcal{R}\end{equation*}](../../assets/1b5b243c20423149.png)


The purpose of a SIR model is to find a series of equations to calculate, at a specific time ![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

![Rendered by QuickLaTeX.com S\left(t\right)](../../assets/9c961d8d9457337e.png)

![Rendered by QuickLaTeX.com I\left(t\right)](../../assets/cf8666a1b76e7a09.png)

![Rendered by QuickLaTeX.com R\left(t\right)](../../assets/f2c9c45346686e96.png)


They are best defined as a series of differential equations:

(12) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}\frac{\partial S}{\partial t} &= -\beta \frac{SI}{N} & \\\frac{\partial I}{\partial t} &= +\beta \frac{SI}{N} & -\gamma I \\\frac{\partial R}{\partial t} &= &+\gamma I \\\end{align}\end{equation*}](../../assets/338dd2f59dd0ec75.png)


(13) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}N &= S+I+R \\\end{align}\end{equation*}](../../assets/d7f3162eab4a1c33.png)


where:


: controls how often an interaction between a susceptible and infected people results in a new infection;

: the rate at which infected people recover (or die) and move into the removed compartment.

If we want to be more precise, we can also indicate on the arrows the parameters that control the *flow* between different compartments:

(14) ![Rendered by QuickLaTeX.com \begin{equation*}\mathcal{S} \xrightarrow{\beta SI} \mathcal{I} \xrightarrow{\gamma I} \mathcal{R}\end{equation*}](../../assets/6dcb34f2cae7c1e8.png)


In this model, ![Rendered by QuickLaTeX.com r_0 =\frac{\beta}{\gamma}](../../assets/6689ff3622632a44.png)


Below, you can find an interactive tool to simulate the evolution of a SIR model. It is based directly on the differential equations presented in ([12](https://www.alanzucconi.com#id1499746777)).

The chart above uses [Hans Nesse](http://www.public.asu.edu/~hnesse)‘s implementation of the Runge-Kutta method.

### Other Models

There are several other models available, which include different compartments. A simpler one is the SIS model, which includes the possibility for people of being reinfected.

(15) ![Rendered by QuickLaTeX.com \begin{equation*}\mathcal{S} \rightarrow \mathcal{I} \rightarrow \mathcal{S}\end{equation*}](../../assets/970fa68d87735a02.png)


A more complex one, SEIRS, contemplates the possibility who have been exposed to the disease but are not infectious yet. This compartment is referred to as **exposed**:

(16) ![Rendered by QuickLaTeX.com \begin{equation*}\mathcal{S} \rightarrow \mathcal{E} \rightarrow \mathcal{I} \rightarrow \mathcal{R} \rightarrow \mathcal{S}\end{equation*}](../../assets/ec77eeeef45b5b6e.png)


### 📚 Recommended Books

## What’s Next…

The first article in this online course about epidemics explored how Mathematicians and Data Scientists model them using differential equations. The exponential and logistic growth curves were introduced, followed by the compartmental models. Among the latter, the SIR model is one of the most popular.

The next article, [Simulating Epidemics](https://www.alanzucconi.com/?p=11840), will move away from the mathematical formulation of epidemics, to focus on a more programmatical and flexible approach.

**Part 1.**[The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838)- Part 2.
[Simulating Epidemics](https://www.alanzucconi.com/?p=11840) - Part 3.
[From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842)

### Additional Resources

[Hans Nesse – Global Health – SIR Model](http://www.public.asu.edu/~hnesse/classes/sir.html)[The Logistic Map](https://www.complexity-explorables.org/flongs/logistic/)[Exponential & logistic growth](https://www.khanacademy.org/science/biology/ecology/population-growth-and-regulation/a/exponential-logistic-growth)[SIR and SIRS models](http://idmod.org/docs/general/model-sir.html)

### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package presented in this tutorial on [Patreon](https://www.patreon.com/posts/35446442). The package contains all the scripts, scenes, prefabs and sprites necessary to recreate the images presented in this online series, including the one below.

![](../../assets/9db03a94f0a8ad52.gif)

All of the revenue from this tutorial will be donated to the [National Emergencies Trust](https://nationalemergenciestrust.org.uk/coronavirus/) (NET), to help those most affected by the recent coronavirus outbreak.

## Leave a Reply Cancel reply