---
title: Using JAX, numpy, and optimization techniques to improve separable image filters
url: https://bartwronski.com/2020/03/15/using-jax-numpy-and-optimization-techniques-to-improve-separable-image-filters/
published: '2020-03-15'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

![](../../assets/1a06187f94f89e08.jpg)

**left**) through an offline optimization process to get the results on the

**right**.

In today’s blog post I will look at two topics: how to use [JAX ](https://github.com/google/jax)(“hyped” new Python ML / autodifferentiation library), and a basic application that is follow-up to [my previous blog post ](https://bartwronski.com/2020/02/03/separate-your-filters-svd-and-low-rank-approximation-of-image-filters/)on using SVD for low-rank approximations and separable image filters – we will look at “optimizing” the filters to **improve **the filtered images.

My original motivation was to play a bit with JAX and see if it will be useful for me, and I immediately had this very simple use-case in mind. The blog post is not intended to be a comprehensive guide / tutorial to JAX, nor a complete optimization primer (one can spend **decades **studying and researching this topic), but a fun example application – hopefully immediately useful, and inspiring for other graphics or image processing folks.

The post is written as separate chapters/sections (problem statement, some basic theory and challenges, practical application, and the results) – feel free to skip ones that seem obvious to you. 🙂

[This post comes with a colab ](https://colab.research.google.com/github/bartwronski/BlogPostsExtraMaterial/blob/master/optimization_for_separable_filters.ipynb)that you can run and modify yourself. The code is not very clean, mostly scratchpad quality, but I decided that it’s still good for the others if I share it, no matter how poorly it reflects on my coding habits.

## Recap of the problem – separable filters

In the last blog post, we have looked at analyzing if convolutional image filters can be made separable, and if not, finding separable approximations (as a sum of N separable filters). For this we used [Singular Value Decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition) and using a low rank approximation by taking first N singular values.

We have found that to approximate a 50×50 circular filter (can be though of as a circular bokeh), one needs ~13 separable passes over the whole image, and even 8 singular components (that have extremely low numerical error) can produce **distracting, unpleasant visual artifacts** – negative values cause “ringing”, and some “leftover” corner errors.

![](../../assets/2e044b4ddb2f2e76.jpg)

I have suggested that this can be solved with optimization, and in this post I will describe most likely the simplest method to do so!

**Side note:** After my blog post, I had a chat with a colleague of mine, [Soufiane Khiat ](https://twitter.com/soufianekhiat?lang=en)– we used to work together at Ubisoft Montreal – and given his mathematical background much better than mine, he had some cool insights on this problem. One of suggestions was to use [singular value thresholding algorithm ](https://arxiv.org/abs/0810.3286)and some [proximal methods ](https://en.wikipedia.org/wiki/Proximal_gradient_method)and generally it is probably the way to go for the specific problem – but a bit of against “educational” goal of my blog posts (and staying as general as possible). I still recommend reading about this approach if you want to go much deeper into the topic and again – thanks Soufiane for a great discussion.

## What is optimization?

Optimization is a loaded term and quite likely I am going to use it in a way you didn’t expect! Most graphics folks understand it as in “low level optimization” (or algorithmic optimization), aka optimizing the computational cost – memory, CPU/GPU usage, total timing spent on computations – and this is how I used to think of term “optimization” for many years.

But this is not the kind of optimization that a mathematician, or most academics think of and not the topic of my blog post!

[Optimization ](https://en.wikipedia.org/wiki/Mathematical_optimization)that I will use is the one in which you have some function that depends on a set of parameters, and your goal is to find the set of parameters that achieves a certain goal, usually minimum (sometimes maximum, but they can be equivalent in most cases) over this function. This definition is **very **general – and in theory it even covers also computational performance optimizations (we are looking for a set of computer program instructions that optimizes performance while not diverging from the desired output).

Optimization of arbitrary functions is generally a [NP-hard problem ](https://en.wikipedia.org/wiki/NP-hardness)(there are no solutions other than exploring every possible value, which is impossible in the case of continuous functions), but under some constraints like [convexity](https://en.wikipedia.org/wiki/Convex_optimization), or looking for [local minima](https://en.wikipedia.org/wiki/Local_search_(optimization)), it can be made feasible, and relatively robust and fast – and is basis of modern convolutional neural networks, and algorithms like gradient descent.

This post will skip explaining the [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent). If it’s a new or vague concept for you, I don’t recommend just trusting me 🙂 – so if you would like to get a good basic, but intuitive and visual understanding, be sure to check [this fantastic video from Grant Sanderson ](https://www.youtube.com/watch?v=IHZwWFHWa-w)on the topic.

## What is JAX?

[JAX ](https://github.com/google/jax)is a new ML library that supports auto-differentiation and just-in-time compilation targeting CPUs, GPUs, and TPUs.

JAX got very popular recently (might be a sampling bias, but seemed to me like half of ML twitter was talking about it), and I am usually very skeptical about such new hype bandwagons. But I was also not very happy with my previous options, so I tried it, and I think it is popular for a few good reasons:

- It is extremely lean, in the most basic form it is a “replacement” import for numpy.
- Auto-differentiation “just works” (without any gradient tapes, graphs etc.) over most of numpy and Python constructs like loops, conditionals etc.
- There are higher level constructs developed on top of it – like NNs and other ML infrastructure, but you can still use the low-level constructs.
- There is no more weird array reshaping and expressing everything over batches, constantly thinking about shapes and dimensions. If you want to process a batch, just use functions that map your single-example functions over batches.
- It is actively developed both by open-source, as well as some Google and DeepMind developers, and available right at your fingers with
[Colab](https://colab.research.google.com/)– zero installation needed.

I have played with it for just a few days, but definitely can recommend it and it will become my go-to auto-diff / optimization library for Python.

## Optimization 101 – defining a loss function

This might seem obvious, but before we can start optimizing an objective, we have to define it in some way that is understandable for the computer and optimizeable.

What is non-obvious is that **coming up with a decent objective function is the biggest challenge of machine learning**, IMO a much bigger problem than any particular choice of a technique. (Note: it also has much wider implications than our toy problems; ill-defined objectives can lead to catastrophes in wider social context, e.g. optimizing for engagement time leads to clickbaits, low quality filler content, and fake news).

For our problem – optimizing filters, we know three things that we want to optimize for:

- Maintain the low rank of the filter,
- Keep the separable filter similar to the original one,
- Avoid the visual artifacts.

The first one is the simple – we don’t have much wiggle room there. We have a hard limit on maximum of N separable passes and fixed number of coefficients. But on the other hand, the two other goals are not well defined.

The “similarity” that we are looking for can be anything – average squared error, average absolute error, maximum error, some perceptual/visual similarity… Anything else, or even any combination of the above. Mathematically, we use term of distance, or [metric](https://en.wikipedia.org/wiki/Metric_(mathematics)). Convenient and well researched are metrics that are based on [p-norm ](https://en.wikipedia.org/wiki/Norm_(mathematics)#p-norm)and mathematicians like to operate on squared Euclidean distance ([L2 norm](https://en.wikipedia.org/wiki/Lp_space#The_p-norm_in_finite_dimensions)), so average squared errors. Average squared error is so often used as it usually has a simple, closed form solutions like [linear least squares](https://en.wikipedia.org/wiki/Linear_least_squares), linear regression, [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis)), but in many cases it might not be the right loss. Defining **perceptual similarity **is the most difficult and is an **open problem **in computer vision, with the recent universal approach of using [similarity features extracted by neural networks ](https://arxiv.org/abs/1603.08155)for the purpose of image recognition.

The third one “avoid the visual artifacts” is even more difficult to define, as we are talking about artifacts that are present in the final image, and not about numerical error in the approximated filter. Deciding on components of the loss function to avoid visual artifacts and tuning them is often the most time consuming part of optimization and machine learning.

![](../../assets/0e6cc277feaab05e.png)

**Left:**original filter,

**right:**rank 4 approximation. Notice the negative values (blue color) and some leftover “garbage” values in the corners. Those will contribute to visual artifacts.

Looking at artifacts in the filtered images I think that the two most objectionable ones are: negative values causing [ringing](https://en.wikipedia.org/wiki/Ringing_artifacts), and some “garbage” pixels in the corners of the filter.

## Putting it together – target loss function for optimizing separable image filters

Given all that together, I decided on minimizing a loss function that will sum three terms:

- Squared mean error term,
- Heavily penalizing any negative elements in the approximated filter,
- Additional penalty when a zero element of the original filter becomes non-zero after the approximation.

This is a very common approach – summing together multiple different terms with different meanings and finding the parameters that optimize such a sum. Open challenge is tuning the weights of the different components of the loss function, a further section will show the impact of it.

This loss function might not be the best one, but this is what makes such problems fun – often designing a better loss (closer corresponding to our intentions) can lead to significantly better results without changing the algorithm at all! This was one of my huge surprises – so many great papers just propose simple optimization framework together with an improved loss function to advance state of the art significantly.

Also if you think that it is quite **“ad-hoc”** – yes, it is! Most academic papers (and productionized code…) have such ad-hoc loss functions where each component might have some good motivation, but they end up with a hodge-podge that doesn’t make too much sense when put together, but empirically works (often verified by ablation studies).

In numpy, an example implementation of the loss function might look like:

```
def loss(target, evaluated_filter):
l2_term = L2_WEIGHT * np.mean(np.square(evaluated_filter - target))
non_negative_term = NON_NEGATIVE_WEIGHT * np.mean(-np.minimum(evaluated_filter, 0.0))
keep_zeros_term = KEEP_ZEROS_WEIGHT * np.mean((target == 0.0) * np.abs(evaluated_filter))
return l2_term + non_negative_term + keep_zeros_term
```

Now that we have a loss function to optimize, we need to find parameters that minimize it. This is where things can become difficult. If we want to have rank 4 approximation of a 50×50 filter, we end up with 4*(50*2) == **400 parameters**. If we wanted to do a brute force search in this 400 dimensional space, this could take a very long time! Let’s say we just wanted to evaluate 10 different potential values – this would take 10^400 loss function evaluations – and this is quite a toy problem!

Luckily, we are in a situation where our **initial guess **obtained through SVD is already **kind of ok**, and we want to just improve it. This is a classic assumption of “local optimization” and can be achieved through greedily minimizing the error, for example by coordinate descent, or even better gradient descent – going in the direction where the error is decreasing the most. In a general scenario we don’t get any theoretical guarantees of finding the true, best solution, but we are guaranteed that we will get **a solution that will be better or at worst the same** when compared to the initial one (according to our loss function).

## Gradient descent in JAX

How do we compute the gradient of our loss function? For the function that I wrote it is relatively simple and follows calculus 101, but anytime we would change it, we need to re-derive our gradient… Wouldn’t it be great if we could compute it automatically?

This is where various [auto-differentiation ](https://en.wikipedia.org/wiki/Automatic_differentiation)libraries can help us. Given some function, we can compute its gradient / derivative with regards to some variables completely automatically! This can be achieved either symbolically, or in some cases even numerically if closed-form gradient would be impossible to compute.

In C++ you can use [Ceres](http://ceres-solver.org/) (I highly recommend it; its templates can be non-obvious at first, but once you understand the basics, it’s really powerful and fast), in Python one of many frameworks, from smaller ones like [Autograd](https://github.com/hips/autograd) to huge ones like [Tensorflow ](http://tensorflow.org/)or [PyTorch](https://pytorch.org/). Compared to tf and pt, I wanted something lower level, simpler, and more convenient to use (setting up a graph or gradient tapes is not great 😦 ) – and JAX fills my requirements perfectly.

JAX can be a drop-in replacement to a combo of pure Python and numpy, keeping most of the functions exactly the same! In colab, you can import it either instead of numpy, or in addition to numpy. Here is code that computes our separable filter from list of separable vector pairs, and the loss function.

(note: I will paste some code here, but I highly encourage you to [open the colab that accompanies this blog post](https://colab.research.google.com/github/bartwronski/BlogPostsExtraMaterial/blob/master/optimization_for_separable_filters.ipynb) and explore it yourself.)

```
import numpy as np
import jax.numpy as jnp
# We just sum the outer tensor products.
# vs is a list of tuples - pairs of separable horizontal and vertical filters.
def model(vs):
dst = jnp.zeros((FILTER_SIZE, FILTER_SIZE))
for separable_pass in vs:
dst += jnp.outer(separable_pass[0], separable_pass[1])
return dst
# Our loss function.
def loss(vs, l2_weight, non_negativity_weight, keep_zeros_weight):
target = model(vs)
l2_term = l2_weight * jnp.mean(jnp.square(target- REF_SHAPE))
non_negative_term = non_negativity_weight * jnp.mean(-jnp.minimum(target, 0.0))
keep_zeros_term = keep_zeros_weight * np.mean((REF_SHAPE == 0.0) * jnp.abs(target))
return l2_term + non_negative_term + keep_zeros_term
```

Note how we mix some simple Python loops and logic in the model function, and numpy-like code (I could have imported jax.numpy as simply np, and you can do it if you want to, but to me such library shadowing feels a bit confusing).

Ok, but so far there is nothing interesting about it; I just kind of rewrote some numpy code as jax.numpy, what’s the big deal?

Now, the “magic” is that you compute the gradient of this function just by writing **jax.grad(loss)**! By default the gradient is wrt the first function parameter (you can change it if you want). [JAX has some limitations and gotchas](https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html) on what it can compute the gradient of and can require workarounds, but most of them feel quite “natural” (e.g. that PRNG requires explicit state) and I haven’t hit those in practice with my toy example.

Our whole gradient descent step function would look like:

```
def update_parameters_step(vs, learning_rate, l2_weight, non_negativity_weight, keep_zeros_weight):
grad_loss = jax.grad(loss)
grads = grad_loss(vs, l2_weight, non_negativity_weight, keep_zeros_weight)
return [(param[0] - learning_rate * grad[0], param[1] - learning_rate * grad[1]) for param, grad in zip(vs, grads)]
```

I was mind-blown how simple it is – no gradient tapes, no graph definitions requires. This is how auto-differentiation should look like from user’s perspective. 🙂 What is even cooler is that the resulting function code can be JIT-compiled to native code for orders of magnitude speed-up! You can place a decorator **@jax.jit** above your function, or manually create optimized function from **jax.jit(function)**. This makes it really fast and allows you to pick-and-choose what you jit (you can even unroll a few optimization iterations if you want).

## Tuning loss function term weights

Time to run an optimization loop on our loss function. I picked a learning_rate of *0.1* and *5000 *steps. Those are ad-hoc choices, step count is definitely an overkill, but it just worked and the optimization is pretty fast even on the CPU, so I didn’t bother tweaking them. The whole optimization looks like this:

```
# Our whole optimization loop.
def optimize_loop(vs, l2_weight, non_negativity_weight, keep_zeros_weight, print_loss):
NUM_STEPS = 5000
for n in range(NUM_STEPS):
vs = update_parameters_step(vs, learning_rate=0.1, l2_weight=l2_weight, non_negativity_weight=non_negativity_weight, keep_zeros_weight=keep_zeros_weight)
if print_loss and n % 1000 == 0:
print(loss(vs))
return vs
```

Finally we get to the problem of testing different loss function term weights. Luckily, because our problem is small, and jit’d optimization runs very fast, we can actually test it with a few different parameters.

One thing to note is that while we have 3 terms, in fact if we multiply all 3 of them by the same value, we will end up with loss function 3x bigger, but with the same parameters. So we have effectively just **2 degrees of freedom **and can keep one of the weights “frozen” – I will set the L2 mean loss as just 1.0 and operate on the weight for the non-negativity and keeping-zeros.

Without further ado, here are our **rank 4 separable circular filters **after the optimization:

![](../../assets/b3c54fe5c9090600.jpg)

**Left to right**: keep_zeros_weight of 0.0, 0.3, 0.8.

**Top to bottom**: non_negativity_weight of 0.0, 0.5, 1.5.

We can notice how those two loss terms affect the results and interact with each other. **Non-negativity** will very effectively reduce the negative ringing, but won’t address the artifacts in corners of the filter.

The extra **penalty of the zero terms becoming non-zero **nicely cleans up the corners, but there is still mild ringing around the radius of the filter.

**Both of them together** reduce all artifacts, but the final shape starts to deviate from our circle, becoming more like a sum of four separate box-filters (which is exactly what is happening)! So it is a trade-off of accuracy, filter shape, and the artifacts. There is no free lunch! 🙂

## Results when applied to an real image

Let’s look at the same filters when applied to the same image we have looked at in [my previous blog post](https://bartwronski.com/2020/02/03/separate-your-filters-svd-and-low-rank-approximation-of-image-filters/). **Note:** I have slightly boosted the gamma function from 7.0 to 8.0 as compared to my previous post to emphasize the visual error.

![](../../assets/d86eb1cb39bcf469.jpg)

**Left to right**: keep_zeros_weight of 0.0, 0.3, 0.8.

**Top to bottom**: non_negativity_weight of 0.0, 0.5, 1.5.

I highly encourage opening this image in a new tab and zooming in – otherwise the artifacts and differences are hard to notice.

When you zoom in, the difference in artifacts and overall appearance becomes quite obvious. I personally like the most the center picture, and the one below it. Column on the right minimized artifacts the most, especially the bottom-right example, but to me looks too *“blocky”*.

Can you design a better loss function and parameters for this problem? I am sure you can, feel free to play with the colab! 🙂

**Some random ideas** that can be fun to evaluate and get better understanding of how loss functions affect the results: penalizing zeros becoming non-zeros more as they get further away from the center, using L1 loss instead of L2 loss, playing with maximum allowed error, optimizing for computational performance by trying to create filter with explicitly zero weights that could get skipped in a shader.

## When such simple optimization through gradient descent is going to work?

While I mentioned that optimization is a whole field of mathematics and computer science and beyond scope of any simple blog, in my posts I usually try to give the readers some “intuition” about the topics I write about, and practical tips and tricks, so will mention a few gotchas regarding the optimization.

Gradient descent is so successful and ubiquitous technique (have you heard about this whole field of machine learning through artificial neural networks?!) because of few interesting properties:

First of all, in case of **multivariate functions**, we **don’t need to be strictly convex**! There might exist some path in the parameter space that gradient descent can use to “walk in the valleys and around the hills”.

![](../../assets/d25482665d721aab.jpg)

Second related observation is that the more dimensions we have, the easier it is to find some “good” solution (that might not be the total global minimum, but some almost-as good local minimum). **Over-completeness and over-parametrization is one of the things that makes very deep networks train well**. We are not looking for a single unique perfect solution, but one of many good ones, and the more parameters and dimensions there are, the more (combinatoricly explosive) combinations of parameters can be ok. Think about the example I have visualized above – in 1D we could never “walk around” a locally bad solution, the more dimensions we add, the more paths are there that can lead to improving the results.

It’s one of the areas that are researched in machine learning and called [“lottery ticket hypothesis”](https://arxiv.org/abs/1803.03635). I personally found this to initially to be **super non-intuitive **and was totally mind blown to see how [adding fully linear layers to a network ](http://www.wisdom.weizmann.ac.il/~vision/kernelgan/)can make a huge difference on it converging to good results.

What helps gradient descent a lot is some good initial initialization. This not only increases the chances of convergence, but also the convergence speed. For our filters initializing them with SVD-based low-rank approximation was very helpful – feel free to try if you can get the same results with fully randomized initialization. The worst possible initialization would be something totally-uniform, and with its gradient being same for all variables (or even worse, zero gradient). An example: if optimizing a function that is product of a and b, don’t initialize them both to zero – think how the gradients would look like and what would happen in such case. 🙂

A second practical advice is to keep the learning rate as low as your patience allows for. You avoid the risks of “jumping over” your optimal solution.

![](../../assets/8251a1edeabdef08.jpg)

**Red:**too large learning / optimization rate can jump over the global maximum!

**Green:**Lower learning rate is “safer” for local optimization.

Too high of a learning rate can make your gradients “explode” and jump completely out of reasonable parameter space. Probably everyone who ever played with gradient descent saw **loss or parameters becomeing NaNs or infinity** at some point and then debugged why. There can be many causes, from a wrong loss function, through bad behaving gradients (derivatives of certain function can get huge; e.g. sqrt around zero), but very often it is too large of learning rate. 🙂 If your optimization is too slow, instead of increasing the optimization rate, try [momentum-based](https://distill.pub/2017/momentum/) or [higher order optimization ](https://en.wikipedia.org/wiki/Newton%27s_method_in_optimization)– both are actually **trivial **to code with JAX, especially for such small use-cases!

## Conclusions

In this blog post, we have looked at incorporating some simple offline optimization using numpy and JAX to our programming toolset. We discussed difficulties of designing a “good” loss function and then tuning it, and applied it to our problem of producing good separable image filters. If you do any kind of high performance work, don’t be deterred from machine learning – you don’t have to do it in real time and on the device, but can use it offline. For example of optimizing/computing offline approximations that can make something feasible in real time, check out one of papers that finally got out (I contributed to a longer while ago) – [real time stylization through optimizing discrete filters](https://arxiv.org/abs/2002.10945).

My personal final conclusion is that I want more of such simple, yet expressive and powerful libraries like JAX. The less boilerplate the better! 🙂

found your blog, so many info to read, you are crazy(in good sense) writing all this!

Pingback: Separate your filters! Separability, SVD and low-rank approximation of 2D image processing filters | Bart Wronski

Pingback: “Optimizing” blue noise dithering – backpropagation through Fourier transform and sorting | Bart Wronski

Pingback: Neural material (de)compression – data-driven nonlinear dimensionality reduction | Bart Wronski

Pingback: Comparing images in frequency domain. “Spectral loss” – does it make sense? | Bart Wronski

Pingback: Processing aware image filtering: compensating for the upsampling | Bart Wronski

Pingback: Fast, GPU friendly, antialiasing downsampling filter | Bart Wronski

Pingback: Gradient-descent optimized recursive filters for deconvolution / deblurring | Bart Wronski