---
title: How to make a custom signal receiver with emitter parameter
url: https://gametorrahod.com/how-to-make-a-custom-signal-receiver-with-emitter-parameter/
author: Sirawat Pitaksarit
published: '2019-04-30'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

This is a regular `SignalReceiver`

:

![](../../assets/3003255acda299f9.png)

You could see a problem, I need to make as many signals as the parameter I want to call my method. I want the `int`

parameter to stick together with the emitter that also holds the `SignalAsset`

, and call this `SignalReceived`

method with that parameter.

## Dynamic UnityEvent : UnityEvent<T>

Unfortunately `SignalReceiver`

is pairs of `SignalAsset`

-> `UnityEvent`

mapping. `UnityEvent`

could only be invoked parameterless or with parameter stated in the Inspector box. (**not dynamic**, cannot change at runtime)

This call for a custom `SignalReceiver`

that uses `UnityEvent<T>`

instead. You can see what it looks like by trying the component `EventTrigger`

of uGUI, where it has `UnityEvent<BaseEventData>`

. For example, in `MyScript`

, I have defined :

```
public void ParameterMatches(BaseEventData bed) { }
```


So it will show up on the "Dynamic" category at top.

![](../../assets/617e350df0c2e00d.png)

When selected, there is no box below to enter any `BaseEventData`

value. Indicating that it is "dynamic" based on the caller.

![](../../assets/211ddaf4f54f49dd.png)

However we could not just declare `public UnityEvent<BaseEventData> ue;`

and make that inspector appear, since Unity serialization didn't play well with generic. Instead, one nested level of generic will work :

```
public Why events;
[Serializable]
public class Why : UnityEvent<BaseEventData> { }
```


For simplicity I want to send a `bool`

with the emitter, to a dynamic `UnityEvent<bool>`

.

## Custom SignalEmitter

Make a new file `SignalEmitterWithBool.cs`

with this :

```
public class SignalEmitterWithBool : SignalEmitter
{
public bool parameter;
}
```


You will notice that it is already working on Timeline GUI.

![](../../assets/783ab7831deb2bb2.png)

The option "From Signal Asset" also appears automatically. It knows how to drill down and find your first `SignalAsset`

field and assign that. It should go to the same place as regular `SignalEmitter`

.

To make things "smarter" you may do this, so you could make more emitters with other parameter type.

```
//Put this in its own file
public class SignalEmitterWithBool : ParameterizedEmitter<bool> { }
//Put this in its own file
public class SignalEmitterWithInt : ParameterizedEmitter<int> { }
public class ParameterizedEmitter<T> : SignalEmitter
{
public T parameter;
}
```


Here's what it looks like. The drawer draws my own `parameter`

field before drawing remaining `SignalEmitter`

fields. I have successfully parameterized the emitter with one custom `bool`

.

![](../../assets/5d01ca153b00d901.png)

## Custom SignalReceiver

This is a barebone `SignalReceiver`

that looks for only `ParameterizedEmitter<bool>`

notification from the bool emitter, and then match the `SignalAsset`

to the all pairs, then invoke each one's dynamic event.

Unfortunately the nice editor for `SignalReceiver`

is `internal`

and we could not use it on our own custom receiver. I decided to not subclass from `SignalReceiver`

and create from scratch, and live with uglier inspector.

```
public class SignalReceiverWithBool : MonoBehaviour, INotificationReceiver
{
public SignalAssetEventPair[] signalAssetEventPairs;
[Serializable]
public class SignalAssetEventPair
{
public SignalAsset signalAsset;
public ParameterizedEvent events;
[Serializable]
public class ParameterizedEvent : UnityEvent<bool> { }
}
public void OnNotify(Playable origin, INotification notification, object context)
{
if(notification is ParameterizedEmitter<bool> boolEmitter)
{
var matches = signalAssetEventPairs.Where(x => ReferenceEquals(x.signalAsset, boolEmitter.asset));
foreach (var m in matches)
{
m.events.Invoke(boolEmitter.parameter);
}
}
}
}
```


The `bool`

you see in this source code cannot be replaced with generic `T`

.

This is an uglier `SignalAsset`

-> `UnityEvent<bool>`

I was talking about. But at least it works.

![](../../assets/dff4378f70982f90.png)

Notice the `UnityEvent<bool>`

dropdown could successfully select `AudioSource`

's `loop`

property, and the same with any of your methods that with 1 `bool`

argument.

When the timeline run through my custom marker with `parameter`

set to `true`

, I could see `AudioSource`

's `loop`

goes from unchecked to checked.