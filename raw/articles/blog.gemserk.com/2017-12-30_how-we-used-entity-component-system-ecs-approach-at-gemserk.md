---
title: How we used Entity Component System (ECS) approach at Gemserk - 2/2
url: https://blog.gemserk.com/2017/12/30/how-we-used-entity-component-system-ecs-approach-at-gemserk-22/
published: '2017-12-30'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

So, after [our first attempt on using ECS](https://blog.gemserk.com/2017/12/27/how-we-used-entity-component-system-ecs-approach-at-gemserk-12/), when we started to develop mobile games and moved to the [LibGDX](https://libgdx.badlogicgames.com/) framework, we decided to abandon our ComponentsEngine and start over.

We were [still reading about ECS](http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/) while we were creating our [set of tools and code](https://github.com/gemserk/commons-gdx) over LibGDX. At some point in time, some of the Java community developers started [Artemis](https://github.com/gemserk/artemis/tree/gemserk), a lightweight ECS, and we decided to give it a try.

# Artemis

This is a simplified core architecture diagram:

![](../../assets/19a0550dac5adfa6.png)


*Note: we used a modified version of Artemis with some additions like enable/disable an Entity.*

In this pure approach, Entities and Components are just data, and they are related by identifiers, like these tables in a relational database:

![](../../assets/3464c30b532057a1.png)


Where we have two entities, both with a PositionComponent and only one of them with MovementComponent.

An example of this components in code:

```
public class PositionComponent : Component {
public float x, y;
}
public class MovementComponent: Component {
public float speed;
}
```


EntitySystems perform the game logic. They normally work on a subset of Components from an Entity but they could need it in order to enable/disable/destroy it (if it is part of its logic).

An example of a System is [LimitLinearVelocitySystem](https://raw.githubusercontent.com/gemserk/commons-gdx/master/commons-gdx-artemis/src/main/java/com/gemserk/commons/artemis/systems/LimitLinearVelocitySystem.java), used in multiple of our games to limit the physics velocity of an Entity with PhysicsComponent and LimitVelocityLimitComponent:

```
public void process(Entity e) {
PhysicsComponent physicsComponent =
Components.getPhysicsComponent(e);
Body body = physicsComponent.getPhysics().getBody();
LinearVelocityLimitComponent limitComponent =
e.getComponent(LinearVelocityLimitComponent.class);
Vector2 linearVelocity = body.getLinearVelocity();
float speed = linearVelocity.len();
float maxSpeed = limitComponent.getLimit();
if (speed > maxSpeed) {
float factor = maxSpeed / speed;
linearVelocity.mul(factor);
body.setLinearVelocity(linearVelocity);
}
}
```


There are some extra classes like the TagManager which allows assigning a unique string identifier to an Entity in order to find it, and the GroupManager which allows adding entities to groups identified by a name, which is more like how tags are used everywhere else.

Even though it could look similar to our ComponentsEngine where the Properties in that engine correspond to the Components in this one, and Components to Systems, there is an important difference: Systems are not part of an Entity and work horizontally over all entities with specific Components (data). So, in this approach, changing only data from entities indeed change their behaviour in the game, so it is really data driven.

Since Entities and Components are just data, their instances in memory are easier to reuse. An Entity is just an id, so it is obvious. A Component is a set of data that doesn’t care too much which Entity it belongs to. So, after the Entity doesn’t need it anymore, it could be reused elsewhere, improving a lot memory usage and garbage collection.

Artemis, and other pure ECS implementations, are really lightweight and performant frameworks. The real power comes from the Systems and Components built over them. In our case, we created a lot of Systems that we started to reuse between games, from [SuperFlyingThing](https://github.com/gemserk/superflyingthing) to VampireRunner and even in Clash of the Olympians.

## Scripting

One of the most interesting ones is the [Scripting framework we created over Artemis.](https://blog.gemserk.com/2011/11/13/scripting-with-artemis/) It was really useful and gave us a lot of power to overcome some of the limitations we were facing with the pure approach when we need to create a specific logic for a specific moment during the game and (probably) never again and we didn’t want a System for that.

They work similar to Unity MonoBehaviours and our logic Components from ComponentsEngine, and they also belong to the Entity lifecycle. One difference, however, is that they try to avoid storing data in their instances as much as possible and instead try to store and read data from Components, like Systems do.

Here is an example Script from one of our games:

```
public class MovementScript extends ScriptJavaImpl {
@Override
public void update(World world, Entity e) {
MovementComponent movementComponent = Components.getMovementComponent(e);
SpatialComponent spatialComponent = Components.getSpatialComponent(e);
ControllerComponent controllerComponent = Components.getControllerComponent(e);
Controller controller = controllerComponent.controller;
Movement movement = movementComponent.getMovement();
Spatial spatial = spatialComponent.getSpatial();
float rotationAngle = controllerComponent.rotationSpeed * GlobalTime.getDelta();
Vector2 linearVelocity = movement.getLinearVelocity();
if (controller.left) {
spatial.setAngle(spatial.getAngle() + rotationAngle);
linearVelocity.rotate(rotationAngle);
} else if (controller.right) {
spatial.setAngle(spatial.getAngle() - rotationAngle);
linearVelocity.rotate(-rotationAngle);
}
}
}
```


*Note: GlobalTime.getDelta() is similar to Unity’s Time API.*

One problem about the Scripting framework is that it is not always clear when some logic should be in a Script or a System, and that made reusability a bit harder. In the case of the example above, it is obvious it should be moved to a System.

## Templates

Another useful thing we did over Artemis was [using templates to build entities](https://github.com/gemserk/commons-gdx/blob/master/commons-gdx-artemis/src/main/java/com/gemserk/commons/artemis/templates/EntityTemplate.java) in a specific way, similar to what we had in ComponentsEngine.

We used also a concept of Parameters in templates in order to customize parts of them. Similar to ComponentsEngine, templates could apply other templates and different templates could be applied to the same Entity.

Here is an example of an Entity template:

```
public void apply(Entity entity) {
String id = parameters.get("id");
String targetPortalId = parameters.get("targetPortalId");
String spriteId = parameters.get("sprite", "PortalSprite");
Spatial spatial = parameters.get("spatial");
Script script = parameters.get("script", new PortalScript());
Sprite sprite = resourceManager.getResourceValue(spriteId);
entity.addComponent(new TagComponent(id));
entity.addComponent(new SpriteComponent(sprite, Colors.darkBlue));
entity.addComponent(new Components.PortalComponent(targetPortalId, spatial.getAngle()));
entity.addComponent(new RenderableComponent(-5));
entity.addComponent(new SpatialComponent(spatial));
entity.addComponent(new ScriptComponent(script));
Body body = bodyBuilder //
.fixture(bodyBuilder.fixtureDefBuilder() //
.circleShape(spatial.getWidth() * 0.35f) //
.categoryBits(CategoryBits.ObstacleCategoryBits) //
.maskBits((short) (CategoryBits.AllCategoryBits & ~CategoryBits.ObstacleCategoryBits)) //
.sensor()) //
.position(spatial.getX(), spatial.getY()) //
.mass(1f) //
.type(BodyType.StaticBody) //
.userData(entity) //
.build();
entity.addComponent(new PhysicsComponent(new PhysicsImpl(body)));
}
```


That template configures a Portal entity in SuperFlyingThing which teleports the main ship from one place to another. [Click here](https://github.com/gemserk/superflyingthing/tree/master/superflyingthing-core/src/main/java/com/gemserk/games/superflyingthing/templates) for the list of templates used in that game.

## Interacting with other systems

Sometimes you already have a solution for something, like the physics engine, and you want to integrate it with the ECS. [The way we found](https://blog.gemserk.com/2012/02/02/how-we-use-box2d-with-artemis/) was to create a way to synchronize data from that system to the ECS and vice versa, sometimes having to replicate a bit of data in order to have it easier for the game to use it.

# Finally

Even though we had to do some modifications and we know it could still be improved, we loved using a pure ECS in the way we did.

It was used to build different kind of games/prototypes and even a full game like the [Clash of the Olympians](https://blog.gemserk.com/2013/01/05/clash-of-the-olympians-for-android/) for mobile devices, and it worked pretty well.

# What about now?

Right now we are not using any of this in Unity. However we never lost interest nor feith in ECS, and there are starting to appear new solutions over Unity in the last years that caught our attention. [Entitas](https://github.com/sschmid/Entitas-CSharp) is one of them. The Unity team is working towards this path too as shown in this [video](https://www.youtube.com/watch?v=tGmnZdY5Y-E). Someone who din’t want to wait started [implementing that solution](https://github.com/Spy-Shifty/BrokenBricksECS) in his own way. We’ve also watched some Unite and GDC talks about using this approach in big games and some of them even have a Scripting layer too, which is awesome since, in some way, it validates we weren’t so wrong ;).

I am exited to try ECS approach again in the near future. I believe it could be a really good foundation for multiplayer games and that is something I’m really interested in doing at some point in my life.

Thanks for reading.

# References

[A mini tutorial on how to use Artemis](https://github.com/gemserk/artemis/wiki/Mini-Tutorial).- The source code of
[Artemis + our modifications](https://github.com/gemserk/artemis/tree/gemserk). - A blog post on the
[enable/disable](https://blog.gemserk.com/2012/01/03/reusing-artemis-entities-by-enabling-disabling-and-storing-them/)addition over Artemis. - A blog post explaining our
[Scripting framework over Artemis](https://blog.gemserk.com/2011/11/13/scripting-with-artemis/). - How we managed to use external data like
[box2d physics inside the Artemis](https://blog.gemserk.com/2012/02/02/how-we-use-box2d-with-artemis/). - All
[our code over artemis](https://github.com/gemserk/commons-gdx/tree/master/commons-gdx-artemis), like the Systems used in different games. [Example components](https://github.com/gemserk/superflyingthing/blob/master/superflyingthing-core/src/main/java/com/gemserk/games/superflyingthing/components/Components.java)used in SuperFlyingThing game.[Example systems](https://github.com/gemserk/commons-gdx/tree/master/commons-gdx-artemis/src/main/java/com/gemserk/commons/artemis/systems)we reused among different games.[The first](http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/)of a serie of great articles about ECS.[A website explaining Artemis](http://entity-systems.wikidot.com/artemis-entity-system-framework).