---
title: Misunderstanding Multilayering (Diffuse-Specular Energy Conservation)
url: https://c0de517e.blogspot.com/2019/08/misunderstanding-multilayering-diffuse.html
published: '2019-08-24'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**- Introduction to the problem**

In our last episode,

["misunderstanding multiscattering"](http://c0de517e.blogspot.com/2019/08/misunderstanding-multiscattering.html), we saw how to create a multiscattering BRDF mostly by intuition. We used the concept of directional albedo (a.k.a. directional-hemispherical reflectance) to normalize a specular BRDF and from there we derived a very simple closed-form approximation for GGX energy conservation.
We also showed that the directional albedo is the response of our BRDF in a white light furnace at different normal to view angles, and we typically have that information available in tabular form as it's a key component of the "split sum" approximation to the integrals needed for image-based lighting on contemporary BRDFs. Great!

This time, we'll show how the very same data, ideas, and intuitions, can be used to build multilayered BRDFs, and in particular to couple matte-specular models (diffuse lobes to specular lobes).

Like the previous article, this is not anything particularly novel, this isn't Siggraph worthy material, just some notes on the subject.

Let's start, as always, with the problem, with a very quick recap of things everyone reading this will probably already know (my flight has been delayed a couple of hours, so yes, we have time for recaps).

Under the framework of geometrical optics we look for light interactions with materials at surfaces where the index of refraction changes. We assume that light travels in a medium of uniform IOR (e.g. air), and then eventually hits a surface with a different IOR and either gets reflected out of the surface, or refracted into it.

In fact in real-time rendering we only consider the air->material interface, we don't handle nested objects (e.g. air->glass->water->glass->air) even when we render transparent materials or multilayered materials. Which is wrong, but it's just

[one of the many ways we are still totally wrong](http://c0de517e.blogspot.com/2019/05/seeing-whole-physically-based-picture.html)(and yet might or might not be right by not caring). Even for offline path-tracers, this is not entirely trivial, depending on how you do light transport.
We then consider, for a small but not infinitesimal patch of our surface, the statistics of how probable are these reflections and refraction in function of the light incident angle, a given outgoing angle we want to measure, and the surface patch normal, and these statistics create a BRDF "lobe".

But BRDFs though don't typically have a single lobe: we usually have "metals" and "dielectrics" and in the latter case we have a specular and a diffuse lobe. How comes? Well, because we don't really consider a single interaction, that was sort-of a lie. We do create a lobe with the light that is scattered from the surface interaction, but we also have to consider the light that gets refracted into the surface. In the case of metals, the energy that goes into the material somehow disappears (becomes heat or maybe fairy dust who knows - physics) and we effectively have a single lobe.

For dielectrics, though the refracted light keeps hitting molecules inside what's essentially a participating medium, and eventually taking random paths it comes back out from the surface and we model that as a diffuse lobe.

Diffuse lobes are reasonable when the "bouncing around" is such that it effectively randomizes the direction at which the light comes out, but still happens in such a small space that we consider the light coming out effectively at the same point it came in.

If that's not true, and the scattering distances are bigger, we have what we call "subsurface scattering" effects. If the direction is not randomized "enough", then instead we have transparent materials, and somewhere in the middle, we have what we usually address as participating media.

Any time that we consider multi-layered materials we have to model the way the light that is refracted by a layer reaches the next. At the very least, we have to know at least how much energy is "handled" by a given layer/lobe and how much is "passed down" to the subsequent lobes, as if we gave the same input light to all the layers we would sum the interactions up and potentially end up with more energy coming out of a material than it came in!

In theory we should understand much more than that, namely how the light travels in a given layer and reaches another one (its statistical distribution over directions and space), but for diffuse lobes found in dielectrics we can imagine that it doesn't matter much (anyways the light is going to be randomized...), so right now we just want to know how much energy survives the topmost specular lobe of a dielectric (gets refracted as opposed to reflected).

This might seem a lot of handwaving. And it is! This is the point of this post -and- the previous one!

We know that we have certain problems in our math, but should we care? How much should we care and why? Does it matter for the goal of generating photorealistic images easily? Remember, this is our goal, not fixing physics. Then again if we wanted to look at the physics there are

[a ton of assumptions that we are making anyways](http://c0de517e.blogspot.com/2019/05/seeing-whole-physically-based-picture.html).
![]() |

It turns out that this problem matters a lot, much more in fact than the energy loss in non-multiscattering specular lobes. The multiscattering issue was small, happened only at high roughnesses and it was entirely fixable by artists tweaking specular albedo (typically controlled by Fresnel f0 parameter) a bit.

Tweaking albedo is fine because it still keeps the materials decoupled from lighting, the main issue we wanted to fix by embracing physically-based rendering models, and it's doable because the tweaks needed are small and entirely in the range of realistic albedos (which don't ever go to f0 = 1 for metals, and of course even less so for dielectrics).

Not having any energy conservation between specular and diffuse instead creates overly bright materials that can look fine in a certain scene but will glow unnaturally under different conditions, and it's quite hard for artists to make sure that the lobes are tuned in a way that doesn't produce more energy than they should.

In fact, most real-time rendering today works without multiscattering BRDFs, but (hopefully) it always considers some way of balancing specular and diffuse.

**- Solutions and pretty images**

Now we know the problem -and- we know it matters, so we are justified in spending some time to investigate further. How? Well, as we did with the previous post, we bring back our friend the white furnace test. Pretty much any time we want to check for energy conservation, we take our materials and put them in a furnace!

As for the previous time though, just putting a material in a furnace doesn't tell us that much. Yes, it's already apparent how the middle image looks unnaturally bright, but that's not a great test. What we want is to setup our scene so we expect the material to reflect back exactly all the light that comes in, no matter which path the light takes in the material and across the microfacets, and then see if we get more light than we expect or less.

We have to think, what is that is absorbing light in our materials? The specular reflects light out or refracts it in, it doesn't absorb, so all the energy loss is when we go "inside" the material, in the dielectrics case, in the diffuse layer. It stands to reason then that if we set our diffuse albedo to one, regardless of the specular parameters, we should be perfectly white in a white furnace. Let's see:

![]() |

Bingo! We see now that just adding diffuse with no attempt at energy conservation does indeed result in energy being created. And surprisingly it looks like that the simple idea of using (1-F) as a multiplication factor to normalize diffuse is indeed doing a very good job, in fact, it looks alright if it wasn't for the grazing angles... Why is that?

![]() |

![]() |

Well if we think about it, it's fairly obvious. For the terms we commonly use, at the incident angle (N=V=L) the shadowing term has no effect and the NDF takes a constant value regardless of the roughness parameter, Fresnel dominates. At grazing angles, the shadowing term starts to matter, and there is where we see our simple normalization breaking down.

What we can try to fix this? If you read the previous post, it should be obvious by now. We have something that should be white in a furnace, it isn't, let's make it! We know how much energy the specular lobe will scatter back in the furnace, for any roughness, Fresnel f0, and viewing angle, this again is the split-sum table we use for environment map lighting. We know that a Lambert diffuse is correctly normalized, so it will scatter back all incoming energy if the albedo is set to one. So how much do we have to scale the lobe for the sum of the specular plus diffuse to be one, with an arbitrary specular and a unitary albedo diffuse? Obviously just by 1-E, where E is what we get from the split-sum table!

![]() |

Note: some artifacts remain due to approximations in the Directional Albedo table I used.

Furnace fixed! And note, this works regardless of if we're using or not the multiscattering specular BRDF, as a non-multiscattering one will just behave as it's refracting more light to the diffuse layer, which in our case will still bounce it all back out. And, if we're using the simple renormalization for multiscattering presented in the previous post, we don't even need to compute a new table for directional albedo, as it's easy to derive how to analytically modify the output of the single scattering table to accommodate for the multiscattering correction (I'll leave this as an exercise for the reader, it's trivial and might motivate you to actually look at the definition of directional albedo...)

As it was for the multiscattering normalization idea, this is wrong and we can see immediately that it's wrong from the equation, even if the error won't show in the furnace, because we don't respect reciprocity (we consider only ndotv and not ndotl). It's even intuitive, as we don't seem to consider at all that the light going from the specular layer to the diffuse, scattering inside the material and eventually coming out, has to cross again the specular interface as it comes out!

Before we delve further into this, I want though to stop for a second and check out what we are doing (again, same as last time). Let's plot the 1-E multiplicative factor we're applying to diffuse and see what happens:

![]() |

for a non-multiscattering specular.

![]() |

Same as above, but using simple multiscattering specular.

This is interesting! Albeit we can couple diffuse with and without a multiscattering specular, the plots for the multiscattering case are much simpler, so much so that it's easy to derive, by hand, a function that would approximate them. Fun!

![]() |

And now, at last, let's have a look at a more correct solution that respects reciprocity and see if that matters or not for real-time rendering. This is quite hard to know intuitively, so we'll have just to implement something and check.

Luckily this is nothing new, in 2001 Kelemen and László Szirmay-Kalos published "A Microfacet Based Coupled Specular-Matte BRDF Model with Importance Sampling", and we can pretty much copy and paste their equation, which unsurprisingly ends up looking very close to the way we adjust for reciprocity in specular multiscattering (in fact Kulla and Conty cite the afore mentioned KSK paper in theirs).

Without further ado:

![]() |

Simple Multiscattering GGX, Roughness 0.1.

![]() |

And some more images. The difference between (1-F) and (1-E) can be seen only at low roughness. Difference is even less pronounced for table-based (1-E), the approximation showed above and the full KSK method.

![]() |

![]() |

![]() |

![]() |

## No comments:

Post a Comment