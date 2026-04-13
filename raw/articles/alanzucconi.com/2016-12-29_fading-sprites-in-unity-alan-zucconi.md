---
title: Fading Sprites in Unity - Alan Zucconi
url: https://www.alanzucconi.com/2016/12/29/fading-sprites-unity-5/
author: Alan Zucconi
published: '2016-12-29'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial shows how to extend the class `SpriteRenderer`

to support intuitive, painless fading transitions. Despite referring to sprites, this approach can be used to easily animate any property of a game object in Unity.

[Introduction](https://www.alanzucconi.com#introduction)- Step 1.
[Extending the SpriteRenderer](https://www.alanzucconi.com#step1) - Step 2.
[The Coroutine](https://www.alanzucconi.com#step2) - Step 3.
[Invoking the Coroutine](https://www.alanzucconi.com#step3) - Step 4.
[The Callback](https://www.alanzucconi.com#step4) [Conclusion](https://www.alanzucconi.com#conclusion)

The link for the script used in this tutorial is at the end of the post.

One of the most important features that I feel Unity lacks, is the ability to animate sprites and material in an quick, efficient way. If you’re familiar with Unity you probably know that it comes with **Mechanim**, its own animation engine. However, using it to fade sprites in and out introduces too much overhead for a developer. If you want to make a sprite disappear by using Unity’s animation engine, you need to:

- Create an Animation that changes the alpha value of the sprite colour
- Create a finite state machine within the Animator, so that it can responds to events
- Connect the Animator to the object
- Trigger the animation via code

All of the above mentioned steps must be repeated for each animation, and it’s easy to see how tedious this can be. On top of that, Mechanim is a very powerful (and heavy) tool and I believe it’s not the right tool to use for something so simple.

The basic idea is to provide an intuitive interface that allows developer to fade sprites in the most natural possible way. It would be amazing to have a function called `FadeSprite`

that, when invoked on a `SpriteRenderer`

, make the sprite disappear. Something like this:

SpriteRenderer renderer = GetComponent<SpriteRenderer>(); renderer.FadeSprite();

Unfortunately, the `SpriteRenderer`

component doesn’t come with a `FadeSprite`

method. Likely, we can add it using a feature of C# called [extension methods](https://www.alanzucconi.com/2015/08/05/extension-methods-in-c/).

We can create the above-mentioned extension by adding the following C# class anywhere in our Unity project:

public static class SpriteRendererExtension { public static void FadeSprite(this SpriteRenderer renderer) { // ... } }

The use of the keyword `this`

in the definition of the first parameter makes the `FadeSprite`

method an extension of the class `SpriteRenderer`

. If everything worked, we can see that even Visual Studio now recognises `FadeSprite`

as a valid method we can invoke on any instance of `SpriteRenderer`

:

![](../../assets/d369c1e9dd491797.png)

Note that Visual Studio clearly shows that this method was not originally defined in the `SpriteRenderer`

class, showing *(extension)* before it.

This tutorial explores a different approach to animation, and is based on **coroutines**. If you are unfamiliar with this concept: coroutines are functions that, once invoked, are executed “in parallel” to your code and can lasts for several frames. Conversely, the traditional `Update`

and `Start`

methods that Unity offers will be executed in a single frame.

The idea is to start a coroutine within `FadeSprite`

. While the method we invoke terminates almost instantly, the coroutine that spawns will survive for as long as its needed. A possible implementation of this coroutine is:

private static IEnumerator SpriteCoroutine ( SpriteRenderer renderer, float duration ) { // Fading animation float start = Time.time; while (Time.time <= start + duration) { Color color = renderer.color; color.alpha = 1f - Mathf.Clamp01((Time.time - start) / duration); renderer.color = color; yield return new WaitForEndOfFrame(); } }

The coroutine takes an additional parameter, called `duration`

. The coroutine uses it to loop until enough time has passed. During each iteration, it alters the alpha value of the sprite, from one to zero. The `WaitForEndOfFrame`

class allows to split the execution of this code over several frames.

The first problem we encounter, however, is that coroutines in Unity can only be started from a `MonoBehaviour`

object. `SpriteRenderer`

, unfortunate, isn’t a `MonoBehaviour`

. To solve this problem, out extension method needs to receive a `MonoBehaviour`

as a parameter, and use it to spawn a coroutine. Something like this:

public static void FadeSprite ( this SpriteRenderer renderer, MonoBehaviour mono, float duration, ) { mono.StartCoroutine(FadeCoroutine(renderer, duration)); }

This needs to be invoked in the following way:

SpriteRenderer renderer = GetComponent<SpriteRenderer>(); renderer.FadeSprite(this, 2);

We can add some more feature to out extension method. The most useful is probably a **callback**. Callbacks are functions that can be passed as parameters. The idea is to pass a function that is finally invoked when the animation is completed. We can use it, for instance, to destroy the game object that we are fading out.

Callbacks in C# can be implemented using **delegates**. C# comes with a few delegates ready to use. One of the most common is `Action<>`

, which represents a function with a single parameter and no return value. Perfect for our scenario.

public static void FadeSprite ( this SpriteRenderer renderer, MonoBehaviour mono, float duration, Action<SpriteRenderer> callback = null ) { mono.StartCoroutine(FadeCoroutine(renderer, duration, callback)); }

Now we only need to invoke the callback at the end of the coroutine:

private static IEnumerator SpriteCoroutine ( SpriteRenderer renderer, float duration, Action<SpriteRenderer> callback ) { // Fading animation float start = Time.time; while (Time.time <= start + duration) { Color color = renderer.color; color.alpha = 1f - Mathf.Clamp01((Time.time - start) / duration); renderer.color = color; yield return new WaitForEndOfFrame(); } // Callback if (callback != null) callback(renderer); }

The easiest way in which we can use this, is:

... renderer.FadeSprite(this, 2f, DestroySprite); ... private void DestroySprite (SpriteRenderer renderer) { Destroy(renderer.gameObject); }

Alternatively, you can also create an anonymous function and use that as a parameter:

renderer.FadeSprite ( this, 2f, delegate (SpriteRenderer r) { Destroy(r.gameObject); } );

C# also allows for a more compact syntax, which some programmers prefer:

renderer.FadeSprite ( this, 2f, (SpriteRenderer r) => { Destroy(r.gameObject); } );

The technique shown in this tutorial allows to easily animate any property of a game object. The toy example shown in this post referred to a `SpriteRenderer`

, but its’ really up to you how to use it.

There are few aspects that could be improved:

**Support for multiple transitions.**What happens if we run two coroutines at the same time? Most likely, they’ll interfere with each other, causing the animation to glitch. A more structured approach should check whether any transition is currently occurring on an object, and act accordingly. This means either interrupting the current coroutine, or ignoring it. If you’re looking for a more advanced solution, you could store all the running coroutines in a static list.**Support for animation curves.**Lerping is boring, we all know it. Your fading function could take an animation curve as a parameter, and use it for a custom fading curve.**Support for in-game pause.**The current effect assumes the flow of time depends on`Time.time`

. If you have implemented your custom in-game pause system, the variable might not represent what the name suggests. You can pass a delegate to the fading function that indicates how to get the current time. For instance something like:

renderer.FadeSprite ( this, 2f, delegate () { return PauseManager.gameTime; } );.

You can download the script used in this tutorial from [Patreon](https://www.patreon.com/posts/7607389).

## Leave a Reply Cancel reply