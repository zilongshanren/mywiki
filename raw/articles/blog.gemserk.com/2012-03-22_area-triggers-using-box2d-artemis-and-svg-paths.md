---
title: Area triggers using Box2D, Artemis and SVG paths
url: https://blog.gemserk.com/2012/03/22/area-triggers-using-box2d-artemis-and-svg-paths/
published: '2012-03-22'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As we explained in previous posts, we are [using Inkscape to design the levels](https://blog.gemserk.com/2011/05/03/using-inkscape-as-scene-editor/) of some of our games, in particular, our current project. In this post we want to share how we are making area triggers using Box2D sensor bodies, Artemis and SVG paths.

### What is an area trigger

When we say area trigger we mean something that should be triggered, an event for example, when an entity/game object enters the area, to perform custom logic, for example, ending the game or showing a message. Some game engines provides this kind of stuff, for example Unity3d with its [Collider](http://unity3d.com/support/documentation/ScriptReference/Collider.html) class and different events like OnTriggerEnter.

### Building an area trigger in Inkscape

Basically, we use SVG paths with [custom XML data](https://blog.gemserk.com/2011/04/28/archers-vs-zombies-dev-log-03/) to define the area trigger to later parse it by the game level loader to create the corresponding game entities. The following screen shot shows an example of an area defined using Inkscape:

Right now, we are exporting two values with the SVG path, the event we want to fire identified by the XML attribute named eventId, and extra data for that event identified by the XML attribute eventData. For example, for our current game we use the eventId `showTutorial`

with a text we want to share with the player on eventData attribute like `"Welcome to the training grounds"`

. The following example shows the XML data added to the SVG path:

<path id="path4187" eventId="showTutorial" eventData="We will start by learning how the ship moves..." d="m 4.242641,5927.8761 482.246829,0 0,-205.0609 -489.3178971,-8.4853 z" />

The exported data may depend on your framework or game, so you should export whatever data you need instead.

### Defining the area trigger inside the game

Inside the game, we have to define a entity/game object for the area trigger. In the case of our current game, that entity is composed by a Box2D sensor body with a shape built using the SVG path and a Script with logic to perform when the main character collides it.

We use sensor bodies because they are mainly used to detect collisions but not to react to them by changing their angular and linear velocities. As we explained in a [previous post](https://blog.gemserk.com/2011/06/27/simplifying-building-bodies-and-joints-with-libgdx-box2d), we are using our custom builders to help when building Box2D bodies and fixtures. Our current body declaration looks like this:

Body body = bodyBuilder // .fixture(bodyBuilder.fixtureDefBuilder() // .polygonShape(vertices) // the vertices from the SVG path .categoryBits(Collisions.Triggers) // the collision category of this body .maskBits(Collisions.MainCharacter) // the collision mask .sensor() // ) // .position(0f, 0f) // .type(BodyType.StaticBody) // .angle(0f) // .userData(entity) // .build();

The previous code depends on specific stuff of the current game but it could be modified to be reused in other projects.

As we explained in another previous post, we are using a [basic scripting framework over Artemis](https://blog.gemserk.com/2011/11/13/scripting-with-artemis/). Our current script to detect the collision looks like this:

public static class TriggerWhenShipOverScript extends ScriptJavaImpl { private final String eventId; private final String eventData; EventManager eventManager; public TriggerWhenShipOverScript(String eventId, String eventData) { this.eventId = eventId; this.eventData = eventData; } @Override public void update(World world, Entity e) { PhysicsComponent physicsComponent = Components.getPhysicsComponent(e); Contacts contacts = physicsComponent.getContact(); if (contacts.isInContact()) { eventManager.submit(eventId, eventData); e.delete(); } } }

For the current game, we are testing this stuff for a way to communicate with the player by showing messages from time to time, for example, in a basic tutorial implementation. The next video shows an example of that working inside the game:

### Conclusion

The idea of the post is to share a common technique of triggering events when a game object enters an area, which is not framework dependent. So you could use the same technique using your own framework instead Box2D and Artemis, a custom level file format instead SVG and the editor of your choice instead Inkscape.

### References

- Custom XML data - </2011/04/28/archers-vs-zombies-dev-log-03/>
- Scripting with Artemis - </2011/11/13/scripting-with-artemis/>
- Simplifying building Box2D bodies and joints - </2011/06/27/simplifying-building-bodies-and-joints-with-libgdx-box2d>
- Unity3d Collider -
[http://unity3d.com/support/documentation/ScriptReference/Collider.html](http://unity3d.com/support/documentation/ScriptReference/Collider.html) - Using Inkscape as Scene Editor - </2011/05/03/using-inkscape-as-scene-editor/>