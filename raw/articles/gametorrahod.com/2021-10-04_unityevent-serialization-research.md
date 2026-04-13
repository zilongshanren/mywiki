---
title: UnityEvent Serialization Research
url: https://gametorrahod.com/unityevent-serialization-research/
author: Sirawat Pitaksarit
published: '2021-10-04'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

This is something I always forget when designing a new API that I want to be compatible with `UnityEvent`

target serialization. I would like to end that, by writing this article so I could come back and read instead of blindly trial-and-error again to no avail.

## What is `UnityEvent`

serialization?

Everyone knows that declaring `public`

will "expose the variable".

More correct term is that it mark that field for **serialization. **Serialization means the data could be remembered in the asset or in the scene instead of starting from zero. It is the data you can input to that exposed slot that get **saved.**

Then advanced Unity users know that `[SerializeField]`

property is a way to also allows other access modifier not `public`

to be serialized.

Finally even more advanced Unity user knows that `UnityEvent`

is equivalent to C# `Action`

but more awesome because it could be serialized! In other words, you get a nice editor that allows assigning invoke targets, which stays there nicely.

![](../../assets/ebe5e75e58f07918.png)

![](../../assets/18a47a64800bcdaa.png)

![](../../assets/5fa4782e58692d47.png)

Despite an editor feature this nice available, I still see tons of Unity developers intentionally not using `Button`

's nice on click event box that appears in the editor and instead assign everything by code even though they are only one-time assignment. A month or so later, it is impossible to trace which button do what because they are all empty in the editor, and who know which code assign or replace the listener at which moment!

Main topics here is that what would be the criteria to make it appear in the dropdown? Surely, these aren't everything that `Camera`

has to offer.

![](../../assets/0ea5f76a5f382b4c.png)

### What does the serialization looks like?

![](../../assets/5537adf9ac17e223.png)

Notice that it "remember" the target with **assembly-qualified class name. **This has some concerns :

- If you change the
**class name**will everything breaks? - If you move the class to different
`.asmdef`

will it also breaks? - Remembered
**argument**is also assembly qualified full name. If Unity is evil and change assembly name of`UnityEngine`

then would it breaks the universe? - If you refactor target method's name, I think it will breaks?

## Argument editor is more awesome than you think

You see the check box above for booleans. It also supports number box and string box. But less known feature (probably) is that it also supports an asset picker!

![](../../assets/3411f8beea71f827.png)

![](../../assets/3f2f376a6a5cefdf.png)

![](../../assets/bc0659d78740eca2.png)

This is really useful to not have little pieces of audio playing code bits littering all over. Also it is extremely good with **prefab workflow. **It shows the blue override bar correctly. The prefab variant can add more entries, keep inheriting entries from root prefab, etc. It is critical with the new Unity Localization package which it uses event targeting extensively, all my texts are a variant of one root text prefab! But it is not our interest right now.

The serialization :

![](../../assets/e07f6fe911571e9b.png)

You also notice here that it is limited to only 5 types : object, int, float, string, bool. But the object type is so flexible and is my favorite. You should abuse it!

## When will things break

See that `Assembly-CSharp`

over there? I thought I could instantly screw up the serialization simply by moving the `ConnectionTarget`

to different assembly.

![](../../assets/992167734fa0946c.png)

But turns out it is still fine.

![](../../assets/490ab8d0e28d07eb.png)

Seems like the **priority goes to the class name first** and assembly is there to tie-break. If I rename the class...

![](../../assets/d57154faf643851e.png)

Ok finally it breaks!

![](../../assets/273f61ef90396ba0.png)

But you can still save its life. By doing things in this scene and save it, it will **not try to nullify invalid serialization. **Therefore when you realized you broken the link as far as the last month, it could still be saved somehow as old serialization is still there.

I could remove the `z`

in the class name, and the serialization **could come back to life**.

In a way, this non-GUID serialization is both blessing and a curse. Sometimes it makes you unable to refactor. But at the same time it allows certain flexibility... once in my project, I got into deep trouble and break everything in the project while refactoring!! I fixed the problem by scanning all YAML files and perform string replace of these class names and an entire project is saved. Thank god.

## Dynamic events

It means that normally `UnityEvent`

requires an invoker to **specify nothing, **the argument is **fixed **by whatever serialized.

Therefore **dynamic **means that the argument is specified **by the invoker** instead. Unity supports this by providing you `UnityEvent<T>`

, `UnityEvent<T1,T2>`

, .. and so on. Up to 4 dynamic parameters. (Note that static one only supports 1 argument that you can type in Unity Inspector.)

![](../../assets/7a5916c0000e5769.png)

But the catch is Unity can't serialize generic classes, it must be a solid class known ahead of time. How to make it "solid" is like this. It could be `private`

just fine too but remember to put on that `[Serializable]`

(Unlike fields, a `public class`

is not automatically serializable.)

![](../../assets/17d076727c07f6ae.png)

Conveniently, Unity shows eligible dynamic event target up top. Selecting this no longer show `AudioClip`

selection box, because invoker will supply it.

![](../../assets/377006f1b8416d9c.png)

You can still ignore the dynamic event and go back to use the static one as well.

![](../../assets/45dc90085f8dca87.png)

## Only `public`

works (??)

This is the first criteria to get it on the dropdown. Supposed we have 3 versions like this :

![](../../assets/cfc9efd8b8d66871.png)

Only `public`

works. There is no magic attribute like `[SerializeMethod]`

to paste to make it work with `internal`

. This is quite sad for C# freaks who like an extra tidy code.

![](../../assets/cb172727fec9a9eb.png)

Only the `public`

one appears...

### Can we hack it?

Where's the fun in playing fair, right? What if I just go ahead and edit the serialization like this. If you love serialization by name so much, then get wrecked.

![](../../assets/7a1b4d79749d6f51.png)

Turns out it works (lmao), but do you want to sacrifice usability in Unity editor just to call `internal`

or `private`

methods?

![](../../assets/427d1e34ef5db14b.png)

![](../../assets/9b0fcd4ebf7b3d81.png)

It even lights up in JetBrains Rider!

![](../../assets/fcc3906e85ea5587.png)

You can also "hack" in the editor by entering debug mode. To be honest the "debug" editor is kinda nice!

![](../../assets/31928392cec709a9.png)

I am designing **an Asset Store **package however, so it is unacceptable that user must hack like this in order to make my component compatible with `UnityEvent`

. I have no choice but to play with `public`

rule.

Other than that, you decide for yourself is the code hygiene of not using `public`

and still be able to call it from `UnityEvent`

important to you or not.

## Only 1 static argument allowed

![](../../assets/2a6e3d14fab2e96b.png)

![](../../assets/32f2a713ca1c90e5.png)

The static event can only call 1 argument methods. You can kinda confirm this by looking at the internal fields of event : the `arguments`

may have an `s`

, but it stands for holding 5 different type of arguments **in 1 argument**.

![](../../assets/739a85d4be8b3f4e.png)

## What if we have mismatched parameters than required

This event has 2 dynamic arguments `AudioClip`

**and **`float`

. I want to try targeting the one with only `AudioClip`

.

![](../../assets/ee6d6d26fa898e1f.png)

It **does not work**. Unity doesn't know how to ignore extra arguments.

What about less argument? Call this method but with the dynamic event with only one `AudioClip`

.

![](../../assets/e3d0177df01e7ad4.png)

![](../../assets/fa6b4fe1fc5e852c.png)

Nope, nothing appears. Just in case, the perfectly matched one of course works.

![](../../assets/42d581ebf535bf52.png)

### What about optional arguments?

![](../../assets/a4072b82ac235d7f.png)

![](../../assets/9b9e05c7116af3f6.png)

No! It is not that smart! You better think the optional argument as a real argument.

But this will place heavy restriction to package API design as well, as when you finally get a lot of smart optional arguments and overload resolution planned to work beautifully (e.g. just one `Play`

method name that works in many ways), then you want to make those compatible with `UnityEvent`

suddenly there is a wrench throw in.

A way to get out is to make a new entry point just for the `UnityEvent`

, but you have to invent a new name which may get ugly. (e.g. suspiciously wordy `PlayAudio`

in addition to `Play`

, just so `UnityEvent`

has something to connect to.) I do this in my package because it can't be helped.

### Can we hack it?

![](../../assets/c04efe64950dbef1.png)

It has just `AudioClip`

, but method name is edited to the one that also requires `float`

(or optional `float`

)

![](../../assets/dcfd2393fda970d9.png)

It does not work. (Entering Play Mode and invoke will not do anything when "Missing", no error also.)

## If there is a return value?

In my Asset Store package, I want the play to also return a value. This could be used to stop the already played audio.

![](../../assets/d2e12c072cf73156.png)

Unfortunately, having non `void`

return value disqualifies everything. Including the `public`

one.

![](../../assets/ce36d7b4936a7931.png)

Same as dynamic version :

![](../../assets/0e2231b0bc7c909f.png)

### Can we hack it?

Perform the same hack by directly edit the method name. Note that the argument is perfectly compatible, exactly 1 `AudioClip`

.

![](../../assets/860e067485c26348.png)

![](../../assets/4a5bbe56a479c831.png)

Whoops, I was caught this time!

Though, we now additionally know that it uses `System.Delegate.CreateDelegate`

underneath, which is standard C# rather than a Unity-thing. So if we know how that works, then we know what could and could not be hacked. It could be assumed now that Unity engine coded such that it binds to `void`

return value of the target class, but there is no criteria on access modifier so the hack was successful.

Interestingly [CreateDelegate](https://docs.microsoft.com/en-us/dotnet/api/system.delegate.createdelegate) overloads has `firstArgument`

criteria, so maybe this implies if we hack the 2nd argument it could get through. But I am too tired to try that now.

## No `interface`

arguments, but subclass OK

If you made your API to be nicely handling `interface`

of your custom class, then bad news the serializer don't know how to deal with it.

But subclass is OK! This allows the asset picker to pick **any subclass **from the base class specified in the method's signature. This allows you to use `abstract class`

as well. In this image, `AuditoPlayableBase`

is an `abstract class`

.

In this picture, that `public void`

is just a scapegoat for `UnityEvent`

targeting. It is using a `class`

not `interface`

so Unity know how to serialize the static argument. Moreover it has `void`

return and not `AuditoHandle`

I actually want to use.

![](../../assets/a4b2686a8916a115.png)

The object picker shows all the choices that subclassed from `AuditoPlayableBase`

that aren't `abstract`

anymore. This is a really nice developer experience for the user.

![](../../assets/32861bbdc108419f.png)

This leads to **weird** class tree design where an `abstract class`

is there just so Unity could know how to serialize, but the real deal is the `interface`

I want to use everywhere. The best solution maybe to hide the `interface`

behind `abstract class`

, and `abstract class`

may essentially do nothing because the `interface`

had already locked in everything. (lol)

![](../../assets/b1fbaf26fae1c5d6.png)

## Can call `static`


![](../../assets/8f9a33452592e788.png)

![](../../assets/f1ca869e75353995.png)

I found about this by mistake. Though it make sense that it should be able to, I didn't think Unity would actually let me to do this lol.

This is given all the previous criteria are passed, so must be returning `void`

. It can take arguments just fine, like discussed.

## Implications in API design

Because the target's name will be **forever **serialized in the client's code, you must make damn sure you don't refactor the name to something else. This already applies to all your `public`

code, but breaking people's serialized event target won't trigger compilation error. Scary stuff!

And you have to be more skillfully sidestep everything. Take a look at this :

![](../../assets/9e5abf883c5a3b72.png)

- The first requirement is that I want the
`static`

method`Play`

with complete overload + default argument, so I could type`NonpositionalAudio.Play`

to use it. It has return value too. - Then I want to make an instance
`public`

`Play`

method to service those that wants to use`UnityEvent`

. First I have to sacrifice return type, then also`interface`

is not usable. - Lastly there is one more
`Play`

overload I want to be able to use with events. But if that is named`Play`

, it will cause infinite recursion to itself instead of resolving to the`static`

method. Now I have to name it something else.

And this 5 `Play`

:

![](../../assets/c1eb79d485b5c21d.png)

Normally the bottom 2 are enough to handle everything I want, but if I want it to be compatible with events, I need 3 more above with no return value. Also I cannot just use default arguments, I need to explicitly add all the combinations. Of course I cannot use `interface`

too. Lastly, I can't name the top 3 `Play`

anymore as it would cause similar problem as before. So, I name them `PlayAudio`

instead.

(Other idea includes `PlayFromEvent`

, to explicitly excuse that there is no return value because it is "for event", but I think that is weirder.)