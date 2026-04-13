---
title: A Different Entity Component System
url: https://dewitters.com/a-different-entity-component-system/
published: '2015-08-02'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

When programming [Rabbit Wars](http://www.aimproductions.be/rabbit_wars/downloadPromotion/rabbitWarsPromotion.php) back in 2007, I ended up with huge objects for each of my game entities. They handled player input, AI, moving, shooting, health points and rendering. I didn’t like it, it drove me mad. But then I came across this [Evolve Your Hierarchy](http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/) article. Since I was still in the middle of programming, I refactored my game entity code to use components instead of multiple inheritance (just like the article described). It worked great, my code was readable again.

![](../../assets/80a579a7d6af5044.jpg)

Rabbit Wars for PocketPC


But now I’m writing [RPG Playground](http://rpgplayground.com), a game editor. And because it’s a game editor and not a game, I really need to take care of making my entities and components generic.

The thing is, when I look at the current state of [Entity Component Systems](https://en.wikipedia.org/wiki/Entity_component_system) (also called ECS) and my own game architecture, they seem to have diverged. I’m more of a high-level, top-down kind of guy, and not so much into low-level, bottom-up reasoning. So I don’t really care how data is organized in memory, or getting the last bit of performance out of C or C++ code. And while the current Entity Component Systems seem to lean towards a more technical solution, my system is more conceptual. It might not be as optimized, but in my opinion doesn’t break Object Oriented Programming, and better supports reusing existing game libraries.

You can find a good explanation of the current state of Entity Component Systems at Richard Lord’s [What is an entity system framework](http://www.richardlord.net/blog/what-is-an-entity-framework). So go and read that first (yes, it’s long). Don’t worry, this page will still be here when you finish that article… I’ll wait… . The next few paragraphs will refer to that article.

So, the problem we want to solve is basically the same: First the huge game loop. I actually solved this without using components, but then you end up with multiple inheritance and huge entity classes, which is also not exactly what you want. So both of our solutions use entities that are composed out of components, entities that are just containers for components. But the difference lies in components themselves.

When Richard splits the components into view, position, rotation, velocity and angular velocity, that’s already one step too far for me. And it’s probably at this point where our architectures start to divert.

When I was thinking about the different components, I ended up with 3 functional types of components. The first one is pretty obvious. Games are tiny simulated worlds, so game items have a position, velocity, etc. I call all items inside this simulated world ‘models’. They all adhere to the rules of the game world. But it won’t be much of a game if they weren’t displayed onto the screen. So a game entity also contains rendering functionality, for which I call the component that handles it ‘view’. And you can probably also guess the last type: ‘controller’. This is player input and AI that influences certain models inside the game world. Yes, you end up with model-view-controller components (like described in my blog post explaining [MVC game engine architecture](http://www.koonsolo.com/news/model-view-controller-for-games/)).

And you know what else I find weird about putting position, velocity and angular velocity in different components? Because there are tons of great physics engines out there which already handle this functionality. I don’t have (or event want) to keep track of all these properties individually. My ‘model’ component contains a physics bodies, which is registered to the physics engine. I don’t handle it myself, I outsource it.

So how does the view component know about the position of game items? Well, that part I also find strange about current entity component systems. In that system, components ‘share’ properties. Since components don’t know about each other, they share the same properties. They actually see this as an advantage that components don’t know about each other, but in my opinion, it breaks logical reasoning. It seems obvious to me that a view knows about the model to be able to render itself onto the screen. And that a controller knows about the model that it manipulates.

So instead of sharing properties (which from an OOP standpoint might also raise some eyebrows), I want to encapsulate certain properties inside the model component (which are further encapsulated by the physics library), and the view uses the model component to get the relevant info.

And if that wasn’t enough, they take it even further: split data and functionality! Thank god we all agree that this breaks Object Oriented Programming. These entity systems seem to use the strategy pattern to support different functionality. Well, in my system, the component just specifies its own functionality, in a good old Object Oriented way, and encapsulated.

Don’t ask me how such a ECS uses an external physics engine for example. I guess they try to synchronize their own component data with the body properties delivered by the physics engine, I don’t know. Or they just write their own physics engine because 3rd party libraries aren’t good enough. The typical [NIH](https://en.wikipedia.org/wiki/Not_invented_here) syndrome ;).

Anyway, from a conceptual standpoint, it feels wrong. It also breaks Object Oriented Programming, which probably also contributes to the weird feeling I have when looking at that architecture.

When I was young I would probably call the current Entity Component System *wrong*, but now that I’m older, I realize everything has advantages and disadvantaged. The obvious advantage is performance, as also mentioned in [Misconceptions of Component-Based Entity Systems](http://www.shaneenishry.com/blog/2014/12/27/misconceptions-of-component-based-entity-systems/):

There are multiple reasons for this and the biggest is performance.


But as said before, I prefer a good conceptual architecture, which allows easy reasoning, above an architecture that tries to pull the last bit of performance out of the hardware. Yes, I make old-school 2D games, I can afford that. Besides, since I use external libraries for physics and rendering, I leave optimization to the bit-loving C/C++ programmers that wrote the library. (I love those guys, because they love the work that I hate).

Now that I gave you some indication on how my entity component system differs from others out there, I still haven’t gone into details. But because this (ranting) article is already becoming quite lengthy, I will keep the complete explanation for a follow-up blog post. (Yes, all good series end with a cliffhanger)

## 3 Comments

## Joe · October 23, 2015 at 22:06

Before I go into everything else, I want to point out that what you have decided on is not ECS, you are simply using OOP with a component-based design. ECS is completely different, other than the fact there are things labeled as “components”. For this reason, your title is misleading; really, you are just using MVC while chucking labels around and adding in a couple extra design approaches.

The “What is an Entity Framework” blog post did not read as something that would be the best way to understand the ECS architecture. I highly recommend you read a more thorough overview from someone who has been working with, and designing, ECS for more than 10 years – http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/.

I can relate to your perspective on things (if anything, I think any programmer can) as it is never fun wasting time on an alternate solution when another already exists. I, too, am not entertained by grinding out performance and low-level functionality; it is always more fun just getting things done in the easiest way possible. That is why there is so much garbage in the software industry – everyone wants to take shortcuts. Programming is a job for a reason; there are always aspects we won’t enjoy and we have to push through it and get it done if we want to do it right.

Unfortunately, when it comes to deciding on using a new architecture it isn’t as simple as just understanding the principles and you’re away laughing. We have to put the time into researching and experimenting with how it works to learn the best approach to applying it correctly.

Sorry if the rest of this comment comes across as if I am attacking you, I just don’t know how else to get the point across without being blunt about it.

To get started with the problems with your post – you are trying to mix three different architectures together (OOP, MVC, and your assumed view of ECS) and then trying to say ECS is weird/confusing because it doesn’t fit in; I don’t understand what logical point you are trying to make as there is no logic in expecting multiple architectures to fit together without issues/conflicts.

The reason ECS “breaks” OOP is because it is NOT OOP. It is data-oriented programming, not object-oriented programming; it isn’t meant to fit with OOP because it is completely different.

If you are trying to create something new that fits your specific desires, you have to come up with something that actually makes sense. You can’t just try to mash things together then complain that one of the architectures you mashed in didn’t fit.

You also appear to misunderstand why ECS is done in the way it is (especially seeing as you are trying to compare it to OOP).

The point in splitting up functionality from the component is so that you can have functionality for an entity depending on the components it has, rather than mashing all of its possible (but likely unused) functionality into itself and/or duplicating functionality across different components and then trying to get them all to communicate with each other (which is why people using OOP with component-based design generally run into problems with doing so, hence the reason ECS exists instead of going with the more comfortable/relatable approach of OOP with component-based design).

It is better keeping specific functionality together rather than duplicating and convoluting it so with OOP we put the functionality into an object. With ECS, A system takes over this but allows for much more flexibility as it isn’t specific to an object but instead specific to a component or set of components.

The other benefit of splitting functionality from components is so that one system can handle the specific functionality rather than having each instance of a component deciding when to run its functionality; this makes parallel programming and multi-threading much simpler to deal with.

It is also much more straight-forward to debug a problem via a system in comparison to debugging instanced functionality.

Even with OOP, systems are used for things like physics for similar reasons.

Your point on things like physics engines/libraries not tying in with ECS (and bashing on people using ECS as if to say they resort to NIH syndrome) – there are lots of physics libraries which have the functionality required that can tie in with your own properties rather than forcing you to use their objects or components. If you have decided you are too lazy to bother making stuff fit in with your properties and would rather just have the third party solution do everything for you then why the hell are you bothering with coming up with a proper architecture?

If someone wants to create a solid framework which does not conform aspects of itself to fit third party solutions, there is always going to be at least re-writing of third-party source code to re-structure. Why do you think a lot of companies make their own in-house solutions or pay for source access; it is always tidier and much more manageable when you have a solid architecture instead of trying to fit around different approaches.

You are also missing the fact that one architecture likely won’t fit with other architectures.

If you are using something like a physics engine designed with an OOP architecture (which will be common, as OOP is the most widely-used architecture in the gaming industry), you don’t just create a game or engine with a different architecture and then complain that it doesn’t conform to it. Deciding you have to re-invent the wheel or change to an entirely new architecture to fit their system is a joke; you can fit it in, it just means you won’t have your engine or game following a solid architecture. Using third party solutions and expecting them to perfectly fit your preferred approach is illogical.

If it all just lead you to “oh I can’t be bothered, OOP is just simpler because I already know how to do it” then it leads me to ask – why did you bother writing this and why did you bother trying to do something different if you just wanted to stick to what you knew?

If you were expecting it to be a simple transition, unfortunately it never is with architectures; IF you want to do it right, that is (especially when having worked with a completely different architecture for a long time).

I tried to keep it as short as possible, there is a lot more I could go over but I think those are the main things that needed covering. I hope you see this as me trying to be informative rather than as an attack; I put the time in to write this comment to be helpful rather than to offend.

## Joe · October 23, 2015 at 22:27

Just realised I also wanted to touch on the part where you said you were doing this more for more of a conceptual system:

I disagree with the main reasoning for ECS being as a performance gain; if used incorrectly or with an inefficient communication system it can be the opposite. The core reasoning is for decoupled, straightforward and highly flexible code.

I also believe you can find ECS just as easy for conceptualisation because of the flexibility with decoupling in comparison; I think the main issue you are having (as most programmers do) is that your mindset is currently stuck in thinking OOP when doing anything but it differs so much from OOP. I, myself, had to overcome that struggle.

ECS can be slow in comparison to OOP when establishing the framework for a game; but, as soon as the framework is implemented, ECS becomes exponentially faster to work with in comparison to OOP.

Once you build out a proper framework for ECS, and understand exactly how everything works with an ECS architecture, you can create (or prototype) most games much quicker and with much more ease.

## Jim · January 27, 2016 at 11:45

https://github.com/sschmid/Entitas-CSharp