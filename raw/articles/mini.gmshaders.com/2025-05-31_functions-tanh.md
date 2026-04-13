---
title: 'Functions: Tanh'
url: https://mini.gmshaders.com/p/func-tanh
author: Xor
published: '2025-05-31'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Functions: Tanh

### An introduction to the hyperbolic tangent function and how to use it

Welcome back!

[Mini tutorials](https://mini.gmshaders.com/p/design-choices) are back! These will cover a wide range of topics in bite-sized pieces, and I’ll start with some GLSL functions. This series will explain the math behind the functions and how they can be used.

Today is all about the Hyperbolic Tangent. “`tanh`

”, which you may have seen cropping up in several of [my tweet shaders](https://x.com/XorDev/status/1928504290290635042) lately. We’ll cover the math background, how to write your own, its uses, alternatives, and performance considerations.

# Uses

The [domain](https://mini.gmshaders.com/p/readingmath) of `tanh`

(x) is (-∞, +∞) and the range is (-1, +1). This means you can input any value (between negative infinity and positive infinity), and it will map to a value between -1 and +1. Large values of “x” quickly approach an output of 1.0, and negatives approach -1.0, so this function allows you to take values from an unpredictable range and smoothly map them to the normalized (-1, +1) range. Tanh can be thought of as an unbounded [smoothstep](https://gmshaders.com/glossary/?load=smoothstep) function (I’ll have to cover that function later). It smoothly starts and stops without definite endpoints.

From here, you can shift (by adding to the input), scale the smoothness of the curve by multiplying the input and the spread of the output, by multiplying the function.

Here are some of the places where it is often used.

**Smooth blending**: If you need to blend between colors without a definite starting or ending point, you can use tanh! For example, you might use:`mix(col_a, col_b, tanh(x * SPREAD) * 0.5 + 0.5)`

It could also be used for smoothly blending between two shapes or starting and stopping an animation, for example. Anything that needs to be blended without definite endpoints could use tanh!**Tonemapping**: I often use tanh as a way of normalizing my color values in my tweet shaders. It’s a conveniently short tonemapping function that is easy to plug in without altering the code much. It’s not the[best out there](https://mini.gmshaders.com/p/tonemaps), but it’s a pretty decent option and relatively cheap.**Debugging**: I like to use tanh to visualize variables because it works with any domain and brings it to a predictable range. If I seem to be getting values outside of the expected range, I can use tanh to see what these values are and still spot relative differences (higher values still have brighter outputs)**Neural Network activations**: tanh is sometimes used for bounded outputs in Generative Adversarial Networks activation functions, allowing for weights of any domain to be compressed to a usable range.

`tanh`

(x) was not implemented until GLSL 1.30, so in GameMaker and WebGL 1.0, you’ll need to implement this manually. I’ll write how to implement this yourself and about more alternative functions later.

# Math Background

Let’s look at 3 different mathematical ways to interpret the hyperbolic tangent to give a wider context for a variety of readers. Don’t worry if you’re unfamiliar with some of the terms here! It’s still quite useful to understand how this relates to other math concepts, and you can let the details fill in naturally over time later.

### Sigmoid Curve

A sigmoid is a symmetrical “S” curve. [There are several](https://en.wikipedia.org/wiki/Sigmoid_function#Examples) types of sigmoid functions with different ranges. Some range from 0 to 1, while others range from -1 to +1, but they are all symmetrical (rotating 180° around the center point). `tanh`

(x) is a common sigmoid that is supported in many programming languages, optimized and convenient with the [-1, +1] range.

### Trigonometry

The hyperbolic tangent can be understood as an x / y ratio similar to the regular tangent function. With `tan`

(Θ), you are finding the x / y ratio (or slope) of a point on a unit circle. x = `cos`

(Θ) and y = `sin`

(Θ), so the tangent, ratio is cos(Θ) / sin(Θ).

The hyperbolic tangent is the same, but mapped to a [unit hyperbola](https://en.wikipedia.org/wiki/Unit_hyperbola) instead of a circle:

Intuitively, there are hyperbolic sin and cos functions: `sinh`

, `cosh`

:

You might be asking, What is a [hyperbola](https://en.wikipedia.org/wiki/Hyperbola)? The short answer is that it is the intersection slice of a double cone. Here’s an illustration of what I mean:

The mathematical rabbit hole runs deep here, so I’ll leave the rest for you to explore if you feel compelled to do so. Let’s look at one more approach!

### Exponentials

We can also interpret it with exponential curves! The difference of positive and negative exponentials divided by the sum of positive and negative exponentials:

When fully reduced, it can be computed and implemented with just one exponential:

```
//Hyperbolic Tangent
float tanh(float x)
{
float exp_neg_2x = exp(-2.0 * x);
return -1.0 + 2.0 / (1.0 + exp_neg_2x);
}
```



This is how it can be implemented in older versions of GLSL or languages where the tanh function is not implemented. Next, let’s compare this to some other options.

# Alternatives

This section and the next (on performance) will be reserved for my paid supporters!