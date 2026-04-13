---
title: Refactoring with components
url: https://etodd.io/2011/02/02/refactoring-with-components/
published: '2011-02-02'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Refactoring with components

**Update:** check [this article](https://etodd.io/2011/06/27/component-binding-behind-the-scenes/) for more in-depth details on Component Binding!

I've been refactoring my engine with the [component-entity model](http://bit.ly/dZveEa), and things are turning out quite nicely. The one problem I always had with components was the way inter-component dependencies were handled. In the article I linked (one of the classics on the subject), the author says his components originally referenced each other through a component manager, but eventually they allowed components to store pointers to each other for performance reasons. In my mind, that's way too many concrete dependencies.

So I'm rolling my own data binding system. Instead of directly accessing a component's data from another component, I'm having both components store a copy of the properties they need. So if the physics component wants to overwrite the position and orientation of the model component, I don't have to do this inside the physics component:

`this.ModelComponentReference.WorldTransform = blah;`


Instead, the physics component and model component have separate transforms. These act like input/output ports for each component. When constructing an entity, I bind the two "ports" together. I can also use multiple inputs for one output by combining them together with a transformation function. I can also bind actions (which is basically like event handling).

Here's a good example of the power of this system. Let's say I have a working player entity, and I want to have it play footstep sounds when he's walking. I already have a PositionComponent and a PlayerStateComponent (with an enum of states like Idle, Running, Jumping...).

Let's create a TimerComponent that has a few properties like Enabled, Interval, and Repeats, and an action (or event) that fires when the timer expires. First we would set a proper interval and enable repeating. Then we could create a binding for the Enabled state, which would set Enabled to true whenever the player's state is "Running". In my implementation, this is accomplished with a closure.

Then we can create a SoundComponent that's set up with our footstep sounds, and whose 3D position is bound to our player's position. We could then bind the TimerComponent's firing event to the SoundComponent's "Play" method. Mission accomplished.

Bear in mind that this system is still untested and I'm still in the middle of refactoring, but so far it's looking good. Here's a screenshot of my player factory code to give you an idea of how I'm doing this:

So there you go. It's not perfect, but I think it's going to work. The idea, at least, is sound. I'll post later about the details of my binding system, which is still a matter of some contention. I'm trying to keep things clean while avoiding reflection at all costs.