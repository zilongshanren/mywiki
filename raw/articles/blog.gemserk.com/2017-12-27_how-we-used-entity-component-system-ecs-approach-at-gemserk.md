---
title: How we used Entity Component System (ECS) approach at Gemserk - 1/2
url: https://blog.gemserk.com/2017/12/27/how-we-used-entity-component-system-ecs-approach-at-gemserk-12/
published: '2017-12-27'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

When we started Gemserk [eight years ago](https://blog.gemserk.com/2010/01/28/welcome/), we didn’t know which was the best way to make games. So before starting, we did some research. After reading some articles and presentations we were really interested in trying an Entity Component System (ECS) approach for our games. However, since we didn’t find a clear guide or implementation at that point we had to create our own solution while exploring and understanding it. We named our engine [ComponentsEngine.](https://github.com/gemserk/componentsengine)

# Components Engine

The following image shows a simplified core architecture diagram:

![](../../assets/20ba89e0d34c0d5d.png)


*Note: part of the design was inspired by a Flash ECS engine named PushButtonEngine.*

An Entity is just a holder of state and logic. In an ECS, anything can be an Entity, from an enemy ship to the concept of a player or even a file path to a level definition. It depends a lot on the game you are making and how you want to structure it.

A Property is part of the state of an Entity, like the health or the position in the world, anything that means something for the state of the game. It can be accessed and modified from outside.

Components perform logic updating one or more Properties to change the Entity state. A component could for example change the position of an Entity given a speed and a moving direction.

They normally communicate with each other either by modifying common Properties (when on the same Entity) or by sending and receiving Messages through a MessageDispatcher (when on the same or on different Entities). They just have to register a method to handle a message. In some way, this is pretty similar to using SendMessage() method in Unity and having the proper methods in the MonoBehaviours that need to react to those messages.

EntityTemplates are an easy way to define and build specific game entities, they just add Properties and Components (and more stuff) to make an Entity behave in one way or another.

For example, a ShipTemplate could add position, velocity and health properties and some components to perform movement and to process damage from bullet hits:

```
public void build() {
// ... more stuff
property("position", new Vector2f(0, 0));
property("direction", new Vector2f(1, 0));
property("speed", 5.0f);
property("currentHealth", 100.0f);
property("maxHealth", 100.0f);
component(new MovementComponent());
component(new HealthComponent());
}
```


An example of the MovementComponent:

```
public class MovementComponent() {
@EntityProperty
Vector2f position;
@EntityProperty
Vector2f direction;
@EntityProperty
Float speed;
@Handles
public void update(Message message) {
Property<Float> dt = message.getProperty("deltaTime");
position += direction * speed * dt.get();
}
}
```


EntityTemplates are similar to Unity Prefabs or Unreal Engine Blueprints, representing in some way a (not pure) Prototype pattern.

Some interesting stuff of our engine:

- We can apply multiple templates to the same Entity. In this way, we could add generic features, like motion for example, by applying common templates. So, we could do something like OrcTemplate.apply(e) to add the orc properties and components and then MovableTemplate.apply(e), so now we have an Orc that moves.
- Templates can apply other templates inside them. So we could do the same as before but inside OrcTemplate, we could apply MovableTemplate there. Or even use this to create specific templates, like OrcBossTemplate which is an Orc with a special ability.
- Entities have also tags which are defined when applying a template too and are used to quickly identify entities of interest. For example, if we want to identify all bullets in the game, we could add the tag “Bullet” during the Entity creation and then, when processing a special power, we get all the bullets in the scene and make them explode.
*Note: in some ECS a “flag” component is used for this purpose.* - The Property abstraction is really powerful, it can be implemented in any way, for example, an expression property like “my current health is my speed * 2”. We used that while prototyping.

Some bad stuff:

- Execution speed wasn’t good, we had a lot of layers in the middle, a lot of reflection, send and receive messages (even for the update method), a lot of boxing and unboxing, etc. It worked ok in desktop but wasn’t a viable solution for mobile devices.
- The logic started to be distributed all around and it wasn’t easy to reuse, and we started to have tons of special cases, when we couldn’t reuse something we simply copy-pasted and changed it.
- There was a lot of code in the Components to get/set properties instead of just doing the important logic.
- Indirection in Properties code was powerful but we end up with stuff like this (and we didn’t like it since it was too much code overhead):

`e.getProperty("key").value = e.getProperty("key").value + 1.`


- We didn’t manage to have a good data driven approach which is one of the best points of ECS. In order to have different behaviours we were forced to add both properties, components and even tags instead of just changing data.

*Note: Some of these points can be improved but we never worked on that.*

Even though we don’t think the achitecture is bad, it guided us to do stuff in a way we didn’t like it and didn’t scale. We feel that Unity does the same thing with its GameObjects and MonoBehaviours, all the examples in their documentation go in that direction.

That was our first try to the ECS approach. In case you are interested, [ComponentsEngine](https://github.com/gemserk/componentsengine) and [all the games we did](https://github.com/gemserk/componentsengine-games) with it are on Github and even though they are probably not compiling, they could be used as reference.

This post will continue with how we later transitioned to use a more pure approach with [Artemis](https://github.com/gemserk/artemis), when we were more dedicated to mobile games.

# References

[Evolve your hierarchy](http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/) - Classic article about Entity Component System.

[PushButtonEngine](https://github.com/PushButtonLabs/PushButtonEngine/tree/master) - Flash Entity Component System we used as reference when developing our ComponentsEngine.

[Game architecture is different](http://www.richardlord.net/presentations/game-architecture-is-different.html) - A quick transformation from normal game architecture to ECS.

[Slick2D](http://slick.ninjacave.com/) - The game library we were using during ComponentsEngine development.