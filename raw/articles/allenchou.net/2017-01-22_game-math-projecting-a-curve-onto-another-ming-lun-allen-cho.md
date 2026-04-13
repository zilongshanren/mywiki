---
title: 'Game Math: “Projecting” a Curve onto Another | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2017/01/projecting-a-curve-onto-another/
author: Allen Chou
published: '2017-01-22'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

Also, this post is part 1 of a series ([part 2](http://allenchou.net/2017/02/curve-approximation-via-curve-projection/)) leading up to a geometric interpretation of [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform) and [spherical harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics).

Fourier transform and spherical harmonics are mathematical tools that can be used to represent a function as a combination of [periodic functions](https://en.wikipedia.org/wiki/Periodic_function) (functions that repeat themselves, like sine waves) of different frequencies. You can approximate a complex function by using a limited number of periodic functions at certain frequencies. Fourier transform is often used in audio processing to post-process signals as combination of sine waves of different frequencies, instead of single streams of sound waves. Spherical harmonics can be used to approximate baked ambient lights in game levels.

We’ll revisit these tools in later posts, so it’s okay if you’re still not clear how they can be of use at this point. First, let’s start somewhere more basic.


### Projecting a Vector onto Another

If you have two vectors ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

**projecting onto ** means stripping out part of ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)


![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

[Wikipedia](https://en.wikipedia.org/wiki/Vector_projection):

![vector projection](../../assets/2ddc3e2652f2b747.png)


The **dot product** of ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![Rendered by QuickLaTeX.com \[ \vec{a} \cdot \vec{b} = |\vec{a}| |\vec{b}| cos\theta \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-fce96a729e575b92fad0c0a45cc9cb38_l3.png)


Another way of calculating the dot product is adding together the component-wise products. If ![Rendered by QuickLaTeX.com \vec{a} = (a_x, a_y, a_z)](../../assets/5272747c8354d8fb.png)

![Rendered by QuickLaTeX.com \vec{b} = (b_x, b_y, b_z)](../../assets/575f4cedc82eaf85.png)


![Rendered by QuickLaTeX.com \[ \vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f002ec6095d4bae621561b9d7ca32d5d_l3.png)


A follow-up to the alternate formula above is the formula for vector magnitude. The magnitude of a vector is the square root of the dot product of the vector with itself:

![Rendered by QuickLaTeX.com \[ |\vec{a}| = \sqrt{a_x^2 + a_y^2 + a_z^2} = \sqrt{\vec{a} \cdot \vec{a}} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9b2868731ce0226592bca63a0d3f2800_l3.png)


The geometric meaning of the dot product ![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

**scaled** by ![Rendered by QuickLaTeX.com |\vec{b}|](../../assets/6c9c66378bfafe65.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b} = \vec{b} \cdot \vec{a}](../../assets/1be1d048d3c30158.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com |\vec{a}|](../../assets/6bb8162f1ac628f1.png)


So if you want to get the magnitude of the projection of ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \[ |proj(\vec{a}, \vec{b})| = \dfrac{\vec{a} \cdot \vec{b}}{|\vec{b}|} = |\vec{a}| cos\theta \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-0994fb9878031c38f8649e53e12dfe7d_l3.png)


To get the actual projected vector of ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \hat{b}](../../assets/58bee34f605ebb65.png)


![Rendered by QuickLaTeX.com \[ proj(\vec{a}, \vec{b}) = (\dfrac{\vec{a} \cdot \vec{b}}{|\vec{b}|}) \hat{b} = (\dfrac{\vec{a} \cdot \vec{b}}{{|\vec{b}|}^2}) \vec{b} = (\dfrac{\vec{a} \cdot \vec{b}}{\vec{b} \cdot \vec{b}}) \vec{b} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2cdfe25f6a724f5263407643823dc8f3_l3.png)


One important property of dot product ![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \theta < 90^\circ](../../assets/ad53f64465aed90a.png)

![Rendered by QuickLaTeX.com \theta = 90^\circ](../../assets/93ae3a6bf40f9580.png)

![Rendered by QuickLaTeX.com \theta > 90^\circ](../../assets/ccaf0fcb3d310564.png)


For the dot product of two unit vectors, like ![Rendered by QuickLaTeX.com \hat{a} \cdot \hat{b}](../../assets/6f1cd1e5fcb321ad.png)

![Rendered by QuickLaTeX.com cos\theta](../../assets/66a71893e695946f.png)

![Rendered by QuickLaTeX.com \theta = 0^\circ](../../assets/a5168f2f8ecb70c2.png)

![Rendered by QuickLaTeX.com \theta = 180^\circ](../../assets/aeaad8051ab76bf3.png)


Let’s say we have three vectors: ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \hat{a} \cdot \hat{b}](../../assets/6f1cd1e5fcb321ad.png)

![Rendered by QuickLaTeX.com \hat{a} \cdot \hat{c}](../../assets/a7cbfb976494ae16.png)

![Rendered by QuickLaTeX.com \hat{a}](../../assets/39a12ef2cb154ed3.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)


A metric often used to measure the difference between two data objects is the [root mean square error](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSE) which is the square root of the average of component-wise errors. For vectors, that means:

![Rendered by QuickLaTeX.com \[ RMSE(\vec{a}, \vec{b}) = \sqrt{\frac{1}{3}((a_x - b_x)^2 + (a_y - b_y)^2 + (a_z - b_z)^2)} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-635b8f32450bf0c5c27410241a9c351f_l3.png)


It kind of makes sense, because it is exactly the magnitude of the vector that is the difference between ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \frac{1}{\sqrt{3}}](../../assets/2cc8224cb5f52914.png)


![Rendered by QuickLaTeX.com \[ RMSE(\vec{a}, \vec{b}) = (\dfrac{1}{\sqrt{3}})\sqrt{(a_x - b_x)^2 + (a_y - b_y)^2 + (a_z - b_z)^2} = (\dfrac{1}{\sqrt{3}}) |\vec{a} - \vec{b}| \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f01e9df13bcfeed19b0e82259fad0d42_l3.png)


It’s also the square root of the dot product of the difference vector ![Rendered by QuickLaTeX.com \vec{a} - \vec{b}](../../assets/05689cf4d377b43d.png)

![Rendered by QuickLaTeX.com \frac{1}{\sqrt{3}}](../../assets/2cc8224cb5f52914.png)


![Rendered by QuickLaTeX.com \[ RMSE(\vec{a}, \vec{b}) = (\dfrac{1}{\sqrt{3}}) |\vec{a} - \vec{b}| = (\dfrac{1}{\sqrt{3}}) \sqrt{(\vec{a} - \vec{b}) \cdot (\vec{a} - \vec{b})} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-510f0d67d0113a58be8c87d60b4e8345_l3.png)


Here’s an important property of projection:

The projection of a vector ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

**minimal RMSE** with respect to ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com proj(\vec{a}, \vec{b})](../../assets/c7644fd5193ecc8e.png)

**the best scaled version of to approximate **.![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

Also note that if ![Rendered by QuickLaTeX.com \hat{a} \cdot \hat{b}](../../assets/6f1cd1e5fcb321ad.png)

![Rendered by QuickLaTeX.com \hat{a} \cdot \hat{c}](../../assets/a7cbfb976494ae16.png)

![Rendered by QuickLaTeX.com \hat{b}](../../assets/58bee34f605ebb65.png)

![Rendered by QuickLaTeX.com \hat{c}](../../assets/f4c1e87311e319e8.png)

![Rendered by QuickLaTeX.com \hat{a}](../../assets/39a12ef2cb154ed3.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)


Now we’re finished with vectors. It’s time to move onto curves.

### “Projecting” a Curve onto Another

Let’s consider these three curves:

![Rendered by QuickLaTeX.com \begin{flalign*} y &= f(t) = t^2 \\ y &= g(t) = 2(t - \frac{1}{2})^2 \\ y &= h(t) = -t^3 \\ \end{flalign*}](../../assets/c359a5553e862358.png)


When working with curves, as opposed to vectors, we need to additionally specify an interval of of interest. For simplicity, we will consider ![Rendered by QuickLaTeX.com 0 \leq t \leq 1](../../assets/294c1cb95774dc20.png)


Below is a figure showing what they look like side-by-side within our interval of interest:

![curves](../../assets/fde28f98bfa98d58.png)


Just like vectors, “projecting” a curve ![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)


Recall that the dot product of vectors is equal to the sum of component-wise products:

![Rendered by QuickLaTeX.com \[ \vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f002ec6095d4bae621561b9d7ca32d5d_l3.png)


Mirroring that, let’s sum up the products of samples of curves at regular intervals, and we normalize the sum by dividing it with the number of samples, so we don’t get drastically different results due to different number of samples. If we take 10 samples between ![Rendered by QuickLaTeX.com 0 \leq t \leq 1](../../assets/294c1cb95774dc20.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)


![Rendered by QuickLaTeX.com \[ f(t) \cdot g(t) = \frac{1}{10} \sum_{i = 1}^{10} f(\frac{i}{10}) g(\frac{i}{10}) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-100eaf5f9c6d8e9ce8689bd418bc6074_l3.png)


The more samples we use, the more accuracy we get. What if we take an infinite number of samples so we get the most accurate result possible?

![Rendered by QuickLaTeX.com \[ f(t) \cdot g(t) = \lim_{n\to\infty} {\frac{1}{n} \sum_{i = 0}^{n} f(\frac{i}{n}) g(\frac{i}{n}}) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1edc237fbff9c4c6f05c3ba0ab93c942_l3.png)


This basically turns into an integral:

![Rendered by QuickLaTeX.com \[ f(t) \cdot g(t) = \int_{0}^{1} f(t) g(t) dt \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7cc0947943625acb1c6243795ebb2f4d_l3.png)


So there we have it, one common definition of the “dot product” of two curves:

**The integral of the product of two curves over the interval of interest**.

Copying the formula from vectors, the RMSE between two curves ![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)


![Rendered by QuickLaTeX.com \[ RMSE(f(t), g(t)) = \sqrt{(f(t) - g(t)) \cdot (f(t) - g(t))} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-938c3509c36bf5c93b3ff3b3d6bbbe73_l3.png)


In integral form, it becomes:

![Rendered by QuickLaTeX.com \[ RMSE(f(t), g(t)) = \sqrt{\int_{0}^{1} (f(t) - g(t))^2 dt} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b34918303a077278b25ca535ef38086b_l3.png)


The “mean” part of the error is omitted since it’s a division by 1, the length of our interval of interest.

To find out which one of the “normalized” version of ![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com h(t)](../../assets/066fdea2131aecdd.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \hat{f}(t) &= \dfrac{f(t)}{|f(t)|} = \dfrac{f(t)}{\sqrt{f(t) \cdot f(t)}} = \sqrt{5}t^2 \\ \hat{g}(t) &= \dfrac{g(t)}{|g(t)|} = \dfrac{g(t)}{\sqrt{g(t) \cdot g(t)}} = 4 \sqrt{5} (t - \dfrac{1}{2})^2 \\ \hat{h}(t) &= \dfrac{h(t)}{|h(t)|} = \dfrac{f(t)}{\sqrt{h(t) \cdot h(t)}} = -\sqrt{7}t^3 \\ \hat{f}(t) \cdot \hat{g}(t) &= \int_{0}^{1} \hat{f}(t) \hat{g}(t) dt = \dfrac{4}{3} \\ \hat{f}(t) \cdot \hat{h}(t) &= \int_{0}^{1} \hat{f}(t) \hat{h}(t) dt = \dfrac{-\sqrt{35}}{6} \\ \end{flalign*}](../../assets/873f735ebbc07551.png)


The dot product of ![Rendered by QuickLaTeX.com \hat{f}(t)](../../assets/9dcae5828c563925.png)

![Rendered by QuickLaTeX.com \hat{g}(t)](../../assets/9a3de734a08e1b8e.png)

![Rendered by QuickLaTeX.com \hat{f}(t)](../../assets/9dcae5828c563925.png)

![Rendered by QuickLaTeX.com \hat{h}(t)](../../assets/ad6b6415c2fc9363.png)

![Rendered by QuickLaTeX.com \hat{g}(t)](../../assets/9a3de734a08e1b8e.png)

![Rendered by QuickLaTeX.com \hat{h}(t)](../../assets/ad6b6415c2fc9363.png)

![Rendered by QuickLaTeX.com \hat{f}(t)](../../assets/9dcae5828c563925.png)


Drawing analogy from vectors, ![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com h(t)](../../assets/066fdea2131aecdd.png)


Now let’s try finding the best scaled version of ![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)


![Rendered by QuickLaTeX.com \[ proj(f(t), g(t)) = \dfrac{f(t) \cdot g(t)}{g(t) \cdot g(t)} g(t) = \dfrac{4}{3} g(t) = \dfrac{8}{3} (t - \dfrac{1}{2})^2 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b164295bee187bc0c7a4fc2919d59749_l3.png)


And this is what ![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com proj(f(t), g(t))](../../assets/45d7cc069d2dd977.png)


![curve projection](../../assets/f34b1351a4b5566b.png)


The projected curve ![Rendered by QuickLaTeX.com proj(f(t), g(t))](../../assets/45d7cc069d2dd977.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com g(t)](../../assets/25c167816ee70f0c.png)

![Rendered by QuickLaTeX.com f(t)](../../assets/c9e425652e66e402.png)


Now that you know how to “project” a curve onto another, we will see how to approximate a curve with multiple simpler curves while maintaining minimal error.

Great article! Applying linear algebra techniques for function was very clever idea. Now I can see how it is really related to the Fourier transform. Can’t wait to see next part 🙂