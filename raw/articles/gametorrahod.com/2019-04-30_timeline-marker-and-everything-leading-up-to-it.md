---
title: Timeline marker and everything leading up to it
url: https://gametorrahod.com/timeline-marker-and-everything-leading-up-to-it/
author: Sirawat Pitaksarit
published: '2019-04-30'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/54ef78e63c24ca56.png)

New in Unity 2019.1, you can now create a duration-less object on the timeline, **the marker.** Currently the official documentation is still not up, but this 2 forum posts could kickstart you what it is.

If you are confused by "marker" or "signal" feature (not the same thing), here's the technology stack involved from bottom to top :

`UnityEngine.Playables`

: playable graph, playable, playable asset, playable director`UnityEngine.Timeline`

: track, clips, timeline asset`UnityEngine.Playables`

(new in 2019.1) : notification, notification receivers`UnityEngine.Timeline`

(new in 2019.1) : markers, marker track`UnityEngine.Timeline`

(new in 2019.1) : signals

In this article we will learn everything **bottom up, **starting from the new backbone added to `UnityEngine.Playables`

that enabled the marker implementation in `UnityEngine.Timeline`

. Not just that, I will rewind back to the very root. What is a playable? Why is that a graph?

## What is a "playable"

This is one of the most difficult and beginner unfriendly API to learn in my opinion given how abstract it is. ("Timeline" is the beginner friendly abstraction over this, but it helps to understand playables.)

Moreover a "graph" (`PlayableGraph`

) seems not like a thing that could **be played** at all. ([https://docs.unity3d.com/Manual/Playables-Graph.html](https://docs.unity3d.com/Manual/Playables-Graph.html))

The characteristic of things that you could "play" :

- You can order it to play, stop, pause, resume. It is said to be in one of these states. (Resume is not a state however, used to enter play from pause)
- It has a built-in time.
- That time moves or not depending on its state.
- Based on this time it do something.
- Based on that do something, the output state is now at something.

How a graph come into play in all this? Why we not just call em "a playable" but instead, "a playable graph"? Imagine a record player. This is definitely **a playable **thing (literally, and also correctly in Unity's term).

[Wei-Cheng Wu](https://unsplash.com/@spencerwuwu?utm_source=ghost&utm_medium=referral&utm_campaign=api-credit)/

[Unsplash](https://unsplash.com/?utm_source=ghost&utm_medium=referral&utm_campaign=api-credit)

But also, this thing **is a graph** (that could be played). Graph is made from interconnecting nodes, in this case, interconnecting `Playable`

(that's the actual class name). Many things inside a record player (playables) do connect to make the whole thing (graph) work.

## PlayableGraph

There is no `new`

to call, you instead do `static`

call `PlayableGraph.Create()`

and you will get one which you could `.Play()`

. It does nothing however! Until you add some `Playable`

to the graph. There is no `.Add(playable)`

to call either, you will learn how in a bit.

There are several mode of increasing its time it could use : [https://docs.unity3d.com/ScriptReference/Playables.PlayableGraph.SetTimeUpdateMode.html](https://docs.unity3d.com/ScriptReference/Playables.PlayableGraph.SetTimeUpdateMode.html)

### Important

`PlayableGraph`

is playable (adjective), but **not **a `Playable`

(the class name). ...yeah it even has `.Play()`

if that confuse you further, but `Playable`

as in the class name, means things that are inside the graph that do things, and make output become something while the graph is playing/evaluating.

## ScriptPlayable : Playable

But just `Playable`

is boring, it couldn't do anything. Each playable node should has its own behaviour as the time goes on. To create a **playable that behave **we need a `ScriptPlayable`

, defining how it behave.

Creating this is easy, with `static`

method `ScriptPlayable<T>.Create(graphThatItShouldGoTo)`

. (Unintuitively, you don't do something like : `graph.Add(new ScriptPlayable<T>())`

)

How to define **the behaviour **of the created playable? The secret is in that `T`

generic, which is should be of type `PlayableBehaviour`

. You could imagine it will be able to use your `T`

to create "a piece of logic" embeded in your `ScriptPlayable`

without you having to mess with any `delegate`

to send a method in. Sure enough, `PlayableBehaviour`

is an `abstract`

class that ask you to provide the required logic.

Back to the record player analogy, it must contain tons of `ScriptPlayable`

:

- The first node is the disc providing you data.
- The needle node connects to the record, picking up vibration.
- Imagine graph's time (playable graph has a time) as the position of this needle.
- The vibration is sent through metal strip node.
- The metal strip is connected to amplifier node to change little vibrations to music.
- The amplifier is connected to the speaker.
- Maybe you could even think the speaker is also connected to "air" node, before connecting to your ear.
- Your ear is a
[playable output node](https://docs.unity3d.com/ScriptReference/Playables.IPlayableOutput.html).

If you change the needle's position, you are going to receive a certain kind of output (music) if it is in a playing state. Playing is just a loop of change time -> evaluate. You could also just evaluate the graph while in stopped state. Your choice.

### Creating that record player

In simplified steps :

`PlayableGraph.Create`

: You get a thing that could "play" (`.Play()`

), but there is nothing in it yet. You get back a`graph`

.`???Playable*Output?*.Create(graph)`

: Use`Create`

static method to put things in the graph. You do get back that`playable`

, but that`playable`

is already in a`graph`

.- Connect playables up while they are already inside the graph : the returned
`playable`

from`Create`

would have something to do this. For example`PlayableOutput`

gain[these methods](https://docs.unity3d.com/ScriptReference/Playables.PlayableOutputExtensions.html). The`PlayableGraph`

itself contains something like[Connect](https://docs.unity3d.com/ScriptReference/Playables.PlayableGraph.Connect.html)[among other things](https://docs.unity3d.com/ScriptReference/Playables.PlayableGraph.html). - Graph could branch! From my description you may think things are just connected in a linear fashion. How about having multiple speakers using the same needle's vibration? This is why it's "playable graph" not "playable list".

This is a quite nice recap once you know all the terms so far : [https://docs.unity3d.com/ScriptReference/Playables.Playable.html](https://docs.unity3d.com/ScriptReference/Playables.Playable.html)

Looking at `Connect`

's API, you can see that it will get pretty difficult to "imagine" a graph from these "ports". You must ensure something is leading up to the output at least too. You want some sort of GUI to work with this. But before that, needed for the GUI is the ability to "save"...

## PlayableAsset

You might be thinking about storing some kind of "preset" and have that create a `Playable`

for you. Storing things in Unity should be via a `ScriptableObject`

.

Luckily `PlayableAsset`

is exactly what you want and it inherits from `ScriptableObject`

too. Instead of `static`

`Create`

you would have to use when crafting out the playable manually from the playable class, now you can use **instance method **from this loaded asset : `playableAsset.CreatePlayable(graph, gameObject)`

so that it use information serialized **in the asset** to create a part of graph. Note that inside the `CreatePlayable`

method, you likely have to use `Create`

`static`

method anyways. But having settings saved is better than pure scripting.

## PlayableDirector

With the `PlayableAsset`

technology you could have an asset ready to become a graph at any time. In Unity when you have an asset it means you could drag and drop it. (And increasingly Unity is heading towards this "asset" workflow on many packages)

Without `PlayableDirector`

, these are total steps of making use of the `PlayableAsset`

:

- Get the asset in the script. Maybe you use an exposed field because you know
`ScriptableObject`

do show up in editor, or you could use`Resources.Load`

or Addressable Asset System. - Create a playable graph for it :
`PlayableGraph.Create`

- Create a playable from that asset and put it in the graph :
`asset.CreatePlayable(graph)`

- Connect ports and outputs.

There is already drag and drop in the 1st step, but it would be nice if you could drop the asset somewhere and that thing do all 4 steps for you. `PlayableDirector`

is that.

![](../../assets/dec34bb9447145f5.png)

`PlayableDirector`

is commonly thought as "the timeline player", but because you already learn things from bottom-up, we are not even arriving at the Timeline yet. Also notice the top field did not say anything related to "timeline" in general but just "Playable (asset)".

What it want is **any **`PlayableAsset`

. It creates an empty playable graph and put that playable resulting from the asset to the graph. It doesn't even hand you back the graph (though [you could get it](https://docs.unity3d.com/ScriptReference/Playables.PlayableDirector-playableGraph.html)) but has its own `Play()`

, `Stop()`

and the like. (Which I guess will be forwarded to playable graph's own `Play()`

anyways)

It just happen that the most common kind of `PlayableAsset`

you give the director is a serialized timeline asset called `TimelineAsset`

(more on this in a moment), and its `CreatePlayable`

returns you a big-ass stack of playable representing the whole timeline.

### Bindings

The 5th important step that a `PlayableDirector`

could do : the bindings. The assets in Unity are stored in the asset **folder**. They have no knowledge of things in the scene! But this `PlayableDirector`

is a `MonoBehaviour`

, it **could **know something in the scene.

Then we can finally bridge asset workflow with the scene workflow, how about we remember scene-things on the `PlayableDirector`

along with where it should went to when the asset became a playable graph at runtime. When `PlayableDirector`

made a graph, it could additionally "inject" some references from the scene along the way.

By this, bindings are not possible to set in the Timeline GUI without `PlayableDirector`

, as it is **not **really a timeline's feature. You can think the bindings you can set in the Timeline GUI tab doesn't really modify the timeline **asset** but modifying the `PlayableDirector`

**component**'s data. Here is an image showing `PlayableDirector`

holding the bindings, **not the **`TimelineAsset`

. (Which it is also holding, preparing to turn it into the real `Playable`

to uh... play)

![](../../assets/ca52de42ec174465.png)

## Timeline

What you **really want** to do is drag and drop things in GUI at design time, preview it along the way, save that thing in the project, then play it when you want, and have something in the scene changes according to that.

Timeline feature is this. It consist of a dedicated Timeline tab and a new `PlayableAsset`

called `TimelineAsset`

which is used together with already explained `PlayableDirector`

. (The director is actually **not **a part of timeline feature, but it has been popular for processing just the `TimelineAsset`

because that's what Unity promotes.)

It has a time, could be played, stopped, pause, resume, and also things in the scene will be at a certain state depending on timeline's evaluated value. Unity's Timeline (when running) is a playable graph. When not running, the whole thing could be saved in the project thanks to `PlayableAsset`

. And a nice GUI could edit this asset while in it's non-graph state.

Moreover you even could say what happen **when **by dragging and stretching those clips with begin and end point on the timeline. I know it may not sound impressive, but if you think about the playable API I explained earlier in record player analogy, where everything do things all the time based on current time, this is a really great feature to have. The "clip" just happen to have begin and end point, which it could "if" if it should do something or not. Or even blends with other clips when they overlaps.

`UnityEngine.Timeline`

's source is visible, unlike `UnityEngine.Playables`

.

Let's look at this feature with rose-colored glasses : [https://unity3d.com/unity/features/editor/art-and-design/timeline](https://unity3d.com/unity/features/editor/art-and-design/timeline)

Now what it actually is in terms of everything you learned so far :

- The timeline you see in the Timeline tab is showing data from your
`TimelineAsset`

serialized in the project, which is a`PlayableAsset`

. You can now "design" this asset at edit time easily, so it could become sophisicated playable graph at runtime. - All the clips in the timeline are
**also**`PlayableAsset`

. Luckily there is no class called`ClipAsset`

this time. (But you could add`ITimelineClipAsset`

to customize how it behave) And clips are not actually lying around in your project (that would be troublesome) but instead, they are in a track. - Each track that house the clips are
**also**`PlayableAsset`

, of type`TrackAsset`

. Clips will be somehow serialized together in this`TrackAsset`

. You could use`[TrackClipType]`

attribute to control what kind of clips could be on the track. A track could have an output if you want via`[TrackBindingType]`

attribute, which works together with`PlayableDirector`

's binding feature. Entering`GameObject`

type for the binding is possible. Track asset are not in your project either, everything are packed nicely in 1`TimelineAsset`

. Now you see that single`TimelineAsset`

encompassed everything. - On edit time, hand the
`TimelineAsset`

to`PlayableDirector`

, so it could manage the created graph and do bindings at run time. Also it could preview in edit time! I once thought the`PlayableDirector`

must have a big brain but actually most of the brain are in`TimelineAsset`

's`CreatePlayable`

and the`Playables`

API itself that plays the created graph.

### Track's "binding slot" is just an illusion

For example this Animation Track with `Animator`

binding, you see a slot right there. But that slot is not something on the track but just the editor helping you out, so you don't have to go to the `PlayableDirector`

to see which binding corresponds to this track.

Remember again, `PlayableDirector`

holds the power of bindings, **not the track**. Because `PlayableDirector`

is on the scene, and it binds to things in that scene. Track asset is not on the scene, it is in your project folder.

![](../../assets/763883ed2530d0e9.png)

Dispel the illusion by instead of inspecting the `PlayableDirector`

(in the scene) with the `TimelineAsset`

, click on the `TimelineAsset`

in your Project tab directly. The slot disappears! Thanks to bottom-up learning, you know this make perfect sense.

![](../../assets/552a7845cbd5328f.png)

And it now also make sense that you use the same `TimelineAsset`

on 2 different `PlayableDirector`

and it could results in a different bindings.

*It is possible to **ask **`PlayableDirector`

what the binding for a particular track is, because those "Bindings" list are like dictionary. The key is? You guessed it, `TrackAsset`

object. With this `pd.GetGenericBinding(myTrackAsset)`

you could get the correct binding.

For example you are writing a custom inspector for a `TrackAsset`

and want to draw something based on the bound object. You could get the currently inspected director with the helper `static`

property `TimelineEditor.inspectedDirector`

, then throw itself into `GetGenericBinding(this)`

to get the bound object.

## What people want next : "event system"

When time **passed **a certain point in the timeline, you want something to happen **once**.

It might sounded stupid that the Timeline feature in Unity could not do this from the Timeline's release, until you understand how it was made (playables) then you realize "triggering" was not in the playable's concept until now.

Playable just evaluate its current time and change the output accordingly. There is no concept of something that "passed" a certain point. There is just : "it is at this point, the output then should be like this" (evaluation).

Something like this must be 1 level of abstraction over the base system. And sure enough the **marker **system is implemented on the `UnityEngine.Timeline`

namespace. However before 2019.1, we are missing some crucial backbones in `UnityEngine.Playables`

to make this work.

Imagine the same record player, that could eject disc on its own if the needle **passed through **a special kind of grooves on the disc that encoded "the end of disc". That would be an equivalent of this event system and would be very smart for an analog machine that usually just represent what state it is right now. This event mechanism "smells" like "state", commonly seen in digital things more than analog. Or imagine an analog chainsaw which is also a playable because you could "play" to make the blade spin. What if it could stop automatically after spinning for certain rounds? We would need the blade to "notify" the engine to stop somehow after **passing though** a certain time or condition.

## New Playables API : Notification

Drop the "event" wording for now. In the `Playables`

API we now have notifications.

### Output could now be added with multiple INotificationReceiver

A notification came from anywhere in the graph, the output of this graph will notify all of its notification receivers. You could imagine the receivers are sitting even "outer" than the output, on the outmost edge of the graph.

The receiver `INotificationReceiver`

will be called :

`OnNotify(Playable origin, INotification notification, object context)`


These are 3 extension methods on playable output to add/get/remove notification receiver, but the source is closed.

### How to notify those receivers : PushNotification on the output

You might be getting excited how we could notify those receivers. When will the "time" come into play so we could finally run through that point of time and fire up the notification.

But! It is just a method call called `PushNotification`

. On this call, you could send any `INotification`

(along with `context`

of type `object`

even!) to all the receivers. The end!

The "passing certain time and fire event" thing must then be a work of `Timeline`

namespace, that ultimately use `PushNotification`

on **some criteria**. Because `Timeline`

's source code is visible, let's dig right in.

## Timeline utilizing Playables's notification API : Marker, IMarker

`Marker`

is not a `PlayableAsset`

, but it **is **a `ScriptableObject`

like `PlayableAsset`

because it needs to be saved in the timeline asset.

`Marker`

is also an `IMarker`

, which specify it must have a track parent and a single `time`

. (Not `duration`

)

This is not surprising. The definition of `PlayableAsset`

is that it could be turned into a playable to live inside a playable graph. A marker is a new kind of serialized object (saved along with the `TimelineAsset`

) which even though got converted together along with the timeline, tracks, clips (who turned into big playables), it became "something" designed to **be passed through.** It is only a point in time. It works together with tracks because markers live on the track, but it is not considered a playable at runtime like what you could get from tracks or clips.

You could create your own `Marker`

by subclassing it. You can then already create and place the marker that do nothing. You could query for them on the timeline **asset**, they are just not ended up useful in the created playable graph by `PlayableDirector`

.

But one secret, if you add `INotification`

(and maybe `INotificationOptionProvider`

) to your `Marker`

subclass too, a runing timeline (a playable graph created from `TimelineAsset`

) knows how to `PushNotification`

to the receivers when the play head **run through** them!!

### IMarker knows its own track

This `interface`

has `TrackAsset parent`

. This suggest that by definition the marker couldn't float on its own in the timeline (that would be weird lol)

So, combined with the fact that the bound object is not actually the thing on the track but on `PlayableDirector`

, if you are going to draw a custom inspector for the marker and want to know the bound object on its `parent`

track, together with `TimelineEditor.inspectedDirector`

you could get to the bound object with `parent`

as a key for `GetGenericBinding`

on the `PlayableDirector`

.

![](../../assets/7a80ee4520924629.png)

![](../../assets/6f54a429d0a33846.png)

## TimeNotificationBehaviour

This is no magic, it is just a **new kind of **`ScriptPlayable`

from a new built-in `PlayableBehaviour`

called `TimeNotificationBehaviour`

put in your resulting graph automatically if there is any marker on the `TimelineAsset`

. Sure enough if you search the source code of `TimeNotificationBehaviour.cs`

, you will find `PushNotification`

in there.

`PushNotification`

require `INotification`

, that means the running timeline graph will throw **the marker itself** as a notification to all receivers. (The free `object`

argument `context`

is always `null`

however when timeline is doing it.)

### When will it push?

There is something called `PrepareFrame`

in all `PlayableBehaviour`

. It remembers the previous time the playable was, then differentiate with the current time, then push ALL markers in this range, inclusive. In effect I observed these behaviour :

- If the game lags and time skips ahead a lot, all markers are guaranteed to be pushed
**simultaneously**on this frame. It works even if the lag results in a new loop. - If you somehow manages to pause the play head at
**exactly**where the marker is after playing normally, the marker will be pushed before the pause because the time range is inclusive. When you resume from the pause, that same marker**will be pushed again**because the time range is inclusive. This is evidenced in the`TimeNotificationBehaviour.cs`

source code :

```
if (notificationTime < start || notificationTime > end)
continue;
if (e.triggerInEditor || playMode)
{
Trigger_internal(playable, info.output, ref e);
m_Notifications[i] = e;
}
```


### What did it push?

We will look at this `INotificationReceiver`

interface again :

`OnNotify(Playable origin, INotification notification, object context)`


`Playable origin`

: this is the playable in the playable graph generated from`TimelineAsset`

. With`.GetPlayableType()`

, it is revealed that this is`TimeNotificationBehaviour`

.

It is possible to`.GetTime()`

and`.GetDuration()`

to get an equivalent of`playableDirector.time`

and`playableDirector.duration`

. It is just an "at root" playable API rather than ask the director to ask its created graph's root playable.`INotification notification`

: this is your triggered marker, which you added`INotification`

to it. You can cast to either your marker type, to`Marker`

, or to`IMarker`

.`object context`

: this is`null`

.

## New track type : MarkerTrack

![](../../assets/9a0ac138710bfce9.png)

You notice a **smaller track** named "Markers" on every timeline asset in 2019.1. This is a new built-in `markerTrack`

property on every `TimelineAsset`

.

Also it is possible to create your own this smaller track by instead of inheriting from `TrackAsset`

, inherit from `MarkerTrack`

instead. You will then get a smaller drawer, also it will not allow any clips on it.

On contrary, the marker could be on **any **track, even overlapping with the clip. As far as I know you cannot lock a certain type of `Marker`

on a certain type of `MarkerTrack`

. Unity also made one `MarkerTrack`

called `SignalTrack`

. More on this at the end.

I created a single custom `Marker`

called `TimeCueMarker`

which you see scatterred around, and a custom `MarkerTrack`

colored purple with output locked to `TimeCueReceiver`

. You see even on Unity's `SignalTrack`

, I could still put my own kind of marker (other than `SignalEmitter`

marker that supposed to go there) on it.

You could guess what I am going for on that purple track. I am making a plugin called **Time Cue**, which provide new markers that affect the `TimelineAsset`

's playable graph's playback like jump from cue to cue, or execute conditional pause/resume when it reaches a certain cue. This graph control will be via the special `INotificationReceiver`

called `TimeCueReceiver`

, that knows the `PlayableDirector`

that creates the graph that is sending this notification in the first place, and could manipulate the graph also using that `PlayableDirector`

. (Infinite loop incoming!)

## Who's the receiver?

![](../../assets/f4eaaced674fa639.png)

When `PlayableDirector`

turned (2019.1) timeline asset into a graph, now it will take time to set up `AddNotificationReceiver`

too so they receive an `INotification`

from markers.

- If that track is the special "Marker" track (reveal with the pin button)
**it first find a GameObject**that has`PlayableDirector`

that is governing the playable graph generated from this`TimelineAsset`

. (red arrows) - If that track has an output binding,
**it first find a GameObject**that has that output component. (red arrows) - The
`GameObject`

is then**search for ALL of its components**for anything with`INotificationReceiver`

to add as a**receiver.**(yellow arrows)

Imagine `MyScript`

you see on the Inspector which is a `: MonoBehaviour, INotificationReceiver`

as this :

```
public class MyScript : MonoBehaviour, INotificationReceiver
{
public void OnNotify(Playable origin, INotification notification, object context)
{
Debug.Log($"JAM JAM REGGAE {notification}");
}
}
```


It could receive `OnNotify`

from the special Marker track** and also** from the orange audio track** **as well even though you don't see any connection of audio track to this script at glance. Because it goes from component to `GameObject`

first, then broadcast the notification back down to every components. (You could also lock the track to bind to `GameObject`

to remove the component -> `GameObject`

step)

Look at control track and playable track, because those track don't have any bindings markers on them are useless.

As you could imagine the receiver could receive all sorts of markers given how lenient it is and how the marker could even stay anywhere. But on your `INotificationReceiver`

's `OnNotify(Playable origin, INotification notification, object context)`

, you can still do something like `if( notification is TimeCueMarker)`

for example to look for the **type **of marker you want.

## Receiver's problem

The `INotificationReceiver`

's callback being of signature `OnNotify(Playable origin, INotification notification, object context)`

left you wondering this : "Where the heck in the timeline is this `notification`

?" Sure you could check for **type **with `is`

, but you want to know a specific one. Maybe you want to do something specific if the incoming marker is *that one*.

Remember that your `Marker`

is **both **`INotification`

and `IMarker`

. You can cast the `INotification`

back to your marker subclass at the same time as `if`

check like : `if(notification is TimeCueMarker tcm)`

(that's C# 6.0 feature) then thanks to `IMarker`

, you could get a time position or even its `name`

you name the marker in the Timeline GUI.

Now you could `if`

on the `name`

or the `time`

. Or even `.parent`

to access its owning track to do something specific on receiving a specific marker.

## Finally : SignalEmitter, SignalReceiver, SignalAsset

Instead of your own custom type of marker, a new built-in `SignalEmitter`

is a `Marker`

that could be **tagged** with `SignalAsset`

. (Just a dumb `ScriptableObject`

you could create)

And then in the `SignalReceiver`

which is an `INotificationReceiver`

, instead of `if`

ing on the `name`

or `time`

, it could check if the `SignalAsset`

is the one you are looking for or not for you.

Why **check for asset **instead of `==`

to a `string`

? It sounds very redundant...

- Drag and drop support and better editor support when it could query assets for you to select.
`string`

could be the same, assets are ensured by Unity to have unique GUID.`string`

are hard to rename, it disconnects everywhere if you do so. Renaming an asset will keep the GUID as long as you do it inside Unity that it could also migrate the`.meta`

file.- Asset are version controlled.
- One team member (designer) could create an asset, push it for the programmer, and the designer can continue using that asset independently without talking to the programmer ever again.
- You gain automatic support from everything related to asset. For example Addressable Asset System. You can make a DLC which use the same marker as your main game, without having the marker in the DLC package because it remembers only the GUID of the asset.
- If you are thinking you now need hundreds of signal assets, calm down. For example most of my game only use a signal asset named "SequenceFinished" and "DelayEnded". You could name it generically and reuse them. It's not like the notification will be broadcast to the world and cause conflict.

Now that's short thanks to bottom-up learning. Time to say good bye to those `yield return new WaitForSeconds`

in your script. Have a nice day!