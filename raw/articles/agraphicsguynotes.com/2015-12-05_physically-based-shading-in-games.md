---
title: Physically Based Shading in Games
url: https://agraphicsguynotes.com/posts/physically_based_shading_in_games/
author: Jiayin Cao
published: '2015-12-05'
source_blog: A Graphics Guy's Note
source_site: https://agraphicsguynotes.com/
category: graphics
fetched: '2026-04-19'
---

Physically based shading has been around for years, it not only eases the workflow for artist, but also delivers high quality shading with neglectable overhead, I see no reason to avoid it in today’s game. Here is an image taken from UE4 document.

![](../../assets/3d0c0294d68e1dfb.png)

When the term first came out, I was totally no idea what this new stuff is. And it took me quite a while to get some basic idea on it because there are so many materials and some of them are a little confusing. I can’t say that I fully understand all of the theory simply because I don’t, however I would still like to write something that I knew and list something useful that I found in this blog. Hopefully it can be helpful for someone.

# Physically Based Shading

Basically physically based shading performs shading operation in a more physical accurate way than the old common ‘ad-hoc’ model, which is usually Phong or any modified version. Here is the basic form of Phong model (note that it is shading model listed below, not BRDF):

$$ I_p=\sum_{m\in lights}(k_dm_d(L_m\cdot N)+k_sm_s(R\cdot V)^\alpha)$$Ambient term is dropped since it is not involved in this topic. R is the reflected vector of the incident direction around normal. It has many parameters for artist to tune and special care needs to be taken in certain aspect to avoid unnatural look. Although this model is used ever since fixed function graphics hardware, it is apparently out-dated comparing with more advanced model like ‘microfacet’ model.

## Diffuse and Specular

Generally there are two categories of reflection, diffuse and specular. In the following diagram, the yellow ones are specular reflection and the rest are diffuse reflection.

![](../../assets/b643bb570813ac67.png)

Diffuse is the kind of reflection whose distribution is totally random. It happens when the photons actually penetrate into the surface and get out after several bounces. Depending on what the material inside the surface is, it can manifest itself as diffuse reflection or subsurface scattering which is a much more complex concept. There are several brdf model available for simulating it.

- Lambert
- OrenNayar
- Burley

UE4 uses the simplest one, lambert, as their diffuse model because little difference can be noticed between those models. Although UE4 users can enable other diffuse model with simple macro switching in the uber shader, I seriously doubt if it helps on the visual quality of the final image. See the image below, it is basically no difference to me. I can’t justify the reason to do the switching.

![](../../assets/7309f7b94f2f9a49.png)

Unlike diffuse reflection, specular happens right at the surface being shaded. And its reflected direction is highly dependent on the incident angle. Take an extreme case, mirror will reflect viewing angle into exact one direction. Microfacet model is the most commonly used bxdf for specular lighting. It assumes that the surface is composed of many small micro facets, each one among them is a pure specular surface or in other words, perfect mirror. Only micro facets with normal exactly the same with the half angle between incident and reflected direction will contribute. It is the aggregate behavior defines what the surface actually looks like. The more uniform those microfacet normals are, the smoother the surface is, vice versa. Here is the microfacet brdf:

$$ f(\omega_i,\omega_o,x) = \dfrac{F(\omega_i , h) G(\omega_i,\omega_o,h) D(h)}{4 cos(\theta_i) cos(\theta_o)} $$F is the fresnel term which will be mentioned later. D is the distribution term defining where these microfacets face, here is more information on it. G is a shadowing factor for masking and it is usually a less dominant term in this bxdf.

![](../../assets/9c428a20d113e8ac.png)

Wait a second, phong model also takes diffuse and specular into account, what is the big deal in this new PBS model?

In term of diffuse reflection, they are the same. Both use lambert bxdf. However it is microfacet bxdf model which delivers much better result than the phong model. And another subtle difference is the way pbs model blends diffuse and specular.

# Energy Conservation

Energy conservation is one of the basic rules for every physical correct bxdf to obey. It says that the total amount of reflected energy of light can’t not be larger than received unless it is emissive material. It makes perfect sense. From a mathematics perspective, it can be expressed this way:

$$ \int_{\Omega}f_r(p,\omega_o,\omega_i) cos\theta_i d\omega_i \le 1$$Unfortunately bxdf of phong totally ignores this rule, forwarding the responsibility to artists in their workflow, which usually costs them a lot of time.

## Specular bxdf

Let’s focus on the specular part first. Two things deserve our attention, reflection intensity and the high light shape. In the phong model, we have two parameters controlling each of these, which used to be defined as “Specular Color” and “Specular Power”. Unfortunately, it is quite easy to break the rule of energy conservation because these two terms should be related to each other in order to preserve it. Simply put it, phong brdf is just not a normalized brdf.

![](../../assets/d10e68ec86dedeba.jpg)

See the above image, the top row, as the specular power becomes higher, we get narrower high light. While the ugly fact is that the specular intensity never changes. That is just not true in our real life. As we can notice from the bottom row, the reflection becomes stronger as it narrows down. In order to simulate it in the phong model, it forces artist to increase specular color, sometimes even above one. And if there are only two values to tune, it may be acceptable, not to mention it is not accurate. What if the specular power is provided by a texture? Artist will have to make sure they have a cooresponding specular color texture and what is worse is that every pair of pixels from these two textures needs to be tuned.

With the microfacet brdf model, artists have only one parameter defining both of the shape and intensity of the reflection. And that is the roughness, or glossyness in some engines. So only one parameter needs to be set and the shading policy will force it to be energy conservation no matter what value is provided by the artist. In other words, artists will have little chance to make mistake.

![](../../assets/8cca671fe62cd33b.png)

Notice the mud and water have different reflection intensity. As a matter of fact their reflectivities are exactly the same, the only thing different is the gloss parameter. Here is another example from my offline renderer (I know I’m talking about physically based shading in real time rendering, however the theory behind these are exactly the same, so it can be used as a reference too):

![](../../assets/c3c1356698fbf4b2.png)

These monkeys have different roughness values with the same base color. The reflection on the left-most one is clearly more sharp comparing with the right ones.

There are also ways to make phong brdf energy conservative, check [here](http://www.thetenthplanet.de/archives/255).

## Blend between Diffuse and Specular

Besides the unnormalized feature of phong model, the other ugly thing that breaks energy conservation is the way it blends diffuse and specular. As a matter of fact, it doesn’t even blend them, it just add them together which makes little sense in a physical manner. From a micro perspective, photons either reflect at the surface or penetrate into it, they can do both at the same time. That said the total energy reflected by diffuse and specular should obey the rule of energy conservation. Obviously phong fails to keep it again.

The right way of blending these two is to make sure the following equation goes right:

$$ m_d + m_s \le 1 $$UE4 uses a specific parameter called Mettalic to lerp between diffuse and specular. One minor detail in UE4 material system to be noticed is that even if metallic is zero, 8% percent specular reflection will still be present. Another paramter called specular is introduced to remove this 8% for some special materials. Here is an image showing a sphere with different metallic value. There is no diffuse reflection for surfaces with 1 as metallic parameter, that makes sense because metal doesn’t show any diffuse reflection in our real life.

![](../../assets/a16c4ebca69dfd75.png)

# Fresnel Effect

The other big benefit that can’t be ignored is the fresnel effect. That said light reflection will be much higher at grazing angle. Rim color is what we used to simulated in the old ad-hoc model. Check here for the importance of fresnel effect, the author takes many real life examples convincing readers how importance fresnel effect is in our daily life. Here is one sphere demonstrating how importance fresnel effect is, we get much more brighter reflection at grazing angle. And that is just the work of fresnel.

![](../../assets/eb6c650690715529.png)

For a real time solution for fresnel equation, Schlick’s approximation is enough most of the time.

$$ R = R(0) + ( 1 - R(0) ) ( 1 - cos\theta)^5$$It is relatively easy to see from this image that when at grazing angle, fresnel value will approach 1 no matter what value R(0) is provided in the material system. That is exactly why we are seeing bright reflection around the contour of this sphere. One can also check [here](https://seblagarde.wordpress.com/2013/04/29/memo-on-fresnel-equations/) for further information.

Valuable resources

Here are the courses on pbs at each year siggraph:

[Siggraph 2010 pbs course](http://renderwonk.com/publications/s2010-shading-course/)[Siggraph 2012 pbs course](http://blog.selfshadow.com/publications/s2012-shading-course/)[Siggraph 2013 pbs course](http://blog.selfshadow.com/publications/s2013-shading-course/)[Siggraph 2014 pbs course](http://blog.selfshadow.com/publications/s2014-shading-course/)[Siggraph 2015 pbs course](http://blog.selfshadow.com/publications/s2015-shading-course/)

# Summary

I guess the features listed above are not all about pbs in games. However they are definitely the importance ones.

And as we can see from the above images, pbs introduces quite a lot of new nice features in games. It is too good to be ignored. Of course it needs more instructions than before, however texture operations are roughly the same. Since even mobile devices can achieve very high GFLOPS, those extra instructions in physically based shading won’t affect much performance on modern graphics hardware, which just gives us no excuses to avoid it.

# References

[1] [Energy Conservation in Games](http://www.rorydriscoll.com/2009/01/25/energy-conservation-in-games/)

[2] [Phong Normalization Factor derivation. Blinn-Phong normalization factor](http://www.farbrausch.de/~fg/stuff/phong.pdfhttp://www.farbrausch.de/~fg/stuff/phong.pdf)

[3] [How is the NDF really defined](http://www.reedbeta.com/blog/2013/07/31/hows-the-ndf-really-defined/)

[4] [The Blinn-Phong Normalization Zoo](http://www.thetenthplanet.de/archives/255)

[5] [Basic Theory of Physically Based Rendering](https://www.marmoset.co/toolbag/learn/pbr-theory)

[6] [Physically Based Materials](https://docs.unrealengine.com/latest/INT/Engine/Rendering/Materials/PhysicallyBased/index.html)

[7] [Physically Based Shading In UE4](https://www.unrealengine.com/blog/physically-based-shading-in-ue4)

[8] [Memo on Fresnel equations](https://seblagarde.wordpress.com/2013/04/29/memo-on-fresnel-equations/)