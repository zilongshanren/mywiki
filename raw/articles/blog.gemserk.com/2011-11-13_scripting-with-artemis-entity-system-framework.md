---
title: Scripting with Artemis Entity System Framework
url: https://blog.gemserk.com/2011/11/13/scripting-with-artemis/
published: '2011-11-13'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

[Artemis](http://gamadu.com/artemis/) is a component based entity system framework made in Java by Arni Arent (appel) and Tiago Costa (spiegel).

The core of Artemis is small and it is based on four main concepts. The **Component**, where all information about an Entity is stored. The **Entity**, which represents a game object. The **EntitySystem**, where custom logic, for entities with one or more component, is processed. And finally the **World**, where Entities and EntitySystems live. The idea is to grow over those concepts by making your own Components and EntitySystems.

### The problem

There are some cases where it depends a lot how are you using Artemis, to feel it is helping you or not. For example, when you want an Entity to have some custom behavior on a specific level you could follow the next approach.

First, create an SpecificBehaviorForLevelComponent to declare that an Entity with that component will have that custom behavior and then create the SpecificBehaviorForLevelSystem which performs the logic.

The problem with this approach is that you will have an empty Component used only as a mark to let the EntitySystem work over it. Also, you will have an EntitySystem that will perform logic only in a specific moment of the game and then it will be useless.

If you have to create more than just one custom behavior, then you are a bit doomed and you will hate Artemis. However, it is not Artemis, or any component based entity framework, fault.

### Script Framework, a possible solution

To simplify working with cases like the one mentioned before, we created a scripting framework over Artemis, composed by three main concepts: the **Script**, the **ScriptComponent** and the **ScriptSystem**.

#### Script

This is an interface which provides the following three methods:

- init(world, entity) : called once when the entity enters the world.
- update(world, entity) : called in each world update
- dispose(world, entity) : called once when the entity leaves the world.

It should be implemented and added to the ScriptComponent of an Entity in order to perform the behavior.

#### ScriptComponent

This is an Artemis Component which contains a collection of Scripts and it is used by the ScriptSystem in order to know which Scripts to process on each Entity.

#### ScriptSystem

This is an Artemis EntitySystem responsible of calling, for each Entity, the init/update/dispose methods of each Script declared in the ScriptComponent of that Entity.

For the previous example, where we wanted a specific behavior for an entity in one level, we could create a SpecificBehaviorForLevelScript and, when loading that level, add that script to the ScriptComponent. So, instead creating Components and EntitySystems, we can create only Scripts.

**Pros**

- Clear and simple API.
- Easy to add/remove a Script vs add/remove a System.
- Scripts are easily reusable (when you want two or more entities with a custom behavior).
- Logic localized in one place.
- Allow different implementations of the Script interface, for example, a Groovy implementation.

**Cons**

- Not good for global stuff like rendering, an EntitySystem keeps being better for those cases.
- Hard to know the right balance between which code should be on Scripts and which one on Systems.

### Conclusion

The Script Framework is some point in the middle between Entities with no logic at all and Entities with all the logic. It should be used with care, learning to balance which code should be on Scripts and which code on Systems is not easy.

Artemis is only a **small core**, a **foundation of classes** to work with. The real power comes from the custom Components and Systems you create over it. For example, in our case we created several Systems that we reuse between games, some of them are the RenderSystem responsible of rendering the entities with the RenderComponent using libGDX and the PhysicsSystem responsible of processing the Box2d world.

### References

There are a lot of resources about components based entity systems, however the best/correct solution between all these references is not so clear.

- Artemis Entity System -
[http://gamadu.com/artemis/](http://gamadu.com/artemis/) - Slick Forums - topic - Artemis Entity System Framework -
[http://slick.javaunlimited.net/viewtopic.php?f=10&t=3076](http://slick.javaunlimited.net/viewtopic.php?f=10&t=3076) - Entity/Component Game Design That Works: The Artemis Framework -
[http://piemaster.net/2011/07/entity-component-artemis/](http://piemaster.net/2011/07/entity-component-artemis/) - PushButton Engine -
[http://pushbuttonengine.com/](http://pushbuttonengine.com/) - Entity System: RDBMS-beta (a new example with source) - T-machine -
[http://t-machine.org/index.php/2011/08/22/entity-system-rdbms-beta-a-new-example-with-source/](http://t-machine.org/index.php/2011/08/22/entity-system-rdbms-beta-a-new-example-with-source/) - Evolve your hierarchy - Cowboy Programming -
[http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/](http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/) - Game Objects 1 - Game Architect -
[http://gamearchitect.net/Articles/GameObjects1.html](http://gamearchitect.net/Articles/GameObjects1.html) - Data-Driven Design - Game Architect -
[http://gamearchitect.net/Articles/DataDrivenDesign.html](http://gamearchitect.net/Articles/DataDrivenDesign.html) - Entity Systems - Tom Davies -
[http://www.tomseysdavies.com/2011/01/23/entity-systems/](http://www.tomseysdavies.com/2011/01/23/entity-systems/) - Writing Reusable Code - Games From Within -
[http://gamesfromwithin.com/writing-reusable-code](http://gamesfromwithin.com/writing-reusable-code) - Data Oriented Design now and in the future - Games From Within -
[http://gamesfromwithin.com/data-oriented-design-now-and-in-the-future](http://gamesfromwithin.com/data-oriented-design-now-and-in-the-future) - Scott Bilas Game Objects -
[http://scottbilas.com/files/2002/gdc_san_jose/game_objects_slides.ppt](http://scottbilas.com/files/2002/gdc_san_jose/game_objects_slides.ppt)

Hope you like it.