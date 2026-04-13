---
title: How we use Box2D with Artemis
url: https://blog.gemserk.com/2012/02/02/how-we-use-box2d-with-artemis/
published: '2012-02-02'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As you may know from our previous posts or from your personal knowledge (obviously), Box2D is a 2D physics engine and Artemis is an Entity System Framework. Box2D is used to add physics behavior to games however it could be used only to detect collisions if you want (that means no dynamic behavior). In this post, we want to share a bit how we are using both frameworks together.

### Introduction

The main idea is to react to physics events, like two bodies colliding, to perform some game logic. For example, whenever the main character ship touches an asteroid, it explodes.

When you use Artemis, the game logic is done in an Artemis System or a Script (custom), if you use our customization. The ideal situation would be if you could check in your game logic which entities are in contact or not. In order to make that work, you have to find a way to link a Box2D contact with an Artemis Entity and vice versa.

### Our solution

The first thing we do is, to each Artemis Entity we want to have a physics behavior, we add a PhysicsComponent the Box2D Body of the Entity and a Contacts instance where all the Box2D contacts for that Body are stored. Also, in order to get the Entity from the Body, we set the its userData pointing to the Entity.

The Contacts concept gives us useful methods to get information about contacts and the API looks like this:

getContactsCount() : int - returns the contacts quantity getContact(index: int) : Contact - returns the contact information

And our Contact concept API, returned by the Contacts getContact() method, looks like this:

getMyFixture() : Fixture - returns the fixture in contact of the Contacts owner Entity. getOtherFixture() : Fixture - returns the fixture of the other Entity. getNormal() : Vector2 - returns the normal of the contact.

(note: we decided to make a deep copy of the contacts information since it is recommended in the [Box2D manual](http://www.box2d.org/manual.html#_Toc258082975) if you use a ContactsListener)

Then, we have a ContactsListener (named PhysicsListener) which, whenever a contact is reported (begin or end), it gets the bodies from the contact and gets the entities from each body userData and then adds or removes the contact data to/from each Entity’s PhysicsComponent using its Contacts instance.

(note: we decided to use a custom ContactListener since it is recommended in the [Box2D manual](http://www.box2d.org/manual.html#_Toc258082975))

Finally, in each Artemis System or Script, we use the Entity’s PhysicsComponent to get the contacts data and we proceed to do the logic we want, for example, destroy the character or enable some special ability, etc.

Here is an example of how we use it inside a Script from our Leave me Alone game:

public void update(World world, Entity e) { PhysicsComponent physicsComponent = Components.getPhysicsComponent(e); Contacts contacts = physicsComponent.getContact(); if (!contacts.isInContact()) return; boolean shouldExplode = false; for (int i = 0; i < contacts.getContactCount(); i++) { Contact contact = contacts.getContact(i); Entity otherEntity = (Entity) contact.getOtherFixture().getBody().getUserData(); GroupComponent groupComponent = Components.getGroupComponent(otherEntity); if (groupComponent == null) continue; if (groupComponent.group.equals(Groups.EnemyCharacter)) { shouldExplode= true; break; } } if (shouldExplode) eventManager.dispatch(Events.MainExploded, e); }

If you use Box2D and you are starting to use Artemis or vice versa, hope this post could help you. Otherwise, I hope you like it.

Also, if you use Artemis with Box2D in another way, would be great to have your point of view.

Thanks.