---
title: Why composition is often better than inheritance
url: http://joostdevblog.blogspot.com/2014/07/why-composition-is-often-better-than.html
author: Joost van Dongen
published: '2014-07-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*has a*cushion and a seat

*is a*piece of furniture. While in this example the difference is really obvious, there are in practice many cases where both could make sense. Does a character in a game

*have a*collision box, or

*is it*a collidable object? These are not the same, but each can be used as the main structure for collision handling (or even both together) and it is not always clear which is better. In my experience intuition often favours inheritance, but it gives so many problems that in many cases composition is better.

Let's first have a look at an example of how the same problem can often be solved in both ways. In

[Awesomenauts](http://www.awesomenauts.com)we have a separate class that handles the 'physics' of a character. This class handles things like gravity, knockback, sliding and jumping. Since a character

*is a*physics object, it would make sense to say that Character inherits from PhysicsObject. It is also possible to say that a character

*has a*PhysicsObject that handles its collision. Instead of

*has a*we might also word this as

*uses a*.

![](../../assets/03b689e8fe117869.gif)

Let's see what this relation would look like in code. This is a highly simplified version, but it shows the basic concepts nicely:

class PhysicsObject { Vector2D position; void updatePhysics(); void applyKnockback(Vector2D force); Vector2D getPosition() const; }; //Using PhysicsObject through inheritance class CharacterInheritance: PhysicsObject { void update() { updatePhysics(); } }; //Using PhysicsObject through composition class CharacterComposition { PhysicsObject physicsObject; void update() { physicsObject.updatePhysics(); } void applyKnockback(Vector2D force) { physicsObject.applyKnockback(force); } void getPosition() const { return physicsObject.getPosition(); } }; |

As you can see in this code, CharacterInheritance is shorter. It also feels more natural, since we don't have to write these extra accessor functions for

*applyKnockback*and

*getPosition*. However, after years of creating both of these kinds of structures I have learned that in a situation like this, using composition is actually more flexible, less sensitive to bugs and even more understandable than using inheritance.

**Flexibility**

Let's start with the flexibility argument. What if we want to make an enemy that consists of two blocks linked by an energy chain. This enemy does damage to anyone who touches the chain. The blocks can move separately, making for some interesting positional gameplay when fighting this enemy. The two blocks this object consists of move entirely separately and each have their own physics. Knocking back one block does not influence the other block. Yet they really are one character: they have one healthbar, one AI, one entry on the minimap and can only exist together.

![](http://www.proun-game.com/Oogst3D/BLOG/Inheritance%20versus%20composition%20-%20Enemy.gif)

With a composition structure it would be pretty straightforward to create this enemy, since we could just create a character that has several PhysicsObjects. With inheritance however we cannot make this as a single character, since we cannot inherit from PhysicsObject twice. We could probably work around this somehow and make it work with inheritance, but it quickly becomes much less simple and intuitive.

If you read this and think this is a far-fetched situation and not all that relevant, then you have probably never been in a project of significant size where gameplay was king. Game designers constantly come up with game mechanics that are exceptions to what you already programmed. Saying no to these just because your code structure cannot handle them will seriously damage your game quality, since in the end the only argument should be whether it is

*fun to play*(okay, and maybe whether it is achievable within the scope of the project).

Just take a look at the diversity of the hundreds of upgrades in Awesomenauts and you will realise how many of those were likely exceptions to what our code could do. Our designers came up with those upgrades and the code had to make it work somehow. An important goal in game programming is flexibility: making your code in such a way that it is relatively easy to add whatever weird whim the game designers come up with today. In most cases composition is much more flexible than inheritance.

**Readability**

My next argument against inheritance is readability. "Readability" is always accomponied by "sensitivity to bugs", since if a programmer does not really understand how something works, then he will likely break it when working on it.

At

[Ronimo](http://www.ronimo-games.com)one of the more important rules in our coding standard is that we strive to keep the size of all classes below 500 lines of code. We don't always see ways to keep to that, but the goal is clear: keep classes relatively short so that they are easy to understand and a programmer can fit the workings of the entire class in his head.

Let's say our code has grown over time as more and more features were added to our game, and Character and PhysicsObject have both grown to 500 lines of code each. We have also added two more classes that use PhysicsObject: Pickup and Projectile. These are also 500 lines of code each.

![](../../assets/e0d4c6a177af34e2.gif)

In such a situation inheritance will usually make all of this very confusing. We might have strived to keep as much

*private*as possible, but in the end inheritance almost always introduces a bunch of

*virtual*and

*protected*functions. In other words: PhysicsObject has become pretty intertwined with its three child classes Character, Pickup and Projectile. In my experience this nearly always happens: inherited classes work together to create complex behaviour and intertwine more and more over time.

By itself this might not be that much of a problem, but to really understand any of these classes we now need to know them all. If we restructure something in PhysicsObject because Projectile needs a new feature, then Character and Pickup will also be involved. To understand the entire situation, the programmer now needs to think about four different classes and fit all 2000 lines of code in her head simultaneously. In my experience this quickly becomes impossible: this is just too much code to really grasp it all at once without starting to mix things up. The result is that readability decreases and the programmer becomes more likely to introduce bugs because she overlooked something.

Of course a composition based structure does not magically fix all of this, but it does help a lot in keeping this structure simple and understandable. With composition there is no

*virtual*or

*protected*, so the separation between PhysicsObject on the one side and Character, Projectile and Pickup on the other is much clearer. This keeps the classes from intertwining over time and makes it easier to keep them truly separate. While they could in theory also have been kept separate with inheritance, in my experience this is too difficult to maintain, while composition enforces it. We have numerous cases in our code where an inheritance structure of classes that all grew too big is hardly understandable any more.

**Diamond problem**

Any discussion of inheritance versus composition is incomplete without mentioning the famous

*diamond problem*. What happens when a class A inherits from two classes B and C that both inherit from a single parent D? A now has a D twice and chaos ensues.

![](http://www.proun-game.com/Oogst3D/BLOG/Inheritance%20versus%20composition%20-%20Diamond.gif)

There are several solutions to the diamond problem in C++. For example, you might just accept that A has double D. (Haha, double D! Ahum.) Or you might use

*virtual inheritance*to solve it. However, both solutions cause all kinds of problems and potential bugs, so just avoiding the diamond problem altogether is highly preferable.

This problem is usually not around in the initial design of a gameplay code structure, but as features are added it might pop up occasionally. The problem is that when it does, it can often be very difficult to come up with a good solution for how to get rid of it without doing a lot of refactoring.

Nevertheless, the diamond problem has only popped up a couple of times in my 12 years of object oriented programming, so I don't think the diamond problem is a very strong argument against inheritance.

(By the way, even without the diamond problem complex multiple inheritance structures tend to get a little sleazy, as I explained in this previous blogpost about

[why](http://joostdevblog.blogspot.nl/2013/03/hardcore-c-why-this-sometimes-doesnt.html).)

*this*is not always*this***Use inheritance, but use it less**

Does all of this mean that I am against inheritance in general? Nope, absolutely not! Inheritance is very useful for a lot things, for example in polymorphism and in design patters like listeners and factories. My point is just that inheritance is not as generally useful as it might seem. There are lots of cases where inheritance may seem the cleanest solution, while in practice composition would be better. So use inheritance, but don't overuse it.

Great post, I agree to all that is said :D I actually came across the diamond problem during my graduation, but never really knew it had a name!



ReplyDeleteIn my case I had a base class DataObject, and a Renderable and Updatable class. Both the Renderable and Updatable should inherit from the DataObject to be removed from memory when marked for removal.. but as other classes usually extend both Updatable and Renderable this didn't feel quiet right. What I eventually did was not extending the Renderable and Updatable from the DataObject, but made other's extend from all 3 of these classes.

Still didn't feel really pretty though..

I share same thoughts. Composition is more often than not lead me to a clean solution. By the way, I have also shared my 2 cents on Why composition is better than Inheritance in Java, Java developers may find it useful.

DeleteI learned from your article, Javin.

DeleteGood to hear that Noumenon :)

DeleteOne thing I'd add is that composition also provides some greater flexibility when it comes to unit testing, via the ability to inject mock implementations of the composition objects/interfaces.


ReplyDeleteI've found when it comes to maintaining a complex code base the ability to unit test with mock implementations has proven invaluable.

Goof point! Writing unit tests gives you a great perspective on your code. If it is flexible the test can be written very fast. With complicated hierarchies and code structures it can be painful.


DeleteRegarding the whole post: I like the summary "Use inheritance, but use it less".

Looking at Unity (which i praise for their design). Only use inheritance, if and only if a class will 'always' inherit from the inherited class.







ReplyDeleteFor instance a BoxCollider inherits Collider inherits UnityObject inherits System.Object.

But gameplay-like things such as characters that inherit a physics object may be useful for game A but not in game B where no collision exists at all.

Therefore, to keep an abstract system unity works entirely with components.

The core object is a GameObject, it has always a Transform component (rotation, scale, translation) and a pointer to a renderer component, a collider, a camera, a text mesh, a network view, an animator, an animation, a audio, a guitext, a etc...

Using this method, the gameobject can be extended in any way desirable and one does not have to know anything about the upper laying gameplay, therefore any game built on top will suffice this design.

In fact, a script is also a component, and an unspecified amount of scripts can be attached to a game object just as any other component. This is a cool thing because one can use script components to avoid duplication of script code rather than functions. In practice a combination of both works best, but a function in code can be seen as a component to a gameobject as well.

For example, a piece of code that makes a camera look at a other game object can be used as a different component. By adding or removing this script component from a gameobject it will start/stop looking at some other object.

I couldn't agree more. I frequently have to explain this topic to both experience developers and fresh college grads. I wish they'd stop playing up inheritance in curriculum (*cough* I'm looking at you Java schools).

ReplyDeleteThis was a very good read. Thank you for putting this together.

ReplyDeleteYet another great post! Love the additional clarity given with the diagrams as well. :)

ReplyDeleteEvery time I read one of your posts I get seriously brainfucked. But I also learn a lot, so thanks for sharing your wisdom, Mr. Joost.

ReplyDeleteI can't make up my mind whether that is a compliment or an insult... ;)

Delete