---
title: '"But How Do I Actually Start?" Making Games on Your Own as an Engineer'
url: https://blog.eyas.sh/2021/02/unity-for-engineers-pt11-development-process/
author: Eyas Sharaiha
published: '2021-02-21'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

In the ** Unity for Software Engineers**
(now updated and

[available as a book](https://leanpub.com/unity-for-engineers)), series, I give an accelerated introduction to game development in Unity.

[Subscribers](http://eepurl.com/gVgusL)have been following this series over the past few months, often suggesting areas to cover or elaborate on. A few months ago, a reader—also a software engineer—reached out to me (lightly edited, emphasis mine):


The biggest unknown for me is: How do I start?What does the process of creating a game look like? Should I build the scenes first? Should I design the gameplay mechanics first? With business software, it’s much more familiar. It’s easy to think, “Well, okay, I need to write the DAO or controller, etc.” But with games, I’m lost.

While there is no single correct answer, we can still make some distinctions
that can help get us oriented. The answer will also undoubtedly depend on *who*
is doing the development: an individual, small indie team, or larger studio? If
an individual, the answer will also depend on their primary skillset: a
developer, artist, or designer?

Here, I’ll give heuristics especially helpful for individual Software Engineers building a game on their own as a side project, hobby, or proof-of-concept.

![Scrum board, at an office](../../assets/948df805b194b5e0.img)

Photo by İrfan Simsar, [via unsplash](https://unsplash.com/photos/wxWulfjN-G0).

## Questions you should ask yourself

Before we start, here are some questions you should ask yourself.

### Do you know *what* you’re building?

Do you know what your game is about? Do you have a sense of what game mechanics your game will have? Do you know what genre, controls, and themes this game will have?

If *yes*, you’re ready to decide ** where to start coding**.
Otherwise, you have a few more questions to ask yourself.

### Do you *want* to know what you’re building?

It’s totally fine not to have a project in mind! Maybe you’re prototyping. Perhaps you’re throwing a bunch of mini-games on the wall and seeing what sticks. Or you’re looking for inspiration and trying to implement random mechanics to see what feels fun.

**If you’re hoping to begin working on a specific, cohesive game**, you will
likely want to know what you’re building. Consider brainstorming and sketching
out an informal
[game design document](https://en.wikipedia.org/wiki/Game_design_document).
There are
[plenty of templates](https://www.google.com/search?q=game+design+document+template)
of various levels of detail you could decide to use. Especially as a software
engineer toying with abstract ideas in my brain, I’ll start with a super
high-level GDD, covering the feel, themes, genre, and mechanics of the game I
have in mind. Maybe a few pictures or sketches for inspiration, and that’s it.
The key part of this exercise will be the list of mechanics I’m working on.

**If you want to prototype and experiment**, you should already have a vague
sense of 1-2 mechanics that could be fun: Maybe unusual movement or a different
control scheme. It could be a traditional mechanic that you’re wondering how to
implement. For instance, I might decide to build a 3rd Person character and
camera controller to see the “feel” of it, experiment with it a tiny bit, and do
something smooth and polish that I feel good about. I might end up keeping that
code in my back pocket for later, or I might use play-through sessions with that
controller to move around a scene, add a few assets, and use that as a starting
place to see the “feel” various mechanics and designs.

## I know the mechanics I care about. Now what?

![Spiral graph showing a representation of iterative development, between three axes: Plan, Build, and Test.](../../assets/7641c8024e1bfe9b.img)

By Dave Gray, [via Flickr](https://www.flickr.com/photos/davegray/6865783267).
[CC BY-ND 2.0](https://creativecommons.org/licenses/by-nd/2.0/).

The goal of many iterative software development models is to de-risk software
development. You do that by failing fast and getting feedback early. In game
development, the primary metric for success is a feeling: the game should be
fun. So, when deciding what to start with when working on a game, one good
question to ask is: *“How can I see if this game is fun as soon as possible?”*
or *“How can I implement the ‘fun’ part of the game ASAP?”*

One way to do that is to look at a game’s mechanics and implement them in some
order. The advice that resonates with me is implementing game mechanics in order
of what the most *“core”* mechanic first.

Let’s take [Strikers 1945](https://en.wikipedia.org/wiki/Strikers_1945)—the
plane shooting game—as an example. Here’s my attempt at writing its main
mechanics in descending order of importance:

- Movement: Navigate a vertically scrolling world
- Obstacles & Dodging: Player can collide with stationary obstacles and debris
- Shooting: Player can shoot straight ahead to defeat obstacles
- Enemies: Enemies are moving obstacles that can shoot back
- Player Health: A player can take a finite number of hits before losing the game
- Enemy Health: Some enemies take multiple shots to destroy
- Boosts: The player can pick up boosts that improve health, shooting, etc.

… and so on.

If I’m trying to develop *1945* from scratch, I will implement that list in that
order. The game’s mechanics build on each other, so I can only tell if shooting
is “fun” is if I can move around the screen and if there are obstacles I’m
trying to clear (otherwise, there’s no urgency to just pressing *Space* and
seeing projectiles coming out of a plane).

In simpler games, we might order our mechanics so that every new feature adds to a game’s feel. So, with every new mechanic you add, you can play the game and tell if it’s adding what you hope for it to add.

In more complex games, some of the “core” mechanics might be too ‘standard’ to
be “risky” *per se*, but you’ll still need the core mechanics implemented to
assess how fun the other mechanics are. You might choose to use a simpler
throwaway implementation, like a few lines of input-handling code and Unity’s
`CharacterController`

component. You’ll want your core mechanics just smooth
enough that they don’t ruin the fun of the things you’ll layer on top of it.
Another approach here is to use the asset store. I’ve previously mentioned the
[Ultimate FPS (UFPS)](https://assetstore.unity.com/packages/tools/game-toolkits/ufps-ultimate-fps-106748?aid=1011leWs6)
asset, which you might choose to use when building an FPS game, and move on to
implementing the combat or some more unique (but still “core” feature of the
gameplay first).

## So I picked a mechanic, but where do I start programming *within* this mechanic?

*Within* a mechanic, your traditional software engineering intuition becomes
helpful. I hope to spend subsequent articles discussing patterns that are
especially helpful in Unity, but here are a few to consider:

- Work within Unity’s Object-Component paradigm. If you’re adding a new
*capability*to your player, write it as its own component. *Tuning*is especially important in game development; representing a mechanic’s interesting pieces as*configurable*,*serializable*data that can be input to a component will help you playtest and iterate.- Don’t shy away from using plain-old data objects to represent core concepts you’re working with. E.g., health, ammo information, or powerups. Make it serializable if you want it passed around in the editor (or saved to disk across sessions).
- Where pieces of a concept don’t correspond to a single object in a scene, consider using Scriptable Objects to do the jobs. Scriptable Objects introduce many patterns that might help represent what you’re doing.

A few articles I have already written might prove helpful:

[Basic Concepts in Unity for Software Engineers](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts/)[6 Software Practices to Keep, Shed, and Adopt in Unity](https://blog.eyas.sh/2020/10/unity-for-engineers-pt2-six-practices/)[Making Sense of Patterns in Unity’s Adventure Game Tutorial](https://blog.eyas.sh/2020/09/patterns-in-unity-adventure-tutorial/)[Understanding Unity Engine Objects](https://blog.eyas.sh/2020/10/unity-for-engineers-pt5-object-component/)

You might also take a look at patterns covered in:

[Three ways to architect your game with ScriptableObjects](https://unity.com/how-to/architect-game-code-scriptable-objects), via the Unity Blog (based on[his talk](https://www.youtube.com/watch?v=raQ3iHhE_Kk))[Unity Input System, from Basic Principles](https://blog.eyas.sh/2020/10/unity-for-engineers-pt3-input-system/)[Pathfinding with NavMesh](https://blog.eyas.sh/2020/11/unity-for-engineers-pt10-1-pathfinding/)[Physics Raycasting](https://blog.eyas.sh/2020/11/unity-for-engineers-pt10-2-raycasting/)

Once you have a stronger intuition of *how* you can represent different kinds of
data and abstractions, the reader’s initial comment also becomes the answer:

It’s easy to think, “Well, okay, I need to write the DAO or controller, etc.” But with games, I’m lost.


Beyond learning about useful patterns and abstractions in game development to
make development clearer and cleaner, the real takeaway is to decide *what* to
work on at a macro-level.

## How much time should I spend on one mechanic?

As you’re developing a mechanic, what’s a good signal you should move on to the next on your list? Generally, that would be when you’re convinced:

- This mechanic
*feels fun*and*adds to the game*, - Your implementation adds
*just the*of technical debt.[right amount](https://www.e4developer.com/2018/11/21/having-just-the-right-amount-of-technical-debt/)

Traditionally, folks will often say to worry about polish at the later stages of
your development. In his GDC 2016 micro-talk *“Pizzazz First, Polish Later”*,
Lee Perry makes a distinction in this traditional wisdom.

Certain levels of pizzazz might give you a better sense of your mechanic and how
fun it feels. A certain amount of polish or pizzazz can also help you see your
game in a new light and motivate you to keep going.
[Juice](https://gameanalytics.com/blog/squeezing-more-juice-out-of-your-game-design/)
is another form of pizzazz; in certain dull moments of your game design, adding
juice might be a low-cost way to get back into the groove of things.

I hope the conflicting advice shows there isn’t a silver bullet on what to add when. Rather—as in traditional software development—this choice is about a series of trade-offs that depend on the developer, the project, and lots more.

## Are you developing a game or architecting systems?

For some software engineers, we’re often drawn to writing code for systems that
seem *interesting*. Sometimes, I have a game in mind, but *really*, I’m
interested in implementing a cool inventory system where *everything* in the
game is an item. It might not be the core mechanic, but it might be the thing I
want to build.

It’s important to recognize when you’re not building a game but building a
system. If you just quit your job to be a full-time indie gamedev and have a
year of runway before your run out of cash, it is probably a bad idea to start
building a complex inventory system that you don’t even know you’ll need 1.
But if you’re programming on the side to flex your game development muscle, then
go right at it.

I don’t think I’m qualified *per se* to answer the question of “How do I
start?”. Yet, I hope that by showing examples of the conflicting pieces of
advice given to answer this question, you will get a sense of the *parameters*
you can tune when deciding what to try and what will eventually work for you.

If you’ve had success with one paradigm (especially something I haven’t
discussed here), do let me know! Feel free to reach out
[on Twitter](https://twitter.com/EyasSH) or
[directly](https://eyas.sh/#contact).

## Footnotes

-
This is probably an important takeaway that I haven’t made fully implicit so far. What you

*think*is your most unique mechanic might not end up being all that important when you build the whole game. That’s why starting at the ‘core’ and iterating is so useful.[↩](https://blog.eyas.sh#user-content-fnref-1)