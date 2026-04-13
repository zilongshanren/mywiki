---
title: Differentiable Programming from Scratch
url: https://thenumb.at/Autodiff/
published: '2022-07-31'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Differentiable Programming from Scratch

[Differentiable programming](https://en.wikipedia.org/wiki/Differentiable_programming) has become a hot research topic, and not only due to the popularity of machine learning frameworks like TensorFlow, PyTorch, and JAX. Many fields apart from machine learning are finding differentiable programming to be a useful tool for solving optimization problems. In computer graphics, differentiable [rendering](https://www.youtube.com/watch?v=Tou8or1ed6E), differentiable [physics](https://physicsbaseddeeplearning.org/diffphys.html), and [neural representations](https://thenumb.at/Neural-Graphics/) are all gaining popularity.

*This article received an honorable mention in 3Blue1Brown’s Summer of Math Exposition 2!*

# Prerequisites

## Differentiation

It all starts with the definition you learn in calculus class:

In other words, the derivative computes how much $$f(x)$$ changes when $$x$$ is perturbed by an infinitesimal amount. If $$f$$ is a one-dimensional function from $$\mathbb{R} \mapsto \mathbb{R}$$, the derivative $$f^{\prime}(x)$$ returns the slope of the graph of $$f$$ at $$x$$.

However, there’s another perspective that provides better intuition in higher dimensions. If we think of $$f$$ as a map from points in its domain to points in its range, we can think of $$f^{\prime}(x)$$ as a map from *vectors* based at $$x$$ to *vectors* based at $$f(x)$$.

### One-to-One

In 1D, this distinction is a bit subtle, as a 1D “vector” is just a single number. Still, evaluating $$f^{\prime}(x)$$ shows us how a vector placed at $$x$$ is scaled when transformed by $$f$$. That’s just the slope of $$f$$ at $$x$$.

### Many-to-One

If we consider a function $$g(x,y) : \mathbb{R}^2 \mapsto \mathbb{R}$$ (two inputs, one output), this perspective will become clearer. We can differentiate $$g$$ with respect to any particular input, known as a partial derivative:

The function $$g_x$$ computes the change in $$g$$ given a change in $$x$$. By combining $$g_x$$ with the corresponding $$g_y$$, we produce the *gradient* of $$g$$:

That is, $$\nabla g(x,y)$$ tells us how $$g$$ changes if we change either $$x$$ or $$y$$. If we multiply $$\nabla g(x,y)$$ with a column vector of differences $$\Delta x,\Delta y$$, we’ll get their combined effect on $$g$$:

It’s tempting to think of the gradient as just another vector. However, it’s often useful to think of the gradient as a *higher-order function*: $$\nabla g$$ is a function that, when evaluated at $$x,y$$, gives us *another function* that transforms *vectors* based at $$x,y$$ to *vectors* based at $$g(x,y)$$.

It just so happens that the function returned by our gradient is linear, so it can be represented as a matrix multiplication.

The gradient is typically explained as the “direction of steepest ascent.” Why is that? When we evaluate the gradient at a point $$x,y$$ and a vector $$\Delta x, \Delta y$$, the result is a change in the output of $$g$$. If we *maximize* the change in $$g$$ with respect to the input vector, we’ll get the direction that makes the output increase the fastest.

Since the gradient function is just a product with $$\begin{bmatrix}g_x(x,y) & g_y(x,y)\end{bmatrix}$$, the direction $$\begin{bmatrix}\Delta x & \Delta y\end{bmatrix}$$ that maximizes the result is easy to find: it’s parallel to $$\begin{bmatrix}g_x(x,y) & g_y(x,y)\end{bmatrix}$$. That means the gradient vector is, in fact, the direction of steepest ascent.

#### The Directional Derivative

Another important term is the *directional derivative*, which computes the derivative of a function along an arbitrary direction. It is a generalization of the partial derivative, which evaluates the directional derivative along a coordinate axis.

Above, we discovered that our “gradient function” could be expressed as a dot product with the gradient vector. That was, actually, the directional derivative:

Which again illustrates why the gradient vector is the direction of steepest ascent: it is the $$\mathbf{v}$$ that maximizes the directional derivative. Note that in curved spaces, the “steepest ascent” definition of the gradient still holds, but the directional derivative becomes more complicated than a dot product.

### Many-to-Many

For completeness, let’s examine how this perspective extends to vector-valued functions of multiple variables. Consider $$h(x,y) : \mathbb{R}^2 \mapsto \mathbb{R}^2$$ (two inputs, two outputs).

We can take the gradient of each part of $$h$$:

What object would represent $$\nabla h$$? We can build a matrix from the gradients of each component, called the *Jacobian*:

Above, we argued that the gradient (when evaluated at $$x,y$$) gives us a map from input *vectors* to output *vectors*. That remains the case here: the Jacobian is a 2x2 matrix, so it transforms 2D $$\Delta x,\Delta y$$ vectors into 2D $$\Delta h_1, \Delta h_2$$ vectors.

Adding more dimensions starts to make our functions hard to visualize, but we can always rely on the fact that the derivative tells us how input vectors (i.e. changes in the input) get mapped to output vectors (i.e. changes in the output).

### The Chain Rule

The last aspect of differentiation we’ll need to understand is how to differentiate function composition.

We could prove this fact with a bit of analysis, but the relationship is again easier to understand by thinking of the derivative as higher order function. In this perspective, the chain rule itself is just a function composition.

For example, let’s assume $$h(\mathbf{x}) : \mathbb{R}^2 \mapsto \mathbb{R}$$ is composed of $$f(\mathbf{x}) : \mathbb{R}^2 \mapsto \mathbb{R}^2$$ and $$g(\mathbf{x}) : \mathbb{R}^2 \mapsto \mathbb{R}$$.

In order to translate a $$\Delta \mathbf{x}$$ vector to a $$\Delta h$$ vector, we can first use $$\nabla f$$ to map $$\Delta \mathbf{x}$$ to $$\Delta \mathbf{f}$$, based at $$f(\mathbf{x})$$. Then we can use $$\nabla g$$ to map $$\Delta \mathbf{f}$$ to $$\Delta g$$, based at $$g(f(\mathbf{x}))$$.

Because our derivatives/gradients/Jacobians are linear functions, we’ve been representing them as scalars/vectors/matrices, respectively. That means we can easily compose them with the typical linear algebraic multiplication rules. Writing out the above example symbolically:

The result is a 2D vector representing a gradient that transforms 2D vectors to 1D vectors. The composed function $$h$$ had two inputs and one output, so that’s correct. We can also notice that each term corresponds to the chain rule applied to a different computational path from a component of $$\mathbf{x}$$ to $$h$$.

## Optimization

We will focus on the application of differentiation to optimization via gradient descent, which is often used in machine learning and computer graphics. An optimization problem always involves computing the following expression:

Which simply means “find the $$\mathbf{x}$$ that results in the smallest possible value of $$f$$.” The function $$f$$, typically scalar-valued, is traditionally called an “energy,” or in machine learning, a “loss function.” Extra constraints are often enforced to limit the valid options for $$\mathbf{x}$$, but we will disregard constrained optimization for now.

One way to solve an optimization problem is to iteratively follow the gradient of $$f$$ “downhill.” This algorithm is known as gradient descent:

- Pick an initial guess $$\mathbf{\bar{x}}$$.
- Repeat:
- Compute the gradient $$\nabla f(\mathbf{\bar{x}})$$.
- Step along the gradient: $$\mathbf{\bar{x}} \leftarrow \mathbf{\bar{x}} - \tau\nabla f(\mathbf{\bar{x}})$$.

- while $$|\nabla f(\mathbf{\bar{x}})| > \epsilon$$.

Given some starting point $$\mathbf{x}$$, computing $$\nabla f(\mathbf{x})$$ will give us the direction from $$\mathbf{x}$$ that would increase $$f$$ the fastest. Hence, if we move our point $$\mathbf{x}$$ a small distance $$\tau$$ along the negated gradient, we will decrease the value of $$f$$. The number $$\tau$$ is known as the step size (or in ML, the learning rate). By iterating this process, we will eventually find an $$\mathbf{x}$$ such that $$\nabla f(\mathbf{x}) \simeq 0$$, which is hopefully the minimizer.

This description of gradient descent makes optimization sound easy, but in reality there is a lot that can go wrong. When gradient descent terminates, the result is only required to be a critical point of $$f$$, i.e. somewhere $$f$$ becomes flat. That means we could wind up at a maximum (unlikely), a saddle point (possible), or a *local* minimum (likely). At a local minimum, moving $$\mathbf{x}$$ in any direction would increase the value of $$f(\mathbf{x})$$, but $$f(\mathbf{x})$$ is **not** necessarily the minimum value $$f$$ can take on globally.

| Maximum | Saddle Point | Local Minimum |

Gradient descent can also diverge (i.e. never terminate) if $$\tau$$ is too large. Because the gradient is only a linear approximation of $$f$$, if we step too far along it, we might skip over changes in $$f$$’s behavior—or even end up *increasing* both $$f$$ and $$\nabla f$$. On the other hand, the smaller we make $$\tau$$, the longer our algorithm takes to converge. Note that we’re assuming $$f$$ has a lower bound and achieves it at a finite $$\mathbf{x}$$ in the first place.

| Divergence | Slow Convergence |

The algorithm presented here is the most basic form of gradient descent: much research has been dedicated to devising loss functions and descent algorithms that have higher likelihoods of converging to reasonable results. The practice of adding constraints, loss function terms, and update rules is known as *regularization*. In fact, optimization is a whole field in of itself: if you’d like to learn more, there’s a vast amount of literature to refer to, especially within machine learning. [This interactive article](https://distill.pub/2017/momentum/) explaining *momentum* is a great example.

# Differentiating Code

Now that we understand differentiation, let’s move on to programming. So far, we’ve only considered mathematical functions, but we can easily translate our perspective to programs. For simplicity, we’ll only consider *pure* functions, i.e. functions whose output depends solely on its parameters (no state).

If your program implements a relatively simple mathematical expression, it’s not too difficult to manually write another function that evaluates its derivative. However, what if your program is a deep neural network, or a physics simulation? It’s not feasible to differentiate something like that by hand, so we must turn to algorithms for automatic differentiation.

There are several techniques for differentiating programs. We will first look at numeric and symbolic differentiation, both of which have been in use as long as computers have existed. However, these approaches are distinct from the algorithm we now know as *autodiff*, which we will discuss later.

## Numerical

Numerical differentiation is the most straightforward technique: it simply approximates the definition of the derivative.

By choosing a small $$h$$, all we have to do is evaluate $$f$$ at $$x$$ and $$x+h$$. This technique is also known as differentiation via *finite differences*.

Implementing numeric differentiation as a higher order function is quite easy. It doesn’t even require modifying the function to differentiate:

function numerical_diff(f, h) { return function (x) { return (f(x + h) - f(x)) / h; } } let df = numerical_diff(f, 0.001);

You can edit the following JavaScript example, where $$f$$ is drawn in blue and numerical_diff($$f$$, 0.001) is drawn in purple. Note that using control flow is not a problem.

Unfortunately, finite differences have a big problem: they only compute the derivative of $$f$$ in one direction. If our input is very high dimensional, computing the full gradient of $$f$$ becomes computationally infeasible, as we would have to evaluate $$f$$ for each dimension separately.

That said, if you only need to compute one directional derivative of $$f$$, the full gradient is overkill: instead, compute a finite difference between $$f(\mathbf{x})$$ and $$f(\mathbf{x} + \Delta\mathbf{x})$$, where $$\Delta\mathbf{x}$$ is a small step in your direction of interest.

Finally, always remember that numerical differentiation is only an approximation: we aren’t computing the actual limit as $$h \rightarrow 0$$. While finite differences are quite easy to implement and can be very useful for validating other results, the technique should usually be superseded by another approach.

## Symbolic

Symbolic differentiation involves transforming a representation of $$f$$ into a representation of $$f^\prime$$. Unlike numerical differentiation, this requires specifying $$f$$ in a domain-specific language where each syntactic construct has a known differentiation rule.

However, that limitation isn’t so bad—we can create a compiler that differentiates expressions in our symbolic language for us. This is the technique used in computer algebra packages like Mathematica.

For example, we could create a simple language of polynomials that is symbolically differentiable using a small set of recursive rules.

```
d(n) -> 0
d(x) -> 1
d(Add(a, b)) -> Add(d(a), d(b))
d(Times(a, b)) -> Add(Times(d(a), b), Times(a, d(b)))
```


Try out the following implementation:

If we want our differentiable language to support more operations, we can simply add more differentiation rules. For example, to support trig functions:

```
d(sin a) -> Times(d(a), cos a)
d(cos a) -> Times(d(a), Times(-1, sin a))
```


Unfortunately, there’s a catch: the size of $$f^\prime$$’s representation can become very large. Let’s write another recursive relationship that counts the number of terms in an expression:

```
Terms(n) -> 1
Terms(x) -> 1
Terms(Add(a, b)) -> Terms(a) + Terms(b) + 1
Terms(Times(a, b)) -> Terms(a) + Terms(b) + 1
```


And then prove that `Terms(a) <= Terms(d(a))`

, i.e. differentiating an expression cannot decrease the number of terms:

```
Base Cases:
Terms(d(n)) -> 1 | Definition
Terms(n) -> 1 | Definition
=> Terms(n) <= Terms(d(n))
Terms(d(x)) -> 1 | Definition
Terms(x) -> 1 | Definition
=> Terms(x) <= Terms(d(x))
Inductive Case for Add:
Terms(Add(a, b)) -> Terms(a) + Terms(b) + 1 | Definition
Terms(d(Add(a, b))) -> Terms(d(a)) + Terms(d(b)) + 1 | Definition
Terms(a) <= Terms(d(a)) | Hypothesis
Terms(b) <= Terms(d(b)) | Hypothesis
=> Terms(Add(a, b)) <= Terms(d(Add(a, b)))
Inductive Case for Times:
Terms(Times(a, b)) -> Terms(a) + Terms(b) + 1 | Definition
Terms(d(Times(a, b))) -> Terms(a) + Terms(b) + 3 +
Terms(d(a)) + Terms(d(b)) | Definition
=> Terms(Times(a, b)) <= Terms(d(Times(a, b)))
```


This result might be acceptable if the size of `df`

was linear in the size of `f`

, but that’s not the case. Whenever we differentiate a `Times`

expression, the number of terms in the result will at least *double*. That means the size of `df`

grows *exponentially* with the number of `Times`

we compose. You can demonstrate this phenomenon by nesting multiple `Times`

in the JavaScript example.

Hence, symbolic differentiation is usually infeasible at the scales we’re interested in. However, if it works for your use case, it can be quite useful.

# Automatic Differentiation

We’re finally ready to discuss the automatic differentiation algorithm actually used in modern differentiable programming: autodiff! There are two flavors of autodiff, each named for the direction in which it computes derivatives.

## Forward Mode

Forward mode autodiff improves on our two older techniques by computing exact derivatives without building a potentially exponentially-large representation of $$f^\prime$$. It is based on the mathematical definition of *dual numbers*.

### Dual Numbers

Dual numbers are a bit like complex numbers: they’re defined by [adjoining](https://en.wikipedia.org/wiki/Field_extension) a new quantity $$\epsilon$$ to the reals. But unlike complex numbers where $$i^2 = -1$$, dual numbers use $$\epsilon^2 = 0$$.

In particular, we can use the $$\epsilon$$ part of a dual number to represent the derivative of the scalar part. If we replace each variable $$x$$ with $$x + x^\prime\epsilon$$, we will find that dual arithmetic naturally expresses how derivatives combine:

Addition:

Multiplication:

Division:

The chain rule also works: $$f(x + x^\prime\epsilon) = f(x) + f^\prime(x)x^\prime\epsilon$$ for any smooth function $$f$$. To prove this fact, let us first show that the property holds for positive integer exponentiation.

Base case: $$(x+x^\prime\epsilon)^1 = x^1 + 1x^0x^\prime\epsilon$$

Hypothesis: $$(x+x^\prime\epsilon)^n = x^n + nx^{n-1}x^\prime\epsilon$$

Induct:

We can use this result to prove the same property for any smooth function $$f$$. Examining the Taylor expansion of $$f$$ at zero (also known as its *Maclaurin series*):

By plugging in our dual number…

…we prove the result! In the last step, we recover the Maclaurin series for both $$f(x)$$ and $$f^\prime(x)$$.

### Implementation

Implementing forward-mode autodiff in code can be very straightforward: we just have to replace our `Float`

type with a `DiffFloat`

that keeps track of both our value and its dual coefficient. If we then implement the relevant math operations for `DiffFloat`

, all we have to do is run the program!

Unfortunately, JavaScript does not support operator overloading, so we’ll define a `DiffFloat`

to be a two-element array and use functions to implement some basic arithmetic operations:

function Const(n) { return [n, 0]; } function Add(x, y) { return [x[0] + y[0], x[1] + y[1]]; } function Times(x, y) { return [x[0] * y[0], x[1] * y[0] + x[0] * y[1]]; }

If we implement our function $$f$$ in terms of these primitives, evaluating $$f([x,1])$$ will return $$[f(x),f^\prime(x)]$$!

This property extends naturally to higher-dimensional functions, too. If $$f$$ has multiple outputs, their derivatives pop out in the same way. If $$f$$ has inputs other than $$x$$, assigning them constants means the result will be the partial derivative $$f_x$$.

### Limitations

While forward-mode autodiff does compute exact derivatives, it suffers from the same fundamental problem as finite differences: each invocation of $$f$$ can only compute the directional derivative of $$f$$ for a single direction.

It’s useful to think of a forward mode derivative as computing one *column* of the gradient matrix. Hence, if $$f$$ has few inputs but many outputs, forward mode can still be quite efficient at recovering the full gradient:

Unfortunately, optimization problems in machine learning and graphics often have the opposite structure: $$f$$ has a huge number of inputs (e.g. the coefficients of a 3D scene or neural network) and a single output. That is, $$\nabla f$$ has many columns and few rows.

## Backward Mode

As you might have guessed, backward mode autodiff provides a way to compute a *row* of the gradient using a single invocation of $$f$$. For optimizing many-to-one functions, this is exactly what we want: the full gradient in one pass.

In this section, we will use Leibniz’s notation for derivatives, which is:

Leibniz’s notation makes it easier to write down the derivative of an arbitrary variable with respect an arbitrary input. Derivatives also obtain nice algebraic properties, if you squint a bit:

### Backpropagation

Similarly to how forward-mode autodiff propagated derivatives from inputs to outputs, backward-mode propagates derivatives from outputs to inputs.

That sounds easy enough, but the code only runs in one direction. How would we know what the gradient of our input should be before evaluating the rest of the function? We don’t—when evaluating $$f$$, we use each operation to build a *computational graph* that represents $$f$$. That is, when $$f$$ tells us to perform an operation, we create a new node noting what the operation is and connect it to the nodes representing its inputs. In this way, a pure function can be nicely represented as a directed acyclic graph, or DAG.

For example, the function $$f(x,y) = x^2 + xy$$ may be represented with the following graph:

When evaluating $$f$$ at a particular input, we write down the intermediate values computed by each node. This step is known as the *forward pass*, and computes *primal* values.

Then, we begin the *backward pass*, where we compute *dual* values, or derivatives. Our ultimate goal is to compute $$\frac{\partial f}{\partial x}$$ and $$\frac{\partial f}{\partial y}$$. At first, we only know the derivative of $$f$$ with respect to final plus—they’re the same value, so $$\frac{\partial f}{\partial +} = 1$$.

We can see that the output was computed by adding together two incoming values. Increasing either input to the sum would increase the output by an equal amount, so derivatives propagated through this node should be unaffected. That is, if $$+$$ is the output and $$+_1,+_2$$ are the inputs, $$\frac{\partial +}{\partial +_1} = \frac{\partial +}{\partial +_2} = 1$$.

Now we can use the chain rule to combine our derivatives, getting closer to the desired result: $$\frac{\partial f}{\partial +_1} = \frac{\partial f}{\partial +}\cdot\frac{\partial +}{\partial +_1} = 1$$, $$\frac{\partial f}{\partial +_2} = \frac{\partial f}{\partial +}\cdot\frac{\partial +}{\partial +_2} = 1$$.

When we evaluate a node, we know the derivative of $$f$$ with respect to its output. That means we can propagate the derivative back along the node’s incoming edges, modifying it based on the node’s operation. As long as we evaluate all outputs of a node before the node itself, we only have to check each node once. To assure proper ordering, we may traverse the graph in [ reverse topological order](https://en.wikipedia.org/wiki/Topological_sorting).

Once we get to a multiplication node, there’s slightly more to do: the derivative now depends on the *primal* input values. That is, if $$f(x,y) = xy$$, $$\frac{\partial f}{\partial x} = y$$ and $$\frac{\partial f}{\partial y} = x$$.

By applying the chain rule, we get $$\frac{\partial f}{\partial *_1} = 1\cdot*_2$$ and $$\frac{\partial f}{\partial *_2} = 1\cdot*_1$$ for both multiplication nodes.

Applying the chain rule one last time, we get $$\frac{\partial f}{\partial y} = 2$$. But $$x$$ has multiple incoming derivatives—how do we combine them? Each incoming edge represents a different way $$x$$ affects $$f$$, so $$x$$’s total contribution is simply their sum. That means $$\frac{\partial f}{\partial x} = 7$$. Let’s check our result:

You’ve probably noticed that traversing the graph built up a derivative term for each path from an input to the output. That’s exactly the behavior that arose when we manually computed the gradient using the chain rule!

Backpropagation is essentially the chain rule upgraded with dynamic programming. Traversing the graph in reverse topological order means we may evaluate each vertex only once, then reuse its derivative everywhere else it shows up. Despite having to express $$f$$ as a computational graph and traverse both forward and backward, the whole algorithm has the same time complexity as $$f$$ itself. Space complexity, however, is a separate issue.

### Implementation

We can implement backward mode autodiff using a similar approach as forward mode. Instead of making every operation use dual numbers, we can make each step add a node to our computational graph.

function Const(n) { return {op: 'const', in: [n], out: undefined, grad: 0}; } function Add(x, y) { return {op: 'add', in: [x, y], out: undefined, grad: 0}; } function Times(x, y) { return {op: 'times', in: [x, y], out: undefined, grad: 0}; }

Note that JavaScript will automatically store references within the `in`

arrays, hence build a DAG instead of a tree. If we implement our function $$f$$ in terms of these primitives, we can evaluate it on an input node to automatically build the graph.

let in_node = {op: 'const', in: [/* TBD */], out: undefined, grad: 0}; let out_node = f(in_node);

The forward pass performs a post-order traversal of the graph, translating inputs to outputs for each node. Remember we’re operating on a DAG: we must check whether a node is already resolved, lest we recompute values that could be reused.

function forward(node) { if (node.out !== undefined) return; if (node.op === 'const') { node.out = node.in[0]; } else if (node.op === 'add') { forward(node.in[0]); forward(node.in[1]); node.out = node.in[0].out + node.in[1].out; } else if (node.op === 'times') { forward(node.in[0]); forward(node.in[1]); node.out = node.in[0].out * node.in[1].out; } }

The backward pass is conceptually similar, but a naive pre-order traversal would end up tracing out every path in the DAG—every gradient has to be pushed back to the roots. Instead, we’ll first compute a reverse topological ordering of the nodes. This ordering guarantees that when we reach a node, everything “downstream” of it has already been resolved—we’ll never have to return.

function backward(out_node) { const order = topological_sort(out_node).reverse(); for (const node of order) { if (node.op === 'add') { node.in[0].grad += node.grad; node.in[1].grad += node.grad; } else if (node.op === 'times') { node.in[0].grad += node.in[1].out * node.grad; node.in[1].grad += node.in[0].out * node.grad; } } }

Finally, we can put our functions together to compute $$f(x)$$ and $$f^\prime(x)$$:

function evaluate(x, in_node, out_node) { in_node.in = [x]; forward(out_node); out_node.grad = 1; backward(out_node); return [out_node.out, in_node.grad]; }

Just remember to clear all the `out`

and `grad`

fields before evaluating again! Lastly, the working implementation:

### Limitations

If $$f$$ is a function of multiple variables, we can simply read the gradients from the corresponding input nodes. That means we’ve computed a whole row of $$\nabla f$$. Of course, if the gradient has many rows and few columns, forward mode would have been more efficient.

Unfortunately, backwards mode comes with another catch: we had to store the intermediate result of every single computation inside $$f$$! If we’re passing around substantial chunks of data, say, weight matrices for a neural network, storing the intermediate results can require an unacceptable amount of memory and memory bandwidth. If $$f$$ contains loops, it’s especially bad—because every value is immutable, naive loops will create long chains of intermediate values. For this reason, real-world frameworks tend to encapsulate loops in monolithic parallel operations that have analytic derivatives.

Many engineering hours have gone into reducing space requirements. One problem-agnostic approach is called checkpointing: we can choose not to store intermediate results at some nodes, rather re-computing them on the fly during the backward pass. Checkpointing gives us a natural space-time tradeoff: by strategically choosing which nodes store intermediate results (e.g. ones with expensive operations), we can reduce memory usage without dramatically increasing runtime.

Even with checkpointing, training the largest neural networks requires far more fast storage than is available to a single computer. By partitioning our computational graph between multiple systems, each one only needs to store values for its local nodes. Unfortunately, this implies edges connecting nodes assigned to different processors must send their values across a network, which is expensive. Hence, communication costs may be minimized by finding min-cost graph cuts.

### Graphs and Higher-Order Autodiff

Earlier, we could have computed primal values while evaluating $$f$$ itself. Frameworks like PyTorch and TensorFlow take this approach—evaluating $$f$$ both builds the graph (also known as the ’tape’) and evaluates the forward-pass results. The user may call `backward`

at any point, propagating gradients to all inputs that contributed to the result.

However, the forward-backward approach can limit the system’s potential performance. The forward pass is relatively easy to optimize via parallelizing, vectorizing, and distributing graph traversal. The backward pass, on the other hand, is harder to parallelize, as it requires a topological traversal and coordinated gradient accumulation. Furthermore, the backward pass lacks some mathematical power. While computing a specific derivative is easy, we don’t get back a general *representation* of $$\nabla f$$. If we wanted the gradient of the gradient (the Hessian), we’re out of luck.

Thinking about the gradient as a higher-order function reveals a potentially better approach. If we can represent $$f$$ as a computational graph, there’s no reason we can’t also represent $$\nabla f$$ *in the same way*. In fact, we can simply add nodes to the graph of $$f$$ that compute derivatives with respect to each input. Because the graph already computes primal values, each node in $$f$$ only requires us to add a constant number of nodes in the graph of $$\nabla f$$. That means the result is only a constant factor larger than the input—evaluating it requires exactly the same computations as the forward-backward algorithm.

For example, given the graph of $$f(x) = x^2 + x$$, we can produce the following:

Defining differentiation as a function *on computational graphs* unifies the forward and backward passes: we get a single graph that computes both $$f$$ and $$\nabla f$$. That means we can compute higher order derivatives by applying the transformation again! Distributed training is easier, too—we don’t have to implicitly synchronize gradient updates across multiple systems. JAX implements this approach, enabling its seamless gradient, JIT compilation, and vectorization transforms. PyTorch also supports higher-order differentiation via including backward operations in the computational graph, and [functorch](https://github.com/pytorch/functorch) provides a JAX-like API.

# De-blurring an Image

Let’s use our fledgling differentiable programming framework to solve a real optimization problem: de-blurring an image. We’ll assume our observed image was computed using a simple box filter, i.e., each blurred pixel is the average of the surrounding 3x3 ground-truth pixels. Of course, a blur loses information, so we won’t be able to reconstruct the exact input—but we can get pretty close!

Ground Truth Image | Observed Image |

We’ll need to add one more operation to our framework: division. The operation and forward pass are much the same as addition and multiplication, but the backward pass must compute $$\frac{\partial f}{\partial x}$$ and $$\frac{\partial f}{\partial y}$$ for $$f = \frac{x}{y}$$.

function Divide(x, y) { return {op: 'divide', in: [x, y], out: undefined, grad: 0}; } // Forward... if(node.op === 'divide') { forward(node.in[0]); forward(node.in[1]); node.out = node.in[0].out / node.in[1].out; } // Backward... if(node.op === 'divide') { n.in[0].grad += n.grad / node.in[1].out; n.in[1].grad += (-n.grad * node.in[0].out / (node.in[1].out * node.in[1].out)); }

Before we start programming, we need to express our task as an optimization problem. That entails minimizing a loss function that measures how far away we are from our goal.

Let’s start by guessing an arbitrary image—for example, a solid grey block. We can then compare the result of blurring our guess with the observed image. The farther our blurred result is from the observation, the larger the loss should be. For simplicity, we will define our loss as the total squared difference between each corresponding pixel.

Using differentiable programming, we can compute $$\frac{\partial \text{Loss}}{\partial \text{Guess}}$$, i.e. how changes in our proposed image change the resulting loss. That means we can apply gradient descent to the guess, guiding it towards a state that minimizes the loss function. Hopefully, if our blurred guess matches the observed image, our guess will match the ground truth image.

Let’s implement our loss function in differentiable code. First, create the guess image by initializing the differentiable parameters to solid grey. Each pixel has three components: red, green, and blue.

let guess_image = new Array(W*H*3); for (let i = 0; i < W * H * 3; i++) { guess_image[i] = Const(127); }

Second, apply the blur using differentiable operations.

let blurred_guess_image = new Array(W*H*3); for (let x = 0; x < W; x++) { for (let y = 0; y < H; y++) { let [r,g,b] = [Const(0), Const(0), Const(0)]; // Accumulate pixels for averaging for (let i = -1; i < 1; i++) { for (let j = -1; j < 1; j++) { // Convert 2D pixel coordinate to 1D row-major array index const xi = clamp(x + i, 0, W - 1); const yj = clamp(y + j, 0, H - 1); const idx = (yj * W + xi) * 3; r = Add(r, guess_image[idx + 0]); g = Add(g, guess_image[idx + 1]); b = Add(b, guess_image[idx + 2]); } } // Set result to average const idx = (y * W + x) * 3; blurred_guess_image[idx + 0] = Divide(r, Const(9)); blurred_guess_image[idx + 1] = Divide(g, Const(9)); blurred_guess_image[idx + 2] = Divide(b, Const(9)); } }

Finally, compute the loss using differentiable operations.

let loss = Const(0); for (let x = 0; x < W; x++) { for (let y = 0; y < H; y++) { const idx = (y * W + x) * 3; let dr = Add(blurred_guess_image[idx + 0], Const(-observed_image[idx + 0])); let dg = Add(blurred_guess_image[idx + 1], Const(-observed_image[idx + 1])); let db = Add(blurred_guess_image[idx + 2], Const(-observed_image[idx + 2])); loss = Add(loss, Times(dr, dr)); loss = Add(loss, Times(dg, dg)); loss = Add(loss, Times(db, db)); } }

Calling `forward(loss)`

performs the whole computation, storing results in each node’s `out`

field. Calling `backward(loss)`

computes the derivative of loss at every node, storing results in each node’s `grad`

field.

Let’s write a simple optimization routine that performs gradient descent on the guess image.

function gradient_descent_step(step_size) { // Clear output values and gradients reset(loss); // Forward pass forward(loss); // Backward pass loss.grad = 1; backward(loss); // Move parameters along gradient for (let i = 0; i < W * H * 3; i++) { let p = guess_image[i]; p.in[0] -= step_size * p.grad; } }

We’d also like to compute `error`

, the squared distance between our guess image and the ground truth. We can’t use error to inform our algorithm—we’re not supposed to know what the ground truth was—but we can use it to measure how well we are reconstructing the image. For the current iteration, we visualize the guess image, the guess image after blurring, and the gradient of loss with respect to each pixel.

|

|

# Further Reading

If you’d like to learn more about differentiable programming in ML and graphics, check out the following resources:

[JAX](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html),[PyTorch](https://pytorch.org/tutorials/beginner/basics/intro.html),[TensorFlow](https://www.tensorflow.org/tutorials/quickstart/beginner),[tinygrad](https://github.com/geohot/tinygrad),[TinyAD](https://github.com/patr-schm/TinyAD)[Physics-Based Deep Learning](https://physicsbaseddeeplearning.org/intro.html),[Differentiable Rendering Intro](https://www.youtube.com/watch?v=Tou8or1ed6E),[Differentiable Rendering Papers](https://rgl.epfl.ch/publications),[Neural Fields in Visual Computing](https://neuralfields.cs.brown.edu/)[CMU Deep Learning Systems](https://dlsyscourse.org/)