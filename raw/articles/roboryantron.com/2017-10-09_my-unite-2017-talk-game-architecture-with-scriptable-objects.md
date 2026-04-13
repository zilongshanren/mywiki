---
title: My Unite 2017 Talk - Game Architecture with Scriptable Objects
url: http://www.roboryantron.com/2017/10/unite-2017-game-architecture-with.html
author: Roboryantron
published: '2017-10-09'
source_blog: roboryantron
source_site: http://www.roboryantron.com/
category: game programming
fetched: '2026-04-13'
---

Unite 2017 wrapped up in Austin last week and I finally got to give a talk that was all about ScriptableObjects (and ride a jackalope). I have been exploiting the hell out of these things since I first discovered the under-documented feature back in 2011.

### Session Details

Game Architecture with Scriptable Objects focuses on making modular, data-driven, editable game systems while avoiding (and trash talking) crutch patterns like singletons.Using ScriptableObject based classes, you can easily edit and store references to data from prefabs in a scene. However, ScriptableObjects are not constrained to just static data. You can change data from one prefab and read it from another. This allows for the exchange of state between prefabs without the need for a rigid connection between them.

A similar pattern can be used to construct an event system. Scene objects can add themselves to a list on a ScriptableObject based asset to indicate that they are listening for a certain game event. Later, a different scene object can "raise" the event, looping through the list and notifying all listening objects. Again, this pattern removes rigid connections between different systems in the game.

Game Architecture with Scriptable Objects covers these topics and more, with a ton of simple code samples, practical demos, and bad programming jokes.

[The video is on Unity's YouTube channel](https://youtu.be/raQ3iHhE_Kk)

[The slides are on SlideShare](https://www.slideshare.net/RyanHipple/game-architecture-with-scriptable-objects)

[The sample project is on GitHub](https://github.com/roboryantron/Unite2017)

### Follow Up

One common question I got about the FloatVariable is how to avoid having the runtime data save when the game stops. The truth here is that the sample I showed in the session has been dramatically simplified from what I normally use so it does not handle this use case. You can use OnEnable to copy your default value into a non-serialized current value. Then you only access through the CurrentValue property. An added benefit here is that a float property can be set by a UnityEvent while a float field cannot.Another note with these is that you may want to add

[DontUnloadUnusedAsset](https://docs.unity3d.com/ScriptReference/HideFlags.html)to the HideFlags to make sure you do not lose state if nothing is referencing it.

The full implementation of this variable system that we use at Schell Games has a bunch more features, custom icons, and a generic base class making it easier make new variable types. Same thing goes for our event system. While I can not post the source for these things, I hope that the concept helps people start hacking apart ScriptableObjects more!

This was a great presentation - thanks for sharing! Super keen on implementing this idea :)


ReplyDeleteOne of my favorite talks from the conference. Thank you so much!

ReplyDeleteI love everything presented in your talk! Thanks for putting the effort into that!

ReplyDeleteI know you cannot post source for this, but as a non-specific question: How do you keep the editor view for this the most generic. Do you dynamically create code for property drawers and such? I'm currently working on something that also uses SOs for simple types. It's not the same thing and a very different use-case but it still has the principle that a SO sometimes wraps a single value and I need the most generic way of doing that. I currently derive a new sub-class for every atomic value that has a simple type. Do you do that with ValueReference or do you have a very generic version that somehow also has a generic property drawer that knows how to generate code to render it in the inspector?

ReplyDeleteThe event system that I made handles this by keeping the generated code simple. The generated class is nothing more than a definition of the class and fulfillment of a few generics.


DeleteThe inspector then works with SerializedProperty rather than directly with the fields. This means that the inspector does not need to know the actual type since PropertyField takes care of that.

One thing that seems a bit problematic also is the GameEvent. You give it a list of GameEventListeners that every monobehavior has to derive from that wants to listen to it. That seems very limiting. An interface would obviously better but Unity doesn't serialize on interfaces... so unless I use a monobehavior per event I want to listen to and then let that communicate with other monobehaviors that do the ACTUAL logic... I don't know this seems like one of those hacks that work around the big limitations of Unity's serialization system. Adding a component per event a gameobject needs to react to seems very very cluttering and not like good design at all to me.

DeleteIs that how you do it or do you have a more clever solution in real projects?

In our system, there are three ways to register for an event: GameEventListener MonoBehaviour, interface, and delegate.




DeleteThe MB one is the most flexible since it does not require any code changes. It does use a MB per event responded to so we kept the editor simple with an optional "Advanced" dropdown. If not planned, this list can get large, but if you properly modularize your systems, each prefab will only be concerned with a small number of events since it does only one thing. Enemies are only concerned with combat and high level state related events so even if your game gets bigger, they should not observe every new system.

The interface option allows us to do the response in code. This is for things that we know need to respond to certain events to have any functionality. It is less flexible but faster and cleaner on the editor. A MB implementing the interface takes the events it responds to in the editor and the response is done in code. There is no need to serialize the interface references since they register at runtime.

The delegate option is similar to the interface one, but makes it easier for a class to respond to multiple events.

Hi that talk was amazing... i am used to use singleton but i hate when I have to drag all manager into the scene to test out a new scene. The process you discussed is amazing. But I can't understand how i start implementing those in my project in a bigginer friendly way. Please need your attention on this

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThanks for showing us a great architectural concept with Scriptable Objects! This indeed is very helpful in creating small modular building blocks which are easily configurable. Just awesome!



DeleteOne thing I noticed from your example code, and what makes me wonder, is that you simply assign those SO variables to various instance objects (like the slider, health meter, pitch value in the mixer, etc.) directly inside update() methods of all their corresponding MonoBehaviours.

I guess this is just to simplify the demonstration code and not something we really would want?

If your data is subject to change every frame you would do it in the Update loop, if it is not changing frequently, you could do it as an event model.


DeleteI simplified a lot of these systems for demonstration purposes, but in the real-world games we have shipped with a system like this, that pattern occurs a lot. What is it about the implementation that is making you wonder?

Thank you for the excellent talk at Unite 2017. It was a great explanation. I have a question about the events. All the events in your demo were static events (no arguments). How do you handle dynamic events (with arguments)? Do you add more variables to the GameEvent SO to handle this, or do you create multiple SO's to handle them? For example, if want to call a custom event with a GameObject argument.

ReplyDeleteIn the much more elaborate system I built in the studio, we allow for argument passing with events. This means that you need a new event type definition for each passed type. for example, GameObjectEvent : GameEvent. You also need a listener type, GameObjectEventListener : GameEventListener and a UnityEvent type, GameObjectUnityEvent : UnityEvent.


DeleteI have this code get auto generated to make it easy to add new types, but it is still simple to implement each one.

That answers my question. Thanks.

DeleteThis comment has been removed by the author.

DeleteThis comment has been removed by the author.

DeleteIf I do that (making a GameObjectUnityEvent:UnityEvent) I will loose it on the inspector !

DeleteYou said you auto generate the code to create new types. I have been having issues with some AOT platforms and using generics. Is that why you auto generate instead of using generics? What method do you use to generate the implementation?

DeleteHi, thank you for your presentation and the talk! I have a question about resetting ScriptableObject variables when the game stops (I've asked the same question on YouTube).



ReplyDeleteSuppose you have a variable IntVariable (which is an asset of your ScriptableObject). You can access and change its RuntimeValue integer field in playmode. However, when you reload your scene and get every GameObject and Component re-initialized, your IntVariable asset instance will still have the previous RuntimeValue, because it had no chance to reset it. Neither OnEnable/Awake nor ISerializationCallbackReciever methods are called on ScriptableObject asset instance when reloading the scene.

What is the solution to resetting all these variables when the scene reloads? Having a gameobject with a component which looks up all variables and resets them? Of course, this component must be executed before all other scripts, so this looks like a hack...

You are correct that the RuntimeValue does not naturally reset between scenes. In a lot of cases, this is a desired feature. It allows data to carry from one scene to another without needing DontDestroyOnLoad objects.



DeleteIn the case where you do want them to reset, define a function that sets RuntimeValue to InitialValue. You can write a component with an OnDestroy in each scene that resets a bunch of Variables. Alternatively you could use the SceneManager.sceneUnloaded callback.

If you have more than a few variables to reset, you could make a ScriptableObject that indexes all of the variables that need to be reset and use OnDestroy or sceneUnloaded to have that object reset all of the variables it is pointing at. You could even make that object auto-populate itself by scanning the asset database for variables at build time or onvalidate.

Thank you! This is helpful for most of scenarios. However, resetting the required variables in OnDestroy/sceneUnloaded of some component does not solve the issue that these variables will not be reset when exiting the play mode in the editor. Do you have some suggestions for this case? Using playmodeStateChanged event?

DeleteThere should be no need to reset on playmode stop if you operate on a RuntimeValue that is explicitly non-serialized.



DeleteI would have Value or InitialValue be the serialized data that you change in the inspector. When the game starts (something like ISerializationCallbackReciever.OnAfterDeserialize), copy InitialValue into the nonserialized RuntimeValue.

If you operate on RuntimeValue it should not get saved to disk.

Yes, you're right. Every time I enter the play mode, I get OnDisable and then OnEnable called on my variables. I can reinitialize runtime values there. Thank you!

DeleteWhat is the usage of copying InitialValue into RuntimeValue ?

DeleteOne question that I keep coming back to is where you mention in your talk that "this can become quite cumbersome" and then you introduce FloatReference as an additional layer to FloatVariable ... but you omitted to explain WHY this had to be a separate class and what the benefits are.



ReplyDeleteWhat are the reasons of using this "xxxxReference" class layer? Can't we just throw this all in the xxxxVariable classes? I think I'm missing a point but I just can't see it.

Additional question: how do you prevent developers from using the xxxxVariable instances directly, or is that not a concern?


DeleteMoreover, have you had issues with the variables being "public settable" by default and how do you combat that? For example, I can foresee weird bugs that end up being caused by, imagine that, the player's health changed from the GUI system? I'm thinking of preventing that by restricting write access to variables, at a minimum by adding a "writable" checkbox.

Dammit. I got it. :)




DeleteThinking about the "writable" bit brought it to my attention. If I had this "writable" flag in the variable itself, it would be either globally writable or globally read-only. I would HAVE to put that in the reference class, so individual "consumers" of the variable can have the writable status set individually for them.

Though for instance your "constant" use case seems to make more sense to have in the variable class, ie this would then make the variable "globally read-only". Whereas if you need the reference to be constant, you could as well use a simple float field instead.

The only neat thing about constant being a flag in the reference class seems to be able to switch between constant and non-constant value without losing the variable reference - perhaps this is meant for experimenting/debugging stuff? I can imagine something like setting player health to constant temporarily to make the player invincible during playtesting.

My full implementation actually does have a "read-only" option for variables. If a write is attempted, it can be ignored and optionally throw an exception.





DeleteThe goal of the serializeable reference class is to give designers the choice to use a shared scriptable object variable or specify a value in line. (I was using the term "constant" in the talk but I have since changed it to "literal" which is a better description)

As for making things read-only from certain contexts, I would not go in that direction. We define certain variables as read-only to allow for a way to flag runtime constants. Preventing writes from specific places gets weird. Variables have a public set function that can be called from a UnityEvent. There isn't really a good way to identify the source at that point.

Our workflow is kind of simple, if you do not want to edit the HP from the UI, do not call the setter from the UI. I do not want to take power away from designers just because it lets them break things. It is this kind of flexibility that lets them create new features.

Setting the player HP to read-only at runtime to debug sounds like an awesome idea, I never thought of that!

Hi! Awesome talk and architecture. I'm new to Unity and these approaches make me very enthusiastic about it.


ReplyDeleteBut probably because I lack the experience I'm missing some important piece in the picture. In your example with FloatVariable for player hp it was created as an asset which then was referenced from different components to bind them to the same instance of a variable. But how should I go about making 'enemy' prefab containing game object for unit itself and game object for a life bar that use the same approach in a way I will still be able to drop as many of them to the scene and have them use personal hp instances (one per enemy)?

This has been a pretty common question. First, unless you are building a game that focuses on one on one combat, I would not recommend making a scriptable object HP variable for each enemy. The variable examples I gave do not work well in a situation where you have a dynamic set of targets like with a lot of enemy setups. I have a much more in depth system that we are using in the studio now that allows us to instance HP variables per enemy, but it is not trivial.


DeleteFor applying HP meters to various enemies, you could consider a RuntimeSet from my examples. Each enemy could add and remove themselves from the set on spawn and death. Then you could have a system monitoring the set and assigning health UI from a pool. Having a higher level system for the health UI also lets you intelligently lay it out on screen so that it doesn't overlap.

Sounds good. Thank you very much!

DeleteI loved your talk and have started using some of the ideas in my own project, namely runtime sets. However, I'm using Asset Bundles in my project, and this is causing big problems, because it seems that the scriptable object assets get copied into every bundle where an asset references it. This results in assets that are using scriptable object in editor without problem suddenly using copies in builds, because they are not in the same asset bundle as other objects that reference the data.


ReplyDeleteOne way around the scriptable object data being duplicated is to put it all into a single data bundle and load it via the bundle manager for each asset that references it, but this then completely breaks the inspector and ease of use. Do you use Asset Bundles at Schell, and if so do you have any tricks to avoid the data being duplicated?

Nevermind, I figured out that I just needed to put the ScriptableObject assets into another asset bundle to prevent each asset that references it getting its own copy. Now I just preload my data bundle on startup and everything works fine in builds.


DeleteThanks for the talk by the way.

I'm glad you found a solution! Sorry I couldn't point you in that direction sooner. There is some Unity documentation (https://docs.unity3d.com/Manual/AssetBundles-Dependencies.html) that covers this a bit.



DeleteIf a asset A is put in an asset bundle and it references another asset B, B is copied into the bundle as well. This can obviously lead to multiple copies of the same event.

If you do not want things to be copied, they must be in their own bundle. Depending on the scope of the game, this could be something like one bundle with the core events and a bundle for the events used in each level.

Hey! I think I saw you mention in one of the comments that you have a system for using ScriptableObjects as instance variables. Could you elaborate on that?

ReplyDeleteThe system we have for this centers around a VariableInstancer component. An instancer defines a lit of variables that it will create its own local copy of (in memory). We then pass the instancer a variable SO like a key and ask it for its local copy.


DeleteSo an enemy prefab could have a VariableInstancer component that says it instances the HP variable. On Enable, this will create a copy of the HP variable in memory. If we ask the instancer for HP it returns the local copy. This is super useful to use in a behavior tree where we can have nodes that branch on variable values specific to the tree owner.

Is there any ways to visually tweak those instances in editor ? Or raise event for just that certain enemy ? (Like death event)

DeleteThat sample project on github...How is it used? There is no scene. I thought this was going to be the project that was shown in the video.

ReplyDeleteThat is the project from the video and there are several scenes. Each demo folder has one or more scenes in it.

Deletehmmm. That's weird. There are no demo folders in my project. I'm going to re-download to check.


DeleteThanks. I am OK now.


DeleteI had downloaded the wrong file: UnityGameArchitecture-master. Do you have any idea what UnityGameArchitecture-master is? (I'm not sure where I got it, or how I got it instead of Unite-2017-master.)

I was looking at your Inventory Example trying to figure out how best to do game state saving & serialization. I figured out the basic idea behind the saving/loading with serializers but I was wondering how and what called Save() and Load() on the Inventory assets.




ReplyDeleteIn a real (non-demo) project would you add everything that needed to be saved to a list manually? Or would you have a class that went through and collected everything up for you?

Once you had all of your objects what events would you most likely call Save() and Load() on? Awake? OnEnabled? OnApplicationPause? Ect.

Thank you for publishing all of this info about Scriptable Objects! It has really helped me create more modular architecture!

I wouldn't look too much into the inventory system, I cut it from the presentation (and the repo) for a reason. I could not find a simplified implementation that would not distract from the point.



DeleteThat said, in the past I have done serialization by having a ScriptableObject that represents player state data that wants to be saved. This is reasonably inexpensive to keep up to date. From there you can call JsonUtility.ToJson to save it at checkpoints of any kind, but this really depends on the game. JsonUtility.FromJsonOverwrite can be used to load from disk back to your data in the SO.

If you are on a slower platform and want a "continuous" save, you may want to go with a solution that can be multithreaded.

I see the use of "public static implicit operator float" in a few areas of the sample code. Is this to make sure your FloatReference is cast properly?



ReplyDeleteDo you have plans on talks for 2018?

I'd love to learn more about how to create clean modular code within Unity.(If you have anymore references please share)

public static implicit operator float lets you use a FloatVariable as a float with less code since it will implicitly cast. This is super useful, but be careful when using it with a bool! An object in c# evaluated as a bool can be interpreted as a null check!


DeleteI do plan on submitting for Unite 2018, but I have not decided the topic yet.

This got me!



Deleteif (BoolVariable)

{

do something

}

..was continuously running.. had to go through and change it to (BoolVariable.Value == true)

A small correction. Not "in C#" but "in Unity". It's qute abnormal for any C# tech to implement implicit cast to bool for null check on a core base class. It's just Unity's quirky "beginner-friendly" architecture.

DeleteHow would you go about passing certain instances with your Event System in the video?




ReplyDeleteI'm familiar with Extending a UnityEvent. But not sure how you'd go about handling this.

Lets say I had a List and List.

Would you be able to Select a "NPC" and and "Item" from the lists and pass them to a listener when the Event is fired?

The system that I built at Schell Games does support passing data through an event, but the super-simplified version I presented does not have that. The main goal of the talk was to introduce the concept, not to distribute a complex implementation.




DeleteThat said, making an event that passes data isn't too tricky. You would need to define a NPCGameEvent : ScriptableObject and a NPCGameEventListener : MonoBehaviour. NPCGameEvent has a list of registered NPCGameEventListeners (and add/remove listener calls to populate it).

NPCGameEvent needs a .Raise(NPC npc) function that calls a .OnEventRaised(NPC npc) for each of the listeners. The OnEventRaised function can invoke a NPCUnityEvent if you want to hook up the response in the inspector.

To get fancier, you can implement most of this with generics to make it simpler to define new event arguments.

Thanks for the reply, I'll work on creating generic versions of the classes like you mentioned.


DeleteHow would you deal with events that need to be unique for each instance of the prefab? As an example DeathEvents for enemies where only the 1 instance of the enemy needs to respond to it.

ReplyDeleteThere are a few options:

Delete1. You could either have all enemies get the player death event and only have certain ones do anything in the response.

2. You could have enemies register with the event only when they have a reason to respond. For instance, when an enemy is aggro on the player they listen for the death event, when they de-aggro, they stop listening.

3. You could use a different system like c# events and have the enemy register with the player based on whatever conditions you are using to know if the enemy responds.

Thank you for answering. Would you use the same kind of options for communicating between different components on the same prefab? I know delegates are useful but I'm not sure if there is a better way to keep the systems decoupled. Not sure if I'm trying too hard to avoid direct references between scripts :P

DeleteI tend to not use my event system when communicating within a prefab. It is helpful to make sure things are modular and do not always need direct connections, but within a prefab, it is easy to see the connections.



DeleteWhen you do want to keep things modular, you can use UnityEvents for some simple communication between components for a small performance fee (but it is really flexible).

Another thing you can do is use interfaces. A component can scan for all other components that implement an interface and make calls on them.

Thank you so much for the advice. It's been really helpful for a relative newbie like me :)

DeleteThis comment has been removed by the author.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteI've watched your Unite talk, read this blog, and poked through the sample code. Thank you so much for this info. I have a couple questions now that I'm about halfway through implementing these concepts in my game:





ReplyDelete1. Do scriptable objects remove the need to save game data to a file on the users device? For example, the amount of coins a player has?

2. Is there an easy way to see all the listeners of an event? I have to click around my project to find them all now. I could manually keep track in a separate application but that seems tedious.

3. Do you have a state machine integrated with this type of event system? I have almost completely gotten rid of my "GameManager" class. One benefit of having that class was a clean state machine with state enter and exit methods. Now the state changes have been replaced with GameEvents. It's more decoupled, but feels a little fragile.

Thanks again!!

Replying to my own comment here...




Delete1. So while these assets are persisted between sessions, you will still want to save data somewhere else. If you push an update to your game, then everyone's scriptable object assets will be the same as what you pushed with.

2. So far I just go into the game event listener class and print out the object that is listening. Not the best solution but it's better than nothing.

3. I'm still not sure how to handle overall game state cleanly with so much modularity and with game events like these.

Never thought about using scriptable objects as anything other than a settings container. Great stuff!





ReplyDeleteOn the question of architecture, how do you apply your "everything's a prefab" philosophy to your overall state flow?

Take a baseball game with a batting phase, running phase, and pitching phase. Would you have a top down approach, like a state machine, waiting for a batter to hit and sending instructions to interfaces on prefabs that implement them, or would you have a loose group of components, like a "hit detector" that simply sends a message when a bat has a ball, and lets every other game object do what it does, changing the phase naturally?

Would your camera have various scripts and logic for each phase, or would your camera be dumb (zoom in/out) and have a camera controller prefab feeding it instructions based on the phase?

This comment has been removed by the author.

ReplyDeleteCan use this architecture with UNet ? (Both HLAPI and LLAPI)

ReplyDeleteSpectacular presentation! I work alone (literally: there's no one else here), so a good, clear, useful video like that one is invaluable. Kind of like having a colleague (who knows what he's doing).


ReplyDeleteRegarding the listener lists: do you think using C#'s built-in event system be adequate?

I just want to tell you than you for sharing ;)

ReplyDeleteIt is very nice approach. I also like the idea to move a lot of wok to the designers xD

Thanks for a presentation that was a real eye opener! I wish I new this a few years ago.

ReplyDeleteI am a solo developer but even so the ideas are also great for making objects undependable from singletons making debug and test scenes much more due-able!

However the event system seems very hard to debug when the project gets big in size. I understand that you developed custom debug routines for that.

As you cant share the source code. I would ask if its possible to give some pointers to point us in the right direction?

As you pointed out if we all would use this workflow it would be much easier to add extern components to an existing project. thanks gain!

I really loved reading your blog. It was very well authored and easy to understand. Unlike other blogs I have read which are really not that good.Thanks alot! architect

ReplyDeleteI have read your article; it is very informative and helpful for me. I admire the valuable information you offer in your articles. Thanks for posting it. town planning

ReplyDeleteWorth noting that you can replace lines 3-9 in the FloatVariable.cs (the file exert shown in the blog post above), with an AutoProperty, like:



ReplyDeletepublic float CurrentValue { get; set; }

Which creates a private field, and creates the get and set properties/functions/methods for it automatically (thus the name).

Need a change at Line 13 as well.


DeleteGreat framework examples, many thanks. One little thing, when you run the Demo_05 scene the EnabledThings set is full of "Type mismatch" objects.

ReplyDeleteyeah, me too.

DeleteI downloaded the git project exactly because I have the same issue in my project hoping this would give me a hint but, it seems the problem is the same in the "Sets" scene demo on your git repo...

any idea ?

I have two doubts that have been emerging at the time of implementing this architecture:




ReplyDelete1. How do I handle cases of collisions that need values of the collided object? Example: Pickable Items, power ups, etc.

2. I have a solution (not optimized at all) for this question but I would like to know your opinion: How to manage situations in narrative games where there are a series of linear/semilinear events?

Thank you very much for that great talk, it is helping me a lot to improve.

I know this post is old but I have a question: a lot of time what I need to do is get the player position so should I make a Vector3Variable and a Vector3Reference (or maybe a TransformVariable)?

ReplyDeleteThose would both work fine. The pattern Ryan describes is easily extensible to other types. Of course, you could also create a Vector3Reference that stored three FloatVariable objects too. I would suggest you try your options in a series of small experiments and see what feels like the best fit to your needs.


DeleteAlso, this would be a great question to take up in the Unity C# Scripting forum. You'll get a lot of help there: https://forum.unity.com/forums/scripting.12/

Thanks for replying! Just made a forum post https://forum.unity.com/threads/scriptable-objects-pattern-for-players-position.1008790/

DeleteHi Ryan.

ReplyDeleteYour talk is amazing and is certainly reaching gospel status.

I see little activity here two years after the talk but I can't find any info anywhere.

I am calling addresables scenes in additive mode from a remote existing build.

When I raise () the event from the "EventEditor" button that you included in the repository, or from any other Unity Events trigger, everything works great. But if I try to Raise() the event directly from code, it doesn't work. It seems very strange to me. I do not know what I am missing or if we are facing a engine limitation. At same time, if I Raise() the event from code for a scene that it is not in a remote existing build ... it also works. It is not weird? If is addressable related why it works through the button trigger?

One week later I don't know where else to look.

Cheers,

Joan

Hi Joan, I have run into similar issues with scriptable-objects and addressables myself. I think your issue will likely be due to addressables/bundles. In my case, I found it was calling the methods on a new 'instance' of the SO, not the original asset. So I had to get access to the asset (loaded it up via addressables and stored a reference to it) - then I called all my methods via this stored reference.

DeleteIt was a pain, but it got it all working :)

I hope this helps your project too!

Hi Dinner.

ReplyDeleteThanks for aswering.

You was right. I passed everything to addressables scenes and removed all the scripts from the initial scene. Everything work fine when called from addressables to addressables.

You saved a developer from suicide :)

Thank you very much.

Hahaha, omg - happy to have saved a life 😂

DeleteI'm glad it helped!

The King Casino Company - Ventureberg

ReplyDeleteIt ventureberg.com/ was born in apr casino 1934. The titanium metal trim Company offers luxury hotels, If you don't have herzamanindir.com/ a poker room in your house, then you'll find a poker room https://febcasino.com/review/merit-casino/ in the