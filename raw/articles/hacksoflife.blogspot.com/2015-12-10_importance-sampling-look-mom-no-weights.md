---
title: 'Importance Sampling: Look Mom, No Weights'
url: http://hacksoflife.blogspot.com/2015/12/importance-sampling-look-mom-no-weights.html
author: Benjamin Supnik
published: '2015-12-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For anyone doing serious graphics works, this post will be totally "duh", but it took me a few minutes to get my head straight, so I figure it might be worth a note.



As an example, imagine that we want to sample a lighting function integrated over a hemisphere, and we know that that lighting function has a cosine term (e.g. it is multiplied by the dot product of the light direction and the normal.)


What this means is that the contributing values of the integration will be largest in the direction of the normal and zero at 90 degrees.


We could sample equally all around the hemisphere to learn what this function does. But every sample around the the outer rim (90 degrees off) of the hemisphere is a total waste; the sampled function is multiplied by cos(90), in other words, zero, so we get no useful information. Spending a lot of our samples on this area is a real waste. Ideally we'd sample more where we know we'll get more information back (near the normal) and less at the base of the hemisphere.


One way we can do this is to produce a sample distribution over the hemisphere with weights. The weight will be


You can implement this by using a table of sample directions and weights and walking it, and you can get just about any sampling pattern you want. Buuuuuut...










#### Fair and Balanced or Biased?

The idea of importance sampling is to sample a function in a*biased*way, where you intentionally bias your samples around where most of the information is. The result is better leverage from your sampling budget.As an example, imagine that we want to sample a lighting function integrated over a hemisphere, and we know that that lighting function has a cosine term (e.g. it is multiplied by the dot product of the light direction and the normal.)

What this means is that the contributing values of the integration will be largest in the direction of the normal and zero at 90 degrees.

We could sample equally all around the hemisphere to learn what this function does. But every sample around the the outer rim (90 degrees off) of the hemisphere is a total waste; the sampled function is multiplied by cos(90), in other words, zero, so we get no useful information. Spending a lot of our samples on this area is a real waste. Ideally we'd sample more where we know we'll get more information back (near the normal) and less at the base of the hemisphere.

One way we can do this is to produce a sample distribution over the hemisphere with weights. The weight will be

*inversely proportional*to the sample density. We come up with a**probability density function**- that is, a function that tells us how likely it is that there is information in a given location, and we put more samples where it is high, but with lower weights. In the high probability regions, we get the sum of lots of small-weight samples, for a really good, high quality sampling. In the low probability region, we put a few high weight samples, knowing that despite the high weight, the contribution will be small.You can implement this by using a table of sample directions and weights and walking it, and you can get just about any sampling pattern you want. Buuuuuut...

#### Lighting Functions - Kill the Middle Man

With this approach we end up with something slightly silly:

- We sample a lighting equation at a high density region (e.g. in the middle of a specular highlight).
- We end up with a "strong" lighting return, e.g. a high radiance value.
- We multiply this by a small weight.
- We do this a lot.

- We sample a lighting equation in a low density region.
- We end up with a very low radiance value.
- We multiply it by a heavy weight.
- We do this once.

*match*the lighting function. The relative weight of the brightness thus comes from the number of samples (a lot at the specular highlight, very few elsewhere).

We can simplify this by (1) throwing out the weights completely and (2) removing from our lighting equation the math terms that are exactly the same as our probability density function. Steps 2 and 3 go away, and we can sample a simpler equation with no weighting.

Here's the key point: when you find a probability density function for some part of a lighting equation on the interwebs, the author

**will have already done this**.#### An Example

For example, if you go look up the GGX distribution equation, you'll find something like this:

GGX distribution:

float den = NdotH * NdotH * (alpha2 - 1.0f) + 1.0f;

return alpha2 / (PI * den * den);

That's the actual math for the distribution, used for analytic lights (meaning, like, the sun). The probability density function will be something like this:

float Phi = 2 * PI * Xi.x;

float CosTheta = sqrt( (1 - Xi.y) / ( 1 + (a*a - 1) * Xi.y ) );

float SinTheta = sqrt( 1 - CosTheta * CosTheta );

(In this form, theta of 90 points at your normal vector; Xi is a 2-d variable that uniformly samples from 0,0 to 1,1. The sample at y = 0 samples in the direction of your normal.)

Note that the probability density function contains no weights. That's because the sample density resulting from running this function over a hemisphere (you input a big pile of 0,0 to 1,1 and get out phi/theta for a hemisphere)

**replaces**the distribution function itself.
Therefore you don't need to run that GGX distribution function

*at all*when using this sampling. You simply sample your incoming irradiance at those locations, add them up, divide by the samples and you are done.#### Doing It The Silly Way

As a final note, it is totally possible to sample using a probability density function that is

*not*related to your actual lighting equation - you'll need to have sample weights and you'll need to run your full lighting equation at every point.
Doing so is, however, woefully inefficient. While it is better than uniform sampling, it's still miles away from importance sampling with the real probability density function replacing the distribution itself.

## No comments:

## Post a Comment