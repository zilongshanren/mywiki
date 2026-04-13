---
title: Time Series Decomposition - Alan Zucconi
url: https://www.alanzucconi.com/2016/06/05/time-series-decomposition/
author: Alan Zucconi
published: '2016-06-05'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will teach you how you can extract valuable information from time series, such as your sold copies on Steam or your Google Analytics. The previous part of this series introduced a technique called **moving average**, which has been used to attenuate the effects of noise in a signal. When signals represent an event that evolves over time, we are in front of a **time series**. Classical decomposition is a technique that attempts to find the main trends within time series.

[Introduction](https://www.alanzucconi.com#introduction)[Time Series (De)Coposition](https://www.alanzucconi.com#part1)[Trend Component Estimation](https://www.alanzucconi.com#part2)[Seasonal Component Estimation](https://www.alanzucconi.com#part3)[Irregular Component Estimation](https://www.alanzucconi.com#part4)[Summary](https://www.alanzucconi.com#part5)[Conclusion](https://www.alanzucconi.com#conclusion)

Even when it’s highly effective, moving average is completely agnostic to the signal that is filtering. We can achieve much better results if we understand the process that is generating our data, and which components contribute to its final shape. Let’s think for a second about a game on Steam. The following chart shows the number of copies activated each day, for a hypothetical game:

Time series that represents sold copies naturally contains several components. The **trend component **![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

**seasonal component**, ![Rendered by QuickLaTeX.com S](../../assets/4b8b5ff505466deb.png)

**irregular **(or **residual**)** component**, ![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)


The sales chart shown in the previous section was indeed generated as the sum of these three components:

The seasonal cycle has a length of 30 days; it is reasonable to assume that every month has a similar influence on the sold copies. Knowing the length of a cycle will be essential to decompose our time series in its basic components.

As described in the previous part of this tutorial, [An Introduction to Signal Smoothing](https://www.alanzucconi.com/?p=5010), a first possible step to highlight the true trend of the data is to use **moving average**. One of the assumption is that the data contained a 30-day seasonal cycle. If that is the case, we should choose a window that covers those 30 days entirely. Since 30 is an even number, ![Rendered by QuickLaTeX.com 2 \times 30 MA](../../assets/1b064fd5f86c8171.png)

![Rendered by QuickLaTeX.com MA](../../assets/4d0819ee1512d9dc.png)


This produces a new time series, which we call ![Rendered by QuickLaTeX.com \hat{T}](../../assets/0afa251583a06692.png)

![Rendered by QuickLaTeX.com T=\hat{T}](../../assets/4dcccc56b6958b72.png)

![Rendered by QuickLaTeX.com \hat{T}](../../assets/0afa251583a06692.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

**detrended series**.

The effectiveness of ![Rendered by QuickLaTeX.com 2\times 30 MA](../../assets/ccdaf787e145098e.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

![Rendered by QuickLaTeX.com \hat{S}^\star](../../assets/66652f9ad1e94526.png)


float [] season = new float [30]; for (int day = 0; day < 30; day ++) { // Averages across all months float sum = 0; for (int month = 0; month < 12; month ++) sum += detrended[month*30 + day]; season[day] = sum / 30; }

We can now replicate those ideal 30 days 12 times, to reconstruct the seasonal component ![Rendered by QuickLaTeX.com \hat{S}](../../assets/51cbf4e37e59cce3.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)


If you look at our Steam sales toy example, you can see that the seasonal component is a sinusoid. This means that it sums up to zero. The assumption under which moving average removes noise is that it must sum up to zero. This is rarely the case, since most seasonal cycles sums up to a positive quantity. This is the stage in which we can check whether our assumption is correct or not. What we have to do is to sum up all the days in a month, to see whether or not the zero-sum property yields:

![Rendered by QuickLaTeX.com \[s=\sum_{j=0}^{30-1}_ \hat{S}^\star_j W_j\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-26648cdb944903a67bcec1e56a577dd9_l3.png)


where ![Rendered by QuickLaTeX.com W_j](../../assets/a017789fb4e6ccad.png)

![Rendered by QuickLaTeX.com s](../../assets/864f28b25521f331.png)

![Rendered by QuickLaTeX.com \hat{T}](../../assets/0afa251583a06692.png)


![Rendered by QuickLaTeX.com \[\hat{T} = MA_{2\times 30}\left( Y \right) - s\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8d6e6ed5b9d7ecc0838ab72a61a85a6d_l3.png)


The last step is to extract all the components from ![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

![Rendered by QuickLaTeX.com \hat{I}](../../assets/29a9bca4f61f5f14.png)


![Rendered by QuickLaTeX.com \[\hat{I} = Y - \hat{T} - \hat{S}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f8f9ea5328aa4a3151955aaa0eb2a205_l3.png)


The results of this analysis can be seen in the graph below. The original components are shown with a dotted line for reference:

**Assumptions**

- The time series can be decomposed in trend, seansonal and irregular components:
![Rendered by QuickLaTeX.com \[Y = T + S + I\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a46df9d3dedfd41e06cb33a08d80bb0a_l3.png)

- Seasonal component

has known period

.

For instance,

if we have a monthly cycle. - The seasonal component is repeated

times, meaning

is composed of

observations.

For instance,

if we have data for twelve months. - There is one entry for each day.

**Inputs**


: the original time series;

: the lenght of the seasonal cycle;

: the number of cycles in the data.

**Output**


: estimation for

;

: estimation for

;

: estimation for

.

**Procedure**

- Smooth

using moving average to find the first approximation of the trend component,

.

If m is odd, use

, otherwise

:![Rendered by QuickLaTeX.com \[\hat{T}^\star = MA_m \left( Y \right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-895cbe14b1ef8e61c5a5051a27a9d19f_l3.png)

- Calculate the detrended series

:![Rendered by QuickLaTeX.com \[\hat{D} = Y - \hat{T}^\star\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-eb5c2b83464f332e18cbf97d6bbff351_l3.png)

- Calculate a single seasonal cycle

(of lenght

) by averaging out the data across all available repetitions of the cycle:![Rendered by QuickLaTeX.com \[\hat{S}^\star_i = \frac{1}{n} \sum_{j=0}^{n-1} \hat{D}_{jm + i}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6e7f5448bcf069447a748b2569f58f3b_l3.png)

- Calculate the averaged sum a single seasonal cycle, using the same weights

used in moving average of step 1:![Rendered by QuickLaTeX.com \[s=\sum_{j=0}^{m-1}_ \hat{S}^\star_j W_j\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6854508e1630109cfbbfaa48b3ef07d1_l3.png)

- Calculate a better estimation for the trended component:
![Rendered by QuickLaTeX.com \[\hat{T}_i = \hat{T}^\star_i - s\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-bc7d7838d5611d62fb6da49de37b54e3_l3.png)

- Calculate the seasonal component

by concatenating

for

times:![Rendered by QuickLaTeX.com \[\hat{S} = \hat{S}^\star \times n\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8c5ad308552ba5bfd79ecf72675ae2ce_l3.png)

- Calculate the irregular component:
![Rendered by QuickLaTeX.com \[\hat{I} = \hat{D} - \hat{S}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f69afa2fb03f3c7c618cc8057807479e_l3.png)


### 📚 Recommended Books

This tutorial shown a powerful approach to decompose time series in their main components. The technique has been developed for financial purposes, and it works very well with sales data. The main drawback of the classical time series decomposition is that it does not work well with random events, or multiple cycles. Real sales often exhibit not only monthly but also weekly and quarterly cycles.

### Other resources

- Part 1.
[An Introduction to Signal Smoothing](https://www.alanzucconi.com/?p=5010) **Part 2. Time Series Decomposition**- Part 3.
[The Autocorrelation Function](https://www.alanzucconi.com/?p=5104) [Time Series Decomposition – OTexts](https://www.otexts.org/fpp/6)

## Leave a Reply Cancel reply