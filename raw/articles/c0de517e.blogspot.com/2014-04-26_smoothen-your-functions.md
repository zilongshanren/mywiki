---
title: Smoothen your functions
url: http://c0de517e.blogspot.com/2014/04/smoothen-your-functions.html
published: '2014-04-26'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Do you have an "if", "step" or such? Replace with a saturate(multiply-add(x)).

Do you have a smoothstep? Replace with smootherstep...

Ok, kidding, but sort-of, I actually do often ed up replacing ramps (saturate/mad... the fairy dust of shading, I love sprinkling mads in shader code) instead of steps, I remember years ago turning a pretty much by-the-book crysis 1-style SSAO into a much better SSAO by just "feathering" the hard in/out tests (which is kinda what line sampling SSAO does btw).

If you think about it, it's a bit of "code smell". What shading functions should be discontinuous? True, most lighting has a max or saturate right? But why? Really we're considering infinitesimal lights, for physically realistic lights we would have an area of emission, and that area would be fractionally shadowed by a surface, so even there, the shadowing function wouldn't just be a step of the dot product. This might not be evident on diffuse, but already when you're trying to use half-angle based specular attention has to be taken when handling transition to the "nightside".

And of course even when reasonable, any "step" function (well -any- function!) in a shader should be anti-aliased... And of course everybody knows what's the convolution of a step with a box (pixel footprint) is...

[Texturing and Modeling, a Procedural Approach](http://www.amazon.com/Texturing-Modeling-Third-Edition-Procedural/dp/1558608486)is the canonical text for this, but it's funny, googling around one of the first hits is[this documentation page](https://renderman.pixar.com/resources/current/rps/basicAntialiasing.html)of Renderman on antialiasing, whose slides are horribly aliased. The OpenGL Orange Book also has examples, and I really want to mention[this IQ's article](http://www.iquilezles.org/www/articles/filtering/filtering.htm)on ray differentials even if it doesn't do analytic convolution...
Many times the continuity of derivatives is not that important (visible), that's why we can use saturated ramps (discontinuous in the first derivative) or saturated smoothsteps (discontinuous in the second), with the big exception of manipulating inputs to specular shading. In that case, even second-derivative discontinuities can very clearly show, thus the need of the famous "

[smootherstep](http://en.wikipedia.org/wiki/Smoothstep#5th_order_equation)".
Anyhow. I usually have a bunch of functions around to help with ramps, triangle ramps, smoothsteps and so on, most of them are trivial and can be derived on paper in a second or so. Lately I had to use a few I didn't know before, so I'll be writing them down here.

Yes, all this introduction was useless. :)

**- Smooth Min/Max**

log(pow(pow(exp(x),s) + pow(exp(y),s),1/s))

This will result is a smooth "min" between x and y for negative values of s (which controls the smoothness of the transition), "max" for positive values.

For s=-1 this results in the "smoothest" min:

log(exp(x+y)/(exp(x)+exp(y))

If you know that x,y are always positive a simpler formulation can be employed, as we don't need to go through the exponential mapping:

pow(pow(x,s) + pow(y,s),1/s)

Note also that if you need a soft minimum of more than two values, your expressions simplify, e.g. pow(pow(pow(pow(x,s) + pow(y,s),1/s),s) + pow(z,s),1/s) = pow(pow(x,s) + pow(y,s) + pow(z,s) ... ,1/s).


Note also the link between softmax and



Note also the link between softmax and

[norm-infinity](https://en.wikipedia.org/wiki/Uniform_norm).**- A few notes on smoothsteps**
Deriving smoothstep and smootherstep is trivial, just create a polynomial of the right degree (cubic or quintic) and impose f(0)=0, f(1)=1 and f'(0)=0, f'(1)=0 (and the same for f'' in case of smootherstep), solve and voila'.

Once you do that, it's equally trivial to start toying around and derive polynomials with other properties. E.g. imposing derivatives only at one extreme:

You can have a "smoothstep" with non-zero derivatives at the extremes:

Or a quartic that shifts the midpoint:

It would seem that the more "properties" you need to have the higher degree polynomial you need to craft. Until you remember that you can do everything piecewise...

Which is basically making small, specialized splines. For example, a quadric smoothstep can look like this:

Which is basically making small, specialized splines. For example, a quadric smoothstep can look like this:

This is helpful also because there are certain tradeoffs based on applications, especially as having continuous derivatives don't mean automatically that it will be nice looking...

You can make functions that impose more and more derivatives (and do you know that smoothsteps can be chained? smoothstep(smoothstep(x))...) but that doesn't mean the derivatives will "behave", as they can vary wildly in the domain and result in visible "wobbling" in shading.

Another thing that you might not have noticed is how close smoothstep is to a (shifted) cosine, I didn't before a coworker or mine, the all-knowing Paul Edelstein, mentioned it. Probably not too useful, but never know, in certain situations it might be applicable and cheaper.

**- Sigmoid functions**

Another class of functions that are widely useful are sigmoids, "s shaped functions"

Smooth Sigmoid: x/pow((pow(abs(x),s)+1),1/s)

Logistic: 1/(1+exp(-x))

Sigmoids are similar to smoothsteps, but usually reach zero derivatives at infinity instead at 0,1 endpoints.



They make nice "replacements" for "step" as they approach nicely their limits as they go to infinity:

But also for saturated ramps, especially the smooth sigmoid as it has f'(0)=1 as we have shown before.

Another sigmoid is the Gompertz function, which has nice and clear parameters:

asymptote*exp(-displacement*exp(-rate*x))

Beware though, it's not symmetric around its midpoint:

There are a ton more, but I'd say not as generic. If you look at the various tonemapping curves, most of them are sigmoids, but most of them are in exponential space and not symmetric.

In fact at a given point I made tonemapping curves out of sigmoids, piecewise sigmoids or other weird things glued together :)

**- Bias and Gain**

*(thanks to Steve Worley for reminding me of these)*

Bias pow(x,(-log2(a))

Gain if x < 0.5 then 0.5*bias(2*x, a) else 1-0.5*bias(2-2*x, a)

Schlick's Bias x/((1/a-2)*(1-x)+1)

Schlick's Gain if x < 0.5 then SBias(2*x,a)*0.5 else 1-0.5*SBias(2-2*x,a))

Bias is just a power (-log2(a) only maps 0...1 to the power), and Gain maps one power next to a mirrored copy around the midpoint, the easiest way you can construct a piecewise sigmoid (without imposing conditions on the derivatives and so on).

Schlick's versions were published in Graphics Gems IV, and are not only an optimization of the original Bias/Gain formulas (credited to Perlin's Hypertexture paper), but are symmetric over the diagonal, which is a nifty property (it also means that for parameter a the inverse curve is given by the same formula with 1-a)


*- Smooth Abs*

Obviously if you have any "smoothstep" you can shift it around zero to create a "smoothsign" and multiply by the original value to get a smoothed absolute. The rational polynomial sigmoid works quite well for that:

SmoothAbsZero d*x*x/sqrt(1+d*d*x*x)

SmoothAbs sqrt(x*x+e)

*And that's all what I have for now,*

**if you encountered other nifty functions for modelling and tinkering with procedurals and so on, let me know**in the comments!*I'm always looking for nifty functions that can be useful for sculpting mathematical shapes :)*



**- Bonus example: Soft conditional assignment**

*Some links:*

*Wikipedia has a not bad refresher on polynomials and rational polynomials for interpolation*[http://en.wikipedia.org/wiki/Polynomial_and_rational_function_modeling](http://en.wikipedia.org/wiki/Polynomial_and_rational_function_modeling)*Analytic approximation of the Heaviside function (HLSL step)*[http://mathworld.wolfram.com/HeavisideStepFunction.html](http://mathworld.wolfram.com/HeavisideStepFunction.html)and[http://en.wikipedia.org/wiki/Heaviside_step_function](http://en.wikipedia.org/wiki/Heaviside_step_function)*John D.Cook on smooth max*[http://www.johndcook.com/blog/2010/01/20/how-to-compute-the-soft-maximum/](http://www.johndcook.com/blog/2010/01/20/how-to-compute-the-soft-maximum/)*IQ on smooth min formulations*[http://www.iquilezles.org/www/articles/smin/smin.htm](http://www.iquilezles.org/www/articles/smin/smin.htm)also,**some other useful functions here**[http://iquilezles.org/www/articles/functions/functions.htm](http://iquilezles.org/www/articles/functions/functions.htm)*Paul Bourke on interpolation*[http://paulbourke.net/miscellaneous/interpolation//](http://paulbourke.net/miscellaneous/interpolation//)*Easing functions*[http://easings.net/](http://easings.net/)*Polynomial interpolating function toy*[http://www.timotheegroleau.com/Flash/experiments/easing_function_generator.htm](http://www.timotheegroleau.com/Flash/experiments/easing_function_generator.htm)*Schlick paper on bias and gain*[http://dept-info.labri.fr/~schlick/DOC/gem2.ps.gz](http://dept-info.labri.fr/~schlick/DOC/gem2.ps.gz)*R-Functions, a primer by Vadim Shapiro*[http://ecommons.library.cornell.edu/bitstream/1813/7059/1/91-1219.pdf](http://ecommons.library.cornell.edu/bitstream/1813/7059/1/91-1219.pdf)- IQ on the associativity of smin https://www.shadertoy.com/view/XdyGWt

## 8 comments:

Interesting idea about the smooth min/max! I note that your formula can be simplified a bit, to:





-log(exp(x*s) + exp(y*s)) / s

I had occasion once to try to make a smooth min filter for images - in other words, a min filter that weighs farther-away pixels less somehow, so that the resulting image remains smooth. I came up with this:

min(pixelValue + smoothstep(0, filterRadius, pixelRadius))

where the min is over all the pixels within filterRadius. If the image values are between 0 and 1, this leads to the min ignoring anything farther than filterRadius, "almost ignoring" things near filterRadius, and so on. Handy thing to remember.

Cool, thanks for noticing that, it's also nice to know that someone actually reads the formulas and everything :)



It's written in that way because I actually made first the "always positive" version, and you can notice that's the same just "dropping" the log/exp.

Cool also to know about the weighted min, I used something similar to bias a buffer towards "dark", I was actually planning to blog about that trick (it's actually in the fight night champion slides if you look for it)

I had some use for the weighted median as a denoising filter in the past as well (http://en.wikipedia.org/wiki/Weighted_median)

Inigo Quilez has a page of "useful little functions" here: http://iquilezles.org/www/articles/functions/functions.htm

I have a collection of 10 different contrast S-curves in the source code of SweetFX (look in the curves.h file) , as well as a few not-quite-working ones.





I use curve #2 the most - it's my current favorite.

You can find SweetFX at http://forums.guru3d.com/showthread.php?t=381912

There is also Dino Dinis Normalized Tunable Sigmoid Function : http://dinodini.wordpress.com/2010/04/05/normalized-tunable-sigmoid-functions/


And the followup 2.0 formula : https://www.youtube.com/watch?v=R5IZyQpYvZA

Dini's formuals are the same as Shlick's Gain

Schlick's versions were published in Graphics Gems 4, not 2.

Thanks for spotting the mistake

Post a Comment