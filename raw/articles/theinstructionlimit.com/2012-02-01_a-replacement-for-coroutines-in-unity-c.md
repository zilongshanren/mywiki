---
title: A Replacement for Coroutines in Unity + C#
url: https://theinstructionlimit.com/a-replacement-for-coroutines
author: Author Renaud Bédard
published: '2012-02-01'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

[Coroutines](http://unity3d.com/support/documentation/ScriptReference/index.Coroutines_26_Yield.html) are a great idea and super useful, but they’re kind of unwieldy to use in C# and sometimes they just don’t plain work. Or I don’t know how to use them properly. All I know is that they’re more complicated than they need to be, and I remember having problems using them from an Update method.

So I made my own version of Coroutines inspired by the XNA [WaitUntil](http://theinstructionlimit.com/waituntil-component) stuff I posted about a long time ago. Here it is!

using System; using UnityEngine; using Debug = UnityEngine.Debug; using Object = UnityEngine.Object; class ConditionalBehaviour : MonoBehaviour { public float SinceAlive; public Action Action; public Condition Condition; void Update() { SinceAlive += Time.deltaTime; if (Condition(SinceAlive)) { if (Action != null) Action(); Destroy(gameObject); Action = null; Condition = null; } } } public delegate bool Condition(float elapsedSeconds); public static class Wait { public static void Until(Condition condition, Action action) { var go = new GameObject("Waiter"); var w = go.AddComponent<ConditionalBehaviour>(); w.Condition = condition; w.Action = action; } public static void Until(Condition condition) { var go = new GameObject("Waiter"); var w = go.AddComponent<ConditionalBehaviour>(); w.Condition = condition; } }

Here’s an example of use, straight out of the [Volkenessen](http://theinstructionlimit.com/volkenssen-global-game-jam-2012) code (with special guest appearance from my [ported easing functions](http://theinstructionlimit.com/flash-style-tweeneasing-functions-in-c)) :

var initialOffset = new Vector3(hitDirection.x * -1, 0, 0); var origin = armToUse.transform.localPosition; armToUse.renderer.enabled = true; Wait.Until(elapsed => { var step = Easing.EaseOut(1 - Mathf.Clamp01(elapsed / Cooldown), EasingType.Cubic); armToUse.transform.localPosition = origin + initialOffset * step; return step == 0; }, () => { armToUse.renderer.enabled = false; });

What’s going on here :

- You call
`Wait.Until`

as a static method and pass it one or two methods (be it lambdas or method references) : The first one is the*Condition*which gets evaluated every Update until it returns true, and the second gets evaluated when the condition is true (it’s a shorthand, basically) - The Wait static class instantiates a “Waiter” game object and hooks a custom script component to it that does the updating and checking stuff
- The condition gets passed the number of seconds elapsed since the component was created, so you don’t have to keep track of it separately.

I use it for waiting for amounts of time (`Wait.Until(elapsed => elapsed > 2, () => { /* Something */ })`

), interpolate values and do smooth transitions (like the code example above, I animate the player’s arm with it), etc.

I’ll probably keep updating my component as I need more things out of it, but up to now it’s served me well. Hope it helps you too!

I agree that coroutines are unwieldy to handle in C# but I never had an issue with them not working. Do you have an example where you struggled with using them?

I like the approach of using delegates to define the wait condition, which gives great freedom to implement different conditions. However, this approach looses the sequential nature of coroutines, which is great to script sequences of actions spread over time. It seems to me be two approaches are quite different in what they’re trying to achieve.

Yeah, I should’ve researched what I’m complaining about more before posting. I’ll try to reproduce my problems and post back.

I also agree that the approaches are different, but out of habit I’ve never felt the need to have more than what my Waiters provide.

I’ve been linked a comprehensive article on coroutines and how they work on twitter, looks like I have some studying to do. :P

Might you be willing to post that link here?

Hmm, that was 3 years ago… I can’t recall what that link was, sorry. I’m sure there’s good resources if you look around though!

Dude, when we worked together last year I liked your waiters so much that I reimplemented a lightweight variant of them in Unity too. I didn’t share the code because, uh, I’m still sort of shy about sharing code for some reason, but now I feel silly for not at least sending it to you/telling you about it!

In my variant, I have an overloaded version of the instantiation method that allows you to attach the new component to an arbitrary GameObject — which can be useful in cases where an object affected by the action might be destroyed, or is otherwise mutable in a such a way that would require the interruption of the action before it’s through.

Aha! Glad to hear it :D

Hooking to an existing object is a great idea, and addresses the problem of garbage (one short-lived object per waiter isn’t very nice for the GC). I’ll try it when I have a chance!

I shamelessly took your idea and went a few steps further: http://theoneswiththelight.com/2012/unity-taskmanager/. I’m pretty sure it’s garbage free, allows for multiple task managers (so you can easily scope tasks and disable task managers when you go paused), and allows for chaining up all sorts of behaviors with its fluent API.

:)

Seeing as my stuff was shamelessly taken from YOUR interpolators, this just loops the loop :D

I really like your implementation!

Oddly enough, I came up with a similar, mostly garbage free concept based around what I term tasks. It uses a coroutine to run the show so that it turns itself on/off as needed and allows tasks to occur on the UI thread or a background thread: https://github.com/prime31/P31TaskManager/blob/master/Assets/P31TaskManager/P31TaskManager.cs

I mostly do stuff using stock Coroutine functionality, since you don’t have to put anything into “void Update()”.

Everybody had issues figuring out Coroutines, but once you figure out why Unity3D developers implemented it – you will get a hang of it.

Unitygems.com helped me a lot on this topic, but now it’s unfortunately down. Anyways, somebody made a cached copy of it.

https://web.archive.org/web/20140626101041/http://unitygems.com/

Correct, this post is almost 3 years old now :)

I do use Coroutines and I phased out my “replacement” from my projects. I still think it can be a nice exercise in how to use lambdas, and how to use fluent interfaces to chain functions.