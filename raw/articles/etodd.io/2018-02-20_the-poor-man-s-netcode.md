---
title: The Poor Man's Netcode
url: https://etodd.io/2018/02/20/poor-mans-netcode/
published: '2018-02-20'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# The Poor Man's Netcode

The more you know about a given topic, the more you realize that no one knows anything.

For some reason (why God, why?) my topic of choice is game development. Everyone in that field agrees: don't add networked multiplayer to an existing game, you drunken clown.

Well, I did it anyway because I hate myself. Somehow it turned out great. None of us know anything.

## Problem #1: assets

My first question was: how do I tell a client to use such-and-such mesh to render an object? Serialize the whole mesh? Nah, they already have it on disk. Send its filename? Nah, that's inefficient and insecure. Okay, just a string identifier then?

Fortunately, before I had time to implement any of my own terrible ideas, I watched a talk from Mike Acton where he mentions the danger of "lazy decision-making". One of his points was: strings let you lazily ignore decisions until runtime, when it's too late to fix.

If I rename a texture, I don't want to get a bug report from a player with a screenshot like this:

![](../../assets/344a002d06465c4e.jpg)

I had never thought about how powerful and complex strings are. Half the field of computer science deals with strings and what they can do. They usually require a heap allocation, or something even more complex like ropes and interning. I usually don't bother to limit their length, so a single string expands the possibility space to infinity, destroying whatever limited ability I had to predict runtime behavior.

And here I am using these complex beasts to *identify objects*.
Heck, I've even used strings to access object properties. What madness!

Long story short, I cultivated a firm conviction to avoid strings where possible. I wrote a pre-processor that outputs header files like this at build time:

```
namespace Asset
{
namespace Mesh
{
const int count = 3;
const AssetID player = 0;
const AssetID enemy = 1;
const AssetID projectile = 2;
}
}
```


So I can reference meshes like this:

`renderer->mesh = Asset::Mesh::player;`


If I rename a mesh, the compiler makes it my problem instead of some poor player's problem. That's good!

The bad news is, I still have to interact with the file system, which requires the use of strings. The good news is the pre-processor can save the day.

```
const char* Asset::Mesh::filenames[] =
{
"assets/player.msh",
"assets/enemy.msh",
"assets/projectile.msh",
0,
};
```


With all this in place, I can easily send assets across the network. They're just numbers! I can even verify them.

```
if (mesh < 0 || mesh >= Asset::Mesh::count)
net_error(); // just what are you trying to pull, buddy?
```


## Problem #2: object references

My next question was: how do I tell a client to please move/delete/frobnicate "that one object from before, you know the one". Once again, I was lucky enough to hear from smart people before I could shoot myself in the foot.

From the start, I knew I needed a bunch of lists of different kinds of objects, like this:

```
Array<Turret> Turret::list;
Array<Projectile> Projectile::list;
Array<Avatar> Avatar::list;
```


Let's say I want to reference the first object in the Avatar list, even without networking, just on our local machine. My first idea is to just use a pointer:

```
Avatar* avatar;
avatar = &Avatar::list[0];
```


This introduces a ton of non-obvious problems. First, I'm compiling for a 64 bit architecture, which means that pointer takes up 8 whole bytes of memory, even though most of it is probably zeroes. And memory is the number one performance bottleneck in games.

Second, if I add enough objects to the array, it will get reallocated to a different place in memory, and the pointer will point to garbage.

Okay, fine. I'll use an ID instead.

```
template<typename Type> struct Ref
{
short id;
inline Type* ref()
{
return &Type::list[id];
}
// overloaded "=" operator omitted
Ref<Avatar> avatar = &Avatar::list[0];
avatar.ref()->frobnicate();
```


Second problem: if I remove that Avatar from the list, some other Avatar will get moved into its place without me knowing. The program will continue, blissfully and silently screwing things up, until some player sends a bug report that the game is "acting weird". I much prefer the program to explode instantly so I at least get a crash dump with a line number.

Okay, fine. Instead of actually removing the avatar, I'll put a revision number on it:

```
struct Avatar
{
short revision;
};
template<typename Type> struct Ref
{
short id;
short revision;
inline Type* ref()
{
Type* t = &Type::list[id];
return t->revision == revision ? t : nullptr;
}
};
```


Instead of actually deleting the avatar, I'll mark it dead and increment the revision number. Now anything trying to access it will give a null pointer exception. And serializing a reference across the network is just a matter of sending two easily verifiable numbers.

## Problem #3: delta compression

If I had to cut this article down to one line, it would just be a link to Glenn Fiedler's blog.

Which by the way is here: [gafferongames.com](https://gafferongames.com/)

As I set out to implement my own version of Glenn's netcode, I read [this article](https://gafferongames.com/post/snapshot_compression/),
which details one of the biggest challenges of multiplayer games.
Namely, if you just blast the entire world state across the network 60 times a second, you could gobble up 17 mbps of bandwidth.
*Per client.*

Delta compression is one of the best ways to cut down bandwidth usage. If a client already knows where an object is, and it hasn't moved, then I don't need to send its position again.

This can be tricky to get right.

The first part is the trickiest: does the client really know where the object is? Just because I sent the position doesn't mean the client actually received it. The client might send an acknowledgement back that says "hey I received packet #218, but that was 0.5 seconds ago and I haven't gotten anything since."

So to send a new packet to that client, I have to remember what the world looked like when I sent out packet #218, and delta compress the new packet against that. Another client might have received everything up to packet #224, so I can delta compress the new packet differently for them. Point is, we need to store a whole bunch of separate copies of the entire world.

Someone on Reddit asked "isn't that a huge memory hog"?

No, it is not.

Actually I store *255* world copies in memory. All in a single giant array.
Not only that, but each copy has enough room for the maximum number of objects (2048) even if only 2 objects are active.

If you store an object's state as a position and orientation, that's 7 floats. 3 for XYZ coordinates and 4 for a quaternion. Each float takes 4 bytes. My game supports up to 2048 objects. 7 floats * 4 bytes * 2048 objects * 255 copies = ...

14 MB. That's like, half of one texture these days.

I can see myself writing this system five years ago in C#. I would start off immediately worried about memory usage, just like that Redditor, without stopping to think about the actual data involved. I would write some unnecessary, crazy fancy, bug-ridden compression system.

Taking a second to stop and think about actual data like this is called *Data-Oriented Design*.
When I talk to people about DOD, many immediately say,
"Woah, that's really low-level. I guess you want to wring out every last bit of performance. I don't have time for that. Anyway, my code runs fine."
Let's break down the assumptions in this statement.

**Assumption 1: "That's really low-level".**

Look, I multiplied four numbers together. It's not rocket science.

**Assumption 2: "You sacrifice readability and simplicity for performance."**

Let's picture two different solutions to this netcode problem. For clarity, let's pretend we only need 3 world copies, each containing up to 2 objects.

Here's the solution I just described. Everything is statically allocated in the [.bss segment](https://en.wikipedia.org/wiki/.bss). It never moves around. Everything is the same size. No pointers at all.

![](../../assets/58adb8937bc0c997.png)

Here's the idiomatic C# solution. Everything is scattered randomly throughout the heap. Things can get reallocated or moved right in the middle of a frame. The array is jagged. 64-bit pointers all over the place.

![](../../assets/92665445f873089e.png)

Which is simpler?

The second diagram is actually far from exhaustive. C#-land is a lot more complex in reality. Check the comments and you'll probably find someone correcting me about how C# actually works.

But that's my point. With my solution, I can easily construct a "good enough" mental model to understand what's actually happening on the machine. I've barely scratched the surface with the C# solution. I have no idea how it will behave at runtime.

**Assumption 3: "Performance is the only reason you would code like this."**

To me, performance is a nice side benefit of data-oriented design. The main benefit is clarity of thought. Five years ago, when I sat down to solve a problem, my first thought was not about the problem itself, but how to shoehorn it into classes and interfaces.

I witnessed this analysis paralysis first-hand at a game jam recently.
My friend got stuck designing a grid for a [2048-like game](https://tilerisers.etodd.io/).
He couldn't figure out if each number was an object, or if each grid cell was an object, or both.
I said, "the grid is an array of numbers. Each operation is a function that mutates the grid."
Suddenly everything became crystal clear to him.

**Assumption 4: "My code runs fine".**

Again, performance is not the main concern, but it's important. The whole world switched from Firefox to Chrome because of it.

Try this experiment: open up calc.exe. Now copy a 100 MB file from one folder to another.

![](../../assets/70e05278114b1b88.png)

I don't know what calc.exe is doing during that 300ms eternity, but you can draw your own conclusions from my two minutes of research: calc.exe actually launches a process called Calculator.exe, and one of the command line arguments is called "-ServerName".

Does calc.exe "run fine"?
Did throwing a server in simplify things at all, or is it just slower *and* more complex?

I don't want to get side-tracked. The point is, I want to think about the actual problem and the data involved, not about classes and interfaces. Most of the arguments against this mindset amount to "it's different than what I know".

## Problem #4: lag

I now hand-wave us through to the part of the story where the netcode is somewhat operational.

Right off the bat I ran into problems dealing with network lag. Games need to respond to players immediately, even if it takes 150ms to get a packet from the server. Projectiles were particularly useless under laggy network conditions. They were impossible to aim.

I decided to re-use those 14 MB of world copies. When the server receives a command to fire a projectile, it steps the world back 150ms to the way the world appeared to the player when they hit the fire button. Then it simulates the projectile and steps the world forward until it's up to date with the present. That's where it creates the projectile.

I ended up having the client create a fake projectile immediately, then as soon as it hears back from the server that the projectile was created, it deletes the fake and replaces it with the real thing. If all goes well, they should be in the same place due to the server's timey-wimey magic.

Here it is in action. The fake projectile appears immediately but goes right through the wall. The server receives the message and fast-forwards the projectile straight to the part where it hits the wall. 150ms later the client gets the packet and sees the impact particle effect.

The problem with netcode is, each mechanic requires a different approach to lag compensation. For example, my game has an "active armor" ability. If players react quick enough, they can reflect damage back at enemies.

This breaks down in high lag scenarios. By the time the player sees the projectile hitting their character, the server has already registered the hit 100ms ago. The packet just hasn't made it to the client yet. This means you have to anticipate incoming damage and react long before it hits. Notice in the gif above how early I had to hit the button.

To correct this, the server implements something I call "damage buffering". Instead of applying damage instantly, the server puts the damage into a buffer for 100ms, or whatever the round-trip time is to the client. At the end of that time, it either applies the damage, or if the player reacted, reflects it back.

Here it is in action. You can see the 200ms delay between the projectile hitting me and the damage actually being applied.

Here's another example. In my game, players can launch themselves at enemies. Enemies die instantly to perfect shots, but they deflect glancing blows and send you flying like this:

Which direction should the player bounce? The client has to simulate the bounce before the server knows about it. The server and client need to agree which direction to bounce or they'll get out of sync, and they have no time to communicate beforehand.

At first I tried quantizing the collision vector so that there were only six possible directions. This made it more likely that the client and server would choose the same direction, but it didn't guarantee anything.

Finally I implemented another buffer system. Both client and server, when they detect a hit, enter a "buffer" state where the player sits and waits for the remote host to confirm the hit. To minimize jankiness, the server always defers to the client as to which direction to bounce. If the client never acknowledges the hit, the server acts like nothing happened and continues the player on their original course, fast-forwarding them to make up for the time they sat still waiting for confirmation.

## Problem #5: jitter

My server sends out packets 60 times per second. What about players whose computers run faster than that? They'll see jittery animation.

Interpolation is the industry-standard solution. Instead of immediately applying position data received from the server, you buffer it a little bit, then you blend smoothly between whatever data that you have.

In my previous attempt at networked multiplayer, I tried to have each object keep track of its position data and smooth itself out. I ended up getting confused and it never worked well.

This time, since I could already easily store the entire world state in a struct, I was able to write just two functions to make it work. One function takes two world states and blends them together. Another function takes a world state and applies it to the game.

How big should the buffer delay be?
I originally used a constant until I watched [a video from the Overwatch devs](https://www.youtube.com/watch?v=vTH2ZPgYujQ) where they mention adaptive interpolation delay.
The buffer delay should smooth out not only the framerate from the server, but also any variance in packet delivery time.

This was an easy win. Clients start out with a short interpolation delay, and any time they're missing a packet to interpolate toward, they increase their "lag score". Once it crosses a certain threshold, they tell the server to switch them to a higher interpolation delay.

Of course, automated systems like this often act against the user's wishes, so it's important to add switches and knobs to the algorithm!

![](../../assets/41f0ffc845dbc208.gif)

## Problem #6: joining servers mid-match

Wait, I already have a way to serialize the entire game state. What's the hold up?

Turns out, it takes more than one packet to serialize a fresh game state from scratch. And each packet may take multiple attempts to make it to the client. It may take a few hundred milliseconds to get the full state, and as we've seen already, that's an eternity. If the game is already in progress, that's enough time to send 20 packets' worth of new messages, which the client is not ready to process because it hasn't loaded yet.

The solution is—you guessed it—another buffer.

I changed the messaging system to support two separate streams of messages in the same packet. The first stream contains the map data, which is processed as soon as it comes in.

The second stream is just the usual fire-hose of game messages that come in while the client is loading. The client buffers these messages until it's done loading, then processes them all until it's caught up.

## Problem #7: cross-cutting concerns

This next part may be the most controversial.

Remember that bit of gamedev wisdom from the beginning? "don't add networked multiplayer to an existing game"?

Well, most of the netcode in this game is literally tacked on. It lives in its own 5000-line source file. It reaches into the game, pokes stuff into memory, and the game renders it.

Just listen a second before stoning me. Is it better to group all network code in one place, or spread it out inside each game object?

I think both approaches have advantages and disadvantages. In fact, I use both approaches in different parts of the game, for various reasons human and technical.

But some design paradigms (*cough* OOP) leave no room for you to make this decision. Of course you put the netcode inside the object! Its data is private, so you'll have to write an interface to access it anyway. Might as well put all the smarts in there too.

## Conclusion

I'm not saying you should write netcode like I do; only that this approach has worked for me so far.
[Read the code and judge for yourself.](https://github.com/etodd/deceiver/blob/master/src/net.cpp)

There is an objectively optimal approach for each use case, although people may disagree on which one it is. You should be free to choose based on actual constraints rather than arbitrary ones set forth by some paradigm.

Thanks for reading. DECEIVER is launching on Kickstarter soon. [Sign up to play the demo here!](https://deceivergame.com)