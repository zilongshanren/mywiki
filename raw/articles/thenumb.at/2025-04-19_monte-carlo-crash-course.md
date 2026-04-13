---
title: Monte Carlo Crash Course
url: https://thenumb.at/Rendering/
published: '2025-04-19'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Monte Carlo Crash Course

[Continuous Probability](https://thenumb.at/Probability)[Exponentially Better Integration](https://thenumb.at/Monte-Carlo)[Sampling](https://thenumb.at/Sampling)[Case Study: Rendering](https://thenumb.at/Rendering)[Quasi-Monte Carlo](https://thenumb.at/QMC)*Coming Soon…*

# Case Study: Rendering

So far, we’ve explored Monte Carlo methods using simple examples, like sampling the unit disk and sphere.
Now, we’ll apply Monte Carlo to a more realistic task: simulating light traveling through a scene, or [ rendering](https://github.com/TheNumbat/Diopter?tab=readme-ov-file#renders).

## Direct Lighting

To keep our focus on Monte Carlo methods, we’ll use a simplified model of light transport in two dimensions. 1
In particular, we will only define one quantity:

*radiance*. Denoted as $$\mathcal{L}_i(\mathbf{x},\theta)$$, radiance measures the amount of light arriving at a point $$\mathbf{x}$$ from an incoming direction $$\theta$$.

To compute $$\mathcal{L}_i(\mathbf{x},\theta)$$, we trace a ray starting from $$\mathbf{x}$$ and travelling along $$\theta$$.
When we trace a ray, it travels in the *opposite* direction as the above diagram—we will draw arrows to illustrate the direction *light* travels.

If the ray hits a light source, we return its color, or *emitted radiance*.
Otherwise, we’ll return zero.

```
def radiance(x, θ):
hit = trace_ray(x, θ)
if hit.light:
return hit.emission
return 0
```


Since radiance depends on angle, it’s hard to visualize directly.
Instead, we will associate a color with $$\mathbf{x}$$ by averaging radiance over all incoming $$\theta$$. 2
To render an image, we can evaluate this quantity at each pixel.


[3](https://thenumb.at#fn:3)![](../../assets/efae3b498ba89ede.png)

This model is known as *direct lighting*, since we only consider radiance along rays that immediately hit light sources.
Despite its simplicity, it has some interesting behavior: for example, [soft shadowing](https://ciechanow.ski/lights-and-shadows/#shadow) occurs when only a portion of the light source is visible from $$\mathbf{x}$$.

### Monte Carlo Integration

To actually compute average radiance at $$\mathbf{x}$$, we can apply [Monte Carlo integration](https://thenumb.at/Monte-Carlo#monte-carlo-integration) to the above integral.

Assuming we sample $$\theta$$ uniformly, this boils down to averaging $$\mathcal{L}_i$$ over $$N$$ samples of $$\theta \in [0,2\pi]$$.

```
def pixel(x):
L = 0
for i in range(N):
θ = random(0, 2π)
L += radiance(x, θ)
return L / N
```


The implementation below shows the resulting image after a single sample—it’s very noisy! Use the numbered buttons to increase the sample count $$N$$, shown in blue.

Like we saw in [chapter two](https://thenumb.at/Monte-Carlo/#escaping-the-curse), each pixel’s error will decrease in proportion to $$\frac{1}{\sqrt{N}}$$.
Perceptually, you might notice that the random noise becomes half as significant given four times the sample count.

## Indirect Lighting

If direct lighting was the end goal, we wouldn’t need Monte Carlo integration in the first place—we could use a simpler technique to evaluate our one-dimensional integral.
However, we also want to model how light bounces between surfaces, or *indirect lighting*.
Indirect lighting looks much more realistic:

![](../../assets/1813481485a209aa.png)

Under direct lighting, surfaces were not reflective—whenever a ray hit a surface, we returned zero radiance.
Now, we’ll assume surfaces scatter light uniformly in all directions (also known as *diffuse reflection*).

When a ray hits a surface at a point $$\mathbf{s}$$, we need to determine the total radiance reflected through $$\mathbf{s}$$ toward $$\mathbf{x}$$.
This quantity is known as *outgoing radiance*, written as $$\mathcal{L}_o(\mathbf{s},\theta_o)$$.
Outgoing radiance can be computed by integrating incoming radiance over all $$\theta_i$$ comprising the hemisphere above $$\mathbf{s}$$.

Intuitively, we’re adding up radiance coming from all visible directions, scaled by the portion of light $$\mathbf{s}$$ reflects from that direction.
We won’t get into the [details](https://en.wikipedia.org/wiki/Rendering_equation) of this integral here, but each term has a physical meaning:

$$\mathcal{L}_i(\mathbf{s},\theta_i)$$ measures the amount of incoming light along $$\theta_i$$.

$$f_\mathbf{s}(\theta_o,\theta_i)$$ is a

*bidirectional reflectance distribution function*or BRDF.It measures the proportion of light coming from $$\theta_i$$ that gets reflected along $$\theta_o$$.[4](https://thenumb.at#fn:4)For ideal diffuse surfaces, we have $$f_\text{diffuse}(\theta_o,\theta_i)=\frac{1}{2}$$.[5](https://thenumb.at#fn:5)[6](https://thenumb.at#fn:6)$$\cos\theta_i$$ scales down incoming light from

[grazing angles](https://ciechanow.ski/lights-and-shadows#position).

Notice that $$\mathcal{L}$$ is now *recursive*: evaluating outgoing radiance requires integrating incoming radiance, which requires evaluating outgoing radiance, and so on.
The recursion encodes how light can reflect off any number of surfaces before reaching $$\mathbf{x}$$.

Our integration problem is now extremely high dimensional: we want to sum incoming radiance over **all possible paths** from a light to $$\mathbf{x}$$.
It’s no longer feasible to apply an integration technique like [quadrature](https://thenumb.at/Monte-Carlo/#quadrature).

### Monte Carlo Integration

As before, we’ll use Monte Carlo integration to compute the average radiance at each pixel $$\mathbf{x}$$.
However, when our ray hits a surface, we will perform *another* Monte Carlo integration to compute the reflected radiance.

In our inner estimator, we recursively compute $$\mathcal{L}_i(\mathbf{s},\theta_m)$$ for each sample.
If we make $$d$$ recursive calls, that means we’ll have to trace $$M^d$$ rays.
Have we run into the [curse of dimensionality](https://thenumb.at/Monte-Carlo/#the-curse-of-dimensionality) again?

To avoid the combinatorial explosion, we’ll simply set $$M=1$$. Concretely, we choose a single direction to continue with at each surface.

```
def radiance(x, θ):
hit = trace_ray(x, θ)
if hit.light:
return hit.emission
elif hit.diffuse:
θi = random(-π/2, π/2)
return (π / 2) * radiance(hit.point, hit.to_world(θi)) * cos(θi)
return 0
```


Using only one sample might sound unwise, since our estimate of reflected radiance will have high variance. Nonetheless, we’ll find that this strategy works well in practice:

Although the resulting image is noisier, our *top-level* estimator only converges slower by a constant factor.
Regardless of the variance of each sample (as long as it’s [finite](https://thenumb.at/Monte-Carlo/#escaping-the-curse)), overall error still scales with $$\frac{1}{\sqrt{N}}$$! 7
This is why Monte Carlo integration is critical for rendering: it handles our high-dimensional sample space with ease.

## Specular Reflection

Diffuse lighting looks fairly realistic, but most surfaces aren’t perfectly diffuse reflectors.
At the other extreme, we have mirrors and prisms, which only reflect light in specific (*specular*) directions.
Real-world surfaces typically fall between these models, exhibiting both diffuse and specular reflections.[8](https://thenumb.at#fn:8)

![](../../assets/15a0a25c04177a40.png)

![](../../assets/b03f806ae34598d8.png)

For diffuse surfaces, we used a simple BRDF that did not depend on the incoming or outgoing angle.

Mirrors are a bit more complicated—let’s find a suitable BRDF. It must have two properties:

- It’s non-zero only when $$\theta_o$$ and $$\theta_i$$ form a perfect reflection, i.e. $$\theta_i = -\theta_o$$.
- It doesn’t emit or absorb light, so $$\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} f(\theta_o,\theta_i) \cos\theta_i\, d\theta_i = 1$$ for all $$\theta_o$$.

Recalling [chapter one](https://thenumb.at/Probability/#dirac-delta-distributions), we can use the Dirac delta distribution to satisfy the first property.

But it doesn’t quite work for the second.

We just need to divide out the cosine factor, giving us the final BRDF.

Using similar reasoning, we could find a BRDF for specular refraction, too—but doing so introduces some [additional complexity](https://pbr-book.org/4ed/Reflection_Models/Dielectric_BSDF#Non-SymmetricScatteringandRefraction) that’s out of scope for this chapter.

### Monte Carlo Integration

Naively, our new Dirac delta BRDF seems to be incompatible with Monte Carlo integration.
If we randomly sample incoming directions, we’ll [never](https://thenumb.at/Probability/#probability-mass-vs-probability-density) end up picking precisely $$\theta_m = -\theta_o$$, so we’ll always return zero.

Fortunately, we already know exactly which direction gives us a non-zero result: it’s $$-\theta_o$$. In fact, we can simplify the integral and eliminate the Monte Carlo step entirely.

From another perspective, we’re using a single-sample Monte Carlo estimate of a discrete distribution over one outcome: $$-\theta_o$$. This estimator could then be extended to support BRDFs with multiple discrete elements, as well as mixed discrete/continuous BRDFs.

For mirrors, though, we can simply return incoming radiance from the reflected direction.

```
def radiance(x, θ):
hit = trace_ray(x, θ)
if hit.light:
return hit.emission
elif hit.diffuse:
θi = random(-π/2, π/2)
return (π / 2) * radiance(hit.point, hit.to_world(θi)) * cos(θi)
elif hit.mirror:
θo = hit.to_local(θ)
θi = -θo
return radiance(hit.point, hit.to_world(θi))
return 0
```


This strategy handles perfect specular reflections quite well in practice.

However, it *only* handles perfect specular reflections—we’re relying on the fact that there’s a discrete set of directions to choose from.
In any other case, we would still need to sample $$\theta_i$$ from a continuous distribution.

When $$f$$ is close to specular (i.e. near-zero everywhere except a small range of directions), uniformly sampling $$\theta_i$$ is likely to choose an irrelevant angle, which increases variance.
Handling this situation requires *importance sampling*, which we will discuss in a future chapter.

## Challenges

So far, our renderer implements *unidirectional path tracing*, which means it samples light paths starting from $$\mathbf{x}$$ and ending a light source.
This approach works well when you have diffuse materials and large lights—but consider the following scenes:

![](../../assets/c81bce84f5b60078.png)

![](../../assets/f71a84d51b96341c.png)

We’re unlikely to sample paths that intersect physically small lights, or paths that have to bounce between many surfaces before reaching a light. In the limit, sampling a point-like light is impossible—we will never choose a ray that precisely intersects the light.

Rarely sampling important paths leads to high variance.
Intuitively, finding a rare path results in a disproportionately large estimate, since it has high radiance and low probability density.
In fact, the probability density along a path decreases *exponentially* with each bounce.

In practice, our renderer struggles with these scenes, requiring tens of thousands of samples to converge.

Further, we start encountering *fireflies*: pixels that found a particularly rare path and produced a much brighter estimate than their neighbors.
With enough samples, fireflies will average out—they’re **not** a bug—but many practical renderers instead ignore paths that produce too much radiance, introducing [bias](https://thenumb.at/Monte-Carlo/#bias-and-consistency).

Uniform Monte Carlo integration makes rendering possible, but handling harder cases will require a more advanced estimator. We will explore more powerful strategies throughout the remaining chapters.

# Footnotes

For an introduction to radiometry, refer to

and*Lights and Shadows*. For a rigorous model of 2D rendering, refer to*Radiometry: I got it backwards*. Fully understanding radiometry won’t be necessary for this chapter.*Theory, analysis and applications of 2D global illumination*[↩︎](https://thenumb.at#fnref:1)This quantity is related to

*irradiance*, but ignores foreshortening (factor of $$\cos\theta$$).[↩︎](https://thenumb.at#fnref:2)This is ambiguous—what does it mean to integrate $$\mathcal{L}_i$$ at a pixel? One option is to always evaluate $$\mathcal{L}_i$$ at the pixel’s center point. Alternatively, we could reduce

[aliasing](https://en.wikipedia.org/wiki/Aliasing)by averaging $$\mathcal{L}_i$$ over the pixel area:\[ \text{Image}[x_i,y_j] = \frac{1}{2\pi(x_{i+1}-x_i)(y_{j+1}-y_j)}\int_{x_i}^{x_{i+1}}\int_{y_j}^{y_{j+1}}\int_0^{2\pi} \mathcal{L}_i(x,y,\theta)\, d\theta\, dy\, dx \]Our renderer will estimate this average by uniformly sampling $$\mathbf{x}$$ within each pixel. In signal processing terms, we’re

[convolving](https://www.youtube.com/watch?v=KuXjwB4LzSA)our signal with a[box filter](https://en.wikipedia.org/wiki/Box_blur). Using[another filter](https://en.wikipedia.org/wiki/Filter_(signal_processing))with wider[support](https://en.wikipedia.org/wiki/Support_(mathematics))could further reduce aliasing, and can be[easily integrated](https://research.nvidia.com/publication/2024-05_filtering-after-shading-stochastic-texture-filtering)into a Monte Carlo rendering pipeline.[↩︎](https://thenumb.at#fnref:3)You might see $$f_\mathbf{s}$$ referred to as a “

[BxDF](https://en.wikipedia.org/wiki/Bidirectional_scattering_distribution_function#Overview_of_the_BxDF_functions)” for some x other than reflectance, depending on its domain.[↩︎](https://thenumb.at#fnref:4)More rigorously, $$f_\mathbf{s}$$ is the ratio of incoming

*differential irradiance*to outgoing*radiance*. The factor of $$\cos\theta_i$$ converts the incoming radiance $$\mathcal{L}$$ to differential irradiance at $$\mathbf{s}$$.[↩︎](https://thenumb.at#fnref:5)We can’t get more light out of a point than goes in, so $$\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} f_\mathbf{s}(\theta_o,\theta_i)\cos\theta_i\, d\theta_i \le 1$$ for all $$\theta_o$$. For a perfectly diffuse surface, $$f$$ is a constant such that this integral is equal to one, so $$f = \frac{1}{2}$$. In three dimensions, we would have $$f = \frac{1}{\pi}$$ for equivalent reasons.

[↩︎](https://thenumb.at#fnref:6)From another perspective, our recursive procedure generates one sample of the space of all light paths. We then integrate over the space of paths using a single Monte Carlo estimator, which we know converges with $$\frac{1}{\sqrt{N}}$$. We will discuss this approach in more detail in a future chapter.

[↩︎](https://thenumb.at#fnref:7)Actually, at a microscopic level,

*all*reflections are specular—what we perceive as diffuse reflection is the[aggregate distribution](https://cs.dartmouth.edu/~wjarosz/publications/seyb24from.pdf)of directions in which a*rough*specular surface scatters light. Further, if the surface has geometric features on the scale of the wavelength of light,[interesting things](https://en.wikipedia.org/wiki/Iridescence)can happen.[↩︎](https://thenumb.at#fnref:8)