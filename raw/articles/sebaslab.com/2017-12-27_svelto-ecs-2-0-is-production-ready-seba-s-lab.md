---
title: Svelto.ECS 2.0 is production ready - Seba's Lab
url: https://www.sebaslab.com/svelto-ecs-2-0-production-ready/
author: Sebastiano Mandalà
published: '2017-12-27'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

This an introductory post to **Svelto.ECS 2.0**. Other two posts will follow, one explaining the examples line by line and another explaining all the Svelto.ECS concepts in a simpler fashion than before. Therefore this article is written for who already knows Svelto.ECS.

Svelto.ECS 2.0 is (at the time of writing this) available in alpha stage (pick the alpha branch to have a look now) and, compared to Svelto.ECS, introduce new features, new optimizations and unluckily some breaking changes (main reason why I decided to bump the major version).

I have also updated the [Svelto.ECS.Examples](https://github.com/sebas77/Svelto.ECS.Example) code (available on the alpha branch at the time of writing) and added a new [“vanilla”](https://github.com/sebas77/Svelto.ECS.Vanilla.Example) example which I can consider the minimum amount of code to write to show almost all the framework features available without using Unity. The new example is, in fact, targeting Net.Core and Net.Standard.

I will quickly go through the list of new features:

- New terminologies have been introduced. If you read the previous articles or used Svelto.ECS 1.0, you must know that the term “
**Node**” has been abolished as it was meaningless in the framework context and has been renamed to “**EntityView**“. I will explain why it makes more sense with the next articles. - The
**GenericEntityDescriptor**has been extensively used in all the examples to show how to reduce the boilerplate code with minimum effort. **EntityDescriptors**are now pure static classes and must not be instantiated. The**EntityDescriptor**must conceptually identify your entity. The future articles will explain why it’s a big design mistake to identify Entities as**EntityViews**instead. A Entity is now built with the new signature*entityFactory.BuildEntity<*In any case you should rarely need to inherit from EntityDescriptor as most of the time you must inherit from**SimpleEntityDescriptor**>(entityID, implementors).*GenericEntityDescriptor*and*MixedEntityDescriptor*.- EntityDescriptors can now refers, using the same signature, either to class based EntityViews and struct based Entities, so that
*entityFactory.BuildEntity<*will actually build struct based entities. Previously the struct based entities were build in a more awkward fashion. While I deprecated the previous method to build struct entities, changes may be introduced later to support thread safe code as currently Svelto.ECS data structures are not thread safe (custom structures or strategies must be adopted to support thread safe engines). With the next articles I will explain when and how to use EntityViews and Entities as struct. EntityViews should be used for flexibility and Entities as structs for speed. An EntityDescriptor must inherit from the new**SimpleStructEntityDescriptor**>(entityID);*MixedEntityDescriptor*generic class to build entities made out of Entity structs and/or EntityViews. - Another very important feature is the possibility to create entities inside buckets (groups). In this way is possible to query a set of entities from a specific group. This is a feature that was absolutely needed in our products (and very likely in yours too). For example we can now easily query all the wings for each machine in Robocraft. This means that we could potentially create a Svelto.Tasks taskroutine for each machine inside the WingsPhysicEngine and stop a specific task if all the wings of a specific machine are shot off. Previously there wasn’t a way to be able to split wings per machine unless custom datastructures were used inside the engines. The new function has the signature:
*entityFactory.BuildEntityInGroup<SimpleStructEntityDescriptor>(entityID, groupID)*and can be used both for struct Entities and class EntityViews. - Entities can also be moved between groups. This was a last minute idea and I need to experiment more with it.
*EnginesRoots*must never be hard referenced. Previously I made two mistakes: first hard referencing it inside the*SubmissionNodeScheduler*(now called SubmisisonEntityViewScheduler) and second letting it be passed around through the*IEntityFactory*interface. Now an IEntityFactory wrapper must be generated from the EngineRoot.- A
*IRemoveComponent*cannot be implemented with a custom implementor any more. Just use it and don’t worry to pass a*RemoveImplementor*among the other implementors (it will be ignored as it is created by the framework now). - The framework is now more rigid and output more warnings in case of misuse.
- All the previous framework engines, except for the
*SingleEntityViewEngine*and*MultiEntityViewsEngine,*have been deprecated. An engine can inherit either from one or the another and/or implement*IQueryingEntityViewEngine*(which is an IEngine too now) - I am adding comments all over the code, but I will add more while I write the new articles to come.

then optimizations:

- Building an entity can be up to 3.3 times faster than in svelto.ECS. However remember that entities should be sporadically or never built during the execution of the gameplay. Entities should always be prebuilt and enabled/disabled when needed. This is even more effective than pooling them, so design them properly. Below a table to show how long takes to build 256k entities as class with Unity 2017.3 (building entities as struct is an order of magnitude faster).

**Version****Platform****Time(MS)**1.0 .net 2.0 903 2.0 .net 2.0 344 2.0 .net 4.6 260(!) 2.0 .net Core UWP 203 2.0 .net Core IL2CPP 288 if you wonder while IL2CPP is a bit slower, is because I cannot dynamically create code that allows avoid Reflection functions, however the c++ implementation of the reflection is much faster so no much trouble there.

- Thanks to the new feature to move entities between groups, you can create a group to store the disabled entities, so that you can retrieve a disabled entity yourself to be reused later.
- Several optimizations here and there, especially to reduce allocations.

and breaking changes (at least the ones I took note of):

- The BuildEntity signature is totally different and will need to be explained in an another article.
*IRemoveComponent*was breaking a not enforced (yet) rule of Svelto.ECS which is that a component cannot hold references to other classes (except Unity ones at the moment). This is because a component must be seen a data container and cannot be used to call external functions. Thus, the method to remove an entity has changed to*_entityFunctions.RemoveEntity<SimpleEntityDescriptor>(entityView.ID);***Mass Renames***(hope I didn’t get any wrong, I will fix later in case)*:- rename IQueryableNodeEngine into IQueryingEntityViewEngine
-
rename IEngineNodeDB into IEngineEntityViewDB
-
rename NodeWithID into EntityView
-
.QueryNode< to .QueryEntityView<
-
.QueryNodes< to .QueryEntityViews<
-
.TryQueryNode( to .TryQueryEntityView(
-
all the nodesDB must be renamed to entityViewsDB
-
MultiNodesEngine to MultiEntityViewsEngine
-
SingleNodeEngine to SingleEntityViewEngine
-
UnitySumbmissionNodeScheduler is
UnitySumbmissionEntityViewSche duler - INodeBuilder to IEntityViewBuilder (you should use the GenericEntityDescriptor/MixedEntityDescriptor though)
- NodeBuilder to EntityViewBuilder (you should use the GenericEntityDescriptor/MixedEntityDescriptor though)

-
*ICallBackOnAddEngine*doesn’t exist anymore and it has been merged into the*IQueryingEntityViewEngine*interface. This means that the Ready function must be always implemented in these cases.

N.B.: As long as Svelto.ECS 2.0 stays in to alpha state, do not use in a production environment. It still needs to be heavily tested and I will need to write some unit tests too. [However you are invited to start experimenting with it and leave some feedback.](https://github.com/sebas77/Svelto.ECS)

**(*) The evolution of my reasoning can be found in these articles that I strongly suggest to read:**

[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)[http://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/](http://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/)(shows what’s changed since 2.5)[http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/](http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/)(shows what’s changed since 2.0)[http://www.sebaslab.com/svelto-ecs-2-0-almost-production-ready/](http://www.sebaslab.com/svelto-ecs-2-0-almost-production-ready/)(shows what’s changed since 1.0)[http://www.sebaslab.com/ecs-1-0/](http://www.sebaslab.com/ecs-1-0/)[http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/)[http://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/)[http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/](http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/)

Would you refactor example to have Input not embedded in the systems? I want to see how would input would be done if it enter the system as entities.

How would you go about implementing FSM as a base engine of the game and all other engines to respect it? Can you turn on/off engines somehow? Maybe create engines per state and enable disable them with state changes.

How to manage the input is a common question. I don’t want to make the example code more complicated than it is to not confuse new people and also because input management is a problem regardless the paradigm you adopt. How would have you solved it in Unity if you don’t want to use the Input static class? A common approach is to create an InputEngine, maybe specialized for each Entity, that takes as input an EntityInputView which has components that are read by other views as gameplay states. For example, the Input engine read the action linked to the… Read more »

What I want to see from any type of highly decoupled opinionated framework is ways to do the most common things in decoupled ways. Why use this highly decoupled ECS if we are going to have input embedded inside Engines and thus not unit-testable? I know there are ways to do it but I disagree that “make the example code more complicated”, it is already complicated enough. Showing how input should be handled will not make it more complicated in my opinion.

heads up about the changes almost finished. You can already give a look at the solutions you were seeking.

Yes that’s obvious, but the example shows just one way to use the ECS framework. Under my point of view I see an ECS framework more like an extension of the language than a framework (and that’s why I often speak of paradigm), as it forces to think different ways to approach classic problems. So even if I am trying to make it as rigid as possible, it doesn’t mean that the user cannot fall in to the classic coding errors. Obviously you say that I shouldn’t promote bad coding…that’s a good point. Well you made me think, because so… Read more »

Both Svelto.ECS and Svelto.Tasks has Utilities. Including both projects as submodules leads to Utilities duplication. Maybe they should be a submodule also?

yes good point I have to do it

if Svelto.ECS and Svelto.Tasks have the same submodule, you will need to decide which one to initialize anyway. I wonder if there is a better solution.

What is the main use of the Svelto.ECS? I have read some blog in github and this website, but i have no idea about this framework.

Well, to keep it simple, it’s just a way to write code for your game. It forces the coder to use several good practices. Because of this at first it can look counterintuitive, but after passed the initial wall, it becomes quite easy to get in the flow (this has been proved several times).

You may wonder if Svelto.ECS is necessary. Of course it’s not, it’s just a way write code, however if you use it you will be able to get familiar with good code design practices.

you build from top to bottom , i read your blog posts and can’t wrap my head around the framework ,

maybe building from bottom to top is a better approach , your vanilla example can’t be understood either ,

no matter how good a framework is , when there is no simple doc i rather not use it and get lost after spending time on it.

Hey, if you don’t know what is the problem ECS is trying to solve, it will be hard to understand the theory. In this case it would be better to start with the practical examples. Start from these: http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/ . You must download the code, it’s full of comments, literally hundreds of lines, enough to make another article, you must study them to try to understand what’s going on. then you can switch to these other tutorials: https://eagergames.wordpress.com/category/ecs/ (Dario Oliveri) https://blogs.msdn.microsoft.com/uk_faculty_connection/2018/05/08/entity-component-system-in-unity-a-tutorial/ (Lee Stott) they may refer to different version of Svelto.ECS. If you start to understand what it’s all about,… Read more »

Yes, I’ve just found this ‘Zombie’ tutorial at msdn, and I had seen the light. I can honestly recommend this tutorial to all of you, that had trouble to understand how it works. Sebastiano, Sir, I want to thank you for your contribution, work and willingness to share knowledge with us. I thought that I can write a code. But it always was messy. Back in late 90’s there was always only OOP, strict OOP. But I could never think that way. When I finally found your blog, it hits me. It’s right way, I want to think that way.… Read more »

great story Tomasz, keep up the good work and let me know if I can help or you want to help us 🙂

Is there a way to reach you on Discord? The link I found is not working any more 🙁

Try this https://discordapp.com/invite/3qAdjDb