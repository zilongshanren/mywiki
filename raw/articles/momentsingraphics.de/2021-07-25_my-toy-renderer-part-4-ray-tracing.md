---
title: 'My toy renderer, part 4: Ray tracing'
url: http://momentsingraphics.de/ToyRenderer4RayTracing.html
published: '2021-07-25'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My toy renderer, part 4: Ray tracing

Part 4 of this [series about my toy renderer](http://momentsingraphics.de/ToyRendererOverview.html) is all about ray traced shadows. In particular, I discuss direct lighting with [polygonal](http://momentsingraphics.de/Siggraph2021.html) and [linear lights](http://momentsingraphics.de/HPG2021.html) for diffuse and specular surfaces. I have described the corresponding methods in two recent research papers but this post is written with a broader audience in mind. While the papers focus on the mathematical derivation of the algorithms, this post starts with some basics of physically-based rendering and explains in detail why there is a need for these algorithms and how they can be used in a renderer.

## Ray queries

Obviously, ray traced shadows require ray tracing. Thankfully, that has gotten much faster and easier with the introduction of dedicated ray tracing hardware and graphics APIs that expose this hardware. In Vulkan, three extensions come into play: [VK_KHR_acceleration_structure](https://vulkan.lunarg.com/doc/view/1.2.182.0/linux/1.2-extensions/vkspec.html#VK_KHR_acceleration_structure), [VK_KHR_ray_tracing_pipeline](https://vulkan.lunarg.com/doc/view/1.2.182.0/linux/1.2-extensions/vkspec.html#VK_KHR_ray_tracing_pipeline) and [VK_KHR_ray_query](https://vulkan.lunarg.com/doc/view/1.2.182.0/linux/1.2-extensions/vkspec.html#VK_KHR_ray_query). These supersede various vendor specific or provisional extensions.

Setting up an acceleration structure for ray tracing is a little cumbersome. You have to manage a lot of staging buffers, scratch memory, intermediate geometry copies, instance data and so forth but writing [this code](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/scene.c#L135) once is not so bad. Every time my renderer loads a scene, it constructs a single bottom-level acceleration structure that contains all the geometry of that scene. It also creates a single top-level acceleration structure, which holds a single untransformed instance of that bottom-level acceleration structure. Since my scenes are completely static, that is all I need.

For the actual ray tracing, we have two options called ray tracing pipelines and ray queries in Vulkan. Ray tracing pipelines add five new shader types to the API: Ray generation, intersection, any hit, closest hit and miss shader. I'm afraid at this rate, the 32 bits in [VkShaderStageFlagBits](https://vulkan.lunarg.com/doc/view/1.2.182.0/linux/1.2-extensions/vkspec.html#VkShaderStageFlagBits) won't last much longer. Although this programming model feels quite natural for the implementation of a path tracer, its reputation has suffered. Apparently, the driver essentially takes all the shaders used in a ray tracing pipeline and fuzes them into an uber shader. Anis Benyoub described the resulting performance issues in a [talk at SIGGRAPH 2019](https://advances.realtimerendering.com/s2019/Benyoub-DXR%20Ray%20tracing-%20SIGGRAPH2019-final.pdf) (as part of [Advances in Real-Time Rendering](https://advances.realtimerendering.com/s2019/index.htm)). Another issue is that it takes a lot of additional Vulkan boilerplate code to set up all these different shader types.

Thus, ray queries were conceived. Their concept is so much simpler: Start a ray query from any shader, write a while loop to figure out which potential intersections to accept and then query their meta data to do shading. Instead of spreading the functionality across (up to) five different shader types, there's just a little loop. Fragment shaders can take the role of ray generation shaders, intersection shaders and any hit shaders live inside the while loop and after that an if-else branch can implement functionality of closest hit and miss shaders.

In my particular case, I do not even need the loop. I only cast shadow rays and there is [no alpha test](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#No_alpha_testing). I just figure out whether an intersection exists:

```
rayQueryEXT ray_query;
rayQueryInitializeEXT(ray_query,
g_top_level_acceleration_structure,
gl_RayFlagsTerminateOnFirstHitEXT | gl_RayFlagsOpaqueEXT | gl_RayFlagsSkipClosestHitShaderEXT,
0xFF, shading_position, min_t,
sampled_dir, max_t);
rayQueryProceedEXT(ray_query);
bool occluder_hit =
(rayQueryGetIntersectionTypeEXT(ray_query, true)
!= gl_RayQueryCommittedIntersectionNoneEXT);
```


Note the various flags to indicate that the first hit terminates traversal. Overall, I find this API much more pleasant than the one for ray tracing pipelines. It simply takes much less code to get to the point where rays can be traced. And even if I cared about more than shadows, the generic way in which I handle shading for the visibility buffer is also absolutely applicable to ray queries. Thus, there is no point in having closest hit shaders. Besides, characteristics of the shaders that impact performance are easier to control.

Speaking of performance, there's something that I found to be quite crucial although I still don't have really clear recommendations. It can make a big difference whether ray queries are invoked inside a loop or not (resp. in an unrolled loop). The unroll directive in the GLSL extension GL_EXT_control_flow_attributes does not reliably give the same result as manual copying of all runs through the loop. Thus, I have a (somewhat terrible) [solution with the preprocessor](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/unrolling.glsl). For very low sample counts, unrolling offers a major performance gain. At some point, instruction cache misses become a concern and a loop is faster. Thus, I don't want to make a recommendation along the lines of “unroll always” but it's definitely something to investigate with profiling.

## First steps with ray tracing

In my experience, when graphics developers get their hands on ray tracing, it takes roughly a day until they've used it for soft shadows, ambient occlusion and glossy reflections. Of course, these implementations won't be ready to ship in a product. It's just incredibly tempting to try them. With rasterization, each of these effects is a bottomless pit where you can combat artifacts for years. But once you employ ray tracing, a huge number of problems is swept away immediately. Shadows don't alias. Soft shadows get proper penumbras. Ambient occlusion and reflections account for surfaces that aren't on screen. It's freeing.

That's not to say that everything is simple with ray tracing. Ray tracing comes with the promise of increased realism but it can be difficult to get the physics of light transport and the intricacies of Monte Carlo integration right. While methods based on rasterization have their flaws, they have become very familiar. With ray tracing, many developers are entering a whole different branch of graphics research and practice. We are seeing a convergence of methods between offline and real-time rendering. Offline rendering is starting to embrace GPU acceleration while path tracing is gaining traction in real-time rendering. Practitioners on both sides will have to learn new tricks to advance the field. It's exciting but maybe also a little intimidating.

## Soft shadows for polygons

As a specific example of how ray tracing can get complicated, I want to speak about soft shadows for a polygonal area light (see [Figure 1](http://momentsingraphics.de#SoftShadowExample)). That should not be too hard with ray tracing, right? Sample a bunch of points on the polygon randomly, cast shadow rays towards these points and multiply the shading by the ratio of unshadowed rays. Of course, it helps to use some stratification (see the [previous post](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#Stratified_random_numbers_blue_noise_)) and denoising will be needed for good results at low sample counts.

![SoftShadowExample](../../assets/5fb8140d981c6026.webp)

**Figure 1:**An attic lit by a polygonal area light with five vertices (the window). Shadows are ray traced at 128 samples per pixel using

[my methods](http://momentsingraphics.de/Siggraph2021.html). Even at this high sample count, rendering takes only 33 ms (at 1440² on an RTX 2080 Ti).

This approach leaves two important questions unanswered: How should the points be distributed on the polygon and how do we compute shading anyway? The latter question is easily answered for point lights but not so easily for polygonal lights. I will get to that shortly but first let us look at the distribution of samples.

## Area sampling for polygons

The most obvious approach is to sample the area of the polygon uniformly (but we will see below that other strategies are much better). That means that a subset of the polygon that has half the area is expected to receive half of the samples. To implement that, we need a method that maps two uniform random numbers in \([0,1)\) to a single point on the polygon. This way, there is a generic interface to the source of random numbers. We can easily exchange it, e.g. for a solution that [pushes noise into higher frequencies](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#Stratified_random_numbers_blue_noise_) [[Ahmed2020]](http://momentsingraphics.de#_Ahmed2020). If the polygon is triangulated, we can precompute the size of the area for each triangle \(A_0,\ldots,A_{m-3}>0\), where \(m\in\mathbb{N}\) is the vertex count of the polygon. Then we use the first random number \(\xi_0\in[0,1)\) to decide which triangle we want to sample. We pick the triangle index \(j\in\{0,\ldots,m-3\}\) such that

In other words, the random number multiplied by the total area of the polygon lies between the summed area of the first \(j\) triangles and the summed area of the first \(j+1\) triangles. This way, the probability to pick triangle \(j\) is proportional to the area of that triangle \(A_j\), which is what we wanted.

We are not done with the first random number yet. We still need it to pick a point inside the chosen triangle. From the inequalities above, we know which range it is in, so we can simply remap it to the range from \([0,1)\) to allow reuse:

\[\xi_0^\prime := \frac{\xi_0 \sum_{k=0}^{m-3} A_k - \sum_{k=0}^{j-1} A_k}{A_j}\in[0,1)\]## Area sampling for triangles

Now we have to pick a point from the triangle. We know its vertices \(v_0,v_1,v_2\in\mathbb{R}^3\). It is easy to come up with formulas that map random numbers \(\xi_0^\prime,\xi_1\in[0,1)\) to that triangle. For example, we can first interpolate linearly along one edge and then linearly away from the remaining vertex:

\[(1-\xi_1)v_0 + \xi_1((1-\xi_0^\prime) v_1 + \xi_0^\prime v_2)\]The problem is that this strategy does not give uniform samples as is evident from [Figure 2](http://momentsingraphics.de#WrongAreaSampling).

A correct formula for area sampling of triangles is [[Turk1992]](http://momentsingraphics.de#_Turk1992)

[Figure 3](http://momentsingraphics.de#CorrectAreaSampling) shows the result, which looks much more uniform indeed. Intuitively, the problem is that the first formula places as many samples in the point \(v_0\) as on the edge \(v_1,v_2\). But the square root \(\sqrt{\xi_1}\) grows rapidly at 0, so it reduces the density at \(v_0\). The most common way to construct such methods rigorously is inverse function sampling. [Chapter 13.4](https://pbr-book.org/3ed-2018/Monte_Carlo_Integration/Sampling_Random_Variables) and [13.6 of Physically-Based Rendering](https://pbr-book.org/3ed-2018/Monte_Carlo_Integration/2D_Sampling_with_Multidimensional_Transformations) provide a decent explanation.

For rectangles or parallelograms, the problem can be solved more easily but we stick with the general case of triangulated polygons.

## The rendering equation

Now we know how to sample the area of a polygon uniformly but we are still far from done. If the area light is equally bright everywhere, area sampling seems reasonable at first but there is a problem: Not all parts of the area light contribute equally to the shading of a particular point on a surface. Some parts of the area light may be closer than others. Some may be seen at a grazing angle or their light may reach the surface at a grazing angle. And if the surface is specular, some parts of the area light may be exactly at the main reflection direction such that they contribute heavily to the specular highlight while other parts don't.

If we just trace shadow rays to uniform points on the area and multiply shading by the ratio of unshadowed shadow rays, we pretend that all these effects don't exist. For small, distant lights and diffuse shading, that's an acceptable approximation but in many cases the error is considerable. Besides, we still don't have a plan for how to compute shading for the area light in the first place.

To get all these things right, we need the rendering equation. This marvelous formula conveys most problems in rendering concisely and correctly. At the same time, it maps to an implementation in a path tracer naturally. There are some generalizations, e.g. for subsurface scattering or participating media but our concern is direct lighting of surfaces, so the rendering equation is all we need. Here it is:

\[L(x,\omega_o)=L_{e}(x,\omega_o)+\int_{\mathbb{S}^2}L_{i}(x,\omega_i)f_{r}(\omega_i,x,\omega_o)|n(x)\cdot\omega_i|\mathrm{d}\omega_i\]Let's go through this term by term. We want to compute the radiance \(L(x,\omega_o)\) emanating from a point on a surface \(x\in\mathbb{R}^3\) towards a direction \(\omega_o\in\mathbb{S}^2\). \(\mathbb{S}^2\subset\mathbb{R}^3\) is simply the set of all normalized direction vectors, i.e. the unit sphere. Intuitively, radiance is what an idealized camera with infinitesimally small aperture, pixel area and exposure time measures. The pinhole cameras that we commonly use in real-time rendering match all these simplifications. In other words, \(L(x,\omega_o)\) is the color that you see when you are at point \(x\) and look in direction \(\omega_o\).

The surface may emit light by itself, so we have the term \(L_e(x,\omega_o)\) to contribute the emitted radiance. For points on our polygonal area light, this term would be non-zero but for other surfaces in the scene where we want to compute the shading it is usually irrelevant.

We are more concerned with reflected light. The surface point \(x\) can receive light from all directions and may reflect it towards the camera. Thus, we have to compute an integral over all directions, i.e. over \(\mathbb{S}^2\). It's an integral over the area of the unit sphere, which also goes by the name solid angle. The variable of integration is the direction from which we receive light \(\omega_i\in\mathbb{S}^2\). If light comes in at a grazing angle, it is spread out over a larger area. Thus, it contributes less to the reflected light of the point \(x\). To account for this effect, we take the dot product between the shading normal \(n(x)\in\mathbb{S}^2\) and the incoming light direction \(\omega_i\). This kind of weighted integration over the unit sphere is known as projected solid angle measure.

Of course, we need to know how much light point \(x\) actually receives from direction \(\omega_i\). Thus, one factor in the integrand is \(L_i(x,\omega_i)\), which gives the incoming radiance at point \(x\) from direction \(\omega_i\). A path tracer, determines this incoming radiance recursively by tracing a ray from \(x\) towards \(\omega_i\) and computing the outgoing radiance at the intersected point for direction \(-\omega_i\). We are more concerned with direct lighting. Thus, we just have to figure out whether the ray intersects the polygonal area light. If so, we evaluate \(L_e\) at this intersection point (which may be as simple as using a constant value).

Finally, there is the bidirectional scattering distribution function (BSDF) \(f_r(\omega_i,x,\omega_o)\), which is a slight generalization of the bidirectional reflectance distribution function (BRDF). The BSDF supports transparent surfaces because light reaching the surface from below can get refracted to the top. In what follows, we assume that a BRDF is used, so \(f_r(\omega_i,x,\omega_o)\) is zero unless \(n(x)\cdot\omega_i>0\) and \(n(x)\cdot\omega_o>0\). In particular, we can limit the integral to the hemisphere around \(n(x)\). BRDFs are a common concept in real-time rendering these days. They tell us how much light gets reflected from direction \(\omega_i\) towards direction \(\omega_o\). My renderer uses the [Frostbite BRDF](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#Frostbite_BRDF).

And that's the rendering equation. The whole problem of computing direct and indirect illumination expressed in one line of math. We just integrate over all the incoming light, weighting it appropriately for the outgoing direction. In particular, it tells us how to weight the contribution of each part of our area light. However, one aspect of that weighting is easily overlooked, so keep reading.

## Monte Carlo integration with area sampling

Back to the problem at hand: For simplicity, suppose that the polygonal area light emits a constant radiance \(L_e\) into all directions and at each point on its area. That's called a Lambertian emitter. We disregard indirect illumination. Thus, we set

\[L_i(x,\omega_i)=L_eV(x,\omega_i),\]where \(V(x,\omega_i)=1\) when the area light is visible from point \(x\) in direction \(\omega_i\) and \(V(x,\omega_i)=0\) otherwise. In practice, we only ever generate shadow rays towards points on the light, so this visibility term is one if and only if the shadow ray doesn't hit any occluder.

Above, we considered area sampling of the polygon. With that method, we can generate a random point \(y\) that is distributed uniformly over the area of the polygon \(\mathbb{P}\subset\mathbb{R}^3\). But we cannot use that point in the rendering equation. We need a normalized direction vector \(\omega_i\) towards that point. Thus, we set

\[\omega_i:=\frac{y-x}{\|y-x\|}\in\mathbb{S}^2.\]To use this random direction for an estimate of the integral in the rendering equation, we need Monte Carlo integration. We estimate the integral

\[\int_{\mathbb{S}^2}L_e V(x,\omega_i)f_{r}(\omega_i,x,\omega_o)|n(x)\cdot\omega_i|\mathrm{d}\omega_i\]through the single-sample Monte Carlo estimate

\[\frac{L_e V(x,\omega_i)f_{r}(\omega_i,x,\omega_o)|n(x)\cdot\omega_i|}{p(\omega_i)}.\]We can repeat that and take the average of these random results to reduce the noise in this estimate. Eventually, the error approaches zero.

In that estimate, we divide by \(p(\omega_i)\), which is supposed to be the probability density function for samples \(\omega_i\) on the unit sphere. Probability densities are related to probabilities but they are not the same thing. If we want to know the probability that \(\omega_i\) falls into a set \(\mathbb{A}\subset\mathbb{S}^2\), we can compute that from the probability density function via the integral

\[\int_{\mathbb{A}} p(\omega_i)\mathrm{d}\omega_i.\]In particular, the probability density function is normalized such that

\[\int_{\mathbb{S}^2} p(\omega_i)\mathrm{d}\omega_i = 1.\]Nonetheless, probability densities can be greater than one in the same way that specular BRDFs take values far greater than one although they satisfy energy conservation. Like probabilities, probability densities don't take negative values.

A beginners mistake is to think that \(p(\omega_i)\) must be constant in our case because the distribution on the area of the polygon is uniform. It's true, that the density for \(y\) on the area \(\mathbb{P}\) is constant (with respect to the area measure). But \(\omega_i\) is not \(y\) and \(\mathbb{S}^2\) is not \(\mathbb{P}\). As we compute \(\omega_i\) from \(y\), we warp the distribution of the points. [Figure 4](http://momentsingraphics.de#AreaSamplesOnSphere) illustrates this problem. The projection of more distant parts of the triangle is smaller but per area of the polygon, these regions receive the same number of samples. Thus, samples on the unit sphere are more dense.

![AreaSamplesOnSphere](../../assets/6854f2919dcd113b.svg)


**Figure 4:**Samples that are uniform on the area of the polygon won't be uniform as direction vectors on the unit sphere.

We have to convert the density from the area measure of the polygon to the area measure of the unit sphere around point \(x\), which is called solid angle measure. The sampled density with respect to the area measure is simply the reciprocal of the total area of the polygon because it is constant and integrates to one:

\[\frac{1}{A_\Sigma} := \frac{1}{\sum_{j=0}^{m-3} A_k}\]To convert to solid angle measure, we apply a correction factor that depends on the distance and on the dot product between \(\omega_i\) and the normal \(n_l\in\mathbb{S}^2\) of the polygon:

\[p(\omega_i) = \frac{1}{A_\Sigma} \frac{\|x-y\|^2}{|n_l\cdot\omega_i|}\]This conversion factor is a standard result in graphics. The factor \(\|x-y\|^2\) is much like the square falloff of point lights. As the distance to \(x\) grows, the area of the projection of the polygon on the unit sphere shrinks quadratically. The dot product is necessary because an area that you see from the side is an area that you do not see at all. The size of the projection to the unit sphere is proportional to the dot product with the normal vector.

Now that we have the correct density, we can put together the whole Monte Carlo estimate:

\[L_e V(x,\omega_i)f_{r}(\omega_i,x,\omega_o) \frac{|n(x)\cdot\omega_i| |n_l\cdot\omega_i|}{\|x-y\|^2} A_\Sigma.\]That's proper physically-based shading. Each sample is weighted correctly and if we take enough samples, the result will converge to the true integral in the rendering equation, i.e. it is unbiased.

## Solid angle sampling

The thing is, we are doing real-time rendering and with the approach described above, we might not have the time to take “enough samples.” [Figure 5](http://momentsingraphics.de#AreaSamplingResult) shows an example that provokes problems. The area light is fairly big and some of the surfaces are close to it. Especially on these surfaces, we get a lot of noise. They appear darker than they should because some pixels are almost black while others are much brighter than the brightest sRGB white. The method is unbiased but clamping of sRGB introduces bias. The main source of noise is that there is a lot of variation in \(\|x-y\|^2\) because parts of the area light are really close while others are far away. On top of that, the two dot products introduce additional variation.

![AreaSamplingResult](../../assets/0ce02bc3f5c5c881.webp)


![AreaSamplingResult](../../assets/0ce02bc3f5c5c881.webp)

**Figure 5:**A Cornell box with a long rectangular light near the ceiling. With area sampling, we get considerable noise, especially in spots close to the light source.

One could argue that this happens mostly in overexposed parts of the scene near the area light. If the pixel is going to be white anyway, it shouldn't matter whether there is some noise in its value. But this argument fails as soon as we consider indirect illumination. A lot of indirect light comes from walls or ceilings that are lit by nearby area lights. If we introduce a lot of noise whenever we estimate this direct lighting, path tracing is going to propagate the noise throughout the scene.

It is definitely worthwhile to look for better strategies. In fact, an option that is much better than area sampling has been around for a long time: Solid angle sampling [[Arvo1995]](http://momentsingraphics.de#_Arvo1995). Solid angle sampling means that we distribute samples uniformly in the projection of the polygon onto the unit sphere. Thus, the density \(p(\omega_i)\) is constant. If the solid angle (i.e. the area of the projection to the unit sphere) has size \(S>0\), the density is

Then the Monte Carlo estimate is

\[L_e V(x,\omega_i)f_{r}(\omega_i,x,\omega_o) |n(x)\cdot\omega_i| S.\]The distance term and one of the dot products are gone. As expected, the results in [Figure 6](http://momentsingraphics.de#SolidAngleSamplingResult) are much better. However, they are still not perfect. Essentially, the dot product \(n(x)\cdot\omega_i\) can cause the same kind of problems that we had before. On the red wall, it is zero for some points on the polygon but bigger for others. Some samples get weighted down heavily while others don't. The result is noise.

![SolidAngleSamplingResult](../../assets/31e441cfc3283f39.webp)

**Figure 6:**Using solid angle sampling instead of area sampling improves results considerably but there is still noise when \(n(x)\cdot\omega_i\) has a lot of variation.

Deriving solid angle sampling is more tricky than deriving area sampling. In area sampling, we only care about a triangle. With solid angle sampling, we consider the triangle in relation to a point \(x\). But that has been solved a long time ago [[Arvo1995]](http://momentsingraphics.de#_Arvo1995). Unfortunately, this algorithm has always been a bit unstable and expensive. For small triangles far away from the shading point, the involved floating point numbers might underflow to zero and then the end result will be not a number. In these cases, area sampling works fine but using an if-statement to switch from one to the other is annoying. The good news is that I [looked into it](http://momentsingraphics.de/Siggraph2021.html) and developed a version of [solid angle sampling that is faster and more robust](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/polygon_sampling.glsl#L114).

## Projected solid angle sampling

Making solid angle sampling better is not the only thing I did in my [recent paper](http://momentsingraphics.de/Siggraph2021.html). Above, we observed that the factor \(n(x)\cdot\omega_i\) in the Monte Carlo estimate is a bit of a problem because it causes noise. It would be nice to get rid of it, wouldn't it? To accomplish that, we need a density \(p(\omega_i)\) that is proportional to \(n(x)\cdot\omega_i\). Defining that density is easy but figuring out how to map random numbers \(\xi_0,\xi_1\) to the unit sphere in such a way that they are distributed according to that density is much harder. But that's exactly what I did.

If you want to know how, you'll have to [read the paper](http://momentsingraphics.de/Siggraph2021.html). I put a lot of effort into that explanation and won't repeat it here. But at least now you know why it's worth it. If you don't care about the internals but I've convinced you to use this method, there's BSD-licensed code for you to copy. The key methods are [prepare_projected_solid_angle_polygon_sampling()](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/polygon_sampling.glsl#L508) and [sample_projected_solid_angle_polygon()](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/polygon_sampling.glsl#L742). Before you invoke them, you have to make sure that the vertices of the polygon are ordered the right way, given in a coordinate frame where the normal is \(n(x)=(0,0,1)^\mathsf{T}\) and clipped to the half-space \(z\ge0\). Also, the polygon has to be convex.

The method provides a sampled direction \(\omega_i\) and the projected solid angle of the polygon \(P>0\). The density is

\[\frac{n(x)\cdot\omega_i}{P},\]so the Monte Carlo estimate is simply

\[L_e V(x,\omega_i)f_{r}(\omega_i,x,\omega_o) P.\]That's looking pretty good. On diffuse surfaces, the BRDF is nearly constant (Lambertian diffuse is exactly constant, other BRDFs don't stray too far). Thus, there can't be a lot of variation in the results. Either the result is black because the shadow ray hit an occluder or it's the product of emitted radiance, BRDF and projected solid angle, all of which are (nearly) constant. For a Lambertian diffuse BRDF, this product of constants is exactly the color of reflected light. Essentially, we've computed the unshadowed shading in a way similar to linearly transformed cosines [[Heitz2016]](http://momentsingraphics.de#_Heitz2016). But since we sneak this shading integral into the sampled density, Monte Carlo integration can be used so that we get physically-based soft shadows. [Figure 7](http://momentsingraphics.de#ProjectedSolidAngleSamplingResult) shows the result. As expected, the only strong noise occurs in penumbras.

![ProjectedSolidAngleSamplingResult](../../assets/0a19faf6083eb1b8.webp)

**Figure 7:**Using projected solid angle sampling, we get almost no noise on diffuse surfaces, except in penumbras.

## LTC importance sampling

For diffuse shading, we are all set. However, specular BRDFs still cause major problems as shown in [Figure 8](http://momentsingraphics.de#RoughnessPlanesDiffuse). The sampling strategy doesn't really know anything about the BRDF. All it cares about is that it wants to hit the polygon and it wants to sample proportional to \(n(x)\cdot\omega_i\). If that direction happens to be close to the main reflection direction where the specular BRDF takes large values, that's sheer luck. But we only get lucky every once in a while. The result are scattered dots with extremely large specular shading in places where we would want a smooth specular highlight.

![RoughnessPlanesDiffuse](../../assets/363a546cf444c647.webp)

**Figure 8:**Projected solid angle sampling fails to sample the lobe of a specular BRDF often enough. The three planes get smoother from left to right. The lower the roughness, the bigger the problem.

A standard strategy to resolve this problem is BRDF sampling. For GGX-based materials, an efficient solution is available [[Heitz2018]](http://momentsingraphics.de#_Heitz2018). The sampled density is almost proportional to \(f_r(\omega_i,x,\omega_o)|n(x)\cdot\omega_i|\), i.e. BRDF and cosine term. However, this strategy knows nothing about the whereabouts of the polygonal light. If we want a contribution to direct lighting, we have to be lucky and relying on luck is generally the last thing we want to do in real-time path tracing.

If we could make a wish, it would be a sampling strategy that samples proportional to *all* factors in the rendering equation. But we should stay realistic, we probably can't sample proportional to the visibility term because that requires knowledge of the whole scene. So what we want is a density satisfying

but only for directions \(\omega_i\) that point towards the polygon. For other directions, the density should be zero because they do not contribute to direct lighting.

The stunning thing, is that it's actually easy to get very close to such a strategy with what we've got so far. In the [previous post](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#Linearly_transformed_cosines_LTCs_), I discussed linearly transformed cosines (LTCs) [[Heitz2016]](http://momentsingraphics.de#_Heitz2016). With LTCs, we get good approximations to commonly used specular BRDFs, e.g. the Frostbite BRDF. We approximate the specular BRDF by starting with a cosine distribution (such as the one that we sample with projected solid angle sampling) and distorting the sampled density through a linear transformation of direction vectors. So if we first apply the inverse transform to our polygon, sample that proportional to a cosine and then transform back, we have sampled the polygon proportional to an LTC. And if the LTC approximates \(f_r(\omega_i,x,\omega_o)|n(x)\cdot\omega_i|\) (it does), that means that we get close to sampling the ideal sampling density above.

If we assume, that the LTC provides a perfect approximation, our Monte Carlo estimate for specular shading becomes extremely compelling:

\[V(x,\omega_i) U,\]where \(U\) is the estimate for unshadowed shading according to LTCs. Again, penumbras are the only source of noise. And we do not even need the assumption of a perfect fit. We can use the correct BRDF and get unbiased shading but that takes a few extra steps.

## Combining diffuse and specular

In most cases, we use BRDFs that combine a diffuse and a specular component. Since we have one sampling strategy that works well for diffuse and one that works well for specular, we should take one sample with each strategy and combine the results. Of course, we can also use different sample counts, e.g. two for diffuse and one for specular.

Combining the results is more easily said than done when we want unbiased rendering. One idea would be to only evaluate the diffuse BRDF for diffuse samples and only the specular BRDF for specular samples. In the end, we just add up the results. But this approach is biased and suboptimal. It is biased because the sampling density that we get with LTC sampling is zero in parts of the upper hemisphere. In general, the correct specular BRDF will have a small but positive value in these parts. By using a zero density, in these parts, we are not integrating over them and thus the integral is incomplete and biased. Besides, we may get fireflies when we divide by a density that is close to zero where the BRDF is moderately big.

The second problem is that specular shading doesn't contribute much in most locations. Specular highlights are really bright but the farther we move away from them, the darker the specular contribution gets. Thus, we go through a lot of effort to compute a sampled direction and to trace a shadow ray and then in the end, we multiply this contribution by a small factor because specular shading just can't contribute much to that pixel. Wasting work like that is a shame.

To overcome these problems, we have to look into multiple importance sampling (MIS) [[Veach1995]](http://momentsingraphics.de#_Veach1995). The idea is that we treat the combination of both sampling strategies as though they were a single sampling strategy with a combined density. For our purposes, a certain type of MIS is particularly interesting: A weighted balance heuristic. Let's say we take one sample \(\omega_0\) with projected solid angle sampling (density \(p_0(\omega_i)\)) and another one \(\omega_1\) with LTC sampling (density \(p_1(\omega_i)\)). We have also defined two weights \(c_0,c_1>0\). Then the MIS estimate (which generalizes our single-sample Monte Carlo estimate) is

It adds up contributions from both samples. But for both samples, it evaluates the full BRDF (with diffuse and specular components). Similarly, instead of dividing only by the density used to produce this sample, it mixes both densities together. It looks like a Monte Carlo estimate that uses the mixed density \(c_0 p_0(\omega_j) + c_1 p_1(\omega_j)\) and that's essentially what it is. The nice thing is that this pattern is provably unbiased as long as \(c_0,c_1>0\) [[Veach1995]](http://momentsingraphics.de#_Veach1995).

Now the question is how we should choose \(c_0,c_1>0\). One possibility is to ensure that

\[\frac{f_r(\omega_i,x,\omega_o) |n(x)\cdot\omega_i|}{c_0 p_0(\omega_i) + c_1 p_1(\omega_i)}\]is as close to being constant as possible. After all, \(p_0(\omega_i)\) approximates the diffuse BRDF times \(n(x)\cdot\omega_i\) and \(p_1(\omega_i)\) approximates the specular BRDF times \(n(x)\cdot\omega_i\). We just have to apply the correct weights. Doing [the math](http://momentsingraphics.de/Siggraph2021.html) right, it turns out that \(c_0\) and \(c_1\) have to be the LTC-based estimates of diffuse and specular shading, respectively. These are side-products of the sampling computation, so this strategy is efficient. It also works well, as long as we look at fully lit surfaces, as shown in [Figure 9](http://momentsingraphics.de#RoughnessPlanesWeighted).

![RoughnessPlanesWeighted](../../assets/956569164b8d50dd.webp)

**Figure 9:**The weighted balance heuristic combines diffuse and specular samples in a way that is optimal when there are no penumbras.

However, this strategy does not solve the problem that specular samples don't contribute much unless we are looking at a specular highlight. In parts where specular shading is dark, \(c_1\) is much smaller than \(c_0\), so the specular samples get weighted down. In fully lit regions that is not a problem because the whole Monte Carlo estimate is nearly constant but in penumbras it matters. Many pixels where the diffuse ray is occluded but the specular ray isn't will be almost black. Another way to look at it is that the goal of making

\[\frac{f_r(\omega_i,x,\omega_o) |n(x)\cdot\omega_i|}{c_0 p_0(\omega_i) + c_1 p_1(\omega_i)}\]nearly constant neglects the visibility term \(V(x,\omega_j)\). As soon as visibility isn't constant (i.e. in penumbras), optimizing for this goal isn't optimizing for image quality.

Thus, it's worthwhile to think about the other extreme. It could be useful if the MIS heuristic treats diffuse and specular samples in exactly the same manner. If the contribution of a sample only depends on the sampled direction \(\omega_i\) but not on the technique that produced this sample, both techniques help us equally to get better penumbras. And getting such a strategy is easy, we just set \(c_0=c_1=1\). The result is the standard balance heuristic shown in [Figure 10](http://momentsingraphics.de#RoughnessPlanesBalance). For this example with fully lit surfaces, it is not so great but penumbras look better (see Figure 10 in [the paper](http://momentsingraphics.de/Siggraph2021.html)).

![RoughnessPlanesBalance](../../assets/7383196fdc812cfa.webp)

**Figure 10:**The standard balance heuristic combines diffuse and specular samples in a way that treats samples from both techniques equally.

I've searched for ways to get the best of both worlds for quite some time. That can be made arbitrarily complicated by embracing optimal multiple importance sampling [[Kondapaneni2019]](http://momentsingraphics.de#_Kondapaneni2019). But I like to [keep it simple](http://momentsingraphics.de/ToyRenderer1KeepItSimple.html), remember? Thus, the solution that I settled for is to use a linear blend between the standard balance heuristic and the weighted balance heuristic. Through the interpolation coefficient \(v\in[0,1]\), there is an intuitive way to make tradeoffs. I always set it to \(v=\frac{1}{2}\). [Figure 11](http://momentsingraphics.de#RoughnessPlanesClamped) shows the result of this so-called clamped optimal MIS. It's worse than the weighted balance heuristic in this example but would look better in penumbras. I'm quite happy with this approach.

![RoughnessPlanesClamped](../../assets/602882cc6467df36.webp)

**Figure 11:**Clamped optimal MIS takes the result half way between the standard balance heuristic and the weighted balance heuristic. Results in fully lit regions are fairly good while specular samples still make a reasonable contribution everywhere.

## Textures and portals

So now we've got good soft shadows for polygonal lights and diffuse and specular shading. That's pretty good but we can do more with it. Above, I said that we assume a constant emitted radiance \(L_e\) for the area light. There's no particularly good reason for this assumption. Of course, it's nice to be able to say that we get zero noise outside penumbras if the LTC fit is perfect. But maybe we'd be willing to accept a little bit of noise for more interesting shading. We have that option and there are several interesting things that we can do with it.

Firstly, we can map a texture onto the surface of an area light. That's extremely useful if we want to use displays as light source ([Figure 12](http://momentsingraphics.de#TexturedLight)). And all it takes is a texture lookup for each sample to figure out what \(L_e(x,\omega_i)\) should be. Of course, the sampling strategies know nothing about this texture, so this texture isn't canceled out when we divide by the density. But as long as the dynamic range in the texture isn't too big, it only adds moderate noise.

![TexturedLight](../../assets/91fd1515f2d4b762.webp)

**Figure 12:**An area light with a texture mapped onto its surface to control the emission color.

We can also let the emission color depend on the sampled direction \(\omega_i\) itself. One way to do that is to use an emission profile for each point on the area light. [Figure 13](http://momentsingraphics.de#IESProfileLight) uses a measured IES profile, stored in a texture. Transitions between regions of different brightness become a bit noisy but the emission profile adds a lot of realism.

![IESProfileLight](../../assets/42610a83018fdd36.webp)

**Figure 13:**An area light with an IES profile defining its emission.

Probably, the fanciest way to use non-constant emission is to use the light source as portal [[Bitterli2015]](http://momentsingraphics.de#_Bitterli2015). [Figure 14](http://momentsingraphics.de#PortalLight) uses a lookup in [a low-contrast light probe](https://hdrihaven.com/hdri/?c=low%20contrast&h=fish_hoek_beach). Thus, the light turns into a window and we get entirely realistic shading from the light probe through that window with little noise. The radiance behind that portal doesn't have to come from a texture. It can also be determined recursively by a path tracer. I haven't experimented with that yet but it could be a pretty good way to ensure that rooms receive indirect lighting from a more brightly lit adjacent room.

![PortalLight](../../assets/7ec05b6938738748.webp)

**Figure 14:**An area light used as portal that shows a light probe.

## Linear lights

Convex polygonal lights are fairly flexible but cannot approximate every shape well. Besides, the cost of my sampling methods for polygons is not unreasonable but significant in the context of real-time rendering. It makes sense to consider some special cases and to optimize for them. Linear lights are such a special case.

Like point lights, linear lights are somewhat degenerate. To define them, we start with a cylinder, acting as Lambertian emitter ([Figure 15](http://momentsingraphics.de#Cylinder)). Then we let the radius \(R\) go to zero in the limit. As the light shrinks, we make its radiance bigger so that the overall power doesn't change. Fluorescent tubes are essentially thin cylinders, so linear lights approximate those well. But they are also great for laser projectiles, light sabers or various futuristic elongated lights.

![Cylinder](../../assets/2c44130f1cec401a.png)

**Figure 15:**A cylindrical light. To turn it into a linear light, we let the radius \(R\) go to zero in the limit.

Deriving projected solid angle sampling for linear lights requires care. It is easy to overlook some factors in the limit process for zero radius. But in the end, algorithms that are rather similar to the ones for polygonal lights are applicable. And of course, that also gives rise to LTC sampling and the same MIS heuristics are applicable. The whole machinery for polygonal lights applies here as well. The result is the image in [Figure 16](http://momentsingraphics.de#BistroExteriorLinearLight). For more details, please [read the paper or watch the presentation](http://momentsingraphics.de/HPG2021.html). As pointed out before [blue noise works particularly well](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#Stratified_random_numbers_blue_noise_) for linear lights.

![BistroExteriorLinearLight](../../assets/a6de303465c183db.webp)

**Figure 16:**A scene lit by a long linear light using projected solid angle sampling, LTC sampling and clamped optimal MIS.

## Timings

I've put a lot of effort into optimization of the sampling methods discussed here. For linear lights, the cost is so low that it's usually irrelevant. At least on NVIDIA hardware (an RTX 2080 Ti in my case), latency hiding for ray tracing works well. The sampling computations run while ray tracing units do their memory-intense work. The cost of this computation in absolute numbers is really low: Taking 128 samples per pixel from a single linear light at 1920×1080 takes only 2 milliseconds.

The cost for polygonal lights is more significant and in my experiments I wasn't able to hide it completely with the cost of ray tracing. Taking 128 samples per pixel from a quad at 1920×1080 takes 11.5 ms. The cost to set up the first sample is quite high, at one sample per pixel the timing is at 0.23 ms. Not unreasonable but still a noteworthy chunk of a 16 ms frame budget.

Therefore, I also proposed a biased variant of the sampling method. From a mathematical point of view, it is clearly incorrect but the error is moderate. If things go poorly, the brightness levels in penumbras within specular highlights of nearby light sources, may not change in quite the right way but overall the bias is hardly ever visible. With this method, 128 samples take 5.5 ms instead of 11.5 ms and one sample takes 0.16 ms instead of 0.23 ms.

More detailed timings with tons of comparisons are in [the](http://momentsingraphics.de/HPG2021.html) [papers](http://momentsingraphics.de/Siggraph2021.html).

## Conclusions and Future Work

And that's how you get physically correct and affordable ray traced soft shadows for individual polygonal or linear lights. Years ago, my research began with works on [real-time shadows](http://momentsingraphics.de/I3D2015.html) and as a result of that, I sometimes joke that shadows are the only hard problem in rendering. Of course, that's a massive exaggeration but there is a bit of truth in it. Dynamic soft shadows require us to compute visibility between two arbitrary points, which is about as difficult as ray tracing (closest hit instead of any hit is of course a bit harder but not much). The research described above can be thought of as specific realization of that joke: It can handle everything efficiently with almost no noise, except shadows.

As always, there's more work to be done. Common types of area lights still cannot be handled in this manner. Especially, ellipsoids require more attention and I'm planning to look into that. Meanwhile, you can combine my [projected solid angle sampling for spherical lights](http://momentsingraphics.de/I3D2019.html) with a suitable method for specular shading [[Dupuy2017]](http://momentsingraphics.de#_Dupuy2017). If you want soft shadows for more than just a few hero lights, you should probably take a look at ReSTIR [[Bitterli2020]](http://momentsingraphics.de#_Bitterli2020). It's not mutually exclusive with what I presented here since my approach can provide good candidate samples to ReSTIR. And of course, we have a long way to go for fast and robust global illumination.

Anyway, if you need more convincing, that ray traced soft shadows are worthwhile, just take a look at [Figure 17](http://momentsingraphics.de#ChallengingSoftShadow) and imagine how terrible that would look with shadow mapping. If you still don't want to copy the [code for linear lights](https://github.com/MomentsInGraphics/vulkan_renderer/blob/linear_lights/src/shaders/line_sampling.glsl) and [polygonal lights](https://github.com/MomentsInGraphics/vulkan_renderer/blob/main/src/shaders/polygon_sampling.glsl) into your renderer, that's your problem 😉.

![ChallengingSoftShadow](../../assets/8ad49e545804fac7.webp)


![ChallengingSoftShadow](../../assets/8ad49e545804fac7.webp)

**Figure 17:**The window seat casts a very soft shadow whereas the cable and parts of the chair cast hard contact-shadows. All of these fuze in a physically correct manner. There is no aliasing either. This image uses 128 samples per pixel and takes 66.6 ms to render but with a bit of denoising, much lower sample counts would get a similar result.

## References

[ Ahmed, Abdalla G. M. and Wonka, Peter (2020). Screen-Space Blue-Noise Diffusion of Monte Carlo Sampling Error via Hierarchical Ordering of Pixels. ACM Transactions on Graphics (proc. SIGGRAPH Asia), 39(6). ][Official version](https://doi.org/10.1145/3414685.3417881) | [Author's version](http://abdallagafar.com/publications/zsampler/)

[ Arvo, James (1995). Stratified Sampling of Spherical Triangles. Proceedings of the 22nd Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH '95). ][Official version](https://doi.org/10.1145/218380.218500) | [Author's version](https://www.graphics.cornell.edu/pubs/1995/Arv95c.pdf)

[ Bitterli, Benedikt and Novák, Jan and Jarosz, Wojciech (2015). Portal-Masked Environment Map Sampling. Computer Graphics Forum (proc. EGSR), 34(4). ][Official version](https://doi.org/10.1111/cgf.12674) | [Author's version](https://cs.dartmouth.edu/~wjarosz/publications/bitterli15portal.pdf)

[ Bitterli, Benedikt and Wyman, Chris and Pharr, Matt and Shirley, Peter and Lefohn, Aaron and Jarosz, Wojciech (2020). Spatiotemporal Reservoir Resampling for Real-Time Ray Tracing with Dynamic Direct Lighting. ACM Transactions on Graphics (proc. SIGGRAPH), 39(4). ][Official version](https://doi.org/10.1145/3386569.3392481) | [Author's version](https://research.nvidia.com/publication/2020-07_Spatiotemporal-reservoir-resampling)

[ Dupuy, Jonathan and Heitz, Eric and Belcour, Laurent (2017). A Spherical Cap Preserving Parameterization for Spherical Distributions. ACM Transactions on Graphics (proc. SIGGRAPH), 36(4). ][Official version](https://doi.org/10.1145/3072959.3073694) | [Author's version](https://onrendering.com/)

[ Heitz, Eric and Dupuy, Jonathan and Hill, Stephen and Neubelt, David (2016). Real-time Polygonal-light Shading with Linearly Transformed Cosines. ACM Transactions on Graphics (proc. SIGGRAPH), 35(4). ][Official version](https://doi.org/10.1145/2897824.2925895) | [Author's version](https://eheitzresearch.wordpress.com/415-2/)

[ Eric Heitz (2018). Sampling the GGX Distribution of Visible Normals. Journal of Computer Graphics Techniques, 7(4):1-13. ][Official version](https://jcgt.org/published/0007/04/01/)

[ Kondapaneni, Ivo and Vevoda, Petr and Grittmann, Pascal and Skřivan, Tomáš and Slusallek, Philipp and Křivánek, Jaroslav (2019). Optimal Multiple Importance Sampling. ACM Transactions on Graphics (proc. SIGGRAPH), 38(4). ][Official version](https://doi.org/10.1145/3306346.3323009) | [Author's version](https://graphics.cg.uni-saarland.de/publications/kondapaneni-2019-siggraph-optimal-mis.html)

[ Turk, Greg (1992): Generating random points in triangles. Graphics Gems (editor Glassner, Andrew S.). Academic Press ][Official version](https://www.sciencedirect.com/book/9780080507538/graphics-gems)

[ Veach, Eric and Guibas, Leonidas J. (1995). Optimally Combining Sampling Techniques for Monte Carlo Rendering. Proceedings of the 22nd Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH '95). ACM. ][Official version](https://doi.org/10.1145/218380.218498) | [Author's version](https://graphics.stanford.edu/papers/combine/)