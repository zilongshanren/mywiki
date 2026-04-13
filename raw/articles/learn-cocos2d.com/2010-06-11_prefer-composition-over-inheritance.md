---
title: Prefer Composition over Inheritance
url: http://www.learn-cocos2d.com/2010/06/prefer-composition-inheritance/
author: Blenderificus says
published: '2010-06-11'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

When the question came up [whether to subclass CCSprite or use some model class to build your game entity hierarchy](http://www.cocos2d-iphone.org/forum/topic/6621) in the cocos2d forum, i stressed that one should try not to use inheritance and keep the inheritance hierarchy to as few levels as possible. I’ve worked with codebases with hundreds of thousands of lines of code, and hundreds of different types of actors in the world. Yet the inheritance hierarchy was 2 super (parent) classes for almost all objects, only very few game objects had 3 or 4 super classes. How can you make complex games this way?

The answer lies in composition, often referred to as Game Components by engines like [TorqueX](http://www.torquepowered.com/products/torquex-3d) and the [PushButton Engine](http://pushbuttonengine.com/) (a Flash game engine from the original Torque developers). This video from the PushButton lead developer Ben Garney explains it very well and also illustrates the problem with inheritance over-use in game engines. Something that most developers new to object-oriented and/or game programming do in fact tend to over-use - i blame that on poorly written books and other introductory OOP sources which emphasize inheritance without discussing its disadvantages.

You can read more about [PushButton’s Components system in their documentation](http://pushbuttonengine.com/docs/04-Components.html). How they implemented [Components in TorqueX and what the differences are to XNA Game Components](http://docs.torquepowered.com/torquex/official/content/documentation/TorqueX%20Core/Concepts/Component%20System.html) further enhances understanding of the concept.

For further reading and arguments read the [Wikipedia article on component based software engineering](https://en.wikipedia.org/wiki/Component-based_software_engineering). As a matter of fact, the Objective-C language was invented to be able to create re-usable software components!

Scott Bilas’ GDC 2002 talk about [A Data-Driven Game Object System (PDF)](http://www.learn-cocos2d.com/files/2002/gdc_san_jose/game_objects_slides_with_notes.pdf) as used by [Dungeon Siege](http://www.gaspowered.com/dsuniverse/) contains more pointers on why inheritance fails for game developers and what the advantages (but also some caveats) are with component-based game engines. The talk may be old but it’s still as valid today as it was back then. In fact, in 2002 i started working on [SpellForce](http://store.steampowered.com/app/39540/) which already had a component system built into its core, called Aspects, Abilities and Spells. It allowed us to enter all the game data in the database and programmers only needed to write the generic code that dealt with the data, as well as setting certain limits and validity checks (eg. you couldn’t use a damaging spell on yourself but if you wanted to you could target enemies with your heal spell, or have archers shoot buildings … errm).

During GDC 2009 a similar presentation was held by Radical Entertainment’s Marcin Chady. The talk was called [Theory and Practice of Game Object Component Architecture (PPT)](http://cmpmedia.vo.llnwd.net/o1/vault/gdccanada09/slides/marcinchadyGDCCanada.ppt).

Mick West wrote an article [Refactoring Game Entities with Components](http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/) which describes the challenges and benefits of changing the Tony Hawk codebase from an inheritance model to a game component system.

A somewhat more advanced read on component use is a collaborative paper called [Dynamic Game Object Component System for Mutable Behavior Characters](http://www.josericardojunior.com/docs/DGOCSMBC_SBG08_1.pdf) which talks about components in context of [finite state machines](https://en.wikipedia.org/wiki/Finite_state_machine) and NPC behaviors with a rule-based activation system.

The Game Architect blog calls it an [Anatomy of Despair](http://gamearchitect.net/2008/06/01/an-anatomy-of-despair-aggregation-over-inheritance/) and sums up very good what the cons of inheritance-based class design is and how composition solves them.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[CCSprite](http://www.learn-cocos2d.com/tag/ccsprite/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[cocos2d-iphone](http://www.learn-cocos2d.com/tag/cocos2d-iphone/)•

[component](http://www.learn-cocos2d.com/tag/component/)•

[component based software](http://www.learn-cocos2d.com/tag/component-based-software/)•

[component system](http://www.learn-cocos2d.com/tag/component-system/)•

[Components](http://www.learn-cocos2d.com/tag/components/)•

[documentation](http://www.learn-cocos2d.com/tag/documentation/)•

[Dungeon Siege](http://www.learn-cocos2d.com/tag/dungeon-siege/)•

[game components](http://www.learn-cocos2d.com/tag/game-components/)•

[game data](http://www.learn-cocos2d.com/tag/game-data/)•

[game developers](http://www.learn-cocos2d.com/tag/game-developers/)•

[game engine](http://www.learn-cocos2d.com/tag/game-engine/)•

[game engines](http://www.learn-cocos2d.com/tag/game-engines/)•

[game object](http://www.learn-cocos2d.com/tag/game-object/)•

[game objects](http://www.learn-cocos2d.com/tag/game-objects/)•

[game programming](http://www.learn-cocos2d.com/tag/game-programming/)•

[GDC](http://www.learn-cocos2d.com/tag/gdc/)•

[gdc 2002](http://www.learn-cocos2d.com/tag/gdc-2002/)•

[generic code](http://www.learn-cocos2d.com/tag/generic-code/)•

[inheritance](http://www.learn-cocos2d.com/tag/inheritance/)•

[inheritance hierarchy](http://www.learn-cocos2d.com/tag/inheritance-hierarchy/)•

[Objective-C](http://www.learn-cocos2d.com/tag/objective-c/)•

[Programming](http://www.learn-cocos2d.com/tag/programming/)•

[PushButton](http://www.learn-cocos2d.com/tag/pushbutton/)•

[scott bilas](http://www.learn-cocos2d.com/tag/scott-bilas/)•

[spellforce](http://www.learn-cocos2d.com/tag/spellforce/)•

[XNA](http://www.learn-cocos2d.com/tag/xna/)

great vid and post. far better layout for certain classes IMO

Inheritance is very good for bureaucratic Java stuffs (:

[…] Iterheim over at learn cocos2d posted a good article discussing the benefits of composition in games, and he linked the “Understanding Components” QuickTalk I did for PushButton […]

Could you do a dedicated tutorial (perhaps including video) of how to do Bitmap fonts, and how to integrate them with UILabels, things of that nature?

One more thing, in some games cash is represented in a shorthand, so instead of $1,000,000 you get $1m, (other examples include 0.25k, 0.75k, 250k, etc) (similar to the way Sensible World of Soccer used to do it), do you have a knowledge base on how to best accomplish this?

Thanks

[…] Objective C is a really nice language to extend because of its easy to use class categories and lack of multiple inheritance. So, when you find yourself challenged with something that goes beyond the game engine, just create […]

Hi,

I am desperate to get this book as I see there are so many interesting topics about cocos2d. When i checked on Amazon about this book it shows that ” this book has not been released yet”. So I am confused that book has released it in stores or do i need to wait a long for this amazing book.

The book is available as Alpha eBook directly from Apress:

http://apress.com/book/view/1430233036

[…] by Ben Garney on June 12, 2010 Steffen Iterheim over at learn cocos2d posted a good article discussing the benefits of composition in games, and he linked the “Understanding Components” QuickTalk I did for PushButton […]

[…] MVC pattern is somewhat similar to a game object component system that I described here. For both systems, the general idea is not to subclass CCSprite and put your game logic in there. […]

[…] You did learn OOP and inheritance. Be carefull inheritance can be evil if abused see why: Prefer Composition over Inheritance […]

Been putting together a really light component framework for Cocos2D.

Here is the blog post: http://bit.ly/hQFdii

Hey Steffen,

I’ve been introduced to constructing game objects using composition through your book, great work by the way!

What is interesting to me at this moment, is whether there is a middleware or game engine out there, that is targeted to work with entities and components out of the box, and give the developer features like Cocos2d

Regards.

Unity is built on a component system. I think Torque uses it too. Not sure about Sparrow Framework, it’s very cleanly designed and it supports a code extension system so I bet it uses some kind of composition. That’s the engine that comes closest to cocos2d.

thanks a lot, I take a look at Sparrow

[…] not inherit from the other. A good rule of thumb, no matter what you’re programming, is to prefer composition to inheritance, so let’s do […]

[…] Coming back to the XCode side I also took a long hard look at the code design. I habitually think “inheritance” from many years of “normal” software development and these links opened my eyes to looking at “component” based gameobjects. They apparently refactored the Tony Hawk series with this pattern to great effect (see link in article): http://www.learn-cocos2d.com/2010/06/prefer-composition-inheritance/ […]

[…] about it and began to read reading everything I could find including this great blog post over at http://www.learn-cocos2d.com, it also has a link to lots of talks and papers on the subject, which I have mostly added […]

[…] about it and began to read reading everything I could find including this great blog post over at www.learn-cocos2d.com, it also has a link to lots of talks and papers on the subject, which I have mostly added […]