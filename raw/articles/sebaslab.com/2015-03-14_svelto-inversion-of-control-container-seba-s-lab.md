---
title: Svelto Inversion of Control Container - Seba's Lab
url: https://www.sebaslab.com/svelto-inversion-of-control-container/
author: Sebastiano Mandalà
published: '2015-03-14'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

If it’s the first time you visit my blog, please don’t forget to read my main articles on the subject before to continue this post:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)

It’s finally time to share the latest version of my Inversion of Control container, which I named Svelto IoC, which I will keep updated from now on. This new version is the current IoC container that Freejam is using for the Unity3D game Robocraft ([http://www.robocraftgame.com](http://robocraftgame.com)).

Thanks to the possibility to use the library in production, I could analyse in depth the benefits and disadvantages in using extensively an IoC container on a big project with a medium sized team of programmers. I am preparing an exhaustive article on the subject, but I am not sure when I will be able to publish it, so stay tuned.

The new IoC container is structurally similar to the old one, but has several major differences. In order to use it, a *UnityRoot* specialised monobehaviour must still be created. The class that implements *ICompositionRoot* is the Compositon Root of the project. The game object holding the *UnityRoot* monobehaviour is the game context of the scene.

All the dependencies bound in the **Composition Root**, will be injected during the Unity *Awake* period. Dependencies cannot be used until the *OnDependenciesInjected* function or the *Start* function (in case of dependencies injected inside monobehaviours) are called. Be careful though, *OnDependenciesInjected* is called while the injection waterfall is still happening, however injected dependencies are guaranteed to have, on their turn, their dependencies injected. Dependencies are not guaranteed to be injected during the Awake period, therefore you shouldn’t use injected dependencies inside Monobehaviour Awake calls.

Other changes include:

- Monobehaviours that are created by unity after the scene is loaded, don’t need to ask explicitly to fill the dependencies anymore. They will be automatically injected.
- Monobehaviours cannot be injected as dependency anymore (that was a bad idea).
- Dynamically created monobehaviours have always dependencies injected through factories (
*MonoBehaviourFactory*and*GameObjectFactory*are part of the framework). - Now all the contracts are always injected through “providers”, this simplifies the code and makes it more solid. Also highlights the importance of providers in this framework.
- A type injection cache has been developed, therefore injecting dependencies of the same type is way faster than it used to be.
- It’s now possible to create new instances for each dependency injected, if the factory
*MultiProvider*is used explicitly. - You can create your own provider for special cases.
- Improved type safety of the code. It’s not possible anymore to bind contracts to wrong types. For this reason
*AsSingle()*has been substituted by*BindSelf().* - Various improvements and bug fixes.
- Dependencies can be injected as weak references automatically.

What is still need to do:

- Improve the documentation and explain the bad practices
- Add the possibility to create hierarchical context and explain why they are necessary
- Add the possibility to inject dependencies by construction, in order to reduce the necessity to hold references.
- Explain how to exploit custom providers.

The new project can be found at this link: [https://github.com/sebas77/Svelto-IoC](https://github.com/sebas77/Svelto-IoC)


Thanks for sharing the newest version of the container!

After reading the post, I was wondering why you said that injecting into MonoBehaviours was a bad idea. Since the very first version of your container, I always enjoyed this concept and I even carried it on to my current container, Adic. With a little bit of caching, this has never been a problem in any game I implemented it.

Why did you changed your mind about it?

I have ready a very long article that encloses all my current thoughts about code design which I will publish soon, even if I didn’t finish to code the proof of concept (it will take too much time otherwise). In it, you will find more details about my current decisions. According my current rules Monobehaviours don’t ever need to be injected (it’s a feature that is not needed, therefore better remove it for simplicity). Monobehaviours in my current vision can be used as – behaviours for game objects, therefore they don’t need to be injected anywhere, however they can have… Read more »

Interesting thoughts on the problem! However, after reading your P.S., it made me think that maybe I understood your observation all wrong. In fact, injecting MonoBehaviours somewhere is really a bad idea, as you pointed out – missing references can be a mess! However, as you also indicated, injecting dependencies INTO MonoBehaviours is no problem at all – and that’s where I think got it all wrong: I was thinking that wiring dependencies into MonoBehaviours was a bad idea. Anyway, your observations were interesting, as usual. I’ll wait until the article to read more details about your decisions on the… Read more »

ops sorry for the confusion, I will change the sentence.

I like a lot your tight implementation and minimalistic approach.

One question though – why no container hierarchies?

Simple parent-children hierarchy would be quite easy to add into your framework.

Have you never meet the need?

Thanks, I was talking about it with my colleague today. So far I didn’t find a reason to use it, but actually I lately realised that probably the reason why coders tend to use injection as singletons is mainly due to the injection blob resulting by using one container only.

I may add the hierarchical container feature soon.

My most frequent use case is kind of builder/factory that uses child container to wiry dependencies for a complex object assembled from several components. Where parent container provides access to the global (often singleton) services.

For my experiments, I’ve just added a simple single-parent container support into your framework – like 6 new lines or so.

I think its worth it.

(but now I see a need to have nested lookup contexts too… no, better to stop right now. 😉

please send me a code example, I want to understand what you do exactly and why 😉

thank you very much, I’ll check later. It seems pastebin would have been a better solution for the code tho.

Please find below an example code of my usage of the hierarchical containers. The idea is simple: root container defines all “globally” accessible services (app-wide singletons), while children containers are used to assist in wiring together of the “complex” objects – e.g. Vehicles in my example. VehicleBuilder class defines a child container with all necessary components required to construct a new Vehicle instance. For simplicity, the container is discarded after the vehicle is constructed. (some kind of nested scope support could help here for price of added complexity in the framework code, but I’m not sure it’s worth it). The… Read more »

pastebin… of course. sorry, didn’t come to my mind.

here is the link to the code example:

http://pastebin.com/0k1DmmCe

Thank you for the input, it will be useful! I’ll be back on this one probably next week after the 18th, since I am off for holidays ;).

Btw, in your specific case I am a bit concerned about performance. However something must be done.

Hi. That was very interesting to find your site with the IoC framework for Unity, as I have just developed my own framework, and it looks very similar feature and usage cases wise. It’s funny how our solutions are matching, especially with factory things, and also the approach to the mono behaviours 🙂 I wanted to comment on injection of MonoBehaviour as I think it can be still needed sometimes. In my project i have a generic view, that is MonoBehaviour and is created through the factory dynamically. So for different object types, the different instances of the generic view… Read more »

Hello Andrey,

thanks for the comment. In Robocraft, which is a huge project, we never felt the need to inject monobehaviour. Injecting monobehaviour would go against my rules too, since a monobehaviour should be used ONLY as mean to extend a gameobject, therefore belonging only to the relative gameobject and nothing else. Destroying a monobehaviour, which is referenced somewhere else, is kind of awkward and one of the many Unity framework pitfalls.

GUI are always managed by presenter (in a MVP scenario), so it’s the presenter that should be injected, never the view.

Hi. I have several situations where I do inject MonoBehaviours. E.g. have a single coroutine manager for the whole application to start all coroutines on, that i can inject to any objects that start coroutine. Or for example I have a presentation that is aware of its view and injects the view. When instantiating the presentation, I want the view to be resolved automatically together as dependency, and instantiated. There can be many other cases, and while I’m also thinking, that the usage of MonoBehaviour should be careful, I think that I don’t want to limit of how people might… Read more »

WordPress swallows less and greater charaxters so the class signature was this with [] instead of “less-greater” brackets (I don’t know how to screen them)

public class MergePanelUI [T, TChild] : ContextMonoBehaviour, IMergePanelUI[T, TChild]

Hello! Thanks for your IoC container. I am started using it in our Unity3D project. I have one question. You probably use the IoC container in a multiplayer game. In a multiplayer game GameObject should have NetworkBehaviour instead of MonoBehaviour component. The question is how to create a network GameObjects? When the network objects are created on the server scene, they will automatically appear on client scenes. How to control it? The same should be done for the Player GameObject. You can of course override the handlers to control spawn players and objects, but maybe you already have a ready-made… Read more »

Hello,

I am not sure if this question is really relevant to the article, however we don’t use NetworkObjects. All our network events are handled by us explicitly. Anyway you may want to try Photon Bolt, you will find it on the Asset Store.

Thank you for this update. Great work, as always. Regarding the containers hierarchies i tried doing that (in cpp) and Was never Happy with the result, actually i preferred ti keep multiplex Independent containers from which some instances could be “shared” but that is fine manually. The fact is that Sharon bindings in a hierarchies way makes much less obvious which implementation is choosen

Ehm seems this is off post Sorry. I Just saw the last update in github

As I wrote I don’t find IoC containers useful anymore, however if they must be used they should be used hierarchically. One day I will explain why.