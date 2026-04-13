---
title: Animation4j - Transitions
url: https://blog.gemserk.com/2011/03/25/animation4j-transitions/
published: '2011-03-25'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As we said on a previous post, we are going to talk a bit more about the current released version (0.0.8) of [animation4j](https://github.com/gemserk/animation4j), remember that the API could change since we wrote this post.

In this case, we are going to talk about making a transition from one value to another in some time. Animation4j provides you one interface to make transitions, the [Transition](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transition.java) interface, the API by now looks like this:

public interface Transition<T> { /** * Returns the current value of the transition. * */ T get(); /** * Start an interpolation from a to b in the specified default time. * * @param t * The wanted new value. */ void set(T t); /** * Start an interpolation from a to b in the specified time. * * @param t * The wanted new value. * @param time * The time to set the new value. If time is zero, then value is applied directly. */ void set(T t, int time); }

The library uses generics so you can create transitions of any type. To do this, you can use the [Transitions](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transitions.java) factory class, where you can create transitions for your types. The API of the factory class looks like this:

<T> Transition<T> transition(T startValue, TypeConverter<T> typeConverter);

The current Transition generic implementation internally work with a float[] in order to optimize memory and to simplify internal work. To use it, you will have to create a converter from your type to float[] and vice versa by implementing the [TypeConverter

/** * Provides a way to convert an object in a float[] array and vice versa, for interpolation purposes. * * @param <T> * The type to convert. * @author acoppes */ public interface TypeConverter<T> { /** * Returns the quantity of variables are used to convert the object to the float[] and vice versa. * * @return the quantity of variables used. */ int variables(); /** * Copy the values of the object to the specified float array, if null it will create a new float array. * * @param object * The object from where to get the values to fulfill the float array. * @param x * The float array to copy the values of the object. If null it will create a new float array. * @return The float array with the values of the object. */ float[] copyFromObject(T object, float[] x); /** * Copy the values of the float array to the specified object. * * @param object * The object which the float array values will be copied to. If null or object immutable, it will create a new object. * @param x * The float array to get the values to fulfill the object. * @return An object with the values of the float array. */ T copyToObject(T object, float[] x); }

Type converters should be stateless, so you can reuse a single type converter for all your transitions of the same type. For the next Vector2f class example:

public class Vector2f { public float x,y; public Vector2f(float x, float y) { set(x,y); } public void set(float x, float y) { this.x = x; this.y = y; } }

We could create the next type converter:

public class Vector2fConverter implements TypeConverter<Vector2f> { @Override public float[] copyFromObject(Vector2f v, float[] x) { if (x == null) x = new float[variables()]; // don't worry about garbage generation, the transition implementation will cache these values. x[0] = v.x; x[1] = v.y; return x; } @Override public Vector2f copyToObject(Vector2f v, float[] x) { if (v == null) v = new Vector2f(0, 0); // don't worry about garbage generation, the transition implementation will cache these values. v.x = x[0]; v.y = x[1]; return v; } @Override public int variables() { // we are only using two variables. return 2; } }

So, to create a transition, your code would look like:

TypeConverter<Vector2f> converter = new Vector2fConverter(); // could be reused Transition<Vector2f> transition = Transitions.transition(new Vector2f(100, 100), converter); // now, set a transition to (500,500) in five seconds. transition.set(new Vector2f(500, 500), 5000); // wait some time, and get the value interpolated Vector2f v = transition.get();

For more information, there is an [transitions example](https://github.com/gemserk/animation4j/blob/animation4j-0.0.8/animation4j-examples/src/main/java/com/gemserk/animation4j/examples/TransitionsExample.java) in the examples module.

The idea is to provide different TypeConverter implementations for different libraries as project modules so you don’t have to implement a TypeConverter for a Slick2D vector2f, or libgdx Vector2. However it is really easy to implement a type converter and you only have to do it once. Also, you will probably use transitions only for some types.

In one of the next posts, we want to talk about interpolation functions (and how are they used for transitions) as they are key concepts in animation4j project.