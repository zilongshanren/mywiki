---
title: The Autocorrelation Function - Alan Zucconi
url: https://www.alanzucconi.com/2016/06/06/autocorrelation-function/
author: Alan Zucconi
published: '2016-06-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

The purpose of this tutorial is to show a simple technique to estimate periodicity in time series, called ** autocorrelation**.

[Introduction](https://www.alanzucconi.com#introduction)[The Correlation Coefficient](https://www.alanzucconi.com#part1)[Autocorrelation Function](https://www.alanzucconi.com#part2)[The Code](https://www.alanzucconi.com#part3)[The Correlogram](https://www.alanzucconi.com#part4)[Conclusion](https://www.alanzucconi.com#conclusion)

This tutorial is part of a longer series that focuses on how to analyse time series.

- Part 1.
[An Introduction to Signal Smoothing](https://www.alanzucconi.com/?p=5010) - Part 2.
[Time Series Decomposition](https://www.alanzucconi.com/?p=5079) **Part 3. The Autocorrelation Function**

In the previous part of this tutorial, [Time Series Decomposition](https://www.alanzucconi.com/?p=5079), we have seen how is possible to decompose sales in their original components. One of the inputs of this process, is knowing the exact periodicity of the seasonal components. When it comes to real data, this is rarely the case.

The first step is to find a way of measuring how similar two time series are. There are countless way of doing this, depending on the underlying assumptions of your data. The most used one for those applications is called **correlation**. The correlation between two functions (or time series) is a measure of how similarly they behave. It can be expressed as:

![Rendered by QuickLaTeX.com \[corr \left(X, Y \right) = \frac{cov\left(X, Y\right)}{std\left(X\right) std\left(Y\right)}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c0db1b4bc6f19b6fb6eddd63c80f7dfd_l3.png)


with ![Rendered by QuickLaTeX.com std\left(X\right)](../../assets/1f2db02c470d150c.png)

![Rendered by QuickLaTeX.com mean\left(X\right)](../../assets/1370d416f1cfbe5a.png)

**standard deviation** and the **mean** of ![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)


![Rendered by QuickLaTeX.com \[std\left(X\right) = \sqrt{ \frac{1}{N} \sum_{i=1}^{N} \left[ X_i - mean\left(X\right) \right]^2 }\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-aaf8fc0e35c53260847b4c044a76526b_l3.png)


![Rendered by QuickLaTeX.com \[mean\left(X\right) = \frac{1}{N} \sum_{i=1}^{N} X_i\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8ee1f45b7973dce7c8b3e565f222fe80_l3.png)


The mean is simply the average of the whole time series. The standard deviation, instead, indicates how much the points of the series tends distance themselves from the mean. This quantity is often associated with **variance**, defined as:

![Rendered by QuickLaTeX.com \[var\left(X\right) = std\left(X\right)^2\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-262ceca781bb5deac58dba5dc86d7d94_l3.png)


When the variance is zero, all the points in the series are equal to the mean. A high variance indicates that the points are scattered around.

The term ![Rendered by QuickLaTeX.com cov\left(X, Y\right)](../../assets/3a93c138d292ba26.png)

[ covariance ](https://en.wikipedia.org/wiki/Covariance)between

![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

The covariance is calculated as follow:

![Rendered by QuickLaTeX.com \[cov \left( X, Y \right) = \frac{1}{N} \sum_{i=1}^{N} \left[ X_i - mean\left(X\right) \right]\left[ Y_i - mean\left(Y\right) \right]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-65f99654098899d0097e5609c546797d_l3.png)


and is easy to see that indeed ![Rendered by QuickLaTeX.com cov\left(X,X\right) = var\left(X\right)](../../assets/08fe383e3982ef9f.png)


Looking back to the definition of correlation, it is now easy to understand what is trying to capture. It’s a measure of how similarly ![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

![Rendered by QuickLaTeX.com -1](../../assets/5209a4a606950b66.png)

![Rendered by QuickLaTeX.com +1](../../assets/07166c3ac7d7ae94.png)


The idea behind the concept of autocorrelation is to calculate the correlation coefficient of a time series with itself, shifted in time. If the data has a periodicity, the correlation coefficient will be higher when those two periods resonate with each other.

The first step is to define an operator to shift a time series in time, causing a delay of ![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

**lag operator**:

![Rendered by QuickLaTeX.com \[lag\left(X_i,t\right) = X_{i-t}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-1ccf17b3150c5b1afc02e8f584205f37_l3.png)


The autocorrelation of a time series with lag ![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)


![Rendered by QuickLaTeX.com \[autocorr\left(X,t\right) = corr\left[X, lag\left(X,t\right) \right]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-697926abb521bec043ec86002b1acaa1_l3.png)


which can also be expressed as:

![Rendered by QuickLaTeX.com \[autocorr\left(X,t\right)=\frac{cov\left[X, lag\left(X,t\right)\right]}{std\left[X\right] std\left[ lag\left(X,t\right) \right]}=\frac{cov\left[X, lag\left(X,t\right)\right]}{var\left(X\right) }=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7883476080f28df66930803be5ce6d72_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{\sum_{i=1}^{N} \left[ X_i - mean\left(X\right) \right]\left[ X_{i-t} - mean\left(X\right) \right]}{\sum_{i=1}^{N} \left[ X_i - mean\left(X\right) \right]^2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-61a722bab979bbca4073a4b53bb4980c_l3.png)


The above mentioned form is amenable to be written as code. The easiest function is surely the one that calculates the mean of a time series:

public float Mean (float [] x) { float sum = 0; for (int i = 0; i < x.length; i ++) sum += x[i]; return sum / x.length; }

A little bit complicates is the case for the autocorrelation function. It creates an array which will contain the final result. Each `t`

-th element contains ![Rendered by QuickLaTeX.com autocorr\left(X,t\right)](../../assets/663f178942314955.png)

![Rendered by QuickLaTeX.com \frac{N}{2}](../../assets/49bb9fa3b57a3ae1.png)


public float [] Autocorrelation (float [] x) { float mean = Mean(x); float [] autocorrelation = new float[x.length/2]; for (int t = 0; t < autocorrelation.length; t ++) { float n = 0; // Numerator float d = 0; // Denominator for (int i = 0; i < x.length; i ++) { float xim = x[i] - mean; n += xim * (x[(i + t) % x.length] - mean); d += xim * xim; } autocorrelation[t] = n / d; } return autocorrelation; }

Line 14 implements an inline lag operator. It shifts `i`

by `t`

, and uses the modulo operator so that the time series loops. If this is not the desired case, then you should only loop up to `x.length -t`

.

Autocorrelation is a relatively robust technique, which doesn’t come with strong assumptions on how the data has been created. If in the previous post we have used a synthetic sales data, this time we can confidently use real analytics:

This is the plot for the autocorrelation function, also known as **correlogram**:

All correlograms start at ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com t=0](../../assets/6c6cee41bddf42e5.png)

![Rendered by QuickLaTeX.com t=7](../../assets/3ec7045178b704ee.png)

![Rendered by QuickLaTeX.com 7](../../assets/f42317be7373fc5e.png)

![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

![Rendered by QuickLaTeX.com 7](../../assets/f42317be7373fc5e.png)


Because of this resonance, interpreting correlograms is not always easy. There are several improvements on this technique which can help to extract actual cycles. **Partial autocorrelation functions** controls for the values of the time series at all shorter lags. This removes interference and resonance with multiple cycles, highlighting a more clear periodicity. A more advanced technique, called ** Power Spectral Density**, performs a Fourier analysis on the correlogram to find its main component.

### 📚 Recommended Books

This tutorial concludes the series on time series analysis. We have explored valuable techniques to extract information from temporal data, focusing on their potential and limitations.

### Other resources

- Part 1.
[An Introduction to Signal Smoothing](https://www.alanzucconi.com/?p=5010) - Part 2.
[Time Series Decomposition](https://www.alanzucconi.com/?p=5079) **Part 3. The Autocorrelation Function**

## Leave a Reply Cancel reply