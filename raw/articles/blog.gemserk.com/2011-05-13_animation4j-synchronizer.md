---
title: Animation4j - Synchronizer
url: https://blog.gemserk.com/2011/05/13/animation4j-synchronizer/
published: '2011-05-13'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In this post I will talk a bit more about [animation4j](https://github.com/gemserk/animation4j) project, particularly the Synchronizer class.

When working with transitions we could want to declare them in a seamlessly way. In a [previous post](https://blog.gemserk.com/2011/03/25/animation4j-transitions/) I introduced the [Transition

### Meet the Synchronizer

For this reason, animation4j provides a class named [Synchronizer](https://github.com/gemserk/animation4j/blob/master/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/sync/Synchronizer.java), which handles all the synchronization internally for you. To create a new transition you have to declare something like this:

// create a synchronizer in some part of your initialization code Synchronizer synchronizer = new Synchronizer(); // create a transition in some parte of your game logic, for example when the user press something Vector2f position = new Vector2f(100, 100); synchronizer.transition(position, Transitions.transitionBuilder().end(new Vector2f(200, 200)).time(500)); // this will perform the synchronization, it will set to my object the current value of the transition. // normally this call will be on an update() method of your game synchronizer.synchronize(delta); // so now my object will be update with the new values System.out.prinln(position);

note: I used a [Vector2f](https://github.com/gemserk/animation4j/blob/master/animation4j-core/src/test/java/com/gemserk/animation4j/Vector2f.java) class in the example because it is a known class, all libraries have a Vector implementation.

In the previous example, I create a transition of a Vector2f class from (100,100) to (200, 200) in 500ms.

To register a new transition to be synchronized you call transition() method and each time synchronize(delta) method is called, Synchronizer will perform synchronization of all registered transitions. The registration method comes in to flavors, one will modify the object you pass but it only works if you are using a mutable object. The other one works over the field of an object using reflection and calling public set method to modify the internal field. It works for both mutable and immutable objects because it is setting a new value each time, however, one pending improvement is to modify current field value, instead creating a new one each time, when the field class is mutable.

Synchronizer class could be used in a static way using the Synchronizers class, which holds an internal singleton instance to do all the work. That is really useful when you want to use the synchronization stuff wherever you want. However a restriction is that it will updates all registered transitions and that could be a problem if you have different states for your game, for example, a pause game state which keeps rendering a playing game state, you don’t want the transitions started in that state to go on, so in that case could use different instances for each game state.

### TransitionBuilder is your friend

Another interesting stuff added to the library is the [TransitionBuilder](https://github.com/gemserk/animation4j/blob/master/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transitions.java) class provided inside the Transitions class. In previous versions, there were different methods to create a Transition using the [Transitions](https://github.com/gemserk/animation4j/blob/master/animation4j-core/src/main/java/com/gemserk/animation4j/transitions/Transitions.java) factory class, one only specifying speed, other specifying speed and end value, other specifying speed and the interpolation functions, and the list goes on and on. In order to improve this, the TransitionBuilder class was created. It lets you specify the parameters you want when building a Transition, for example:

Transition transition = Transitions.transitionBuilder().start(v1) .end(v2) .time(5000) .functions(InterpolationFunctions.easeIn(), InterpolationFunctions.easeOut()) .build();

The previous code will create a transition from value v1 to value v2 in 5000ms using the declared interpolation functions to interpolate between the internal values of v1 and v2 (as explained in a [previous post](https://blog.gemserk.com/2011/03/26/animation4j-interpolation-functions/)).

These classes simplify a lot working with animation4j but there is still a lot of work to do in order to improve usage and internal performance.