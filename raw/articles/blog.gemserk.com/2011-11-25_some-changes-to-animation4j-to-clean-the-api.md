---
title: Some changes to animation4j to clean the API
url: https://blog.gemserk.com/2011/11/25/some-changes-to-animation4j-to-clean-the-api/
published: '2011-11-25'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Lately, [animation4j](https://github.com/gemserk/animation4j) API received some love by removing a lot of unused classes and improving a bit how things are used. Now both Transitions and Timelines (hence the animations based time lines) work over mutable objects only.

To illustrate some of the changes there are two examples shown in the next sections.

### Transitions

This example shows how to use new API to create a Transition:

// a mutable object example, if you use LibGDX this could be a Vector2 class MyObject { float a, b; } // we need a TypeConverter for that object, as explained in a previous post. // an instance of this class could be reused since holds no internal state class MyObjectTypeConverter implements TypeConverter<MyObject> { @Override public float[] copyFromObject(MyObject o, float[] x) { if (x == null) x = new float[variables()]; x[0] = o.a; x[1] = o.b; return x; } @Override public MyObject copyToObject(MyObject o, float[] x) { if (o == null) o = new MyObject(); o.a = x[0]; o.b = x[1]; return o; } @Override public int variables() { return 2; } } // now, to create a transition to be used we use the Transitions class which provides // some builder methods MyObjectTypeConverter myObjectTypeConverter = new MyObjectTypeConverter(); MyObject myObject = new MyObject(); Transition transition = Transitions.transition(myObject, myObjectTypeConverter) // .start(0f, 50f) // .end(1f, 50f, 100f) // (time, value1, value2, ....) .build(); transition.update(0.5f); // this should print 25,75 since the update of the transition updated the object // directly. System.out.println("" + myObject.a + "," + myObject.b);

### TransitionBuilder

[TransitionBuilder](https://github.com/gemserk/animation4j/blob/271dbf21b08e1a8c4aef81a45dc3270f04f2bfa9/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transitions.java) changed its interface to create transitions specifying the object to be modified. It now also provides some methods which lets you specify the start and end values with a float[] by using var args, it is convenient if you want to write less code (you could avoid new Object(..)) but will generate garbage as new Object() does. The recommendation to avoid that is to reuse the end/start values, for example, if you want a Transition of a color from yellow to red, create the yellow and red colors and store them somewhere (maybe static final fields) and reuse them each time you need a new Transition.

### Animations

This example shows how to create an Animation which uses a Timeline:

// using the same classes we defined before MyObjectTypeConverter myObjectTypeConverter = new MyObjectTypeConverter(); MyObject myObject = new MyObject(); Animation animation = Builders.animation(Builders.timeline() // .value(Builders.timelineValue(myObject, myObjectTypeConverter) // .keyFrame(0f, new MyObject(50, 50)) // at the beginning of the Timeline, the object should be at 50, 50 .keyFrame(2f, new MyObject(100, 100)) // two seconds after that, it should be at 100, 100 .keyFrame(10f, new MyObject(200, 200)) // eight seconds after that, it should be at 200, 200 )) // .speed(2f) // we want the animation to run at double speed .build(); animation.start(1); // starts the animation with 1 iteration. animation.update(1f); // this should print 100,100 since the update we asked for double speed. System.out.println("" + myObject.a + "," + myObject.b); animation.update(4f); // this should print 200,200 System.out.println("" + myObject.a + "," + myObject.b);

(note: if you want more examples, there is an examples project with the project, some of the examples needs to be simplified but the idea of how to used animations and transitions should be clear enough)

Animation interface is very rich, it has methods to start the animation specifying the iterations you want, if you want to alternate directions or not, etc.

### Immutable Objects

As I said before, animations and transitions can only be performed over mutable objects. This means you can’t animate a java.lang.Float or a java.awt.Color since you have no way to change their values without creating a new instance. To animate immutable objects the idea is to create your own mutable objects with the corresponding variables, animate them and then, when needed, create a new instance of the required immutable object using the values of the mutable instance, for example, new java.awt.Color(values).

### Conclusion

All the changes were made to improve performance and reduce garbage generation, mainly because we are using the project on our Android games. The changes also improve the usability of the library since they reduce a lot of noise and reduce what you need to use. For example, all the modules slick2d, java2d and componentsengine were removed from the project since they had unused code and they depended on libraries that aren’t on maven central.

I wanted to share a bit the changes but, as things keep changing, for now all this stuff is on an unstable 0.2.0-SNAPSHOT version and wasn’t released on maven central yet.