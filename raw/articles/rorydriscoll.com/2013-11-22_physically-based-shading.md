---
title: Physically-Based Shading
url: https://www.rorydriscoll.com/2013/11/22/physically-based-shading/
author: Rory
published: '2013-11-22'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

I’ve noticed the term ‘physically-based shading’, or variants thereof, used with increasing frequency these days. I’m happy about this, since it represents a movement away from hacking around with magic numbers and formulae in shaders, towards focusing on the underlying material and lighting models. It offers consistency, predictability and constraints where previously these had been somewhat lacking. There was a great [course](http://blog.selfshadow.com/publications/s2013-shading-course/) at Siggraph this year purely about physically based shading.

The trouble is, I’m still not really sure exactly what it means…

### Energy Conservation

When looking at material response, I expect that most people start with the usual Lambert for diffuse plus Blinn-Phong with a Fresnel effect for specular and continue on their happy way. At some point, they may start to read about physically-based shading, and discover the idea of energy conservation (something I [wrote about](http://www.rorydriscoll.com/2009/01/25/energy-conservation-in-games/) before).

The standard Lambert diffuse response can emit more light than it receives. The standard Blinn-Phong specular model can either lose energy or gain energy depending on the specular power and color. If you just add the diffuse and specular responses together, materials can also emit more light than they receive.

It’s fairly easy to change these functions to be energy-conserving, and there are some benefits to doing so, but is energy-conserving Lambert and Blinn-Phong (LBP) considered ‘physically based shading’? It’s based on the concept that energy can neither be created or destroyed, right?

### BRDF Model

I think what most people are referring to when they’re talking about physically based shading, is the model underlying the BRDF. For example, the Torrance-Sparrow microfacet BRDF is modeled on the idea of a surface being comprised of many tiny ideal Fresnel mirrors. TheÂ [Phong](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.131.7741&rep=rep1&type=pdf)Â BRDF is vastly simplified, but still grounded in a model of how light is reflected off a mirror.

Is more physically-based, fewer simplifications better? Have we lost any need for magic numbers and hacks?

To even think about answering this question, we have to understand what are we trying to do when we write a BRDF. In general, we’re trying to approximate the physical response of a real-world material using a combination of functions. That physical response is the ratio of radiance to irradiance based on the incoming light direction and the outgoing light direction. Ideally our BRDF will be flexible enough to handle a range of different material types within the same model.

### Measure Twice, Cut Once

So if we’re approximating real-world data with our BRDF, can’t we just compare it to a real material? That’s a tricky prospect unfortunately. We can only compare our model to what we actually see, and this is the result of not only the BRDF, but the lighting environment as well. The lighting environment consists of many factors such as the number and geometry of the light emitters, the power of the lights, reflections, refractions, occlusion, volumetric scattering. It sounds impossible, doesn’t it?

There is some good news though. The boffins at the [Mitsubishi Electric Research Laboratories](http://www.merl.com/) (MERL) have laser-scanned a number of materials, and have made them freely [available](http://www.merl.com/brdf/) for research and academic use. Also, Disney Animation [created a tool](http://www.disneyanimation.com/technology/brdf.html) to visualize these scanned materials and to compare them to any BRDF written in GLSL.

### BRDF Comparison

I thought it would be interesting to compare energy-conserving LBP to the [Disney Principled BRDF](http://disney-animation.s3.amazonaws.com/library/s2012_pbs_disney_brdf_notes_v2.pdf). The Disney BRDF is energy-conserving and is based on the Torrance-Sparrow microfacet specular model and the Lambert diffuse model with some tweaks (for example, to handle diffuse retro-reflection). While it is more physically-based than straight LBP, it still contains an empirical model for the diffuse part.

To make these test images, I loaded up a MERL material in the BRDF explorer, and then used the graph views to match the parameters of each of the BRDFs as closely as possible for the peak specular direction.

The most interesting view in the BRDF explorer shows an image representing a slice of the BRDF (not the overall lighting response) as a two dimensional function. This function is parameterized in a [different space](http://www.cs.princeton.edu/~smr/papers/brdf_change_of_variables/brdf_change_of_variables.pdf) than you might be used to, with the half-angle (the angle between the normal and the half-vector) vs difference-angle (the angle between the half vector and the incoming or outgoing light direction).

Where did the other two dimensions go? They’re still there… The slice just represents the theta angles, and you have to scroll through the slices for different phi values. The nice thing about this representation is that in general it’s enough to look at just one slice to get a really good idea of how well a BRDF fits the data.

For each of the following images, the Lambert-Blinn-Phong BRDF is on the left, the scanned material is in the middle, and the Disney BRDF is on the right. I’ve included the BRDF view as well as a lit sphere view.

This first material is shiny red plastic. The left side of the BRDF view clearly shows the tight specular peak. In the top left, you can see the strong Fresnel effect as the viewing direction gets to grazing angles. The darkening effect in the extremes I believe is due to the Fresnel effect, since light coming in from other angles is being mirrored away.

The LBP BRDF captures the Fresnel effect to a small amount, but cannot capture the darkening on the extremes. The Disney BRDF clearly does a better job at capturing these features of the scanned material, but still cannot quite match the reference.

In this dull red plastic, you can see the effects of the retro-reflection in both the sphere and BRDF view of the MERL material. The Disney BRDF captures this to a certain extent, but the LBP BRDF does not. Note that the Disney BRDF also did a better job at capturing the shape of the specular highlight, especially at grazing angles. The Blinn-Phong response is a compromise between the width of the specular lobe at grazing angles, and the intensity when more face on.

This is a brass material. It’s pretty clear here how inadequate Blinn-Phong is to capture the long tail of the brass specular response. The Disney BRDF fares a little better, but it’s still not close to the scanned material. It’s possible to alter the Disney BRDF slightly to allow for longer tails, but this then makes matching non-metal materials more difficult.

This steel material in appears to have some artifacts from the laser scanning process in the MERL view. Again, it’s difficult for both BRDFs to capture the specular response, but the Disney one does a little better than LBP.

### How Physical Is Your Shader?

Clearly the Disney BRDF does a much better job at capturing these materials than Lambert plus Blinn-Phong. Of course, it’s more expensive to calculate too. It still contains what some would consider a ‘hack’ to handle diffuse retro-reflection, and was specifically engineered to match the MERL BRDFs. Does this make it bad? Not really. At the end of the day, we have to use the best approximation we can that will work within our budgets.

The primary benefit of the movement towards physically-based models for me is really in achieving more consistency via increasing constraints. An artist would probably tell you that it’s about achieving a closer match to the real-world materials. Both are really nice to have.

So what do you think of when someone says they’re using a physically based shader?

Physically Based Shaders in the game context have the following scientific requirements:

– energy conservation has to be mentioned somewhere, not necessarily enforced (because: art)

– the specular falloff has to be messed around with somewhat, because Blinn-Phong is so passÃ©

– “gloss” drives both specular exponent and reflection

– use environment maps everywhere

– it absolutely must have fresnel in it

– gamma correction is performed

– it must be praised as an amazing “next-gen” feature even though it’s technically something pretty trivial

The term “Physically Based” is required to make it abundantly clear that we’re performing some serious and important science here.

Well, the problem starts when talking about the BRDF. Some people are thinking that BRDFs are actually the real deal, and just using them is the solution for everything, but this is not correct. Actually BRDFs are the children of a whole family of reflectance functions, each having certain assumptions, inheriting them to their children. The following paragraphs will have a very … well … academical touch, because these terms have their mathematical origin in computer graphics papers.

The general light scattering function has 12 dimensions (x_i, t_i, omega_i, lambda_i, x_o, t_o, omega_o, lambda_o). It gives us a proportionality value between incident irradiance and reflected radiance (as you have already written). The function parameters are the incoming light position (2D), incoming time, incoming solid angle (2D) and incoming wavelength, and everything once again for the outgoing light ray. Fixing t_i=t_o to a certain constant point in time (no phosphorescence) and setting lambda_i=lambda_o (no fluorescence) yields a 9 dimensional, simplified scattering function. Now assuming a discrete representation for the domain of the wavelength lambda, e.g. three RGB channels, this yields the 8 dimensional BSSRDF (bidirectional surface scattering reflectance distribution function) with (x_i, omega_i, x_o, omega_o). Disregarding light transport inside the material, i.e. x_i=x_o, finally leads us to the 6 dimensional SVBRDF (spatially varying BRDF) (x, omega_i, omega_o). Assuming a uniform material, i.e. we have the same value for every x, finally gets us to the BRDF f(omega_i, omega_o).

As we see, we often do not use the BRDF, but the SVBRDF for the rendering equation (often written as the term f(x, omega_i, omega_o) inside the integral). But even the MERL data set only gives us BRDFs, and not SVBRDFs, and thus giving us only uniform materials. And of course it contains all the other assumptions inherited by BRDFs, that is no phospho-/fluorescence, a discrete wavelength-domain (think about spectral ray tracers, which are using more than three spectral bands), and no sub-subsurface scattering — with the uniformity probably being the most harsh assumption. Want to vary your BRDF with a specular texture? Congratulations, you already have a SVBRDF, going beyond the limits of BRDFs.

On a side node, the best fits for most samples in the MERL database are Cook-Torrance BRDFs. For the full paper, see ‘Experimental Analysis of BRDF Models’ by Ngan, Durand and Matusik.

All these 12D, 9D, 8D, 6D and 4D functions have some properties in common. Probably I’m boring you repeating them all.

1. Positivity: That’s easy, it just means that f(x,omega_i,omega_o)>=0. This is necessary for f being a probability distribution function.

2. Reciprocity: Now it gets interesting, Reciprocity means that f(x,omega_i,omega_o)=f(x,omega_o,omega_i), i.e. we can swap the incoming and outgoing light directions. This property is essential for ray tracing, and one of the basic assumptions of standard ray optics.

3. Energy-conservation: This is probably the most important property. It means that if we integrate the BRDF times cos(theta_i), the result will be <= 1. So we are of course allowed to absorb energy, but not allowed to magically generate energy.

4. Superposition: This is actually just the reflection equation (a little bit too tedious to write that one down here). But practically it means that we are actually allowed to add the lighting contributions of different light sources independently. You can just use the normal linear properties of an integral. There is actually a kind of dispute whether this is a property of the BRDF or the rendering equation. I think the latter is the case, because it defines a property which is about the interaction between the BRDF and the lighting. But that is only my personal view.

These constraints for BRDFs do not only exist to make physicists happy, but are actually useful to quickly discard non-physical models, e.g. the Phong model is not a BDRF because it lacks reciprocity (and energy conservation, but that is harder to see).

But even when talking about BRDFs, we are also only talking about one part of the rendering equation. Of course we also have the other part of the equation, that is the emission E(x,omega_o) and incident lighting terms L_i(x,omega_i). There we have our next problems, for example it is impossible to represent point-lights as functions for the rendering equations — you have to resort to 'distributions', i.e. here we have a dirac-delta impulse centered towards omega_i — because point-lights would yield an infinite radiance for exactly one solid angle of the hemisphere. It is nice to finally see new lighting models, as they got presented in the course notes for 'Real Shading in Unreal Engine 4'.

Bringing both parts (with part 1 being the shading model, i.e. BRDF, and part 2 the lighting/emission model, i.e. light types) together by using the rendering equation is also … well … impossible, as we know. We would have to take care about the correct evaluation of the rendering integral (which is quite impossible for real-time rasterization, or at least only doable for very limited scenes under constant illumination). So at the latest our well defined physically-correct BDRFs and physically-correct lighting/emission models are now doomed to be screwed up in a crude approximation of the rendering integral. That's the unfortunate state of current affairs in rendering.

Perhaps things get a little bit clearer if one distinguishes between 'physically-correct' and 'physically-based'.

Lets start with a practical example: Every image out of the PBRT ray tracer is 'physically-correct', but not necessarily 'physically-based'. I.e. we used some BRDFs in our scene, but these BRDFs are not based on any real physical material properties like micro-facets (and thus non-circular highlights due to the half-vector reflectance model), real measurements, etc., but are still physically correct in the sense that all assumptions for BRDFs above are fulfilled. If these materials would exist, the scene would look exactly that way in reality. Vice versa, 'physically-based' materials can lead to non-'physically-correct' rendering, e.g. by simply multiplying a normalized, physically-based BRDF by a constant factor of 2, and thus destroying energy conservation.

So 'physically-correct' and 'physically-based' are actually some kind of orthogonal terms — with 'based' referring to the BRDF and lighting/emission, and 'correct' referring to the evaluation of the rendering equation itself.

One thing worth noting from the 2013 SIGGRAPH course notes is the measurement setup from 'Crafting a Next-Gen Material Pipeline for The Order 1886'. It is actually a piece of hardware that can capture … well .. neither a full BRDF, nor a full SVBRDF. Actually the camera position seems to be fixed, so we have only one fixed omega_o, so it won't capture certain effects like a Fresnel term. But it captures a spatially varying position x. So in the end we have captured some function f(x,omega_i) which … actually I don't think it does have a name (it perhaps is a 4D surface reflectance field, but I am not quite sure). That is interesting to see, because the generalization of that thing is a bidirectional texture function (BTF), and these kind of things are pretty impressive for reconstruction material appearance (however, it is only usable with heavy compression techniques).

Finally, to answer your question 'So what do you think of when someone says theyâ€™re using a physically based shader?', well, I will probably say 'That's the way to go, but that is only part 1. Also think about part 2 (emission/lighting models) and part 3 (putting part 1&2 into the rendering equation.'.

The real benefit of using phisically-based shading is (if correctly implemented):

– materials stay consistent between different lighting configurations, no need to hacks parameters, and we have the possibility to share the same asset that can (petentially) become graphics-engine agnostic.

– artists have less parameters to work on, and these parameters are intuitive and they have phisically sense (R0, roughness, diffuse)

eXile,

Hello, I created the hardware and software for the measurement setup you referred to.

I don’t believe it is necessary to capture the full set of data because it is overly redundant. After capturing many types of materials it is easy to classify different material types.

Fresnel, scattering, etc.. can easily be modeled and can be studied independently of the spatially varying data of the capturing process. You say BTF’s can only be represented by heavy compression but I don’t agree. I think if you pick your material type you can represent it as long as you study it and pick the correct analytical formula that best represents it.

I don’t believe cook-torrence/ggx is the best fit for all but I also don’t believe a database of captured data is the end-all be all.

I believe we can separate the process of capturing materials from the process of representing them. I also believe we don’t need to be concerned with the dimensionality of the problem because each material falls in some classification of a simple model we can follow.

I think the next step is exposing these classifications of materials so we can refine the models.

Cheers,

-= Dave

[…] More good introductions to PBR by Julien Guertault and Rory Driscoll […]