---
title: Learning Svelto.ECS by example - The Vanilla Example - Seba's Lab
url: https://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/
author: Sebastiano Mandalà
published: '2018-01-11'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## Note: this is a seriously outdated article. Some concepts may be still valid, other totally misleading. Be sure you put all the pieces together reading all the articles and give more importance to the latest ones.

It’s not simple to learn a new framework and even less shift code paradigm. This is why **Svelto.ECS** has been written with simplicity in mind. Even so, I realised that I ought to write more tutorials to clarify some simple concepts that are not straightforward to grasp at first. That’s why I thought to explain, step by step, what I have done with the examples bundled on github.

*A word before to start:* I would really appreciate if you send me your feedback and, when you start to have a good understanding of the framework, share your knowledge with others. I am willing also to review your code when possible, if you share it publicly, for example on github. You can also feel free to update the Svelto.ECS wiki page and send pull requests. You may also think that it would be better to study Unity ECS framework and in this case I would say that being an open sourced c# framework built on top of the Unity engine, it will probably do the same things Svelto.ECS does, only in a different way. At the moment I recognize that Svelto.ECS has some unique features that cannot be found on other currently available frameworks, so it’s your choice to take advantage of them and compare them. Svelto.ECS has been engineered to be both fast and convenient to use, but also rigid enough to dictate, when possible, the right way to design your code, reliving the coder from the responsibility to take the right decisions to write maintainable code easy to refactor without penalizing performance.

All that said, let’s start from the simplest possible project! This project doesn’t even use Unity, so you can just run it with Visual Studio or compatible IDE/compiler. Just for fun I decided to use the .Net Core and .Net Standard frameworks (yes both!!) but the code will compile also on the classic .Net framework. Get it from [https://github.com/sebas77/Svelto.ECS.Vanilla.Example](https://github.com/sebas77/Svelto.ECS.Vanilla.Example)

It’s a bit longer than I would have liked because I decided eventually to cram inside most of the features available. Still, if you remove the comments, the real lines of codes aren’t many!

Let’s have a look at the lot, hoping you will not get lost (you shouldn’t)

Well, well, still there? I put the whole code in one file only to demonstrate that the boilerplate to write is very minimal, remember I am showing virtually all the features available in the framework. Now, instead to repeat what I wrote in the code comments, I will try to explain the concept behind it. Please be sure to have understood the previous code before to continue reading. When I develop with Svelto.ECS (always now :)), the real first task I perform is to identify conceptually the entities I want to manage. This first step is of crucial importance and I will explain better why in the next articles about pitfalls and best practices. You must strive to identify an Entity inside the game design domain, using a game design language. For example, good entities are: *MainCharacterEntity*, *CoinGUIWidgetEntity*, *MinimapEntity*, *TileEntity* (if you have tiles that perform any logic) and so on. In the example, I identified the entities *SimpleEntity* and *SimpleEntityStruct*. Those are really bad names, first because they are conceptually abstracted and they must not be, second because the fact that an Entity will be built in a group doesn’t actually identify a new entity as the same entity can be built either grouped or not. Those names are for the purpose of the simplest example I could write, so forgive me to break the rules.

Let’s pick-up now the entity we want to start to work with, for example the *SimpleEntity*. The next step is to add behaviours to this entity and in order to do so an *Engine* must be created (If you never read any article of mine before, please note that I chose the word *Engine* over *System* as I find it more meaningful). Now for the sake of the example I called it *BehaviourForSimpleEntityEngine ***but you have to name your engines according the behaviour you want to implement***. *For example good names for Engines are: *WingsPhysicEngine*, *WheelsRenderingEngine*, *MachineInputEngine* and so on…

In a classic ECS framework, Systems usually handle entities directly. Instead I decided to use a different approach that I first saw in the Actionscript ECS framework called *Ash*, introducing the concept of *EntityView *(previously named Node in Svelto.ECS 1.0). It’s very simple: an EntityView is how the Engine must see the Entity. It’s basically a filter to not let the Engine have access to all the Entity data. In this way you can focus the engine responsibility, since global data access would promote less modularity. If the *Lazy Coders(*)* could access to ALL the entity components nothing would keep them from adding more logic in the engine that is not really responsibility of that engine. *EntityViews* promote encapsulation, modularization, single responsibility and design rigidity.

In our case the *BehaviourEntityClassEngine *can see and handle the entities *SimpleEntity* through the views *BehaviourEntityViewForSimpleEntity *(yeah, it’s pretty hard to name abstract concepts)*. *Entity views can be created as classes for flexibility and as structs for speed. I will talk about EntityViews more on other articles as their properties must be explained properly, but I don’t want to add too much information right now.

Now careful about this: an Engine usually should just implement the *IQueryingEntityViewEngine *interface as most of the time is enough to query the entities you want to handle with the *EntityViewsDB.* However Svelto.ECS has also the feature to know when entities are removed and added from the engine through the *Add* and *Remove* callbacks. If you want to enable them, you can use the *SingleEntityViewEngine* and *MultiEntityViewsEngine* pre-made classes which help to reduce boilerplate code. You will notice that the *MultiEntityViewsEngine* doesn’t accept more than four *EntityViews*. This because empirically I noticed that an engine handling more than four different entities is very likely to have more responsibilities than should and must be refactored. Also note, engines should never contain states and if you design your entity views properly, you don’t really need to. A perfect engine is totally encapsulated and its methods are both private and static (pure encapsulated logic). Advanced scenarios will be explained in other articles.

*EntityViews* group **Entity** **components**. When EntityViews are classes, EntityViews group components as interfaces. In Svelto.ECS components are always seen as interfaces, this is another unique feature and I will explain the benefits on other articles. In our simple example, the *SimpleEntity* is composed by just one component the *ISimpleComponent*. An entity can be composed by several components and an EntityView can reference more than one entity component, but for the time being, let’s keep things simple. When Entity components are structs, they actually coincide with the components themselves. Entity as struct is an advanced concept and I don’t need to explain it now, as you would need to use them only in very specific scenarios or just for fun.

OK that’s it, the code now compiles as you have all the elements needed, however it will not run since those components are not implemented…well that’s right, I didn’t explain how to actually *build* the entities. Build entities come for last in the order of things to do.

Often you will read that in modern ECS frameworks entities are just IDs. This concept can be extremely confusing for a person who comes from an object oriented background, so for the moment ignore it. In Svelto.ECS you have a real convenient way to identify an Entity and this is the *EntityDescriptor*. In the example I avoided all the boiler plate needed to create an EntityDescriptor using the *GenericEntityDescriptor* and the *MixedEntityDescriptor* pre-made classes. Use them whenever possible.

The *EntityDescriptor* links Entity Components to the relative *EntityViews* and/or *EntityStructs*. If EntityViews as classes are used, we just need a way to implement those components as interface. Finally this is what the *Implementors* are for! Implementor is a very powerful concept, but I don’t need to explain them in detail now. After all, from the example, it should be simple to understand how to use them.

OK This should be enough to give you an introduction to the framework! Is something not clear? Please leave a comment here, I will try to help!

In summary:

- Always define your Entities conceptually first
- Start to write Engines and identify the EntityViews that these engines need. EntityViews define how the Engine must see the entities it must handle, so EntityViews are named after the Engine and the Entity and must be created together with the Engine and in the Engine namespace.
- Define the Entity Components the engine must access to while you code the Engine behaviours, use refactoring tool to easily generate the interfaces you need (I will explain some tricks on other articles)
- Create the EntityDescriptors that link the Entities to the EntityViews
- Finally implement the Entity Components as interfaces through Implementors and build your entities. The EntityView instances will be automatically generated and inserted in the EntityViewsDB by the framework.

(*) Lazy coders are the best, but if they lack of discipline they could lead to catastrophes 🙂

**if you are new to the ECS design and you wonder why it could be useful, you should read my previous articles:**

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

Check also the other ECS articles:

http://www.sebaslab.com/learning-svelto-ecs-by-example-the-survival-example/

and for reference:

What is exactly the purpose of IEntityfunctions?

I am going to talk about it in the next article but if you check the interface should be self explanatory

I meant the intent should be

It was not for me 😀 I had to look to implementation. why RemoveEntityFromGroup ignore the groupID?

Hello Sebastiano!

Are you going to update the “Vanilla” example to ECS 2.7? And, probably, you will make an accent on Entity as struct because right-organized memory is the most valuable benefit of ECS and DOD?

Thanks

Yes I’ll do. There is another example, also to update, dedicated to the cache friendliness. Personally for me the greatest benefit of the ECS is instead the organisation of the code and I extensively talk about in my articles.cache friendliness is cool, but has limited real life applications multi threading is way more important and ECS helps for that too .