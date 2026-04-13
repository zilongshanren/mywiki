---
title: Misunderstanding Multiscattering
url: http://c0de517e.blogspot.com/2019/08/misunderstanding-multiscattering.html
published: '2019-08-12'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Today we will build a state-of-the-art multiscattering GGX BRDF for physically-based rendering.


Already done you say? Yes, you're right, by people who understand maths and physics, that's cheating. We instead will try to do the same trying to learn as little as possible...

Already done you say? Yes, you're right, by people who understand maths and physics, that's cheating. We instead will try to do the same trying to learn as little as possible...

If you want to do this the right way instead, these are some excellent articles:

[Stephen Hill - "A Multifaceted Exploration"](https://blog.selfshadow.com/2018/05/13/multi-faceted-part-1/)[Danny Chan "Material advances in Call of Duty: WWII"](http://advances.realtimerendering.com/s2018/index.htm)[McAuley "A journey through implementing Multiscattering BRDFs and Area Lights"](http://advances.realtimerendering.com/s2019/index.htm)

Ok, ready?


Let's start from your vanilla contemporary GGX with all the correlated-Smith fixings. The following sequence of images is generated with Disney's BRDF explorer environment lighting mode. They show a metallic GGX withy varying roughness, from 0.3 to 0.9, using the common parametrization alpha = roughness squared.

Let's start from your vanilla contemporary GGX with all the correlated-Smith fixings. The following sequence of images is generated with Disney's BRDF explorer environment lighting mode. They show a metallic GGX withy varying roughness, from 0.3 to 0.9, using the common parametrization alpha = roughness squared.

Note: please always indicate the parametrization you are using in your articles and presentations. There are so many variants out there. Here I use one of the most common ones, even if, for what is worth probably the best idea is alpha = roughess^4, which is more perceptually linear and also manages to be a great approximation for the one-over-square-root Blinn-Phong Gloss to GGX mapping many engines prefer.

We can notice how at high roughness the material looks noticeably darker. This is annoying, and smart people have worked hard to find and fix this issue.


Let's compare the image above with

Let's compare the image above with

[Kulla/Conty's Multiscattering GGX BRDF](https://blog.selfshadow.com/publications/s2017-shading-course/).
Fixed!

Now, we could try to understand how this solution work, the math is already there. And you probably should, it's both interesting and useful to understand other related problems. But, let's try not to...


First of all, we should ask why is this a problem? How do we know it is a problem? And also, if it is a problem, how big of a problem it is?

First of all, we should ask why is this a problem? How do we know it is a problem? And also, if it is a problem, how big of a problem it is?

Let's start at the top. Why do we like "PBR"? It's not because we like physics, at least, I don't... And if we did like physics, this would be a small error to focus on, considering that

[we are surely committing worse sins in our end-to-end image pipeline](http://c0de517e.blogspot.com/2019/05/seeing-whole-physically-based-picture.html)...
Computer graphics is not predictive rendering. We don't try to simulate physics to make accurate simulations, that's not a goal (and the people who care about physics are an order of magnitude ahead of us). We make pretty pictures.

At a given point, we noticed that using some physics to make pretty pictures allowed for easier workflows, decoupling materials from lighting, reducing the number of hacks and parameters, allowing to use libraries of real materials and so on.

We thought artists would be happier and be able to work more efficiently, while still being able to create a lot of different scenes. It took a while to move over all our workflows, but it was the right call.

We thought artists would be happier and be able to work more efficiently, while still being able to create a lot of different scenes. It took a while to move over all our workflows, but it was the right call.

So, when we look for right and wrong, we have to start with art and artists. If there is a need we can identify there, then we can look at physics to see if the answers are there. In this case, we can say that yes, indeed we have a (small) problem.

It would be nice if our material parameters were orthogonal, and having things go darker as we change roughness is not ideal.

It would be nice if our material parameters were orthogonal, and having things go darker as we change roughness is not ideal.

Let's move to step two then. Can physics help? Is this darkening physically correct, or not? How do we test? Enter the furnace! Let's put our "GGX coated" metallic object in a uniformly lit environment and see what happens:

Light hits our surface, hits our microfacets. The microfacets reflect back some light, and refract some other, according to Fresnel. If we're assuming a metal people told us that the refracted light, that goes "inside" the surface, is quickly absorbed and never comes out (becomes heat).


It's reasonable that even in a furnace our metallic object has a color, as some of the energy will be absorbed. But what if we take our microfacets and make them always reflect all the light, no absorption?

This means we need to set our f0 to 1 (remember, Fresnel is what controls how much light the microfacets scatter), let's try that and see what happens:

It's reasonable that even in a furnace our metallic object has a color, as some of the energy will be absorbed. But what if we take our microfacets and make them always reflect all the light, no absorption?

This means we need to set our f0 to 1 (remember, Fresnel is what controls how much light the microfacets scatter), let's try that and see what happens:

The object is still not white. Something's wrong! Ok, the inquisitive reader might still say - how do you know it's wrong. Perhaps certain directions scatter more light and others less, so we still see some shading even if all the light eventually comes out...

If we think of BRDF and lobes it's not easy to get correct intuition. Let's instead think of how a light path, starting from the camera, looks like. It might hit some of the microfacets, one or many times, bounce around then eventually escape and connect to the furnace environment which will always be a emitting a given contant energy.

How much of that energy reaches the camera? All of it! Because regardless of which and how many microfacets we hit, all the energy is reflected and none is absorbed.

Now we have an intuition of why the image above should be white, it isn't, so we have a problem in our math...

If you studied BRDFs you know that in microfacet model we have a masking-shadowing visibility function that models which microfacets are occluded by others. What we don't typically model though is the fact that these occlusions are themselves microfacets, so the light should bounce around and eventually get out, not just be discarded.

This is what the multiscattering models model and fix, and indeed if we did put in a furnace Kulla and Conty's GGX that we have shown before, it would generate a boring and correct white image for a fully reflective material, regardless of its roughness.

This is what the multiscattering models model and fix, and indeed if we did put in a furnace Kulla and Conty's GGX that we have shown before, it would generate a boring and correct white image for a fully reflective material, regardless of its roughness.

Kulla's model is not trivial though, and in many cases is likely not worth using to fix such a relatively minor problem. So. Can we be more ignorant? What if we knew how much light our BRDF gives out in a furnace, for a given roughness and viewing angle (fixing then again f0 = 1)? Could we just take that value and normalize the BRDF with it?


Spoiler alert, we can. And not only we can but it's also trivial to do, because we already have this "furnace" value in most modern engines, in the look-up tables used for the popular split-sum image based lighting approximation.

Spoiler alert, we can. And not only we can but it's also trivial to do, because we already have this "furnace" value in most modern engines, in the look-up tables used for the popular split-sum image based lighting approximation.

The split-sum table boils down the "BRDF in a furnace" (also known as directional albedo or directional-hemispherical reflectance) to a scale and bias (add) factor to be applied to the Fresnel f0 value.

In our case, we want to normalize considering f0=1 so all we do is to scale our BRDF lobe by one over bias(roughness,ndotv) + scale(roughness,ndotv). This is the result:

In our case, we want to normalize considering f0=1 so all we do is to scale our BRDF lobe by one over bias(roughness,ndotv) + scale(roughness,ndotv). This is the result:

Indeed, we're getting some energy back at high roughness, and if we tested this in a furnace it would come up white, correctly, at f0 = 1. But it's also different from Kulla's, in particular, color is not quite as saturated in the rough materials. How comes? Well again, if you studied this problem already (cheater!) you know the answer.



Proper multiscattering adds saturation because as light hits more and more microfacets before escaping the surface, we pick up more color (raising a color to a power results in a more saturated color). But so how can this be physically wrong, but still correct in our test?

Well, it's simple, really. By not simulating this extra saturation we are still energy conserving, but we changed the meaning of our BRDF parameters. The f0 "meaning" in our "ignorant" multiscattering BRDF is not the same as Kulla's, it results in a different albedo, but the BRDF itself is still energy conserving, it's just a different parametrization.

Most importantly, I'd argue it's a better parametrization!

Most importantly, I'd argue it's a better parametrization!

**Then again, remember our objectives. We don't do physics for physics' sake, we do it to help our production.**


We wanted to make our parameters more orthogonal so that artists don't need to artificially "brighten" our BRDF at high roughness. If we went with the "more correct" solution (about that,

You can imagine some scenarios where this might be desirable, but I'd say it's almost always wrong for our use-cases.

[this recent post by Narkowicz](https://knarkowicz.wordpress.com/2019/08/11/comparing-microfacet-multiple-scattering-with-real-life-measurements/)is a great read) we would add a different dependency, now roughness instead of darkening our materials it makes them more saturated, which would kind of defeat the purpose.You can imagine some scenarios where this might be desirable, but I'd say it's almost always wrong for our use-cases.

If we wanted to simulate the added saturation, there are a few easy ways. Again, going for the most "ignorant" (simple) we can just scale the BRDF by 1+f0*(1/(bias(roughness,ndotv) + scale(roughness,ndotv)) - 1), resulting in the following:

Now we are close to Kulla's solution. This is still not entirely correct if you wonder why Kulla's approximation is better, as it might not show in images, it's because ours doesn't respect reciprocity.

This might be important for Sony Imageworks, as certain offline path-tracing light transport algorithms do require it, but it's fairly irrelevant for us.

Ok, so now that we have found an approximation we're happy with we can (and should) go a step further and see what we are really doing. Yes, we have a formula, but it depends on some look-up tables.

This isn't a big issue as we need these tables around for image-based lighting anyways, but it would be an extra texture fetch and in general it's always important to double-check our math, so let's visualize the 1/(bias(roughness,ndotv) + scale(roughness,ndotv)) function we're using:

This isn't a big issue as we need these tables around for image-based lighting anyways, but it would be an extra texture fetch and in general it's always important to double-check our math, so let's visualize the 1/(bias(roughness,ndotv) + scale(roughness,ndotv)) function we're using:

It looks remarkably simple! Indeed, it's so simple it has a trivial approximation, you don't even need any sophisticated tool to find it so I'll just show it:

**1 + 2*alpha*alpha * ndotv**. This fits very well:
![]() |

You can see that there is a bit of error in the furnace test. We could improve by doing a proper polynomial fit - yes, it turns out "2" and "1" in the formula above are not exactly the best constants.

Actually defining "best" would be a problem all on its own, because doing a simple mean-square minimization on the normalization function doesn't really make a lot of sense (we should care about end visuals, perceptive measures, which angles matter more and so on), and I think we already spent too much time for such a small fix.

Moreover, the actual rendered images are really hard to distinguish from the table-based solution.


What is interesting is to see what could we achieve if we wanted to be even simpler, dropping the dependency from ndotv. It turns out in this case

This means that we're just applying a multiplicative factor to our BRDF to brighten it at high roughness, which just makes a lot of sense.



Actually defining "best" would be a problem all on its own, because doing a simple mean-square minimization on the normalization function doesn't really make a lot of sense (we should care about end visuals, perceptive measures, which angles matter more and so on), and I think we already spent too much time for such a small fix.

Moreover, the actual rendered images are really hard to distinguish from the table-based solution.

What is interesting is to see what could we achieve if we wanted to be even simpler, dropping the dependency from ndotv. It turns out in this case

**1 + alpha*alpha**does the trick decently as well.This means that we're just applying a multiplicative factor to our BRDF to brighten it at high roughness, which just makes a lot of sense.

This of course adds more error and it starts to show as the BRDF shape changes, we get more energy at grazing angles on rough surfaces, but it might just be good enough depending on your needs:

![]() |

## No comments:

Post a Comment