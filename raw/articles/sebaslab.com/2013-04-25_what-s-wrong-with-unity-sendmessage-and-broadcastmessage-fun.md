---
title: What's Wrong with Unity SendMessage and BroadcastMessage functions
url: https://www.sebaslab.com/whats-wrong-with-sendmessage-and-broadcastmessage-and-what-to-do-about-it/
author: Sebastiano Mandalà
published: '2013-04-25'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Unity 3D is a well designed tool, I can say that. It is clearly less painful to use than UDK, no matter what its limitations are. However, as I keep on saying, the c# framework is still full of bad design choices, probably unfortunate inheritances from unity script (why don’t they abolish it and just switch to c#?).

Emblematic example of these bad choices is the communication system built around *SendMessage* and *BroadcastMessage*. If you use them, you should just stop already!

In fact *SendMessage* and *BroadcastMessage* are so wrong mostly because they heavily rely on reflection to find the functions to call. This of course has a given impact on performance, but performance is not the issue here, the issue is instead related to the quality of the resulting code.

What can be so bad about it? First (and foremost) the use of a string to recognize a function is way worse than using a string to recognize an Event. Just think about it: what happens if someone in the team decides to refactor the code where the calling function is defined and decides to rename the function or delete it?

I tell you what happens: the compiler will not warn the poor programmer of the mistake is doing and even worse, the code will just run as nothing happened. When the error will be found, it could be already too late.

Even worse is the fact that the calling function can be declared as private since the system uses reflection. You know what I usually do when I find a private function that is not used inside the declaring class? I just delete it, because the code is telling me: this function cannot be used outside this class and I am not using it, so why keep useless code?

Ok, in c# I mostly use delegate events, so I have to be honest, I basically do not use *SendMessage*, but I still find the *BroadcastMessage* useful when it is time to implement GUI widget communication.

Since GUIs are usually implemented in hierarchical way (i.e. if you use NGUI), being able to push a message down into a hierarchy could have several advantages, since it is basically not needed to know the target of the message. This is actually similar to * Chain of Responsibility *pattern.

For this reason I decided to implement a little framework to send a message through a *GameObject* hierarchy and it works like this:

If the root (or a parent) of the target that must be reached is known, you can use it to send a signal through the hierarchy in a top down fashion. All the nodes of the hierarchy will be searched until a compatible “listener” is found. The code is pretty trivial and, as my usual, relies on implementation of interfaces.

*CubeAlone* is a *MonoBehaviour* that is present in a *GameObject* that is outside the hierarchy to search. It could have been inside as well, but I will reserve this case for the next example.

using UnityEngine; using Svelto.Communication.SignalChain; public class CubeAlone : MonoBehaviour { public Transform root; SignalChain _chain; void Awake() { _chain = new SignalChain(root); } void OnMouseDown() { _chain.Broadcast("event"); _chain.Broadcast(new BetterEvent(Color.green)); } }

Through the *SignalChain* object two events are sent to two different targets. I decided to do so to show you the flexibility of the interface. In fact it is possible to identify events using whatever kind of object, from a string to a more complicated type that could hold parameters.

In the hierarchy of the example that can be found at this address[ https://github.com/sebas77/SignalChain](https://github.com/sebas77/SignalChain) there are two targets listening the *CubeAlone*, these are the *Sphere* and the *Cylinder*.

In order to be recognized as listener, these two *MonoBehaviour* must implement a *IChainListener* interface:

public class Sphere : MonoBehaviour, IChainListener { public void Listen(T message) { if (message is BetterEvent) { this.transform.renderer.material.color = (message as BetterEvent).color; } } }

public class Cylinder : MonoBehaviour, IChainListener { public void Listen(T message) { if (message is string && (message as string) == "event") { this.transform.renderer.material.color = Color.red; } } }

and from the code it is pretty clear how it works. Should I add something? If leftmost cube is clicked, the Sphere and the Cylinder will change color.

Well, let’s see now the case when the dispatching event object is already in the hierarchy. In this case we could dispatch events in the hierarchy without knowing the root. However the root must be signed with *IChainRoot* interface:

using UnityEngine; using Svelto.Communication.SignalChain; public class Cube : MonoBehaviour, IChainRoot { }

and the dispatching event object can use the *BubbleSignal* object in this way:

using UnityEngine; using Svelto.Communication.SignalChain; public class Capsule : MonoBehaviour { BubbleSignal _bubbleSignal; void Awake() { _bubbleSignal = new BubbleSignal(this.transform); } void OnMouseDown() { _bubbleSignal.Dispatch(new BetterEvent(Color.blue)); } }

Try to click on the capsule now, the sphere will change again color but this time will be blue!

Very nice!

Maybe you should save a local variable when you do “_root.GetComponentsInChildren” inside a foreach loop.

I’m not sure on this, but I think that for each compoment he finds, he keeps running the GetComponentsInChildren multiple times?

I hope you are wrong, but for safety I will put it out. Thank you for the feedback.

Very nice system. Wondering if its possible to add the listeners as components to the gameObject instead of making the monobehaviour inherit from and interface. The reason is that I would like to dynamically add and remove listeners to gameobjects.

Cheers.