---
title: An Introduction to Signal Smoothing - Alan Zucconi
url: https://www.alanzucconi.com/2016/06/03/an-introduction-to-signal-smoothing/
author: Alan Zucconi
published: '2016-06-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Noise is everywhere. Whether you’re sampling accelerometer data for a mobile game or trying to measure the temperature of a room, noise will be there. Even if you could remove all the noise from an input device, you’ll still have a certain degree of uncertainty. If a player has tapped on the screen, where did they really wanted to tap? All these scenarios forces to re-think about how we gather and preprocess data.

Filters are mathematical and computational tools that, taken a series of observations, attempt to find the most likely signal that generated them. Filters are used to tackle the ubiquitous noise and uncertainty that permeates all sensor readings. All modern devices record user input via sensors. Whether it’s a touch screen or a joystick, mobile phones and game controllers are not immune to noise. Consequently, filters play an essential (yet somehow hidden) role in the perceived user experience.

This series on smoothing filters will introduce the most common types of techniques. Applying them to games can lead to significantly improvements in usability.

Let’s start with a very simple example which will help us to understand how noise affects signals. Imagine a sensor that is queried at fixed intervals, producing the observation ![Rendered by QuickLaTeX.com S_i](../../assets/9b0db370730efcd1.png)

![Rendered by QuickLaTeX.com i](../../assets/9079b2bc6b821844.png)

`Input.GetAxis("Vertical")`

. If you’re an engineer, it could be the voltage reading from a potentiometer, such as `analogRead(3)`

. What these time sequences have in common is that they are affected by noise. The following chart shows the above-mentioned signal, and how it is after being affected by noise.

In this example, noise has been artificially injected into the original signal. To each point ![Rendered by QuickLaTeX.com S_i](../../assets/9b0db370730efcd1.png)


![Rendered by QuickLaTeX.com \[N_i = S_i + rand\left(\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-044e32933c52529fbd6b70aae3d83a15_l3.png)


When this happens, we are talking about **additive noise**, uniformly distributed. The noise injected here is totally independent from the original signal. Additive uniform noise is often the result of an external interference. Like picking up static with an old CTR monitor.

Is it possible to recover a signal that has been corrupted by noise? The answer is …it depends. It depends on the type of noise (which is a direct consequence of the process that altered the signal), and on its extent. One of the simplest technique to attenuate additive noise is called moving average. It is based on the assumption that independent noise is not going to change the underlying structure of the signal. If this is true, averaging few points should attenuate the contribution of the noise. [ Moving average](https://en.wikipedia.org/wiki/Moving_average) is the name of a technique that, for each point in a signal, calculates the average of its neighbouring points. If we average (for instance) three points, the filtered signal is given by:

![Rendered by QuickLaTeX.com \[F_i = \frac{N_{i-1}+N_{i}+N_{i+1}}{3}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8e491b7542b56e277d81528e4e722f77_l3.png)


If all the observations of the signal are available, we can define moving average with **window size** ![Rendered by QuickLaTeX.com N=2k+1](../../assets/fb082e8019e0a719.png)


![Rendered by QuickLaTeX.com \[F_i = \frac{1}{N} \sum_{j = -k}^{+k} S_{i-j}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7e0514c08d31f7d8c2c783d1d1fe84b7_l3.png)


In the following chart, a moving average technique (with window size of 6 points) has been applied to the above-mentioned noisy sinusoid:

The original signal is almost entirely recovered. If you’re a developer, this filter can be achieved with the following (very naïve) code:

public float [] MovingAverage (float [] data, int size) { float [] filter = new float [data.length]; for (int i = points/2; i < data.length-points/2; i++) { float mean = 0; for (var j = -points/2; j < points/2; j++) mean += data[i + j]; filter[i] = mean / size; } return filter; }

Increasing the window size allows to reduce the effect of the added noise, but is also likely to cause an excessive smoothing of the original signal. Moving average, in fact, works nicely for signals that are continuous and smooth. When big changes are present, this filtering technique is likely to alter the original signal more than the noise itself:

It’s also interesting to notice that the signal is completely recovered in its linear parts. Moving average is the optimal solution when you have linear signals which are affected by additive uniform noise. Such a situation, however, is extremely fictitious. Real world applications are unlikely to have such convenient constraints.

While presenting moving average, we have also introduced a contraint over ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

*symmetrical*. We sample an equal number of points ![Rendered by QuickLaTeX.com k](../../assets/1f6815ea9a6d4626.png)

![Rendered by QuickLaTeX.com N_i](../../assets/957289454b08cb87.png)

![Rendered by QuickLaTeX.com N_i](../../assets/957289454b08cb87.png)

![Rendered by QuickLaTeX.com 2k+1](../../assets/db3bdeba5b3871ae.png)

![Rendered by QuickLaTeX.com M = 2k](../../assets/935331fc45adc5e7.png)

![Rendered by QuickLaTeX.com k=2](../../assets/898e25ba303d198e.png)


![Rendered by QuickLaTeX.com \[MA^L_4=\frac{N_{i-2} + N_{i-1} + N_{i}+ N_{i+1} }{4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a429ade7e2735315ca512c8a60433d3f_l3.png)


![Rendered by QuickLaTeX.com \[MA^R_4=\frac{N_{i-1} + N_{i} + N_{i+1}+ N_{i+2} }{4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fe9f78b56fe356cdee280519b2d913a7_l3.png)


Both these expressions are valid, and there is no reason to prefer one over the other. For this reason, we can average the together to get a centered moving average. This is often referred as ![Rendered by QuickLaTeX.com 2\times 4 MA](../../assets/d3b8bfcc107417a6.png)


![Rendered by QuickLaTeX.com \[2\times 4 MA=\frac{1}{2} \left[ \frac{1}{4}\left(N_{i-2} + N_{i-1} + N_{i} + N_{i+1} \right)+\frac{1}{4}\left( N_{i-1} + N_{i} + N_{i+1} + N_{i+2} \right) \right]=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ef41cee50b020f5b89200841ce0501ea_l3.png)


![Rendered by QuickLaTeX.com \[=\frac{N_{i-2}}{8} + \frac{N_{i-1}}{4} + \frac{N_{i}}{4}+\frac{N_{i+1}}{4}+\frac{N_{i+2}}{8}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8c4d9393a93fdc7718feacf1d52f84e7_l3.png)


The result obtained looks very similar to a moving average centered on ![Rendered by QuickLaTeX.com N_i](../../assets/957289454b08cb87.png)


Moving average treats each point in the window with the same importance. A more reasonable approach is to value points that are further away from ![Rendered by QuickLaTeX.com S_i](../../assets/9b0db370730efcd1.png)

**weighted moving average** does, introducing a weight ![Rendered by QuickLaTeX.com W_j](../../assets/a017789fb4e6ccad.png)


![Rendered by QuickLaTeX.com \[F_i = \sum_{j = -k}^{+k} S_{i-j} W_{k+j}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-353e12b68b7f3f37e7a3701d4b9e3bb4_l3.png)


with the additional contraint that all ![Rendered by QuickLaTeX.com W_j](../../assets/a017789fb4e6ccad.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


The previous code for moving average can be corrected like this:

for (var j = -points/2; j < points/2; j++) mean += data[i + j] * weights[j+points/2];

Looking back at the repeated average, we can now say that ![Rendered by QuickLaTeX.com 2\times 4 MA](../../assets/d3b8bfcc107417a6.png)

![Rendered by QuickLaTeX.com \frac{1}{8},\frac{1}{4},\frac{1}{4},\frac{4}{8}](../../assets/b02520ecaa136f83.png)


This tool is not incredibly more powerful, but at the drawback of having many more parameters to set. If you are familiar with function analysis, you might have recongised this as a very rough definition of the [convolution](https://en.wikipedia.org/wiki/Convolution) operator. Carefully chosing the weights results in a variety of interesting effects, from edge detection to gaussian blur.

To give an example of this, we can perform a convolution of a square wave with the [Mexican Hat function](https://en.wikipedia.org/wiki/Mexican_hat_wavelet). To do this, all that is needed is to initialise the weights so that their shape follows this function:

![Rendered by QuickLaTeX.com \[f\left(t\right)=\left(1-t^2\right) e^{\frac{-t^2}{2}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e7fd36d60d8a43d4bea77934990b83ef_l3.png)


With a piece of code like this:

float[] kernel = new float[10]; for (int i = 0; i <= kernel.length; t ++) { float t = i +4; kernel[i] = (1-(t*t)) * Math.exp(-(t*t)/2); }

Convolution with the Mexican Hat function allows to perform edge detection.

This technique extracts rapid changes from the data. If you’re a game developer, it can be used to detect sudden movements in the player’s input. This is the first step towards a reliable gesture detection algorithm.

### 📚 Recommended Books

This post introduced the problem of noisy signals, and discussed two common techniques to tackle it. It’s important to remember that there isn’t an “ultimate” technique that always works. Every algorithm has its own pros and cons. Knowing under which assumptions it has been design is essential.

The next part of this tutorial will explore how the moving average technique here introduced can be used to decompose time series. You’ll need this technique to fully understand (and possibly predict) your revenues on Steam.

### Other resources

**Part 1. An Introduction to Signal Smoothing**- Part 2.
[Time Series Decomposition](https://www.alanzucconi.com/?p=5079) - Part 3.
[The Autocorrelation Function](https://www.alanzucconi.com/?p=5104)

## Leave a Reply Cancel reply