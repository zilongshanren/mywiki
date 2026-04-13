---
title: How to generate Gaussian distributed numbers - Alan Zucconi
url: https://www.alanzucconi.com/2015/09/16/how-to-sample-from-a-gaussian-distribution/
author: Alan Zucconi
published: '2015-09-16'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In a [previous post](https://www.alanzucconi.com/2015/09/09/understanding-the-gaussian-distribution/) I’ve introduced the Gaussian distribution and how it is commonly found in the vast majority of natural phenomenon. It can be used to dramatically improve some aspect of your game, such as procedural terrain generation, enemy health and attack power, etc. Despite being so ubiquitous, very few gaming frameworks offer functions to generate numbers which follow such distribution. Unity developers, for instance, heavily rely on `Random.Range`

which generates uniformly distributed numbers (in blue). This post will show how to generate Gaussian distributed numbers (in red) in C#.

![gvu](../../assets/1530504dea74d6d2.png)

I’ll be explaining the Maths behind it, but there is no need to understand it to use the function correctly. You can download the `RandomGaussian`

Unity script [here](https://www.patreon.com/posts/3331323).

### Step 1: From Gaussian to uniform

Many gaming frameworks only include functions to generate continuous uniformly distributed numbers. In the case of Unity3D, for instance, we have `Random.Range(min, max)`

which samples a random number from `min`

and `max`

. The problem is to create a Gaussian distributed variable out of a uniformly distributed one.

#### Sample two Gaussian distributed values

![Gaussian - Copy - Copy](../../assets/e81ccd1fc5e6d703.png)

Let’s imagine we already have two independent, normally distributed variables:

![Rendered by QuickLaTeX.com \[X \sim \mathcal{N} \left(0,1 \right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d284f3e30bc88400fb3b62afd4d9075a_l3.png)


![Rendered by QuickLaTeX.com \[Y \sim \mathcal{N} \left(0,1\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-bc3edb979a837391218d384403f9139f_l3.png)


from which we sampled two values, ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com y](../../assets/6cc181d8f36d0fd4.png)

![Rendered by QuickLaTeX.com (0,0)](../../assets/28bca627b65f648f.png)


#### Calculate their joint probability

![Gaussian - Copy - Copy (2)](../../assets/6c30d186462b450f.png)

The probability of having a certain ![Rendered by QuickLaTeX.com (x,y)](../../assets/82b05d4346325097.png)

![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com y](../../assets/6cc181d8f36d0fd4.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

*joint probability* and since samplings from ![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)


![Rendered by QuickLaTeX.com \[P(x,y) = P(x)P(y) =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e133e0a946c8bad9e4adb4674d2f6a21_l3.png)


![Rendered by QuickLaTeX.com \[ =\frac{1}{\sqrt{2\pi }}e^{-{\frac{x^2}{2}}}\frac{1}{\sqrt{2\pi }}e^{-{\frac{y^2}{2}}} =\frac{1}{2\pi}e^{-{\frac{x^2+y^2}{2}}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-709d6e50f624ef816ddcaee2bbb5be64_l3.png)


#### Switch to polar coordinates

The point ![Rendered by QuickLaTeX.com (x,y)](../../assets/82b05d4346325097.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


![Gaussian - Copy](../../assets/8f58f715d8006967.png)

![Rendered by QuickLaTeX.com \[R=\sqrt{x^2+y^2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5a7cc40af5e54ad512d032c53e7a71f5_l3.png)


![Rendered by QuickLaTeX.com \[\theta=arctan\left (\frac{y}{x}\right )\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-bb2086cd8f5e4520722aeac84a753dd1_l3.png)


Now the original point ![Rendered by QuickLaTeX.com (x,y)](../../assets/82b05d4346325097.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![Rendered by QuickLaTeX.com \[x = R cos\left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-eeb2d380b7cb197da853971ecd257b2e_l3.png)


![Rendered by QuickLaTeX.com \[y = R sin\left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-3bc8b8a5c8f6dc341cab2100160a49e0_l3.png)


#### Rewrite the joint probability

We can now rewrite the joint probability ![Rendered by QuickLaTeX.com P(x,y)](../../assets/1abcaec4271b403a.png)


![Rendered by QuickLaTeX.com \[\frac{1}{2\pi }e^{-{\frac{x^2+y^2}{2}}}=\frac{1}{2\pi}e^{-{\frac{R^2}{2}}}=\left (\frac{1}{2\pi } \right )\left (e^{-{\frac{R^2}{2}}} \right )\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8149276347ff7a756af09e5f2c224031_l3.png)


which is the product of the two probability distributions:

![Rendered by QuickLaTeX.com \[R^2 \sim Exp\left(\frac{1}{2}\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-70c85b963573f710d34e69efc0edfb8c_l3.png)


![Rendered by QuickLaTeX.com \[\theta \sim Unif(0,2\pi) = 2\pi Unif(0,1)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5ad0166fedf6ab6e860843676033236a_l3.png)


#### Expanding the exponential distribution

While ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com R^2](../../assets/38335e811ff3d07b.png)

[exponential distribution](https://en.wikipedia.org/wiki/Exponential_distribution):

![Rendered by QuickLaTeX.com \[Exp(\lambda)=\frac{-log(Unif(0,1))}{\lambda}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8fb84c0fd163f9d8b9aef868c520237b_l3.png)


![Rendered by QuickLaTeX.com \[R \sim \sqrt{-2log\left( Unif(0,1)\right)}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-040455d3657ecd4eab573451c4e189a0_l3.png)


Now both ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


### Step 2: From uniform to Gaussian

We can now reverse the procedure done in **Step 1** to derive a simple algorithm:

- Generate two random numbers
![Rendered by QuickLaTeX.com u_1,u_2 \sim Unif(0,1)](../../assets/1efc02c56b0f8b22.png)

- Use them to create the radius

and the angle ![Rendered by QuickLaTeX.com \theta = 2\pi u_2](../../assets/04f51ebd3ea5983d.png)

- Convert

from polar to Cartesian coordinates: ![Rendered by QuickLaTeX.com (R cos\theta, R sin\theta)](../../assets/f129cb492e28ffdb.png)


This is know as the [Box-Muller transform](https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform). The image below (from Wikipedia) shows how the uniformly distributed points from the unit square are re-mapped by the Box-Muller transform onto the Cartesian plane, in a Gaussian fashion.

![Box-Muller_transform_visualisation.svg](../../assets/2e67969f6efeca9f.png)

### Step 3: The Marsaglia polar method

The Box-Muller transform has a problem: it uses trigonometric functions which are notoriously slow. To avoid that, a slightly different technique exists, called the [Marsaglia polar method](https://en.wikipedia.org/wiki/Marsaglia_polar_method). Despite being similar, it stars from an uniformly distributed point in the interval ![Rendered by QuickLaTeX.com (-1,+1)](../../assets/26d880cecf22bc3a.png)

![Rendered by QuickLaTeX.com (0,0)](../../assets/28bca627b65f648f.png)


public static float NextGaussian() { float v1, v2, s; do { v1 = 2.0f * Random.Range(0f,1f) - 1.0f; v2 = 2.0f * Random.Range(0f,1f) - 1.0f; s = v1 * v1 + v2 * v2; } while (s >= 1.0f || s == 0f); s = Mathf.Sqrt((-2.0f * Mathf.Log(s)) / s); return v1 * s; }

Approximately 21% of the points will be rejected with this method.

### Step 4: Mapping to arbitrary Gaussian curves

The algorithm described in **Step 3** provides a way to sample from ![Rendered by QuickLaTeX.com \mathcal{N} \left(0,1 \right)](../../assets/2ce003a748bf9d91.png)

![Rendered by QuickLaTeX.com \mathcal{N} \left(\mu,\sigma^2 \right)](../../assets/11f9daecf9fa861a.png)


public static float NextGaussian(float mean, float standard_deviation) { return mean + NextGaussian() * standard_deviation; }

![Gaussianb](../../assets/996c4b5e79ba2a30.png)

There is yet another problem: Gaussian distributions have the nasty habit to generate numbers which can be quite far from the mean. However, clamping a Gaussian variable between a `min`

and a `max`

can have quite catastrophic results. The risk is to squash the left and right tails and having a rather bizarre function with three very likely values: the mean, the min and the max. The most common technique to avoid this is to take another sample if it falls outside its range:

public static float NextGaussian (float mean, float standard_deviation, float min, float max) { float x; do { x = NextGaussian(mean, standard_deviation); } while (x < min || x > max); retun x; }

Another [solution](http://stackoverflow.com/questions/1303368/how-to-generate-normally-distributed-random-from-an-integer-range/1303512#1303512) changes the parameter of the curve so that `min`

and `max`

are at 3.5 standard deviations from the mean (which *should* contain more than 99.9% of the sampled points).

### 📚 Recommended Books

## Conclusion

This tutorial shows how to sample Gaussian distributed numbers starting from uniformly distributed ones. You can download the complete `RandomGaussian`

script for Unity [here](https://www.patreon.com/posts/3331323).

#### Other resources

[Probability and Games: Damage Rolls](http://www.redblobgames.com/articles/probability/damage-rolls.html): a very detailed explanation of how dices can be used to sample from different distributions;[ProjectRhea](https://www.projectrhea.org/rhea/index.php/The_principles_for_how_to_generate_random_samples_from_a_Gaussian_distribution): the principle of how to generate a Gaussian random variable;[Sampling From the Normal Distribution](https://theclevermachine.wordpress.com/2012/09/11/sampling-from-the-normal-distribution-using-the-box-muller-transform/): a similar tutorial;[Box-Muller transforms](http://www.flyingcoloursmaths.co.uk/an-insight-into-the-mathematical-mind-box-muller-transforms/): a more Maths-y tutorial.

**Part 1**:[Understanding the Gaussian distribution](https://www.alanzucconi.com/2015/09/09/understanding-the-gaussian-distribution/)**Part 2**: How to generate Gaussian distributed numbers

## Leave a Reply Cancel reply