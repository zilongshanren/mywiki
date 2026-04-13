---
title: Extension methods in C# - Alan Zucconi
url: https://www.alanzucconi.com/2015/08/05/extension-methods-in-c/
author: Alan Zucconi
published: '2015-08-05'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Following the heritage of C++, C# comes with a number of powerful features which can either be used to massively improve your code …or to make it completely unreadable. In this post we’ll discuss a technique to add new methods to already existing classes. Yes, even classes you don’t have access to such as `Vector3`

, `Rigidbody`

and even `string`

. Let’s introduce * extension methods* with a practical example.

### The problem

Let’s imagine you have a game object with a rigid body you want to suddenly stop. You might want to do that for a number of reasons, such as pausing your game or stopping the time. A possible first approach is to set the relevant properties of the rigid body (velocity, angular momentum, etc…) to zero, an then set the property `isKinematic`

to `true`

. As a result your game object will not be controlled by PhysX any more. This is a possible way of doing it:

// Gets the rigidbody public new Rigidbody2D rigidboyd2D; public void Awake () { rigidbody2D = GetComponent<Rigidbody2D>(); } // Freezes is public void Freeze () { rigidbody2D.velocity = Vector2.zero; rigidbody2D.angularVelocity = 0; rigidbody2D.isKinematic = true; }

This method works, but is not very elegant.

### Introducing extension methods

It would be much more elegant if the class `Rigidbody2D`

itself had provided the `Freeze `

method. Luckily enough, C# allows you to add a method to a class from another file. This is done by creating a *static class *with has a *static method, *which has a `Rigidbody2D`

as its first parameter. All the magic happens by adding the keyword `this`

…

public static class Rigidbody2DExtension { public static void Freeze (this Rigidbody2D rigidbody2D) { rigidbody2D.velocity = 0; rigidbody2D.angularVelocity = 0; rigidbody2D.isKinematic = true; } }

By doing this, a new method called `Freeze`

will be added to `Rigidbody2D`

:

rigidbody2D.Freeze(); // Equivalent to Rigidbody2DExtension.Freeze(rigidbody2D);

Both the class and the methods can have the name you like. If you are using Visual Studio or any other sufficiently advanced IDE, you’ll see that `Freeze`

is marked as an *extension method*:

![c](../../assets/ac42d0bdffef9bfb.png)

### Handling nulls

It’s important to notice that extension methods are not methods in the “traditional” sense. The definition of the `Rigidbody2D`

class has not been altered during compilation. Quite the opposite, the compiler changes any call to `Rigidbody2D.Freeze`

to `Rigidbody2DExtension.Freeze`

. This means that even if `rigidbody2D`

is `null`

, the function can still be invoked successfully. We can then embed all the integrity check directly into the `Freeze`

method:

public static bool Freeze (this Rigidbody2D rigidbody2D) { if (rigidbody2D == null) return false; rigidbody2D.velocity = 0; rigidbody2D.angularVelocity = 0; rigidbody2D.isKinematic = true; return true; }

This is extremely powerful, because it allows to get rid of many null checks. At the same time, it can hide structural problems in your code and finding null references can be harder.

### Saving the state

Let’s improve our code by saving the state of the rigid body so that it can be restored later:

// The state of a Rigidbody2D public class Rigidbody2DState { public Vector2 velocity; public float angularVelocity; } // Inside the Rigidbody2DExtension class public static Rigidbody2DState GetState (this Rigidbody2D rigidbody2D) { Rigidbody2DState state = new Rigidbody2DState(); state.velocity = rigidbody2D.velocity; state.angularVelocity = rigidbody2D.angularVelocity; return state; }

which can be called as:

Rigidbody2DState state = rigidbody2D.GetState();

### Adding references

If you’re going to invoke `GetState`

a lot, creating new objects is not a good idea. The best way is to create the object once and then re-use it. We can then pass the instance to `GetState`

so that it can be recycled.

public static Rigidbody2DState GetState (this Rigidbody2D rigidbody2D, Rigidbody2DState state = null) { if (state == null) state = new Rigidbody2DState(); state.velocity = rigidbody2D.velocity; state.angularVelocity = rigidbody2D.angularVelocity; return state; }

Which can be invoked like this:

state = rigidbody2D.GetState(state)

### Other uses

C# has several interesting features which game developers rarely encounter. Learning to master a language so powerful can really speed up your coding. For instance, you can extend the class `string`

to add this interesting method:

public static bool IsNullOrEmpty(this string value) { return string.IsNullOrEmpty(value); } // Old version string.IsNullOrEmpty(myString); // New version myString.IsNullOrEmpty();

[tmachineorg](https://www.reddit.com/user/tmachineorg) on Reddit suggested an extension method to get a component, or add it if it doesn’t exist:

public static T Get<T>(this GameObject gameObject) where T: Component { T result = gameObject.GetComponent<T>(); if(result == null) result = gameObject.AddComponent<T>(); return result; }

Of, if you like the fancy double question mark operator:

public static T Get<T>(this GameObject gameObject) where T: Component { return gameObject.GetComponent<T>() ?? gameObject.AddComponent<T>(); }

Another interesting way of using extension method for Unity is to simply the way the position of an object is changed. Since `transform.position`

is a property and not a variable, it cannot be changed directly; trying to write into into one of its fields (such as `transform.position.x = 10`

) will result in an error. This can be solve by doing this:

public static Vector3 ChangeX (this Transform transform, float x) { Vector3 position = transform.position; position.x = x; transform.position = position; return position; } // Do the same for ChangeY and ChangeZ // ... // Old version Vector3 position = transform.position; position.x = 10; transform.position = position; // New version transform.ChangeX(10);

Alternatively, you can “transform” `Vector3`

s in *packed arrays*, like the one used in shaders:

public static Vector3 xyz (this Vector3 v, float x, float y, float z) { v.x = x; v.y = y; v.z = z; return v; } public static Vector3 xy (this Vector3 v, float x, float y) { v.x = x; v.y = y; return v; } public static Vector3 xz (this Vector3 v, float x, float z) { v.x = x; v.z = z; return v; } // ...

Which allows to write:

Vector3 v = Vector3.zero; v.xz(5f,10f)

### Conclusion

Extension methods are powerful enough to make your code more expressive by creating safe shortcuts and aliases. But all these changes are not just cosmetic; if used properly they can dramatically reduce the number of mistakes and avoid code duplication. The only shortage of this technique is that it can’t be used to change an existing method. Creating an extension method with the same signature or another one is not an error; however, it will always be shadowed by the original one hence, never called.

*Use extension methods responsibly.*

#### Other resources

[PicosRapture](https://github.com/foolmoron/PicosRapture/tree/master/Assets/Scripts/Extensions): A very beefy set of method extensions specifically designed for Unity;[PubSub from scratch](http://forspareparts.github.io/2015/05/22/messaging-in-unity-pt-2/): A more efficient way to implement a messaging system in Unity without`SendMessage`

.

## Leave a Reply Cancel reply