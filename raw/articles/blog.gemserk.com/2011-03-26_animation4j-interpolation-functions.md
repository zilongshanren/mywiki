---
title: Animation4j - Interpolation Functions
url: https://blog.gemserk.com/2011/03/26/animation4j-interpolation-functions/
published: '2011-03-26'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Interpolation Functions are a key concept in animation4j project, they define how to a variable should change from one value to another. To define interpolation functions in animation4j, [InterpolatorFunction](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/interpolator/function/InterpolatorFunction.java) interface should be implemented, the API looks like this:

public interface InterpolatorFunction { /** * @param t * A real number in the interval [0,1] * @return The interpolated value. */ float interpolate(float t); }

So basically, functions works for values of `t`

between interval [0,1]. An example [implementation](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/interpolator/function/LinearBezierInterpolatorFunction.java) of this function is a linear [Bézier](https://en.wikipedia.org/wiki/B%C3%A9zier_curve):

/** * Linear Bézier curve implementation of an InterpolatorFunction. * */ public class LinearBezierInterpolatorFunction implements InterpolatorFunction { private final float p0, p1; public LinearBezierInterpolatorFunction(float p0, float p1) { this.p0 = p0; this.p1 = p1; } @Override public float interpolate(float t) { if (t < 0) return p0; if (t > 1) return p1; return (1 - t) * p0 + t * p1; } }

The library already provides some implementations, you could instantiate them using [InterpolatorFunctionFactory](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/interpolator/function/InterpolatorFunctionFactory.java) factory class. The API of the factory looks like this:

// returns a cubic Bézier interpolation function based on the four specified points. InterpolatorFunction cubicBezier(float p0, float p1, float p2, float p3); // returns a quadratic Bézier interpolation function based on the four specified points. InterpolatorFunction quadratic(float p0, float p1, float p2); // returns a cubic Bézier interpolation function with presetted values. InterpolatorFunction ease(); // returns a linear Bézier interpolation function. InterpolatorFunction linear(); // returns a cubic Bézier interpolation function with presetted values. InterpolatorFunction easeIn(); // returns a cubic Bézier interpolation function with presetted values. InterpolatorFunction easeOut(); // returns a cubic Bézier interpolation function with presetted values. InterpolatorFunction easeInOut();

In the previous post we talked about transitions of variables from one value to another using [Transition](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transition.java) interface. When building a transition using the [Transitions](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transitions.java) factory, you could specify the interpolation functions you want to use, if you don’t, then linear Bézier functions are used by default. One example of how to create a Transition specifying the interpolation functions looks like this:

Transition<Vector2f> transition = Transitions.transition( new Vector2f(0f, 0f), // the starting value vector2fConverter, // the type converter (using two variables) InterpolatorFunctionFactory.easeOut(), // the interpolation function for the first variable InterpolatorFunctionFactory.easeIn()); // the interpolation function for the second variable

One thing to mention is that Transitions factory methods use a varargs to specify interpolation functions parameters because we don’t know beforehand how many variables you need. In case you specify less functions than variables, then linear Bézier functions will be used for the variables without functions specified.

As we said on the previous post, animation4j API could change since this blog post was written. API used for this post is the one of the [current released version 0.0.8](https://github.com/gemserk/animation4j/tree/animation4j-0.0.8) (already uploaded to maven central).