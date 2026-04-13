---
title: 'Proof Without Words: Gregory’s Theorem'
url: https://divisbyzero.com/2018/09/28/proof-without-word-gregorys-theorem/
author: Dave Richeson
published: '2018-09-28'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Archimedes famously used inscribed and circumscribed polygons to approximate the circumference of a circle. He then repeatedly doubled the numbers of sides to get an approximation for π.

![James_Gregory](../../assets/65f657baadc561c0.jpeg)

[James Gregory](https://en.wikipedia.org/wiki/James_Gregory_(mathematician)) did the same, but he used areas: He discovered the following beautiful double-recurrence relation that can be used to compute the areas of inscribed and circumscribed *n*-gons:

**Gregory’s Theorem. ***Let I k and Ck denote the areas of regular k-gons inscribed in and circumscribed around a given circle. Then for all n, I2n is the geometric mean of In and Cn, and C2n is the harmonic mean of I2n and Cn; that is,*

and


We can use these formulas to approximate π. For instance, a square inscribed in a unit circle has area *I*4=2 and a square circumscribed about the unit circle has area *C*4=4. Applying the recurrence relations, we obtain the following sequence of bounds:

n |
In |
Cn |
| 4 | 2 | 4 |
| 8 | 2.828427125 | 3.313708499 |
| 16 | 3.061467459 | 3.182597878 |
| 32 | 3.121445152 | 3.151724907 |
| 64 | 3.136548491 | 3.144118385 |
| 128 | 3.140331157 | 3.14222363 |
| 256 | 3.141277251 | 3.141750369 |
| 512 | 3.141513801 | 3.141632081 |
| 1024 | 3.14157294 | 3.14160251 |
| 2048 | 3.141587725 | 3.141595118 |

This summer I tweeted this theorem:

My friend [Tom Edgar](https://community.plu.edu/~edgartj/)—a mathematician at Pacific Lutheran University and a master at finding “proofs without words”—emailed me to see if I wanted to try finding a proof without words of Gregory’s theorem. This is what we came up with.

The two parts of Gregory’s theorem follow from the two parts of the following lemma. We give the proof… without words.

**Lemma. ** and


*Proof.*

![main](../../assets/fa88468e44e07e97.png)



God, I wish I knew your blog sooner.