---
title: A Journey Through the Atmosphere - Alan Zucconi
url: https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-4/
author: Alan Zucconi
published: '2017-10-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post describes how to model the density of the atmosphere at different altitude. This is a critical step, since the atmospheric density is one of the parameters necessary to correctly calculate the Rayleigh scattering.

![](../../assets/488fe0db18d2fa0c.gif)

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) **Part 4.**[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557)- Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

You can **download** the **Unity package** for this tutorial at the bottom of the page.

#### Atmospheric Density Ratio

Something that we have not addressed yet is the role of the atmospheric density ratio ![Rendered by QuickLaTeX.com \rho](../../assets/d2238a452efe47fa.png)

**troposphere**, the temperature decreases linearly and the pressure decreases exponentially.

The diagram below shows the relationship between density and altitude in the lower atmosphere.

The value of ![Rendered by QuickLaTeX.com \rho \left(h\right)](../../assets/2fe69865f8813782.png)

![Rendered by QuickLaTeX.com h](../../assets/5b0f1268bf785a2d.png)

![Rendered by QuickLaTeX.com \rho](../../assets/d2238a452efe47fa.png)

**density ratio** because it can be also defined as:

![Rendered by QuickLaTeX.com \[\rho\left(h\right) = \frac{density\left(h\right)}{density\left(0\right)}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9f09be06848fed56d6316e05a0d91ec6_l3.png)


Dividing the actual density by ![Rendered by QuickLaTeX.com density\left(0\right)](../../assets/91535b64c9d67448.png)

![Rendered by QuickLaTeX.com \rho\left(h\right)](../../assets/bad1c9ecb9cc6db7.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com density\left(h\right)](../../assets/f2820c75caf32b4c.png)

**exponential decay**.

If we want to approximate the density ratio with an exponential curve, we can do it like this:

![Rendered by QuickLaTeX.com \[\rho\left(h\right) = exp\left\{-\frac{h}{H}\right\}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9a57bcac97792931e879995351f5d3b7_l3.png)


where ![Rendered by QuickLaTeX.com H_0](../../assets/0d95ccf601b27ffd.png)

**scale height**. For the Rayleigh scattering in the lower atmosphere of Earth, it is often assumed ![Rendered by QuickLaTeX.com H=8500](../../assets/e4fa5f2d635d1bf8.png)

![Rendered by QuickLaTeX.com 1200](../../assets/6fe5f9e744311dcf.png)


The value used for ![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)

![Rendered by QuickLaTeX.com \rho\left(h\right)](../../assets/bad1c9ecb9cc6db7.png)


#### Exponential Decay

In the previous parts of this tutorial, we have derived an equation that shows how to account for the out-scattering that a ray of light is subjected to after interacting with a single particle. The quantity used to model this phenomenon was called the **scattering coefficient** ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


In the case of the Rayleigh scattering, we have also provided a closed form to calculate the amount of light that is subjected to atmospheric scattering per single interaction:

![Rendered by QuickLaTeX.com \[\beta \left(\lambda, h \right )=\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{\rho\left(h\right)}{N}\frac{1}{\lambda^4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-3906bff30524399c8699a8f74f0b771c_l3.png)


When evaluated at sea level, which means using ![Rendered by QuickLaTeX.com h=0](../../assets/c046ce8a19a8027c.png)


![Rendered by QuickLaTeX.com \[\beta\left(680nm\right) = 0.00000519673\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-81cd42dab446959f2204dbd758913dcd_l3.png)


![Rendered by QuickLaTeX.com \[\beta\left(550nm\right) = 0.0000121427\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a2c82b3cb20c2dc6928b40421b8e61e2_l3.png)


![Rendered by QuickLaTeX.com \[\beta\left(440nm\right) = 0.0000296453\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a6282614241a20505bb063bf0d49012d_l3.png)


Where ![Rendered by QuickLaTeX.com 680](../../assets/32266ad34a38ee87.png)

![Rendered by QuickLaTeX.com 550](../../assets/a2db4730957f2260.png)

![Rendered by QuickLaTeX.com 440](../../assets/cd5320bcef9eb7a5.png)


What is the meaning of those numbers? They represent the ratio of light that is lost by a single interaction with a particle. If we assume a ray of light has initial intensity ![Rendered by QuickLaTeX.com I_0](../../assets/2e533417c872eeba.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

*not* lost to scattering is:

![Rendered by QuickLaTeX.com \[I_1=\underset{\text{initial energy}}{\underbrace{I_0}} - \underset{\text{energy lost}}{\underbrace{I_0 \beta}}=I_0 \left(1-\beta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b6750a768de61331bb6ededc6a35e4ee_l3.png)


While this holds for a single collision, we are interested in understanding how much energy is scattered over a certain distance. This means that, at each point, the remaining light is subjected to this process.

When light travels through a uniform medium with scattering coefficient ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


For those of you who have studied Calculus, this should sound familiar. Whenever a multiplicative process like ![Rendered by QuickLaTeX.com \left(1-\beta\right)](../../assets/395539fdfcf01287.png)

**Euler’s number **makes its grand appearance. The amount of light that survives scattering after travelling for ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)


![Rendered by QuickLaTeX.com \[I = I_0 exp \left\{-\beta x \right\}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-94ddf82370de44683c19549ebb484650_l3.png)


Once again, we encounter an exponential function. This is not in any way related to the exponential function used to describe the density ratio ![Rendered by QuickLaTeX.com \rho](../../assets/d2238a452efe47fa.png)


#### Uniform Transmittance

In the second part of this tutorial we have introduces the concept of **transmittance** ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)


Let’s look at the diagram below, and see how we can calculate the transmittance factor for the segment ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

**sun intensity** ![Rendered by QuickLaTeX.com I_S](../../assets/de81e6e81d28e2ea.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com I_P](../../assets/457e324e8f29677a.png)

![Rendered by QuickLaTeX.com I_S](../../assets/de81e6e81d28e2ea.png)


![](../../assets/7ad5c8a7e1aa0372.png)

The amount of light scattered depends on the distance travelled. The longer the journey, the strongest the attenuation will be. According to the law of exponential decay, the amount of light at ![Rendered by QuickLaTeX.com I_P](../../assets/457e324e8f29677a.png)


![Rendered by QuickLaTeX.com \[I_P = I_S \exp{\left\{-\beta \overline{CP}\right\}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0efc9aea82a1491221583ad324cd4027_l3.png)


where ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com \exp{\left\{x\right\}}](../../assets/522f2dd127a42e38.png)

**exponential function** ![Rendered by QuickLaTeX.com e^{x}](../../assets/a554c06df2e1e799.png)


#### Atmospheric Transmittance

We have based our equation on the assumption that the chance of being deflected (the **scattering coefficient** ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)


The scattering coefficient strongly depends on the atmospheric density. More air molecules per cubic metre mean higher chances of impact. The density of a planet’s atmosphere is not uniform, but changes depending on the altitude. This also means that we cannot calculate the out-scattering over ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)


To understand how this work, let’s start with an approximation. The segment ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

![Rendered by QuickLaTeX.com \overline{CQ}](../../assets/134e1cfdbcf199dc.png)

![Rendered by QuickLaTeX.com \overline{QP}](../../assets/49e16eac9b639d51.png)


![](../../assets/a53cd91fd07935d0.png)

We calculate first the amount of light from ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)


![Rendered by QuickLaTeX.com \[I_Q = I_S \exp{\left\{-\beta{\left(\lambda, h_0\right)} \overline{CQ} \right\}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-bed106a65f8c0a1e2cb10230fa87ea31_l3.png)


Then, we use the same approach to calculate the amount of light that reaches ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)


![Rendered by QuickLaTeX.com \[I_P = \boxed{I_Q} \exp{\left\{-\beta{\left(\lambda, h_1\right)} \overline{QP} \right\}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f407f4c9bae5534c63499f9e227f95c0_l3.png)


If we subsitute ![Rendered by QuickLaTeX.com I_Q](../../assets/2d2d9b372424e7dc.png)


![Rendered by QuickLaTeX.com \[I_P = \boxed{I_S \exp{\left\{-\beta{\left(\lambda, h_0\right)} \overline{CQ} \right\}}} \exp{\left\{-\beta{\left(\lambda, h_1\right) \overline{QP} \right\}}=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-dd69421f59879105164dfc73961f94e5_l3.png)


![Rendered by QuickLaTeX.com \[=I_S \exp{\left\{-\beta{\left(\lambda, h_0\right)} \overline{CQ} -\beta{\left(\lambda, h_1\right) \overline{QP} \right\}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0dd07ececa2b75ca7bf2242fa5cc4d7e_l3.png)


If both ![Rendered by QuickLaTeX.com \overline{CQ}](../../assets/134e1cfdbcf199dc.png)

![Rendered by QuickLaTeX.com \overline{QP}](../../assets/49e16eac9b639d51.png)

![Rendered by QuickLaTeX.com ds](../../assets/a15125f89deb0218.png)


![Rendered by QuickLaTeX.com \[I_P=I_S \exp{\left\{-\boxed{\left({\beta{\left(\lambda, h_0\right)} +\beta{\left(\lambda, h_1\right)\left) ds} }} \right\}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-142166107f9f13860f6b8e97ccb6ea52_l3.png)


In the case of two segments of equal length with different scattering coefficients, the out-scattering can be calculated by summing up the scattering coefficient of the individual segments, multiplied by the segment lengths.

We can repeat this process with an arbitrary number of segments, getting closer and closer to the actual value. This leads to the following equation:

![Rendered by QuickLaTeX.com \[I_P = I_S\exp\left\{-\boxed{ \sum_{Q \in \overline{CP}}{\beta\left( \lambda, h_Q \right)}\, ds}\right \} \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-012c7190b9a08978e5a404c360b1a160_l3.png)


where ![Rendered by QuickLaTeX.com h_Q](../../assets/aa7ba7c6380c04a2.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)


The approach of splitting a line into multiple segments just like we have done is called **numerical integration**.

If we assume that the initial amount of light received is equal to ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


![Rendered by QuickLaTeX.com \[T\left(\overline{CP}\right) =\exp\left\{-\sum_{Q \in \overline{CP}}{\beta\left( \lambda, h_Q \right)}\, ds\right \} \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2c3b00d7db196a221e2947ef4ecf0b8d_l3.png)


We can further expand this expression by replacing the generic ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


![Rendered by QuickLaTeX.com \[T\left(\overline{CP}\right) =\exp\left\{-\sum_{Q \in \overline{CP}}{\boxed{\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{\rho\left(h_Q\right)}{N}\frac{1}{\lambda^4}}}\, ds\right \} \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-65ab05749a3ba0bed758f30bec26653e_l3.png)


Many factors of ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


![Rendered by QuickLaTeX.com \[T\left(\overline{CP}\right) =\exp\left{\underset{\beta\left(\lambda\right)}{\underset{\text{constant}}{\underbrace{\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{1}{N}\frac{1}{\lambda^4}}}}\overset{\text{optical depth}\,D\left(\overline{CP}\right)}{\overbrace{\sum_{Q \in \overline{CP}}{\rho\left(h_Q\right)}\, ds}}\right }\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6ac0ec5abd8c5b399c17fef7893fe519_l3.png)


The quantity expressed by the summation is referred to as **optical depth **![Rendered by QuickLaTeX.com D\left(\overline{CP}\right)](../../assets/11c6c8c1bb61575c.png)

**scattering coefficient at sea level**. In the final shader, we will calculate only the optical depth, and provide the scattering coefficients at sea level ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


To sum it up:

![Rendered by QuickLaTeX.com \[T\left(\overline{CP}\right) =\exp\left\{- \beta\left(\lambda\right)D\left(\overline{CP}\right)\right\}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0d4d6110899a42da9bd01535d860e1e2_l3.png)


If you are interested in this topic, I would also suggest reading [Carl Davidson](http://davidson16807.github.io/tectonics.js//2019/03/24/fast-atmospheric-scattering.html) post on atmospheric scattering, where he used an improved version of this iterative approach.

#### Coming Next…

This post explained how to model Earth’s atmosphere. With the next post, we will start writing the shader code necessary to simulate atmospheric scattering.

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) **Part 4.**[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557)- Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce the volumetric atmospheric scattering presented in this tutorial.

## Leave a Reply Cancel reply